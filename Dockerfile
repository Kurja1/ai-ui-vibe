# 1. Use Python 3.12 slim as base
FROM python:3.12-slim

# 2. The official, modern way to install uv in Docker
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Set uv environment variables
# UV_COMPILE_BYTECODE: Speeds up container startup time
# UV_LINK_MODE=copy: Required for Docker to prevent hardlink issues
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# 4. Copy ONLY dependency files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# 5. Sync dependencies using Docker BuildKit cache
# --frozen: ensures it strictly follows uv.lock without trying to update
# --no-dev: skips installing pytest, ruff, etc. into your production container
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 6. Now copy the rest of your application code
COPY app/ ./app/

# 7. Expose the port Chainlit will run on
EXPOSE 8000

# 8. Start the app using uv run
CMD ["uv", "run", "chainlit", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]