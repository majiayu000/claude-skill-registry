---
name: code-review-ts
description: TypeScript-specific code review guidelines focusing on type safety and TypeScript idioms
category: development
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# TypeScript Code Review

Includes all guidelines from code-review skill, plus TypeScript-specific rules.

## Prefer Strong Types; Avoid Type Inspection on Known Types

The reviewer MUST:
- Avoid runtime type inspection (`typeof`, `instanceof`) when the type is known or enforced by TypeScript.
- Restrict runtime checks to untyped inputs or boundary validation (e.g., API payloads).

Discouraged:
```ts
function labelCount(count: number) {
  if (typeof count === "number") return `${count} items`;
  return "n/a";
}
```

## Avoid `any` and `unknown` When Possible

The reviewer MUST:
- Reject `any` unless it is a last-resort boundary with clear justification.
- Require immediate narrowing of `unknown` with explicit type guards.

The reviewer SHOULD:
- Prefer generics, `satisfies`, and well-scoped interfaces over `any`.

## Type Casting Must Be Justified

The reviewer MUST:
- Require a comment or invariant when using `as`, non-null assertions (`!`), or unsafe casts.
- Prefer `satisfies` or type guards before asserting a type.

Acceptable with proof:
```ts
const payload = parse(input) as Payload; // validated by parse schema
```

## Additional TypeScript Guidelines

The reviewer SHOULD:
- Encourage use of strict TypeScript compiler options
- Prefer `readonly` for immutable data
- Use discriminated unions over type assertions
- Prefer `unknown` over `any` for external data
- Use template literal types where appropriate