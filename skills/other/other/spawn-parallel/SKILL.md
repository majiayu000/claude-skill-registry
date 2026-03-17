---
name: spawn-parallel
description: Pattern for spawning parallel subagents efficiently. Use when you need multiple independent tasks done concurrently.
allowed-tools: Task
---

# Spawn Parallel Skill

Pattern for spawning and coordinating parallel subagents.

## When to Load This Skill

- You have multiple independent tasks
- Tasks don't depend on each other's output
- You want to maximize concurrency

## Spawning Pattern

### 1. Identify Independent Tasks
Tasks are independent if:
- No data dependencies between them
- No file conflicts (different files or read-only)
- Can complete in any order

### 2. Prepare Contexts
Each subagent needs minimal, focused context:
```json
{"task":{"id":"unique_id","description":"specific task"},"context_files":["only relevant files"],"boundaries":{"owns":["files this agent can modify"],"reads":["files for reference"]},"output_path":"memory/tasks/{id}/output.json"}
```

### 3. Spawn All at Once
Use multiple Task calls in single response:
```
Task(subagent_type: "implementer", model: "sonnet", prompt: "Task 1...")
Task(subagent_type: "implementer", model: "sonnet", prompt: "Task 2...")
Task(subagent_type: "implementer", model: "sonnet", prompt: "Task 3...")
```

**Subagent Type Reference (Custom Dotagent Agents):**
| Type | Model | Use For |
|------|-------|---------|
| `explorer` | haiku | Fast codebase scouting |
| `implementer` | sonnet | Focused code writing |
| `verifier` | haiku | Independent verification |
| `tester` | haiku | Test execution |

**Note:** These are custom dotagent agents (lowercase). Built-in Claude Code
agents like `Explore` and `Plan` (capitalized) have different behavior.

### 4. Collect and Validate
After all complete:
- Check each output file exists
- Validate against schema
- Handle failures (retry or escalate)

## Coordination Rules

### Prevent Conflicts
- Define clear file ownership per agent
- Use contracts for shared interfaces
- Read-only access to shared resources

### Handle Failures

Individual failures don't fail the batch. Apply recovery strategies from
@.claude/skills/error-recovery/SKILL.md:

```
FOR each failed task in batch:
  IF output malformed/timeout:
    → Simple Retry (same prompt, up to 3x)
  ELIF agent said "unclear"/"don't understand":
    → Context Enhancement (add files, clarify)
  ELIF partial completion:
    → Scope Reduction (split into subtasks)
  ELIF boundary/contract violation:
    → Escalation (spawn contract-resolver)
  ELIF 3+ attempts failed:
    → Abort, record failure, continue with others
```

**Retry with Context Enhancement Example:**
```
Task(
  subagent_type: "implementer",
  model: "sonnet",
  prompt: |
    ## RETRY - Previous attempt failed
    Error: "Unclear how to connect to database"

    ## Additional Context
    See database config: @src/config/database.ts
    Connection pattern: @src/services/db-connection.ts

    ## Original Task
    {original_task_description}

    Output: memory/tasks/{id}/output.json
)
```

## Example: Parallel Explorers

```
# Spawn 3 custom explorer agents in parallel
Task(
  subagent_type: "explorer",  # Custom dotagent agent
  model: "haiku",
  prompt: "Explore authentication code. Return compact JSON with findings."
)
Task(
  subagent_type: "explorer",
  model: "haiku",
  prompt: "Explore API routes. Return compact JSON with findings."
)
Task(
  subagent_type: "explorer",
  model: "haiku",
  prompt: "Explore database models. Return compact JSON with findings."
)
```

All run concurrently, results collected when all complete.

## Example: Mixed Agent Types

```
# Parallel implementation with different boundaries
Task(
  subagent_type: "implementer",
  model: "sonnet",
  prompt: |
    Task: Add user validation
    Boundaries: owns=[src/validators/user.ts], reads=[src/types/]
    Output: memory/tasks/task-001/output.json
)
Task(
  subagent_type: "implementer",
  model: "sonnet",
  prompt: |
    Task: Add email service
    Boundaries: owns=[src/services/email.ts], reads=[src/config/]
    Output: memory/tasks/task-002/output.json
)
```
