"""
Text processing utilities for handling file attachments.
"""

import PyPDF2
from typing import List

async def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        text = f"Error reading PDF: {str(e)}"
    return text

def chunk_text(text: str, max_chunk_size: int = 1000) -> List[str]:
    """Split text into chunks of specified size."""
    chunks = []
    for i in range(0, len(text), max_chunk_size):
        chunks.append(text[i:i + max_chunk_size])
    return chunks