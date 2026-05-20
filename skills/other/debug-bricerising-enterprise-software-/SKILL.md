---
name: debug
description: "Triage and diagnose production or local issues by following logs → traces → metrics (HTTP/gRPC/async). Use when investigating errors, latency spikes, 5xx responses, SLO violations, or regressions in an instrumented app. NOT for adding new instrumentation (use observability); NOT for applying resilience patterns (use resilience)."
metadata: {"stage":"Harden","tags":["incident-response","triage","logs","tracing","metrics","production-issue","5xx","latency","regression","postmortem"],"aliases":["diagnose","troubleshoot","investigate","triage","incident","production-bug","outage","incident-review"]}
---

# Debug (Log → Trace → Metrics)

## Overview

This skill is for **debugging** with existing telemetry. It does **not** focus on adding instrumentation (use `observability` when telemetry gaps block triage).

Goal: turn “something is broken/slow” into:

- a concrete **symptom + impact** statement,
- an **evidence-backed hypothesis** (or a small set of competing ones),
- a **mitigation** (rollback/flag/scale) when needed,
- a short list of **fix + follow-up** tasks.

## Workflow

### 0) Establish ground truth (2–5 minutes)

Capture:

- Environment (`local`/`dev`/`staging`/`prod`) and time window (start/end).
- Symptom (what’s failing/slow) and impact (SLO/user-visible blast radius).
- One **exemplar**: request/trace ID, job run ID, message ID, or timestamped log line.

### 1) Logs (find the exemplar and its correlation IDs)

1. Find the first error/timeout log line closest to the symptom window.
2. Identify correlation keys (prefer stable IDs):
   - `traceId`, `requestId`, `spanId`
   - `op` (route template / RPC method / job name / message type)
   - error code/type (typed error envelope, gRPC status, HTTP status)
3. Pull the **full log story** for the exemplar (start → downstream call(s) → failure).

Copy/paste helpers live in `references/commands.md`.

### 2) Trace (turn the exemplar into a dependency hypothesis)

If you have a `traceId`, use it.

1. Open the trace and confirm the root span matches the suspected operation (`op`).
2. Identify:
   - the slowest span(s),
   - the first error span(s),
   - retries (multiple similar child spans),
   - deadline/time budget signals (deadline exceeded, timeout errors).
3. Convert that to a dependency statement:
   - “`service A` is timing out calling `service B` method `X`”
   - “DB query `Y` is slow / missing index / deadlocked”
   - “Queue consumer is failing on message type `T` (poison message)”

If you cannot find/interpret traces, fall back to logs + metrics and consider adding missing telemetry via `observability`.

### 3) Metrics (confirm blast radius + regression)

Use metrics to answer:

- Is this widespread or isolated to one tenant/route/method?
- Is it a new regression (deploy-correlated) or a gradual degradation (resource/saturation)?
- Is it primarily errors or latency?

Start with RED for the boundary (HTTP route / gRPC method / consumer group).

### 4) Map failure propagation (technical + organizational)

- If this component degrades, what fails next?
- What is likely failing silently (data drift, dropped work, partial writes, stale reads)?
- What is the organizational cascade (handoff queue, approvals, unclear ownership)?

### 5) Decide: mitigate vs investigate

If impact is high and evidence points to a recent change:

- rollback / disable flag / reduce load / scale critical dependency

If impact is moderate or unclear:

- tighten the hypothesis with 1–2 targeted checks (another exemplar trace, compare two instances, check downstream health)

### 6) Capture learnings (don’t lose the fix)

If you found a systemic gap, capture it:

- missing telemetry field contracts → [`observability`](../observability/SKILL.md)
- retries without idempotency / missing time budgets → [`resilience`](../resilience/SKILL.md)
- repeated boundary logic across services → [`platform`](../platform/SKILL.md)
- cross-service pattern confusion → [`architecture`](../architecture/SKILL.md)

## Guardrails

- Don’t log secrets/PII while triaging (even “temporarily”).
- Don’t use unbounded IDs as metric labels; use logs/traces for per-entity investigation.
- Don’t add retries as a debugging “fix” without idempotency/dedupe.
- Prefer a small number of exemplars (2–3) over “grep everything forever”.

## References

- Copy/paste commands: [`references/commands.md`](references/commands.md)
- Scenario checklists (HTTP/gRPC/consumers): [`references/scenarios.md`](references/scenarios.md)
- Retrospective / Postmortem template: [`../references/structured-thinking-templates.md`](../references/structured-thinking-templates.md)
- If telemetry is missing: [`observability`](../observability/SKILL.md)

## Output Template

When using this skill, return:

- **Symptom**: what is failing/slow (include concrete ops: route/method/job/message type).
- **Impact**: who/what is affected and how badly (errors %, latency p95, backlog size).
- **Time window**: start/end and whether it correlates with deploy/config change.
- **Evidence**: exemplar IDs + the key log/trace/metric observations.
- **Hypothesis**: most likely cause + 1 alternative (if applicable).
- **Failure propagation**: what breaks next, what breaks silently, organizational cascade points.
- **Mitigation**: what you did / recommend doing now (rollback/flag/scale).
- **Fix plan**: code/config changes to make it correct and durable.
- **Follow-ups**: telemetry gaps, runbook updates, tests, new invariants.
  - If root cause is systemic, flag for a follow-up retrospective ([`../references/structured-thinking-templates.md`](../references/structured-thinking-templates.md) — Retrospective / Postmortem).
