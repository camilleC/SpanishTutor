from prometheus_client import Histogram
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple

from spanishtutor.src.core.tutor import SpanishTutor
from spanishtutor.src.core.metrics import (
    chat_turns_total,
    chat_requests_total,
    chat_response_latency,
    llm_error_count
)
from prometheus_fastapi_instrumentator import Instrumentator
import time

app = FastAPI()
instrumentator = Instrumentator().instrument(app).expose(app)

tutor = SpanishTutor()

class ChatRequest(BaseModel):
    message: str
    history: List[Tuple[str, str]]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    chat_requests_total.inc()
    start_time = time.time() # This will work async now.

    try:
        for chunk in tutor.generate_response(request.message, request.history):
            response = chunk
        chat_turns_total.inc()
    except Exception as e:
        llm_error_count.labels(error_type=type(e).__name__).inc() # e is a class, using __name__ gets the string
        raise
    latency = time.time() - start_time
    chat_response_latency.observe(latency)
    return {"reply": response}