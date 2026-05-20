---
description: Run PRD validation to check story quality, test coverage, and structure.
---

# PRD Check

Run PRD validation on demand to check story quality, test coverage, and structure before starting the autonomous loop. Cross-references against learned lessons and past failure patterns.

## Instructions

When the user runs `/prd-check`, validate their PRD file.

### Step 1: Check PRD Exists

```bash
ls -la .ralph/prd.json 2>/dev/null || echo "NOT_FOUND"
```

If no PRD exists, tell the user:
> No PRD found at `.ralph/prd.json`. Generate one first with `/prd`.

**STOP** if no PRD found.

### Step 2: Load Project Knowledge

Read the project's accumulated knowledge:

1. Read lessons:
   ```bash
   cat .ralph/lessons.json 2>/dev/null
   ```

2. Read suggested lessons (last 50 lines — file can be huge):
   ```bash
   tail -50 .ralph/suggested-lessons.txt 2>/dev/null
   ```

3. Read recent progress for failure patterns:
   ```bash
   tail -100 .ralph/progress.txt 2>/dev/null
   ```

### Step 3: Run Structural Validation (dry-run)

```bash
npx ralph prd-check --dry-run 2>&1
```

Present any structural issues found.

### Step 4: Cross-Reference Against Lessons

Read `.ralph/prd.json` and for each story, check if any lesson applies:

- **Backend lessons** → check against backend stories
- **Frontend lessons** → check against frontend stories
- **General lessons** → check against all stories

For each applicable lesson, verify the story's `acceptanceCriteria`, `constraints`,
`notes`, or `testSteps` reflect the pattern. Flag stories that should account for
a lesson but don't.

**Examples:**
- Lesson: "Always use bcrypt cost 10+ for passwords" → Flag auth stories missing
  bcrypt in acceptanceCriteria
- Lesson: "Use date-fns instead of moment.js" → Flag frontend stories that create
  date utilities without this constraint
- Lesson: "Add data-testid for Playwright selectors" → Flag frontend stories missing
  this in constraints

### Step 5: Check Against Suggested Learnings

Scan `suggested-lessons.txt` for patterns relevant to the current PRD's feature area.
Flag any recurring failure patterns that the PRD's stories don't address.

### Step 6: Present Results

Summarize all findings in categories:

> **Structural Issues** (from prd-check):
> - [list]
>
> **Lesson Conflicts** (stories that don't account for known patterns):
> - TASK-003: Missing lesson "bcrypt cost 10+" in auth story
> - TASK-005: Missing lesson "data-testid attributes" in frontend story
>
> **Suggested Improvements** (from past learnings):
> - [relevant patterns from suggested-lessons.txt]

Ask: "Would you like me to fix these issues in the PRD?"

**STOP and wait for user response.**

If yes, update `.ralph/prd.json`:
- Add missing lesson patterns to relevant story `constraints` or `acceptanceCriteria`
- Fix structural issues per PRD best practices
- Write the fixed file back

## Notes

- This is the same structural validation that runs automatically at `ralph run` startup
- `--dry-run` skips auto-fix so you have control over what changes
- Custom checks in `.ralph/checks/prd/` are also evaluated
- Lessons cross-referencing catches patterns that structural validation can't
- Run this before `ralph run` to catch and fix issues interactively
