---
name: agent-studio
description: Develop, run, and debug the AGENT-Studio repo (Next.js frontend + FastAPI backend). Use for repo onboarding, starting/stopping services (restart.sh, ports 3115/8000), env vars, logs, and common dev workflows. 本仓库开发/排障：启动前后端、端口/日志、环境变量、lint/build、定位关键目录。
---

# Agent Studio (Repo)

## Navigate the repo

- Run `./restart.sh` to start the full stack (kills ports `8000`/`3115`, starts FastAPI, then Next dev on `3115`).
- Find frontend entry points in `src/app/` and shared UI in `src/components/`.
- Find chat API in `src/app/api/chat/route.ts`.
- Find backend API in `backend/main.py` and game engine code in `backend/engine/`.
- Read architectural notes before large refactors:
  - `docs/dev_docs/2025-12-31-chat-architecture-refactor.md`
  - `docs/dev_docs/2025-12-31-game-playground-roadmap.md`
  - `docs/refactoring_docs/2026-01-01-playground-page-refactor.md`

## Run common workflows

- Start frontend only: `npm install` then `npm run dev -- -p 3115`.
- Start backend only: `cd backend && (source .venv/bin/activate || true) && python main.py`.
- Lint/build: `npm run lint`, `npm run build`.

## Check configuration quickly

- Set `OPENROUTER_API_KEY` in `.env.local` for chat (`src/app/api/chat/route.ts`).
- Verify backend health at `http://localhost:8000/health`.
- Tail backend logs at `backend/backend.log` when using `./restart.sh`.

