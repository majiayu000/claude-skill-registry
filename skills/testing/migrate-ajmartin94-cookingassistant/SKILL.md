---
name: migrate
description: |
  Interactive cleanup of broken tests and code after a new feature lands. Use this skill
  when: (1) TDD is complete but the full test suite has failures, (2) the user says
  "migrate" or "fix broken tests", (3) preparing a branch for PR after feature work.
---

# Migrate

Interactive cleanup after TDD execution. You run the suite, surface breakage, and
the user decides what to do about each failure. You execute their decisions.

## Prerequisites

- TDD execution is complete (new feature tests pass)
- Full test suite has not been verified green yet

## Process

### 0. Environment Setup

Activate virtual environments and verify infrastructure before running tests:

```bash
# Backend: activate venv (NEVER claim "pytest unavailable" without checking)
cd backend && source venv/bin/activate && python -m pytest --version

# Frontend: verify node_modules
cd frontend && ls node_modules/.bin/vitest

# E2E: start servers if needed for E2E tests
cd backend && source venv/bin/activate && uvicorn app.main:app --port 8001 &
cd frontend && npm run dev -- --port 5174 &
```

If venv or node_modules don't exist, install dependencies first (`pip install -r requirements.txt` / `npm install`).

### 1. Run Full Suite

Run all test layers (with venv activated for backend):

```bash
cd backend && source venv/bin/activate && python -m pytest
cd frontend && npm test -- --run
cd e2e && npx playwright test
```

Collect all failures.

### 2. Categorize Failures

Separate failures into:

| Category | Meaning | Action |
|----------|---------|--------|
| New feature tests failing | Bug in the feature | Flag — TDD didn't complete cleanly |
| Existing tests failing | Cascade from new behavior | Present to user for decision |

All failures are caused by this branch — main is always green.

### 3. Present Each Failure

For each existing test failure caused by the new feature, use `AskUserQuestion`:

Present:
- Test name and file
- What it asserts (the old behavior)
- Why it fails (the new behavior)
- Relevant code diff if helpful

Options:
- **Update test** — modify assertions to reflect new correct behavior
- **Remove test** — this scenario no longer applies
- **This is a bug** — the feature broke something it shouldn't have; needs fixing
- **Skip for now** — revisit later

Group related failures by topic when possible (e.g., "These 4 tests all assert
the old response format for GET /recipes").

### 4. Execute Decisions

For each decision:

- **Update test**: Modify the test to assert new behavior. Run it to confirm it passes.
- **Remove test**: Delete the test. If it was the only test for that behavior, ask
  if replacement coverage is needed.
- **Bug**: Create a LEARNING task noting the regression. Do not fix in migration —
  this goes back to the feature implementation.
- **Skip**: Leave as-is, note it for later.

### 5. Database Migrations

Evaluate code changes in this branch for database impact:

- Check for new/modified models, schema changes, or new fields
- Check for changed relationships or constraints
- Check for renamed or removed columns/tables

If database changes are detected, present to user via `AskUserQuestion`:
- What changed (model/field/relationship)
- Whether a migration is needed (new table, altered column, etc.)
- Suggested migration approach (e.g., Alembic revision, data backfill, nullable transition)

For each migration needed:
- **Generate migration**: Create the migration file, run it, verify it applies cleanly
- **Data backfill**: If existing rows need default values, suggest and confirm approach
- **Destructive changes**: Flag column/table removals — confirm data loss is acceptable

If no database changes detected, skip this step.

### 6. Verify

After all decisions are executed:
- Run full suite again
- If new failures appear (from the fixes), repeat from step 3
- Continue until suite is green or only skipped/bug items remain

### 7. Summary

Present final state:
- Tests updated: [count and list]
- Tests removed: [count and list]
- Migrations created: [count and list]
- Bugs found: [count and list — these need attention]
- Skipped: [count and list]
- Suite status: GREEN / remaining failures

Tell the user: "Migration complete. Run `/code-review` to verify against the plan
before PR."

## Principles

- **User decides** — never update or remove a test without explicit approval
- **Group related failures** — don't ask about 10 tests one at a time if they're the same issue
- **Bugs go back** — if the feature broke something unintentionally, that's a bug, not a migration
- **Green suite before PR** — the goal is a clean test suite
