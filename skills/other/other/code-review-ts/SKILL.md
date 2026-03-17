---
name: code-review-ts
description: TypeScript-specific code review guidelines focusing on type safety and TypeScript idioms.
Use when: (1) reviewing TypeScript pull requests, (2) auditing type-safety regressions,
(3) checking TS API and error-handling patterns.

category: audit
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# TypeScript Code Review Guidelines

This guide defines how the reviewer evaluates a TypeScript pull request.

## Baseline Assumptions
- The code compiles.
- All tests pass.

## Normative Words
- MUST: Mandatory. Not following this is a violation of the guide.
- MUST NOT: Forbidden.
- SHOULD: Recommended in almost all cases; exceptions need a strong reason.
- SHOULD NOT: Generally discouraged; only do it with clear justification.
- MAY: Optional; use judgment.

## Scope and Priorities

The reviewer MUST:
- Focus on the actual diff and its impact.
- Prioritize in this order:
  1. Correctness and safety (including error handling policy).
  2. Public API and external behavior.
  3. Concurrency and performance issues with real impact.
  4. Readability, idioms, maintainability.

The reviewer MUST NOT:
- Invent business logic or protocol rules not implied by the code or docs.
- Demand large unrelated refactors unless there is a clear correctness or safety concern.

## Review Process

1. Read the PR description and understand the intent
2. Review the diff file by file
3. For each change, consider:
   - Does this introduce bugs or security issues?
   - Is the API appropriate?
   - Are edge cases handled?
   - Is error handling adequate?
4. Provide actionable, specific feedback
5. Distinguish blocking issues from suggestions

## Feedback Format

Use clear prefixes:
- **MUST FIX**: Blocking issue that needs resolution
- **SHOULD FIX**: Strong recommendation
- **CONSIDER**: Optional improvement
- **QUESTION**: Clarification needed

---

## TypeScript-Specific Rules

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
- Require a comment or invariant when using `as`, non-null assertions, or unsafe casts.
- Prefer `satisfies` or type guards before asserting a type.

Acceptable with proof:
```ts
const payload = parse(input) as Payload; // validated by parse schema
```

## Avoid Closures That Capture Large Scopes

The reviewer MUST:
- Flag arrow functions or closures that capture `this`, `init`, `options`, or request bodies when passed to long-lived event listeners.
- Prefer `bind()` so only the necessary reference is retained.

An arrow function such as `() => controller.abort()` captures the surrounding scope, which can include request bodies and other large objects. If a long-lived `AbortSignal` is used, the event listener prevents those objects from being garbage-collected for the lifetime of the signal.

Discouraged:
```ts
signal.addEventListener("abort", () => controller.abort());
```

Preferred:
```ts
signal.addEventListener("abort", controller.abort.bind(controller));
```

## Circular Dependency Detection

The reviewer MUST:
- Flag import cycles when errors like "Cannot access 'X' before initialization" appear
- Recommend `madge --circular --extensions ts,tsx src/` for cycle detection

Common resolution strategies:
1. Extract shared dependencies to separate modules
2. Use dependency injection instead of direct imports
3. Use `import type` for type-only imports (erased at runtime)
4. Restructure barrel files (`index.ts`) to avoid re-export cycles

The reviewer SHOULD:
- Check for barrel file re-export cycles (common source of issues)
- Verify Jest/Vitest module resolution matches bundler behavior

## Additional TypeScript Guidelines

The reviewer SHOULD:
- Encourage use of strict TypeScript compiler options
- Prefer `readonly` for immutable data
- Use discriminated unions over type assertions
- Prefer `unknown` over `any` for external data
- Use template literal types where appropriate