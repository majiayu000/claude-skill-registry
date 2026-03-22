---
name: team-planex
description: Unified team skill for plan-and-execute pipeline. Pure router — coordinator always. Beat model is coordinator-only in monitor.md. Triggers on "team planex".
allowed-tools: Agent(*), TaskCreate(*), TaskList(*), TaskGet(*), TaskUpdate(*), TeamCreate(*), TeamDelete(*), SendMessage(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*), mcp__ccw-tools__team_msg(*)
---

# Team PlanEx

Unified team skill: plan-and-execute pipeline for issue-based development. Built on **team-worker agent architecture** — coordinator orchestrates, workers are team-worker agents loading role-specific instructions from `roles/<role>/role.md`.

## Architecture

```
Skill(skill="team-planex", args="task description")
                    |
         SKILL.md (this file) = Router
                    |
     +--------------+--------------+
     |                             |
  no --role flag              --role <name>
     |                             |
  Coordinator                  Worker
  roles/coordinator/role.md    roles/<name>/role.md
     |
     +-- analyze -> dispatch -> spawn workers -> STOP
                                    |
                    +---------------+---------------+
                    v                               v
               [planner]                       [executor]
         (team-worker agent,            (team-worker agent,
          loads roles/planner/role.md)   loads roles/executor/role.md)
```

## Role Registry

| Role | Path | Prefix | Inner Loop |
|------|------|--------|------------|
| coordinator | [roles/coordinator/role.md](roles/coordinator/role.md) | — | — |
| planner | [roles/planner/role.md](roles/planner/role.md) | PLAN-* | true |
| executor | [roles/executor/role.md](roles/executor/role.md) | EXEC-* | true |

## Role Router

Parse `$ARGUMENTS`:
- Has `--role <name>` → Read `roles/<name>/role.md`, execute Phase 2-4
- No `--role` → `@roles/coordinator/role.md`, execute entry router

## Shared Constants

- **Session prefix**: `PEX`
- **Session path**: `.workflow/.team/PEX-<slug>-<date>/`
- **CLI tools**: `ccw cli --mode analysis` (read-only), `ccw cli --mode write` (modifications)
- **Message bus**: `mcp__ccw-tools__team_msg(session_id=<session-id>, ...)`

## Worker Spawn Template

Coordinator spawns workers using this template:

```
Agent({
  subagent_type: "team-worker",
  description: "Spawn <role> worker",
  team_name: "planex",
  name: "<role>",
  run_in_background: true,
  prompt: `## Role Assignment
role: <role>
role_spec: <skill_root>/roles/<role>/role.md
session: <session-folder>
session_id: <session-id>
team_name: planex
requirement: <task-description>
inner_loop: <true|false>
execution_method: <codex|gemini>

Read role_spec file (@<skill_root>/roles/<role>/role.md) to load Phase 2-4 domain instructions.
Execute built-in Phase 1 (task discovery) -> role Phase 2-4 -> built-in Phase 5 (report).`
})
```

## User Commands

| Command | Action |
|---------|--------|
| `check` / `status` | View execution status graph |
| `resume` / `continue` | Advance to next step |
| `add <issue-ids or --text '...' or --plan path>` | Append new tasks to planner queue |

## Session Directory

```
.workflow/.team/PEX-<slug>-<YYYY-MM-DD>/
├── .msg/
│   ├── messages.jsonl          # Message bus log
│   └── meta.json               # Session state
├── task-analysis.json          # Coordinator analyze output
├── artifacts/
│   └── solutions/              # Planner solution output per issue
│       ├── <issueId-1>.json
│       └── <issueId-N>.json
└── wisdom/                     # Cross-task knowledge
    ├── learnings.md
    ├── decisions.md
    ├── conventions.md
    └── issues.md
```

## Specs Reference

- [specs/pipelines.md](specs/pipelines.md) — Pipeline definitions, task metadata registry, execution method selection

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown command | Error with available command list |
| Role not found | Error with role registry |
| Role spec file not found | Error with expected path (roles/<name>/role.md) |
| team-worker agent unavailable | Error: requires .claude/agents/team-worker.md |
| Planner issue planning failure | Retry once, then skip to next issue |
| Executor impl failure | Report to coordinator, continue with next EXEC-* task |
| Pipeline stall | Coordinator monitors, escalate to user |
| Worker no response | Report waiting task, suggest user `resume` |
