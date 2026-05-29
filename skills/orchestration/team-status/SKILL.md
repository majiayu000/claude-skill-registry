---
description: Show status of parallel development agents launched by team-lead. Activates for: team status, agent status, parallel status, check agents.
---

# Team Status

**Show progress of parallel development agents.**

## Usage

```bash
/sw:team-status
/sw:team-status --watch          # Auto-refresh every 2s
/sw:team-status --json           # Machine-readable output
```

## What This Skill Does

Reads the native Agent Teams session state and each agent's increment to produce a status table.

## Implementation Steps

1. List active teammates in the current team
2. For each teammate, check their assigned increment's `tasks.md`
3. Query teammate status (idle, working, completed)
4. Display terminal pane info (tmux pane index or in-process index)

### Display Summary

5. **Display summary table**

## Output Format

```
Team Status: session-uuid (started 2h ago)
Mode: Native Agent Teams

| Agent    | Domain   | Increment               | Tasks  | Progress | Status  |
|----------|----------|-------------------------|--------|----------|---------|
| Agent 1  | frontend | 0193-checkout-frontend  | 5/8    | 62%      | running |
| Agent 2  | backend  | 0194-checkout-backend   | 3/6    | 50%      | running |
| Agent 3  | shared   | 0195-checkout-shared    | 4/4    | 100%     | done    |

Overall: 12/18 tasks (67%)
Active Skills: sw-frontend:frontend-architect, sw:architect, sw:architect
```

## Agent State Icons

| Icon | Status |
|------|--------|
| `⏳` | pending — agent not yet spawned |
| `🔄` | running — agent actively working |
| `✅` | done — all tasks completed, quality gate passed |
| `❌` | failed — agent encountered unrecoverable error |
| `🚫` | cancelled — agent was stopped by user |

## Error Handling

- If no active agent team found, report "No active agent team — try /sw:team-lead first"
- If an agent's increment is missing, report "increment not found"
- If a task file can't be parsed, show "?" for progress

## Options

| Option | Description |
|--------|-------------|
| `--watch` | Auto-refresh every 2 seconds |
| `--json` | Output as JSON for programmatic use |
| `--verbose` | Show per-task detail for each agent |
