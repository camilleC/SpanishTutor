"""
Test suite for the Spanish Language Learning Assistant.
"""

import unittest
from unittest.mock import patch, MagicMock
from spanishtutor.src.core.tutor import SpanishTutor
from spanishtutor.src.core.ui import SpanishLearningApp

class TestSpanishTutor(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.tutor = SpanishTutor()

    def test_initial_level_setting(self):
        """Test that the first message sets the user level correctly."""
        # Test with A1 level
        response = next(self.tutor.generate_response("A1", []))
        self.assertIn("A1", response)
        self.assertEqual(self.tutor.user_level, "A1")

        # Reset for next test
        self.tutor.user_level = None

        # Test with B2 level
        response = next(self.tutor.generate_response("B2", []))
        self.assertIn("B2", response)
        self.assertEqual(self.tutor.user_level, "B2")

    @patch('spanishtutor.src.core.tutor.OpenAI')
    def test_chat_response(self, mock_openai):
        """Test chat response generation with mocked OpenAI client."""
        # Set up the mock response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_stream = MagicMock()
        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = "¡Hola! ¿Cómo estás?"
        mock_stream.__iter__.return_value = [mock_chunk]
        mock_client.chat.completions.create.return_value = mock_stream

        # Set user level first
        self.tutor.user_level = "A1"

        # Test chat with a simple message
        response = next(self.tutor.generate_response("¿Cómo estás?", []))
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)



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

