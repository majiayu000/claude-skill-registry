---
name: team-review
description: Unified team skill for code review. 3-role pipeline: scanner, reviewer, fixer. Triggers on "team-review".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Agent(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*), mcp__ace-tool__search_context(*)
---

# Team Review

Orchestrate multi-agent code review: scanner -> reviewer -> fixer. Toolchain + LLM scan, deep analysis with root cause enrichment, and automated fix with rollback-on-failure.

## Architecture

```
Skill(skill="team-review", args="task description")
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
                    v       v       v
                [scan]  [review]  [fix]
                team-worker agents, each loads roles/<role>/role.md
```

## Role Registry

| Role | Path | Prefix | Inner Loop |
|------|------|--------|------------|
| coordinator | [roles/coordinator/role.md](roles/coordinator/role.md) | — | — |
| scanner | [roles/scanner/role.md](roles/scanner/role.md) | SCAN-* | false |
| reviewer | [roles/reviewer/role.md](roles/reviewer/role.md) | REV-* | false |
| fixer | [roles/fixer/role.md](roles/fixer/role.md) | FIX-* | true |

## Role Router

Parse `$ARGUMENTS`:
- Has `--role <name>` -> Read `roles/<name>/role.md`, execute Phase 2-4
- No `--role` -> `@roles/coordinator/role.md`, execute entry router

## Shared Constants

- **Session prefix**: `RV`
- **Session path**: `.workflow/.team/RV-<slug>-<date>/`
- **Team name**: `review`
- **CLI tools**: `ccw cli --mode analysis` (read-only), `ccw cli --mode write` (modifications)
- **Message bus**: `mcp__ccw-tools__team_msg(session_id=<session-id>, ...)`

## Worker Spawn Template

Coordinator spawns workers using this template:

```
Agent({
  subagent_type: "team-worker",
  description: "Spawn <role> worker",
  team_name: "review",
  name: "<role>",
  run_in_background: true,
  prompt: `## Role Assignment
role: <role>
role_spec: <skill_root>/roles/<role>/role.md
session: <session-folder>
session_id: <session-id>
team_name: review
requirement: <task-description>
inner_loop: <true|false>

Read role_spec file (@<skill_root>/roles/<role>/role.md) to load Phase 2-4 domain instructions.
Execute built-in Phase 1 (task discovery) -> role Phase 2-4 -> built-in Phase 5 (report).`
})
```

## User Commands

| Command | Action |
|---------|--------|
| `check` / `status` | View pipeline status graph |
| `resume` / `continue` | Advance to next step |
| `--full` | Enable scan + review + fix pipeline |
| `--fix` | Fix-only mode (skip scan/review) |
| `-q` / `--quick` | Quick scan only |
| `--dimensions=sec,cor,prf,mnt` | Custom dimensions |
| `-y` / `--yes` | Skip confirmations |

## Completion Action

When pipeline completes, coordinator presents:

```
AskUserQuestion({
  questions: [{
    question: "Review pipeline complete. What would you like to do?",
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

## Session Directory

```
.workflow/.team/RV-<slug>-<date>/
├── .msg/messages.jsonl     # Team message bus
├── .msg/meta.json          # Session state + cross-role state
├── wisdom/                 # Cross-task knowledge
├── scan/                   # Scanner output
├── review/                 # Reviewer output
└── fix/                    # Fixer output
```

## Specs Reference

- [specs/pipelines.md](specs/pipelines.md) — Pipeline definitions and task registry
- [specs/dimensions.md](specs/dimensions.md) — Review dimension definitions (SEC/COR/PRF/MNT)
- [specs/finding-schema.json](specs/finding-schema.json) — Finding data schema
- [specs/team-config.json](specs/team-config.json) — Team configuration

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with available role list |
| Role not found | Error with expected path (roles/<name>/role.md) |
| CLI tool fails | Worker fallback to direct implementation |
| Scanner finds 0 findings | Report clean, skip review + fix |
| User declines fix | Delete FIX tasks, complete with review-only results |
| Fast-advance conflict | Coordinator reconciles on next callback |
| Completion action fails | Default to Keep Active |
