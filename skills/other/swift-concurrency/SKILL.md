---
name: swift-concurrency
description: "Swift concurrency: async/await, Actor, Task, Sendable patterns."
user-invocable: false
context: fork
agent: swift-general-engineer
routing:
  triggers:
    - "swift concurrency"
    - "swift async await"
    - "Swift Actor"
    - "Swift Task group"
  category: swift
  pairs_with:
    - swift-testing
---

# Swift Structured Concurrency

Pattern catalog for Swift's structured concurrency model: async/await, Actors, TaskGroups, AsyncSequence, Sendable, and cancellation. Load the reference file matching the developer's question.

## Reference Loading Table

| Signal | Reference File | Content |
|--------|---------------|---------|
| async/await, Task, Sendable | references/fundamentals.md | async/await patterns, Task/Task.detached, Sendable/@Sendable |
| Actor, @MainActor, nonisolated | references/actor-isolation.md | Actor isolation, MainActor UI confinement, nonisolated opt-out |
| TaskGroup, AsyncSequence, AsyncStream, cancellation | references/task-patterns.md | Structured concurrency, rate-limited groups, streams, cancellation |
| Failure modes, common mistakes | references/preferred-patterns.md | Blocking MainActor, task leaking, actor reentrancy hazard |

## Key Conventions

- **Prefer structured concurrency** -- use `TaskGroup` over loose `Task { }` whenever possible; structured tasks propagate cancellation and errors automatically.
- **Mark types Sendable** -- enable strict concurrency checking (`-strict-concurrency=complete`) and resolve all warnings before they become errors in Swift 6.
- **Use actors for shared mutable state** -- avoid manual locks; actors provide compiler-verified safety.
- **Cancel what you create** -- every `Task` stored in a property should have a corresponding cancellation path.
- **Minimize @MainActor surface** -- isolate only the UI layer; keep business logic and networking off the main actor.

## References

- `references/fundamentals.md` -- async/await, Task, Sendable basics
- `references/actor-isolation.md` -- Actor, @MainActor, nonisolated
- `references/task-patterns.md` -- TaskGroup, AsyncSequence, AsyncStream, cancellation
- `references/preferred-patterns.md` -- blocking, leaking, reentrancy mistakes
