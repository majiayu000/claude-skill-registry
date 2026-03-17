---
name: dev-servers
description: Start the backend (FastAPI/uvicorn) and frontend (Vite) development servers. Use when user mentions "start dev", "run servers", "launch app", "start the app", or needs to run the application locally.
allowed-tools: Bash
---

# Development Servers

## Instructions
1. Check if dependencies are installed:
   - Backend: Look for `backend/venv/` or ask user about Python environment
   - Frontend: Check if `frontend/node_modules/` exists

2. Install dependencies if missing:
   - Backend: `cd backend && pip install -r requirements.txt`
   - Frontend: `cd frontend && npm install`

3. Start servers (recommend running in separate terminals or background):
   - Backend: `cd backend && uvicorn main:app --reload` (runs on http://localhost:8000)
   - Frontend: `cd frontend && npm run dev` (runs on http://localhost:5173)

4. Verify `.env` file exists in `backend/` with `OPENAI_API_KEY` set

## Examples
- "Start the dev servers"
- "Run the app locally"
- "Launch backend and frontend"

## Guardrails
- Never expose or log the OPENAI_API_KEY
- Confirm with user before installing dependencies
- Warn if ports 8000 or 5173 are already in use
