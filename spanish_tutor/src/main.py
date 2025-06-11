#!/usr/bin/env python
# coding: utf-8

"""
Spanish Language Learning Assistant
An interactive AI-powered Spanish language tutor with cultural context and personalized learning.
"""

import gradio as gr
from typing import List, Tuple
from .tutor import SpanishTutor

class SpanishLearningApp:
    def __init__(self):
        """Initialize the Spanish learning application."""
        self.tutor = SpanishTutor()
        self.setup_interface()

    def setup_interface(self) -> None:
        """Set up the Gradio interface with custom styling."""
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
            examples=[
                "A1 - Beginner          ",
                "A2 - Elementary        ",
                "B1 - Intermediate      ",
                "B2 - Upper Intermediate",
                "C1 - Advanced          "
            ]
        )

    def handle_chat(self, message: str, history: List[Tuple[str, str]]) -> str:
        """Handle chat messages and generate responses."""
        for response in self.tutor.generate_response(message, history):
            yield response

    def launch(self) -> None:
        """Launch the application interface."""
        self.interface.launch(
            share=False,
            server_name="0.0.0.0",
            server_port=7860,
            show_error=True,
            show_api=False,
        )

def main():
    """Launch the Spanish learning application."""
    app = SpanishLearningApp()
    app.launch()

if __name__ == "__main__":
    main() 