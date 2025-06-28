# 🇪🇸 Spanish Tutor

An AI-powered Spanish language tutor that adapts to your proficiency level using open-source LLMs, local inference, and modern backend tooling.

Built with:
- **Gradio**: Chat-style UI served in a standalone service
- **FastAPI**: Production-grade API backend for metrics and chat processing
- **Ollama**: Local LLM inference using LLaMA models
- **Prometheus + Grafana**: Metrics and observability
- **Docker + Docker Compose**: Clean microservice architecture with easy deployment

---

## Features

- Interactive, real-time conversation practice
- Adaptive difficulty (A1–C2 proficiency levels)
- English translation for better understanding
- Prometheus metrics exposed via FastAPI at `/metrics`
- Grafana dashboard for monitoring usage patterns

---

##  Motivation

This project demonstrates how to deploy a **cost-effective, self-hosted LLM model** by:
- Using the OpenAI-compatible client with a **local Ollama server** to avoid cloud API costs
- Keeping the system **modular and extensible** for future integration with other models or services
- Supporting **observability and containerization** for real-world, production-like deployments


##  Installation

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

Services will be available at:
- Gradio UI: [http://localhost:7860](http://localhost:7860)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- Grafana: [http://localhost:3000](http://localhost:3000)

---

## Metrics

FastAPI exposes Prometheus-compatible metrics such as:

- `chat_turns_total`

To view:
- Visit [http://localhost:8000/metrics](http://localhost:9090/metrics)
- Or in Grafana:
  1. Open [http://localhost:3000](http://localhost:3000)
  2. Add Prometheus as a data source
  3. Build dashboards from the exposed metrics

---

## Running Tests

```bash
pytest spanishtutor/tests/
pytest --cov=spanishtutor
```

---

## Usage

Start Ollama (if not already running):

```bash
ollama run llama3.2
```

Then run the full system:

```bash
docker-compose up --build -d
```

Open your browser:
- Gradio UI: [http://localhost:7860](http://localhost:7860)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- Grafana: [http://localhost:3000](http://localhost:3000)

---

## Contributing

1. Fork this repo
2. Create a branch (`feature/my-feature`)
3. Commit your changes
4. Push and open a PR

---

## Acknowledgments

- [Ollama](https://ollama.ai) for local LLMs
- [Gradio](https://gradio.app) for the chat UI
- [FastAPI](https://fastapi.tiangolo.com) for the backend API
- [Prometheus](https://prometheus.io) and [Grafana](https://grafana.com) for observability