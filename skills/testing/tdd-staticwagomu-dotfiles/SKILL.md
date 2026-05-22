---
name: tdd
description: Guide Test-Driven Development using Kent Beck's Red-Green-Refactor cycle. Use when writing tests, implementing features via TDD, or following plan.md test instructions.
---

# INSTRUCTIONS

Follow Kent Beck's TDD and Tidy First principles using the three-phase workflow:

1. **RED** - `/tdd:red` - Write ONE small failing test
2. **GREEN** - `/tdd:green` - Make it pass with minimal code, then commit
3. **REFACTOR** - `/tdd:refactor` - Improve structure without changing behavior, commit each step

## Workflow Pattern

```
/tdd:red → write failing test → /tdd:green → pass test → /git:commit
                                                              ↓
        ← next feature ← /tdd:red ← satisfied? ← /tdd:refactor (repeat as needed)
```

## Core Principles

- **One test at a time**: Each RED adds exactly ONE failing test
- **Minimal code**: GREEN phase writes just enough to pass
- **Never skip REFACTOR**: Every TDD cycle must complete all three phases
- **Tidy First**: Separate structural changes (refactor) from behavioral changes (feat/fix)
- **Small commits**: Commit after GREEN, commit after EACH refactor step

## Strategy Selection (GREEN Phase)

| Confidence | Strategy | Use When |
|------------|----------|----------|
| Low | **Fake It** | Return constant, generalize later |
| High | **Obvious Implementation** | Solution is clear |
| Generalizing | **Triangulation** | Add test to break a fake |

## Quality Standards

- Eliminate duplication between test and production code
- Express intent through clear naming
- Keep methods small and focused
- Run ALL tests after EVERY change
