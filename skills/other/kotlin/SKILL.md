---
name: kotlin
description: "Kotlin development: coroutines, Flow, Channels, testing with JUnit 5 and Kotest."
user-invocable: false
context: fork
agent: kotlin-general-engineer
routing:
  triggers:
    - "kotlin coroutines"
    - "kotlin structured concurrency"
    - "kotlin Flow"
    - "kotlin Channel"
    - "suspend function"
    - "structured concurrency kotlin"
    - "kotlin testing"
    - "junit kotlin"
    - "kotest"
    - "junit 5 kotlin"
    - "kotlin test dispatcher"
  category: kotlin
  pairs_with:
    - test-driven-development
---

# Kotlin Skill

Kotlin coroutine patterns and testing: structured concurrency, Flow, StateFlow/SharedFlow, Channels, dispatchers, JUnit 5, Kotest, MockK, and coroutine test dispatchers.

## Reference Loading Table

| Signal | Reference | Size |
|--------|-----------|------|
| concurrency, scopes, cancellation, dispatchers, exception handling | `references/concurrency-patterns.md` | ~130 lines |
| Flow, StateFlow, SharedFlow, operators, flow builders | `references/flow-patterns.md` | ~120 lines |
| Channels, producer-consumer, fan-in, fan-out | `references/channel-patterns.md` | ~100 lines |
| GlobalScope, unstructured launch, CancellationException, failure modes | `references/preferred-patterns.md` | ~80 lines |
| coroutine skill overview, structured concurrency principles | `references/kotlin-coroutines.md` | ~55 lines |
| JUnit 5, Kotest, MockK, runTest, parameterized tests, assertions | `references/kotlin-testing.md` | ~290 lines |

**Load greedily.** If the user's question touches any signal keyword, load the matching reference before responding. Multiple signals matching = load all matching references.
