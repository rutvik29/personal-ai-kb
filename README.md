# 🧠 Personal AI Knowledge Base

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=flat)](https://ollama.ai)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5-FF6B35?style=flat)](https://www.trychroma.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **100% private, local-first AI knowledge base** — ingest notes, PDFs, and URLs; chat with your knowledge using local Ollama LLMs + ChromaDB. Zero data leaves your machine.

## ✨ Highlights

- 🔒 **100% local** — Ollama LLMs + local ChromaDB, zero cloud API calls required
- 📝 **Multi-format ingestion** — Markdown notes, PDFs, web URLs, plain text
- 💬 **Chat with your knowledge** — ask questions, get cited answers from your notes
- 🔍 **Semantic search** — find related notes you didn't know you had
- ⚡ **Fast indexing** — background ingestion with real-time chat
- 🏠 **Self-hosted** — runs entirely on your MacBook/Linux machine

## Quick Start

```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2

# 2. Clone and install
git clone https://github.com/rutvik29/personal-ai-kb
cd personal-ai-kb
pip install -r requirements.txt

# 3. Ingest your notes
python ingest.py --source ~/Documents/notes/ --source ~/Downloads/*.pdf

# 4. Start chatting
streamlit run ui/app.py
# or
python chat.py "What did I write about machine learning last month?"
```

## License
MIT © Rutvik Trivedi
