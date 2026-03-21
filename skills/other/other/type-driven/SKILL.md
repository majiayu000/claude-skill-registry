---
name: type-driven
description: Type-driven development - design type specifications from requirements, then execute CREATE -> VERIFY -> IMPLEMENT cycle. Use when developing with refined types, state machines encoded in types, or proof-carrying types; enforces totality and exhaustive pattern matching.
---

# Type-driven development

Types encode the specification -- design from requirements before implementation. Make illegal states unrepresentable (Yaron Minsky). Parse, don't validate (Alexis King). For parsed opaque domain types within trusted boundaries, if the type compiles, the value is valid.

**Modern insight (2025)**: "Encode invariants in types, not runtime checks" is the evolved formulation. Type richness should match risk -- start simple, add complexity where bugs actually occur. Types serve AI-assisted development: they communicate intent better than comments and reduce LLM hallucinations.

See [patterns](references/patterns.md) for language-specific refined types, state machine techniques, and language-specific validation gates.
See [examples](references/examples.md) for brief "parse, don't validate" patterns per language.
See [formal-tools](references/formal-tools.md) for dependent type systems and verification tools.

---

## Parse, Don't Validate

- **Validate**: Check if data is valid -> return bool -> caller must remember check happened. Proof is lost.
- **Parse**: Transform untrusted data into typed value that proves validity -> return new type. Proof is preserved.
- **Consequence**: Once parsed into an opaque domain type, internal code within trusted boundaries receives typed values and should not re-validate the same invariant. Note: deserialization, casts, FFI, and unsafe escape hatches can bypass the type system -- runtime checks remain necessary at those boundaries.
- **Alexis King clarification**: Newtypes are convenient but encapsulation-dependent. Best for simple invariants. Phantom types and branded types provide richer guarantees.

## Making Illegal States Unrepresentable

1. **ADTs / Discriminated Unions**: Model business rules as sum types. `Payment = Pending | Processing { id } | Success { id, amount } | Failed { reason }`. Compiler ensures every case handled.
2. **Phantom/Branded Types**: Prevent accidental mixing of structurally identical but semantically different values (UserId vs PostId). Zero runtime cost.
3. **Typestate Pattern**: Encode valid method sequences in types. `Client<Disconnected>` has no `read()` method. Compile error if called wrong.
4. **Newtype Wrappers**: Lightweight validated wrappers. `EmailAddress(String)` with private constructor + validation in `new()`.

---

## When to Apply

- Domain modeling (money, email, permissions, IDs)
- State machines encoded in types (typestate pattern)
- Complex business rules with multiple valid configurations
- API boundary types -- parse external data into domain types
- Anywhere primitive obsession exists (raw strings, ints as IDs)
- Builder patterns requiring ordered construction steps

## When NOT to Apply

- Thin wrapper scripts with short lifespan
- Rapid prototyping where types add friction
- Languages without expressive type systems
- Configuration/glue code
- When type complexity exceeds domain complexity -- type gymnastics that obscure intent
- Internal code where a simple assertion suffices

---

## Anti-patterns

- **Primitive obsession**: Raw strings for emails, ints for money, unbranded IDs
- **Validating after construction**: If the constructor allows invalid values, the type is lying
- **Trusting external data**: JSON/API/user input must be parsed, never `as`-cast
- **Type holes**: Placeholder markers left in final code (language-specific: see [patterns](references/patterns.md))
- **Fixing types to match broken implementation**: Types never lie -- fix the code, not the types
- **Stringly-typed APIs**: `fn process(action: string)` instead of `fn process(action: Action)`
- **`as` casts bypassing type checker**: Escape hatches that negate type safety
- **Over-engineering with types**: Phantom types for every invariant -> complexity explosion; unreadable signatures defeat documentation purpose
- **Type gymnastics without clarity**: Complex generics/HKT that obscure intent -- worse than runtime validation

---

## The Reinforcing Cycle

```
Type-Driven Design (static proofs) -> reduces test scope needed
  -> Test-Driven Development (examples + edges) -> validates type assumptions
    -> Design by Contract (runtime boundaries) -> documents type guarantees
      -> Types + TDD + DbC = highest confidence software
```

---

## Workflow (language-neutral)

1. **PLAN** -- Identify value, relationship, state, and proof constraints from requirements
2. **CREATE** -- Write type definitions first. Use the language's mechanism for incomplete implementations (typed holes, abstract members, stubs) to sketch the shape. Follow "parse, don't validate" at boundaries.
3. **VERIFY** -- Type-check with the project's strict mode. Zero incomplete markers, exhaustive matching, no escape hatches. See [patterns](references/patterns.md) for language-specific check commands and hole markers.
4. **IMPLEMENT** -- Fill in bodies guided by types. The type checker is your pair programmer.

---

## Constitutional Rules (Non-Negotiable)

1. **CREATE Types First**: All type definitions before implementation
2. **Types Never Lie**: If it doesn't type-check, fix implementation (not types)
3. **Holes Before Bodies**: Leave function bodies unimplemented and let the type checker report what is required before filling them in
4. **Exhaustiveness Enforced**: All match/switch cases covered by the compiler
5. **Pattern Match Exhaustive**: All cases covered

## Validation Gates

| Gate | Pass Criteria | Blocking |
|------|---------------|----------|
| Types Compile | Type checker reports no errors | Yes |
| Exhaustiveness | No missing match/switch cases | Yes |
| Holes | Zero incomplete implementation markers (language-specific -- see [patterns](references/patterns.md)) | Yes |
| Target Build | Full build succeeds | Yes |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Types verified, implementation complete |
| 11 | Type checker not available |
| 12 | Type check failed |
| 13 | Exhaustiveness/totality check failed |
| 14 | Type holes remaining |
| 15 | Target implementation failed |
