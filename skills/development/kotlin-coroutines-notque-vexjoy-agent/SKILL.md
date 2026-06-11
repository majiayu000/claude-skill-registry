---
name: kotlin-coroutines
description: "Kotlin structured concurrency, Flow, and Channel patterns."
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
  category: kotlin
  pairs_with:
    - kotlin-testing
---

# Kotlin Coroutines Patterns

Umbrella skill for Kotlin coroutine development: structured concurrency, cancellation,
Flow, StateFlow/SharedFlow, Channels, exception handling, and dispatchers. Routes to
the correct reference based on the task at hand.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Concurrency | `concurrency-patterns.md` | Scopes, cancellation, dispatchers, exception handling |
| Flow | `flow-patterns.md` | Flow builders, StateFlow, SharedFlow, operators |
| Channels | `channel-patterns.md` | Producer-consumer, fan-in/fan-out patterns |
| Failure modes | `preferred-patterns.md` | GlobalScope, unstructured launch, CancellationException |

## Instructions

### Step 1: Identify the Domain

Classify the task into one or more domains, then load the corresponding reference files.
Only load what is needed -- do not load all references for every task.

| Domain | Load Reference | When |
|--------|---------------|------|
| Concurrency | `references/concurrency-patterns.md` | Scopes, cancellation, dispatchers, exception handling |
| Flow | `references/flow-patterns.md` | Flow builders, StateFlow, SharedFlow, operators |
| Channels | `references/channel-patterns.md` | Producer-consumer, fan-in/fan-out patterns |
| Failure modes | `references/preferred-patterns.md` | GlobalScope, unstructured launch, CancellationException |

Multiple domains may apply. For example, reviewing code that uses both Flow and Channels
should load both `flow-patterns.md` and `channel-patterns.md`.

### Step 2: Load and Follow the Reference

Read the selected reference file(s) using `${CLAUDE_SKILL_DIR}/references/<name>.md`.
Each reference contains the full patterns, code examples, and decision matrices for that
domain. Follow the instructions in the reference as if they were this skill's instructions.

### Step 3: Execute

Apply the loaded reference patterns to the task. Use the code examples as templates
for implementation guidance.

## Key Principles

1. **Structured concurrency is non-negotiable** -- every coroutine must have a parent scope that defines its lifetime.
2. **Inject dispatchers** -- accept `CoroutineDispatcher` as a parameter so callers (and tests) can control threading.
3. **Always rethrow CancellationException** -- rethrow it immediately or use specific exception types instead of catching `Exception`.
4. **Prefer Flow over Channel** -- Flow is cold, composable, and handles backpressure. Channels are lower-level; reach for them only when Flow cannot express the pattern.
5. **Use supervisorScope for partial failure tolerance** -- when independent tasks should not cancel each other, wrap them in supervisorScope.
6. **Use scoped coroutines instead of GlobalScope** -- it has no lifecycle, no cancellation, and no structured concurrency. Pass a scope from your application framework instead.
