---
name: team-iterdev
description: Unified team skill for iterative development team. Pure router — all roles read this file. Beat model is coordinator-only in monitor.md. Generator-Critic loops (developer<->reviewer, max 3 rounds). Triggers on "team iterdev".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Agent(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team IterDev

Iterative development team skill. Generator-Critic loops (developer<->reviewer, max 3 rounds), task ledger (task-ledger.json) for real-time progress, shared memory (cross-sprint learning), and dynamic pipeline selection for incremental delivery.

## Architecture

```
Skill(skill="team-iterdev", args="task description")
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
                    +-------+-------+-------+
                    v       v       v       v
               [architect] [developer] [tester] [reviewer]
              (team-worker agents, each loads roles/<role>/role.md)
```

## Role Registry

| Role | Path | Prefix | Inner Loop |
|------|------|--------|------------|
| coordinator | [roles/coordinator/role.md](roles/coordinator/role.md) | — | — |
| architect | [roles/architect/role.md](roles/architect/role.md) | DESIGN-* | false |
| developer | [roles/developer/role.md](roles/developer/role.md) | DEV-* | true |
| tester | [roles/tester/role.md](roles/tester/role.md) | VERIFY-* | false |
| reviewer | [roles/reviewer/role.md](roles/reviewer/role.md) | REVIEW-* | false |

## Role Router

Parse `$ARGUMENTS`:
- Has `--role <name>` → Read `roles/<name>/role.md`, execute Phase 2-4
- No `--role` → `@roles/coordinator/role.md`, execute entry router

## Shared Constants

- **Session prefix**: `IDS`
- **Session path**: `.workflow/.team/IDS-<slug>-<date>/`
- **CLI tools**: `ccw cli --mode analysis` (read-only), `ccw cli --mode write` (modifications)
- **Message bus**: `mcp__ccw-tools__team_msg(session_id=<session-id>, ...)`

## Worker Spawn Template

Coordinator spawns workers using this template:

```
Agent({
  subagent_type: "team-worker",
  description: "Spawn <role> worker",
  team_name: "iterdev",
  name: "<role>",
  run_in_background: true,
  prompt: `## Role Assignment
role: <role>
role_spec: <skill_root>/roles/<role>/role.md
session: <session-folder>
session_id: <session-id>
team_name: iterdev
requirement: <task-description>
inner_loop: <true|false>

Read role_spec file (@<skill_root>/roles/<role>/role.md) to load Phase 2-4 domain instructions.
Execute built-in Phase 1 (task discovery) -> role Phase 2-4 -> built-in Phase 5 (report).`
})
```

## User Commands

| Command | Action |
|---------|--------|
| `check` / `status` | View execution status graph |
| `resume` / `continue` | Advance to next step |

## Session Directory

```
.workflow/.team/IDS-<slug>-<YYYY-MM-DD>/
├── .msg/
│   ├── messages.jsonl          # Team message bus
│   └── meta.json               # Session state
├── task-analysis.json          # Coordinator analyze output
├── task-ledger.json            # Real-time task progress ledger
├── wisdom/                     # Cross-task knowledge accumulation
│   ├── learnings.md
│   ├── decisions.md
│   ├── conventions.md
│   └── issues.md
├── design/                     # Architect output
│   ├── design-001.md
│   └── task-breakdown.json
├── code/                       # Developer tracking
│   └── dev-log.md
├── verify/                     # Tester output
│   └── verify-001.json
└── review/                     # Reviewer output
    └── review-001.md
```

## Specs Reference

- [specs/pipelines.md](specs/pipelines.md) — Pipeline definitions and task registry

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown command | Error with available command list |
| Role not found | Error with role registry |
| GC loop exceeds 3 rounds | Accept with warning, record in shared memory |
| Sprint velocity drops below 50% | Coordinator alerts user, suggests scope reduction |
| Task ledger corrupted | Rebuild from TaskList state |
| Conflict detected | Update conflict_info, notify coordinator, create DEV-fix task |
| Pipeline deadlock | Check blockedBy chain, report blocking point |
