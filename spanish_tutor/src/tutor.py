"""
Tutor module for Spanish language learning.
"""

from openai import OpenAI
from typing import Generator, List, Tuple, Optional

class SpanishTutor:
    def __init__(self, model_name: str = "llama3.2"):
        """Initialize the Spanish tutor with the specified model."""
        self.model_name = model_name
        self.llama = OpenAI(
            base_url='http://localhost:11434/v1',
            api_key='ollama'
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
                if chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content
                    yield response
        except Exception as e:
            yield f"Error: {str(e)}. Please ensure Ollama is running with the {self.model_name} model." 