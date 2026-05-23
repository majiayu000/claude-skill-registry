---
name: ln-400-story-executor
description: Orchestrates Story tasks. Prioritizes To Review -> To Rework -> Todo, delegates to ln-401/ln-403/ln-404, hands Story quality to ln-500. Metadata-only loading up front.
---

# Story Execution Orchestrator

Executes a Story end-to-end by looping through its tasks in priority order and delegating quality gates to ln-500-story-quality-gate.

## Purpose & Scope
- Load Story + task metadata (no descriptions) and drive execution.
- Process tasks in order: To Review -> To Rework -> Todo (foundation-first within each status).
- Delegate per task type: ln-402-task-reviewer (independent context for unbiased review), ln-403-task-rework, ln-401-task-executor, ln-404-test-executor.
- Delegate Story quality to ln-500-story-quality-gate (Pass 1/Pass 2) and loop if new tasks are created.

## Task Storage Mode

This skill supports dual-mode task storage:

| Aspect | Linear Mode | File Mode |
|--------|-------------|-----------|
| **Detection** | Default (MCP Linear available) | `docs/tasks/epics/` directory exists |
| **Load tasks** | `list_issues(parentId=Story.id)` | `Glob("docs/tasks/epics/*/stories/*/tasks/*.md")` + parse status |
| **Source of truth** | Linear API | Task files + kanban_board.md |

**Auto-detection:** Check if `docs/tasks/epics/` exists → File Mode, otherwise Linear Mode.

**File Mode status parsing:** Extract `**Status:** {value}` from `## Status` section in each task file.

**Status values:** Backlog, Todo, In Progress, To Review, To Rework, Done, Canceled

## When to Use
- Story is Todo or In Progress and has implementation/refactor/test tasks to finish.
- Need automated orchestration through To Review and quality gates.

## Plan Mode Support

When invoked in **Plan Mode** (agent cannot execute actions), this skill operates differently:

**Phase 1-2:** Same as normal mode (Discovery + Load metadata)

**Phase 3-4 (Plan Mode only):** Instead of executing, generate execution plan:

1) Build task execution sequence by priority (To Review → To Rework → Todo)
2) For each task, show:
   - Task ID, Title, current Status
   - Worker to be invoked (ln-401/ln-402/ln-403/ln-404)
   - Expected status after worker
3) Include Quality Gate phases (ln-500 Pass 1/Pass 2)
4) Write plan to plan file (if available)
5) Call ExitPlanMode for user approval

**Plan Output Format:**

```
## Execution Plan for Story {STORY-ID}: {Title}

### Tasks ({N} total)

| # | Task ID | Title | Status | Executor | Reviewer |
|---|---------|-------|--------|----------|----------|
| 1 | {ID} | {Title} | {Status} | ln-40X | ln-402 |

### Sequence

1. [Execute] {Task-1} via ln-401-task-executor
2. [Review] {Task-1} via ln-402-task-reviewer
...
N. [Quality Gate Pass 1] via ln-500-story-quality-gate
N+1. [Quality Gate Pass 2] → Story Done
```

**After approval:** User exits Plan Mode, invokes skill again → normal execution.

## Workflow (concise)
- **Phase 1 Discovery:** Auto-discover Team ID/config from kanban_board.md + CLAUDE.md. Check current git branch: if not `feature/{story-id}-{story-slug}`, create/switch to it.
- **Phase 2 Load:** Fetch Story metadata and all child task metadata (ID/title/status/labels only).
  - **Linear Mode:** `list_issues(parentId=Story.id)`
  - **File Mode:** `Glob("docs/tasks/epics/*/stories/{story-slug}/tasks/*.md")` + parse `**Status:**` from each file

  Summarize counts (e.g., "2 To Review, 1 To Rework, 3 Todo"). **NO analysis** — proceed immediately to Phase 3/4.

- **Phase 3 Context Review (before each Todo task execution):**
  Before delegating a Todo task to ln-401/ln-404, verify its plan against current codebase:

  1) **Load task description** (get_issue or Read task file)
  2) **Extract referenced files** from task plan (files to create/modify)
  3) **Check current state:**
     - Do referenced files still exist?
     - Have related files changed significantly since task creation?
     - Are patterns/approaches mentioned still valid in current code?
  4) **Decision:**
     - **No conflicts** → proceed to execution
     - **Minor changes** → update task description with current context, then execute
     - **Major conflicts** → flag task, ask user whether to replan or proceed

  **What to check:**
  - Files mentioned in "Files to modify" section
  - Import patterns and dependencies
  - Related tests and fixtures
  - API contracts if integrating with other components

  **Skip Context Review for:**
  - To Review tasks (already executed, just need review)
  - To Rework tasks (reviewer provided specific fixes)
  - Test tasks (ln-404) when implementation tasks are freshly Done
  - Tasks created in same session (< 24h ago)

- **Phase 4 Loop (immediate delegation via Skill tool, one task at a time):**
  1) To Review → **Use Skill tool to invoke `ln-402-task-reviewer`**. Reload metadata after worker.
  2) To Rework → **Use Skill tool to invoke `ln-403-task-rework`**. After worker, verify status = To Review, then **MANDATORY: immediately use Skill tool to invoke `ln-402-task-reviewer`** on that same task. Reload metadata.
  3) Todo → pick first Todo; if label "tests" **use Skill tool to invoke `ln-404-test-executor`** else **use Skill tool to invoke `ln-401-task-executor`**. After worker, verify status = To Review (not Done/In Progress), then **MANDATORY: immediately use Skill tool to invoke `ln-402-task-reviewer`** on that same task. Reload metadata. Repeat loop; never queue multiple tasks in To Review—review right after each execution/rework.

> **⚠️ STRICT RULE: Every task execution MUST be followed by review. NO EXCEPTIONS.**
> Execute → Review → Next task. Never skip review. Never batch reviews. Never proceed to next task without completing review of current task.

**TodoWrite format (mandatory):**
For each task, add BOTH steps to todos before starting execution:
1. `Execute [Task-ID]: [Title]` — mark in_progress when starting executor
2. `Review [Task-ID]: [Title]` — mark in_progress after executor completes, completed after ln-402

**Git branch management (mandatory):**
Before starting any task execution, ensure working in correct branch:
1. Get Story identifier from Linear (e.g., PROJ-42) and title
2. Generate branch name: `feature/{identifier}-{story-title-slug}`
   - story-title-slug: lowercase, spaces→dashes, remove special chars
3. Check current branch: `git branch --show-current`
4. If not matching:
   - Check if branch exists: `git branch --list "feature/{identifier}-*"`
   - If exists: `git checkout feature/{identifier}-{slug}`
   - If not: `git checkout -b feature/{identifier}-{slug}`
5. Confirm branch before proceeding to Phase 2

- **Phase 5 Quality Delegation:** Ensure all implementation tasks Done, then **use Skill tool to invoke `ln-500-story-quality-gate`** Pass 1. If it creates tasks (test/refactor/fix), return to Phase 4 to execute them. When test task is Done, set Story In Progress -> To Review and **use Skill tool to invoke `ln-500-story-quality-gate`** Pass 2. If Pass 2 fails and creates tasks, loop to Phase 4; if Pass 2 passes, Story goes To Review -> Done via ln-500.

## Critical Rules
- Branch isolation: all Story work MUST happen in `feature/{story-id}-{story-slug}` branch. Never commit directly to main/master.
- Metadata first: never load task descriptions in Phase 2; only workers load full text.
- No pre-analysis: after Phase 2 counts, pick ONE task by priority (To Review > To Rework > Todo) and delegate immediately. Do not plan, analyze, or reason about other tasks until they become next in queue.
- Single-task operations: each worker handles only the passed task ID; ln-400 never bulk-updates tasks.
- **Mandatory review after every task (ZERO COMPROMISE):** After ln-401/ln-403/ln-404, task MUST go to ln-402 review IMMEDIATELY. No batching, no skipping, no "I'll review later". Execute → Review → Next. Only ln-402 may set Done. Stop and report if any worker leaves task Done or In Progress.
- Source of truth: trust Linear metadata (Linear Mode) OR task files (File Mode) for orchestration decisions. Kanban_board.md is for navigation only.
- Story status ownership: ln-400 moves Todo -> In Progress (first execution) and In Progress -> To Review (all tasks Done); ln-500 handles To Review -> Done.
- Independent review context: ln-402 runs as subagent with isolated context. Orchestrator passes ONLY task ID—reviewer loads all context independently from Linear. This ensures unbiased "fresh eyes" review without executor's assumptions.

## Worker Invocation (MANDATORY)

> **CRITICAL:** All worker delegations MUST use Skill tool. DO NOT execute tasks directly or do manual reviews.

| Status | Worker to Invoke | How |
|--------|-----------------|-----|
| To Review | ln-402-task-reviewer | `Use Skill tool: ln-402-task-reviewer` |
| To Rework | ln-403-task-rework | `Use Skill tool: ln-403-task-rework` |
| Todo (tests) | ln-404-test-executor | `Use Skill tool: ln-404-test-executor` |
| Todo (impl) | ln-401-task-executor | `Use Skill tool: ln-401-task-executor` |
| Quality Gate | ln-500-story-quality-gate | `Use Skill tool: ln-500-story-quality-gate` |

**❌ FORBIDDEN SHORTCUTS (Anti-Patterns):**
- Running `mypy`/`ruff`/`pytest` directly instead of invoking ln-500/ln-501/ln-502
- Doing "minimal quality check" and asking "Want me to run the full skill?"
- Marking Quality Gate as "completed" in todo without actually invoking ln-500
- Any "self-service" execution that bypasses Skill tool invocation
- Partial workflow: "I ran linters, skipped manual testing" — NO, invoke full ln-500
- **Skipping review:** Executing multiple tasks before review — NO, every task gets reviewed IMMEDIATELY
- **Batching reviews:** "I'll review all tasks at the end" — NO, review after EACH task
- **Self-review bypass:** Marking task Done without ln-402 — NO, only ln-402 can set Done

**✅ CORRECT BEHAVIOR:**
- Use `Skill(skill: "ln-500-story-quality-gate")` — ALWAYS, NO EXCEPTIONS
- Wait for skill completion before proceeding
- Reload metadata after each skill invocation
- If skill creates tasks → return to Phase 4 loop

**ZERO TOLERANCE:** If you find yourself running commands (mypy, ruff, pytest) directly instead of invoking the appropriate skill, STOP immediately and use Skill tool instead.

### Independent Context Pattern (Architecture Decision)

Review delegation uses **isolated subagent context** for quality:

| Aspect | Implementation | Benefit |
|--------|---------------|---------|
| **Data passed** | Task ID only | No executor bias leaked |
| **Context loading** | ln-402 fetches from Linear | Fresh perspective |
| **Assumptions** | Reviewer has none | Catches implicit bugs |
| **Timing** | **IMMEDIATELY after execution** | No context drift, no forgotten issues |

**Analogy:** External code reviewer who wasn't involved in implementation—sees only the result, not the "journey".

**Why immediate review matters:**
- Fresh context = accurate review (delay = context loss)
- One task at a time = focused quality check
- No batching = no "rubber stamp" reviews
- Independent subagent = unbiased assessment every time

## Definition of Done
- Working in correct feature branch `feature/{story-id}-{story-slug}` (verified in Phase 1).
- Story metadata and task metadata loaded via list_issues (no get_issue in Phase 2); counts shown.
- Context Review (Phase 3) performed for each Todo task before execution (or skipped with justification for fresh tasks).
- Loop executed (Phase 4): all To Review via ln-402; all To Rework via ln-403 then immediate ln-402 on the same task; all Todo via ln-401/ln-404 then immediate ln-402 on the same task (validated To Review after each worker).
- If tasks were created by ln-500: executed through the loop.
- ln-500 Pass 1 invoked when impl tasks Done; Pass 2 invoked when test task Done or not needed. Result handled (pass/fail -> loop).
- Story status transitions applied (Todo -> In Progress -> To Review) and kanban updated by workers/ln-500.
- Final report with task counts and next step (if any).

## Reference Files
- Quality orchestration: `../ln-500-story-quality-gate/SKILL.md`
- Executors: `../ln-401-task-executor/SKILL.md`, `../ln-403-task-rework/SKILL.md`, `../ln-404-test-executor/SKILL.md`, `../ln-402-task-reviewer/SKILL.md`
- Auto-discovery: `CLAUDE.md`, `docs/tasks/kanban_board.md`

---
**Version:** 3.3.0 (Added Phase 3 Context Review to verify task plan against current codebase before execution)
**Last Updated:** 2026-01-15
