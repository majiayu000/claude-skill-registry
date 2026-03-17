---
name: implement
description: Use when the user has a clear, small task ready for direct implementation from conversation context without needing a plan or Arc pipeline. Arc's Simple tier executor.
invocation: agent
---

# Implement

Execute implementation directly from conversation context and task description. This is Arc's true Simple tier executor — no plan, spec, or `/arc-start` state required.

**Key difference from `/arc:core:execute`**: This skill is standalone. It does not require `.arc/` state, plans, or beads. It works from conversation context alone.

**Source**: Conversation context + input + mentioned files.

## Instructions

### Step 1: Create Task Graph Immediately

**ONLY use what's already available:**
- The user's input
- Conversation history (already in context)

**DO NOT:**
- Read files unless the user explicitly asks you to
- Grep or explore the codebase
- Spawn sub-agents or delegate work — do ALL implementation directly yourself

Create tasks immediately from context. Include file paths in task descriptions so they can be read during execution.

For each work item, create a task:

```
TaskCreate({
  "subject": "Fix auth token validation",
  "description": "Full implementation details from context",
  "activeForm": "Fixing auth token validation"
})
```

**Set dependencies with `addBlockedBy`** to identify which tasks depend on others.

### Step 2: Execute Tasks Sequentially

For each task (in dependency order):

1. **Claim**: `TaskUpdate({ taskId: "N", status: "in_progress" })`
2. **Read files as needed**: Use Read tool on file paths from task description
3. **Implement**: Make changes based on context
4. **Verify**: Run any task-specific verification
5. **Complete**: `TaskUpdate({ taskId: "N", status: "completed" })`
6. **Next**: Find next unblocked task via TaskList

### Step 3: Run Exit Criteria

Before declaring completion:
1. Run the verification (tests, commands, etc.)
2. If pass → "Exit criteria passed"
3. If fail → fix issues and retry

### Step 4: Loop Until Done

Continue until:
- All tasks completed AND
- Exit criteria pass

Say **"Exit criteria passed"** when complete.

## Error Handling

| Scenario | Action |
|----------|--------|
| Context unclear | Ask for clarification |
| Exit criteria fail | Fix issues and retry |
| Context compacted | TaskList → continue |
