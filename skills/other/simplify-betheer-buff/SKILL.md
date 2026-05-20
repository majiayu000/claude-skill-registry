---
name: buff-simplify
description: This skill should be used when the user asks to "simplify the code", "clean up this function", "reduce complexity", "run /buff:simplify", "refactor for clarity", "make this code cleaner", "reduce nesting", "this function is too long", or any request to reduce code complexity or improve clarity without changing behavior.
version: 0.2.0
argument-hint: "[file] [start-end line range]"
allowed-tools: Read, Edit, Grep, Bash
---

# buff-simplify

The simplify skill is a scalpel, not a bulldozer. Analyze the target code for complexity hotspots, rank them, then fix only the worst offenders. Never touch what doesn't need touching. Never change behavior — only clarity.

## Core principle

**Simplify only what earns it.** A function that is long but clear does not need simplification. A short function with 5 nested conditionals does. Measure first, act second.

## Complexity metrics (ranked by impact)

Score each function/block against these metrics:

| Metric | Threshold | Score |
|---|---|---|
| Cyclomatic complexity | > 10 branches | +3 |
| Nesting depth | > 4 levels | +3 |
| Function length | > 50 lines | +2 |
| Parameter count | > 5 params | +2 |
| Duplicate logic | 3+ similar blocks | +2 |
| Unclear naming | opaque abbreviations | +1 |
| Mixed abstraction levels | high+low in same function | +1 |

Rank all functions by total score. Target the top 3 by default.

## Scope resolution

| Invocation | Scope |
|---|---|
| `/buff:simplify` | Current file — analyze all, fix top 3 hotspots |
| `/buff:simplify src/auth.ts` | Specified file — same |
| `/buff:simplify 40-80` | Lines 40-80 of current file only |
| `/buff:simplify src/auth.ts 40-80` | Lines 40-80 of specified file |

For line range scope: do not read the full file if a range is specified — only read what's needed.

## Workflow

1. Read the target file (or range)
2. Score all functions/blocks
3. Select top 3 by score (or all in range if range-scoped)
4. For each hotspot: apply one simplification technique
5. Output terse diff-style report
6. Apply changes

Never simplify more than 3 hotspots per invocation unless user explicitly asks. Fixing too much at once creates noise and makes the diff hard to review.

## Simplification techniques

Apply one technique per hotspot, matched to the top scoring metric:

| Metric | Technique |
|---|---|
| Nesting depth > 4 | Early return — invert conditions and return/throw at top |
| Function length > 50 | Extract function — split into named single-responsibility helpers |
| Magic values | Named constants — `MAX_RETRIES`, `TIMEOUT_MS`, etc. |
| Complex conditions | Named predicate — `const isEligible = ...` before the `if` |
| Parameter count > 5 | Config object — replace positional params with a single options object |

## What never to touch

- **Imports** — never reorder, remove, or restructure imports unless they are provably unused
- **Type signatures** — never change a type annotation unless it is wrong (a type bug)
- **Public API** — never rename exported symbols (breaking change)
- **Comments** — never remove comments, even if you'd phrase them differently
- **Test files** — never simplify tests; test verbosity is intentional
- **Performance-sensitive code** — do not simplify if the pattern exists for performance

If a type signature looks wrong, report it as a validate finding, not a simplify change.

## Output format

```
## Simplify — src/auth.ts

### Hotspot 1: validatePermissions() [score: 6]
  Nesting depth: 5 → reduced to 2 via early return
  Lines 42-67

### Hotspot 2: buildQuery() [score: 5]
  Function length: 72 lines → extracted 2 helpers
  Lines 89-161

### Hotspot 3: handleError() [score: 3]
  Magic values: 3 → named constants
  Lines 12-18

Changes: 3 functions simplified · behavior unchanged
```

Always state "behavior unchanged" only after verifying the simplification is semantically equivalent.

## Counterfeit integration

Read from `.buff/memory/preferences.json`:
- `code_style.naming` → apply correct naming convention when extracting functions/constants
- `code_style.error_handling` → preserve the user's preferred error handling pattern when extracting
