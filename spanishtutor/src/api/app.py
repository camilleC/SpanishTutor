from fastapi import FastAPI
from spanishtutor.src.main import get_interface

app = FastAPI()

interface = get_interface()
app.mount("/demo", interface.app)

@app.get("/health")
def health_check():
    return {"status": "ok"}