---
name: team-lifecycle-v4
description: Full lifecycle team skill with clean architecture. SKILL.md is a universal router — all roles read it. Beat model is coordinator-only. Structure is roles/ + specs/ + templates/. Triggers on "team lifecycle v4".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Agent(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team Lifecycle v4

Orchestrate multi-agent software development: specification → planning → implementation → testing → review.

## Architecture

```
Skill(skill="team-lifecycle-v4", args="task description")
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
     +-- analyze → dispatch → spawn → STOP
                                 |
                    +--------+---+--------+
                    v        v            v
             [team-worker]  ...    [team-supervisor]
              per-task               resident agent
              lifecycle              message-driven
                                     (woken via SendMessage)
```

## Role Registry

| Role | Path | Prefix | Inner Loop |
|------|------|--------|------------|
| coordinator | [roles/coordinator/role.md](roles/coordinator/role.md) | — | — |
| analyst | [roles/analyst/role.md](roles/analyst/role.md) | RESEARCH-* | false |
| writer | [roles/writer/role.md](roles/writer/role.md) | DRAFT-* | true |
| planner | [roles/planner/role.md](roles/planner/role.md) | PLAN-* | true |
| executor | [roles/executor/role.md](roles/executor/role.md) | IMPL-* | true |
| tester | [roles/tester/role.md](roles/tester/role.md) | TEST-* | false |
| reviewer | [roles/reviewer/role.md](roles/reviewer/role.md) | REVIEW-*, QUALITY-*, IMPROVE-* | false |
| supervisor | [roles/supervisor/role.md](roles/supervisor/role.md) | CHECKPOINT-* | false |

## Role Router

Parse `$ARGUMENTS`:
- Has `--role <name>` → Read `roles/<name>/role.md`, execute Phase 2-4
- No `--role` → `@roles/coordinator/role.md`, execute entry router

## Shared Constants

- **Session prefix**: `TLV4`
- **Session path**: `.workflow/.team/TLV4-<slug>-<date>/`
- **CLI tools**: `ccw cli --mode analysis` (read-only), `ccw cli --mode write` (modifications)
- **Message bus**: `mcp__ccw-tools__team_msg(session_id=<session-id>, ...)`

## Worker Spawn Template

Coordinator spawns workers using this template:

```
Agent({
  subagent_type: "team-worker",
  description: "Spawn <role> worker",
  team_name: <team-name>,
  name: "<role>",
  run_in_background: true,
  prompt: `## Role Assignment
role: <role>
role_spec: <skill_root>/roles/<role>/role.md
session: <session-folder>
session_id: <session-id>
team_name: <team-name>
requirement: <task-description>
inner_loop: <true|false>

Read role_spec file (@<skill_root>/roles/<role>/role.md) to load Phase 2-4 domain instructions.
Execute built-in Phase 1 (task discovery) -> role Phase 2-4 -> built-in Phase 5 (report).`
})
```

## Supervisor Spawn Template

Supervisor is a **resident agent** (independent from team-worker). Spawned once during session init, woken via SendMessage for each CHECKPOINT task.

### Spawn (Phase 2 — once per session)

```
Agent({
  subagent_type: "team-supervisor",
  description: "Spawn resident supervisor",
  team_name: <team-name>,
  name: "supervisor",
  run_in_background: true,
  prompt: `## Role Assignment
role: supervisor
role_spec: <skill_root>/roles/supervisor/role.md
session: <session-folder>
session_id: <session-id>
team_name: <team-name>
requirement: <task-description>

Read role_spec file (@<skill_root>/roles/supervisor/role.md) to load checkpoint definitions.
Init: load baseline context, report ready, go idle.
Wake cycle: coordinator sends checkpoint requests via SendMessage.`
})
```

### Wake (handleSpawnNext — per CHECKPOINT task)

```
SendMessage({
  type: "message",
  recipient: "supervisor",
  content: `## Checkpoint Request
task_id: <CHECKPOINT-NNN>
scope: [<upstream-task-ids>]
pipeline_progress: <done>/<total> tasks completed`,
  summary: "Checkpoint request: <CHECKPOINT-NNN>"
})
```

### Shutdown (handleComplete)

```
SendMessage({
  type: "shutdown_request",
  recipient: "supervisor",
  content: "Pipeline complete, shutting down supervisor"
})
```

## User Commands

| Command | Action |
|---------|--------|
| `check` / `status` | View execution status graph |
| `resume` / `continue` | Advance to next step |
| `revise <TASK-ID> [feedback]` | Revise specific task |
| `feedback <text>` | Inject feedback for revision |
| `recheck` | Re-run quality check |
| `improve [dimension]` | Auto-improve weakest dimension |

## Completion Action

When pipeline completes, coordinator presents:

```
AskUserQuestion({
  questions: [{
    question: "Pipeline complete. What would you like to do?",
    header: "Completion",
    multiSelect: false,
    options: [
      { label: "Archive & Clean (Recommended)", description: "Archive session, clean up team" },
      { label: "Keep Active", description: "Keep session for follow-up work" },
      { label: "Export Results", description: "Export deliverables to target directory" }
    ]
  }]
})
```

## Specs Reference

- [specs/pipelines.md](specs/pipelines.md) — Pipeline definitions and task registry
- [specs/quality-gates.md](specs/quality-gates.md) — Quality gate criteria and scoring
- [specs/knowledge-transfer.md](specs/knowledge-transfer.md) — Artifact and state transfer protocols

## Session Directory

```
.workflow/.team/TLV4-<slug>-<date>/
├── team-session.json           # Session state + role registry
├── spec/                       # Spec phase outputs
├── plan/                       # Implementation plan + TASK-*.json
├── artifacts/                  # All deliverables
├── wisdom/                     # Cross-task knowledge
├── explorations/               # Shared explore cache
├── discussions/                # Discuss round records
└── .msg/                       # Team message bus
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown command | Error with available command list |
| Role not found | Error with role registry |
| CLI tool fails | Worker fallback to direct implementation |
| Fast-advance conflict | Coordinator reconciles on next callback |
| Supervisor crash | Respawn with `recovery: true`, auto-rebuilds from existing reports |
| Supervisor not ready for CHECKPOINT | Spawn/respawn supervisor, wait for ready, then wake |
| Completion action fails | Default to Keep Active |
