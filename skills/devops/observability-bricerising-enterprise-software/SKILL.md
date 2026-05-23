---
name: observability
description: "Add or change observability instrumentation (structured logging, OpenTelemetry traces/spans, RED metrics, dashboards, alerts). Use when adding logs/metrics/traces to code, defining telemetry field contracts, or building monitoring runbooks. NOT for diagnosing existing issues with existing telemetry (use debug); NOT for security-specific logging concerns (use security)."
metadata: {"stage":"Harden","tags":["logging","monitoring","tracing","metrics","telemetry","opentelemetry","dashboards","alerts"],"aliases":["logs","traces","metrics","monitoring","instrumentation","otel","opentelemetry","RED-metrics"]}
---

# Observability (Instrumentation + Verification)

## Overview

Make observability consistent and actionable: every boundary emits traces, metrics, and structured logs that correlate via IDs and stable fields.

This is intentionally opinionated: you should be able to answer “what happened?” with **log → trace → metrics** within a minute.

## Workflow

1. Name the **decision** this telemetry will inform (for example: keep current architecture, tune a timeout, roll out a migration).
2. Define the **unit of work** (one trace): HTTP request, gRPC call, job run, queue message, WebSocket action.
3. Define the measurement ladder:
   - 3 leading indicators (move within days)
   - 3 lagging outcomes (move within weeks/months)
   - owner + review cadence + trigger for action
4. Instrument end-to-end:
   - traces: spans around the unit of work + key downstream calls
   - metrics: RED for the boundary + a few domain metrics
   - logs: structured JSON that includes correlation IDs
5. Declare the field contract (stable keys).
6. Add guardrails (PII rules, label cardinality rules, sampling/log levels).
7. Verify correlation in a failure case (error log includes `traceId`; trace contains downstream spans; metrics show error rate).
8. Define the operating ritual:
   - where metrics/logs/traces are reviewed
   - who decides and who executes follow-up
   - what threshold triggers rollback/escalation

## Clarifying Questions

- What decision does this telemetry inform (keep current architecture, tune a timeout, roll out a migration, etc.)?
- What boundaries need instrumentation (HTTP handlers, gRPC methods, DB clients, consumers, jobs, WebSockets)?
- Is there existing telemetry infrastructure (OpenTelemetry, Prometheus, Grafana, Datadog, etc.)?
- What correlation IDs already exist in the system (traceId, requestId, sessionId)?
- Are there PII/privacy constraints on what can be logged or labeled?
- Who will review these metrics, and how often (owner + cadence)?

## Chooser (What To Instrument)

Start with the user-impact boundaries:

- **HTTP handlers**: one root span per request + RED metrics per route template.
- **gRPC methods**: one root span per RPC + RED metrics per service/method.
- **DB/cache clients**: child spans per query/command; include target system and operation.
- **Async jobs / schedulers**: one root span per run; metrics for runs/success/failure/duration.
- **Event consumers**: one root span per message (or per batch); include message type and dedupe/idempotency metadata.
- **WebSockets**: session context + per-action spans; metrics for connections, messages, disconnect reasons.

## Field Contract (Opinionated Defaults)

### Logs (structured JSON)

Include these keys where applicable:

- `service`: stable service/app identifier
- `env`: environment (local/dev/staging/prod)
- `traceId`, `spanId`: correlation IDs (when tracing exists)
- `requestId`: if you use a separate request ID (often equals `traceId`)
- `op`: operation name (route template, RPC method, job name)
- `userId` / `actorId`: only if policy allows; never as a metric label
- `durationMs`: for timing logs (prefer metrics for aggregates)
- `err`: structured error (`type`/`code`, message, stack for unknown failures)

### Spans (traces)

- Name spans by operation (`HTTP GET /api/foo`, `grpc PlayerService/GetProfile`, `redis GET gateway:...`).
- Set attributes for routing and outcome (status code, error code, retry count).
- Prefer stable, low-cardinality attributes; avoid raw request bodies.

### Metrics (RED + domain)

- **RED** for each boundary (per route/RPC): request count, error count, duration histogram.
- Add a few **domain metrics** that align with product intent (tables created, orders completed, etc.).
- Avoid high-cardinality labels (no `userId`, no unbounded IDs); use logs/traces for per-entity detail.

## Guardrails (Prevent “Telemetry Debt”)

- **Cardinality discipline**: metric label values must be bounded sets; default to route templates, not raw URLs.
- **PII discipline**: never log secrets; be explicit about what IDs are safe to log.
- **Log once**: avoid logging the same error in every layer; log at the boundary with enough context.
- **Sample intentionally**: if you sample traces, keep error traces at higher priority.
- **Always end spans**: long-running work should have explicit shutdown and cancellation semantics.
- **Decision linkage**: no metric without a named decision and action threshold.

## Minimal TypeScript Snippet (Trace IDs in Logs)

If you use OpenTelemetry, you can enrich logs with the active span context:

```ts
import { context, trace } from '@opentelemetry/api';

export function getTraceLogFields(): { traceId?: string; spanId?: string } {
  const span = trace.getSpan(context.active());
  if (!span) return {};
  const { traceId, spanId } = span.spanContext();
  return { traceId, spanId };
}
```

## Testing / Verification

- Exercise a failing request and verify:
  - the error log includes `traceId`
  - the trace contains downstream span(s)
  - boundary RED metrics reflect the error
- Prefer consumer-visible tests for behavior; treat telemetry verification as a local/dev smoke check unless the project already has telemetry assertions.

## References

- Deeper checklists: [`references/checklists.md`](references/checklists.md)
- TypeScript instrumentation snippets: [`references/snippets/typescript.md`](references/snippets/typescript.md)
- Related patterns: [`Application metrics`](../architecture/references/application-metrics.md), [`Log aggregation`](../architecture/references/log-aggregation.md), [`Distributed tracing`](../architecture/references/distributed-tracing.md), [`Health Check API`](../architecture/references/health-check-api.md), [`Audit logging`](../architecture/references/audit-logging.md), [`Exception tracking`](../architecture/references/exception-tracking.md), [`Log deployments and changes`](../architecture/references/log-deployments-and-changes.md)
- Boundary tests: [`testing`](../testing/SKILL.md)
- Typed errors + explicit lifetimes: [`typescript`](../typescript/SKILL.md)

## Output Template

When applying this skill, return:

- The decision being informed and the measurement ladder (leading/lagging, owner, cadence, trigger).
- The instrumentation plan (which boundaries, what telemetry, what fields).
- The minimal code changes (where to start spans, where to log, what metrics to add).
- The verification steps (how to reproduce and correlate log → trace → metrics).
