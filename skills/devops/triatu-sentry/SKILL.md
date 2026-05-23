---
name: triatu-sentry
description: "Sentry observability guidance for Triatu. Use when documenting, planning, or implementing error tracking, performance monitoring, and alerting in Next.js."
---

# Triatu Sentry

## Quick start

- Use env vars for DSN and project metadata.
- Capture errors in Server Actions, route handlers, and background tasks.
- Avoid PII in events; scrub or tag carefully.

## Workflow

1) Define env vars (`SENTRY_DSN`, `SENTRY_ENVIRONMENT`, `SENTRY_RELEASE`, sampling rates).
2) Decide scope: server, client, edge.
3) Define what to capture: errors, traces, and key transactions.
4) Add tags: feature, use case, room id (no PII).
5) Add alert rules for spikes and critical errors.
6) Document exceptions and redaction rules.

## Guardrails

- Never commit DSN or API keys in the repo.
- Avoid logging user email, full prompts, or raw payloads.
- Use sampling for traces to control cost and noise.

## References

- `docs/OBSERVABILITY.md`
- `docs/SECURITY.md`
- `docs/DEVELOPMENT.md`
