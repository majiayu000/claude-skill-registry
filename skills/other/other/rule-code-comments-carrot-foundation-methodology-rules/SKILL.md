---
name: rule-code-comments
description: 'Rule mapping for code-comments'
---

# Rule code-comments

Apply this rule whenever work touches:
- `*.ts`
- `*.tsx`

Comments should add information that the code cannot express on its own. If the code can be made clear enough without a comment, prefer that approach.

### When to comment

Write a comment when:

- A business rule or domain constraint is not obvious from the code alone.
- A workaround exists for a known issue, library bug, or platform limitation.
- A non-trivial algorithm or calculation requires context about the approach chosen.
- A `TODO` marks future work that is tracked and assigned.

### When NOT to comment

Do not write a comment when:

- The function name, parameter names, and return type already explain the behavior.
- The comment merely restates the code in English.
- The comment exists only because the code is too complex; simplify the code instead.

### TSDoc for exports

Exported symbols may use TSDoc when additional guidance helps consumers:

```ts
/**
 * Computes the carbon credit score based on the mass balance and
 * methodology-specific weighting factors.
 *
 * Returns zero if the input document has no valid mass entries.
 */
export function computeCarbonCreditScore(input: MassBalance): number { ... }
```

Avoid boilerplate TSDoc that adds no value:

```ts
// Bad - repeats the signature
/**
 * @param input - the input
 * @returns the result
 */
export function computeCarbonCreditScore(input: MassBalance): number { ... }
```

### Commented-out code

Never commit commented-out code. If the code is no longer needed, delete it. Git history preserves everything. If you need to temporarily disable logic during development, remove it before committing.

### Stale comments

When modifying a function or behavior, review any adjacent comments. If a comment no longer matches reality, update or remove it in the same commit.
