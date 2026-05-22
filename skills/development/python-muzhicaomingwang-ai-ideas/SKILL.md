---
name: python
description: Build, review, and refactor Python backend services. Use for tasks like FastAPI/Flask service setup, API design, request/response schemas, database access (PostgreSQL), migrations, background jobs, observability (logging/metrics/tracing), authentication, configuration, testing, and production hardening.
---

# python

Use this skill for Python 后端服务开发与评审。

## Defaults (unless repo dictates otherwise)

- Framework: FastAPI (preferred) or follow existing
- Python: follow repo’s version; prefer modern typing
- API: JSON over HTTP, explicit schemas
- DB: PostgreSQL; prefer explicit migrations

## Service structure (recommended)

- `app/`
  - `main.py` (app factory, routers)
  - `api/` (routers, request/response models)
  - `core/` (config, logging, security)
  - `db/` (session/engine, repositories)
  - `models/` (ORM models if used)
  - `schemas/` (Pydantic models)
  - `services/` (business logic)
  - `integrations/` (3rd party clients)
  - `tests/`

## Workflow

1) Clarify contract
- Endpoints, auth requirements, error model, SLAs.
- Data ownership and persistence requirements.

2) API design
- Version paths (`/v1/...`) and consistent naming.
- Pydantic schemas: validate on input, shape output explicitly.
- Error responses: stable `code` + `message` + optional `details`.

3) Persistence
- Define schema and migrations (Alembic if used).
- Avoid leaking DB models into API; map to schemas.
- Use indexes for query paths; ensure safe defaults and constraints.

4) Security
- Keep secrets in env vars; never in code.
- AuthN/AuthZ: token validation, scopes/roles.
- Input validation, rate limiting (if relevant), safe logging (no PII).

5) Observability
- Structured logs with request IDs.
- Metrics for latency, error rate, DB timings; tracing if available.

6) Testing
- Unit tests for business logic.
- API tests for endpoints (happy path + errors).
- Deterministic fixtures; avoid flaky time/network dependencies.

## Output expectations when making changes

- Prefer small, incremental diffs.
- Update schemas/migrations/tests together.
- Document new env vars and run steps.

