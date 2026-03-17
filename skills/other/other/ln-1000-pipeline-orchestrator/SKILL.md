---
name: ln-1000-pipeline-orchestrator
description: "Meta-orchestrator: reads kanban board, lets user pick ONE Story, drives it through pipeline 300->310->400->500 via TeamCreate. Creates worktree isolation; coordinates workers + reports."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Pipeline Orchestrator

Meta-orchestrator that reads the kanban board, shows available Stories, lets the user pick one to process, and drives it through the full pipeline (task planning -> validation -> execution -> quality gate) using Claude Code Agent Teams.

## Purpose & Scope
- Parse kanban board and show available Stories for user selection
- Ask business questions in ONE batch before execution; make technical decisions autonomously
- Spawn worker via TeamCreate for selected Story (single worker)
- Drive selected Story through 4 stages: ln-300 -> ln-310 -> ln-400 -> ln-500
- Collect branch name + stats from worker reports, generate pipeline report
- Handle failures, retries, and escalation to user

## Hierarchy

```
L0: ln-1000-pipeline-orchestrator (TeamCreate lead, delegate mode, single story)
  +-- Worker (fresh per stage, shutdown after completion, one at a time)
       |   All stages: Opus 4.6  |  Effort: Stage 0 = low | Stage 1,2 = medium | Stage 3 = medium
       |   Names: story-{id}-decompose | story-{id}-validate | story-{id}-implement | story-{id}-qa
       +-- L1: ln-300 / ln-310 / ln-400 / ln-500 (invoked via Skill tool, as-is)
            +-- L2/L3: existing hierarchy unchanged
```

**Key principle:** ln-1000 does NOT modify existing skills. Workers invoke ln-300/ln-310/ln-400/ln-500 through Skill tool exactly as a human operator would.

## MCP Tool Preferences

When `mcp__hashline-edit__*` tools are available, workers MUST prefer them over standard file tools:

| Standard Tool | Hashline-Edit Replacement | Why |
|---------------|--------------------------|-----|
| `Read` | `mcp__hashline-edit__read_file` | Hash-prefixed lines enable precise edits |
| `Edit` | `mcp__hashline-edit__edit_file` | Atomic validation prevents corruption |
| `Write` | `mcp__hashline-edit__write_file` | Same behavior, consistent interface |
| `Grep` | `mcp__hashline-edit__grep` | Results include hashline refs for follow-up edits |

**Fallback:** If hashline-edit MCP unavailable (tools not in ToolSearch), use standard tools. No error.

## Task Storage Mode

**MANDATORY READ:** Load `shared/references/tools_config_guide.md` and `shared/references/storage_mode_detection.md`

Extract: `task_provider` = Task Management → Provider (`linear` | `file`).

## Agent Teams Mode

Extract from `docs/tools_config.md` → Agent Teams → Mode:
- `teams`: Full Agent Teams (TeamCreate + heartbeat + SendMessage). Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
- `subagents`: Fallback. Sequential Agent() spawns, results return directly. No heartbeat needed. ~2x cheaper.

IF tools_config.md has no Agent Teams section:
  1. Check env var: `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`
  2. IF "1" → ask user: "Agent Teams available. Use teams mode (richer coordination, ~2x cost) or subagents mode (simpler, cheaper)?"
  3. IF absent → set mode=subagents, WARN: "Agent Teams env var not set. Using subagent mode."
  4. Update docs/tools_config.md with detected mode

## When to Use
- One Story ready for processing — user picks which one
- Need end-to-end automation: task planning -> validation -> execution -> quality gate
- Want controlled Story processing with pipeline report

## Pipeline: 4-Stage State Machine

**MANDATORY READ:** Load `references/pipeline_states.md` for transition rules and guards.

```
Backlog       --> Stage 0 (ln-300) --> Backlog      --> Stage 1 (ln-310) --> Todo
(no tasks)        create tasks         (tasks exist)      validate            |
                                                          | NO-GO             |
                                                          v                   v
                                                       [retry/ask]    Stage 2 (ln-400)
                                                                             |
                                                                             v
                                                                      To Review
                                                                             |
                                                                             v
                                                                      Stage 3 (ln-500)
                                                                       |          |
                                                                      PASS       FAIL
                                                                       |          v
                                                                      Done    To Rework -> Stage 2
                                                               (branch pushed)  (max 2 cycles)
```

| Stage | Skill | Input Status | Output Status |
|-------|-------|-------------|--------------|
| 0 | ln-300-task-coordinator | Backlog (no tasks) | Backlog (tasks created) |
| 1 | ln-310-multi-agent-validator | Backlog (tasks exist) | Todo |
| 2 | ln-400-story-executor | Todo / To Rework | To Review |
| 3 | ln-500-story-quality-gate | To Review | Done / To Rework |

## Team Lead Responsibilities

This skill runs as a **team lead** in delegate mode. The agent executing ln-1000 MUST NOT write code or invoke skills directly.

| Responsibility | Description |
|---------------|-------------|
| **Coordinate** | Assign stages to worker, process completion reports, advance pipeline |
| **Verify board** | Re-read kanban/Linear after each stage. Workers update via skills; lead ASSERTs expected state transitions |
| **Escalate** | Route failures to user when retry limits exceeded |
| **Report** | Collect branch name + stats from worker, generate pipeline report |
| **Shutdown** | Graceful worker shutdown, team cleanup |

**NEVER do as lead:** Invoke ln-300/ln-310/ln-400/ln-500 directly. Edit source code. Skip quality gate. Force-kill workers.

## Workflow

### Phase 0: Recovery Check

```
IF .pipeline/state.json exists AND complete == false:
  # Previous run interrupted — resume from saved state
  1. Read .pipeline/state.json → restore: selected_story_id, story_state, worker_map,
     quality_cycles, validation_retries, crash_count,
     story_results, infra_issues,
     stage_timestamps, git_stats, pipeline_start_time, readiness_scores
  2. Read .pipeline/checkpoint-{selected_story_id}.json → validate story_state consistency
     (checkpoint.stage should match story_state[id])
  3. Re-read kanban board → verify selected story still exists
  4. Read team config → verify worker_map members still exist
  5. Set suspicious_idle = false (ephemeral, reset on recovery)
  5a. IF worktree_dir exists (.worktrees/story-{selected_story_id}): cd {worktree_dir}
  6. IF story_state[id] IN ("STAGE_0".."STAGE_3"):
     IF checkpoint.agentId exists → Agent(resume: checkpoint.agentId)
     ELSE → respawn worker with checkpoint context (see checkpoint_format.md)
  7. Jump to Phase 4 event loop

IF .pipeline/state.json NOT exists OR complete == true:
  # Fresh start — proceed to Phase 1
```

### Phase 1: Discovery, Kanban Parsing & Story Selection

**MANDATORY READ:** Load `references/kanban_parser.md` for parsing patterns.

1. Auto-discover `docs/tasks/kanban_board.md` (or Linear API via storage mode operations)
2. Extract project brief from target project's CLAUDE.md (NOT skills repo):
   ```
   project_brief = {
     name: <from H1 or first line>,
     tech: <from Development Commands / tech references>,
     type: <inferred: "CLI", "API", "web app", "library">,
     key_rules: <2-3 critical rules>
   }
   IF not found: project_brief = { name: basename(project_root), tech: "unknown" }
   ```
3. Parse all status sections: Backlog, Todo, In Progress, To Review, To Rework
4. Extract Story list with: ID, title, status, Epic name, task presence
5. Filter: skip Stories in Done, Postponed, Canceled
6. Detect task presence per Story:
   - Has `_(tasks not created yet)_` → **no tasks** → Stage 0
   - Has task lines (4-space indent) → **tasks exist** → Stage 1+
7. Determine target stage per Story (see `references/pipeline_states.md` Stage-to-Status Mapping)
8. Show available Stories and ask user to pick ONE:
   ```
   Project: {project_brief.name} ({project_brief.tech})

   Available Stories:
   | # | Story | Status | Stage | Skill | Epic |
   |---|-------|--------|-------|-------|------|
   | 1 | PROJ-42: Auth endpoint | To Review | 3 | ln-500 | Epic: Auth |
   | 2 | PROJ-55: CRUD users | Backlog (no tasks) | 0 | ln-300 | Epic: Users |
   | 3 | PROJ-60: Dashboard | Todo | 2 | ln-400 | Epic: UI |

   AskUserQuestion: "Which story to process? Enter # or Story ID."
   ```
9. Store selected story. Extract story brief for selected story only:
   ```
   description = get_issue(selected_story.id).description
   story_briefs[id] = parse <!-- ORCHESTRATOR_BRIEF_START/END --> markers
   IF no markers: story_briefs[id] = { tech: project_brief.tech, keyFiles: "unknown" }
   ```

### Phase 2: Pre-flight Questions (ONE batch)

1. Load selected Story description (metadata only)
2. Scan for business ambiguities — questions where:
   - Answer cannot be found in codebase, docs, or standards
   - Answer requires business/product decision (payment provider, auth flow, UI preference)
3. Collect ALL business questions into single AskUserQuestion:
   ```
   "Before starting Story {selected_story.id}:
    Which payment provider? (Stripe/PayPal/both)
    Auth flow — JWT or session-based?"
   ```
4. Technical questions — resolve using project_brief:
   - Library versions: MCP Ref / Context7 (for `project_brief.tech` ecosystem)
   - Architecture patterns: `project_brief.key_rules`
   - Standards compliance: ln-310 Phase 2 handles this
5. Store answers in shared context (pass to worker via spawn prompt)

**Skip Phase 2** if no business questions found. Proceed directly to Phase 3.

### Phase 3: Team Setup

**MANDATORY READ:** Load `references/settings_template.json` for required permissions and hooks.

#### 3.0 Linear Status Cache (Linear mode only)

```
IF storage_mode == "linear":
  statuses = list_issue_statuses(teamId=team_id)
  status_cache = {status.name: status.id FOR status IN statuses}

  REQUIRED = ["Backlog", "Todo", "In Progress", "To Review", "To Rework", "Done"]
  missing = [s for s in REQUIRED if s not in status_cache]
  IF missing: ABORT "Missing Linear statuses: {missing}. Configure workflow."

  # Persist in state.json (added in 3.2) and pass to workers via prompt CONTEXT
```

#### 3.1 Pre-flight: Settings Verification

**IF agent_teams_mode == "teams":**

Verify `.claude/settings.local.json` in target project:
- `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` = `"1"` (required for TeamCreate/SendMessage)
- `defaultMode` = `"bypassPermissions"` (required for workers)
- `hooks.Stop` registered → `pipeline-keepalive.sh`
- `hooks.TeammateIdle` registered → `worker-keepalive.sh`

If missing or incomplete → copy from `references/settings_template.json` and install hook scripts via Bash `cp` (NOT Write tool — Write produces CRLF on Windows, breaking `#!/bin/bash` shebang):
```
# Preflight: verify dependencies
which jq || ABORT "jq is required for pipeline hooks. Install: https://jqlang.github.io/jq/download/"

mkdir -p .claude/hooks
Bash: cp {skill_repo}/ln-1000-pipeline-orchestrator/references/hooks/pipeline-keepalive.sh .claude/hooks/pipeline-keepalive.sh
Bash: cp {skill_repo}/ln-1000-pipeline-orchestrator/references/hooks/worker-keepalive.sh  .claude/hooks/worker-keepalive.sh
```

**Hook troubleshooting:** If hooks fail with "No such file or directory":
1. Verify hook commands use `bash .claude/hooks/script.sh` (relative path, no env vars — `$CLAUDE_PROJECT_DIR` is NOT available in hook shell context)
2. Verify `.claude/hooks/*.sh` files exist and have `#!/bin/bash` shebang
3. On Windows: ensure LF line endings in .sh files (see hook installation above — use Bash `cp`, not Write tool)

**IF agent_teams_mode == "subagents":**

Verify `.claude/settings.local.json` in target project:
- `defaultMode` = `"bypassPermissions"` (required for subagent workers)

No hooks, no env var, no TeamCreate needed — subagents return results directly to lead.

#### 3.2 Initialize Pipeline State

```
pipeline_dir = "$(pwd)/.pipeline"                    # Absolute path — workers in worktree use this
Write .pipeline/state.json (schema: checkpoint_format.md → Pipeline State Schema):
  Initialize: complete=false, selected_story_id, stories_remaining=1,
  all counters=0, empty collections, team_name="pipeline-{YYYY-MM-DD}",
  business_answers from Phase 2, storage_mode, project_brief, story_briefs,
  status_cache (Linear) or {} (file), pipeline_dir
Write .pipeline/lead-session.id with current session_id   # Stop hook uses this to only keep lead alive
```

#### 3.2a Sleep Prevention (Windows only)

```
IF platform == "win32":
  Bash: cp {skill_repo}/ln-1000-pipeline-orchestrator/references/hooks/prevent-sleep.ps1 .claude/hooks/prevent-sleep.ps1
  Bash: powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File .claude/hooks/prevent-sleep.ps1 &
  sleep_prevention_pid = $!
  # Script polls .pipeline/state.json — self-terminates when complete=true
  # Fallback: Windows auto-releases execution state on process exit
```

#### 3.3 Create Team

**Model routing:** All stages use `model: "opus"`. Thinking mode: always enabled (adaptive). Crash recovery = same effort as target stage.

| Worker | Stage 0 | Stage 1 | Stage 2 | Stage 3 |
|--------|---------|---------|---------|---------|
| Effort | low | medium | medium | medium |

**IF agent_teams_mode == "teams":**
```
TeamCreate(team_name: "pipeline-{YYYY-MM-DD}-{HHmm}")
# TeamCreate assigns lead name "team-lead" (lead_agent_id: "team-lead@{team_name}")
# Workers use recipient: "team-lead" — hardcoded in references/worker_prompts.md
```

**IF agent_teams_mode == "subagents":**
Skip TeamCreate. Lead spawns Agent() calls directly in Phase 4.
Workers are sequential subagents — no team_name, no SendMessage, no heartbeat.

#### 3.4 Worktree Isolation

**MANDATORY READ:** Load `shared/references/git_worktree_fallback.md`

```
branch_check = git branch --show-current
IF branch_check matches feature/* / optimize/* / upgrade/* / modernize/*:
  # Already isolated — skip (standalone ln-400 created it earlier)
  worktree_dir = CWD
ELSE:
  # Create worktree so ALL workers (Stage 0-3) operate in feature branch
  story_slug = slugify(selected_story.title)    # lowercase, spaces→dashes
  branch = "feature/{selected_story_id}-{story_slug}"
  worktree_dir = ".worktrees/story-{selected_story_id}"

  # Carry uncommitted changes (per git_worktree_fallback.md steps 2-3a)
  changes = git diff HEAD
  IF changes not empty:
    git diff HEAD > .pipeline/carry-changes.patch

  git fetch origin
  git worktree add -b {branch} {worktree_dir} origin/master    # Branch from origin/master directly, don't touch current branch

  IF .pipeline/carry-changes.patch exists:
    git -C {worktree_dir} apply .pipeline/carry-changes.patch && rm .pipeline/carry-changes.patch
    IF apply fails: WARN user "Patch conflicts — continuing without uncommitted changes"

  cd {worktree_dir}    # All subsequent workers inherit this CWD
```

Workers self-detect `feature/*` on startup → skip their own worktree creation (ln-400 Phase 1 step 5).

### Phase 4: Execution Loop

**MANDATORY READ:** Load `references/message_protocol.md` for exact message formats and parsing regex.
**MANDATORY READ:** Load `references/worker_health_contract.md` for crash detection and respawn rules.

**Lead operates in delegate mode — coordination only, no code writing.**

**MANDATORY READ:** Load `references/checkpoint_format.md` for checkpoint schema and resume protocol.

```
# --- INITIALIZATION (single story) ---
selected_story = <from Phase 1 selection>
quality_cycles[selected_story.id] = 0       # FAIL→retry counter, limit 2
validation_retries[selected_story.id] = 0   # NO-GO retry counter, limit 1
crash_count[selected_story.id] = 0          # crash respawn counter, limit 1
suspicious_idle = false                      # crash detection flag
story_state[selected_story.id] = "QUEUED"
worker_map = {}                              # {storyId: worker_name}
story_results = {}                           # {storyId: {stage0: "...", stage1_agents: "...", stage3_agents: "...", ...}} — for pipeline report
infra_issues = []                            # [{phase, type, message}] — infrastructure problems
heartbeat_count = 0                          # Heartbeat cycle counter (ephemeral, resets on recovery)
stage_timestamps = {}                        # {storyId: {stage_N_start: ISO, stage_N_end: ISO}}
git_stats = {}                               # {storyId: {lines_added, lines_deleted, files_changed}}
pipeline_start_time = now()                  # ISO 8601 — wall-clock start for duration metrics
readiness_scores = {}                        # {storyId: readiness_score} — from Stage 1 GO
previous_quality_score = {}                  # {storyId: score} — saved on FAIL for rework degradation detection

# Helper functions — defined in phase4_heartbeat.md (loaded above)
# skill_name_from_stage(stage), predict_next_step(stage), stage_duration(id, N)

# --- SPAWN FIRST WORKER ---
id = selected_story.id
target_stage = determine_stage(selected_story)    # pipeline_states.md guards
# Stage names: 0=decompose, 1=validate, 2=implement, 3=qa
stage_names = {0: "decompose", 1: "validate", 2: "implement", 3: "qa"}
worker_name = "story-{id}-{stage_names[target_stage]}"

IF agent_teams_mode == "teams":
  Agent(name: worker_name, team_name: "pipeline-{date}",
       model: "opus", mode: "bypassPermissions",
       subagent_type: "general-purpose",
       prompt: worker_prompt(selected_story, target_stage, business_answers))
  worker_map[id] = worker_name
  Write .pipeline/worker-{worker_name}-active.flag     # For TeammateIdle hook

IF agent_teams_mode == "subagents":
  result = Agent(name: worker_name,
       model: "opus", mode: "bypassPermissions",
       subagent_type: "general-purpose",
       prompt: worker_prompt_subagent(selected_story, target_stage, business_answers))
  # Result returns directly — parse for COMPLETE/ERROR, no SendMessage needed
  # worker_prompt_subagent = same as worker_prompt but WITHOUT Step 5 (ACK/shutdown)
  # Worker just does the work and returns result as final output

story_state[id] = "STAGE_{target_stage}"
stage_timestamps[id] = {}
stage_timestamps[id]["stage_{target_stage}_start"] = now()
Update .pipeline/state.json

# --- EVENT LOOP ---

IF agent_teams_mode == "teams":
  # Heartbeat-driven: Stop hook → exit 2 → new agentic loop → worker messages delivered → ON handlers → repeat
  # See: phase4_handlers.md (message processing), phase4_heartbeat.md (health monitoring + recovery)
  # Anti-pattern: NEVER say "waiting for messages" — heartbeat keeps lead alive automatically.
  # Context loss after compression? Follow recovery protocol in phase4_heartbeat.md.

IF agent_teams_mode == "subagents":
  # Sequential: Agent() returns result → parse → update state → spawn next Agent() → repeat
  # No heartbeat, no SendMessage, no crash detection needed — subagents are managed by Claude Code.
  # Crash recovery: use Agent(resume: agentId) to resume failed subagent.

WHILE story_state[id] NOT IN ("DONE", "PAUSED"):

  IF agent_teams_mode == "teams":
    # 1. Process worker messages (reactive message handling)
    #
    **MANDATORY READ:** Load `references/phases/phase4_handlers.md` for all ON message handlers:
    - Stage 0 COMPLETE / ERROR (task planning outcomes)
    - Stage 1 COMPLETE (GO / NO-GO validation outcomes with retry logic)
    - Stage 2 COMPLETE / ERROR (execution outcomes)
    - Stage 3 COMPLETE (PASS/CONCERNS/WAIVED/FAIL quality gate outcomes with rework cycles)
    - Worker crash detection (3-step protocol: flag → probe → respawn)

    Handlers include sender validation and state guards to prevent duplicate processing.

    # 2. Active done-flag verification (proactive health monitoring)
    #
    **MANDATORY READ:** Load `references/phases/phase4_heartbeat.md` for bidirectional health monitoring:
    - Lost message detection (done-flag exists but state not advanced)
    - Synthetic recovery from checkpoint + kanban verification (all 4 stages)
    - Fallback to probe protocol when checkpoint missing
    - Structured heartbeat output (single story status line)
    - Helper functions (skill_name_from_stage, predict_next_step)

    # 3. Heartbeat state persistence
    #
    ON HEARTBEAT (Stop hook stderr: "HEARTBEAT: ..."):
      Write .pipeline/state.json with ALL state variables.
      # phase4_heartbeat.md persistence details (loaded above)

  IF agent_teams_mode == "subagents":
    # Result already returned from Agent() call above (or from loop iteration below).
    # Parse result text for stage outcome:
    #   - Match "Stage {N} COMPLETE" → extract details, advance to next stage
    #   - Match "Stage {N} ERROR" → handle error per phase4_handlers.md logic
    #   - Apply same business logic as ON handlers (retry limits, quality cycles, etc.)
    #
    # Spawn next stage worker:
    next_stage = current_stage + 1    # or rework cycle per handler logic
    worker_name = "story-{id}-{stage_names[next_stage]}"
    result = Agent(name: worker_name,
         model: "opus", mode: "bypassPermissions",
         subagent_type: "general-purpose",
         prompt: worker_prompt_subagent(selected_story, next_stage, business_answers))
    # Parse result, update state, continue loop

    Update .pipeline/state.json

```

**`determine_stage(story)` routing:** Stage-to-Status Mapping table in `references/pipeline_states.md` (loaded above).

> **Worktree** created by ln-1000 in Phase 3.4 — all workers operate in `feature/*`. **Branch finalization** (commit, push, worktree cleanup) is handled by ln-500 after quality gate verdict. ln-1000 collects the branch name + stats from the worker's completion report.

### Phase 5: Cleanup & Report

```
# 0. Signal pipeline complete (allows Stop hook to pass)
Write .pipeline/state.json: { "complete": true, ... }

# 1. Self-verify against Definition of Done
verification = {
  story_selected:   selected_story_id is set              # Phase 1 ✓
  questions_asked:  business_answers stored OR none        # Phase 2 ✓
  team_created:     team exists OR agent_teams_mode == "subagents"  # Phase 3 ✓
  story_processed:  story_state[id] IN ("DONE", "PAUSED") # Phase 4 ✓
}
IF ANY verification == false: WARN user with details

# 2. Read stage notes (written by workers in .pipeline/)
stage_notes = {}
FOR N IN 0..3:
  IF .pipeline/stage_{N}_notes_{id}.md exists:
    stage_notes[N] = read file content
  ELSE:
    stage_notes[N] = "(no notes captured)"

# 3. Finalize pipeline report
durations = {N: stage_timestamps[id]["stage_{N}_end"] - stage_timestamps[id]["stage_{N}_start"]
             FOR N IN 0..3 IF both timestamps exist}

Write docs/tasks/reports/pipeline-{date}.md:

  # Pipeline Report — {date}

  **Story:** {selected_story_id} — {title}
  **Branch:** {branch_name from worker report}
  **Final State:** {story_state[id]}
  **Duration:** {now() - pipeline_start_time}

  ## Task Planning (ln-300)
  | Tasks | Plan Score | Duration |
  |-------|-----------|----------|
  | {N} created | {score}/4 | {durations[0]} |

  {stage_notes[0] — Key Decisions + Artifacts sections}

  ## Validation (ln-310)
  | Verdict | Readiness | Agent Review | Duration |
  |---------|-----------|-------------|----------|
  | {verdict} | {score}/10 | {story_results[id].stage1_agents} | {durations[1]} |

  {stage_notes[1] — Key Decisions + Artifacts sections}

  ## Implementation (ln-400)
  | Status | Files | Lines | Duration |
  |--------|-------|-------|----------|
  | {result} | {git_stats[id].files_changed} | +{git_stats[id].lines_added}/-{git_stats[id].lines_deleted} | {durations[2]} |

  {stage_notes[2] — Key Decisions + Artifacts sections}

  ## Quality Gate (ln-500)
  | Verdict | Score | Agent Review | Rework | Duration |
  |---------|-------|-------------|--------|----------|
  | {verdict} | {score}/100 | {story_results[id].stage3_agents} | {quality_cycles[id]} | {durations[3]} |

  {stage_notes[3] — Key Decisions + Artifacts sections}

  ## Pipeline Metrics
  | Wall-clock | Workers | Crashes | Validation retries | Infra issues |
  |------------|---------|---------|-------------------|--------------|
  | {total_duration} | {worker_spawn_count} | {crash_count[id]} | {validation_retries[id]} | {len(infra_issues)} |

  {IF infra_issues: list each issue with phase, type, message}

# 4. Show pipeline summary to user
```
Pipeline Complete:
| Story | Branch | Planning | Validation | Implementation | Quality Gate | State |
|-------|--------|----------|------------|----------------|-------------|-------|
| {id} | {branch} | {stage0} | {stage1} | {stage2} | {stage3} | {story_state[id]} |

Report saved: docs/tasks/reports/pipeline-{date}.md
```

# 5. Shutdown worker (if still active)
IF worker_map[id]:
  SendMessage(type: "shutdown_request", recipient: worker_map[id])

# 6. Cleanup team (with hung agent escalation)
SendMessage(type: "shutdown_request") to all remaining workers
TeamDelete(team_name)
IF TeamDelete fails (timeout 60s or error):
  # Force cleanup: platform doesn't support force-kill (#31788)
  Bash: rm -rf ~/.claude/teams/{team_name} ~/.claude/tasks/{team_name}
  Display: "TeamDelete blocked by hung agent. Force-cleaned team resources."

# 7. Worktree cleanup
IF story_state[id] == "PAUSED" AND worktree_dir exists AND worktree_dir != CWD:
  # Save partial work to branch before cleanup
  git -C {worktree_dir} add -A
  git -C {worktree_dir} commit -m "WIP: {storyId} pipeline paused at stage {current_stage}" --allow-empty
  git -C {worktree_dir} push -u origin {branch}
  # Clean worktree (branch preserved on remote)
  cd {project_root}
  git worktree remove {worktree_dir} --force
  Display: "Partial work saved to branch {branch} (remote). Worktree cleaned."
# IF story_state[id] == "DONE": worktree already cleaned by ln-500

# 8. Stop sleep prevention (Windows safety net)
IF sleep_prevention_pid:
  kill $sleep_prevention_pid 2>/dev/null || true

# 9. Remove pipeline state files
Delete .pipeline/ directory

# 10. Report results and report location to user
```

## Kanban as Single Source of Truth

- **Lead = single writer** to kanban_board.md. Workers report results via SendMessage; lead updates the board
- **Re-read board** after each stage completion for fresh state
- **Update algorithm:** Follow `shared/references/kanban_update_algorithm.md` for Epic grouping and indentation

## Error Handling

| Situation | Detection | Action |
|-----------|----------|--------|
| ln-300 task creation fails | Worker reports error | Escalate to user: "Cannot create tasks for Story {id}" |
| ln-310 NO-GO (Score <5) | Worker reports NO-GO | Retry once (ln-310 auto-fixes). If still NO-GO -> ask user |
| Task in To Rework 3+ times | Worker reports rework loop | Escalate: "Task X reworked 3 times, need input" |
| ln-500 FAIL | Worker reports FAIL verdict | Fix tasks auto-created by ln-500. Stage 2 re-entry. Max 2 quality cycles |
| Worker crash | TeammateIdle without completion msg | Re-spawn worker, resume from last stage |
| Business question mid-execution | Worker encounters ambiguity | Worker -> lead -> user -> lead -> worker (message chain) |

## Critical Rules

1. **Single Story processing.** One worker at a time. User selects which Story to process
2. **Delegate mode.** Lead coordinates only — never invoke ln-300/ln-310/ln-400/ln-500 directly. Workers do all execution
3. **Skills as-is.** Never modify or bypass existing skill logic. Workers call `Skill("ln-310-multi-agent-validator", args)` exactly as documented
4. **Kanban verification.** Workers update Linear/kanban via skills. Lead re-reads and ASSERTs expected state after each stage. In file mode, lead resolves merge conflicts
5. **Quality cycle limit.** Max 2 quality FAILs per Story (original + 1 rework cycle). After 2nd FAIL, escalate to user
6. **Worktree lifecycle.** ln-1000 creates worktree in Phase 3.4 (Pipeline-Managed model). Branch finalization (commit, push, worktree cleanup) owned by ln-500 on DONE. On PAUSED, lead saves partial work + cleans worktree in Phase 5
7. **Re-read kanban.** After every stage completion, re-read board for fresh state. Never cache
8. **Graceful shutdown.** Always attempt shutdown via shutdown_request first. If TeamDelete blocked by hung agent, force-clean team resources (Phase 5 step 6)

## Known Issues

| Symptom | Likely Cause | Self-Recovery |
|---------|-------------|---------------|
| Lead outputs generic text after long run | Context compression destroyed SKILL.md + state | Follow CONTEXT RECOVERY PROTOCOL in phase4_heartbeat.md |
| Worker checkpoint/done.flag not found | Worker in worktree wrote to `.worktrees/` not project root | `pipeline_dir` set as absolute path in Phase 3.2, passed to workers via `{pipeline_dir}` template var |
| hashline-edit tools unavailable | MCP tool references lost after compression | `ToolSearch("+hashline-edit")` to reload |
| Lead can't spawn workers after compression | team_name/business_answers lost | Read from `.pipeline/state.json` (persisted since Phase 3.2) |
| Workers DM wrong lead name | `recipient: "pipeline-lead"` — TeamCreate assigns `"team-lead"` | Use `recipient: "team-lead"` hardcoded in `references/worker_prompts.md` |

## Anti-Patterns
- Running ln-300/ln-310/ln-400/ln-500 directly from lead instead of delegating to workers
- Processing multiple stories without user selection
- Creating worktrees outside Phase 3.4 or managing branches post-creation (finalization owned by ln-500)
- Lead skipping kanban verification after worker updates (workers write via skills, lead MUST re-read + ASSERT)
- Skipping quality gate after execution
- Caching kanban state instead of re-reading
- Reading `~/.claude/teams/*/inboxes/*.json` directly (messages arrive automatically)
- Using `sleep` + filesystem polling for message checking
- Parsing internal Claude Code JSON formats (permission_request, idle_notification)
- Reusing same worker across stages (context exhaustion — spawn fresh worker per stage)
- Processing messages without verifying sender matches worker_map (stale message confusion from old/dead workers)

## Plan Mode Support

When invoked in Plan Mode, show available Stories and ask user which one to plan for:

1. Parse kanban board (Phase 1 steps 1-7)
2. Show available Stories table
3. AskUserQuestion: "Which story to plan for? Enter # or Story ID."
4. Execute Phase 2 (pre-flight questions) if business ambiguities found
5. Resolve `skill_repo_path` — absolute path to skills repo root (locate this SKILL.md, go up one level)
6. Show execution plan for selected Story
7. Write plan to plan file (using format below), call ExitPlanMode

**Plan Output Format:**
```
## Pipeline Plan for {date}

> **BEFORE EXECUTING — MANDATORY READ:** Load `{skill_repo_path}/ln-1000-pipeline-orchestrator/SKILL.md` (full file).
> This plan requires Agent Teams (TeamCreate), worktree isolation, delegate mode, and heartbeat event loop.
> The executing agent MUST NOT write code or invoke skills directly — only coordinate workers.
> After reading SKILL.md, start from Phase 3 (Team Setup) using the context below.

**Story:** {ID}: {Title}
**Current Status:** {status}
**Target Stage:** {N} ({skill_name})
**Storage Mode:** {file|linear}
**Project Brief:** {name} ({tech})
**Business Answers:** {answers from Phase 2, or "none"}
**Skill Repo Path:** {skill_repo_path}

### Execution Sequence
1. Read full SKILL.md + references (Phase 3 prerequisites)
2. TeamCreate("pipeline-{date}")
3. Spawn worker -> Stage {N} ({skill_name})
4. Drive through remaining stages via heartbeat event loop
5. Collect branch name + stats from worker reports
6. Generate pipeline report
7. Cleanup (Phase 5)

### Task Decomposition (from planning phase)
{task breakdown if available from Plan agent research}
```

## Definition of Done (self-verified in Phase 5)

Pipeline-level verification. Per-stage verifications are in `phase4_handlers.md` VERIFY blocks.

| # | Criterion | Verified By | Scope |
|---|-----------|-------------|-------|
| 1 | User selected Story | `selected_story_id` is set | Always |
| 2 | Business questions resolved | `business_answers` stored OR skip | Always |
| 3 | Team created + operated | team exists in state | Always |
| 4 | Story processed to terminal state | `story_state[id] IN ("DONE", "PAUSED")` | Always |
| 5 | Per-stage verifications passed | All VERIFY blocks passed (phase4_handlers.md) | DONE only |
| 6 | Pipeline report generated | Report file exists at `docs/tasks/reports/` | Always |
| 7 | Pipeline summary shown to user | Phase 5 table output | Always |
| 8 | Team cleaned up | TeamDelete called | Always |
| 9 | Worktree status communicated | DONE: cleaned by ln-500. PAUSED: saved + cleaned by lead | Always |
| 10 | Meta-Analysis run | Phase 6 completed, appended to pipeline report | Always |

## Phase 6: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md` and `references/phases/phase6_meta_analysis.md`

Skill type: `execution-orchestrator`. Runs after Phase 5. Pipeline-specific implementation (worker audit, recovery map, trend tracking, assumption audit, report format) in `phase6_meta_analysis.md`.

## Reference Files

### Phase 4-6 Procedures (Progressive Disclosure)
- **Message handlers:** `references/phases/phase4_handlers.md` (Plan Gate, Stage 0-3 ON handlers, crash detection)
- **Heartbeat & verification:** `references/phases/phase4_heartbeat.md` (Active done-flag checking, structured heartbeat output)
- **Meta-analysis:** `references/phases/phase6_meta_analysis.md` (Worker audit, recovery map, trend tracking, report format)

### Core Infrastructure
- **MANDATORY READ:** `shared/references/git_worktree_fallback.md`
- **MANDATORY READ:** `shared/references/research_tool_fallback.md`
- **Pipeline states:** `references/pipeline_states.md`
- **Worker prompts:** `references/worker_prompts.md`
- **Worker health:** `references/worker_health_contract.md`
- **Checkpoint format:** `references/checkpoint_format.md`
- **Message protocol:** `references/message_protocol.md`
- **Kanban parsing:** `references/kanban_parser.md`
- **Kanban update algorithm:** `shared/references/kanban_update_algorithm.md`
- **Settings template:** `references/settings_template.json`
- **Hooks:** `references/hooks/pipeline-keepalive.sh`, `references/hooks/worker-keepalive.sh`
- **Tools config:** `shared/references/tools_config_guide.md`
- **Storage mode operations:** `shared/references/storage_mode_detection.md`
- **Auto-discovery patterns:** `shared/references/auto_discovery_pattern.md`

### Delegated Skills
- `../ln-300-task-coordinator/SKILL.md`
- `../ln-310-multi-agent-validator/SKILL.md`
- `../ln-400-story-executor/SKILL.md`
- `../ln-500-story-quality-gate/SKILL.md`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-25
