---
name: core-dev
description: Development guide for the lemline-core module. Use when working with
  workflow execution (orchestrators,
---

---
name: core-dev
description: Development guide for the lemline-core module. Use when working with workflow execution (orchestrators,
processors), node tree navigation (Node, NodePosition), task states (TaskState, WorkflowCommand, WorkflowEvent),
expression evaluation (JQ, scope), error handling (TryTask, retry, catch), parallel execution (Fork), or DSL parsing.
Covers the step-by-step execution model, exception-driven control flow, and stateless architecture.
---

# Lemline Core Development Guide

## Purpose

Guide development of the lemline-core module - the pure, stateless workflow execution engine implementing the Serverless
Workflow DSL v1.0 specification.

**Documentation:**

- [Overview](lemline-core/docs/core-overview.md) - Module structure, DSL parsing, adding tasks
- [Nodes](lemline-core/docs/core-nodes.md) - Node tree, NodePosition, navigation
- [Orchestrators](lemline-core/docs/core-orchestrators.md) - StepByStep vs Full execution
- [Processors](lemline-core/docs/core-processors.md) - NodeProcessor, control flows, activities
- [Fork](lemline-core/docs/core-fork.md) - Parallel branches, error boundaries
- [Errors](lemline-core/docs/core-errors.md) - Exceptions, retry, error handling
- [States](lemline-core/docs/core-states.md) - TaskState, WorkflowCommand, WorkflowEvent
- [Expressions](lemline-core/docs/core-expressions.md) - JQ evaluation, scope variables

---

## Quick Reference

### If you need to change something in...

**Orchestration:**

First, read [core-orchestrators.md](lemline-core/docs/core-orchestrators.md)

- **Change step execution flow** →
  Modify [StepByStepOrchestrator.kt](lemline-core/src/main/kotlin/com/lemline/core/orchestrator/StepByStepOrchestrator.kt)
- **Change synchronous test execution** →
  Modify [FullOrchestrator.kt](lemline-core/src/main/kotlin/com/lemline/core/orchestrator/FullOrchestrator.kt)
- **Add a new WorkflowCommand/Event** →
  Modify [WorkflowState.kt](lemline-core/src/main/kotlin/com/lemline/core/orchestrator/WorkflowState.kt)

**Nodes:**

First, read [core-nodes.md](lemline-core/docs/core-nodes.md)

- **Change node tree structure** →
  Modify [Node.kt](lemline-core/src/main/kotlin/com/lemline/core/nodes/Node.kt)
- **Add a new Token type** →
  Modify [Token.kt](lemline-core/src/main/kotlin/com/lemline/core/nodes/Token.kt)
- **Change position addressing** →
  Modify [NodePosition.kt](lemline-core/src/main/kotlin/com/lemline/core/nodes/NodePosition.kt)

**Processors:**

First, read [core-processors.md](lemline-core/docs/core-processors.md)

- **Add a new task type** → Read [core-overview.md](lemline-core/docs/core-overview.md#adding-a-new-task-type)
- **Change control flow logic (Do, For, Switch)** →
  Modify `processors/DoProcessor.kt`, `ForProcessor.kt`, `SwitchProcessor.kt`
- **Change activity behavior (Wait, Call, Run)** →
  Modify `processors/WaitProcessor.kt`, `CallProcessor.kt`, `RunProcessor.kt`

**States:**

First, read [core-states.md](lemline-core/docs/core-states.md)

- **Add a new TaskState** → Create in `states/` directory, extend `TaskState`
- **Change scope variables** → Modify the `scope` property in the relevant state class
- **Change state serialization** → Modify `TaskStates.kt`

**Error Handling:**

First, read [core-errors.md](lemline-core/docs/core-errors.md)

- **Change retry logic** →
  Modify [TryProcessor.kt](lemline-core/src/main/kotlin/com/lemline/core/processors/TryProcessor.kt)
- **Add a new AsyncTaskException** →
  Modify [AsyncTaskException.kt](lemline-core/src/main/kotlin/com/lemline/core/errors/AsyncTaskException.kt)
- **Change error types** →
  Modify [WorkflowException.kt](lemline-core/src/main/kotlin/com/lemline/core/errors/WorkflowException.kt)

**Expressions:**

First, read [core-expressions.md](lemline-core/docs/core-expressions.md)

- **Change JQ evaluation** →
  Modify [JQExpression.kt](lemline-core/src/main/kotlin/com/lemline/core/expressions/JQExpression.kt)
- **Add scope variables** → Modify the relevant state class's `scope` property
- **Change input/output transformation** → Modify transformation helpers in orchestrator

**Fork/Parallel:**

First, read [core-fork.md](lemline-core/docs/core-fork.md)

- **Change fork execution** →
  Modify [ForkProcessor.kt](lemline-core/src/main/kotlin/com/lemline/core/processors/ForkProcessor.kt)
- **Change branch detection** → Modify `forkBranchCompleted`/`forkBranchFailed` in `StepByStepOrchestrator.kt`

**DSL Parsing:**

First, read [core-overview.md](lemline-core/docs/core-overview.md#dsl-parsing)

- **Change parsing logic** →
  Modify [DefinitionCache.kt](lemline-core/src/main/kotlin/com/lemline/core/definitions/DefinitionCache.kt)

---

## Critical Rules

### ✅ ALWAYS Do This

1. **Keep processors stateless** - receive state, return updated state via `NextStepInfo`
2. **Use exception-driven control flow** - throw `AsyncTaskException` for wait/fork/runWorkflow
3. **Serialize all state** - `TaskState` subclasses must be `@Serializable`
4. **Clean up states** - return `null` in `stateUpdates` when leaving a node
5. **Provide scope variables** - override `scope` property when state provides expression variables
6. **Test with FullOrchestrator** - use for unit testing workflow logic
7. **Build node tree lazily** - use `by lazy` for `children` property
8. **Use `FlowDirective`** - `Continue`, `End`, or `Then(target)` for navigation

### ❌ NEVER Do This

1. **Store mutable state in processors** - processors are stateless
2. **Modify Node objects** - nodes are immutable definitions
3. **Skip state serialization** - breaks stateless worker pattern
4. **Use blocking operations** - all I/O should be in `suspend` functions
5. **Throw regular exceptions for control flow** - use `AsyncTaskException` subtypes
6. **Ignore `Direction` parameter** - behavior differs based on entry direction
7. **Leak state across branches** - clean states when completing fork branches

---

## Architecture Overview

### Step-by-Step Execution Model

```
WorkflowCommand
    │
    ▼
Orchestrator.runByTask()
    │
    ├── Check if condition (skip if false)
    ├── Transform input (inputFrom)
    ├── Get processor for node
    └── Call processor.getNextStepInfo()
            │
            ├── AsyncTaskException ──► WaitStarted/ForkStarted/RunWorkflowStarted
            │
            └── NextStepInfo ──► completeTask()
                                    ├── Transform output (outputAs)
                                    ├── Export to context (exportAs)
                                    └── Navigate to next
                                            │
                                            └── TaskScheduled/WorkflowCompleted/WorkflowFailed
```

### Key Files

| Purpose | File |
|---------|------|
| Step orchestration | `orchestrator/StepByStepOrchestrator.kt` |
| Full execution | `orchestrator/FullOrchestrator.kt` |
| Node structure | `nodes/Node.kt` |
| Position addressing | `nodes/NodePosition.kt` |
| Processor interface | `processors/NodeProcessor.kt` |
| Base state | `states/TaskState.kt` |
| Commands/Events | `orchestrator/WorkflowState.kt` |
| JQ evaluation | `expressions/JQExpression.kt` |
| DSL parsing | `definitions/DefinitionCache.kt` |

---

## Common Patterns

### Creating a New Processor

```kotlin
// 1. State class
@Serializable
data class CustomState(
    override val startedAt: Instant = Clock.System.now(),
    val customField: String = ""
) : TaskState() {
    // Optional: provide scope variables
    override val scope: Scope get() = buildJsonObject {
        put("custom", JsonPrimitive(customField))
    }
}

// 2. Processor
class CustomProcessor(override val node: Node<CustomTask>) : NodeProcessor<CustomTask, CustomState> {
    override fun createInitialState() = CustomState()

    override fun getNextStepInfo(state: CustomState, dataset: JsonElement, scope: Scope, direction: Direction): NextStepInfo<CustomState> {
        return when (direction) {
            FROM_PARENT -> {
                // Process task
                NextStepInfo(
                    state = state,
                    rawOutput = result,
                    stateUpdates = mapOf(node.position to null), // Clean up
                    flowDirective = FlowDirective.Continue
                )
            }
            FROM_CHILD -> { /* Handle child completion */ }
            else -> { /* Handle other directions */ }
        }
    }
}

// 3. Register in factory
fun createProcessor(node: Node<*>) = when (node.task) {
    is CustomTask -> CustomProcessor(node as Node<CustomTask>)
    // ...
}
```

### Throwing AsyncTaskException

```kotlin
// For activities that need orchestrator coordination
override fun getNextStepInfo(...): NextStepInfo<WaitState> {
    throw AsyncTaskException.WaitStartedException(
        state = state,
        transformedInput = dataset,
        config = WaitStartedException.Config(waitUntil = calculateWaitUntil())
    )
}
```

### Handling Navigation

```kotlin
override fun getNextStepInfo(state, dataset, scope, direction) = when (direction) {
    FROM_PARENT -> {
        // First entry - initialize and go to first child
        NextStepInfo(state = initialState, flowDirective = Continue)
    }
    FROM_CHILD -> {
        if (hasMoreChildren) {
            NextStepInfo(state = nextState, flowDirective = Continue)
        } else {
            // Done - clean up state and return to parent
            NextStepInfo(stateUpdates = mapOf(node.position to null), flowDirective = Continue)
        }
    }
}
```

---

## Testing Patterns

### Unit Test with FullOrchestrator

```kotlin
@Test
fun `should execute workflow`() = runTest {
    val yaml = """
        document:
          name: test
          version: "1.0"
        do:
          - myTask:
              set:
                result: "success"
    """.trimIndent()

    val workflow = DefinitionCache.parse(yaml)
    val orchestrator = FullOrchestrator(activityRunner, definitionLoader)

    val result = orchestrator.start(workflow, JsonObject(mapOf()))

    assertEquals("success", result.jsonObject["result"]?.jsonPrimitive?.content)
}
```

### Testing Individual Processors

```kotlin
@Test
fun `DoProcessor should iterate children`() {
    val node = createDoNode(childCount = 3)
    val processor = DoProcessor(node)

    val result = processor.getNextStepInfo(
        state = processor.createInitialState(),
        dataset = JsonObject(mapOf()),
        scope = JsonObject(mapOf()),
        direction = Direction.FROM_PARENT
    )

    assertEquals(0, (result.state as DoState).index)
}
```

---

## Running Tests

```bash
# All tests
./gradlew :lemline-core:test

# Specific test class
./gradlew :lemline-core:test --tests "com.lemline.core.tests.MyTest"

# Specific test method
./gradlew :lemline-core:test --tests "com.lemline.core.tests.MyTest.should do something"
```

---

## Related Documentation

- **CLAUDE.md** - Project-wide guidelines and architecture overview
- **runner-dev skill** - lemline-runner module (messaging, persistence, CLI)
- **Serverless Workflow DSL** - https://serverlessworkflow.io/
