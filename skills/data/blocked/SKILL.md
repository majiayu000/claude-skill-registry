---
name: blocked
description: Mark expedition as blocked with reason and optional unblock agent
disable-model-invocation: true
allowed-tools: Bash(yurtle-kanban *), Bash(git *), Read, Edit
argument-hint: "<EXP-XXX> <reason> [--unblock-by agent-X]"
---

# Mark as Blocked

Mark an expedition as blocked with a clear reason so other agents know why and who can help.

## Required Arguments

- `EXP-XXX` - The expedition ID to block
- `reason` - Why it's blocked (quote if multiple words)

## Optional Arguments

- `--unblock-by agent-X` - Which agent can unblock this

## Steps

### 1. Move to Blocked Status

```bash
yurtle-kanban move EXP-XXX blocked
```

### 2. Update Expedition File

Add a blocked section to the expedition file:

Find the expedition file and add after the frontmatter:

```markdown
> **BLOCKED**: [reason]
> **Since:** YYYY-MM-DD
> **Can unblock:** [agent-X or "anyone"]
```

Also add a Ship's Log entry:

```markdown
### YYYY-MM-DD: BLOCKED

**Reason:** [reason]
**Can unblock:** [who]
**Context:** [any additional context]
```

### 3. Commit and Push

```bash
git add kanban-work/expeditions/EXP-XXX*.md
git commit -m "blocked(exp-XXX): [short reason]

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

### 4. Confirm Block

Show:
- Current blocked items count
- Who can unblock
- Suggest notifying the unblocking agent

## Common Block Reasons

| Reason | Who Can Unblock |
|--------|-----------------|
| "Waiting for GPU training to complete" | agent-a, agent-c |
| "Needs architecture decision" | agent-b, agent-d, captain |
| "Waiting for PR review" | any agent |
| "Blocked by EXP-XXX" | whoever finishes that expedition |
| "Needs Captain input" | captain |
| "External dependency" | depends |

## Unblocking

When you unblock an item:

1. Remove the `> **BLOCKED**` section from the file
2. Add Ship's Log entry: "Unblocked: [what changed]"
3. Move status: `yurtle-kanban move EXP-XXX in_progress`
