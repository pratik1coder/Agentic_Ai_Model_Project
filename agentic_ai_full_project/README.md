# Agentic Company Research Assistant (Full Project)

This repository contains a fully prepared conversational AI agent (chatbot + optional voice in the browser) for the Company Research Assistant / Account Plan Generator assignment.

## What is included
- `backend/` - FastAPI backend with agent orchestration, simple tools, and OpenAI wrapper
- `frontend/` - React-based chat UI using browser SpeechRecognition and speechSynthesis for voice
- `Dockerfile` + `docker-compose.yml` - Run the backend in Docker

## Important local file included
The uploaded assignment PDF is available at this path inside the environment and is referenced by the backend as a local source:

**/mnt/data/AI Agent Building Assignment - Eightfold.pdf**

(The backend exposes `/local-assignment` which serves this file when present.)

## Quickstart - Run locally (without Docker)

### Prerequisites
- Node.js + npm (for frontend) - optional (you can interact with backend via curl/Postman)
- Python 3.10+

### Backend
1. `cd backend`
2. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` if you have one (optional for demo)
3. `pip install -r requirements.txt`
4. `python -m uvicorn app.main:app --reload --port 8000`
5. Open `http://localhost:8000/docs` to test API endpoints.

### Frontend (optional)
1. `cd frontend`
2. `npm install`
3. `npm start`
4. Open `http://localhost:3000` and interact with the chat UI. Make sure backend is running at `http://localhost:8000`.

## Run with Docker
1. `docker-compose up --build`
2. Backend will be available at `http://localhost:8000`

## How it works
- The frontend sends messages to `/api/chat` which either triggers a research pipeline (if message asks for research or a company is provided) or calls a lightweight chat assistant.
- The backend `app.agent` runs `run_research`, which calls `run_web_search` and ingests the uploaded PDF at `/mnt/data/AI Agent Building Assignment - Eightfold.pdf`.
- If `OPENAI_API_KEY` is set, real model calls will be used. Otherwise, the system returns deterministic stubbed outputs so the demo works offline.

## Demo video script (short)
1. 0:00 - 0:20 Show app and goal.
2. 0:20 - 1:30 Do a quick "Research Acme Corp" and show summary.
3. 1:30 - 2:30 Show the agent detecting conflicting numbers and asking to resolve.

## Notes
- Replace `run_web_search` with SerpAPI / Bing for live web research.
- Consider adding a vector DB (Pinecone/FAISS) for ingestion and retrieval of long docs.
