## Architecture Overview
# Dockerized Chainlit + Ollama Chat UI

```
project-root/                                 # Root of the repository
├── app/                                      # Main application package
│   ├── __init__.py
│   ├── main.py              # Chainlit entry point – starts the chat UI
│   ├── config.py            # Load env vars & default settings
│   ├── llm/                 # LLM‑related code
│   │   ├── __init__.py
│   │   ├── ollama_client.py # Wrapper around ollama‑python
│   │   └── rag_pipeline.py  # RAG pipeline using LangChain
│   ├── utils/               # Helper utilities
│   │   ├── __init__.py
│   │   ├── chunking.py      # Chunking logic for RAG
│   │   └── metrics.py       # Custom metrics collection
│   ├── ui/                  # Chainlit UI components
│   │   ├── __init__.py
│   │   └── chat.py          # Chat UI definition & event handlers
│   └── evaluation/          # Evaluation scripts
│       ├── __init__.py
│       ├── promptfoo.py     # Promptfoo integration
│       └── ragas.py         # Ragas integration
├── tests/                   # Unit tests
│   ├── __init__.py
│   └── test_llm.py
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Compose file to run the app
├── requirements.txt         # Python dependencies
├── INSTRUCTIONS.md          # Build & run instructions (see below)
└── .env.example             # Example environment variables
```
The Docker container runs the Chainlit app (`app/main.py`).  
It connects to a **local** Ollama instance (hosted on Windows 11) via the
`OLLAMA_HOST` environment variable.  
Evaluation scripts are bundled but not automatically executed; they can be
invoked manually or integrated into CI.

## Prerequisites
- **Docker Desktop** (Windows 11, 64‑bit) – [download](https://www.docker.com/products/docker-desktop)
- **Ollama** installed locally and running (`ollama serve`) – [install](https://ollama.ai)
- **Python 3.12+** (for local development & testing)
- **UV** (Astral) for dependency and environment management – [install](https://astral.sh/uv)

## Setup & Run

1. **Clone the repo**
   ```bash
   git clone git@github.com:Kurja1/ai-ui-vibe.git
   cd ollama-chainlit
   ```

2. **Create a local environment file**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to point to your Ollama instance:
   ```env
   OLLAMA_HOST=host.docker.internal:11434   # Docker host access on Windows
   ```

3. **Install dependencies with UV**
   ```bash
   uv sync   # Generates a lock file and installs all packages
   ```

4. **Build the Docker image**
   ```bash
   docker compose build
   ```

5. **Start the services**
   ```bash
   docker compose up -d
   ```
   The Chainlit UI will be available at `http://localhost:8080`.

6. **Stop the services**
   ```bash
   docker compose down
   ```

## Development Notes

| Feature | Where to modify |
|---------|-----------------|
| **RAG chunking logic** | `app/utils/chunking.py` |
| **LLM wrapper / model switching** | `app/llm/ollama_client.py` |
| **Chainlit UI layout & event handlers** | `app/ui/chat.py` |
| **Promptfoo evaluation** | `app/evaluation/promptfoo.py` |
| **Ragas evaluation** | `app/evaluation/ragas.py` |
| **Configuration (env vars, defaults)** | `app/config.py` |
| **Docker build** | `Dockerfile` |
| **Compose orchestration** | `docker-compose.yml` |

## Testing

Run unit tests locally (requires the same dependencies as the container):

```bash
pip install -r requirements.txt
pytest tests/
```

## CI / Evaluation

Add the following to your CI pipeline to run Promptfoo or Ragas:

```bash
# Example: Promptfoo
promptfoo run --config promptfoo.yaml

# Example: Ragas
ragas evaluate --config ragas.yaml
```

---

Happy hacking!