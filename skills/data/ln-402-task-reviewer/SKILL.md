---
name: ln-402-task-reviewer
description: L3 Worker. Reviews task implementation for quality, code standards, test coverage. Creates [BUG] tasks for side-effect issues found outside task scope. Sets task Done or To Rework. Usually invoked by ln-400 with isolated context, can also review a specific task on user request.
---

# Task Reviewer

**MANDATORY after every task execution.** Reviews a single task in To Review and decides Done vs To Rework with immediate fixes or clear rework notes.

> **This skill is NOT optional.** Every task executed by ln-401/ln-403/ln-404 MUST be reviewed by ln-402 immediately. No exceptions, no batching, no skipping.

## Purpose & Scope
- **Independent context loading:** Receive only task ID from orchestrator; load full task and parent Story independently (Linear: get_issue; File: Read task file). This isolation ensures unbiased review without executor's assumptions (fresh eyes pattern).
- Check architecture, correctness, configuration hygiene, docs, and tests.
- For test tasks, verify risk-based limits and priority (≤15) per planner template.
- Update only this task: accept (Done) or send back (To Rework) with explicit reasons and fix suggestions tied to best practices.

## Task Storage Mode

| Aspect | Linear Mode | File Mode |
|--------|-------------|-----------|
| **Load task** | `get_issue(task_id)` | `Read("docs/tasks/epics/.../tasks/T{NNN}-*.md")` |
| **Load Story** | `get_issue(parent_id)` | `Read("docs/tasks/epics/.../story.md")` |
| **Update status** | `update_issue(id, state: "Done"/"To Rework")` | `Edit` the `**Status:**` line in file |
| **Add comment** | Linear comment API | Append to task file or kanban |

**File Mode status values:** Done, To Rework (only these two outcomes from review)

## Workflow (concise)
1) **Receive task (isolated context):** Get task ID from orchestrator (ln-400)—NO other context passed. Load all information independently from Linear. Detect type (label "tests" -> test task, else implementation/refactor).
2) **Read context:** Full task + parent Story; load affected components/docs; review diffs if available.
3) **Review checks:**
   - Approach matches Technical Approach or better (documented rationale).
   - No hardcoded creds/URLs/magic numbers; config in env/config.
   - Error handling sane; layering respected; reuse existing components.
   - Logging: critical paths logged (errors, business events); correct log levels (DEBUG/INFO/WARNING/ERROR).
   - Comments: explain WHY not WHAT; no commented-out code; docstrings on public methods; Task ID present in new code blocks (`// See PROJ-123`).
   - Naming: consistent conventions; descriptive names; no single-letter variables (except loops).
   - Docs updated where required.
   - Tests updated/run: for impl/refactor ensure affected tests adjusted; for test tasks verify risk-based limits and priority (≤15) per planner template.
4) **AC Validation (MANDATORY for implementation tasks):**
   Load parent Story AC and verify implementation against 4 criteria (see `references/ac_validation_checklist.md`):
   - **AC Completeness:** All AC scenarios covered (happy path + errors + edge cases).
   - **AC Specificity:** Exact requirements met (HTTP codes 200/401/403, timing <200ms, exact messages).
   - **Task Dependencies:** Task N uses ONLY Tasks 1 to N-1 (no forward dependencies on N+1, N+2).
   - **Database Creation:** Task creates ONLY tables in Story scope (no big-bang schema).
   If ANY criterion fails → To Rework with specific guidance from checklist.
5) **Side-Effect Bug Detection (MANDATORY):**
   While reviewing affected code, actively scan for bugs/issues NOT related to current task:
   - Pre-existing bugs in touched files
   - Broken patterns in adjacent code
   - Security issues in related components
   - Deprecated APIs, outdated dependencies
   - Missing error handling in caller/callee functions

   **For each side-effect bug found:**
   - Create new task in same Story (Linear: create_issue with parentId=Story.id; File: create task file)
   - Title: `[BUG] {Short description}`
   - Description: Location, issue, suggested fix
   - Label: `bug`, `discovered-in-review`
   - Priority: based on severity (security=1 Urgent, logic=2 High, style=4 Low)
   - **Do NOT defer** — create task immediately, reviewer catches what executor missed

6) **Decision (for current task only):**
   - If only nits: apply minor fixes and set Done.
   - If issues remain: set To Rework with comment explaining why (best-practice ref) and how to fix.
   - Side-effect bugs do NOT block current task's Done status (they are separate tasks).
7) **Update:** Set task status in Linear; update kanban: if Done → **remove task from kanban** (Done section tracks Stories only, not individual Tasks); if To Rework → move task to To Rework section; add review comment with findings/actions. If side-effect bugs created, mention them in comment.

## Critical Rules
- One task reviewed at a time; side-effect bugs become separate tasks.
- Zero tolerance: no deferring issues; either fix now or send back with guidance.
- **Side-effect bugs: fix ALL issues found, not just task scope.** Reviewer's fresh eyes catch what executor missed. Create tasks for every bug found, regardless of whether it's "in scope". This is a feature, not scope creep.
- Keep language of the task (EN/RU) in comments/edits.
- If test-task limits/priority violated -> To Rework with guidance.
- Never leave task Done if any unresolved issue exists **in that task's scope**.
- **Kanban Done section:** Contains Stories only, NOT Tasks. When Task → Done, remove it from kanban entirely.
- **Independent review isolation:** This skill runs as subagent with fresh context. Do NOT rely on any data from orchestrator except task ID. Load everything from Linear to maintain objectivity. This emulates external code review by developer who wasn't involved in implementation.
- **Mandatory invocation (ZERO COMPROMISE):** This skill MUST be invoked after EVERY task execution. No task can be marked Done without passing through ln-402 review. Orchestrator (ln-400) enforces this—if you're running standalone, enforce it yourself.

## Definition of Done
- Task and parent Story fully read; type identified.
- Review checklist completed; docs/tests/config verified.
- **Side-effect bugs scanned:** Any bugs found outside task scope → created as new tasks with `[BUG]` prefix.
- Decision applied: Done (minor fixes applied) or To Rework (issues + fix guidance).
- Linear status updated; kanban updated (if Done → task removed from kanban; if To Rework → task moved to To Rework section); review comment posted (including list of any side-effect bug tasks created).

## Reference Files
- AC Validation Checklist: `references/ac_validation_checklist.md` (criteria #4, #9, #17, #19 from ln-310)
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 4.0.0 (BREAKING: Added AC Validation step 4 with 4 criteria from ln-310 - AC completeness/specificity, Task dependencies, Database Creation Principle. Closes validation-execution gap per BMAD Method best practices.)
**Last Updated:** 2026-02-03
