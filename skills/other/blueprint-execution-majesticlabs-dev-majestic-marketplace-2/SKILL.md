---
name: blueprint-execution
description: Execution phase for blueprint workflow - present options and delegate to appropriate commands
---

# Blueprint Execution

Present execution options after plan is written and delegate to appropriate commands.

## Input

```yaml
plan_path: string  # e.g., docs/plans/20260114_auth.md
```

## Workflow

### 1. Present Options

```
AskUserQuestion:
  question: "Blueprint ready. How do you want to proceed?"
  options:
    - "Build as single task" → Step 2
    - "Break into small tasks" → Step 3
    - "Create as single epic" → Step 4
```

### 2. Single Task Flow

Execute entire plan as one task:

```
/majestic:build-task "{plan_path}"
```

**End workflow.**

### 3. Task Breakdown Flow

Decompose into small tasks:

```
Task(majestic-engineer:plan:task-breakdown, prompt="Plan: {plan_path}")
```

Then ask about task creation:

```
AskUserQuestion:
  question: "Tasks added to plan. Create in backlog?"
  options:
    - "Yes, create tasks" → Skill(skill: "backlog-manager") for each task
    - "No, just the plan" → Step 5
```

After tasks created, go to Step 5.

### 4. Epic Flow

Create single backlog item:

```
Skill(skill: "backlog-manager")
```

Update plan with task reference, go to Step 5.

### 5. Build Offering

```
AskUserQuestion:
  question: "Start building?"
  options:
    - "Build all tasks now" → /majestic:run-blueprint "{plan_path}"
    - "Build with ralph" → /majestic-ralph:ralph-loop "/majestic:run-blueprint {plan_path}"
    - "Done for now" → End workflow
```

## Output

```yaml
execution_type: "single_task" | "breakdown" | "epic"
build_started: boolean
```
