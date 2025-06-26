from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple

from spanishtutor.src.core.tutor import SpanishTutor
from spanishtutor.src.core.metrics import chat_turns_total
from prometheus_fastapi_instrumentator import Instrumentator

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
    chat_turns_total.inc()
    response = ""
    for chunk in tutor.generate_response(request.message, request.history):
        response = chunk
    return {"reply": response}
