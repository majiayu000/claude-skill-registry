---
name: agent-observability
description: Design privacy-aware observability for AI agents using traces, spans, structured events, metrics, cost attribution, dashboards, alerts, and investigation workflows. Use when instrumenting an agent, debugging intermittent tool or model failures, defining service-level objectives, analyzing latency or spend, auditing agent decisions, or preparing production monitoring.
---

# Agent Observability

Make agent behavior explainable from request entry through model, retrieval, tool, handoff, and response spans.

## Use when

- Add telemetry to a new or existing agent workflow.
- Diagnose slow, costly, incorrect, looping, or failed executions.
- Define dashboards, alerts, service-level indicators, or audit evidence.
- Standardize traces across models, tools, and orchestration frameworks.

## Inputs

Collect the workflow graph, runtime boundaries, incident questions, traffic and failure expectations, telemetry stack, data classification, retention policy, sampling limits, and owners. State what cannot be observed.

## Output contract

Produce:

1. An observability objective and system boundary.
2. A trace and event schema with identifiers, span taxonomy, attributes, and redaction rules.
3. Metrics with definitions, units, dimensions, and ownership.
4. Dashboard and alert specifications tied to user impact.
5. A sampling, retention, access, and cost plan.
6. An investigation runbook and instrumentation verification results.

## Workflow

1. Start with operational questions such as “Which tool causes timeouts?” or “Why did cost per resolved task rise?” Do not collect fields without a decision use.
2. Define one trace per user-visible attempt. Create spans for model calls, retrieval, tools, handoffs, approvals, retries, and final validation. Preserve parent-child relationships and propagate a correlation identifier across queues.
3. Record stable semantic fields. Include version identifiers, status, timing, token and cost measures, retry counts, tool names, policy outcomes, and evaluation tags when available. Read [trace-schema.md](references/trace-schema.md) before defining attributes.
4. Separate content from metadata. Default to content-free telemetry; allow prompt or response capture only through explicit authorization, redaction, access controls, and retention limits.
5. Derive a small set of service indicators: task success, critical-policy violations, end-to-end latency, tool failure rate, escalation rate, and cost per completed task. Define denominators and treatment of cancellations and timeouts.
6. Build dashboards from user outcome to dependency detail. Alert on actionable sustained impact, not individual noisy spans, and attach an owner and runbook.
7. Control cardinality, sampling, and storage cost. Retain all critical failures when permitted; use head or tail sampling for normal traffic without losing rare error classes.
8. Test trace propagation, redaction, retry linkage, clock handling, and degraded telemetry behavior before relying on the data.

Use `python3 scripts/summarize_traces.py spans.jsonl` for a content-free structural and health summary of normalized spans. It exits `1` for missing parents, a root count other than one, parent cycles, or disconnected components. Add `--strict` to also exit `1` when likely content-, personal-data-, secret-, or credential-bearing fields are found. Add `--output summary.json` for an atomic file write; the destination must be a new path or regular file and cannot alias the input through spelling, resolution, a symlink, or a hard link. Findings include field paths and reason classes, never suspected values.

## Safety and permissions

- Never record secrets, authentication tokens, raw credentials, payment data, or unapproved personal data.
- Do not enable production capture, change retention, export telemetry, or widen access without authorization.
- Restrict raw traces by least privilege and log access to sensitive telemetry.
- Do not let instrumentation failures block the user path unless a mandated audit control requires fail-closed behavior.
- Treat traces as partial evidence: absent telemetry does not prove an action did not occur.

## Verification

- Follow a synthetic request end to end and confirm every expected span shares one trace identifier, has exactly one root, and forms one acyclic connected parent graph.
- Trigger a tool error, timeout, retry, refusal, and approval path; verify statuses and parentage.
- Search emitted telemetry for seeded secrets and personal-data canaries.
- Recalculate dashboard metrics from raw spans and confirm units, denominators, and time windows.
- Verify alerts name an owner, include diagnostic context, and avoid high-cardinality dimensions.

## Failure handling

- If trace propagation breaks, preserve local logs with correlation fields and mark cross-service conclusions as incomplete.
- If timestamps are unreliable, prefer monotonic durations within a process and avoid false cross-host ordering.
- If telemetry volume exceeds budget, reduce verbose attributes and normal-traffic sampling before dropping critical errors.
- If sensitive content is found, stop capture, restrict access, follow the incident policy, and purge only with authorized retention owners.

## Example

For “find why the research agent became slower after a release,” compare version-tagged end-to-end traces, slice p95 latency by retrieval, model, and browser-tool spans, inspect retries and queue delay, verify sampling did not change, correlate the regression with deployment time, and return the responsible stage, affected cohort, evidence limits, and a monitored remediation.
