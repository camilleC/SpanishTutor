# Spanish Tutor

An AI-powered Spanish language tutor that adapts to your proficiency level using the Llama language model.

## Features

- Interactive conversation-based learning
- Adaptive difficulty levels (A1-C2)
- Real-time feedback and corrections
- English translations for better understanding
- Beautiful Gradio-based user interface

## Installation

```bash
# Clone the repository
git clone https://github.com/camilleC/SpanishTutor.git
cd SpanishTutor

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Prerequisites

- Python 3.8 or higher
- Ollama with Llama model installed locally
- Internet connection for API calls

## Usage

1. Start the Ollama server with the Llama model:
```bash
ollama run llama3.2
```

2. Run the Spanish Tutor:
```bash
spanish-tutor
```

3. Open your browser and navigate to the provided local URL (typically http://localhost:7860)

## Project Structure

```
spanish_tutor/
├── src/
│   └── main.py          # Main application code
├── tests/
│   └── test_main.py     # Test suite
├── setup.py             # Package configuration
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Development

### Running Tests

```bash
# Run all tests
python -m pytest spanish_tutor/tests/

# Run with coverage report
python -m pytest spanish_tutor/tests/ --cov=spanish_tutor
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Ollama](https://ollama.ai/) for providing the Llama model
- [Gradio](https://gradio.app/) for the beautiful UI framework
- [OpenAI](https://openai.com/) for the API client implementation