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

## Hard gates (before you report findings)

Complete in order. Do not skip ahead while a prior gate is open.

1. **Scope** — **Pass:** You name at least one file or type under review that imports Combine or uses APIs from the Quick Reference (e.g. `AnyPublisher`, `@Published`, `PassthroughSubject`). If none apply, stop with “out of scope.”
2. **Subscription retention** — **Pass:** For each `sink`, `assign`, and `store(in:)` in scope, you state where the `AnyCancellable` is retained (property, `Set`, task lifetime) or mark **ephemeral** with a one-line reason (e.g. synchronous one-shot that cannot outlive caller). If you cannot tell from the snippet, say **unknown** and ask for surrounding storage, do not assume safe.
3. **Retain-cycle claim** — **Pass:** **Confirmed** leak findings state the capture chain (e.g. self → stored cancellable → closure strongly capturing self). Label suspected cases **risk** / **verify**, not confirmed leaks. When arguing safety, cite `[weak self]`, `[unowned self]`, or non-capturing patterns you relied on.
4. **UI / main thread** — **Pass:** For updates to UIKit/SwiftUI from a chain, you either point to `receive(on: DispatchQueue.main)`, `@MainActor`, or equivalent before the UI work, **or** flag missing scheduling with `file:line`.
5. **Severity and checklist** — **Pass:** Every **high** or **critical** item includes `file:line` (or exact pasted lines) and names which **Review Checklist** row it breaks. Lower-severity notes may omit line numbers but must still be reproducible from named files.

## Review Questions

1. Are all subscriptions being retained? (Check for discarded AnyCancellables)
2. Could any sink or assign create a retain cycle with self?
3. Does flatMap need to be switchToLatest for search/autocomplete?
4. What happens when this publisher fails? (Will it kill the main chain?)
5. Are error types preserved or properly mapped after try* operators?
