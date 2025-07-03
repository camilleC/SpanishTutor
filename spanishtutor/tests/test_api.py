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

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_chat_success(self):
        payload = {"message": "A1", "history": []}
        with patch("spanishtutor.src.core.tutor.SpanishTutor.generate_response", return_value=iter(["Test reply"])):
            response = self.client.post("/chat", json=payload)
            assert response.status_code == 200
            assert "reply" in response.json()

    def test_chat_bad_request(self):
        # Missing 'message' field
        payload = {"history": []}
        response = self.client.post("/chat", json=payload)
        assert response.status_code == 422  # Pydantic validation error

    def test_chat_internal_error(self):
        # Simulate internal error by sending a message that triggers TutorInternalError
        # This requires patching tutor.generate_response to raise TutorInternalError
        from unittest.mock import patch
        from spanishtutor.src.exceptions import TutorInternalError
        with patch("spanishtutor.src.core.tutor.SpanishTutor.generate_response", side_effect=TutorInternalError("Internal error")):
            payload = {"message": "A1", "history": []}
            response = self.client.post("/chat", json=payload)
            assert response.status_code == 500
            assert "Internal error" in response.json()["detail"]

    def test_chat_model_unavailable(self):
        # Simulate model unavailable error
        from unittest.mock import patch
        from spanishtutor.src.exceptions import TutorModelUnavailable
        with patch("spanishtutor.src.core.tutor.SpanishTutor.generate_response", side_effect=TutorModelUnavailable("Model unavailable")):
            payload = {"message": "A1", "history": []}
            response = self.client.post("/chat", json=payload)
            assert response.status_code == 503
            assert "Model unavailable" in response.json()["detail"]

    def test_chat_bad_request_custom(self):
        # Simulate bad request error
        from unittest.mock import patch
        from spanishtutor.src.exceptions import TutorBadRequest
        with patch("spanishtutor.src.core.tutor.SpanishTutor.generate_response", side_effect=TutorBadRequest("Bad request")):
            payload = {"message": "A1", "history": []}
            response = self.client.post("/chat", json=payload)
            assert response.status_code == 400
            assert "Bad request" in response.json()["detail"]

    def test_chat_retry_logic(self):
        # Simulate TutorModelUnavailable for first 2 calls, then success
        payload = {"message": "A1", "history": []}
        call_sequence = [
            TutorModelUnavailable("Model unavailable 1"),
            TutorModelUnavailable("Model unavailable 2"),
            iter(["Recovered reply"])
        ]
        def side_effect(*args, **kwargs):
            result = call_sequence.pop(0)
            if isinstance(result, Exception):
                raise result
            return result
        with patch("spanishtutor.src.core.tutor.SpanishTutor.generate_response", side_effect=side_effect) as mock_gen:
            response = self.client.post("/chat", json=payload)
            assert response.status_code == 200
            assert response.json()["reply"] == "Recovered reply"
            assert mock_gen.call_count == 3

        # Simulate TutorModelUnavailable for all 3 attempts
        payload = {"message": "A1", "history": []}
        with patch("spanishtutor.src.core.tutor.SpanishTutor.generate_response", side_effect=TutorModelUnavailable("Always unavailable")) as mock_gen:
            response = self.client.post("/chat", json=payload)
            assert response.status_code == 503
            assert "Always unavailable" in response.json()["detail"]
            assert mock_gen.call_count == 3

class TestSpanishLearningApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.app = SpanishLearningApp()

    def test_app_initialization(self):
        """Test that the app initializes correctly."""
        self.assertIsNotNone(self.app.interface)

    def test_handle_chat(self):
        """Test the chat handling functionality."""
        # Patch the requests.post method used in handle_chat
        with patch("spanishtutor.src.core.ui.requests.post") as mock_post:
            mock_post.return_value.json.return_value = {"reply": "Test response"}
            mock_post.return_value.raise_for_status = lambda: None
            response = self.app.handle_chat("Test message", [])
            self.assertEqual(response, "Test response")

    def test_handle_chat_error(self):
        """Test error handling in handle_chat when API request fails."""
        with patch("spanishtutor.src.core.ui.requests.post") as mock_post:
            mock_post.side_effect = Exception("Network error")
            response = self.app.handle_chat("Test message", [])
            self.assertIn("Error:", response)

    def test_handle_chat_http_error(self):
        """Test error handling in handle_chat when API returns HTTP error."""
        with patch("spanishtutor.src.core.ui.requests.post") as mock_post:
            mock_post.return_value.raise_for_status.side_effect = Exception("HTTP 500")
            response = self.app.handle_chat("Test message", [])
            self.assertIn("Error:", response)