---
name: team-executor
description: Lightweight session execution skill. Resumes existing team-coordinate sessions for pure execution via team-worker agents. No analysis, no role generation -- only loads and executes. Session path required. Triggers on "Team Executor".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Agent(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team Executor

Lightweight session execution skill: load session -> reconcile state -> spawn team-worker agents -> execute -> deliver. **No analysis, no role generation** -- only executes existing team-coordinate sessions.


## Architecture

```
+---------------------------------------------------+
|  Skill(skill="team-executor")                      |
|  args="--session=<path>" [REQUIRED]                |
+-------------------+-------------------------------+
                    | Session Validation
         +---- --session valid? ----+
         | NO                       | YES
         v                          v
    Error immediately          Orchestration Mode
    (no session)               -> executor
                                    |
                    +-------+-------+-------+
                    v       v       v       v
                 [team-worker agents loaded from session role-specs]
```

---

## Session Validation (BEFORE routing)

**CRITICAL**: Session validation MUST occur before any execution.

### Parse Arguments

Extract from `$ARGUMENTS`:
- `--session=<path>`: Path to team-coordinate session folder (REQUIRED)

### Validation Steps

1. **Check `--session` provided**:
   - If missing -> **ERROR**: "Session required. Usage: --session=<path-to-TC-folder>"

2. **Validate session structure** (see specs/session-schema.md):
   - Directory exists at path
   - `team-session.json` exists and valid JSON
   - `task-analysis.json` exists and valid JSON
   - `role-specs/` directory has at least one `.md` file
   - Each role in `team-session.json#roles` has corresponding `.md` file in `role-specs/`

3. **Validation failure**:
   - Report specific missing component
   - Suggest re-running team-coordinate or checking path

---

## Role Router

This skill is **executor-only**. Workers do NOT invoke this skill -- they are spawned as `team-worker` agents directly.

### Dispatch Logic

| Scenario | Action |
|----------|--------|
| No `--session` | **ERROR** immediately |
| `--session` invalid | **ERROR** with specific reason |
| Valid session | Orchestration Mode -> executor |

### Orchestration Mode

**Invocation**: `Skill(skill="team-executor", args="--session=<session-folder>")`

**Lifecycle**:
```
Validate session
  -> executor Phase 0: Reconcile state (reset interrupted, detect orphans)
  -> executor Phase 1: Spawn first batch team-worker agents (background) -> STOP
  -> Worker executes -> SendMessage callback -> executor advances next step
  -> Loop until pipeline complete -> Phase 2 report + completion action
```

**User Commands** (wake paused executor):

| Command | Action |
|---------|--------|
| `check` / `status` | Output execution status graph, no advancement |
| `resume` / `continue` | Check worker states, advance next step |

---

## Role Registry

| Role | File | Type |
|------|------|------|
| executor | [roles/executor/role.md](roles/executor/role.md) | built-in orchestrator |
| (dynamic) | `<session>/role-specs/<role-name>.md` | loaded from session |

---

## Executor Spawn Template

### v2 Worker Spawn (all roles)

When executor spawns workers, use `team-worker` agent with role-spec path:

```
Agent({
  subagent_type: "team-worker",
  description: "Spawn <role> worker",
  team_name: <team-name>,
  name: "<role>",
  run_in_background: true,
  prompt: `## Role Assignment
role: <role>
role_spec: <session-folder>/role-specs/<role>.md
session: <session-folder>
session_id: <session-id>
team_name: <team-name>
requirement: <task-description>
inner_loop: <true|false>

Read role_spec file to load Phase 2-4 domain instructions.`
})
```

---

## Completion Action

When pipeline completes (all tasks done), executor presents an interactive choice:

```
AskUserQuestion({
  questions: [{
    question: "Team pipeline complete. What would you like to do?",
    header: "Completion",
    multiSelect: false,
    options: [
      { label: "Archive & Clean (Recommended)", description: "Archive session, clean up team" },
      { label: "Keep Active", description: "Keep session for follow-up work" },
      { label: "Export Results", description: "Export deliverables to target directory, then clean" }
    ]
  }]
})
```

### Action Handlers

| Choice | Steps |
|--------|-------|
| Archive & Clean | Update session status="completed" -> TeamDelete -> output final summary with artifact paths |
| Keep Active | Update session status="paused" -> output: "Resume with: Skill(skill='team-executor', args='--session=<path>')" |
| Export Results | AskUserQuestion(target path) -> copy artifacts to target -> Archive & Clean |

---

## Integration with team-coordinate

| Scenario | Skill |
|----------|-------|
| New task, no session | team-coordinate |
| Existing session, resume execution | **team-executor** |
| Session needs new roles | team-coordinate (with resume) |
| Pure execution, no analysis | **team-executor** |

---

## Error Handling

| Scenario | Resolution |
|----------|------------|
| No --session provided | ERROR immediately with usage message |
| Session directory not found | ERROR with path, suggest checking path |
| team-session.json missing | ERROR, session incomplete, suggest re-run team-coordinate |
| task-analysis.json missing | ERROR, session incomplete, suggest re-run team-coordinate |
| No role-specs in session | ERROR, session incomplete, suggest re-run team-coordinate |
| Role-spec file not found | ERROR with expected path |
| capability_gap reported | Warn only, cannot generate new role-specs |
| Fast-advance spawns wrong task | Executor reconciles on next callback |
| Completion action fails | Default to Keep Active, log warning |
