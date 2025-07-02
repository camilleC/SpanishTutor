import unittest
from unittest.mock import patch, MagicMock
from openai import APIConnectionError, RateLimitError, BadRequestError, APIError
from spanishtutor.src.core.tutor import (
    SpanishTutor,
    TutorModelUnavailable,
    TutorBadRequest,
    TutorInternalError
)
from spanishtutor.src.core.ui import SpanishLearningApp
from fastapi.testclient import TestClient
from spanishtutor.src.api.app import app

# Dummy classes used in OpenAI error constructors
class DummyRequest: pass
class DummyResponse:
    request = DummyRequest()
    status_code = 400
    headers = {}
    text = "Bad request"

class TestSpanishTutor(unittest.TestCase):
    def setUp(self):
        """Patch OpenAI and set up tutor before each test."""
        self.openai_patcher = patch('spanishtutor.src.core.tutor.OpenAI')
        self.mock_openai_class = self.openai_patcher.start()
        self.mock_client = MagicMock()
        self.mock_openai_class.return_value = self.mock_client

        self.tutor = SpanishTutor()
        self.tutor.user_level = "A1"

    def tearDown(self):
        """Stop patcher after each test."""
        self.openai_patcher.stop()

    def test_initial_level_setting(self):
        self.tutor.user_level = None
        response = next(self.tutor.generate_response("A2", []))
        self.assertIn("A2", response)
        self.assertEqual(self.tutor.user_level, "A2")

    def test_chat_response(self):
        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = "¡Hola!"
        self.mock_client.chat.completions.create.return_value = [mock_chunk]

        response = next(self.tutor.generate_response("¿Cómo estás?", []))
        self.assertEqual(response, "¡Hola!")

    def test_malformed_chunk_handling(self):
        mock_chunk = MagicMock()
        mock_choice = MagicMock()
        mock_choice.delta = None  # causes AttributeError
        mock_chunk.choices = [mock_choice]
        self.mock_client.chat.completions.create.return_value = [mock_chunk]

        with self.assertRaises(TutorInternalError) as cm:
            list(self.tutor.generate_response("Test", []))
        self.assertIn("unexpected response format", str(cm.exception))

    def test_api_connection_error_handling(self):
        self.mock_client.chat.completions.create.side_effect = APIConnectionError(request=DummyRequest())
        with self.assertRaises(TutorModelUnavailable) as cm:
            next(self.tutor.generate_response("Test", []))
        self.assertIn("connect to LLM", str(cm.exception))

    def test_rate_limit_error_handling(self):
        self.mock_client.chat.completions.create.side_effect = RateLimitError(
            message="rate limit", response=DummyResponse(), body=None
        )
        with self.assertRaises(TutorModelUnavailable) as cm:
            next(self.tutor.generate_response("Test", []))
        self.assertIn("Too many requests", str(cm.exception))

    def test_bad_request_error_handling(self):
        self.mock_client.chat.completions.create.side_effect = BadRequestError(
            message="bad request", response=DummyResponse(), body=None
        )
        with self.assertRaises(TutorBadRequest) as cm:
            next(self.tutor.generate_response("Test", []))
        self.assertIn("malformed", str(cm.exception))

    def test_api_error_handling(self):
        self.mock_client.chat.completions.create.side_effect = APIError(
            "api error", request=DummyRequest(), body=None
        )
        with self.assertRaises(TutorInternalError) as cm:
            next(self.tutor.generate_response("Test", []))
        self.assertIn("Model error", str(cm.exception))

    def test_attribute_error_handling(self):
        self.mock_client.chat.completions.create.side_effect = AttributeError("not initialized")
        with self.assertRaises(TutorInternalError) as cm:
            next(self.tutor.generate_response("Test", []))
        self.assertIn("Internal setup issue", str(cm.exception))

    def test_connection_error_handling(self):
        self.mock_client.chat.completions.create.side_effect = ConnectionError("fail")
        with self.assertRaises(TutorModelUnavailable) as cm:
            next(self.tutor.generate_response("Test", []))
        self.assertIn("connect to LLM", str(cm.exception))

    def test_general_exception_handling(self):
        self.mock_client.chat.completions.create.side_effect = Exception("unexpected")
        with self.assertRaises(TutorInternalError) as cm:
            next(self.tutor.generate_response("Test", []))
        self.assertIn("Unexpected error", str(cm.exception))

    def test_format_chat_history(self):
        history = [("Hello", "Hola"), ("How are you?", "¿Cómo estás?")]
        formatted = self.tutor.format_chat_history(history)
        expected = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hola"},
            {"role": "user", "content": "How are you?"},
            {"role": "assistant", "content": "¿Cómo estás?"}
        ]
        self.assertEqual(formatted, expected)

    def test_set_level(self):
        response = self.tutor.set_level("B2")
        self.assertEqual(self.tutor.user_level, "B2")
        self.assertIn("B2", response)