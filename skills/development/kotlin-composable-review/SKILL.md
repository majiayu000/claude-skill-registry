---
name: kotlin-composable-review
description: Strict technical code review for Kotlin Jetpack Compose. Analyzes @Composable functions for recomposition issues, stability violations, memory leaks, state management antipatterns, accessibility gaps, and performance problems.
---

# Kotlin Composable Code Review

Strict technical code review skill for Jetpack Compose. Identifies bugs, performance issues, and architectural violations.

## When to Use

- Reviewing any `@Composable` function
- Analyzing recomposition and stability issues
- Checking state management patterns
- Validating side effect usage
- Reviewing accessibility implementation
- Auditing memory leak potential

## Review Categories

1. **Recomposition & Stability** - Unstable parameters, inline lambdas
2. **State Management** - Lifecycle-aware collection, state hoisting
3. **Side Effects** - LaunchedEffect, DisposableEffect usage
4. **Memory Leaks** - Context leaks, lambda captures
5. **LazyList** - Keys, item stability
6. **Modifier Chain** - Propagation, ordering
7. **Remember & Derivation** - Expensive ops, derivedStateOf
8. **Accessibility** - Semantics, touch targets
9. **Architecture** - Route/Screen separation
10. **Preview Quality** - State coverage, configurations

## Severity Levels

| Level | Criteria |
|-------|----------|
| CRITICAL | Bugs, crashes, memory leaks, data loss |
| HIGH | Performance degradation, architectural violations |
| MEDIUM | Suboptimal patterns that scale poorly |
| LOW | Conventions, readability, minor improvements |

## Verdict Criteria

| Verdict | Criteria |
|---------|----------|
| REJECT | Any CRITICAL, or 3+ HIGH |
| NEEDS_CHANGES | Any HIGH, or 3+ MEDIUM |
| APPROVED | No HIGH/CRITICAL, ≤2 MEDIUM |

## References

- `references/review-checklist.md` - Complete technical checklist
- `references/architectural-patterns.md` - Route/Screen, state patterns
- `references/naming-conventions.md` - File and function naming
