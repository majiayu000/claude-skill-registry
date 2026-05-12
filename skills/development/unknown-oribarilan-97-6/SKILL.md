---
name: observability
description: Use when writing or reviewing request handlers, RPCs, or background jobs for production; adding tracing, metrics, or structured-log calls; or making diagnosability decisions
---

# Observability

## Overview

Code that runs fine in dev and goes inert in production is the dominant operational failure mode for modern services. **When you add code that will run for users, you also add the diagnosability of that code: structured logs, trace context across process boundaries, metrics with bounded cardinality, signals an operator can read without your help.**

This is a **rigid** skill. Jump to the sub-section that matches what you're writing and run that sub-section's checks.

These checks matter most when adding a request handler, RPC, or background job that will run in production with users depending on diagnosability. In MVPs, prototypes, internal dev tools, and one-off scripts, structured-logging, tracing, and SLO discipline are premature — prefer the simplest thing that works.

## When to invoke

Invoke when you're about to:

- Add a request handler, RPC method, or background job that will run in production
- Add or change `log.info` / `log.warn` / `log.error` calls in code that will run under load
- Add tracing instrumentation, span creation, or trace-context propagation
- Add or change a metric (counter, gauge, histogram), especially one with labels
- Make a diagnosability decision that crosses process boundaries (logging across services, distributed traces, error correlation)
- Review observability coverage, log/metric/trace quality, or diagnosability of existing code

### Non-triggers — do NOT invoke for

- A script that runs once locally
- A one-off migration or cleanup job
- A test
- An early-stage MVP or prototype where the architecture is still in flux
- An internal dev tool or debugging endpoint
- Throwaway code expected to be replaced before reaching users

If the change adds an observability call to production code even slightly, **invoke anyway** — the cardinality and trace-context bugs are not.

## Checks by domain

### Logs

1. **Structured, not free-form.** Log as JSON or another key/value format the platform parses. Keys: `timestamp`, `level`, `event` (a short stable name like `user_login_failed`), plus the relevant context fields (`request_id`, `user_id` when not sensitive, `route`, `duration_ms`, `status`). Example: `logger.info(f"user {user.id} logged in via {provider} at {ts}")` is unsearchable; `logger.info("user_login", user_id=user.id, provider=provider)` is queryable. *(`OTel/StructuredLogs`.)*
2. **Every request carries a request id; every cross-process call propagates it.** A single user action that touches three services should be traceable through all three by one ID. Generate at the entry point if upstream did not provide one; pass through every downstream call; include in every log line emitted while handling the request.
3. **Log content boundaries belong to other skills.** What not to log (`security-and-trust-boundaries`); whether log files belong on disk or stdout (`build-deploy-and-tooling` `12F/XI`). This skill decides what fields go on the line and how they are shaped.

### Traces

4. **Propagate W3C Trace Context across process boundaries.** Every outgoing HTTP / gRPC / queue call carries the trace headers; every incoming handler reads them and continues the trace. The platform's tracer SDK does this if you let it; explicit propagation is required when you bypass the SDK (raw `requests.get`, manual queue producer). Example: a handler that reads from one service and writes to another with no propagation — the trace breaks at the boundary and the operator cannot see the cross-service path. *(`OTel/TraceContext`.)*
5. **Spans cover meaningful units of work, not every function call.** A span per HTTP request, per DB transaction, per queue message handle, per batch job — yes. A span per private helper — no, the noise drowns the signal and the trace cost rises. The default tracer auto-instrumentation usually picks the right level; resist adding more spans without a reason.

### Metrics

6. **Watch cardinality on metric labels.** Metric labels are indexed by every unique combination; an unbounded label (user id, request id, full URL path) creates one time series per unique value, which the metrics backend has to store, index, and query forever. Example: `failed_logins_total{user_id="...", reason="..."}` produces a new time series per user — millions of series for a system with millions of users, and the metrics backend falls over. **Per-user, per-request, per-trace-id data belongs in logs and traces, not metric labels.** Metric labels are for low-cardinality, bounded sets: HTTP method, route template, status class, region, downstream name. *(`OE/CardinalityDiscipline`.)*
7. **Choose the four signals deliberately for service code.** For a production service, the canonical operator-facing signals are **latency** (how long is the work taking), **traffic** (how much work), **errors** (rate of failed work), and **saturation** (how full is the resource). For each new request handler or background job, ask which of the four signals is observable; if any is not, add an instrument or note the gap. Not every codebase needs all four — a CLI is not a service — but service code does. *(`SRE/GoldenSignals`.)*

## Red Flags

These thoughts mean STOP — apply the domain check before committing:

| Thought | Reality |
|---|---|
| "I'll log a single human-readable string — it's easier to grep." | Free-form strings are unsearchable in production aggregators. Log structured key-value with stable event names; the operator queries by field, not by substring. (`OTel/StructuredLogs`) |
| "I'll add the user id as a metric label so we can see per-user failures." | Per-user labels create a time series per user. Use a metric for the *count*; put the user id in logs and traces where high cardinality is fine. (`OE/CardinalityDiscipline`) |
| "I'll add the full URL path as a label." | Same problem — `/users/12345` and `/users/12346` are different series. Use the route template (`/users/:id`), not the realized path. (`OE/CardinalityDiscipline`) |
| "I'll instrument every helper function with a span." | Spans cover meaningful units of work; one per private helper buries the trace in noise. Span per request / transaction / job, not per function. (`OTel/TraceContext`) |
| "The downstream call uses raw `requests.get` — no need to thread the trace headers." | The trace breaks at the boundary; the operator cannot see the cross-service path. Propagate W3C Trace Context, even when bypassing the tracer SDK. (`OTel/TraceContext`) |
| "We don't measure latency on this background job — it'll be fine." | Without latency / traffic / errors / saturation visibility, the only way to know it broke is a user complaint. Wire at least the four signals for production service code. (`SRE/GoldenSignals`) |
| "The request id is in the trace — we don't need it in the log." | Logs without the request id force the operator to traverse the trace just to correlate one error line. Put the request id on every log line for the request. (`OTel/StructuredLogs`) |

## What "done" looks like

For every observability surface your change touches, **all** of the following are true:

- [ ] **Logs:** every new log call is structured (JSON or key/value), carries a stable `event` name, and includes the request id.
- [ ] **Traces:** trace context is propagated across every cross-process call your code makes; spans correspond to meaningful units of work, not every function.
- [ ] **Metrics:** every new label is bounded and low-cardinality; per-user / per-request / per-trace-id data lives in logs or traces, not labels.
- [ ] **Signals:** for production service code, the four golden signals (latency, traffic, errors, saturation) are observable for the new code path or you have noted the gap.
- [ ] **Content boundaries:** no secrets, no PII, no auth tokens in logs or traces (verified against `security-and-trust-boundaries`).

If any box that applies to your change is unchecked, you are not done. Either finish, or revert and re-plan.

## Principles in this skill

| ID | Principle | Source |
|---|---|---|
| `OTel/StructuredLogs` | Structured key/value logs with stable event names | OpenTelemetry semantic conventions; SRE book |
| `OTel/TraceContext` | W3C Trace Context propagated across every cross-process call | OpenTelemetry semantic conventions; *Observability Engineering* |
| `SRE/GoldenSignals` | The four signals for service code: latency, traffic, errors, saturation | *Site Reliability Engineering*, ch. 6 |
| `OE/CardinalityDiscipline` | High-cardinality data belongs in logs and traces, not metric labels | *Observability Engineering* (Majors et al.) |

See `principles.md` for the long-form distillations and source citations.
