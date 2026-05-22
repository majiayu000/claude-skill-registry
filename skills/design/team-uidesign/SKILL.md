---
name: team-uidesign
description: Unified team skill for UI design team. Research -> design tokens -> audit -> implementation. Uses team-worker agent architecture with roles/ for domain logic. Coordinator orchestrates dual-track pipeline with GC loops and sync points. Triggers on "team ui design", "ui design team".
allowed-tools: Agent, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, TaskList, TaskGet, TaskUpdate, TaskCreate, TeamCreate, TeamDelete, SendMessage, mcp__ace-tool__search_context, mcp__ccw-tools__read_file, mcp__ccw-tools__write_file, mcp__ccw-tools__edit_file, mcp__ccw-tools__team_msg
---

# Team UI Design

Systematic UI design pipeline: research -> design tokens -> review -> implementation. Built on **team-worker agent architecture** — all worker roles share a single agent definition with role-specific Phase 2-4 loaded from `roles/<role>/role.md`.

## Architecture

```
Skill(skill="team-uidesign", args="task description")
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
                    v       v       v       v
           [team-worker agents, each loads roles/<role>/role.md]
          researcher  designer  reviewer  implementer
```

## Role Registry

| Role | Path | Prefix | Inner Loop |
|------|------|--------|------------|
| coordinator | [roles/coordinator/role.md](roles/coordinator/role.md) | — | — |
| researcher | [roles/researcher/role.md](roles/researcher/role.md) | RESEARCH-* | false |
| designer | [roles/designer/role.md](roles/designer/role.md) | DESIGN-* | false |
| reviewer | [roles/reviewer/role.md](roles/reviewer/role.md) | AUDIT-* | false |
| implementer | [roles/implementer/role.md](roles/implementer/role.md) | BUILD-* | false |

## Role Router

Parse `$ARGUMENTS`:
- Has `--role <name>` → Read `roles/<name>/role.md`, execute Phase 2-4
- No `--role` → `@roles/coordinator/role.md`, execute entry router

## Shared Constants

- **Session prefix**: `UDS`
- **Session path**: `.workflow/.team/UDS-<slug>-<date>/`
- **CLI tools**: `ccw cli --mode analysis` (read-only), `ccw cli --mode write` (modifications)
- **Message bus**: `mcp__ccw-tools__team_msg(session_id=<session-id>, ...)`
- **Max GC rounds**: 2

## Worker Spawn Template

Coordinator spawns workers using this template:

```
Agent({
  subagent_type: "team-worker",
  description: "Spawn <role> worker for <task-id>",
  team_name: "uidesign",
  name: "<role>",
  run_in_background: true,
  prompt: `## Role Assignment
role: <role>
role_spec: <skill_root>/roles/<role>/role.md
session: <session-folder>
session_id: <session-id>
team_name: uidesign
requirement: <task-description>
inner_loop: false

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
.workflow/.team/UDS-<slug>-<date>/
├── .msg/
│   ├── messages.jsonl         # Team message bus
│   └── meta.json              # Pipeline config + GC state
├── research/                  # Researcher output
│   ├── design-system-analysis.json
│   ├── component-inventory.json
│   ├── accessibility-audit.json
│   └── design-intelligence.json
├── design/                    # Designer output
│   ├── design-tokens.json
│   ├── component-specs/
│   └── layout-specs/
├── audit/                     # Reviewer output
│   └── audit-*.md
├── build/                     # Implementer output
│   ├── token-files/
│   └── component-files/
└── wisdom/                    # Cross-task knowledge
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown command | Error with available command list |
| Role not found | Error with role registry |
| Session corruption | Attempt recovery, fallback to manual |
| Fast-advance conflict | Coordinator reconciles on next callback |
| Completion action fails | Default to Keep Active |
| GC loop stuck > 2 rounds | Escalate to user: accept / retry / terminate |
