---
name: tdd
description: Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants test-first development, or requests TDD workflow.
---

# Test-Driven Development

## Philosophy

Tests verify behavior through public interfaces, not implementation. Good tests survive refactors.

See `principles.md` for testing philosophy and anti-patterns.

## Workflow

### 1. Planning
- Confirm interface design with user
- List behaviors to test (prioritize critical paths)
- Get approval before writing code

### 2. Tracer Bullet
```
RED:   Write first test → fails
GREEN: Minimal code to pass → passes
```

### 3. Incremental Loop
For each remaining behavior:
```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:
- One test at a time
- Minimal code to pass
- No refactoring while RED

### 4. Refactor
Once all tests GREEN:
- Remove duplication
- Improve structure
- Tests must stay GREEN

## Anti-Pattern: Horizontal Slices

**DO NOT** write all tests first, then all implementation.
**DO** use vertical slices: one test → one implementation → repeat.

See `examples.md` for workflow demonstrations.
