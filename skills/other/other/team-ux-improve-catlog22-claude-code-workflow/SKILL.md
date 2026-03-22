---
name: team-ux-improve
description: Unified team skill for UX improvement. Systematically discovers and fixes UI/UX interaction issues including unresponsive buttons, missing feedback, and state refresh problems. Uses team-worker agent architecture with roles/ for domain logic. Coordinator orchestrates pipeline, workers are team-worker agents. Triggers on "team ux improve".
allowed-tools: Agent, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, TaskList, TaskGet, TaskUpdate, TaskCreate, TeamCreate, TeamDelete, SendMessage, mcp__ace-tool__search_context, mcp__ccw-tools__read_file, mcp__ccw-tools__write_file, mcp__ccw-tools__edit_file, mcp__ccw-tools__team_msg
---

# Team UX Improve

Systematic UX improvement pipeline: scan -> diagnose -> design -> implement -> test. Built on **team-worker agent architecture** — all worker roles share a single agent definition with role-specific Phase 2-4 loaded from `roles/<role>/role.md`.

## Architecture

```
Skill(skill="team-ux-improve", args="<project-path> [--framework react|vue]")
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
     +-- analyze → dispatch → spawn workers → STOP
                                    |
                    +-------+-------+-------+-------+
                    v       v       v       v       v
           [team-worker agents, each loads roles/<role>/role.md]
          scanner  diagnoser  designer  implementer  tester
```

## Role Registry

| Role | Path | Prefix | Inner Loop |
|------|------|--------|------------|
| coordinator | [roles/coordinator/role.md](roles/coordinator/role.md) | — | — |
| scanner | [roles/scanner/role.md](roles/scanner/role.md) | SCAN-* | false |
| diagnoser | [roles/diagnoser/role.md](roles/diagnoser/role.md) | DIAG-* | false |
| designer | [roles/designer/role.md](roles/designer/role.md) | DESIGN-* | false |
| implementer | [roles/implementer/role.md](roles/implementer/role.md) | IMPL-* | true |
| tester | [roles/tester/role.md](roles/tester/role.md) | TEST-* | false |

## Utility Member Registry

**Coordinator-only**: Utility members can only be spawned by Coordinator. Workers CANNOT call Agent() to spawn utility members.

| Utility Member | Path | Callable By | Purpose |
|----------------|------|-------------|---------|
| explorer | [roles/explorer/role.md](roles/explorer/role.md) | Coordinator only | Explore codebase for UI component patterns and framework-specific patterns |

## Role Router

Parse `$ARGUMENTS`:
- Has `--role <name>` → Read `roles/<name>/role.md`, execute Phase 2-4
- No `--role` → `@roles/coordinator/role.md`, execute entry router

## Shared Constants

- **Session prefix**: `ux-improve`
- **Session path**: `.workflow/.team/ux-improve-<timestamp>/`
- **CLI tools**: `ccw cli --mode analysis` (read-only), `ccw cli --mode write` (modifications)
- **Message bus**: `mcp__ccw-tools__team_msg(session_id=<session-id>, ...)`
- **Max test iterations**: 5

## Worker Spawn Template

Coordinator spawns workers using this template:

```
Agent({
  subagent_type: "team-worker",
  description: "Spawn <role> worker for <task-id>",
  team_name: "ux-improve",
  name: "<role>",
  run_in_background: true,
  prompt: `## Role Assignment
role: <role>
role_spec: <skill_root>/roles/<role>/role.md
session: <session-folder>
session_id: <session-id>
team_name: ux-improve
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

## Specs Reference

- [specs/pipelines.md](specs/pipelines.md) — Pipeline definitions and task registry

## Session Directory

```
.workflow/.team/ux-improve-<timestamp>/
├── .msg/
│   ├── messages.jsonl      # Team message bus
│   └── meta.json           # Pipeline config + role state snapshot
├── artifacts/              # Role deliverables
│   ├── scan-report.md      # Scanner output
│   ├── diagnosis.md        # Diagnoser output
│   ├── design-guide.md     # Designer output
│   ├── fixes/              # Implementer output
│   └── test-report.md      # Tester output
├── explorations/           # Explorer cache
│   └── cache-index.json
└── wisdom/                 # Session knowledge base
    ├── contributions/      # Worker contributions (write-only for workers)
    ├── principles/
    ├── patterns/
    └── anti-patterns/
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown command | Error with available command list |
| Role not found | Error with role registry |
| Project path invalid | Re-prompt user for valid path |
| Framework detection fails | AskUserQuestion for framework selection |
| Session corruption | Attempt recovery, fallback to manual |
| Fast-advance conflict | Coordinator reconciles on next callback |
| No UI issues found | Complete with empty fix list, generate clean bill report |
| Test iterations exceeded | Accept current state, continue to completion |
