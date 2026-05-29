---
name: mapping-invariants
description: "Intro skill for designing and implementing assertions. Use when starting a new protocol to map invariants before writing assertions or tests."
---

# Mapping Invariants

Start here before designing or implementing assertions. This skill defines the invariant‑mapping workflow and hands off to the other skills.

## When to Use
- Starting a new protocol assertion effort.
- You need a structured method to discover invariants.
- You want the step‑by‑step path before `designing-assertions` and `implementing-assertions`.

## When NOT to Use
- You already have a vetted invariant list.
- You only need implementation details. Use `implementing-assertions`.
- You only need testing guidance. Use `testing-assertions`.

## Quick Start
1. Build the protocol map (assets, roles, entrypoints, state, routers).
2. Enumerate invariants by category (access control, accounting, pricing, solvency, limits, modes).
3. Rank invariants by impact and likelihood (losses, control‑plane, liveness).
4. Identify exceptions and acceptable violations.
5. Pick data sources (state, logs, call inputs, slots).
6. Choose enforcement location (chokepoint vs per‑contract).
7. Produce the invariant matrix and trigger map.
8. Hand off to `designing-assertions` → `implementing-assertions` → `testing-assertions`.

## Workflow
- **Protocol map**: read docs/specs/audits/tests; list contracts, assets, roles, and critical entrypoints.
- **Invariant inventory**: express “states that must never occur” and rank by impact.
- **Spec classification**: split global invariants vs action-specific postconditions (GPOST/HSPOST).
- **Exception audit**: capture legitimate exceptions (bad debt, emergency modes, timelocks).
- **Observation plan**: decide which values/events you will read to validate each invariant.
- **Trigger plan**: select the narrowest trigger that guarantees coverage.
- **Coverage check**: confirm each invariant is reachable from at least one trigger and entrypoint.

## Heuristics
- Start with loss‑bearing invariants: solvency, accounting integrity, and upgrade control.
- Prefer cross‑function invariants over per‑function reverts already in code.
- If you cannot observe an invariant reliably, rephrase it to observable signals.
- For lending protocols, classify actions by health‑factor impact and list allowed transitions.

## Deliverables
- Invariant matrix (definition, source, exceptions, priority).
- Trigger map (selector/slot/balance mapping).
- Data source list (storage layout, logs, call inputs).
- Test plan (positive/negative, fuzz, backtest candidates).

## Rationalizations to Reject
- “We can skip invariant mapping and write code directly.”
- “We only need owner checks.” (Protocols usually fail on accounting and pricing.)
- “One broad assertion is enough.” (Gas and coverage risks.)
- “We’ll add exceptions later.” (Most false positives come from ignored exceptions.)

## References
- [Invariant Mapping Workflow](references/invariant-mapping-workflow.md)
- [Protocol Example Patterns](references/protocol-examples.md)
- [Lending Protocol Invariant Checklist](references/lending-invariant-checklist.md)
