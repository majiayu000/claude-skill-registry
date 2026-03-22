---
name: team-perf-opt
description: Unified team skill for performance optimization. Coordinator orchestrates pipeline, workers are team-worker agents. Supports single/fan-out/independent parallel modes. Triggers on "team perf-opt".
allowed-tools: Agent, TaskCreate, TaskList, TaskGet, TaskUpdate, TeamCreate, TeamDelete, SendMessage, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, mcp__ace-tool__search_context
---

# Team Performance Optimization

Profile application performance, identify bottlenecks, design optimization strategies, implement changes, benchmark improvements, and review code quality.

## Architecture

```
Skill(skill="team-perf-opt", args="<task-description>")
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
                    +-------+-------+-------+-------+-------+
                    v       v       v       v       v
                 [profiler] [strategist] [optimizer] [benchmarker] [reviewer]
                 (team-worker agents)

Pipeline (Single mode):
  PROFILE-001 -> STRATEGY-001 -> IMPL-001 -> BENCH-001 + REVIEW-001 (fix cycle)

Pipeline (Fan-out mode):
  PROFILE-001 -> STRATEGY-001 -> [IMPL-B01..N](parallel) -> BENCH+REVIEW per branch

Pipeline (Independent mode):
  [Pipeline A: PROFILE-A->STRATEGY-A->IMPL-A->BENCH-A+REVIEW-A]
  [Pipeline B: PROFILE-B->STRATEGY-B->IMPL-B->BENCH-B+REVIEW-B] (parallel)
```

## Role Registry

| Role | Path | Prefix | Inner Loop |
|------|------|--------|------------|
| coordinator | [roles/coordinator/role.md](roles/coordinator/role.md) | — | — |
| profiler | [roles/profiler/role.md](roles/profiler/role.md) | PROFILE-* | false |
| strategist | [roles/strategist/role.md](roles/strategist/role.md) | STRATEGY-* | false |
| optimizer | [roles/optimizer/role.md](roles/optimizer/role.md) | IMPL-*, FIX-* | true |
| benchmarker | [roles/benchmarker/role.md](roles/benchmarker/role.md) | BENCH-* | false |
| reviewer | [roles/reviewer/role.md](roles/reviewer/role.md) | REVIEW-*, QUALITY-* | false |

## Role Router

Parse `$ARGUMENTS`:
- Has `--role <name>` → Read `roles/<name>/role.md`, execute Phase 2-4
- No `--role` → `@roles/coordinator/role.md`, execute entry router

## Shared Constants

- **Session prefix**: `PERF-OPT`
- **Session path**: `.workflow/.team/PERF-OPT-<slug>-<date>/`
- **Team name**: `perf-opt`
- **CLI tools**: `ccw cli --mode analysis` (read-only), `ccw cli --mode write` (modifications)
- **Message bus**: `mcp__ccw-tools__team_msg(session_id=<session-id>, ...)`

## Worker Spawn Template

Coordinator spawns workers using this template:

```
Agent({
  subagent_type: "team-worker",
  description: "Spawn <role> worker",
  team_name: "perf-opt",
  name: "<role>",
  run_in_background: true,
  prompt: `## Role Assignment
role: <role>
role_spec: <skill_root>/roles/<role>/role.md
session: <session-folder>
session_id: <session-id>
team_name: perf-opt
requirement: <task-description>
inner_loop: <true|false>

Read role_spec file (@<skill_root>/roles/<role>/role.md) to load Phase 2-4 domain instructions.
Execute built-in Phase 1 (task discovery) -> role Phase 2-4 -> built-in Phase 5 (report).`
})
```

**Inner Loop roles** (optimizer): Set `inner_loop: true`.
**Single-task roles** (profiler, strategist, benchmarker, reviewer): Set `inner_loop: false`.

## User Commands

| Command | Action |
|---------|--------|
| `check` / `status` | Output execution status graph (branch-grouped), no advancement |
| `resume` / `continue` | Check worker states, advance next step |
| `revise <TASK-ID> [feedback]` | Create revision task + cascade downstream (scoped to branch) |
| `feedback <text>` | Analyze feedback impact, create targeted revision chain |
| `recheck` | Re-run quality check |
| `improve [dimension]` | Auto-improve weakest dimension |

## Session Directory

```
.workflow/.team/PERF-OPT-<slug>-<date>/
+-- session.json                    # Session metadata + status + parallel_mode
+-- artifacts/
|   +-- baseline-metrics.json       # Profiler: before-optimization metrics
|   +-- bottleneck-report.md        # Profiler: ranked bottleneck findings
|   +-- optimization-plan.md        # Strategist: prioritized optimization plan
|   +-- benchmark-results.json      # Benchmarker: after-optimization metrics
|   +-- review-report.md            # Reviewer: code review findings
|   +-- branches/B01/...            # Fan-out branch artifacts
|   +-- pipelines/A/...             # Independent pipeline artifacts
+-- explorations/                   # Shared explore cache
+-- wisdom/patterns.md              # Discovered patterns and conventions
+-- discussions/                    # Discussion records
+-- .msg/messages.jsonl             # Team message bus
+-- .msg/meta.json                  # Session metadata
```

## Completion Action

When the pipeline completes:

```
AskUserQuestion({
  questions: [{
    question: "Team pipeline complete. What would you like to do?",
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

## Specs Reference

- [specs/pipelines.md](specs/pipelines.md) — Pipeline definitions and task registry
- [specs/team-config.json](specs/team-config.json) — Team configuration

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with role registry list |
| Role file not found | Error with expected path (roles/{name}/role.md) |
| Profiling tool not available | Fallback to static analysis methods |
| Benchmark regression detected | Auto-create FIX task with regression details |
| Review-fix cycle exceeds 3 iterations | Escalate to user |
| One branch IMPL fails | Mark that branch failed, other branches continue |
| Fast-advance conflict | Coordinator reconciles on next callback |
| Completion action fails | Default to Keep Active |
