"""
Tutor module for Spanish language learning.

The reason this setup uses the OpenAI client pointed at a local Ollama server is a practical workaround to avoid paying for API usage on OpenAI's cloud services.
By running the llama model locally via Ollama and configuring the OpenAI client to send requests to this local endpoint, the code:

Uses the same OpenAI SDK interface and code patterns without changes.

Avoids incurring costs associated with calling OpenAI's hosted API.

Maintains flexibility to switch models or endpoints by simply changing the base_url or model name.

So essentially, this approach mimics OpenAI's API locally, allowing one to develop and test against powerful language models without external API charges.

Comments on Exception: In this design, the core logic (generate_response) catches low-level exceptions from the LLM client (like APIConnectionError, RateLimitError) and 
translates them into custom app-specific exceptions (TutorBadRequest, TutorModelUnavailable, etc.). This keeps external dependencies isolated from the FastAPI route, 
which only needs to handle your own exception types and return appropriate HTTP status codes. It makes the system more modular, testable, and easier to maintain or swap out model providers later.
"""

from openai import OpenAI, APIError, APIConnectionError, RateLimitError, BadRequestError
from typing import Generator, List, Tuple, Optional
import logging
import os
from spanishtutor.src.core.metrics import (
    chat_chunks_total,
    llm_error_count
)
from spanishtutor.src.exceptions import (
    TutorBadRequest,
    TutorModelUnavailable,
    TutorInternalError
)

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
current_level = getattr(logging, log_level, logging.INFO)

logging.basicConfig(level=current_level)  # or INFO in production
logger = logging.getLogger(__name__)

class SpanishTutor:
    def __init__(self, model_name: str = "llama3.2"):
        """Initialize the Spanish tutor with the specified model."""
        self.model_name = model_name
        self.llama = OpenAI(
            base_url=os.getenv('LLM_BASE_URL', 'http://host.docker.internal:11434/v1'),
            api_key=os.getenv('LLM_API_KEY', 'ollama')
        )
        self.user_level: Optional[str] = None
        self._setup_system_prompt()

    def _setup_system_prompt(self) -> None:
        """Set up the system prompt for the tutor."""
        self.system_prompt = """You are María, an experienced Spanish language tutor from Madrid.
        Provide engaging and culturally relevant responses in {user_level} level Spanish.
        Include English translations and cultural context when appropriate.
        When correcting mistakes, explain the grammar rules in English.

        Example interactions:

        User: Tell me about Spanish food
        Tutor: ¡La paella es uno de los platos más famosos de España!
        (Paella is one of Spain's most famous dishes! It originated in Valencia and combines rice with seafood or meat.)

        User: How do I say "I'm tired"?
        Tutor: "Estoy cansado" (for men) or "Estoy cansada" (for women).
        Note: In Spanish, adjectives must match the gender of the speaker."""

    def set_level(self, level: str) -> str:
        """Set the user's Spanish proficiency level."""
        self.user_level = level.upper()
        return f"¡Excelente! I'll speak to you in {self.user_level} level Spanish. ¿Qué te gustaría aprender hoy?"

    def format_chat_history(self, history: List[Tuple[str, str]]) -> List[dict]:
        """Format chat history for the LLM."""
        formatted_history = []
        for human, assistant in history:
            formatted_history.extend([
                {"role": "user", "content": human},
                {"role": "assistant", "content": assistant}
            ])
        return formatted_history

    # Even on errors, we `yield` a message — because this is a generator (if yeild is used the whole Fx turns into a generator).
    # Generators can't use `return value`; `yield` sends the error to the caller.
    def generate_response(self, message: str, history: List[Tuple[str, str]]) -> Generator[str, None, None]:
        """Generate a response to the user's message."""
        if not self.user_level:
            yield self.set_level(message)
            return

        current_system_message = self.system_prompt.format(user_level=self.user_level)
        formatted_history = self.format_chat_history(history)
        formatted_history.append({"role": "user", "content": message})
        
        messages = [{"role": "system", "content": current_system_message}] + formatted_history

        try:
            stream = self.llama.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=True
            )

            response = ""
            for chunk in stream:
                # Catch malformed data one chunk at a time.
                try:
                    content = chunk.choices[0].delta.content
                    if content:
                        response += content
                        # yield to emit partial responses as the LLM generates them 
                        chat_chunks_total.inc()
                        yield response
                except (AttributeError, IndexError) as e:
                    logger.error("Malformed chunk received: %s", chunk)
                    llm_error_count.labels(error_type="malformed_chunk").inc()
                    raise TutorInternalError("Received an unexpected response format from the model.")
                    return # is this needed?

        # Exeptions not related to chunks
        except APIConnectionError as e:  # subclass of APIError
            logger.exception("Connection error when calling LLM.")
            llm_error_count.labels(error_type="APIConnectionError").inc()
            raise TutorModelUnavailable(f"Failed to connect to LLM at `{self.model_name}`. Is it running?")

        except RateLimitError as e:  # subclass of APIError
            logger.warning("Rate limited by local LLM API.")
            llm_error_count.labels(error_type="RateLimitError").inc()
            raise TutorModelUnavailable("Too many requests. Please wait a moment and try again.")

        except BadRequestError as e:  # subclass of APIError
            logger.error(f"Bad request: {e}")
            llm_error_count.labels(error_type="BadRequestError").inc()
            raise TutorBadRequest("The request was malformed. Please check your input and try again.")

        except APIError as e:
            logger.exception("OpenAI-style API error")
            llm_error_count.labels(error_type="APIError").inc()
            raise TutorInternalError(f"Model error — {str(e)}")

        except AttributeError as e:
            logger.exception("Client not properly initialized.")
            llm_error_count.labels(error_type="AttributeError").inc()
            raise TutorInternalError("Internal setup issue. Please check if the model client is correctly initialized.")

        except ConnectionError as e:
            logger.exception("Connection to model backend failed.")
            llm_error_count.labels(error_type="ConnectionError").inc()
            raise TutorModelUnavailable(f"Couldn't connect to LLM. Is the `{self.model_name}` model running?")

        except Exception as e:
            logger.exception("Unexpected error during response generation.")
            llm_error_count.labels(error_type="Exception").inc()
            raise TutorInternalError(f"Unexpected error: {str(e)}. Please ensure Ollama is running with the `{self.model_name}` model.")
