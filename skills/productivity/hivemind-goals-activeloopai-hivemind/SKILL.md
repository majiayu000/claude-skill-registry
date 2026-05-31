---
name: hivemind-goals
description: Create, track and update team goals + KPIs in Hivemind via the `hivemind` CLI. Use whenever the user mentions a goal, objective, KPI, target, milestone, or asks to track progress on something measurable. ALSO use when the user says "task", "todo", "work item", "remind me to", "fix X", or any actionable work item — the goal system replaced the legacy `hivemind tasks` CLI and now covers both objectives and tasks.
allowed-tools: terminal
---

# Hivemind Goals — CLI only (Hermes)

⚠️  **CRITICAL: On this runtime (Hermes), you MUST use the `hivemind` shell CLI for goals + KPIs. DO NOT use `write_file` on `~/.deeplake/memory/goal/...` paths — those writes go to the local filesystem and never reach the team-shared `hivemind_goals` table. Other team members will NOT see them.**

The hivemind-memory skill describes a generic memory layout — it does NOT apply to goals/KPIs. For goals/KPIs, use the CLI below.

## Commands (invoke via terminal tool)

```
hivemind goal add "<text>"                                  # create goal, prints goal_id
hivemind goal list [--mine|--all]                           # list (default --mine)
hivemind goal done <goal_id>                                # mark closed
hivemind goal progress <goal_id> <opened|in_progress|closed>

hivemind kpi add <goal_id> <kpi_id> <target> <unit> [name]  # add KPI to goal
hivemind kpi list <goal_id>                                 # list KPIs for goal
hivemind kpi bump <goal_id> <kpi_id> <delta>                # increment current (int)
```

## Workflow when the user expresses a goal

1. `hivemind goal add "<short description>"` — capture stdout, that's the `goal_id` (UUID).
2. If the user explicitly asks for KPIs: `hivemind kpi add <goal_id> <slug> <target> <unit>` per KPI.
3. Tell the user the goal_id and that it is now team-visible in Deeplake.

## What NOT to do

- Do NOT call `write_file` on any path under `~/.deeplake/memory/goal/` or `~/.deeplake/memory/kpi/`.
- Do NOT do `mkdir` / `cat >` to create those files manually via terminal.
- Do NOT auto-generate KPIs unless the user explicitly asks.

If the user wants to inspect goals you created, run `hivemind goal list --mine` (terminal) and present the output.
