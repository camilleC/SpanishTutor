"""
Test suite for the Spanish Language Learning Assistant.
"""

import unittest
from unittest.mock import patch, MagicMock
from openai import APIConnectionError
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

    @patch('spanishtutor.src.core.tutor.OpenAI')
    def test_malformed_chunk_handling(self, mock_openai):
        """Test handling of malformed chunks from the LLM."""
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_stream = MagicMock()
        
        # Create a malformed chunk that will cause AttributeError when accessing delta.content
        mock_chunk = MagicMock()
        mock_choice = MagicMock()
        mock_choice.delta = None  # This will cause AttributeError when accessing delta.content
        mock_chunk.choices = [mock_choice]
        mock_stream.__iter__.return_value = [mock_chunk]
        mock_client.chat.completions.create.return_value = mock_stream

        self.tutor.user_level = "A1"
        response = next(self.tutor.generate_response("Test message", []))
        self.assertIn("Error: Failed to connect to LLM at `llama3.2`. Is it running?", response)

    @patch('spanishtutor.src.core.tutor.OpenAI')
    def test_connection_error_handling(self, mock_openai):
        """Test handling of connection errors to the LLM backend."""
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = ConnectionError("Connection failed")

        self.tutor.user_level = "A1"
        response = next(self.tutor.generate_response("Test message", []))
        self.assertIn("Error: Failed to connect to LLM", response)

    def test_Attribution_error_handling(self):
        """Test handling of AttributeError when client is not properly initialized."""
        # Directly set the llama client to None to trigger AttributeError
        self.tutor.llama = None

        self.tutor.user_level = "A1"
        response = next(self.tutor.generate_response("Test message", []))
        self.assertIn("Error: Internal setup issue. Please check if the model client is correctly initialized.", response)

    @patch('spanishtutor.src.core.tutor.OpenAI')
    def test_general_exception_handling(self, mock_openai):
        """Test handling of general exceptions."""
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("Unexpected error")

        self.tutor.user_level = "A1"
        response = next(self.tutor.generate_response("Test message", []))
        self.assertIn("Error:", response)

    def test_format_chat_history(self):
        """Test the format_chat_history method."""
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
        """Test the set_level method."""
        response = self.tutor.set_level("B2")
        self.assertEqual(self.tutor.user_level, "B2")
        self.assertIn("B2", response)

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

