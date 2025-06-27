
# 🇪🇸 Spanish Tutor

An AI-powered Spanish language tutor that adapts to your proficiency level using open-source LLMs, local inference, and modern backend tooling.

Built with:
- **Gradio**: Chat-style UI for learner interaction
- **FastAPI**: Production-grade API backend for metrics and future endpoints
- **Ollama**: Local LLM inference with LLaMA models
- **Prometheus + Grafana**: Metrics and observability
- **Docker + Docker Compose**: Easy deployment with a clean microservice architecture

---

## Features

- Interactive, real-time conversation practice
- Adaptive difficulty (A1–C2 proficiency levels)
- English translation for better understanding
- Error correction and feedback
- Tracks active users and chat turns
- Prometheus metrics exposed at `/metrics` (via FastAPI service)
- Grafana dashboard for monitoring usage
- Microservice-ready architecture (UI, API, Metrics separated)

---

## Motivation

This project demonstrates how to deploy a **cost-effective, self-hosted AI tutor** by:
- Using the OpenAI client with a **local Ollama server** to avoid cloud API costs
- Keeping the system **modular and maintainable** for scalability
- Supporting **observability and containerization** for real-world deployments

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

- Gradio UI at: http://localhost:7860  
- FastAPI (metrics endpoint): http://localhost:8000  
- Prometheus at: http://localhost:9090  
- Grafana at: http://localhost:3000  

---

## 📈 Metrics

Prometheus scrapes the FastAPI `/metrics` endpoint.

Exposed metrics include:

- `chat_turns_total`: Counts the number of chat turns
- (More coming soon, e.g., `active_users_total`)

To view:
- Visit http://localhost:8000/metrics
- In Grafana:
  1. Go to http://localhost:3000
  2. Add Prometheus as a data source
  3. Build custom dashboards

---

## Running Tests

```bash
pytest
pytest --cov=src
```

---

## Usage

Start Ollama:

```bash
ollama run llama3
```

Run the system via Docker:

```bash
docker-compose up --build
```

Then open:
- Gradio: http://localhost:7860  
- Prometheus: http://localhost:9090  
- Grafana: http://localhost:3000  

⚠️ If Ollama runs outside Docker, make sure your model client points here:

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
