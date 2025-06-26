# 🇪🇸 Spanish Tutor

An AI-powered Spanish language tutor that adapts to your proficiency level using open-source LLMs, local inference, and modern backend tooling.

Built with:
- **Gradio**: Chat-style UI for learner interaction
- **FastAPI**: Production-grade web server to host the Gradio app
- **Ollama**: Local LLM inference with LLaMA models
- **Prometheus + Grafana**: Metrics and observability
- **Docker + Docker Compose**: Easy deployment

---

## Features

- Interactive, real-time conversation practice
- Adaptive difficulty (A1–C2 proficiency levels)
- English translation for better understanding
- Error correction and feedback
- Tracks active users and chat turns
- Prometheus metrics exposed at `/metrics`
- Grafana dashboard for monitoring usage

---

## Motivation

This project demonstrates how to deploy a **cost-effective, self-hosted AI tutor** by:
- Using the OpenAI client with a **local Ollama server** to avoid cloud API costs
- Keeping the system **modular** so it can later be upgraded to use frontier models like GPT-4
- Supporting **observability and containerization** for real-world deployments

---

## Project Structure

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

---

## Installation

### Option 1: Local Python (Recommended for Dev)

```bash
git clone https://github.com/camilleC/SpanishTutor.git
cd SpanishTutor
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -e .
```

### Option 2: Docker + Docker Compose

Ensure Docker is installed, then run:

```bash
docker-compose up --build
```

- FastAPI+Gradio app will run on http://localhost:8000
- Prometheus at http://localhost:9090
- Grafana at http://localhost:3000

---

## 📈 Metrics

Exposed Prometheus metrics:

- `app_chat_turns_total`
- `app_active_users_total`

View at: http://localhost:8000/metrics

In Grafana:
1. Open http://localhost:3000
2. Add Prometheus as a data source
3. Create dashboards

---

## Running Tests

```bash
pytest
pytest --cov=spanishtutor
```

---

## Usage

Start Ollama:

```bash
ollama run llama3
```

Run the tutor:

```bash
spanish-tutor
# OR with Docker
docker-compose up
```

Open:
- Gradio: http://localhost:7860 # don't use http in production
- Prometheus: http://localhost:9090 # don't use http in production
- Grafana: http://localhost:3000 # don't use http in production

⚠️ If Ollama is outside Docker, set:
TODO: Eventually put the model inside of docker
```python
base_url = "http://host.docker.internal:11434/v1"
```

---

## Contributing

1. Fork this repo
2. Create a branch (`feature/my-feature`)
3. Commit your changes
4. Push and open a PR

---

## Acknowledgments

- [Ollama](https://ollama.ai)
- [Gradio](https://gradio.app)
- [FastAPI](https://fastapi.tiangolo.com)
- [Prometheus](https://prometheus.io)
- [Grafana](https://grafana.com)