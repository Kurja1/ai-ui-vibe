# ai-ui-vibe

## 📌 Overview
**ai-ui-vibe** is a lightweight, modular UI framework that integrates seamlessly with Ollama‑powered language models. It provides a set of reusable components, a flexible configuration system, and a developer‑friendly workflow for building AI‑enhanced web applications.

## ✨ Features
- **Model‑agnostic**: Supports any Ollama model via the `config.yaml` schema.
- **Tool‑use enabled**: Built‑in support for Ollama’s tool‑use capability.
- **Auto‑completion**: Autocomplete role for quick code generation.
- **Embedding**: Dedicated embedding role for semantic search and vector operations.
- **Docker‑ready**: `docker-compose.yml` and `.env` for instant local deployment.
- **Testing & CI**: Pre‑configured `pytest` and `ruff` scripts.

## 🚀 Quick Start
```bash
# 1️⃣ Clone the repo
git clone git@github.com:Kurja1/ai-ui-vibe.git
cd ai-ui-vibe

# 2️⃣ Create a local environment file
cp .env.example .env
# Edit .env to point to your Ollama instance:
# OLLAMA_HOST=host.docker.internal:11434

# 3️⃣ Install dependencies with UV
uv sync

# 4️⃣ Build the Docker image (if not using compose)
docker build -t ai-ui-vibe .

# 5️⃣ Launch the container on port 8000
docker run -p 8000:8000 --env-file .env ai-ui-vibe
```

## 📦 Configuration
All model definitions live in `config.yaml`. Add or modify models by editing that file. Refer to the `config.yaml` schema for required fields.

## 🧪 Testing
```bash
uv run pytest
```

## 📄 License
MIT © 2026 Olli Kauppinen

## 🤝 Contributing
Pull requests are welcome! Please open an issue first to discuss major changes.