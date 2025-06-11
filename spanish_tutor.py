#!/usr/bin/env python
# coding: utf-8

"""
Spanish Conversation Tutor
An interactive AI-powered Spanish language tutor that adapts to your proficiency level.
"""

import os
from openai import OpenAI
import gradio as gr

# Initialize Llama client
llama = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)
MODEL = "llama3.2"

# Global variable to store user level
user_level = None

# System message for the technical tutor
system_message = """You are Carlos a helpful and knowledgeable Spanish tutor. 
Provide clear, concise, and accurate responses in {user_level} level spanish that is clear and easy to understand.
Put english translation next to what you said.
If the user makes a spanish language mistake please correct and and use english to explain why it is wrong.

Here are some examples of how to respond:

User: What is Python?
Tutor: ¡Hola! Python es un lenguaje de programación muy popular y fácil de aprender.
(Hello! Python is a very popular and easy-to-learn programming language.)

User: Can you explain variables?
Tutor: ¡Claro! Las variables son como cajas donde guardamos información.
(Of course! Variables are like boxes where we store information.)

User: ¿Qué es tu color favorito?
Tutor: ¿Cuál es tu color favorito?
("Which is your favorite color?" — This is the natural and grammatically correct way to ask.)"""

def chat(message, history):
    """Handle chat messages and generate responses using Llama."""
    global user_level
    
    # If this is the first message and no level is set, ask for level
    if not user_level and not history:
        user_level = message.upper()
        yield f"¡Perfecto! I'll speak to you in {user_level} level Spanish. ¿Qué te gustaría aprender hoy?"
        return
    
    # Prepare messages for Llama with the current user level
    current_system_message = system_message.format(user_level=user_level)
    
    # Convert history to the format Ollama expects
    formatted_history = []
    for human, assistant in history:
        formatted_history.append({"role": "user", "content": human})
        formatted_history.append({"role": "assistant", "content": assistant})
    
    # Add current message
    formatted_history.append({"role": "user", "content": message})
    
    # Add system message at the start
    messages = [{"role": "system", "content": current_system_message}] + formatted_history

    try:
        # Stream the response from Llama
        stream = llama.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )

        response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
                yield response
    except Exception as e:
        yield f"Error: {str(e)}. Please make sure Ollama is running with llama3.2 model."

def main():
    """Launch the Gradio chat interface."""
    # Create and launch the chat interface
    chat_interface = gr.ChatInterface(
        fn=chat,
        title="Spanish Conversation Tutor",
        description="¡Hola! Please tell me your Spanish level (A1, A2, B1, B2, C1, C2) to begin.",
        theme="soft",
        examples=[
            "A1",
            "A2",
            "B1",
            "B2",
            "C1"
        ]
    )
    chat_interface.launch()

if __name__ == "__main__":
    main() 