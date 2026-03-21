---
name: design-by-contract
description: Design-by-Contract (DbC) development - design contracts from requirements, then execute CREATE -> VERIFY -> TEST cycle. Use when implementing with formal preconditions, postconditions, and invariants across any language.
---

# Design-by-Contract development

Contracts (PRE/POST/INV) define behavioral specification -- design from requirements before code exists. Formalized as Hoare Triples: `{P} C {Q}` where P=precondition, C=code, Q=postcondition.

**Modern insight (2025)**: DbC complements LLM-generated code by serving as safety guardrails -- contracts clarify intent and prevent AI from breaking integrations. Spec-driven development (2025) positions contracts as "executable specifications."

See [libraries](references/libraries.md) for language-specific contract tools.
See [examples](references/examples.md) for brief contract patterns per language.

---

## Verification Hierarchy

Use compile-time verification before runtime contracts. If a property can be verified statically, do NOT add a runtime contract.

```
Static Assertions (compile-time) > Test/Debug Contracts > Runtime Contracts
```

| Property | Static | Test | Debug | Runtime |
|----------|--------|------|-------|---------|
| Type size/alignment | `static_assert` | - | - | - |
| Null/type safety | Type checker | - | - | - |
| Exhaustiveness | Pattern match | - | - | - |
| Expensive O(n)+ | - | test_ensures | - | - |
| Internal invariants | - | - | debug_invariant | - |
| Public API input | - | - | - | requires |
| External/untrusted | - | - | - | Always required |

---

## When to Apply

- Public API boundaries -- callers need clear contracts
- Complex state invariants -- balance >= 0, capacity limits
- Financial/business rule enforcement -- regulatory compliance
- Untrusted external data -- always validate at boundaries
- Multi-component integration points -- service contracts
- AI-generated code -- contracts serve as guardrails for LLM output

## When NOT to Apply

- Internal helpers with obvious behavior
- Simple getters/setters, trivial pure functions
- Performance-critical hot paths (runtime contract overhead)
- Prototyping -- contracts add ceremony
- When the type system already enforces the property (prefer static)

---

## Anti-patterns

- **Contracts duplicating type system**: If types enforce it, don't add a runtime check
- **Runtime checks for compile-time properties**: Wrong verification level
- **Contracts without violation tests**: Untested contracts are untrusted
- **Contract fatigue**: Decorating everything -- focus on boundaries and invariants
- **Postconditions restating implementation**: `ensures(result == x - y)` for `subtract(x, y)` adds nothing
- **Forgetting old() semantics**: Postconditions often need the pre-state value
- **Ignoring contract inheritance**: Preconditions weaken in subtypes (contravariance), postconditions strengthen (covariance) -- Liskov Substitution Principle

---

## Contract Inheritance Rules

- **Preconditions**: Can be weakened (loosened) in subtypes -- accept more
- **Postconditions**: Can be strengthened (tightened) in subtypes -- guarantee more
- **Invariants**: Strengthened in subtypes; never weakened
- This enforces Liskov Substitution automatically.

## DbC vs Defensive Programming (decision guidance)

| Approach | Philosophy | When |
|----------|-----------|------|
| **Defensive** | Don't trust caller; always check | Unknown callers, legacy APIs, untrusted input |
| **DbC** | Clear contract; caller handles pre, method handles post | Internal APIs, well-scoped teams, correctness-critical |
| **Hybrid** | Defensive at boundary; DbC internally | Best practice for modern systems |

---

## Contract Formalization

```
Operation: withdraw(amount)

Preconditions:
  PRE-1: amount > 0
  PRE-2: amount <= balance
  PRE-3: account.status == Active

Postconditions:
  POST-1: balance == old(balance) - amount
  POST-2: result == amount

Invariants:
  INV-1: balance >= 0
```

---

## Workflow (language-neutral)

1. **PLAN** -- Extract PRE/POST/INV from requirements. Formalize each with ID and description.
2. **CREATE** -- Enforce contracts at the appropriate verification level per the hierarchy: static proof, test assertion, debug check, or runtime guard. Reserve runtime contracts for public API boundaries and untrusted input.
3. **VERIFY** -- Run static analysis and build. Contracts must compile and lint.
4. **TEST** -- Write violation tests proving contracts catch bad inputs. Every PRE/POST/INV has a test.

---

## Constitutional Rules (Non-Negotiable)

1. **CREATE All Contracts**: Implement every PRE, POST, INV from plan at the appropriate verification level per the hierarchy
2. **Enforcement Enabled**: Runtime contracts, where used, must be active (not compiled out or disabled)
3. **Violations Caught**: Tests prove contracts work -- static contracts verified by type checker, runtime contracts by violation tests
4. **Documentation**: Each contract traces to requirement

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All contracts enforced and tested |
| 1 | Precondition violation in production code |
| 2 | Postcondition violation in production code |
| 3 | Invariant violation in production code |
| 11 | Contract library not installed |
| 13 | Runtime assertions disabled |
| 14 | Contract lint failed |
