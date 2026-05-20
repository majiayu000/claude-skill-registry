---
name: ln-400-story-executor
description: "Executes Story tasks in priority order (To Review, To Rework, Todo). Use when Story has planned tasks ready for implementation."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/{path}`.

# Story Execution Orchestrator

Executes a Story end-to-end by looping through its tasks in priority order. Sets Story to **To Review** when all tasks Done (quality gate decides Done).

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | Yes | args, git branch, kanban, user | Story to process |

**Resolution:** Story Resolution Chain.
**Status filter:** Todo, In Progress

## Purpose & Scope
- Load Story + task metadata (no descriptions) and drive execution
- Process tasks in order: To Review → To Rework → Todo (foundation-first within each status)
- Delegate per task type to appropriate workers (see Worker Invocation table)
- **Mandatory immediate review:** Every execution/rework → ln-402 immediately. No batching

## Task Storage Mode

**MANDATORY READ:** Load `shared/references/tools_config_guide.md`, `shared/references/storage_mode_detection.md`, and `shared/references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider (`linear` | `file`).

## When to Use
- Story is Todo or In Progress and has implementation/refactor/test tasks to finish
- Need automated orchestration through To Review

## Workflow

### Phase 1: Discovery & Worktree Setup

**MANDATORY READ:** Load `shared/references/git_worktree_fallback.md` — use "Story execution" row.

1. **Resolve storyId:** Run Story Resolution Chain per guide (status filter: [Todo, In Progress]).
2. Auto-discover Team ID/config from kanban_board.md + CLAUDE.md
3. Get Story title from resolved storyId
4. Generate branch name: `feature/{identifier}-{story-title-slug}` (lowercase, spaces→dashes, no special chars)
5. **Self-detection:** `git branch --show-current`
   - If already on `feature/*` → use current worktree, skip to Phase 2
   - If on develop/main/master → create worktree + branch (per git_worktree_fallback.md lifecycle steps 1-3, worktree dir: `.worktrees/story-{identifier}`)

### Phase 2: Load Metadata
Fetch Story metadata and all child task metadata (ID/title/status/labels only):
- **Linear Mode:** `list_issues(parentId=Story.id)`
- **File Mode:** `Glob("docs/tasks/epics/*/stories/{story-slug}/tasks/*.md")` + parse `**Status:**`

Summarize counts (e.g., "2 To Review, 1 To Rework, 3 Todo"). **NO analysis** — proceed immediately.

### Phase 3: Context Review (before Todo tasks)
Before delegating a Todo task, verify its plan against current codebase:
1. Load task description (get_issue or Read task file)
2. Extract referenced files from task plan
3. Check: Do files exist? Have related files changed? Are patterns still valid?
4. Decision: No conflicts → proceed | Minor changes → update task, proceed | Major conflicts → ask user

**Skip Context Review for:** To Review tasks, To Rework tasks, test tasks when impl freshly Done, tasks created <24h ago.

### Phase 4: Task Loop

**Priority order:** To Review > To Rework > Todo (foundation-first within each status).

**Group-based dispatch for Todo tasks:**

1. **Parse Parallel Groups:** Extract `**Parallel Group:** {N}` from each Todo task. Tasks without this field = each gets its own group (sequential, backward compatible).
2. **Process To Review / To Rework first** (always sequential, one at a time).
3. **For each Parallel Group** (ascending order):
   - **Single task in group:** Sequential execution (same as current behavior):
     1. Delegate to worker via Agent tool
     2. After executor completes → immediately invoke ln-402 on same task
     3. Reload metadata (task count may change — ln-402 creates [BUG] tasks)
   - **Multiple tasks in group:** Parallel execution via Agent tool subagents:
     1. Spawn all tasks in group concurrently (multiple Agent tool calls in single message)
     2. Wait for ALL subagents to complete
     3. Review each task sequentially via ln-402 (one at a time — review cannot be parallelized)
     4. Reload metadata after all reviews
4. If any worker sets status != To Review → STOP and report.

> **Execute → Review → Next.** Never skip review. Reviews are always sequential (ln-402 inline).

### Stop Conditions (Task Loop)

| Condition | Action |
|-----------|--------|
| All tasks status = Done | STOP — proceed to Phase 5 (Completion) |
| Same task in To Rework 3+ consecutive times | STOP — ESCALATE: "Task rework loop detected, need input" |
| No tasks in processable status (To Review / To Rework / Todo) | STOP — proceed to Phase 5 |

### Phase 5: Completion
When all tasks Done:
1. **Set Story status to To Review** (Linear: `update_issue(id, state: "To Review")`; File: `Edit` the `**Status:**` line)
2. Update kanban: move Story to To Review section
3. Report final status with task counts
- **⚠️ NEVER set Story to Done.** Only the quality gate (5XX) can mark Story as Done after full quality check.
- **Recommended next step:** quality gate for code quality and regression checks

## Worker Invocation

> **CRITICAL:** Executors (ln-401/ln-403/ln-404) use Agent tool for context isolation. Reviewer (ln-402) runs inline via Skill tool in main flow.

| Status | Worker | Notes |
|--------|--------|-------|
| To Review | ln-402-task-reviewer | **Inline (Skill tool).** Load task by ID, review in main flow. No subagent. |
| To Rework | ln-403-task-rework | Then immediate ln-402 on same task |
| Todo (tests) | ln-404-test-executor | Then immediate ln-402 on same task |
| Todo (impl) | ln-401-task-executor | Then immediate ln-402 on same task |
**Prompt templates:**

Executors (ln-401/ln-403/ln-404) — Agent tool (isolated context):
```
Agent(description: "[Action] task {ID}",
     prompt: "Execute task {ID}.

Step 1: Invoke worker:
  Skill(skill: \"{skill-name}\")

CONTEXT:
Task ID: {ID}",
     subagent_type: "general-purpose")
```

Reviewer (ln-402) — Skill tool (main flow):
```
Skill(skill: "ln-402-task-reviewer", args: "{task-ID}")
```

## Formats

### TodoWrite (mandatory)
Before each task, add BOTH steps:
1. `Execute [Task-ID]: [Title]` — mark in_progress when starting
2. `Review [Task-ID]: [Title]` — mark in_progress after executor, completed after ln-402

## Critical Rules
1. **Worktree isolation:** All work in isolated worktree on `feature/{story-id}-{slug}`. Never modify main worktree
2. **Metadata first:** Never load task descriptions in Phase 2; workers load full text
3. **One task at a time:** Pick → delegate → review → next. No bulk operations
4. **Only ln-402 sets Done:** Stop and report if any worker leaves task Done or In Progress
5. **Source of truth:** Trust Linear metadata (Linear Mode) or task files (File Mode)
6. **Story status:** ln-400 handles Todo→In Progress→**To Review**. NEVER set Story to Done — only the quality gate (5XX) can do that after full quality check
7. **Commit policy:** Only ln-402 commits code. Workers (ln-401/ln-403/ln-404) leave changes uncommitted for ln-402 to review and commit.
8. **[BUG] tasks:** ln-402 may create new [BUG] tasks mid-review. After metadata reload, reprioritize — new tasks processed in next loop iteration.
9. **Parallel groups:** Tasks in same group execute concurrently via Agent tool subagents. Reviews (ln-402) remain sequential. If `**Parallel Group:**` missing on any task, fall back to fully sequential execution.

## Anti-Patterns
- ❌ Running `mypy`/`ruff`/`pytest` directly instead of skill invocation
- ❌ "Minimal quality check" then asking "Want me to run full skill?"
- ❌ Skipping/batching reviews
- ❌ Self-setting Done status without ln-402
- ❌ Executors bypassing Agent tool subagent (ln-402 is exception — runs inline)

**ZERO TOLERANCE:** If running commands directly instead of invoking skills, STOP and correct.

## Plan Mode Support

When invoked in Plan Mode (agent cannot execute), generate execution plan instead:

1. Build task execution sequence by priority
2. For each task show: ID, Title, Status, Worker, expected status after
3. Write plan to plan file, call ExitPlanMode

**Plan Output Format:**
```
## Execution Plan for Story {STORY-ID}: {Title}

| # | Task ID | Title | Status | Group | Executor | Reviewer |
|---|---------|-------|--------|-------|----------|----------|
| 1 | {ID} | {Title} | {Status} | {N} | ln-40X | ln-402 |

### Sequence
1. [Execute] {Task-1} via ln-401-task-executor
2. [Review] {Task-1} via ln-402-task-reviewer
...
```

## Definition of Done
- [ ] Working in correct feature branch (verified in Phase 1)
- [ ] Story and task metadata loaded; counts shown
- [ ] Context Review performed for Todo tasks (or skipped with justification)
- [ ] Loop executed: all tasks delegated with immediate review after each
- [ ] Story set to **To Review** (NOT Done); kanban updated
- [ ] Final report with task counts and recommended next step: quality gate

## Phase 6: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `execution-orchestrator`. Run after all phases complete. Output to chat using the `execution-orchestrator` format.

## Reference Files
- **Tools config:** `shared/references/tools_config_guide.md`
- **Storage mode operations:** `shared/references/storage_mode_detection.md`
- **Orchestrator lifecycle:** `shared/references/orchestrator_pattern.md`
- **Task delegation pattern:** `shared/references/task_delegation_pattern.md`
- **Auto-discovery patterns:** `shared/references/auto_discovery_pattern.md`
- **Plan mode behavior:** `shared/references/plan_mode_pattern.md`
- **MANDATORY READ:** `shared/references/git_worktree_fallback.md`
- Executors: `../ln-401-task-executor/SKILL.md`, `../ln-403-task-rework/SKILL.md`, `../ln-404-test-executor/SKILL.md`
- Reviewer: `../ln-402-task-reviewer/SKILL.md`
- Auto-discovery: `CLAUDE.md`, `docs/tasks/kanban_board.md`

---
**Version:** 4.0.0
**Last Updated:** 2026-01-29
