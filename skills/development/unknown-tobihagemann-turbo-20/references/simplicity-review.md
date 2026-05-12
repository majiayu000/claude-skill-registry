# Simplicity Review Reference

## Review Instructions

Focus on single-file simplicity: reuse, quality, efficiency, and clarity issues that surface within an individual file or a small set of changes.

For reuse, identify analogous utilities, helpers, or shared modules elsewhere in the project before suggesting a rewrite. Common locations are utility directories, shared modules, and files adjacent to the changed ones.

## What to Review

### Reuse

- **Duplicate functionality** — new functions that duplicate existing utilities; suggest the existing function to use instead
- **Inline logic that could use an existing utility** — hand-rolled string manipulation, manual path handling, custom environment checks, and similar patterns where a utility already exists

### Single-File Quality

- **Redundant state** — state that duplicates existing state, cached values that could be derived, reactive subscriptions that could be direct calls
- **Parameter sprawl** — new parameters added to a function instead of generalizing or restructuring existing ones
- **Copy-paste with slight variation** — near-duplicate code blocks within the same file that should be unified with a shared abstraction
- **Leaky abstractions** — exposing internal details that should be encapsulated, or breaking existing abstraction boundaries
- **Stringly-typed code** — raw strings used where constants, enums, or dedicated types already exist in the codebase
- **Unnecessary wrapper nesting** — container elements or wrapper layers that add no structural or layout value

### Efficiency

- **Unnecessary work** — redundant computations, repeated file reads, duplicate network/API calls, N+1 patterns
- **Algorithmic complexity** — nested iterations, repeated linear searches replaceable by sets/maps, missing early exits
- **Missed concurrency** — independent operations run sequentially when they could run in parallel
- **Hot-path bloat** — new blocking work added to startup or per-request hot paths
- **Unnecessary existence checks** — pre-checking file/resource existence before operating (TOCTOU anti-pattern); operate directly and handle the error
- **Memory** — unbounded data structures, missing cleanup, resource leaks
- **Overly broad operations** — reading entire files when only a portion is needed, loading all items when filtering for one

### Clarity and Standards

- **Project standards** — coding conventions from AGENTS.md not followed (import sorting, naming conventions, component patterns, error handling patterns, module style)
- **Unnecessary complexity** — deep nesting, redundant abstractions, unclear variable or function names, comments that describe obvious code, nested ternary operators (prefer switch/if-else chains), redundant boolean comparisons (e.g., `x == true` instead of `x`)
- **Unclear code** — overly compact one-liners that sacrifice readability; explicit code is better than clever code
- **Over-simplification** — too many concerns combined into a single function or component, helpful abstractions removed that were aiding code organization, "fewer lines" prioritized over readability
- **Dead weight** — unnecessary comments, redundant code, abstractions that add indirection without value

## Determination Criteria

Flag an issue only when ALL of these hold:

1. The issue meaningfully impacts readability, maintainability, correctness, or performance
2. The issue is discrete and actionable
3. A specific fix is obvious (reuse existing utility X, remove redundant state Y, collapse nested wrapper Z)
4. The fix does not demand rigor beyond what exists in the rest of the codebase
5. The author would likely accept the fix if aware of it

## Priority Levels

- **P0** — Severe efficiency problem on a hot path, or a reuse miss that duplicates a load-bearing utility
- **P1** — Clear duplication, leaky abstraction, or efficiency issue with meaningful impact
- **P2** — Moderate clarity, efficiency, or reuse opportunity
- **P3** — Minor style or readability nit

## What to Ignore

- Style-only differences that do not obscure meaning or violate documented standards
- Micro-optimizations with no measurable impact

**Extra metadata:** `**Category:** <reuse | quality | efficiency | clarity>`

**Verdict label:** `Simplicity: <clean | issues found>`
