---
name: skriptoteket-backend-dev
description: "Backend engineering for Skriptoteket (FastAPI monolith): architecture + file tree navigation (DDD/Clean layers), protocol-first DI, Unit of Work + transactions, DomainError semantics, core data shapes/contracts (tool UI contract v2, runner contracts, file refs), and backend testing strategy. Use when implementing/refactoring/reviewing backend code; use skriptoteket-local-devops for local dev setup and troubleshooting."
---

# Skriptoteket backend dev

## Quick start (preferred: docker hot reload)

- Ensure `.env` exists (copy from `.env.example`; set `BOOTSTRAP_SUPERUSER_*`).
- Start full dev stack (db + web + worker + frontend/Vite): `pdm run dev-start`
- Follow logs: `pdm run dev-containers-logs`
- Health: `curl -sSf http://127.0.0.1:8000/healthz >/dev/null`
- Stop (only when requested): `pdm run dev-stop`

### Alternative: host backend + host Vite

- Backend: `pdm run dev-logs` (writes `.artifacts/dev-backend.log`)
- Frontend: `pdm run fe-dev-logs` (writes `.artifacts/dev-frontend.log`)
- Both: `pdm run dev-local`

## File tree + entrypoints (codemap)

- App factory: `src/skriptoteket/web/app.py` (FastAPI app, middleware order, Dishka wiring)
- Composition root: `src/skriptoteket/di/__init__.py` (providers assembled)
- API surface: `src/skriptoteket/web/api/v1/` (thin routers + boundary DTOs)
- Domain: `src/skriptoteket/domain/` (pure rules; no FastAPI/SQLAlchemy)
- Application: `src/skriptoteket/application/` (command/query handlers; orchestrates UoW + protocols)
- Protocols: `src/skriptoteket/protocols/` (typing.Protocol boundaries)
- Infrastructure: `src/skriptoteket/infrastructure/` (DB/repos, runner, llm, integrations)
- Worker loop: `src/skriptoteket/workers/execution_queue_worker.py` (ADR-0062)
- Runner runtime: `src/skriptoteket/infrastructure/runner/` + `runner/` (sandboxed execution env)
- DB migrations: `migrations/` + `alembic.ini`

Tip: generate a fresh tree with `find src/skriptoteket -maxdepth 2 -type d`.

## Critical invariants (non-negotiable)

- Follow `.agent/rules/000-rule-index.md` (layer boundaries, protocol-first DI, docs workflow).
- Keep domain pure: no web/db/framework imports in `src/skriptoteket/domain/**`.
- Keep web/api thin: validate + call handlers; never put business logic in routers.
- Raise `DomainError` (no HTTP) and map to HTTP in `src/skriptoteket/web/*`.
- Unit of Work owns commit/rollback; repositories never commit (see `src/skriptoteket/infrastructure/db/uow.py`).
- Avoid OpenAPI breakage: do NOT use `from __future__ import annotations` in router modules (rule 040).
- For editor AI / LLM changes: follow `.agent/rules/047-ai-llm-guardrails.md` + `docs/runbooks/runbook-openai-responses-api.md`.
- For execution queue/worker changes: follow `.agent/rules/062-execution-queue-worker-loop.md` + ADR-0062.

## Key ADRs + “goal state” watchlist

Read first when touching these areas:

- Architecture + boundaries: `docs/adr/adr-0004-clean-architecture-ddd-di.md`
- Auth sessions + roles: `docs/adr/adr-0009-auth-local-sessions-admin-provisioned.md`, `docs/adr/adr-0005-user-roles-and-script-governance.md`
- Tool UI contract v2: `docs/adr/adr-0022-tool-ui-contract-v2.md` (models in `src/skriptoteket/domain/scripting/ui/contract_v2.py`)
- Tool sessions + persistence: `docs/adr/adr-0024-tool-sessions-and-ui-payload-persistence.md`
- Multi-file inputs: `docs/adr/adr-0031-multi-file-input-contract.md`
- Execution queue worker loop: `docs/adr/adr-0062-execution-queue-and-worker-loop.md`
- OpenAPI as source + frontend types: `docs/adr/adr-0030-openapi-as-source-and-openapi-typescript.md`
- Runner request envelope v1 (goal state): `docs/adr/adr-0063-runner-request-envelope-v1.md`
- File references + resolver (goal state): `docs/adr/adr-0064-file-references-and-resolver.md`

For roadmap/critical-path work, start from `docs/reference/ref-implementation-map-script-hub-v0-2.md`.

## Stories + planning workflow (when implementing backlog work)

- Planning workflow: `docs/reference/ref-sprint-planning-workflow.md`
- Review gate (required for proposed EPICs/ADRs): `.agent/rules/096-review-workflow.md`

## DB + migrations

- Migrations live in `migrations/versions/`; workflow rules in `.agent/rules/054-alembic-migrations.md`.
- Upgrade dev DB: `pdm run db-upgrade`
- If you add a migration, add/run the docker idempotency integration test (rule 054).

## CLIs + seeding

- Bootstrap superuser: `pdm run bootstrap-superuser`
- Seed script bank:
  - Runbook: `docs/runbooks/runbook-script-bank-seeding.md`
  - Safe default: `pdm run seed-script-bank --dry-run --profile dev`
- Execution worker (one-off): `PYTHONPATH=src pdm run python -m skriptoteket.cli run-execution-worker --once`

## Harnesses (debugging / regression checks)

- OpenAPI export: `pdm run openapi-export-v1`
- Frontend API types: `pdm run fe-gen-api-types`
- UI smoke (Playwright): `pdm run ui-smoke` / `pdm run ui-editor-smoke` / `pdm run ui-runtime-smoke`
- Hot reload probe (Playwright): `pdm run ui-hmr-probe`
- Edit-ops harnesses (ad-hoc): `python -m scripts.edit_ops_harness` and `python -m scripts.chat_edit_ops_context_probe`

## Curl / scripting recipes (sessions + CSRF)

Suggested env vars:

```bash
export BASE_URL=http://127.0.0.1:8000
export COOKIE_JAR=.artifacts/cookies.txt
export EMAIL="${BOOTSTRAP_SUPERUSER_EMAIL:-superuser@local.dev}"
export PASSWORD="${BOOTSTRAP_SUPERUSER_PASSWORD:-change-me}"
```

Login (stores session cookie; returns CSRF token):

```bash
curl -sS -c "$COOKIE_JAR" -H 'Content-Type: application/json' \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}" \
  "$BASE_URL/api/v1/auth/login"
```

Notes:

- Correlation header: `X-Correlation-ID: <uuid>` (echoed back in responses via middleware).
- CSRF header: `X-CSRF-Token: <token>` (see `src/skriptoteket/web/auth/api_dependencies.py`).

## Testing protocol (backend)

- Follow `.agent/rules/070-testing-standards.md` and `docs/runbooks/runbook-testing.md`.
- Default: `pdm run test` (unit tests mock protocols; integration uses Docker/testcontainers).
- Also run: `pdm run lint` and `pdm run typecheck` for backend changes.
