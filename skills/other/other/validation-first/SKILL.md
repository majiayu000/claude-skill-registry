---
name: validation-first
description: Validation-first development - design state machine specifications from requirements, then execute CREATE -> VERIFY -> IMPLEMENT cycle. Use when developing with formal state machine specifications, invariants, and temporal properties before writing implementation code.
---

# Validation-first development

Define state machines from requirements before implementation. Specifications say what the system MUST do. Encode compile-time properties in types first, then layer state machine modeling for properties types cannot express.

**Modern insight (2025)**: State machines exist on a spectrum from runtime enums to compile-time typestates. Use the strongest mechanism available. XState v5 introduces actor model semantics -- state machines are now first-class concurrent entities, not just enum switches.

See [approaches](references/approaches.md) for language-specific state machine mechanisms.
See [examples](references/examples.md) for brief state machine patterns per language.
See [formal-tools](references/formal-tools.md) for specification and model checking tools.

---

## State Machine Taxonomy (decision guidance)

| Level | Mechanism | Strength | Use When |
|-------|-----------|----------|----------|
| **Typestate** (compile-time) | Generic type params, phantom data | Invalid transitions unrepresentable | Protocol APIs, builder patterns, Rust FFI |
| **Statecharts** (hierarchical) | Nested states, parallel regions | Complex workflows, entry/exit | Game state, multi-modal UI, XState |
| **Flat FSM** (runtime) | Enum + match/switch | Simple, auditable | Order lifecycle, connection mgmt |
| **Actor model** | Independent entities, message passing | Concurrent state | Distributed systems, Erlang/Elixir, XState v5 |

**Default choice**: Use the strongest mechanism the language supports. Typestate in Rust, sealed classes in Kotlin, discriminated unions in TypeScript.

## Validation Levels

```
Type system (strongest) > State machine > Contract > Runtime check (weakest)
```

---

## When to Apply

- Protocol implementations (network, API, auth flows)
- Workflow engines (approval chains, CI/CD pipelines)
- Concurrent/distributed systems (coordination state)
- Order lifecycle (e-commerce, payments, shipping)
- Connection/session management
- Actor systems with message-driven state
- Event sourcing aggregates (command validation against current state)

## When NOT to Apply

- Stateless REST endpoints
- Pure data transformations (map/filter/reduce)
- Simple CRUD without lifecycle
- Configuration parsing
- Batch processing without state

---

## Anti-patterns

- **Boolean soup**: `{ isLoading: true, isError: true, data: X }` -- contradictory states representable. Use discriminated unions instead.
- **Stringly-typed states**: `state: "pending"` with no exhaustiveness check
- **Partial transition coverage**: Some transitions undefined -- runtime "impossible" states
- **Split-brain**: State and behavior in separate modules -- changes require cross-module updates
- **Invariants at boundaries only**: Check invariants at every transition, not just entry/exit
- **Implicit transitions**: State changes scattered across codebase -- impossible to audit
- **State explosion without hierarchy**: Flat FSM with 50+ states -- use statecharts (nested states)

---

## Pseudocode Template

```
STATE MACHINE: <Name>
  STATES: S1 | S2 | S3
  VARIABLES: var1: type, var2: type
  INIT: var1 = val, state = S1
  ACTION name(args): PRE: guard -> POST: new_state, effects
  INVARIANT: condition_that_always_holds
```

## Event Sourcing Integration

When state machines guard event-sourced aggregates:
1. Command arrives -> validate against current aggregate state machine
2. If transition valid -> emit immutable event
3. State rebuilt from event replay
4. Invalid transitions rejected before events created -- impossible to corrupt event log

---

## Workflow (language-neutral)

1. **PLAN** -- Identify states, variables, actions, invariants from requirements. Draw state diagram.
2. **CREATE** -- Define state machine spec using pseudocode template. Choose mechanism level (typestate/FSM/actor).
3. **VERIFY** -- Type-check, confirm exhaustive matching on all states, validate invariants hold at every transition.
4. **IMPLEMENT** -- Target code mirrors spec. One state type, one transition function, one invariant check per concern.

---

## Constitutional Rules (Non-Negotiable)

1. **CREATE First**: Define state machine specification from plan
2. **Invariants Must Hold**: All invariants verified at every transition
3. **Actions Must Type**: All actions type-check with exhaustive matching
4. **Implementation Follows Spec**: Target code mirrors specification structure

## Validation Gates

| Gate | Pass Criteria | Blocking |
|------|---------------|----------|
| Typecheck | No errors; exhaustive match where language enforces it | Yes |
| Invariants | All invariant assertions pass after each action | Yes |
| Tests | All state transition tests pass | If present |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Specification verified, ready for implementation |
| 11 | Checker not available |
| 12 | Syntax/type errors in specification |
| 13 | Invariant violation detected |
| 14 | Specification tests failed |
| 15 | Implementation incomplete |
