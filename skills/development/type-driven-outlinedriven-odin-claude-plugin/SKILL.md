---
name: type-driven
description: 'Use when the work is modeling a domain, encoding a state machine, hardening an API boundary, making invalid states unrepresentable, or parsing instead of validating. Not for TypeScript-specific doctrine — use typescript-best-practices; not for remote, credential, publish, deploy, or irreversible changes.'
---

# Type-driven development

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The work is modeling a domain, encoding a state machine, hardening an API boundary, making invalid states unrepresentable, or parsing instead of validating. |
| Authority | Reversible local. No file, VCS, credential, paid, published, or remote mutation. |
| Side effect | Rewrites domain types, public signatures, and affected callers and tests to the new algebraic model. |
| Done | Invalid states are unconstructible, matches are exhaustive, boundaries parse, and no scattered post-hoc validation remains. |

## Inputs

Required: the domain problem, data model, or API surface to encode.
Optional: existing types or callers to refactor.

## Refusals

- Will not add runtime guards to fix a type-design failure — fix the type design.
- Will not add a wildcard arm to silence a non-exhaustive match — add the missing variant.
- Will not proceed with type holes or incomplete bodies.
- Will not use this approach when the language lacks ADTs, sealed hierarchies, or equivalent sum-type support — skip and report.

## Procedure

1. **Plan.** State the domain in one paragraph. List all valid states, all invalid states, and every operation with its preconditions and postconditions. If any operation is partial, mark it as such. **Done when:** the domain is stated with valid states, invalid states, and operations listed.
2. **Design types first.** For each invalid state, write a type that the compiler prevents. Use ADTs, phantom types, branded types, newtype wrappers, sealed hierarchies, or opaque types, whichever the language supports. Do not write implementation bodies until all types compile. **Done when:** all types compile and every invalid state is unrepresentable.
3. **Parse at boundaries.** For every untrusted input (external data, deserialization, FFI, user input), write a `parse` constructor that returns the new type. Do not return `bool` and defer validity to callers. **Done when:** every untrusted input boundary has a parse function returning the new type.
4. **Exhaustive matching.** Encode state machine transitions as exhaustive `match`/`switch`/`visit` on the sum type. Compiler warnings on incomplete arms are failures. **Done when:** every state-machine transition is an exhaustive match with no wildcard arms.
5. **Verify.** Run the language's strict type checker and exhaustiveness check. Fix the type design, not the implementation, when the checker reports an illegal state is representable. **Done when:** the type checker and exhaustiveness check pass.
6. **Build.** Run the full target build. Implement the bodies guided by the types. **Done when:** the target build passes.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| Unsupported language | If the language lacks ADTs, sealed hierarchies, or equivalent sum-type support, skip this approach and report. |
| Type checker failure | Block. Fix the type design until the invalid state is unrepresentable. Do not add runtime guards. |
| Non-exhaustive match | Compile-time failure. Add the missing variant to the type, not a wildcard arm. |
| Invalid state remains representable | Block. The type design is insufficient; iterate until the compiler enforces the invariant. |
| Type holes remain | Block. Complete all incomplete bodies or remove the holes before proceeding. |
| Build fails | Block. Resolve implementation errors until the target build passes. |

## Output

A domain type system where every algebraic constructor is present, every boundary has a parse function returning the new type, every state-machine variant is matched exhaustively, and no runtime validation scattered outside the parse layer remains.
