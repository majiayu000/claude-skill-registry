---
name: hotfix
description: Emergency production fix — branch, fix, test, merge, release in minimal steps (Marcus workflow)
disable-model-invocation: true
---

Emergency hotfix: $ARGUMENTS

This is the FAST PATH for critical production issues. Skip planning, skip full review — fix, test, ship.

## Step 1 — Create Hotfix Branch
```bash
git checkout main
git pull origin main
git checkout -b hotfix/<short-description>
```

## Step 2 — Identify and Fix
- Read the error/symptom
- Find the root cause (minimal investigation)
- Apply the SMALLEST possible fix
- Do NOT refactor, do NOT improve adjacent code
- Do NOT add features — fix ONLY the bug

## Step 3 — Write Regression Test
Write a test that:
1. Reproduces the bug (would fail on main)
2. Passes with the fix applied

## Step 4 — Verify
Run the test and type-check commands (see project config).
Both MUST pass. The hotfix must not break anything else.

## Step 5 — Commit
```bash
git add <specific files only>
git commit -m "fix(<scope>): <description of the fix>

Hotfix for production issue: <brief description of the symptom>"
```

## Step 6 — Merge to Main
```bash
git checkout main
git merge hotfix/<short-description>
```

## Step 7 — Patch Release
Bump the patch version:
1. Update the version field in the config file
2. Update the env example file version
3. Commit: `chore: release v<X.Y.Z+1>`
4. Tag: `git tag -a v<X.Y.Z+1> -m "Hotfix: <description>"`
5. Push: `git push origin main && git push origin v<X.Y.Z+1>`

## Step 8 — Clean Up
```bash
git branch -d hotfix/<short-description>
```

## Rules
- SMALLEST possible change — do not scope-creep a hotfix
- ALWAYS write a regression test — this bug should never recur
- ALWAYS bump the patch version
- NEVER skip tests — even for emergencies
- Total time target: under 30 minutes from diagnosis to deploy