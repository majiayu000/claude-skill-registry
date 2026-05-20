---
name: n8n-impl-workflow-design
description: >
  Use when designing complex n8n v1.x workflows with branching, error handling,
  or sub-workflow patterns. Prevents silent failures from missing error workflows
  or incorrect merge node modes. Covers sub-workflow execution (Execute Workflow
  node), Error Trigger node, retry logic, branching (IF/Switch nodes), merge
  patterns (Merge node modes), loop patterns (Loop Over Items), wait/webhook
  resume, scheduling patterns, and Stop And Error node.
  Keywords: n8n, workflow design, error handling, sub-workflow, merge, branching.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n Workflow Design Patterns

## Quick Reference

| Pattern | Primary Node | When to Use |
|---------|-------------|-------------|
| Sub-workflow | Execute Workflow | Reusable logic, separation of concerns, >20 nodes |
| Error handling | Error Trigger + Stop And Error | Centralized failure notification and recovery |
| Branching | IF / Switch | Conditional routing based on data values |
| Merging | Merge | Combining data from parallel branches |
| Looping | Loop Over Items | Batch processing, rate-limited API calls |
| Wait/Resume | Wait | Human approval, external callback, timed delay |
| Scheduling | Schedule Trigger | Recurring automated execution |

## Decision Tree: Which Pattern Do I Need?

```
Need to reuse logic across workflows?
├─ YES → Sub-workflow (Execute Workflow node)
└─ NO
   Need to handle failures gracefully?
   ├─ YES → Is it a single node that might fail?
   │  ├─ YES → continueOnFail + IF node to check $json.error
   │  └─ NO → Error workflow (Error Trigger node)
   └─ NO
      Need to route data conditionally?
      ├─ YES → Two outcomes? → IF node
      │        Multiple outcomes? → Switch node
      └─ NO
         Need to combine data from multiple sources?
         ├─ YES → Merge node (choose mode based on use case)
         └─ NO
            Need to process items in batches?
            ├─ YES → Loop Over Items node
            └─ NO
               Need to pause and wait?
               ├─ YES → Wait node (time, webhook, or form resume)
               └─ NO → Schedule Trigger for recurring execution
```

## 1. Sub-Workflow Patterns

### Execute Workflow Node

ALWAYS use the Execute Workflow node to call another workflow as a sub-workflow. NEVER duplicate logic across workflows.

**Parameter passing:**
- The calling workflow sends input items to the sub-workflow
- The sub-workflow receives items at its trigger node
- The sub-workflow returns its final output back to the caller

**Caller policy** (`callerPolicy` in workflow settings):
- `workflowsFromSameOwner` — Only workflows owned by the same user (DEFAULT)
- `workflowsFromAList` — Only workflow IDs listed in `callerIds`
- `any` — Any workflow can call this sub-workflow
- `none` — NEVER allow this workflow to be called as a sub-workflow

ALWAYS set `callerPolicy` explicitly on sub-workflows in production. NEVER leave it as default when multiple users share the n8n instance.

**When to extract a sub-workflow:**
- Logic is reused by 2+ workflows
- A workflow exceeds 20 nodes
- A distinct responsibility can be isolated (e.g., "send notification", "enrich contact")

See: [references/methods.md](references/methods.md) for Execute Workflow node details.
See: [references/examples.md](references/examples.md) for sub-workflow patterns.

## 2. Error Handling

### Three Layers of Error Protection

**Layer 1 — Node-level: continueOnFail**
- Enable `continueOnFail` on individual nodes that might fail
- Failed items pass through with `$json.error` containing the error message
- ALWAYS follow a continueOnFail node with an IF node to check `$json.error`

**Layer 2 — Node-level: Retry on Fail**
- Enable `retryOnFail` for transient failures (API timeouts, rate limits)
- Configure `maxTries` (default: 3) and `waitBetweenTries` (default: 1000ms)
- ALWAYS use retry for HTTP Request nodes calling external APIs

**Layer 3 — Workflow-level: Error Workflow**
- Create a dedicated error workflow starting with the **Error Trigger** node
- Assign it in the main workflow's Settings > Error Workflow
- One error workflow can serve multiple production workflows
- The Error Trigger receives execution context: workflow name, execution ID, error message

### Stop And Error Node

Use the **Stop And Error** node to deliberately fail a workflow when:
- Data validation fails
- Business rules are violated
- A required external resource is unavailable

This triggers the configured error workflow, enabling centralized error notification.

### Execution Timeout

Set `executionTimeout` in workflow settings to prevent runaway executions. Configure the global default via `EXECUTIONS_TIMEOUT` environment variable (default: disabled). Maximum allowed timeout is controlled by `EXECUTIONS_TIMEOUT_MAX` (default: 3600 seconds).

See: [references/methods.md](references/methods.md) for error handling node details.
See: [references/examples.md](references/examples.md) for error handling patterns.

## 3. Branching Patterns

### IF Node

The IF node evaluates conditions and routes items to one of two outputs:
- **Output 0 (true)**: Items matching the condition
- **Output 1 (false)**: Items NOT matching the condition

ALWAYS use the IF node for binary (true/false) decisions. NEVER use a Switch node with only two routes.

Conditions support:
- String: equals, contains, startsWith, endsWith, regex, isEmpty
- Number: equals, gt, gte, lt, lte, between
- Boolean: equals
- Date/time comparisons
- Combine with `and` / `or` combinators

### Switch Node

The Switch node routes items to multiple outputs based on rules or expression values:
- **Rules mode**: Define conditions per output (like chained IF nodes)
- **Expression mode**: Route based on the value of an expression

ALWAYS use the Switch node when routing to 3+ destinations. NEVER chain multiple IF nodes for multi-way branching.

### OnError Output

Every node supports the `onError` setting:
- `stopWorkflow` — Stop execution (default)
- `continueRegularOutput` — Send error data to the regular output
- `continueErrorOutput` — Send error data to a dedicated error output

See: [references/methods.md](references/methods.md) for IF and Switch node details.

## 4. Merge Patterns

The Merge node combines data from two or more inputs. ALWAYS choose the correct mode:

| Mode | Use Case | Behavior |
|------|----------|----------|
| **Append** | Combine all items from both inputs into one list | Concatenates items |
| **Combine > Merge By Fields** | Join items by matching field values | SQL-style JOIN |
| **Combine > Merge By Position** | Pair items by index position | items[0]+items[0], items[1]+items[1] |
| **Combine > Multiplex** | Create all combinations | Cartesian product |
| **Choose Branch** | Wait for one branch, discard others | First-to-complete wins |
| **SQL Query** | Complex data combination | Write SQL against inputs |

ALWAYS use "Merge By Fields" when combining data from different sources that share a key field. NEVER use "Merge By Position" for data with different item counts.

See: [references/methods.md](references/methods.md) for Merge node modes.

## 5. Loop Patterns

### Loop Over Items Node

The Loop Over Items node (formerly "Split In Batches") processes items in configurable batch sizes:

1. Splits the input items into batches of N
2. Sends each batch through the loop body
3. Collects results after all batches complete

**When to use:**
- API has rate limits (process N items, then pause)
- Memory-intensive operations (process in smaller chunks)
- Need to call an external API per item or per batch

ALWAYS set a reasonable batch size. NEVER process all items at once when calling rate-limited APIs.

**Loop body rules:**
- Connect the "Loop" output back to the first node in your processing chain
- Connect your processing chain's last node back to the Loop Over Items node
- The "Done" output fires after ALL batches complete

See: [references/examples.md](references/examples.md) for loop patterns.

## 6. Wait and Resume Patterns

### Wait Node

The Wait node pauses execution and resumes via:

**Resume on timer:**
- Wait a fixed duration (seconds, minutes, hours, days)
- Wait until a specific date/time

**Resume on webhook:**
- Generates a unique `$execution.resumeUrl`
- Execution pauses until an HTTP request hits that URL
- The incoming request data is available as the Wait node's output

**Resume on form:**
- Generates a form URL via `$execution.resumeFormUrl`
- Displays a form to the user
- Execution resumes when the form is submitted

ALWAYS use Wait node webhook resume for human-in-the-loop approvals. NEVER poll for status changes when a webhook callback is possible.

### Webhook Resume URL

Access the resume URL in expressions:
- `{{ $execution.resumeUrl }}` — Webhook resume URL
- `{{ $execution.resumeFormUrl }}` — Form resume URL

ALWAYS send the resume URL to the external system (e.g., in an approval email) BEFORE the Wait node pauses execution.

## 7. Scheduling Patterns

### Schedule Trigger

The Schedule Trigger node starts workflow execution on a schedule:
- **Interval**: Every N seconds/minutes/hours
- **Cron expression**: Standard cron syntax for complex schedules
- **Specific times**: At fixed times on specific days

ALWAYS set the correct timezone in workflow settings (`settings.timezone`). NEVER rely on the server's default timezone for scheduled workflows.

ALWAYS set `GENERIC_TIMEZONE` environment variable on deployment to ensure consistent schedule behavior.

### Cron Expression Quick Reference

| Expression | Meaning |
|-----------|---------|
| `0 * * * *` | Every hour at minute 0 |
| `0 9 * * 1-5` | Weekdays at 09:00 |
| `*/15 * * * *` | Every 15 minutes |
| `0 0 1 * *` | First day of every month at midnight |
| `0 8,12,17 * * *` | At 08:00, 12:00, and 17:00 daily |

## 8. Workflow Settings Reference

| Setting | Purpose | Default |
|---------|---------|---------|
| `errorWorkflow` | Workflow to execute on failure | None |
| `executionTimeout` | Max execution time (seconds) | Disabled (-1) |
| `callerPolicy` | Who can call this as sub-workflow | `workflowsFromSameOwner` |
| `callerIds` | Allowed caller workflow IDs (when policy = fromAList) | Empty |
| `timezone` | Timezone for schedule nodes | Instance default |
| `saveDataErrorExecution` | Save data on error | `all` |
| `saveDataSuccessExecution` | Save data on success | `all` |
| `executionOrder` | Node execution algorithm | `v1` |

## Design Principles

1. **ALWAYS** name nodes descriptively — "Fetch Customer Orders" not "HTTP Request1"
2. **ALWAYS** add notes to complex logic nodes explaining the business rule
3. **ALWAYS** set an error workflow on every production workflow
4. **ALWAYS** use sub-workflows for reusable logic — NEVER copy-paste nodes
5. **NEVER** build workflows with more than 30 nodes — extract sub-workflows
6. **NEVER** leave retry settings at default for external API calls — configure explicitly
7. **ALWAYS** test with pinned data before activating a workflow
8. **ALWAYS** set execution timeout on long-running workflows

## Reference Files

- [references/methods.md](references/methods.md) — Core workflow nodes: Execute Workflow, Merge, IF, Switch, Loop Over Items, Wait, Error Trigger, Stop And Error
- [references/examples.md](references/examples.md) — Sub-workflow, error handling, branching, loops, scheduling patterns
- [references/anti-patterns.md](references/anti-patterns.md) — Workflow design mistakes and how to avoid them
