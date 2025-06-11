import unittest
from unittest.mock import patch, MagicMock
from spanish_tutor import chat, user_level

class TestSpanishTutor(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        global user_level
        user_level = None

    def test_initial_level_setting(self):
        """Test that the first message sets the user level correctly."""
        # Test with A1 level
        response = next(chat("A1", []))
        self.assertIn("A1", response)
        self.assertEqual(user_level, "A1")

        # Reset for next test
        global user_level
        user_level = None

        # Test with B2 level
        response = next(chat("B2", []))
        self.assertIn("B2", response)
        self.assertEqual(user_level, "B2")

    @patch('spanish_tutor.llama.chat.completions.create')
    def test_chat_response(self, mock_create):
        """Test chat response generation with mocked Llama API."""
        # Set up the mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].delta.content = "¡Hola! ¿Cómo estás?"
        mock_create.return_value = [mock_response]

        # Set user level first
        global user_level
        user_level = "A1"

        # Test chat with a simple message
        response = next(chat("¿Cómo estás?", []))
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)

    def test_invalid_level(self):
        """Test handling of invalid level input."""
        response = next(chat("INVALID", []))
        self.assertIn("INVALID", response)
        self.assertEqual(user_level, "INVALID")

    @patch('spanish_tutor.llama.chat.completions.create')
    def test_error_handling(self, mock_create):
        """Test error handling when API call fails."""
        # Mock an API error
        mock_create.side_effect = Exception("API Error")

        # Set user level first
        global user_level
        user_level = "A1"

        # Test error handling
        response = next(chat("Test message", []))
        self.assertIn("Error", response)
        self.assertIn("Ollama", response)

if __name__ == '__main__':
    unittest.main() 