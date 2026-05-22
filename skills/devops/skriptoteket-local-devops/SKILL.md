---
name: skriptoteket-local-devops
description: Local development + build/devops workflow for Skriptoteket (FastAPI + Vue/Vite) using PDM. Use when setting up or troubleshooting local dev (`pdm install`, `.env`, `pdm run dev`, frontend proxy/logs, correlation/logging), or when changing dependency groups/extras and Dockerfile install commands to avoid PDM group/--prod pitfalls.
---

# Local development (canonical)

## Hard rules

- Do **not** run `docker compose up` in this repo unless the user explicitly requests it.
- Run the backend via `pdm run dev` (host uvicorn), not via Compose.

## PDM script map (most used)

- Backend:
  - `pdm run dev` / `pdm run dev-logs` (logs to `.artifacts/dev-backend.log`)
  - `pdm run dev-local` (backend + SPA with log piping)
  - `pdm run kill-dev` (kills host uvicorn; only when requested)
- Frontend (SPA):
  - `pdm run fe-install`
  - `pdm run fe-dev` / `pdm run fe-dev-logs` (logs to `.artifacts/dev-frontend.log`)
  - `pdm run fe-build`
- Quality gates:
  - `pdm run format` / `pdm run lint` / `pdm run typecheck` / `pdm run test`
  - `pdm run docs-validate`

## Quick start checklist (backend)

1) Ensure `.env` exists (copy from `.env.example`).
2) Ensure tool artifacts directory exists and is configured:
   - Set `ARTIFACTS_ROOT=/tmp/skriptoteket/artifacts` in `.env`
   - Run `mkdir -p /tmp/skriptoteket/artifacts`
3) Install Python deps:
   - `pdm install -G monorepo-tools`
   - If you need browser tooling locally: `pdm install -G monorepo-tools -G dev`
4) Run backend:
   - `pdm run dev`

## Quick start checklist (frontend SPA)

- Install deps: `pdm run fe-install`
- Run SPA dev server: `pdm run fe-dev`
- When debugging API calls, check backend logs from the `pdm run dev` terminal (Vite proxies to `127.0.0.1:8000`).

## Docker / containers (only when requested)

- DB-only dev:
  - `docker compose up -d db`
  - `pdm run db-upgrade`
- Full dev containers (long-running; don’t stop unless asked):
  - `pdm run dev-start` / `pdm run dev-stop`
  - Logs: `pdm run dev-containers-logs`
- Destructive resets (explicit approval required):
  - `pdm run dev-db-reset`

## Verification (local)

- Health: `curl -sSf http://127.0.0.1:8000/healthz >/dev/null`
- Tokenizer availability (Devstral/Tekken): `pdm run pytest -q tests/unit/infrastructure/llm/test_token_counter_resolver.py`

## Logging + correlation (local)

- Configure via `.env`:
  - `LOG_FORMAT=json|console` (default: `json`)
  - `LOG_LEVEL=INFO|DEBUG|...`
  - `SERVICE_NAME` / `ENVIRONMENT` (defaults: `skriptoteket` / `development`)
- For greppable backend logs: `pdm run dev-logs` (writes `.artifacts/dev-backend.log`)
- Verify correlation end-to-end (access logs + app logs):
  - `curl -s -D - -o /dev/null -H 'X-Correlation-ID: <uuid>' http://127.0.0.1:8000/healthz`
  - `rg '<uuid>' .artifacts/dev-backend.log` (expects a `uvicorn.access` JSON line with `correlation_id`)
- Note: in our pinned Uvicorn (`0.40.0`), `uvicorn.access` is emitted on `http.response.start` (headers sent), so SSE/streaming logs appear when the stream begins.
- If running the backend via container (only when requested), use: `docker logs -f skriptoteket_web | rg '<uuid>'`

# PDM groups/extras (avoid rebuild surprises)

## Mental model

- `[project].dependencies` is **always installed** (prod + local).
- `[dependency-groups]` is for **dev-only groups** (lint/test/dev tooling). These are selected with `pdm install -G <group>` (and are incompatible with `--prod`).
- `[project.optional-dependencies]` is for **extras** (runtime feature toggles). These are selected with `pdm install --prod -G <extra>` in production-like installs.

## Known pitfall

- `pdm install --prod -G <dependency-group>` fails with: `--prod is not allowed with dev groups`.
  - Fix by moving that group to `[project.optional-dependencies]` if it must be selectable in prod builds, or by removing `--prod` if it’s dev-only.
