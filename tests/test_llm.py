# tests/test_llm.py
import pytest
from config import get_config, Settings
from llm.rag_pipeline import RAGPipeline
from utils.chunking import chunk_text, extract_text_from_pdf

def test_config_loading():
    """Test that configuration loads correctly."""
    config = get_config()
    assert config.OLLAMA_HOST == "http://host.docker.internal:11434"
    assert config.OLLAMA_MODEL == "gpt-oss:20b"

def test_config_settings():
    """Test Settings class directly."""
    settings = Settings()
    assert settings.OLLAMA_HOST == "http://host.docker.internal:11434"
    assert settings.OLLAMA_MODEL == "gpt-oss:20b"

@pytest.mark.asyncio
async def test_rag_pipeline():
    """Test RAG pipeline functionality."""
    pipeline = RAGPipeline()
    
    # Test adding document
    await pipeline.add_document("This is a test document with some content.")
    
    # Test retrieving context
    result = await pipeline.retrieve_context("test query")
    assert isinstance(result, list)
    assert len(result) == 1  # Should have added one chunk

def test_chunk_text():
    """Test text chunking functionality."""
    text = "A" * 1500  # 1500 character string
    chunks = chunk_text(text, max_chunk_size=1000)
    
    assert len(chunks) == 2
    assert len(chunks[0]) == 1000
    assert len(chunks[1]) == 500

def test_chunk_text_edge_cases():
    """Test edge cases for chunking."""
    # Empty string
    assert chunk_text("") == []
    
    # Single chunk
    text = "Short text"
    chunks = chunk_text(text, max_chunk_size=100)
    assert chunks == ["Short text"]
    
    # Exact multiple
    text = "A" * 1000
    chunks = chunk_text(text, max_chunk_size=1000)
    assert len(chunks) == 1
    assert chunks[0] == text

# Note: extract_text_from_pdf is async and requires a file path
# This would need a mock PDF file for proper testing
# For now, we'll just verify the function exists and has correct signature
def test_extract_text_from_pdf_signature():
    """Test that extract_text_from_pdf function exists with correct signature."""
    import inspect
    sig = inspect.signature(extract_text_from_pdf)
    assert 'pdf_path' in sig.parameters