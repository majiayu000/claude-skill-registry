---
name: workflow
description: "Auto-select and orchestrate playbook skills end-to-end for feature, bug-fix, or refactor work. Use when the user gives a general request without naming a specific skill — workflow picks the right skills, sequences them, and keeps overhead proportional to the change size. NOT for creating a standalone task breakdown (use plan) or writing spec artifacts (use spec)."
metadata: {"stage":"Define","tags":["workflow","auto-routing","skill-orchestration","delivery-loop","taxonomy","orchestrator","router"],"aliases":["orchestrate","route","auto-select","delivery-loop","end-to-end"]}
---

# Workflow (Auto Router)

## Overview

This skill is a workflow orchestrator: it routes work across the other skills in this repo so you can deliver cohesive enterprise web app changes without the user needing to micromanage “which skill to use”.

Default loop: **Define → Standardize → Harden → Verify → Mechanics**.

## Workflow

### 0) Calibrate scope (keep overhead proportional)

Classify the request:

- **Tiny change**: small UI copy tweaks, rename a local variable, fix a typo. No behavior/contract change.
- **Normal change**: touches behavior, boundary semantics, or adds a feature.
- **Big change**: cross-service work, migrations, or changes that affect multiple boundaries/teams.

For this repo, **non-trivial = normal or big**.

Rule: only create/expand specs and platform primitives when they reduce future drift for the expected scope.

**Proportionality guide** (what to skip per scope):

| Scope | Skip | Always apply | Use if relevant |
| --- | --- | --- | --- |
| **Tiny** | `plan`, `spec`, `architecture`, `design`, `platform`, `review`, `finish` | `typescript` (if TS) | `testing` (if behavior changed) |
| **Normal** | `architecture` (unless cross-service), `platform` (unless 2+ services) | `plan`, `archobs`, `testing`, `finish` | `spec` (if contracts change), `resilience`/`security`/`observability` (if I/O touched) |
| **Big** | nothing | `plan`, `archobs`, `spec`, `testing`, `finish` | all Harden + Standardize skills |

### 0.5) Externalize the system model (for non-trivial changes)

Before pattern/tool selection, write a compact model:

- Objective function: **goal**, **constraints**, and **anti-goals**.
- System sketch: boundary (in/out), time horizon, actors/incentives, key flows, top bottlenecks.
- Reversibility signal: what evidence would make you change direction.

Then, if the work involves choosing between 2+ viable approaches, the first Define-stage skill stress-tests the model with probes (later skills refine, never re-run). If the path is obvious, note `probes: skipped — single viable approach` and move on.

- **Normal scope**: run Assumptions (facts vs assumptions, which to validate first), Second-Order Effects (what changes next week/quarter/year, new load/toil/coupling/failure modes, pre-mortem), and Opportunity Cost / Bias (what we're saying "no" to, sunk cost/familiarity/novelty check). Attach outputs to the decision table.
- **Big scope or high ambiguity**: also run Feedback Loops (reinforcing/balancing loops, delays, accumulations — attach to system sketch).
- **Escalate** to one template from [`../references/structured-thinking-templates.md`](../references/structured-thinking-templates.md) when: 3+ options with no clear winner, multiple stakeholders must align, rollback/incident needs formal learning capture, or big-scope probes surfaced unresolved ambiguity.

### 1) Define (what are we building?)

Pick the minimal “definition artifacts” needed:

- For **non-trivial** changes, use `plan` early to produce an executable task list, trade-off table, and measurement ladder.
- If work changes externally visible behavior (API/WS/event schema, boundary error semantics, auth rules), **use `spec`** first:
  - update the relevant `specs/*.md` and/or `apps/<service>/spec/` bundle
  - update contracts (`contracts/`: OpenAPI/proto/WS docs)
  - write acceptance scenarios and failure-mode expectations
- If the primary pressure is cross-service (partial failures, sagas, event-driven, domain boundaries), **use `architecture`**.
- If the primary pressure is in-process design (construction/structure/behavior), **use `design`**.
- For non-trivial changes, **run `archobs` and wait for its report to complete** before proceeding to `architecture` or `design`. Downstream skills depend on archobs output (risk scores, boundary leakage, cluster assignments) to make evidence-based decisions — do not continue until the report is available.

### 2) Standardize (make it consistent)

Prevent copy/paste drift:

- If the same boundary behavior repeats across services (timeouts, retries, error mapping, telemetry fields), **use `platform`** and extract a small “golden path” primitive.
- If editing TypeScript, apply `typescript` while implementing (typed boundaries, explicit lifetimes, safe module structure).

### 3) Harden (make it survive reality)

If the change touches I/O boundaries (HTTP/gRPC/DB/cache/queues/events/WS), apply these:

- `resilience`: timeouts + cancellation, bounded retries (only when safe), idempotency/dedupe, breakers/bulkheads when needed.
- `security`: authn/authz checks, strict input validation, secrets/PII safety, and SSRF/injection guardrails where applicable.
- `observability`: log/trace/metric correlation, stable field contract, and local verification steps (log → trace → metrics).

### 4) Verify (prove behavior)

- Use `testing` for non-trivial changes:
  - characterization tests before refactors
  - consumer-visible tests for new behavior and failure semantics
  - avoid asserting implementation details

### 5) Mechanics (in-process building blocks)

Only when implementation needs it:

- Apply a specific in-process pattern via `patterns-creational`, `patterns-structural`, or `patterns-behavioral`.
- Prefer wrappers/facades at boundaries; keep pattern seams small.

## Common Compositions (Recipes)

These are typical skill sequences for common work types. Adapt based on scope.

**New endpoint / handler**:
`spec` → `typescript` → `security` → `resilience` → `observability` → `testing` → `finish`

**Bug fix (production issue)**:
`debug` → *(fix)* → `testing` → `finish`

**Refactor (in-process)**:
`archobs` → `design` → `patterns-*` → `testing` → `review` → `finish`

**New service**:
`spec` → `architecture` → `platform` → `typescript` → `resilience` → `security` → `observability` → `testing` → `finish`

**Cross-service feature**:
`archobs` → `plan` → `spec` → `architecture` → `platform` → `typescript` → `resilience` → `security` → `observability` → `testing` → `review` → `finish`

**Feature roadmap**:
`archobs` → `forecast (internal)` → `plan`

**Full situational awareness**:
`archobs` → `forecast (combined)` → `plan`

**Technology adoption assessment** (outside-in):
`intel` → `forecast (external)` → `archobs` → `architecture` → `plan`
Start with ecosystem signals, then check internal readiness. Use when the question is "should we adopt X?" rather than "what should we build next?"

**Conditional composition**: When archobs reveals high coupling to external dependencies (files with high `xnbr` bridging to third-party code, or clusters labeled with external technology names), invoke `forecast` in combined mode (not just internal). Topics for the external engine are derived from archobs cluster labels and high-xnbr file paths.

**Architecture health pass**:
`archobs` → `plan` (from suggestions) → `design` → `patterns-*` → `testing` → `finish`

**Security hardening pass**:
`security` → `testing` → `review` (type: security) → `finish`

## Guardrails

- Don’t create “spec theater”: if the change is tiny, keep docs minimal and move on.
- Don’t choose architecture/patterns before writing objective function + constraints + anti-goals.
- Don’t skip specs for boundary/contract changes: pin behavior with contracts + tests.
- Don’t introduce retries without idempotency.
- Don’t add telemetry labels with unbounded/high-cardinality values.
- Don’t define metrics without a named decision, owner, and review ritual.
- Don’t “helpfully” change response shapes or error semantics unless the spec says so.

## Output Template

When you finish work, report:

- For non-trivial changes, run `finish` before reporting.
- **Skills applied**: which ones you used and why (1 line each).
- **System model** (non-trivial only): objective function + system sketch + reversal signal.
- **What changed**: behavior + contract impacts + key files touched.
- **Decision + measurement** (non-trivial only): chosen option, trade-offs, kill criteria, leading/lagging indicators, and review cadence/owner.
- **Verification**: commands run and results (or why they couldn’t be run).
- **Follow-ups**: optional next tasks (if any).

## References

- Machine-readable skill index (triggers, tags, related, overhead): [`specs/skills-manifest.json`](../../specs/skills-manifest.json)
- Workflow taxonomy: [`specs/003-taxonomy-and-workflow.md`](../../specs/003-taxonomy-and-workflow.md)
- Change process: [`specs/004-change-process.md`](../../specs/004-change-process.md)
- Structured-thinking probes + templates: [`../references/`](../references/) (checklists for inline probes, templates for escalation)
