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
    
    # Initialize variables to track metrics
    total_tokens = 0
    total_duration_ns = 0.0

    # Create a "Thinking" status indicator using cl.Message
    thinking_msg = cl.Message(
        content="⚡ **Thinking...**",
        role="assistant"
    )
    await thinking_msg.send()

    try:
        # Generate response using Ollama
        async for chunk in ollama_client.generate_response(
            prompt=user_message,
            stream=True
        ):
            # Extract text from the structured chunk
            text = chunk.get('text', '')

            # Stream only the text to the UI
            if text:
                await msg.stream_token(text)

            # Accumulate metrics
            if chunk.get('done'):
                metrics = chunk.get('metrics')
                
                # Ensure metrics is not None before accessing it
                if metrics:
                    eval_count = metrics.get('eval_count')
                    # Ollama returns duration in nanoseconds, convert to seconds
                    total_duration_ns = metrics.get('total_duration', 0.0)

                    if eval_count is not None:
                        total_tokens = eval_count
        
        # Update the thinking message to show completion stats or delete it
        await thinking_msg.update()
        
        # Finalize message and optionally display performance summary
        await msg.update()

        # Display a metadata element with performance stats after the chat completes
        if total_duration_ns > 0:
            duration_seconds = total_duration_ns / 1_000_000_000.0
            
            # Update the thinking message to show it's done and add stats
            await thinking_msg.update(
                content=f"⚡ **Response Ready**\n- Tokens Evaluated: {total_tokens}\n- Duration: {duration_seconds:.2f}s"
            )

    except Exception as e:
        # If an error occurs, update the thinking message to show the error
        await thinking_msg.update(content=f"❌ Error: {str(e)}")
        raise e

# Add a simple Streamlit-like interface
@cl.on_chat_start
async def on_chat_start():
    """Initialize chat session with welcome message."""
    await cl.Message(content="Welcome to the Ollama Chat Interface!").send()