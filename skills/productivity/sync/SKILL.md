---
name: sync
description: Start-of-session sync - pull latest, check handoffs, reviews, and blocked items
disable-model-invocation: true
allowed-tools: Bash(yurtle-kanban *), Bash(git *), Read, Glob
---

# Agent Sync

Run at the start of each session to sync with other agents and see what needs attention.

## Steps

### 1. Pull Latest

```bash
git fetch origin main
git checkout main
git pull origin main
```

### 2. Check for Handoffs

Look for handoff notes addressed to this agent:

```bash
# List recent handoffs
ls -la kanban-work/handoffs/ 2>/dev/null | tail -10

# Check for unread handoffs (files modified in last 24h)
find kanban-work/handoffs/ -name "*.md" -mtime -1 2>/dev/null
```

If handoffs exist, read them and summarize what needs attention.

### 3. Check Items in Review

```bash
yurtle-kanban list --status review
```

Can this agent help review any of these? Show the list and offer to run `/review EXP-XXX`.

### 4. Check Blocked Items

```bash
yurtle-kanban list --status blocked
```

Can this agent unblock any of these? Show blockers and reasons.

### 5. Check My In-Progress Items

```bash
yurtle-kanban list --status in_progress
```

Are any of these assigned to this agent or stale? Recommend:
- Resume work on existing item, OR
- Pick up new work if nothing in progress

### 6. Show Ready Work

```bash
# Show ready items filtered by agent capability if tags exist
yurtle-kanban list --status ready --limit 5
```

### 7. Generate Sync Summary

Output a summary like:

```
## Agent Sync Complete

**Handoffs:** X pending (read them with `cat kanban-work/handoffs/...`)
**Reviews:** X items need review
**Blocked:** X items blocked
**In Progress:** X items (Y assigned to me)
**Ready:** X items available

### Recommended Next Action
[Pick the most important thing to do]
```

## Tips

- Run `/sync` at the start of every session
- If there are handoffs, read them first
- If there are reviews from other agents, consider helping
- Check blocked items - you might be able to unblock someone
