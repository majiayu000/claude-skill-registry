---
name: ln-1000-pipeline-orchestrator
description: "Drives a Story through full pipeline (tasks, validation, execution, quality). Use when executing a Story end-to-end from kanban board."
disable-model-invocation: true
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

**Type:** L1 Orchestrator
**Category:** 1000 Pipeline

# Pipeline Orchestrator

Drives a selected Story through the full pipeline (task planning -> validation -> execution -> quality gate) by invoking coordinators as Skill() calls in a single context and advancing from coordinator stage artifacts.

## Purpose & Scope
- Parse kanban board and show available Stories for user selection
- Ask business questions in ONE batch before execution; make technical decisions autonomously
- Drive selected Story through 4 stages: ln-300 -> ln-310 -> ln-400 -> ln-500
- Write stage notes + checkpoints after each stage for reporting and recovery
- Handle failures, retries, rework cycles, and escalation to user
- Generate pipeline report with branch name, git stats, agent review info

## Hierarchy

```
L0: ln-1000-pipeline-orchestrator (sequential Skill calls, single context)
  +-- Skill("ln-300") — task decomposition (internally manages stateful task-plan workers)
  +-- Skill("ln-310") — validation (internally launches Codex/Gemini agents)
  +-- Skill("ln-400") — execution (internally dispatches stateful task workers)
  +-- Skill("ln-500") — quality gate (internally runs artifact-first ln-510/ln-520, verdict, finalization)
```

**Key principle:** ln-1000 invokes coordinators via Skill tool. Each coordinator manages its own internal worker dispatch and emits a stage artifact. ln-1000 does NOT modify existing skills — it calls them exactly as a human operator would and treats coordinator artifacts as the primary completion signal.

## Task Storage Mode

**MANDATORY READ:** Load `shared/references/environment_state_contract.md` and `shared/references/storage_mode_detection.md`

Extract: `task_provider` = Task Management -> Provider (`linear` | `file`).

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

## Workflow

### Phase 0: Recovery Check

```
PIPELINE="{skill_repo}/ln-1000-pipeline-orchestrator/scripts/cli.mjs"
recovery = Bash: node $PIPELINE status

IF recovery.active == true:
  # Previous run interrupted — resume from CLI state
  1. Extract: story_id, stage, resume_action from recovery JSON
  2. Read already-written stage artifacts and runtime state
  3. Re-read kanban board -> secondary verification only
  4. IF recovery.state.worktree_dir exists: cd {recovery.state.worktree_dir}
  5. Jump to Phase 4, starting from resume_action

IF recovery.active == false:
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
   - Has `_(tasks not created yet)_` -> **no tasks** -> Stage 0
   - Has task lines (4-space indent) -> **tasks exist** -> Stage 1+
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
2. Scan for business ambiguities -- questions where:
   - Answer cannot be found in codebase, docs, or standards
   - Answer requires business/product decision (payment provider, auth flow, UI preference)
3. Collect ALL business questions into single AskUserQuestion
4. Technical questions -- resolve using project_brief:
   - Library versions: MCP Ref / Context7 (for `project_brief.tech` ecosystem)
   - Architecture patterns: `project_brief.key_rules`
   - Standards compliance: ln-310 Phase 2 handles this

**Skip Phase 2** if no business questions found. Proceed directly to Phase 3.

### Phase 3: Pipeline Setup

#### 3.0 Linear Status Cache (Linear mode only)

```
IF storage_mode == "linear":
  statuses = list_issue_statuses(teamId=team_id)
  status_cache = {status.name: status.id FOR status IN statuses}

  REQUIRED = ["Backlog", "Todo", "In Progress", "To Review", "To Rework", "Done"]
  missing = [s for s in REQUIRED if s not in status_cache]
  IF missing: ABORT "Missing Linear statuses: {missing}. Configure workflow."
```

#### 3.1 Pre-flight: Settings Verification

Verify `.claude/settings.local.json` in target project:
- `defaultMode` = `"bypassPermissions"` (required for Agent workers spawned by coordinators)

#### 3.2 Worktree Isolation

**MANDATORY READ:** Load `shared/references/git_worktree_fallback.md`

```
branch_check = git branch --show-current
IF branch_check matches feature/* / optimize/* / upgrade/* / modernize/*:
  worktree_dir = CWD
  project_root = CWD
  branch = branch_check
ELSE:
  story_slug = slugify(selected_story.title)
  branch = "feature/{selected_story.id}-{story_slug}"
  worktree_dir = ".hex-skills/worktrees/story-{selected_story.id}"
  project_root = CWD

  changes = git diff HEAD
  IF changes not empty:
    git diff HEAD > .hex-skills/pipeline/carry-changes.patch

  git fetch origin
  base_branch = detect per shared/references/git_scope_detection.md §Base Branch Detection
  git worktree add -b {branch} {worktree_dir} origin/{base_branch}

  IF .hex-skills/pipeline/carry-changes.patch exists:
    git -C {worktree_dir} apply .hex-skills/pipeline/carry-changes.patch && rm .hex-skills/pipeline/carry-changes.patch
    IF apply fails: WARN user "Patch conflicts -- continuing without uncommitted changes"

  cd {worktree_dir}    # All subsequent Skill calls inherit this CWD
```

Coordinators self-detect `feature/*` on startup -> skip their own worktree creation (ln-400 Phase 1 step 5).

#### 3.3 Initialize Pipeline State

```
Bash: node $PIPELINE start \
  --story {selected_story.id} \
  --title "{selected_story.title}" \
  --storage {storage_mode} \
  --project-brief '{JSON.stringify(project_brief)}' \
  --story-briefs '{JSON.stringify(story_briefs)}' \
  --business-answers '{JSON.stringify(business_answers)}' \
  --status-cache '{JSON.stringify(status_cache)}' \
  --skill-repo-path "{skill_repo}" \
  --worktree-dir "{worktree_dir}" \
  --branch-name "{branch}"

IF result.recovery == true:
  # Active run found — resume instead of fresh start
  Jump to Phase 4 using result.state
```

#### 3.4 Sleep Prevention (Windows only)

```
IF platform == "win32":
  Bash: cp {skill_repo}/ln-1000-pipeline-orchestrator/references/hooks/prevent-sleep.ps1 .hex-skills/pipeline/prevent-sleep.ps1
  Bash: powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File .hex-skills/pipeline/prevent-sleep.ps1 &
  sleep_prevention_pid = $!
```

### Phase 4: Pipeline Execution

**MANDATORY READ:** Load `references/phases/phase4_flow.md` for ASSERT guards, stage notes, context recovery, and error handling.
**MANDATORY READ:** Load `references/checkpoint_format.md` for checkpoint schema.

```
# --- INITIALIZATION ---
id = selected_story.id
target_stage = determine_stage(selected_story)    # pipeline_states.md / guards.mjs

# --- PROGRESS TRACKER (survives compaction) ---
TodoWrite([
  {content: "Stage 0: Task Decomposition (ln-300)", status: "pending", activeForm: "Decomposing tasks"},
  {content: "Stage 1: Validation (ln-310)", status: "pending", activeForm: "Validating story"},
  {content: "Stage 2: Execution (ln-400)", status: "pending", activeForm: "Executing tasks"},
  {content: "Stage 3: Quality Gate (ln-500)", status: "pending", activeForm: "Running quality gate"},
  {content: "Pipeline Report + Cleanup", status: "pending", activeForm: "Generating report"}
])

# --- STAGE 0: Task Decomposition ---
IF target_stage <= 0:
  Bash: node $PIPELINE advance --story {id} --to STAGE_0
  Skill(skill: "ln-300-task-coordinator", args: "{id}")
  Read Stage 0 coordinator artifact -> Bash: node $PIPELINE record-stage-summary --story {id} --payload '{...}'
  ASSERT Stage 0 artifact: status=completed, stage=0
  Re-read kanban only as secondary assertion
  IF ASSERT fails: Bash: node $PIPELINE pause --story {id} --reason "Stage 0 artifact missing or invalid"; ESCALATE
  Write stage notes: .hex-skills/pipeline/stage_0_notes_{id}.md (Key Decisions, Artifacts)
  Bash: node $PIPELINE checkpoint --story {id} --stage 0 --plan-score {score} --tasks-remaining '{JSON tasks}' --last-action "Tasks created"

# --- STAGE 1: Validation ---
IF target_stage <= 1:
  Bash: node $PIPELINE advance --story {id} --to STAGE_1
  IF advance fails (guard rejection): handle per error.recovery
  Skill(skill: "ln-310-multi-agent-validator", args: "{id}")
  Read Stage 1 coordinator artifact -> Bash: node $PIPELINE record-stage-summary --story {id} --payload '{...}'
  ASSERT artifact verdict = GO and readiness_score >= 5
  IF NO-GO:
    Bash: node $PIPELINE advance --story {id} --to STAGE_1    # retry (guard auto-increments validation_retries)
    IF advance fails: Bash: node $PIPELINE pause --story {id} --reason "Validation retry exhausted"; ESCALATE
    Skill(skill: "ln-310-multi-agent-validator", args: "{id}")    # retry
    Read retry Stage 1 artifact -> Bash: node $PIPELINE record-stage-summary --story {id} --payload '{...}'
  Re-read kanban only as secondary assertion
  IF still NOT Todo: Bash: node $PIPELINE pause --story {id} --reason "Validation artifact or status invalid"; ESCALATE
  Extract agents_info from Stage 1 artifact metadata or review runtime state
  Write stage notes: .hex-skills/pipeline/stage_1_notes_{id}.md (Verdict, Agent Review, Key Decisions)
  Bash: node $PIPELINE checkpoint --story {id} --stage 1 --verdict {verdict} --readiness {score} --agents-info "{agents}" --last-action "Validated"

# --- COMPACTION RECOVERY (replaces old COMPACTION GUARD) ---
# If context compacted and vars lost: Bash: node $PIPELINE status --story {id}
# Extract resume_action from JSON -> continue from there. No manual JSON reads needed.

# --- STAGE 2+3 LOOP (rework cycle, managed by CLI guards) ---
WHILE true:

  # STAGE 2: Execution
  IF target_stage <= 2 OR (status shows rework cycle):
    Bash: node $PIPELINE advance --story {id} --to STAGE_2
    IF advance fails: Bash: node $PIPELINE pause --story {id} --reason "{error}"; ESCALATE; BREAK
    Skill(skill: "ln-400-story-executor", args: "{id}")
    Read Stage 2 coordinator artifact -> Bash: node $PIPELINE record-stage-summary --story {id} --payload '{...}'
    ASSERT artifact story_status = To Review
    Re-read kanban only as secondary assertion
    IF ASSERT fails: Bash: node $PIPELINE pause --story {id} --reason "Stage 2 artifact missing or invalid"; ESCALATE; BREAK
    git_stats = parse `git diff --stat origin/{base_branch}..HEAD`
    Write stage notes: .hex-skills/pipeline/stage_2_notes_{id}.md (Key Decisions, Git commits)
    Bash: node $PIPELINE checkpoint --story {id} --stage 2 --tasks-completed '{JSON done}' --git-stats '{JSON stats}' --last-action "Implementation complete"

  # STAGE 3: Quality Gate (IMPOSSIBLE TO SKIP — next line after Stage 2)
  Bash: node $PIPELINE advance --story {id} --to STAGE_3
  Skill(skill: "ln-500-story-quality-gate", args: "{id}")
  Read Stage 3 coordinator artifact -> Bash: node $PIPELINE record-stage-summary --story {id} --payload '{...}'
  Extract quality verdict, score, agents_info from Stage 3 artifact
  Re-read kanban only as secondary assertion
  Write stage notes: .hex-skills/pipeline/stage_3_notes_{id}.md (Verdict, Score, Agent Review, Branch)
  Bash: node $PIPELINE checkpoint --story {id} --stage 3 --verdict {verdict} --quality-score {score} --agents-info "{agents}" --last-action "Quality gate: {verdict}"

  IF Story status = Done:
    Bash: node $PIPELINE advance --story {id} --to DONE
    BREAK

  IF Story status = To Rework:
    Bash: node $PIPELINE advance --story {id} --to STAGE_2    # guard auto-increments quality_cycles
    IF advance fails (quality_cycles >= 2):
      Bash: node $PIPELINE pause --story {id} --reason "Quality gate failed 2 times"
      ESCALATE: "Quality gate failed after max cycles. Manual review needed."
      BREAK
    target_stage = 2    # loop back to Stage 2
    CONTINUE

  Bash: node $PIPELINE pause --story {id} --reason "Unexpected Stage 3 outcome"
  ESCALATE: "Story ended Stage 3 in unexpected status. Manual review needed."
  BREAK

### Stop Conditions (Quality Cycle)

| Condition | Action |
|-----------|--------|
| All tasks Done + Story = Done | STOP — Story completed successfully |
| `quality_cycles >= 2` | STOP — ESCALATE: "Quality gate failed after max cycles. Manual review needed." |
| Validation retry fails (NO-GO after retry) | STOP — ESCALATE: ask user for direction |
| Stage 2 precondition fails | STOP — ESCALATE: "Stage 2 incomplete, manual intervention needed" |

### Phase 5: Cleanup & Report

```
# 0. Signal pipeline complete
pre_cleanup_status = Bash: node $PIPELINE status --story {id}
IF pre_cleanup_status.state.phase != "DONE":
  Bash: node $PIPELINE advance --story {id} --to DONE

# 1. Self-verify against Definition of Done
status = Bash: node $PIPELINE status --story {id}
final_state = status.state.phase OR "DONE"
verification = {
  story_selected:   status.state.story_id == id
  story_processed:  final_state IN ("DONE", "PAUSED")
}
IF ANY verification == false: WARN user with details

# 2. Read stage notes
stage_notes = {}
FOR N IN 0..3:
  IF .hex-skills/pipeline/stage_{N}_notes_{id}.md exists:
    stage_notes[N] = read file content
  ELSE:
    stage_notes[N] = "(no notes captured)"

# 3. Extract branch info
branch_name = git branch --show-current
git_stats_final = git diff --stat origin/{base_branch}..HEAD (if not already captured)

# 4. Finalize pipeline report
durations = {N: stage_timestamps.stage_{N}_end - stage_timestamps.stage_{N}_start
             FOR N IN 0..3 IF both timestamps exist}

Write docs/tasks/reports/pipeline-{date}.md:

  # Pipeline Report -- {date}

  **Story:** {id} -- {title}
  **Branch:** {branch_name}
  **Final State:** {final_state}
  **Duration:** {now() - pipeline_start_time}

  ## Task Planning (ln-300)
  | Tasks | Plan Score | Duration |
  |-------|-----------|----------|
  | {N} created | {score}/4 | {durations[0]} |

  {stage_notes[0]}

  ## Validation (ln-310)
  | Verdict | Readiness | Agent Review | Duration |
  |---------|-----------|-------------|----------|
  | {verdict} | {score}/10 | {agents_info} | {durations[1]} |

  {stage_notes[1]}

  ## Implementation (ln-400)
  | Status | Files | Lines | Duration |
  |--------|-------|-------|----------|
  | {result} | {files_changed} | +{added}/-{deleted} | {durations[2]} |

  {stage_notes[2]}

  ## Quality Gate (ln-500)
  | Verdict | Score | Agent Review | Rework | Duration |
  |---------|-------|-------------|--------|----------|
  | {verdict} | {score}/100 | {agents_info} | {quality_cycles} | {durations[3]} |

  {stage_notes[3]}

  ## Pipeline Metrics
  | Wall-clock | Rework cycles | Validation retries |
  |------------|--------------|-------------------|
  | {total_duration} | {quality_cycles} | {validation_retries} |

# 5. Show pipeline summary to user
Pipeline Complete:
| Story | Branch | Planning | Validation | Implementation | Quality Gate | State |
|-------|--------|----------|------------|----------------|-------------|-------|
| {id} | {branch} | {stage0} | {stage1} | {stage2} | {stage3} | {final_state} |

Report saved: docs/tasks/reports/pipeline-{date}.md

# 6. Worktree cleanup
cd {project_root}
IF final_state == "PAUSED" AND worktree_dir exists AND worktree_dir != project_root:
  git -C {worktree_dir} add -A
  git -C {worktree_dir} commit -m "WIP: {id} pipeline paused" --allow-empty
  git -C {worktree_dir} push -u origin {branch}
  git worktree remove {worktree_dir} --force
  Display: "Partial work saved to branch {branch} (remote). Worktree cleaned."
IF final_state == "DONE" AND worktree_dir exists AND worktree_dir != project_root:
  # ln-500 committed + pushed in Phase 7. Clean worktree only.
  git worktree remove {worktree_dir} --force

# 7. Stop sleep prevention (Windows)
IF sleep_prevention_pid:
  kill $sleep_prevention_pid 2>/dev/null || true

# 8. Remove pipeline state files
Delete .hex-skills/pipeline/ directory

# 9. Report results location to user
```

## Coordinator Artifacts as Orchestration Truth

- **Read coordinator artifact first** after each stage completion. Never treat prose output as completion truth
- Re-read board after each stage only as a secondary assertion for expected status transitions
- Coordinators (ln-300/310/400/500) update Linear/kanban via their own logic. Lead verifies the artifact first, then checks board consistency
- **Update algorithm:** Follow `shared/references/kanban_update_algorithm.md` for Epic grouping and indentation

## Error Handling

| Situation | Detection | Action |
|-----------|----------|--------|
| ln-300 task creation fails | Skill returns error | Escalate to user: "Cannot create tasks for Story {id}" |
| ln-310 NO-GO (Score <5) | Stage 1 artifact verdict != GO | Retry once. If still NO-GO -> ask user |
| Task in To Rework 3+ times | ln-400 reports rework loop | Escalate: "Task X reworked 3 times, need input" |
| ln-500 FAIL | Stage 3 artifact verdict = FAIL | Fix tasks auto-created by ln-500. Stage 2 re-entry. Max 2 quality cycles |
| Skill call error | Exception from Skill() | `node $PIPELINE status` -> re-invoke same Skill (runtime + artifacts handle resume) |
| Context compression | PostCompact hook or manual detection | `node $PIPELINE status` -> extract resume_action -> continue |

## Worker Invocation (MANDATORY)

| Stage | Skill | Invocation |
|-------|-------|------------|
| 0 | ln-300-task-coordinator | `Skill(skill: "ln-300-task-coordinator", args: "{id}")` |
| 1 | ln-310-multi-agent-validator | `Skill(skill: "ln-310-multi-agent-validator", args: "{id}")` |
| 2 | ln-400-story-executor | `Skill(skill: "ln-400-story-executor", args: "{id}")` |
| 3 | ln-500-story-quality-gate | `Skill(skill: "ln-500-story-quality-gate", args: "{id}")` |

## TodoWrite format (mandatory)

```text
- Phase 1: Resolve Story and business context (pending)
- Phase 2: Ask targeted business questions only if needed (pending)
- Phase 3: Setup pipeline runtime and worktree state (pending)
- Phase 4: Execute stage 0 -> 3 sequentially with ASSERT guards (pending)
- Phase 5: Write report, clean worktree, and finalize runtime state (pending)
- Phase 6: Run pipeline meta-analysis (pending)
```

TodoWrite format (mandatory):
```
{content: "Stage N: {name} (ln-NNN)", status: "pending", activeForm: "{verb}ing"}
```

## Critical Rules

1. **Single Story processing.** User selects which Story to process
2. **Coordinators via Skill.** Lead invokes ln-300/ln-310/ln-400/ln-500 via Skill tool. Each coordinator manages its own internal worker dispatch (Agent/Skill)
3. **Skills as-is.** Never modify or bypass existing skill logic
4. **Artifact-first verification.** After EVERY Skill call, read coordinator artifact first and re-read kanban only as secondary assertion. Lead never caches stage truth in chat state
5. **Quality cycle limit.** Max 2 quality FAILs per Story (original + 1 rework). After 2nd FAIL, escalate to user
6. **Worktree lifecycle.** ln-1000 creates worktree in Phase 3.4. Branch finalization (commit, push) by ln-500. Worktree cleanup by ln-1000 in Phase 5 (lead is in worktree, so ln-500 skips cleanup)
7. **Stage notes.** Lead writes `.hex-skills/pipeline/stage_N_notes_{id}.md` after each stage for Pipeline Report
8. **Checkpoints.** CLI scripts write run-scoped runtime state under `.hex-skills/pipeline/runtime/runs/{run_id}/` via `node $PIPELINE checkpoint` after each stage

## Known Issues

| Symptom | Likely Cause | Self-Recovery |
|---------|-------------|---------------|
| Lead outputs generic text after long run | Context compression destroyed state vars | `node $PIPELINE status` -> extract resume_action -> continue from there |
| ln-400 stuck on same task | Task in rework loop | ln-400 handles internally; escalates after 3 reworks |

## Anti-Patterns
- Skipping quality gate after execution (Stage 3 is the next line after Stage 2 -- impossible to skip)
- Treating kanban state as the primary completion signal instead of coordinator artifacts
- Running mypy/ruff/pytest directly instead of letting coordinators handle it
- Processing multiple stories without user selection
- Creating worktrees outside Phase 3.4 (coordinators self-detect feature/*)
- Modifying coordinator internal dispatch (ln-400's Agent/Skill pattern is correct as-is)

## Plan Mode Support

When invoked in Plan Mode, show available Stories and ask user which one to plan for:

1. Parse kanban board (Phase 1 steps 1-7)
2. Show available Stories table
3. AskUserQuestion: "Which story to plan for? Enter # or Story ID."
4. Execute Phase 2 (pre-flight questions) if business ambiguities found
5. Resolve `skill_repo_path` -- absolute path to skills repo root
6. Show execution plan for selected Story
7. Write plan to plan file (using format below), call ExitPlanMode

**Plan Output Format:**
```
## Pipeline Plan for {date}

> **BEFORE EXECUTING -- MANDATORY READ:** Load `{skill_repo_path}/ln-1000-pipeline-orchestrator/SKILL.md` (full file).
> After reading SKILL.md, start from Phase 3 (Pipeline Setup) using the context below.

**Story:** {ID}: {Title}
**Current Status:** {status}
**Target Stage:** {N} ({skill_name})
**Storage Mode:** {file|linear}
**Project Brief:** {name} ({tech})
**Business Answers:** {answers from Phase 2, or "none"}
**Skill Repo Path:** {skill_repo_path}

### Execution Sequence
1. Read full SKILL.md + references (Phase 3 prerequisites)
2. Setup worktree + initialize CLI-managed pipeline state (Phase 3)
3. Execute stages sequentially via Skill() calls (Phase 4)
4. Generate pipeline report (Phase 5)
5. Cleanup worktree + state files (Phase 5)
```

## Definition of Done (self-verified in Phase 5)

- [ ] User selected Story (`state.story_id` is set)
- [ ] Business questions resolved (stored OR skip)
- [ ] Story processed to terminal state (`state.phase IN ("DONE", "PAUSED")`)
- [ ] Per-stage ASSERT verifications passed (artifact first, kanban secondary)
- [ ] Stage notes written for each completed stage
- [ ] Pipeline report generated (file exists at `docs/tasks/reports/`)
- [ ] Pipeline summary shown to user
- [ ] Worktree cleaned up (Phase 5 step 6)
- [ ] Meta-Analysis run (Phase 6)

## Phase 6: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md` and `references/phases/phase6_meta_analysis.md`

Skill type: `execution-orchestrator`. Runs after Phase 5. Pipeline-specific implementation (recovery map, trend tracking, assumption audit, report format) in `phase6_meta_analysis.md`.

## Reference Files

### Phase 4-6 Procedures (Progressive Disclosure)
- **Pipeline flow:** `references/phases/phase4_flow.md` (ASSERT guards, stage notes, context recovery, error handling)
- **Meta-analysis:** `references/phases/phase6_meta_analysis.md` (Recovery map, trend tracking, report format)

### Core Infrastructure
- **MANDATORY READ:** `shared/references/git_worktree_fallback.md`
- **MANDATORY READ:** `shared/references/research_tool_fallback.md`
- **Pipeline states:** `references/pipeline_states.md`
- **Checkpoint format:** `references/checkpoint_format.md`
- **Kanban parsing:** `references/kanban_parser.md`
- **Kanban update algorithm:** `shared/references/kanban_update_algorithm.md`
- **Settings template:** `references/settings_template.json`
- **Sleep prevention:** `references/hooks/prevent-sleep.ps1`
- **Environment state:** `shared/references/environment_state_contract.md`
- **Storage mode operations:** `shared/references/storage_mode_detection.md`
- **Auto-discovery patterns:** `shared/references/auto_discovery_pattern.md`

### Delegated Skills
- `../ln-300-task-coordinator/SKILL.md`
- `../ln-310-multi-agent-validator/SKILL.md`
- `../ln-400-story-executor/SKILL.md`
- `../ln-500-story-quality-gate/SKILL.md`

---
**Version:** 3.0.0
**Last Updated:** 2026-03-19
