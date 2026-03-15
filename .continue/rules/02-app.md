---
description: "Application logic rules"
globs: ["app/**/*"]
---
# app/ context – application code

- All modules in `app/` should expose a clear public API.  
- `main.py` is the Chainlit entry point; keep it lightweight.  
- `config.py` loads environment variables; never hard‑code secrets.  
- LLM wrappers (`ollama_client.py`, `rag_pipeline.py`) should be stateless or use dependency injection.  
- UI components (`chat.py`) should register Chainlit event handlers only.  
- Keep business logic out of UI files.  
- Use type hints for all public functions.  
- Add docstrings that explain purpose, parameters, and return values.  
- Follow PEP‑8 formatting; run `ruff` before committing.