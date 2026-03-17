---
name: pr
description: Create a pull request with proper title, description, and test plan
disable-model-invocation: true
---

Create a pull request for the current branch: $ARGUMENTS

## Step 1 — Pre-PR Validation
Run the test and type-check commands (see project config).
Both MUST pass. Never create a PR with failing tests or type errors.

## Step 2 — Analyze Changes
```bash
git log main..HEAD --oneline
git diff main...HEAD --stat
```
Understand the full scope of changes since branching from main.

## Step 3 — Generate PR Title
- Under 70 characters
- Use imperative mood: "Add...", "Fix...", "Update..."
- Be specific about what changed

## Step 4 — Generate PR Body
Use this structure:
```markdown
## Summary
- Bullet point 1: what changed and why
- (1-3 bullets max)

## Changes
- List every file modified/created/deleted with brief reason

## Test Plan
- [ ] All existing tests pass
- [ ] Type checking passes
- [ ] New tests added for: <list new test coverage>
- [ ] Manual verification: <steps>

## Checklist
- [ ] Future annotations pattern followed (see stack concepts)
- [ ] Typed exceptions (no generic `Exception`)
- [ ] Typed schemas for all request/response shapes (see stack concepts)
- [ ] OpenAPI metadata on all new endpoints
- [ ] Project documentation updated (if new endpoints/config)
- [ ] Env example file updated (if new settings)
```

## Step 5 — Push and Create PR
```bash
git push -u origin <branch-name>
gh pr create --title "<title>" --body "<body>"
```

## Step 6 — Confirm
Output the PR URL so it can be reviewed.