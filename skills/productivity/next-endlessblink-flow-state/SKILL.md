---
name: next
description: Analyze and pick the next task to work on. Shows scored recommendations from MASTER_PLAN.md with interactive selection. Use when starting a session or deciding what to tackle.
---

# What's Next?

Analyze MASTER_PLAN.md tasks, score by priority, and let user pick interactively.

## Triggers
- `/next` - Main command
- `/pick` - Alias for task picking
- "what should I work on", "pick a task", "next task"

## Workflow

### Step 1: Get Scored Tasks

Run the task picker to get prioritized tasks:

```bash
cd tools/task-picker-v2 && npx tsx src/get-tasks.ts --limit=8
```

This outputs tasks sorted by:
1. Status (PLANNED first, then REVIEW, IN_PROGRESS, PAUSED)
2. Priority within status (P0 → P3)

**Rationale:** "What's next" means what to START, not what you're already doing.

### Step 2: Check for Active Work

Look for IN PROGRESS tasks first - these should be finished before starting new work.

```bash
cd tools/task-picker-v2 && npx tsx src/get-tasks.ts --progress --limit=5
```

Also check git status:
```bash
git status --short
```

If uncommitted changes exist, mention: "You have uncommitted changes - consider committing first."

### Step 3: Present Interactive Selection

Use `AskUserQuestion` to let user pick:

```typescript
AskUserQuestion({
  questions: [{
    question: "Which task would you like to work on?",
    header: "Task",
    multiSelect: false,
    options: [
      // Top 4 tasks from get-tasks.ts, formatted as:
      { label: "TASK-XXX: Title here", description: "P0 - IN PROGRESS" },
      { label: "BUG-YYY: Another task", description: "P1 - PLANNED" },
      // ...
      { label: "Show more tasks...", description: "See full list" }
    ]
  }]
})
```

**Option formatting:**
- Label: `{ID}: {title (max 40 chars)}`
- Description: `{priority} - {status}`

### Step 4: Show Task Details

When user selects a task:

```bash
cd tools/task-picker-v2 && npx tsx src/show-task.ts TASK-XXX
```

Output the full task context including description.

### Step 5: Offer Actions

After showing task, ask:
- "Start working on this task" → invoke `/start-dev TASK-XXX`
- "Pick a different task" → repeat from Step 3
- "Just show me the context" → done

## Priority Scoring (Reference)

Tasks are pre-sorted, but here's the logic:

| Factor | Points |
|--------|--------|
| P0 (Critical) | +100 |
| P1 (High) | +50 |
| P2 (Medium) | +20 |
| P3 (Low) | +5 |
| IN PROGRESS | +30 (finish first) |
| REVIEW | +25 |
| PLANNED | +10 |

## Filter Arguments

When user says `/next bugs` or `/next planned`:

| Argument | Filter | get-tasks.ts flag |
|----------|--------|-------------------|
| `bugs` | Only BUG-XXX tasks | `--bugs` |
| `progress` | Only IN_PROGRESS | `--progress` |
| `planned` | Only PLANNED (backlog) | `--planned` |
| `review` | Only REVIEW (needs verification) | `--review` |
| `active` | IN_PROGRESS + REVIEW | `--active` |
| `all` | Include DONE tasks | `--all` |

**Note:** Default limit is 15 tasks. Use `--limit=N` to show more/less.

## Output Format

Default shows PLANNED tasks first (what to start next):

```
## What's Next?

Top tasks ready to start:

[Shows AskUserQuestion with top PLANNED tasks by priority]
- BUG-352: Mobile PWA "Failed to Fetch" (P0 - PLANNED)
- BUG-1122: KDE Widget Lost Timer Sync (P1 - PLANNED)
- BUG-1125: Canvas Edge Connections Broken (P1 - PLANNED)
- Show active work... (IN PROGRESS/REVIEW tasks)
```

Use `/next progress` or `/next active` to see tasks you're already working on.

## Rules

1. **Finish before starting** - Always show IN PROGRESS tasks first
2. **P0 trumps all** - Critical issues come first regardless of status
3. **Interactive selection** - Always use AskUserQuestion, never just print a list
4. **Context on selection** - Always show full task details when picked
5. **Action oriented** - Offer to start work with /start-dev

## Example Session

```
User: /next

Claude: [Runs get-tasks.ts]

## Active Work

You have 1 task in progress:

Claude: [Shows AskUserQuestion]
- TASK-1060: Infrastructure & E2E Sync (P0 - IN PROGRESS)
- BUG-1099: VPS Done Tasks Not Filtered (P1 - IN PROGRESS)
- BUG-1086: VPS/PWA Auth Not Persisting (P0 - REVIEW)
- Show more tasks...

User: [Clicks TASK-1060]

Claude: [Runs show-task.ts TASK-1060]

## Selected Task: TASK-1060
**Title:** Infrastructure & E2E Sync Stability
**Priority:** P0
**Status:** IN PROGRESS
...

Claude: Would you like me to continue working on this task?
```

## NPM Scripts

| Script | Description |
|--------|-------------|
| `npm run pick:list` | List all tasks (default 15) |
| `npm run pick:progress` | IN PROGRESS only |
| `npm run pick:planned` | PLANNED only (backlog) |
| `npm run pick:review` | REVIEW only |
| `npm run pick:bugs` | Bugs only |
| `npm run pick:all` | Include DONE tasks |
| `npm run pick:json` | Get tasks as JSON |
| `npm run pick:show TASK-XXX` | Show task details |
