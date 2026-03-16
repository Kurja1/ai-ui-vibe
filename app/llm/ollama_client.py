"""
Ollama client for connecting to local Ollama instance and managing LLM interactions.
"""

import os
from typing import Optional, AsyncGenerator
from ollama import AsyncClient
import asyncio

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
    ) -> AsyncGenerator[dict, None]:
        """
        Generate response from Ollama with performance metrics.
        """
        try:
            if stream:
                # Await the generate call to get the async iterator
                async for chunk in await self.client.generate(
                    model=self.model,
                    prompt=prompt,
                    system=system_prompt,
                    stream=True
                ):
                    if chunk.get('done'):
                        yield {
                            'text': chunk.get('response', ''),
                            'metrics': {
                                'eval_count': chunk.get('eval_count'),
                                'eval_duration': chunk.get('eval_duration'),
                                'total_duration': chunk.get('total_duration'),
                                'load_duration': chunk.get('load_duration'),
                                'prompt_eval_count': chunk.get('prompt_eval_count'),
                                'prompt_eval_duration': chunk.get('prompt_eval_duration'),
                            },
                            'done': True
                        }
                    else:
                        yield {
                            'text': chunk.get('response', ''),
                            'metrics': None,
                            'done': False
                        }

            else:
                # Await the generate call for non-streaming mode
                response = await self.client.generate(
                    model=self.model,
                    prompt=prompt,
                    system=system_prompt,
                    stream=False
                )
                
                yield {
                    'text': response.get('response', ''),
                    'metrics': {
                        'eval_count': response.get('eval_count'),
                        'eval_duration': response.get('eval_duration'),
                        'total_duration': response.get('total_duration'),
                        'load_duration': response.get('load_duration'),
                        'prompt_eval_count': response.get('prompt_eval_count'),
                        'prompt_eval_duration': response.get('prompt_eval_duration'),
                    },
                    'done': True
                }
                
        except Exception as e:
            if "failed" in str(e):
                yield {
                    'text': f"Error: Could not connect to Ollama server at {get_config().OLLAMA_HOST}. Please ensure Ollama is running.",
                    'metrics': None,
                    'done': True
                }
            else:
                yield {
                    'text': f"Error generating response: {str(e)}",
                    'metrics': None,
                    'done': True
                }

# Global client instance
ollama_client = OllamaClient()