import requests
import gradio as gr
from typing import List, Tuple
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/chat") # default value if I'm not running it via docker compose TODO check if it is correct

LEVELS = [
    "A1 - Beginner",
    "A2 - Elementary",
    "B1 - Intermediate",
    "B2 - Upper Intermediate",
    "C1 - Advanced"
]

class SpanishLearningApp:
    def __init__(self):
        self.setup_gradio()

    def setup_gradio(self) -> None:
        self.interface = gr.ChatInterface(
            fn=self.handle_chat,
            title="Spanish Language Learning Assistant",
            description=(
                "¡Bienvenido! I'm María, your Spanish tutor from Madrid. "
                "Please tell me your Spanish level (A1, A2, B1, B2, C1, C2) by clicking a button below to begin. "
                "I'll help you learn Spanish with cultural context and personalized feedback."
            ),
            theme=gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="blue",
                neutral_hue="slate",
                radius_size="md",
                text_size="md",
            ),
            examples=LEVELS
        )

    def handle_chat(self, message: str, history: List[Tuple[str, str]]) -> str:
        try:
            response = requests.post(API_URL, json={
                "message": message,
                "history": history
            })
            response.raise_for_status()
            return response.json()["reply"]
        except Exception as e:
            return f"Error: {str(e)}"

    def launch(self) -> None:
        self.interface.launch(
            share=False,
            server_name="0.0.0.0",
            server_port=7860,
            show_error=True,
            show_api=False,
        )
