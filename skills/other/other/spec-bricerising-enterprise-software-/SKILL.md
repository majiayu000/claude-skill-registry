---
name: spec
description: "Write and maintain spec-first artifacts (service specs, API contracts via OpenAPI/protobuf/WebSocket schemas, ADRs, task lists, quickstarts). Use when creating specs/*.md, apps/*/spec/ bundles, or contracts/ docs, especially before major behavior changes or multi-agent collaboration. NOT for implementation task breakdown without spec artifacts (use plan); NOT for choosing system or code patterns (use architecture or design)."
metadata: {"stage":"Define","tags":["spec-first","contracts","acceptance-criteria","decision-records","nfrs","openapi","protobuf","adr"],"aliases":["specification","contract","api-contract","schema","acceptance","requirements"]}
---

# Spec (Spec-Driven Development)

## Overview

Create a stable “source of truth” for agents and humans: write specs with testable acceptance criteria and keep them aligned with implementation.

This skill treats specs as **operational tooling**: they prevent scope drift, enforce invariants, and make AI iteration converge.

## Core Idea

- Specs define **what must be true** (contracts, scenarios, invariants, NFRs), not “how we coded it”.
- Plans/tasks define **how we’ll get there** (phases, work breakdown, acceptance per task).
- Code + tests are the proof.

## Where Specs Live (Opinionated)

Use one (or both) of these:

- **System specs**: `specs/*.md` for cross-service rules and shared constraints (auth, observability, eventing, product scope).
- **Decision records**: `specs/decisions/*.md` for significant choices (trade-offs, migrations, taxonomy, compatibility).
- **Service spec bundle**: `apps/<service>/spec/` for service-local truth:
  - `spec.md`: requirements and acceptance scenarios
  - `contracts/`: OpenAPI/proto/WS message contracts
  - `data-model.md`: domain entities + storage boundaries
  - `plan.md`: phases and wiring/structure
  - `tasks.md`: checklist-style backlog with acceptance criteria
  - `quickstart.md`: how to run/verify the service in dev

## Chooser (What Spec Artifact To Write)

- **Cross-service rule or shared constraint** (auth, observability, eventing, product scope): write/update a system spec (`specs/NNN-<topic>.md`).
- **Significant trade-off or migration decision**: write a decision record (`specs/decisions/NNN-<topic>.md`).
- **New or changed service behavior**: write/update the service spec bundle (`apps/<service>/spec/`).
- **API/contract change** (new endpoint, changed schema, new event): update contracts (`contracts/`: OpenAPI/proto/WS docs) in the spec bundle.
- **Task breakdown for implementation**: update `tasks.md` in the spec bundle (or `specs/tasks.md` for repo-level backlog).
- **Minor behavior tweak within existing contracts**: update acceptance scenarios in the existing spec; no new artifacts needed.

## Clarifying Questions

- Is this change scoped to one service or does it cross service boundaries?
- Does it change externally visible behavior (API shapes, error codes, event schemas, auth rules)?
- Are there existing specs/contracts that should be updated vs creating new ones?
- Who are the consumers of this contract (other services, clients, external partners)?
- Is backward compatibility required, or can we make breaking changes?

## Workflow

0. **Load archobs data** (before spec writing begins):
   ```bash
   archobs show clusters --format json
   archobs show risks --format json
   ```

   **Use in spec writing**:
   - Ensure spec contracts honor existing cluster boundaries. If the spec introduces a new boundary that cuts across a cluster with `cohesion > 0.60`, flag the conflict — the spec is fighting natural structure.
   - Files with `risk > 0.5` in the spec's scope warrant stricter acceptance criteria and testing requirements.
   - Clusters with `leakage > 0.20` that the spec touches may need explicit boundary contracts (interface types, Facade).

   If archobs artifacts are missing: run `archobs report` or note as a gap. Do not block spec writing on archobs — the spec can be amended when data becomes available.

0b. **Versioning guidance from forecast** (conditional — run when the spec pins an external dependency contract such as an API version, SDK, or protocol):

   ```bash
   intel forecast    # lifecycle phase for the dependency
   ```

   **Decision mapping**: See [Lifecycle Decision Mapping — Spec: Versioning Strategy](../references/lifecycle-decision-mapping.md#spec-versioning-strategy) for lifecycle phase → versioning strategy table.

1. Decide the scope:
   - One service? write/update the service spec bundle.
   - Cross-service or product-wide? write/update a system spec.
2. Write the objective function up front:
   - goal, constraints, anti-goals
   - boundary (in/out) and time horizon
3. Externalize the system sketch:
   - actors + incentives
   - key flows (work/data/risk)
   - top constraints/bottlenecks
4. Write acceptance-first:
   - user story + “independent test”
   - acceptance scenarios (Given/When/Then)
   - edge cases and invariants (“constitution requirements”)
5. Lock down contracts:
   - HTTP/gRPC schemas, message types, error codes, idempotency keys
   - versioning rules and backward compatibility expectations
6. Add non-functional requirements (NFRs) that matter:
   - latency budgets, concurrency, durability, audit, privacy
   - observability and resilience requirements (trace/log/metrics, timeouts/retries/idempotency)
7. Add a compact decision table:
   - options considered (include baseline/no-change)
   - what is optimized vs knowingly worsened
   - kill criteria / reversal trigger
8. Stress-test the decision (if 2+ viable approaches exist; skip for single viable approach):
   - **Assumptions**: What are facts vs assumptions? Which assumption is least certain — how will we validate it? Cross-reference with archobs data from step 0 and versioning guidance from step 0b (if applicable). *(attach to decision table)*
   - **Second-Order Effects**: What happens next week / next quarter / next year? What new load, toil, coupling, or failure mode does this create? If this fails in 6-12 months, what likely caused failure? Cross-reference with archobs data from step 0 and versioning guidance from step 0b (if applicable). *(attach to decision table)*
   - **Opportunity Cost**: What are we saying "no" to? Are we favoring this due to sunk cost, familiarity, or novelty? *(attach to decision table)*
   - If probe output already exists from an earlier Define-stage skill in this flow (including `workflow` orchestration), refine it instead of re-running.
9. Add a measurement ladder:
   - decision being measured
   - leading indicators (early signal)
   - lagging outcomes (business/ops)
   - instrumentation sources + review ritual (owner/cadence/action trigger)
10. Break it into tasks with acceptance:
   - keep tasks small and orderable
   - each task has an observable acceptance check
11. Implement and keep docs honest:
   - if implementation forces a change in behavior, update specs first
   - keep quickstarts and contracts current

## Guardrails

- “No spec, no change”: don’t implement major behavior without updating the spec surface.
- Don’t hide requirements in code; put them in `spec.md` where agents can find them.
- Keep contracts stable; prefer additive changes and version explicitly when you can’t.
- Write down **non-goals** to stop scope creep.
- For non-trivial decisions, record opportunity cost explicitly to avoid accidental scope drift.
- No metric without a named decision and review ritual.
- If a design cannot be measured cheaply enough to guide weekly decisions, treat that as a constraint and simplify.

## References

- Templates: [`references/templates.md`](references/templates.md)
- Spec quality checklist: [`references/checklists.md`](references/checklists.md)
- Structured-thinking probes + templates: [`../references/`](../references/) (checklists for inline probes, templates for escalation)
- Architecture choices: [`architecture`](../architecture/SKILL.md)
- In-process pattern choices: [`design`](../design/SKILL.md)
- Typed boundaries/errors/lifetimes: [`typescript`](../typescript/SKILL.md)
- Consumer-visible tests: [`testing`](../testing/SKILL.md)

## Output Template

When using this skill, return:

- **Scope + objective**: boundary, constraints, anti-goals.
- **Artifacts created/updated**: exact spec files (and contracts/ADRs when relevant).
- **Decision summary**: options considered, selected option, trade-offs, kill criteria, and assumptions (facts vs assumptions, opportunity costs).
- **Measurement ladder**: leading + lagging indicators, owner/cadence/action trigger.
- **Verification plan**: concrete checks/commands that prove acceptance scenarios and failure expectations.
- **Next implementation tasks**: ordered checklist with observable acceptance per task.
