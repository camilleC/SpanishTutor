from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from spanishtutor.src.main import get_interface

# Create the FastAPI app
app = FastAPI()

# Create and mount the Gradio interface
interface = get_interface()
app.mount("/demo", interface.app)

# Health check route
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Prometheus metrics instrumentation
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)