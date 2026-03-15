"""
Chainlit UI components for Ollama chat interface.
"""

import chainlit as cl
from llm.ollama_client import ollama_client

@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle incoming messages from the user.
    
    Args:
        message: Chainlit message object
    """
    # Get the user's message
    user_message = message.content
    
    # Send a response stream
    msg = cl.Message(content="")
    await msg.send()
    
    # Generate response using Ollama
    async for chunk in ollama_client.generate_response(
        prompt=user_message,
        stream=True
    ):
        await msg.stream_token(chunk)
    
    await msg.update()

# Add a simple Streamlit-like interface
@cl.on_chat_start
async def on_chat_start():
    """Initialize chat session with welcome message."""
    await cl.Message(content="Welcome to the Ollama Chat Interface!").send()