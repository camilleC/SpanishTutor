from prometheus_client import Histogram
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Tuple

from spanishtutor.src.core.tutor import SpanishTutor
from spanishtutor.src.core.metrics import (
    chat_turns_total,
    chat_requests_total,
    chat_response_latency,
    llm_error_count
)
from spanishtutor.src.exceptions import (
    TutorBadRequest,
    TutorModelUnavailable,
    TutorInternalError
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
    except TutorBadRequest as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except TutorModelUnavailable as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    except TutorInternalError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        llm_error_count.labels(error_type=type(e).__name__).inc()
        raise HTTPException(status_code=500, detail="Unexpected server error.")
    
    latency = time.time() - start_time
    chat_response_latency.observe(latency)
    return {"reply": response}
