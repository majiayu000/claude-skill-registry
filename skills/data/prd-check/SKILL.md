---
description: Run PRD validation to check story quality, test coverage, and structure.
---

# PRD Check

Run PRD validation on demand to check story quality, test coverage, and structure before starting the autonomous loop.

## Instructions

When the user runs `/prd-check`, validate their PRD file.

### Step 1: Check PRD Exists

```bash
ls -la .ralph/prd.json 2>/dev/null || echo "NOT_FOUND"
```

If no PRD exists, tell the user:
> No PRD found at `.ralph/prd.json`. Generate one first with `/idea` or `/prd`.

**STOP** if no PRD found.

### Step 2: Run Validation (dry-run)

Run validation without auto-fix so you can present results and let the user decide:

```bash
npx ralph prd-check --dry-run 2>&1
```

### Step 3: Present Results

Show the validation output to the user. If there are issues, summarize them clearly.

If issues were found, ask:
> "Would you like me to fix these issues in the PRD?"

**STOP and wait for user response.**

If the user says yes, read `.ralph/prd.json`, fix the issues following PRD best practices (executable testSteps with curl/pytest/playwright, apiContract for backends, testUrl for frontends, security criteria for auth stories, pagination for list endpoints), and write the fixed file back.

## Notes

- This is the same validation that runs automatically at `ralph run` startup
- `--dry-run` skips auto-fix so you have control over what changes
- Custom checks in `.ralph/checks/prd/` are also evaluated
- Run this before `ralph run` to catch and fix issues interactively
