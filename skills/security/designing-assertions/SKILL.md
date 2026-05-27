---
name: designing-assertions
description: "Designs Phylax Credible Layer assertion invariants and trigger mapping. Use when scoping protocols, selecting invariants, or mapping functions to checks."
---

# Designing Assertions

Design high-signal invariants and map them to precise triggers before writing any Solidity.

## When to Use
- Starting a new assertion suite for a protocol or contract.
- Turning protocol rules into enforceable pre/post invariants.
- Choosing between call, storage, or balance triggers.

## When NOT to Use
- You need to discover invariants from scratch. Use `mapping-invariants`.
- You only need cheatcode syntax or implementation details. Use `implementing-assertions`.
- You only need test harness patterns. Use `testing-assertions`.
- You are doing a general security review without writing assertions.

## Quick Start
1. Identify assets, roles, and trust boundaries.
2. List state transitions that can violate safety properties.
3. Express invariants as pre/post comparisons or event-accounting rules.
4. Select data sources (state, logs, call inputs, storage slots).
5. Choose minimal triggers that cover all violating paths.

## Workflow
- Build a protocol map: key contracts, roles, assets, mutable state.
- Draft invariants in plain language and math form.
- Identify legitimate exceptions in specs/audits and encode them explicitly.
- Decide if the invariant is transaction-scoped (pre/post) or call-scoped (per call id).
- Choose enforcement location (per-contract vs chokepoint) based on call routing.
- Flag upgradeability/proxy entrypoints and token integration assumptions.
- Pick observation strategy:
  - State comparisons for monotonicity and conservation.
  - Event-based accounting when internal state is opaque.
  - Call input parsing for authorization or parameter bounds.
- Map to triggers with the smallest blast radius.
- Enumerate edge cases (zero supply, empty vaults, proxy upgrades, nested batches).

## Rationalizations to Reject
- "Trigger on any call; it is simpler." This risks gas-limit reverts and false drops.
- "Post-state is enough." Many invariants need pre/post deltas.
- "Ignore batch or nested calls." Real protocols use them heavily.
- "We can skip edge cases like zero supply." These are common sources of false positives.

## Deliverable
- Invariant spec with: definition, data sources, trigger list, and edge cases.
- A candidate list of assertion functions with one invariant per function.

## References
- [Invariant Patterns](references/invariant-patterns.md)
- [Trigger Mapping Guide](references/trigger-mapping.md)
