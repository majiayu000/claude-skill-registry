---
name: tidying
description: Guide structural code improvements using Kent Beck's Tidy First methodology. Use when seeing messy code, before making behavioral changes, after completing features, or discussing when to clean up code.
---

# INSTRUCTIONS

Apply Kent Beck's "Tidy First?" philosophy: small, safe structural changes that improve code without changing behavior. Tidying is separate from feature work and gets its own commits.

## Core Principle

> "Tidying is a special kind of refactoring... tidying is small, and you never need to tidy."

Tidyings are:
- **Small**: Minutes, not hours
- **Safe**: Structure only, no behavior change
- **Optional**: You choose when (or if) to tidy
- **Separate**: Own commits, distinct from behavioral changes

## When to Tidy: The Three Timings

### Tidy First (Before Behavior Change)
**Trigger**: You need to change code that's hard to understand or modify

Use when:
- Reading code takes longer than it should
- The change you need to make would be simpler if code were cleaner
- Coupling makes the change risky

```
/tidy:first → structural improvements → /git:commit (refactor:)
           → now make behavioral change → /git:commit (feat:/fix:)
```

### Tidy After (After Behavior Change)
**Trigger**: You just finished a feature and see improvement opportunities

Use when:
- The working code revealed better structure possibilities
- You added duplication to make tests pass (TDD GREEN phase)
- You now understand the domain better

```
behavioral change → /git:commit (feat:/fix:)
                 → /tidy:after → cleanup → /git:commit (refactor:)
```

### Tidy Later (Add to Backlog)
**Trigger**: Tidying would take too long or distract from current work

Use when:
- The tidying is substantial (more than a few minutes)
- You're in flow on something else
- The code works and tidying can wait

```
Note the opportunity → add to backlog/TODO → continue current work
```

## Tidying Catalog

Small, safe structural improvements:

| Tidying | Description |
|---------|-------------|
| **Guard Clauses** | Replace nested conditionals with early returns |
| **Dead Code** | Remove unused code (don't comment out—delete) |
| **Normalize Symmetries** | Make similar code look similar |
| **Extract Helper** | Pull out a chunk that does one thing |
| **Inline** | Remove unhelpful abstraction |
| **Rename** | Make names reveal intent |
| **Reorder** | Put related code together |
| **Chunk Statements** | Add blank lines to group related statements |
| **Explaining Variable** | Replace complex expression with named variable |
| **Explaining Constant** | Replace magic number/string with named constant |

## Decision Framework

When you encounter messy code, ask:

```
1. Does this code need to change for my current task?
   No  → Tidy Later (or never)
   Yes → Continue to 2

2. Would tidying make my change easier/safer?
   No  → Make behavioral change, then consider Tidy After
   Yes → Continue to 3

3. Is the tidying small (< 15 minutes)?
   No  → Tidy Later, make behavioral change anyway
   Yes → Tidy First, then make behavioral change
```

## Integration with TDD

Tidying complements TDD's REFACTOR phase:

- **TDD REFACTOR**: Remove duplication introduced during RED→GREEN
- **Tidy First/After**: Broader structural improvements, not tied to a specific test

When using TDD:
1. `/tdd:red` → `/tdd:green` → `/tdd:refactor` (remove test-code duplication)
2. Optionally: `/tidy:after` for broader cleanup
3. Repeat

## Commit Discipline

- **Every tidying gets its own commit**: `refactor: <what you tidied>`
- **Never mix tidying with behavioral changes**: Separate commits
- **Small commits**: One tidying per commit when possible

This separation:
- Makes code review easier
- Enables safe reverts
- Documents intent clearly

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Big Bang Refactor | Risky, hard to review | Many small tidyings |
| Tidying + Feature | Obscures both changes | Separate commits |
| Speculative Tidying | Waste if code changes | Tidy what you're touching |
| Comment-Out Code | Creates noise | Delete it (git has history) |
| Tidying Forever | Procrastination | Time-box, then ship |

## Reference

Based on: *Tidy First?* by Kent Beck (2023) - A practical guide to when and how to make structural improvements to code.
