---
name: subagent-batching
description: Patterns for launching and managing parallel subagents efficiently.
version: "2.0.0"
author: "JacobPEvans"
---

# Subagent Batching

Patterns for parallel subagent execution. Use your judgment on batch sizes based on task complexity.

## When to Parallelize

**Parallelize when**:

- Processing multiple independent items (PRs, issues, files)
- Tasks have no dependencies between items
- Each item can succeed or fail independently

**Don't parallelize when**:

- Later items depend on earlier results
- Shared resources could cause conflicts
- You need to aggregate results before proceeding

## Launch Pattern

Launch subagents in a **single message** with multiple Task tool calls. Don't launch sequentially.

```text
# Correct: ONE message with multiple Task calls
Task 1: Process item A
Task 2: Process item B
Task 3: Process item C
# All launch simultaneously
```

## Batching for Large Sets

For many items, batch them and validate between batches:

1. Launch a batch of subagents in parallel (single message)
2. Wait for all to complete using `TaskOutput` with `block=true`
3. Validate results before proceeding
4. Start next batch after validation

## Subagent Prompts

Give each subagent focused context:

- Clear task description
- Relevant identifiers and locations
- Expected output format
- Success criteria

## Error Handling

- One failure shouldn't block the rest
- Mark failed items for human review
- Continue processing remaining items
- Provide summary of successes and failures

## Reporting

After completion, summarize:

- Total items processed
- Successes with brief descriptions
- Failures with reasons
- Any required follow-up actions
