
# 🇪🇸 Spanish Tutor

An AI-powered Spanish language tutor that adapts to your proficiency level using open-source LLMs, local inference, and modern backend tooling.

Built with:
- **Gradio**: Chat-style UI for learner interaction
- **FastAPI**: Production-grade web server to host the Gradio app
- **Ollama**: Local LLM inference with LLaMA models
- **Prometheus + Grafana**: Metrics and observability
- **Docker + Docker Compose**: Easy deployment

---

## ✨ Features

- Interactive, real-time conversation practice
- Adaptive difficulty (A1–C2 proficiency levels)
- English translation for better understanding
- Error correction and feedback
- Tracks active users and chat turns
- Prometheus metrics exposed at `/metrics`
- Grafana dashboard for monitoring usage

---

## 🧠 Motivation

This project demonstrates how to deploy a **cost-effective, self-hosted AI tutor** by:
- Using the OpenAI client with a **local Ollama server** to avoid cloud API costs
- Keeping the system **modular** so it can later be upgraded to use frontier models like GPT-4
- Supporting **observability and containerization** for real-world deployments

---

## 📁 Project Structure

```
SpanishTutor/
├── spanishtutor/
│   ├── src/
│   │   ├── main.py         # Core logic
│   │   └── api/app.py      # FastAPI app mounting Gradio
│   └── metrics.py          # Prometheus counters
├── tests/                  # Test suite
├── Dockerfile              # Container build file
├── docker-compose.yml      # Multi-service dev stack
├── requirements.txt
├── setup.py
└── README.md
```

---

## Installation

### Option 1: Local Python (Recommended for Dev)

```bash
# Clone the repository
git clone https://github.com/camilleC/SpanishTutor.git
cd SpanishTutor

# Set up environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Option 2: Docker + Docker Compose

Ensure Docker is installed, then run:

```bash
docker-compose up --build
```

- FastAPI+Gradio app will run on [http://localhost:8000](http://localhost:8000)
- Prometheus at [http://localhost:9090](http://localhost:9090)
- Grafana at [http://localhost:3000](http://localhost:3000)

---

## 📈 Metrics

The app will exposes Prometheus metrics like:

- `app_chat_turns_total` (TODO)
- `app_active_users_total` (TODO)

Visit `/metrics` on FastAPI to see raw output:
```
http://localhost:8000/metrics
```

In Grafana:
1. Open [http://localhost:3000](http://localhost:3000)
2. Add Prometheus as a data source
3. Create dashboards for chat usage and activity

---

##  Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=spanishtutor
```

---

##  Usage

Start Ollama (if not already running):

```bash
ollama run llama3
```

Then run the tutor:

```bash
spanish-tutor
# OR if using Docker Compose
docker-compose up
```

Open your browser:
- Gradio UI: [http://localhost:8000/demo](http://localhost:8000/demo)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- Grafana: [http://localhost:3000](http://localhost:3000)

---

## 🧠 Contributing

1. Fork this repo
2. Create a branch (`feature/my-feature`)
3. Commit your changes
4. Push and open a PR

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for local LLMs
- [Gradio](https://gradio.app) for the user interface
- [FastAPI](https://fastapi.tiangolo.com) for API backend
- [Prometheus](https://prometheus.io) and [Grafana](https://grafana.com) for observability
- Inspired by [Udemy’s LLM Engineering course](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models)

