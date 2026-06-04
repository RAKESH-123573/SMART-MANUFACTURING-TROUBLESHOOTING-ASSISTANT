# Smart Manufacturing Troubleshooting Assistant Documentation

## Overview

This repository contains a full-stack solution for a Smart Manufacturing Troubleshooting Assistant:

- `backend/`: FastAPI backend providing RAG ingestion, query, and websocket chat endpoints.
- `frontend/`: Minimal React frontend for interacting with the assistant.

The backend uses a RAG pipeline with LangChain and Chroma, along with a supervisor agent layer for industrial troubleshooting workflows.

## Repository Structure

- `backend/`
  - `app/`: FastAPI application code and agent orchestration.
  - `requirements.txt`: Python dependencies.
  - `.env.example`: Environment variables required by the backend.
- `frontend/`
  - `package.json`: React frontend dependencies and scripts.
  - `public/`: Static frontend assets.
  - `src/`: React application source.
- `docs/`: Documentation for installation, architecture, and usage.

## Setup

### Backend

1. Open a terminal in `backend/`.
2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Copy the environment file and configure it:

```powershell
copy .env.example .env
```

5. Edit `.env` and set `OPENAI_API_KEY`.

6. Run the backend server:

```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. Open a terminal in `frontend/`.
2. Install dependencies:

```powershell
npm install
```

3. Start the frontend:

```powershell
npm start
```

4. Open the app in your browser at `http://localhost:3000`.

## API Endpoints

The backend exposes the following endpoints:

- `POST /api/ingest` — Upload a PDF file for ingestion.
- `POST /api/query` — Send a troubleshooting query with optional sensor data.
- `GET /api/docs` — Open FastAPI interactive API documentation.
- `GET /api/redoc` — Open ReDoc documentation.
- `WS /api/ws/chat` — WebSocket chat interface for streaming agent responses.

## Notes

- The backend currently depends on OpenAI credentials for language model calls.
- The repository includes a `.gitignore` that excludes virtual environments, environment files, and local caches.
- If you encounter installation issues for native packages, install the required build tools for your OS.

## Related Documentation

- `backend/README.md`: Backend-specific setup and usage.
- `frontend/`: Frontend setup and runtime instructions.

## Contribution

To contribute or extend this project, start by reviewing the `backend/app` implementation and the React UI in `frontend/src`.
