---
name: ln-400-story-executor
description: Orchestrates Story tasks. Prioritizes To Review -> To Rework -> Todo, delegates to ln-401/ln-402/ln-403/ln-404, hands Story quality to ln-500. Metadata-only loading up front.
---

# Story Execution Orchestrator

Executes a Story end-to-end by looping through its tasks in priority order and delegating quality gates to ln-500-story-quality-gate.

## Purpose & Scope
- Load Story + task metadata (no descriptions) and drive execution
- Process tasks in order: To Review → To Rework → Todo (foundation-first within each status)
- Delegate per task type to appropriate workers (see Worker Invocation table)
- **Mandatory immediate review:** Every execution/rework → ln-402 immediately. No batching

## Task Storage Mode

| Aspect | Linear Mode | File Mode |
|--------|-------------|-----------|
| **Detection** | Default (MCP Linear available) | `docs/tasks/epics/` directory exists |
| **Load tasks** | `list_issues(parentId=Story.id)` | `Glob("docs/tasks/epics/*/stories/*/tasks/*.md")` + parse status |
| **Source of truth** | Linear API | Task files + kanban_board.md |

**Auto-detection:** Check if `docs/tasks/epics/` exists → File Mode, otherwise Linear Mode.

**File Mode status values:** Backlog, Todo, In Progress, To Review, To Rework, Done, Canceled

## When to Use
- Story is Todo or In Progress and has implementation/refactor/test tasks to finish
- Need automated orchestration through To Review and quality gates

## Workflow

### Phase 1: Discovery & Branch Setup
1. Auto-discover Team ID/config from kanban_board.md + CLAUDE.md
2. Get Story identifier (e.g., PROJ-42) and title
3. Generate branch name: `feature/{identifier}-{story-title-slug}` (lowercase, spaces→dashes, no special chars)
4. Check current branch: `git branch --show-current`
5. If not matching:
   - If branch exists: `git checkout feature/{identifier}-{slug}`
   - If not: `git checkout -b feature/{identifier}-{slug}`

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
For each task by priority (To Review > To Rework > Todo):
1. Delegate to worker via Task tool (see Worker Invocation table)
2. Reload metadata after subagent completes
3. If worker sets status != To Review → STOP and report
4. **After ln-401/ln-403/ln-404:** Immediately invoke ln-402 on same task

> **Execute → Review → Next.** Never skip review. Never batch reviews.

### Phase 5: Quality Gate
When all implementation tasks Done:
1. Invoke ln-500-story-quality-gate Pass 1 via Task tool
2. If creates tasks → return to Phase 4
3. When test task Done → invoke Pass 2
4. If Pass 2 fails and creates tasks → return to Phase 4
5. If Pass 2 passes → Story Done

## Worker Invocation

> **CRITICAL:** All delegations use Task tool with subagent_type: "general-purpose" for context isolation.

| Status | Worker | Notes |
|--------|--------|-------|
| To Review | ln-402-task-reviewer | Pass task ID only. Add: "CRITICAL: Load ALL context independently via get_issue(). Fresh eyes review." |
| To Rework | ln-403-task-rework | Then immediate ln-402 on same task |
| Todo (tests) | ln-404-test-executor | Then immediate ln-402 on same task |
| Todo (impl) | ln-401-task-executor | Then immediate ln-402 on same task |
| Quality Gate | ln-500-story-quality-gate | "Pass 1" or "Pass 2" in prompt |

**Prompt template:**
```
Task(description: "[Action] task {ID}",
     prompt: "Execute {skill-name} for task {ID}. Read skill from {skill-name}/SKILL.md.",
     subagent_type: "general-purpose")
```

## Formats

### TodoWrite (mandatory)
Before each task, add BOTH steps:
1. `Execute [Task-ID]: [Title]` — mark in_progress when starting
2. `Review [Task-ID]: [Title]` — mark in_progress after executor, completed after ln-402

## Critical Rules
1. **Branch isolation:** All work in `feature/{story-id}-{slug}`. Never commit to main/master
2. **Metadata first:** Never load task descriptions in Phase 2; workers load full text
3. **One task at a time:** Pick → delegate → review → next. No bulk operations
4. **Only ln-402 sets Done:** Stop and report if any worker leaves task Done or In Progress
5. **Source of truth:** Trust Linear metadata (Linear Mode) or task files (File Mode)
6. **Story status:** ln-400 handles Todo→In Progress→To Review; ln-500 handles To Review→Done

## Anti-Patterns
- ❌ Running `mypy`/`ruff`/`pytest` directly instead of skill invocation
- ❌ "Minimal quality check" then asking "Want me to run full skill?"
- ❌ Skipping/batching reviews
- ❌ Self-setting Done status without ln-402
- ❌ Any execution bypassing Task tool subagent

**ZERO TOLERANCE:** If running commands directly instead of invoking skills via Task tool, STOP and correct.

## Plan Mode Support

When invoked in Plan Mode (agent cannot execute), generate execution plan instead:

1. Build task execution sequence by priority
2. For each task show: ID, Title, Status, Worker, expected status after
3. Include Quality Gate phases
4. Write plan to plan file, call ExitPlanMode

**Plan Output Format:**
```
## Execution Plan for Story {STORY-ID}: {Title}

| # | Task ID | Title | Status | Executor | Reviewer |
|---|---------|-------|--------|----------|----------|
| 1 | {ID} | {Title} | {Status} | ln-40X | ln-402 |

### Sequence
1. [Execute] {Task-1} via ln-401-task-executor
2. [Review] {Task-1} via ln-402-task-reviewer
...
N. [Quality Gate Pass 1/2] via ln-500-story-quality-gate
```

## Definition of Done
- Working in correct feature branch (verified in Phase 1)
- Story and task metadata loaded; counts shown
- Context Review performed for Todo tasks (or skipped with justification)
- Loop executed: all tasks delegated with immediate review after each
- ln-500 Pass 1/Pass 2 invoked; result handled
- Story status transitions applied; kanban updated by workers
- Final report with task counts

## Reference Files
- Quality orchestration: `../ln-500-story-quality-gate/SKILL.md`
- Executors: `../ln-401-task-executor/SKILL.md`, `../ln-403-task-rework/SKILL.md`, `../ln-404-test-executor/SKILL.md`
- Reviewer: `../ln-402-task-reviewer/SKILL.md`
- Auto-discovery: `CLAUDE.md`, `docs/tasks/kanban_board.md`

---
**Version:** 4.0.0 (Restructured: removed duplications, consolidated sections, ~35% reduction)
**Last Updated:** 2026-01-29
