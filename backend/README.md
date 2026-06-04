# Smart Manufacturing Troubleshooting Assistant (Backend)

Run the FastAPI backend which provides endpoints for PDF ingestion (RAG) and a WebSocket chat for multi-agent troubleshooting.

Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.

3. Run the server:

```bash
uvicorn app.main:app --reload --port 8000
```
