"""
Chainlit UI components for Ollama chat interface.
"""

import chainlit as cl
from llm.ollama_client import ollama_client
from utils.chunking import extract_text_from_pdf, chunk_text

@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle incoming messages from the user.
    
    Args:
        message: Chainlit message object
    """
    user_message = message.content
    
    # Process attachments if any
    file_content = ""
    for attachment in message.elements or []:
        if attachment.mime == "application/pdf":
            file_content += await extract_text_from_pdf(attachment.path)
        elif attachment.mime.startswith("text/"):
            with open(attachment.path, "r") as f:
                file_content += f.read()
    
    # Combine file content with user message
    full_prompt = file_content + "\n\n" + user_message if file_content != "" else user_message
    
    msg = cl.Message(content="")
    await msg.send()
    
    # Accumulate metrics from the final chunk only (as Ollama provides them then)
    final_metrics = {}

    async for chunk in ollama_client.generate_response(
        prompt=full_prompt,
        stream=True
    ):
        text = chunk.get('text', '')

        if text:
            await msg.stream_token(text)

        # Capture metrics when the generation is done
        if chunk.get('done') and chunk.get('metrics'):
            final_metrics = chunk['metrics']

    await msg.update()

    # Display comprehensive performance stats
    if final_metrics:
        total_tokens = final_metrics.get('eval_count', 0) + final_metrics.get('prompt_eval_count', 0)
        total_duration_ns = final_metrics.get('total_duration', 0)
        
        # Convert nanoseconds to seconds
        duration_seconds = total_duration_ns / 1_000_000_000.0
        
        # Calculate tokens per second if duration > 0
        tokens_per_second = (total_tokens / duration_seconds) if duration_seconds > 0 else 0
        
        stats_content = f"""⚡ **Performance Overview**

        - **Total Tokens**: {total_tokens}
        - Prompt: {final_metrics.get('prompt_eval_count', 0)}
        - Completion: {final_metrics.get('eval_count', 0)}
        - **Latency Breakdown**:
        - Load Time: {(final_metrics.get('load_duration', 0) / 1_000_000_000.0):.2f}s
        - Prompt Eval: {(final_metrics.get('prompt_eval_duration', 0) / 1_000_000_000.0):.2f}s
        - Generation: {(total_duration_ns - final_metrics.get('load_duration', 0) - final_metrics.get('prompt_eval_duration', 0)) / 1_000_000_000.0:.2f}s
        - **Speed**: {tokens_per_second:.2f} tokens/sec
        - **Total Duration**: {duration_seconds:.2f}s"""

        await cl.Message(
            content=stats_content,
            metadata={"type": "performance"}
        ).send()

# Add a simple Streamlit-like interface
@cl.on_chat_start
async def on_chat_start():
    """Initialize chat session with welcome message."""
    await cl.Message(content="Welcome to the Ollama Chat Interface!").send()