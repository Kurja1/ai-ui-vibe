---
description: "Unit testing rules"
globs: ["tests/**/*"]
---
# tests/ context – unit tests

- Use `pytest` as the test runner.  
- Test files should be named `test_*.py`.  
- Mock external dependencies (e.g., Ollama client) with `unittest.mock`.  
- Aim for at least 80 % coverage on the `app.llm` package.  
- Keep tests deterministic; avoid network calls.  
- Use fixtures for common setup.  
- Run `pytest --cov=app` to verify coverage.