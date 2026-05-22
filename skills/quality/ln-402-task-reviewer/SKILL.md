---
name: ln-402-task-reviewer
description: Reviews completed tasks (To Review) and moves them to Done or To Rework. Zero tolerance: all issues fixed now.
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
4) **Decision:**  
   - If only nits: apply minor fixes and set Done.  
   - If issues remain: set To Rework with comment explaining why (best-practice ref) and how to fix.
5) **Update:** Set task status in Linear; update kanban: if Done → **remove task from kanban** (Done section tracks Stories only, not individual Tasks); if To Rework → move task to To Rework section; add review comment with findings/actions.

## Critical Rules
- One task at a time; do not touch others.
- Zero tolerance: no deferring issues; either fix now or send back with guidance.
- Keep language of the task (EN/RU) in comments/edits.
- If test-task limits/priority violated -> To Rework with guidance.
- Never leave task Done if any unresolved issue exists.
- **Kanban Done section:** Contains Stories only, NOT Tasks. When Task → Done, remove it from kanban entirely.
- **Independent review isolation:** This skill runs as subagent with fresh context. Do NOT rely on any data from orchestrator except task ID. Load everything from Linear to maintain objectivity. This emulates external code review by developer who wasn't involved in implementation.
- **Mandatory invocation (ZERO COMPROMISE):** This skill MUST be invoked after EVERY task execution. No task can be marked Done without passing through ln-402 review. Orchestrator (ln-400) enforces this—if you're running standalone, enforce it yourself.

## Definition of Done
- Task and parent Story fully read; type identified.
- Review checklist completed; docs/tests/config verified.
- Decision applied: Done (minor fixes applied) or To Rework (issues + fix guidance).
- Linear status updated; kanban updated (if Done → task removed from kanban; if To Rework → task moved to To Rework section); review comment posted.

## Reference Files
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
