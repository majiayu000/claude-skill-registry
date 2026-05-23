---
name: plan-directory
description: >
  Create or update a structured plan directory with a master PLAN.md index and
  numbered task files (001-*.md). Each task file includes goal, dependencies,
  scope, checklist, tests, and completion criteria. Use when scaffolding a
  repeatable project plan in markdown, especially when the user wants a master
  index plus per-task files with checkboxes that are checked off as work
  completes.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
---

# Plan Directory Skill

## When to Use This Skill

- Scaffolding a new project, feature, or migration that benefits from a
  structured, step-by-step plan.
- Creating a repeatable plan that an LLM or engineer can execute with
  explicit, verifiable checkboxes.
- Maintaining an existing plan directory: adding tasks, updating progress,
  or archiving completed plans.
- When the user says "create a plan", "scaffold a plan", "plan this feature",
  or similar intent implying structured task breakdown.

Do **not** use this skill for ad-hoc todo lists, single-file notes, or when
the user explicitly wants a different format.

## LLM Intake (Required Inputs)

Before writing any files, gather these inputs. If any are missing, **ask**
the user for them explicitly.

| Input | Required | Description |
|-------|----------|-------------|
| Plan title | Yes | Human-readable name (e.g., "User Authentication Overhaul") |
| Plan slug | Yes | Hyphenated directory/file slug (e.g., `user-auth-overhaul`) |
| Target location | No | Directory path; defaults to `docs/plans/<slug>/` or `plans/<slug>/` |
| Task list | Yes | List of tasks with short names and scopes |
| Locked decisions | No | Key constraints or choices that must not change |
| Testing expectations | No | Commands, subsets, or manual QA requirements |

When updating an existing plan, read the current `PLAN.md` first to understand
context before modifying.

## Invariants (Do Not Violate)

1. **PLAN.md is the index, not the content.** It contains only the purpose,
   usage instructions, locked decisions, and a task index with checkboxes.
   Detailed steps live in individual task files.

2. **Task files use 3-digit numbering.** Format: `NNN-<slug>.md` where `NNN`
   is zero-padded (001, 002, ..., 999) and `<slug>` is hyphenated lowercase.

3. **Every task file has six sections.** Goal, Scope, Checklist, Tests,
   Completion Criteria, and Dependencies. All are required (use "None" for
   Dependencies if truly independent, "N/A" for Tests only with justification).

4. **Checkboxes are the only status markers.** Do not add "Status: Done"
   fields, emoji indicators, or separate progress sections. Check `- [x]`
   when complete, leave `- [ ]` when pending.

5. **Mirror completion in PLAN.md.** When all checklist items in a task file
   are checked, check the corresponding task in PLAN.md.

6. **Do not renumber existing tasks.** Once a task number is assigned and
   work has started, it is permanent. Append new tasks at the end.

7. **Keep task files self-contained.** A reader should understand the task
   from the file alone without reading other task files.

8. **Track blockers explicitly.** When a task is blocked, add a `## Blockers`
   section describing what's blocking and link to the blocking task or issue.

## Workflow

### 1. Determine Mode: Create or Update

- **Create:** No plan directory exists. Scaffold everything from scratch.
- **Update:** `PLAN.md` already exists. Read it, understand the current
  state, and make targeted modifications.

### 2. Validate Inputs

- Confirm all required inputs are present.
- If the user provides a vague task list, ask for clarification before
  proceeding.
- For updates, verify the plan slug and location match the existing plan.

### 3. Create or Update the Plan Directory

**For new plans:**
1. Create the directory at the target location.
2. Write `PLAN.md` with the master index.
3. Write each task file (`001-*.md`, `002-*.md`, etc.).

**For updates:**
1. Read the existing `PLAN.md` and relevant task files.
2. Apply changes: add new tasks, update checklists, check completed items.
3. Ensure PLAN.md index stays in sync with task files.

### 4. Fill PLAN.md (Master Index)

Keep it minimal. Include only:
- **Purpose:** 1-3 bullets on why the plan exists.
- **How to use:** Brief instructions for working the plan.
- **Decisions (locked):** Key constraints that should not change.
- **Task Index:** Checkbox list linking to task files.
- **Completion:** Definition of when the entire plan is done.

### 5. Fill Task Files

Each task file must include:
- **Goal:** Single sentence describing the outcome.
- **Dependencies:** List of task numbers that must complete first, or "None".
- **Scope:** Bulleted list of what's in scope (and optionally out of scope).
- **Checklist:** 3-8 concrete, actionable steps with checkboxes.
- **Tests:** Specific test commands, files, or manual QA steps.
- **Completion Criteria:** Measurable definitions of done.
- **Notes (optional):** Constraints, references, warnings.
- **Blockers (optional):** Added when work is blocked; removed when unblocked.

### 6. Maintain Progress

As work completes:
1. Check items in the task file's Checklist and Tests sections.
2. When all items are checked, check the Completion Criteria items.
3. Check the corresponding task in PLAN.md's Task Index.

## Task Sizing Rules

- **Target 3-8 checklist items per task.** This keeps tasks focused and
  completable in a reasonable session.
- **Split if exceeding 10 items.** If a task grows beyond ~10 checklist
  items, break it into subtasks.
- **Tests must be explicit.** Include runnable commands or specific file
  paths. Avoid vague "test that it works" items.
- **Completion criteria must be measurable.** Use "X is true" or "Y passes"
  rather than narrative descriptions.

## Update Rules (Existing Plans)

| Scenario | Rule |
|----------|------|
| Adding tasks | Append at the end with the next number |
| Removing tasks | Mark as "[REMOVED]" in PLAN.md; delete file only if user requests |
| Renaming tasks | Update both the task file and PLAN.md index entry |
| Reordering tasks | Do not renumber; use dependencies or notes to indicate order changes |
| Splitting tasks | Create new task files; mark original as "[SPLIT]" pointing to new tasks |

## Templates

### PLAN.md

```markdown
# <Plan Title> - Master Plan

## Purpose

- <Why this plan exists>
- <What it delivers when complete>

## How to Use

1. Work tasks in order unless dependencies indicate otherwise.
2. Check items in task files as they are completed.
3. This file is the index only; details live in task files.

## Decisions (Locked)

- <Key constraint or choice that should not change>
- <Another locked decision>

## Task Index

- [ ] 001 - <Task Name> (`001-<slug>.md`)
- [ ] 002 - <Task Name> (`002-<slug>.md`)
- [ ] 003 - <Task Name> (`003-<slug>.md`)

## Completion

- [ ] All tasks in the index are checked.
- [ ] All tests listed in task files pass.
- [ ] <Any additional project-specific completion criteria>
```

### Task File (NNN-<slug>.md)

```markdown
# NNN - <Task Name>

## Goal

<Single sentence describing the outcome of this task.>

## Dependencies

- Requires: 001, 002 (or "None" if independent)
- Blocks: 004, 005 (tasks waiting on this one)

## Scope

**In scope:**
- <What this task covers>
- <Another in-scope item>

**Out of scope:**
- <What this task explicitly does not cover>

## Checklist

- [ ] <Concrete implementation step with verifiable outcome>
- [ ] <Another concrete step>
- [ ] <Another concrete step>

## Tests

- [ ] Run `<test command>` and verify all pass
- [ ] Manual QA: <specific verification step>

## Completion Criteria

- [ ] <Measurable definition of done>
- [ ] <Another measurable definition>

## Notes

- <Optional: constraints, references, links, or warnings>
```

### Blocked Task (when work cannot proceed)

When a task is blocked, add a `## Blockers` section immediately after Dependencies:

```markdown
## Blockers

- **Blocked by:** External API not yet available (ETA: 2024-02-15)
- **Blocked by:** Waiting on 003 to complete first
- **Action needed:** Contact platform team for API access
```

Remove the Blockers section when the task is unblocked.

## Quality Checklist (LLM Preflight)

Before delivering a plan, verify:

- [ ] All required inputs were gathered or reasonable defaults applied.
- [ ] PLAN.md is short and contains only the index, not detailed steps.
- [ ] Task filenames match the pattern `NNN-<slug>.md` with 3-digit padding.
- [ ] Every task file has all six required sections (Goal, Dependencies,
      Scope, Checklist, Tests, Completion Criteria).
- [ ] Dependencies are explicitly stated (even if "None").
- [ ] Checklist items are concrete and verifiable, not vague.
- [ ] Tests section contains runnable commands or specific QA steps.
- [ ] Completion criteria are measurable, not narrative.
- [ ] PLAN.md Task Index matches the task files exactly.
- [ ] No task exceeds ~10 checklist items (split if needed).
- [ ] Dependency graph has no cycles (task A can't depend on B if B depends on A).
- [ ] Parallel-executable tasks are identified where applicable.

## Parallel Task Execution

Some tasks can run concurrently if they have no dependencies on each other.
Indicate this in PLAN.md using a parallel block notation:

```markdown
## Task Index

- [ ] 001 - Database setup (`001-db-setup.md`)
- [ ] 002 - Frontend scaffolding (`002-frontend-scaffold.md`) [parallel: 001]
- [ ] 003 - API design (`003-api-design.md`) [parallel: 001, 002]
- [ ] 004 - Integration (`004-integration.md`) [after: 001, 002, 003]
```

The `[parallel: NNN]` tag means "can run at the same time as task NNN".
The `[after: NNN]` tag means "must wait for NNN to complete".

When working a plan:
- Start all tasks marked parallel that have no unmet dependencies.
- Track progress on parallel tasks independently.
- Only start `[after: ...]` tasks when all listed dependencies are checked.

## Examples

### Example 1 - Creating a New Plan

**User prompt:**
> "Create a plan for adding user authentication to my app. Use JWT tokens,
> store users in PostgreSQL, and include password reset flow."

**Expected behavior:**
1. Ask for any missing inputs (e.g., preferred directory, additional tasks).
2. Create `docs/plans/user-auth/` (or user-specified location).
3. Write `PLAN.md` with the task index.
4. Write task files like:
   - `001-user-model.md` - Create User model and migrations
   - `002-jwt-setup.md` - Configure JWT authentication
   - `003-login-endpoint.md` - Implement login/logout endpoints
   - `004-password-reset.md` - Implement password reset flow
   - `005-integration-tests.md` - Write integration tests

**Output structure:**
```
docs/plans/user-auth/
  PLAN.md
  001-user-model.md
  002-jwt-setup.md
  003-login-endpoint.md
  004-password-reset.md
  005-integration-tests.md
```

### Example 2 - Updating an Existing Plan

**User prompt:**
> "Add a new task to the user-auth plan for implementing OAuth with Google."

**Expected behavior:**
1. Read the existing `PLAN.md` to understand current state.
2. Determine the next task number (e.g., 006).
3. Create `006-google-oauth.md` with the standard sections.
4. Append the new task to PLAN.md's Task Index.
5. Do not modify existing task files unless explicitly requested.

### Example 3 - Marking Progress

**User prompt:**
> "I've completed the JWT setup task in the user-auth plan."

**Expected behavior:**
1. Read `002-jwt-setup.md`.
2. Check all checklist items, tests, and completion criteria as done.
3. Update `PLAN.md` to check the `002 - JWT Setup` entry.
4. Confirm the update to the user.

### Example 4 - Complete Task File (Reference)

Here's a fully filled-out task file for reference:

```markdown
# 003 - Login Endpoint

## Goal

Implement JWT-based login and logout endpoints that authenticate users and
return tokens.

## Dependencies

- Requires: 001, 002
- Blocks: 004, 005

## Scope

**In scope:**
- POST /api/auth/login endpoint accepting email/password
- POST /api/auth/logout endpoint invalidating tokens
- Token refresh endpoint
- Rate limiting on login attempts

**Out of scope:**
- OAuth/social login (separate task 006)
- Password reset flow (task 004)
- User registration (task 001 handles this)

## Checklist

- [ ] Create LoginSerializer with email and password fields
- [ ] Implement login view returning access and refresh tokens
- [ ] Implement logout view that blacklists the refresh token
- [ ] Add rate limiting: max 5 failed attempts per 15 minutes
- [ ] Return appropriate error codes (401 for bad credentials, 429 for rate limit)
- [ ] Log authentication attempts with user ID and IP (no passwords)

## Tests

- [ ] Run `pytest apps/auth/tests/test_login.py -v` - all pass
- [ ] Run `pytest apps/auth/tests/test_logout.py -v` - all pass
- [ ] Manual QA: Verify login with valid credentials returns token
- [ ] Manual QA: Verify 5 failed attempts triggers rate limit

## Completion Criteria

- [ ] Login endpoint returns valid JWT on correct credentials
- [ ] Logout endpoint invalidates the refresh token
- [ ] Rate limiting activates after 5 failed attempts
- [ ] All automated tests pass
- [ ] No security warnings from `bandit` scan

## Notes

- Use `djangorestframework-simplejwt` for token handling
- Token expiry: access = 15 min, refresh = 7 days
- See RFC 6749 for OAuth2 token response format reference
```

## Anti-Patterns to Avoid

- **Putting task details in PLAN.md.** The master plan is an index only.
- **Using arbitrary numbering.** Always use 3-digit zero-padded numbers.
- **Vague checklist items.** "Set up database" is bad; "Create users table
  with email, password_hash, created_at columns" is good.
- **Missing tests.** Every task should have at least one test or explicit
  "N/A - no automated tests applicable" with justification.
- **Renumbering tasks mid-project.** This breaks references and history.
- **Narrative completion criteria.** "The feature works well" is bad;
  "Users can log in and receive a valid JWT token" is good.
- **Ignoring dependencies.** Always specify what tasks depend on each other
  to prevent wasted work on blocked tasks.
- **Overly large tasks.** Tasks with 15+ checklist items are hard to track;
  split them into focused subtasks.

## Plan Lifecycle

### When a Plan Completes

When all tasks are checked:

1. Verify the PLAN.md Completion section is fully checked.
2. Add a `## Completed` section at the top of PLAN.md with the date:
   ```markdown
   ## Completed

   **Date:** 2024-02-15
   **Duration:** 3 weeks
   **Notes:** All tasks completed successfully. OAuth added as follow-up plan.
   ```
3. Optionally move the plan directory to `docs/plans/archive/<slug>/` or
   add an `[ARCHIVED]` prefix to the directory name.

### Plan Retrospective (Optional)

For significant plans, add a `RETROSPECTIVE.md` in the plan directory:

```markdown
# <Plan Title> - Retrospective

## What Went Well
- <Positive outcomes and practices>

## What Could Be Improved
- <Issues encountered and lessons learned>

## Follow-up Actions
- <New tasks or plans spawned from this work>
```

## Git Integration Best Practices

- **Commit plans early.** Commit the initial PLAN.md and task files before
  starting work so the plan is version-controlled.
- **Commit progress atomically.** When checking off items, commit the file
  changes together with any code changes they represent.
- **Use meaningful commit messages.** Reference the task number:
  `Complete 003-login-endpoint: implement JWT login/logout`
- **Don't commit partial checkbox states.** Either the item is done or it
  isn't. Commit when work is complete, not in-progress.
- **Branch per task (optional).** For larger plans, consider a branch per
  task: `plan/user-auth/003-login-endpoint`.

## Spawning Sub-Plans

When a task is too complex to fit in a single task file (even after splitting),
spawn a nested sub-plan:

1. In the parent task file, add a note:
   ```markdown
   ## Notes
   - **Sub-plan:** See `../user-auth-oauth/PLAN.md` for detailed OAuth implementation
   ```

2. Create the sub-plan in a sibling directory:
   ```
   docs/plans/
     user-auth/
       PLAN.md
       003-oauth-integration.md  # References sub-plan
     user-auth-oauth/            # Sub-plan for complex OAuth work
       PLAN.md
       001-google-oauth.md
       002-github-oauth.md
   ```

3. Link the sub-plan completion to the parent task:
   - The parent task's completion criteria should include:
     `- [ ] Sub-plan user-auth-oauth is fully complete`

4. When the sub-plan completes:
   - Archive the sub-plan as normal.
   - Check off the parent task that spawned it.

This keeps individual task files focused while allowing complex work to be
properly structured.

## Compatibility Notes

This skill is designed to work with both **Claude Code** and **OpenAI Codex**.
The plan directory format is agent-agnostic markdown that any LLM can read,
update, and execute.

For Codex users:
- Install via skill-installer with `--repo DiversioTeam/agent-skills-marketplace
  --path plugins/plan-directory/skills/plan-directory`.
- Use `$skill plan-directory` to invoke.

For Claude Code users:
- Install via `/plugin install plan-directory@diversiotech`.
- Use `/plan-directory:plan` to invoke.
