---
name: rollback
description: Roll back a bad release to the previous known-good version (Marcus workflow)
disable-model-invocation: true
---

Roll back: $ARGUMENTS

When a release causes production issues and a hotfix isn't feasible, roll back to the last known-good state.

## Step 1 — Identify What to Roll Back To
```bash
git tag --sort=-v:refname | head -10
git log --oneline -10
```
Find the last known-good version (usually the tag BEFORE the current one).

## Step 2 — Verify the Target is Good
```bash
git checkout v<known-good-version>
```
Run the test and type-check commands (see project config) to confirm it's stable.

## Step 3 — Choose Rollback Strategy

### Option A: Revert Commit (preferred — preserves history)
```bash
git checkout main
git revert <bad-commit-hash>
```

### Option B: Reset to Tag (if revert is too complex)
```bash
git checkout main
git branch backup/pre-rollback
git reset --hard v<known-good-version>
git push origin main --force-with-lease
```

## Step 4 — Verify Rollback
Run the test and type-check commands.
Verify the app starts correctly using the dev run command (see project config).

## Step 5 — Tag the Rollback
```bash
git tag -a v<rollback-version> -m "Rollback: reverted to v<known-good>"
git push origin main
git push origin v<rollback-version>
```

## Step 6 — Post-Rollback
- Document what went wrong and why
- Create an issue for the proper fix
- Schedule the fix using `/fix-issue` or `/hotfix`
- Consider adding tests that would have caught the issue

## Rules
- ALWAYS verify the target version with tests before rolling back
- ALWAYS create a backup branch before destructive operations
- PREFER `git revert` over `git reset --hard` (preserves history)
- NEVER force-push without team confirmation
- ALWAYS document the rollback reason