---
name: team-ultra-analyze
description: Deep collaborative analysis team skill. All roles route via this SKILL.md. Beat model is coordinator-only (monitor.md). Structure is roles/ + specs/. Triggers on "team ultra-analyze", "team analyze".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Agent(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team Ultra Analyze

Deep collaborative analysis: explore -> analyze -> discuss -> synthesize. Supports Quick/Standard/Deep pipeline modes with configurable depth (N parallel agents). Discussion loops enable user-guided progressive understanding.

## Architecture

```
Skill(skill="team-ultra-analyze", args="<topic>")
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
                    +-------+-------+-------+-------+
                    v       v       v       v
                 [team-worker agents, each loads roles/<role>/role.md]

Pipeline (Standard mode):
  [EXPLORE-1..N](parallel) -> [ANALYZE-1..N](parallel) -> DISCUSS-001 -> SYNTH-001

Pipeline (Deep mode):
  [EXPLORE-1..N] -> [ANALYZE-1..N] -> DISCUSS-001 -> ANALYZE-fix -> DISCUSS-002 -> ... -> SYNTH-001

Pipeline (Quick mode):
  EXPLORE-001 -> ANALYZE-001 -> SYNTH-001
```

## Role Registry

| Role | Path | Prefix | Inner Loop |
|------|------|--------|------------|
| coordinator | [roles/coordinator/role.md](roles/coordinator/role.md) | — | — |
| explorer | [roles/explorer/role.md](roles/explorer/role.md) | EXPLORE-* | false |
| analyst | [roles/analyst/role.md](roles/analyst/role.md) | ANALYZE-* | false |
| discussant | [roles/discussant/role.md](roles/discussant/role.md) | DISCUSS-* | false |
| synthesizer | [roles/synthesizer/role.md](roles/synthesizer/role.md) | SYNTH-* | false |

## Role Router

Parse `$ARGUMENTS`:
- Has `--role <name>` → Read `roles/<name>/role.md`, execute Phase 2-4
- No `--role` → `@roles/coordinator/role.md`, execute entry router

## Shared Constants

- **Session prefix**: `UAN`
- **Session path**: `.workflow/.team/UAN-<slug>-<date>/`
- **Team name**: `ultra-analyze`
- **CLI tools**: `ccw cli --mode analysis` (read-only), `ccw cli --mode write` (modifications)
- **Message bus**: `mcp__ccw-tools__team_msg(session_id=<session-id>, ...)`

## Worker Spawn Template

Coordinator spawns workers using this template:

```
Agent({
  subagent_type: "team-worker",
  description: "Spawn <role> worker",
  team_name: "ultra-analyze",
  name: "<agent-name>",
  run_in_background: true,
  prompt: `## Role Assignment
role: <role>
role_spec: <skill_root>/roles/<role>/role.md
session: <session-folder>
session_id: <session-id>
team_name: ultra-analyze
requirement: <topic-description>
agent_name: <agent-name>
inner_loop: false

Read role_spec file (@<skill_root>/roles/<role>/role.md) to load Phase 2-4 domain instructions.
Execute built-in Phase 1 (task discovery, owner=<agent-name>) -> role Phase 2-4 -> built-in Phase 5 (report).`
})
```

## User Commands

| Command | Action |
|---------|--------|
| `check` / `status` | Output execution status diagram, do not advance pipeline |
| `resume` / `continue` | Check worker status, advance to next pipeline step |

## Session Directory

```
.workflow/.team/UAN-{slug}-{YYYY-MM-DD}/
+-- .msg/messages.jsonl          # Message bus log
+-- .msg/meta.json               # Session metadata + cross-role state
+-- discussion.md                # Understanding evolution and discussion timeline
+-- explorations/                # Explorer output
|   +-- exploration-001.json
|   +-- exploration-002.json
+-- analyses/                    # Analyst output
|   +-- analysis-001.json
|   +-- analysis-002.json
+-- discussions/                 # Discussant output
|   +-- discussion-round-001.json
+-- conclusions.json             # Synthesizer output
+-- wisdom/                      # Cross-task knowledge
|   +-- learnings.md
|   +-- decisions.md
|   +-- conventions.md
|   +-- issues.md
```

## Completion Action

When pipeline completes, coordinator presents:

```
AskUserQuestion({
  questions: [{
    question: "Ultra-Analyze pipeline complete. What would you like to do?",
    header: "Completion",
    multiSelect: false,
    options: [
      { label: "Archive & Clean (Recommended)", description: "Archive session, clean up tasks and team resources" },
      { label: "Keep Active", description: "Keep session active for follow-up work or inspection" },
      { label: "Export Results", description: "Export deliverables to a specified location, then clean" }
    ]
  }]
})
```

| Choice | Action |
|--------|--------|
| Archive & Clean | Update session status="completed" -> TeamDelete() -> output final summary |
| Keep Active | Update session status="paused" -> output resume instructions |
| Export Results | AskUserQuestion for target path -> copy deliverables -> Archive & Clean |

## Specs Reference

- [specs/team-config.json](specs/team-config.json) — Team configuration and pipeline settings

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with role registry list |
| Role file not found | Error with expected path (roles/{name}/role.md) |
| Discussion loop stuck >5 rounds | Force synthesis, offer continuation |
| CLI tool unavailable | Fallback chain: gemini -> codex -> manual analysis |
| Explorer agent fails | Continue with available context, note limitation |
| Fast-advance conflict | Coordinator reconciles on next callback |
| Completion action fails | Default to Keep Active |
