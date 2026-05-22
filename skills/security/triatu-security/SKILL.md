---
name: triatu-security
description: "Security practices for Triatu. Use when adding data access, Server Actions, logging, or Supabase policies, and when reviewing security risks."
---

# Triatu Security

## Quick start

- Validate inputs with Zod before any infrastructure call.
- Apply rate limiting in critical Server Actions.
- Avoid PII in logs; use `lib/logger` and `debug` only in dev.
- Rely on Supabase RLS for data isolation.

## Workflow

1) Identify entry points (Server Actions or route handlers).
2) Add Zod validation for inputs.
3) Add rate limiting where abuse is possible.
4) Use security logging for suspicious events.
5) Ensure adapters enforce least-privilege access.
6) Record new risks in `docs/PROJECT_AUDIT.md`.

## References

- `docs/SECURITY.md`
- `docs/DEVELOPMENT.md`
- `docs/PROJECT_AUDIT.md`
