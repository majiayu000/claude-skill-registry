---
name: combine-code-review
description: Reviews Combine framework code for memory leaks, operator misuse, and error handling. Use when reviewing code with import Combine, AnyPublisher, @Published, PassthroughSubject, or CurrentValueSubject.
---

# Combine Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Publishers, Subjects, AnyPublisher | [references/publishers.md](references/publishers.md) |
| map, flatMap, combineLatest, switchToLatest | [references/operators.md](references/operators.md) |
| AnyCancellable, retain cycles, [weak self] | [references/memory.md](references/memory.md) |
| tryMap, catch, replaceError, Never | [references/error-handling.md](references/error-handling.md) |

## Review Checklist

- [ ] All `sink` closures use `[weak self]` when self owns cancellable
- [ ] No `assign(to:on:self)` usage (use `assign(to: &$property)` or sink)
- [ ] All AnyCancellables stored in Set or property (not discarded)
- [ ] Subjects exposed as `AnyPublisher` via `eraseToAnyPublisher()`
- [ ] `flatMap` used correctly (not when `map + switchToLatest` needed)
- [ ] Error handling inside `flatMap` to keep main chain alive
- [ ] `tryMap` followed by `mapError` to restore error types
- [ ] `receive(on: DispatchQueue.main)` before UI updates
- [ ] PassthroughSubject for events, CurrentValueSubject for state
- [ ] Future wrapped in Deferred when used with retry

## When to Load References

- Reviewing Subjects or publisher selection → publishers.md
- Reviewing operator chains or combining publishers → operators.md
- Reviewing subscriptions or memory issues → memory.md
- Reviewing error handling or try* operators → error-handling.md

## Review Questions

1. Are all subscriptions being retained? (Check for discarded AnyCancellables)
2. Could any sink or assign create a retain cycle with self?
3. Does flatMap need to be switchToLatest for search/autocomplete?
4. What happens when this publisher fails? (Will it kill the main chain?)
5. Are error types preserved or properly mapped after try* operators?
