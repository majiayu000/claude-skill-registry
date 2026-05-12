# Correctness Review Reference

## What to Review

Bugs, logic errors, and correctness problems: incorrect control flow, off-by-one errors, null/undefined access, type mismatches, broken error handling, race conditions, resource leaks, and state lifecycle bugs.

## Determination Criteria

Flag an issue only when ALL of these hold:

1. It meaningfully impacts the accuracy, performance, security, or maintainability of the code
2. The bug is discrete and actionable (not a general codebase issue or combination of multiple issues)
3. Fixing it does not demand rigor beyond what exists in the rest of the codebase
4. The author would likely fix the issue if aware of it
5. The bug does not rely on unstated assumptions about the codebase or author's intent
6. Speculation is insufficient — identify the parts of the code that are provably affected
7. The issue is clearly not an intentional change by the original author

## Priority Levels

- **P0** — Drop everything. Blocking release or operations. Only for universal issues that do not depend on assumptions about inputs
- **P1** — Urgent. Should be addressed in the next cycle
- **P2** — Normal. To be fixed eventually
- **P3** — Low. Nice to have

## What to Ignore

- Trivial style unless it obscures meaning or violates documented standards

**Verdict label:** `Correctness: <correct | incorrect>`
