---
name: swift
description: "Swift development: concurrency patterns, async/await, actors, testing with XCTest and Swift Testing framework."
user-invocable: false
context: fork
agent: swift-general-engineer
routing:
  triggers:
    - "swift concurrency"
    - "swift async await"
    - "Swift Actor"
    - "Swift Task group"
    - "swift testing"
    - "XCTest"
    - "Swift Testing framework"
    - "async test swift"
  category: swift
  pairs_with:
    - test-driven-development
    - code-linting
---

# Swift Skill

Swift concurrency and testing: async/await, Actors, TaskGroups, Sendable, structured concurrency, XCTest, Swift Testing framework, and async test patterns.

## Reference Loading Table

| Signal | Reference | Size |
|--------|-----------|------|
| async/await, Task, Sendable | `references/fundamentals.md` | ~20 lines |
| Actor, @MainActor, nonisolated | `references/actor-isolation.md` | ~20 lines |
| TaskGroup, AsyncSequence, AsyncStream, cancellation | `references/task-patterns.md` | ~20 lines |
| Failure modes, common mistakes | `references/preferred-patterns.md` | ~20 lines |
| concurrency overview, structured concurrency patterns | `references/swift-concurrency.md` | ~30 lines |
| XCTest, Swift Testing, test doubles, async tests, UI tests | `references/swift-testing.md` | ~250 lines |

**Load greedily.** If the user's question touches any signal keyword, load the matching reference before responding. Multiple signals matching = load all matching references.

---

## Core Rules (Always Apply)

### Concurrency

- **Prefer structured concurrency** -- use `TaskGroup` over loose `Task { }` whenever possible; structured tasks propagate cancellation and errors automatically.
- **Mark types Sendable** -- enable strict concurrency checking (`-strict-concurrency=complete`) and resolve all warnings before they become errors in Swift 6.
- **Use actors for shared mutable state** -- avoid manual locks; actors provide compiler-verified safety.
- **Cancel what you create** -- every `Task` stored in a property should have a corresponding cancellation path.
- **Minimize @MainActor surface** -- isolate only the UI layer; keep business logic and networking off the main actor.

### Testing

- **One assertion per concept** -- a single test can have multiple assertions if they verify the same logical behavior, but avoid testing unrelated things together.
- **Arrange-Act-Assert** -- structure every test into setup, execution, and verification phases.
- **Name tests descriptively** -- `testFetchUser_withExpiredToken_throwsAuthError` is better than `testFetch2`.
- **Prefer Swift Testing for new code** -- use `@Test` and `#expect` when targeting Swift 5.9+; fall back to XCTest for older targets or UI tests.
- **Ensure test independence** -- each test must be runnable in isolation; always produce self-contained test state.

---

## Phase 1: ASSESS

Determine what kind of Swift work is needed:

| Request type | Load references | Action |
|-------------|----------------|--------|
| Concurrency patterns | fundamentals, actor-isolation, task-patterns | Pattern guidance |
| Concurrency mistakes | preferred-patterns | Failure mode detection |
| Write tests | swift-testing | Test authoring |
| Async test patterns | swift-testing + fundamentals | Async test guidance |
| Full concurrency review | swift-concurrency + all concurrency refs | Full review pass |

**Gate**: Request classified and relevant references loaded.

---

## Phase 2: EXECUTE

Apply loaded reference knowledge to the user's code or question.

For concurrency work:
1. Verify structured concurrency used where possible
2. Check Sendable conformance
3. Validate actor isolation boundaries
4. Confirm cancellation paths exist

For testing work:
1. Use Swift Testing (`@Test`, `#expect`) for new code on Swift 5.9+
2. Use `@dataProvider`-style parameterized tests with `arguments:`
3. Use protocol-based mock injection
4. Use XCTest for UI tests and older targets

**Gate**: Specific, reference-backed feedback or code provided.

---

## Phase 3: VERIFY

Run the test suite and confirm:

```bash
swift test --enable-code-coverage
swift build
```

**Gate**: All tests pass. Build succeeds with strict concurrency checking.
