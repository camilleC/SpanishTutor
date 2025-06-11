# Spanish Conversation Tutor

An interactive AI-powered Spanish language tutor that adapts to your proficiency level and provides real-time conversation practice.

## Features

- **Real-time Feedback**: Corrects grammar mistakes and explains corrections in English
- **Bilingual Support**: Provides English translations alongside Spanish responses
- **Interactive Interface**: Clean, user-friendly chat interface built with Gradio
- **Local AI Processing**: Powered by Llama 3.2 running locally via Ollama

## Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Llama 3.2 model pulled in Ollama

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/spanish-tutor.git
cd spanish-tutor
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Start Ollama with Llama 3.2:
```bash
ollama run llama3.2
```

## Usage

1. Run the tutor:
```bash
python spanish_tutor.py
```

2. Open your browser to the provided local URL (typically http://127.0.0.1:7860)

3. Enter your Spanish proficiency level when prompted (A1, A2, B1, B2, C1, or C2)

4. Start conversing! You can:
   - Ask questions in English or Spanish
   - Practice grammar and vocabulary
   - Get immediate feedback on your Spanish

## Technical Details

- Built with Python and Gradio for the user interface
- Uses Llama 3.2 for natural language processing
- Implements streaming responses for real-time interaction
- Maintains conversation history for context-aware responses

## Project Structure

```
Spanish Tutor/
├── README.md
├── requirements.txt
├── spanish_tutor.py
└── .gitignore
```

## Contributing

Feel free to submit issues and enhancement requests!