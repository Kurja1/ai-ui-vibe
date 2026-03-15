"""
Ollama client for connecting to local Ollama instance and managing LLM interactions.
"""

import os
from typing import Optional, AsyncGenerator
from ollama import AsyncClient

from config import get_config

class OllamaClient:
    """Async client for interacting with local Ollama instance.

    Provides methods to communicate with local Ollama server for running
    language model inference tasks including streaming responses and
    managing model availability.
    """
    
    def __init__(self):
        config = get_config()
        self.client = AsyncClient(host=config.OLLAMA_HOST)
        self.model = config.OLLAMA_MODEL
    
    async def change_model(self, model_name: str) -> None:
        """Change the active model."""
        self.model = model_name
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        stream: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Generate response from Ollama.
        
        Args:
            prompt: User's message
            system_prompt: System instructions (optional)
            stream: Whether to stream response
            
        Yields:
            Response chunks
        """
        try:
            response = await self.client.generate(
                model=self.model,
                prompt=prompt,
                system=system_prompt,
                stream=stream
            )
            
            if stream:
                async for chunk in response:
                    yield chunk['response']
            else:
                yield response['response']
                
        except Exception as e:
            yield f"Error generating response: {str(e)}"

# Global client instance
ollama_client = OllamaClient()