# Spanish Tutor

An AI-powered Spanish language tutor that adapts to your proficiency level using the Llama language model.

The OpenAI client is pointed at a local Ollama server. This is a practical workaround to avoid paying for API usage on OpenAI’s cloud services.
By running the llama model locally via Ollama and configuring the OpenAI client to send requests to this local endpoint, the code:

Uses the same OpenAI SDK interface and code patterns without changes.

Avoids incurring costs associated with calling OpenAI’s hosted API.

Maintains flexibility to switch models or endpoints by simply changing the base_url or model name.

So essentially, this approach mimics OpenAI’s API locally, allowing one to develop and test against powerful language models without external API charges.

As the purpose of this demo is to show how to wire up a free LLM that can later be replaced by a frontier model comprehensive tests and error handeling are missing.


## Features

- Interactive conversation-based learning
- Adaptive difficulty levels (A1-C2)
- Real-time feedback and corrections
- English translations for better understanding
- Gradio-based user interface



## Installation

### Option 1: Standard Python (Recommended)

```bash
# Clone the repository
git clone https://github.com/camilleC/SpanishTutor.git
cd SpanishTutor

# Create and activate a virtual environment
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

2. Run the Spanish Tutor from the directory containing setup.py:
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

###
This project was inspired by a course I took on large language models. 
While the structure was based on one of my lessons, I significantly adapted the code, 
model backend, and functionality to create a Spanish language tutor.

Original code: [Course Name or Link, if allowed]