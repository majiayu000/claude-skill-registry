---
name: 30-00-refactor-index
description: Refactoring primer index. Read this first before any refactor — it points you to the right guide for your situation. Progressive exploration, not bulk loading.
---

# 30.00 Refactor Index

Guides for restructuring code without breaking behavior. **Don't read them all** — match your situation, read that one.

### General (any language)

| ID | Guide | When to use |
|----|-------|-------------|
| `30.01` | Full refactor guide | Large multi-file refactor with extraction, wiring, verification |
| `30.02` | Convergence audit | Finding semantic duplication — different code doing the same thing |
| `30.03` | Test-driven refactoring | Writing compile-failing tests that define the refactor's end state |

### TypeScript

| ID | Guide | When to use |
|----|-------|-------------|
| `30.04` | Closure monolith decomposition | Splitting a 1000+ line closure into domain modules with shared refs |

## Quick decision aid

- **"This file is huge, where do I start?"** → `30.01`
- **"Different sessions wrote the same thing three ways"** → `30.02`
- **"How do I know the refactor is done?"** → `30.03`
- **"Everything is trapped in one closure"** → `30.04` (TS)
- **"Should I extract this into a new file?"** → `40.02` (module boundaries)
- **"Who owns this state I'm moving?"** → `40.01` (state ownership)
