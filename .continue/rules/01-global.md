---
description: "General project rules"
globs: "**/*"
---
# Root context – general project rules

- The repository follows a **Docker‑first** workflow.  
- All code lives under `app/`.  
- Use **Python 3.11+** with type hints.  
- Follow **SOLID** principles; keep modules small and focused.  
- All public functions should have a docstring.  
- Tests are in `tests/` and use `pytest`.  
- Configuration is loaded from `config.py` and `.env`.  
- When adding new files, place them in the appropriate sub‑folder and update imports accordingly.  
- For any LLM‑related logic, use the `app.llm` package.  
- UI logic lives in `app.ui`.  
- Evaluation scripts are under `app.evaluation`.  
- Docker images are built from `Dockerfile`; use `docker compose up` to run locally.