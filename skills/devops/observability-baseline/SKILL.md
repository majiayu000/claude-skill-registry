---
name: observability-baseline
description: Scaffold-time observability so a shipped product is not blind in prod from day one — error capture (Sentry), request-id structured logging, and /healthz + /readyz endpoints. stack-baseline pins Sentry but nothing wires it; this is the wiring. Loaded by app-scaffolder (bake into the scaffold), infra-provisioner (prod env + probes), and consumed by l3-support (traces) and devops (deploy gate).
when_to_use: |
  Apply when:
  - app-scaffolder is generating a new product (any archetype that runs as a service)
  - infra-provisioner is setting prod env vars + health probes
  - l3-support needs traces/logs to triage an incident
  Do NOT apply to:
  - pure library / cli archetypes with no running service
  - static marketing sites with no backend
effort: medium
allowed-tools: Read, Write, Edit, Grep, Glob
paths:
  - "src/**"
  - "app/**"
  - "docs/infra/**"
---

# observability-baseline

stack-baseline names Sentry and wires it nowhere — so every shipped product's first
prod incident is invisible, and l3-support triages blind. This skill makes three
things exist at scaffold time. Defaults baked in; no founder question.

## 1. Error capture (Sentry)

- `instrumentation.ts` (Next.js) / SDK init at process start; DSN from `SENTRY_DSN`
  env (never hardcoded).
- CI uploads source maps on release so stack traces are readable (release = git sha).
- Capture unhandled rejections + a global error boundary on the client.

## 2. Request-id structured logging

- A logger that emits **JSON** (not `console.log` prose) with a per-request
  `request_id` (generate at the edge, propagate via header/async-local-storage).
- Levels: error / warn / info / debug — diagnostics go to **stderr**, never mixed
  into user-facing stdout. (Same discipline as the CLI logging gap, DEEPEN d94.)
- One log line per request with: request_id, method, path, status, latency_ms.

## 3. Health endpoints

- `GET /healthz` — liveness (process up). `GET /readyz` — readiness (deps reachable:
  db, cache). Cheap, unauthenticated, no PII.
- These are what infra-provisioner probes and what a load balancer checks.

## Wiring (a skill is shelfware unless a consumer loads it)

| Consumer | What it does with this skill |
|----------|------------------------------|
| **app-scaffolder** | bakes `instrumentation.ts` + the JSON logger + `/healthz`+`/readyz` into the generated app; adds `SENTRY_DSN` to `.env.example` |
| **infra-provisioner** | sets `SENTRY_DSN` in the prod env list; points the platform health probe at `/readyz`; records the Sentry project in PROVISION |
| **l3-support** | first triage step reads Sentry + the request-id logs (a trace now exists to read) |
| **devops** | deploy gate fails if `/readyz` doesn't return 200 post-deploy |

## Output

A scaffolded app where the first prod error is captured, every request is traceable
by id, and the platform can health-check it. Record the Sentry project + endpoints
in `docs/infra/PROVISION-{slug}.md`. Done = the three pieces exist AND are wired
into the prod env, not just present in code.
