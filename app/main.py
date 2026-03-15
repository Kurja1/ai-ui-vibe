# app/main.py
"""
Main entry point for the Ollama chat application.
"""

import chainlit as cl
from llm.ollama_client import OllamaClient
from ui.chat import on_message

# This file serves as the Chainlit entry point
# All other functionality is handled in the imported modules

# The on_message function is automatically registered by Chainlit
# when this module is used as the entry point
