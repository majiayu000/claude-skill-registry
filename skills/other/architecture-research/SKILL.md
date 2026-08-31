---
name: architecture-research
description: "Evidence-driven architecture research for understanding real systems and making technical decisions. Use when doing architecture landscape studies, source-backed system archaeology, build-vs-buy or adopt/adapt/build decisions, open-source and commercial comparisons, revisiting an earlier architecture choice, or handling requests such as 架构调研, 架构选型, 竞品架构, 技术尽调, 同类方案, 开源替代, how is X built, and what should we learn from X. Do not use for small mechanical changes, market-only discovery, or detailed design after the technology direction is already fixed."
---

# Architecture Research

Understand how real systems work before committing to a technical direction.
Produce a decision artifact backed by inspectable evidence, not a feature table,
vendor narrative, or speculative target architecture.

Read both references before completing decision-grade work:

- [Architecture lenses](references/architecture-lenses.md) explains how to
  inspect ownership, authority, wiring, lifecycle, recovery, trade-offs, and
  adoption risk.
- [Evidence matrix and decision template](references/evidence-matrix.md)
  provides the output structure.

## Operating Contract

- Direct actions: read-only discovery, source inspection, local experiments,
  decision recovery, comparison, and drafting within the requested access path.
- Escalate before: paid API use, new accounts or legal terms, publication of
  non-public findings, remote mutations, or an unauthorized production choice.
- Evidence-backed pushback: challenge category errors, unsupported architecture
  claims, false equivalence, and premature hyperscale design with cited facts.
- Feedback loop: test decisive claims, record unknowns and reversal evidence,
  then re-open the decision when its review trigger fires.

### Scope and handoff

Use this skill for four related tasks:

- **Landscape research**: identify and compare relevant systems or approaches.
- **System archaeology**: reconstruct how a system actually works from source,
  deployment material, tests, runtime evidence, and authoritative documents.
- **Architecture decision**: choose whether to adopt, adapt, build, defer, or
  retain the current system.
- **Decision reassessment**: recover an earlier decision, check whether its
  assumptions still hold, and keep or revise it using current evidence.

This skill owns external research, evidence, comparison, and the decision
boundary. Once a direction is selected, hand detailed internal boundaries,
contracts, and target architecture to `architecture-foundation`. Use
`product-discovery` for customer or market validation without a technical
decision question.

Respect the requested access path and repository instructions. Never expose
credentials or reproduce private implementation details in a public artifact.

Do not invoke this workflow for a small bug fix, rename, formatting change,
routine dependency use, or when the foundational technology is explicitly fixed
by the user or nearest repository instructions.

## Workflow

### 1. State the decision question

Before searching, write a compact research brief:

- User outcome and the exact capability the system must own.
- Current boundary, missing layer, and the decision to make.
- One or more representative quality scenarios: stimulus, operating condition,
  expected response, and measurable success.
- Constraints that matter now: scale horizon, freshness, latency, quality,
  privacy, deployment, budget, licensing, data ownership, and team capacity.
- Explicit non-goals and the cost of making no change.

Scale research depth to decision risk. Reversible component choices need less
evidence than a new source of truth, data platform, hosted dependency, or
one-way migration.

Challenge category errors early. A browser, API wrapper, scraper, search index,
agent runtime, and answer engine can share a surface while owning different
capabilities.

### 2. Recover existing context without inheriting its claims

When prior decisions, incidents, chats, ADRs, or benchmarks exist, extract:

- The decision and alternatives considered at the time.
- Assumptions, constraints, unresolved unknowns, and promised validation.
- What was actually implemented and what happened in operation.
- Which facts are stale, contradicted, or were never verified.

Prefer focused summaries, exact excerpts, decision records, and runtime
artifacts over loading whole conversation archives. Treat prior conclusions as
leads until their evidence is re-opened.

### 3. Select representative alternatives

Search before proposing architecture. Include only alternatives that can change
the decision:

- Maintained open-source systems with inspectable source and deployment paths.
- Commercial systems with authoritative technical material.
- Standards, public datasets, protocols, and lower-level reusable components.
- The current system and the option to make no change.

Classify each candidate as direct, adjacent, component, or non-comparable.
Do not pad the comparison to reach an arbitrary count. Decide the possible
reuse unit: whole system, subsystem, component, protocol, data model, or pattern.

### 4. Build an evidence ledger

Prefer primary evidence in this order:

1. Source code, tests, manifests, schemas, releases, and reproducible runtime
   behavior.
2. Official technical documentation, papers, standards, patents, and
   engineering posts.
3. Official product, license, and pricing material for product-level claims.
4. Independent measurements whose method, date, and environment are visible.

For current products, dependencies, pricing, licenses, or architecture, browse
and record the date or revision. Use secondary sources only to locate primary
evidence or to add clearly attributed independent evaluation.

Tag every decision-relevant claim:

- **Verified**: directly supported by cited code, documentation, or measurement.
- **Inferred**: supported by evidence but not stated directly; include the
  reasoning and confidence.
- **Unknown**: not revealed by available evidence; say what would resolve it.

Preserve contradictions. A public SDK, plugin, or MCP server proves an interface
exists; it does not prove that the underlying data, model, index, scheduler, or
hosted control plane is open or independently reproducible.

### 5. Trace the real system

Apply the relevant lenses from
[architecture-lenses.md](references/architecture-lenses.md). At minimum answer:

- What is the end-to-end path from input to user-visible result?
- Who owns each data, control, and operational boundary?
- What is authoritative, what is derived, and what is only ephemeral?
- What survives restart, and how are stale or divergent states reconciled?
- Is each claimed capability merely declared, actually implemented, wired into
  the live path, exercised, and measured?
- Which decisions are sensitivity or trade-off points for the named scenarios?

Inspect open-source implementation, tests, releases, and self-host deployment,
not only the README. For closed systems, draw a visible boundary around the
public surface and keep the hidden core unknown.

### 6. Test decision-relevant claims

When practical, run the same small representative workload against viable
options. Define before running:

- Question, candidate versions, corpus or scenario, and expected result.
- Scoring rule, environment, hardware, commands, and raw result location.
- Failure behavior and recovery test when statefulness is part of the decision.

Measure the property that can change the decision: coverage, correctness,
freshness, extraction fidelity, latency, throughput, resource use, operability,
or recovery. A component existing in source is not evidence that the production
path uses it.

If a fair test cannot run, state the missing credential, dataset, environment,
or budget and retain the uncertainty. Do not turn a vendor benchmark or demo
into local proof.

### 7. Evaluate adoption reality

For an adoption candidate, check more than technical fit:

- Maintenance and release activity, governance, contributor concentration, and
  response to security or correctness issues.
- License obligations, distribution model, deployment complexity, upgrade path,
  and operational ownership.
- Supply-chain posture, tests, release provenance, and dependency risk where
  relevant.
- Unit cost, switching cost, lock-in, and the exit path if the project or vendor
  changes direction.

Automated project-health or security scores are leads, not final truth. Inspect
the checks, their applicability, and counterevidence.

### 8. Make and bound the decision

Choose one disposition for each useful idea:

- **Adopt**: use the existing solution substantially as supplied.
- **Adapt**: reuse a bounded unit while owning the differentiating layer.
- **Build**: implement because ownership is itself required or candidates fail
  a named constraint.
- **Defer**: evidence is insufficient or the capability is not needed now.
- **Retain**: keep the current system because change is not yet justified.

Tie the recommendation to the research brief and quality scenarios. State:

- Selected direction, reuse unit, and accepted quality trade-offs.
- Rejected alternatives and what should not be copied.
- Risks, unknowns, and evidence that would reverse the decision.
- Smallest validation milestone and observable success condition.
- Exit path or review trigger for assumptions likely to change.
- Inputs for `architecture-foundation`: selected components, constraints,
  ownership decisions, unresolved questions, and prohibited dependencies.

A long-term ambition can justify staged validation, but not speculative layers
in the current implementation.

## Common failure modes

- Comparing feature names instead of system boundaries and scenarios.
- Treating self-hostable orchestration as ownership of upstream data or models.
- Equating a database row with a recoverable workflow or authoritative state.
- Counting declared modules without checking wiring, execution, and measurement.
- Assuming a public client repository contains a commercial product's core.
- Copying hyperscale architecture before proving a bounded workload.
- Ignoring acquisition, provenance, lifecycle, recovery, and evaluation while
  focusing only on algorithms or storage.
- Ranking choices with invented precision or unconfirmed weights.
- Treating repository popularity or an automated score as adoption proof.
- Hiding unknowns behind confident prose or silently degrading when research
  access fails.

## Done when

The decision artifact contains:

- A bounded decision question, scenarios, constraints, and no-change baseline.
- Candidate classification and a named reuse unit for viable options.
- An evidence ledger with citations and verified/inferred/unknown labels.
- End-to-end, ownership, authority, recovery, and capability-maturity analysis.
- Trade-offs and decision-relevant tests, or an explicit test blocker.
- Adoption viability when a third-party dependency is recommended.
- An adopt/adapt/build/defer/retain decision, rejected alternatives, accepted
  risks, reversal evidence, exit or review trigger, and smallest milestone.

Before claiming completion, re-open decisive sources, check dates and revisions,
and run repository-required validation for any changed files.
