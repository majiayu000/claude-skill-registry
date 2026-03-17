---
name: hotfix
description: Fast-track an urgent fix through a streamlined pipeline. Skips Product/Feature Council, applies the fix, runs a focused review, and creates a PR with optional Deployment Council. Use for production bugs, security patches, or critical regressions that cannot wait for the full planning pipeline.
user-invokable: true
---

# Hotfix Workflow

Apply an urgent fix through a streamlined pipeline that skips the full planning cycle. This skill is for production bugs, security patches, and critical regressions.

> [!CAUTION]
> **This is NOT a shortcut for feature work.** If the change adds new functionality, changes user-facing behavior, or touches more than ~100 lines, use `/plan-feature` instead. Hotfixes should be small, focused, and clearly scoped.

> [!CAUTION]
> **Scope boundary**: This skill implements the fix, reviews it, creates a PR, and monitors CI. It covers the full lifecycle for urgent fixes so the user does not need to chain multiple skills.

## Step 1: Define the Fix

### CHECKPOINT: Confirm Hotfix Scope

Ask the user to describe the issue. Gather:

1. **What is broken?** (symptom, error message, affected users)
2. **Where is the bug?** (file, endpoint, component — if known)
3. **How urgent?** (production down, data corruption, security vulnerability, degraded experience)
4. **GitHub issue number** (if one exists)

If the user provides a GitHub issue number, fetch it:

```bash
gh issue view <number> --json title,body,labels,state,number
```

Present a summary and ask the user to confirm this is appropriate for hotfix (not a feature).

## Step 2: Create Branch and Investigate

1. Ensure you are on `main` and up to date:

   ```bash
   git fetch origin
   git checkout main
   git pull origin main
   ```

2. Create a `fix/` branch:

   ```bash
   git checkout -b fix/<short-description>
   ```

3. If a GitHub issue exists, add the `in-progress` label (following AGENTS.md label management rules — remove from any other issue first).

4. Investigate the bug: read relevant files, reproduce the issue if possible, identify the root cause.

Present the root cause analysis to the user before proceeding.

## Step 3: Apply the Fix

1. Make the minimal change needed to resolve the issue.
2. Write or update tests to cover the bug (regression test).
3. Run self-checks:

   ```bash
   pnpm type-check
   pnpm lint
   pnpm test
   ```

4. Fix any failures from the checks above.

### CHECKPOINT: Review the Fix

Present:
- Files changed (with a brief description of each change)
- Tests added or modified
- Test results (pass/fail, coverage)

Wait for user approval before committing.

## Step 4: Commit

Commit with conventional commit format:

```bash
git add <specific-files>
git commit -m "fix(<scope>): <description>"
```

## Step 5: Focused Review

Run a lightweight review (not the full Review Council):

1. **Security scan** (always): Invoke `/security-scanning:security-sast` on changed files.
2. **Accessibility check** (if frontend changes): Invoke `/ui-design:accessibility-audit` on modified components.

If the security scan finds Critical or High severity issues in the changed files, present them to the user. Fix any legitimate findings before proceeding.

## Step 6: Deployment Council (Conditional)

Activate the **Deployment Council** only if the fix involves:
- Database migrations
- Docker or infrastructure changes
- Environment variable modifications
- Authentication or authorization code

If none of these apply, skip to Step 7.

If activated, run the Deployment Council evaluation from `.claude/councils/deployment-council.md` with all 3 members (Platform Engineer, Security Engineer, QA Lead).

### CHECKPOINT: Deployment Readiness

Present the Deployment Council verdict. Wait for user approval.

## Step 7: Create PR and Monitor CI

1. Run pre-push checks:

   ```bash
   pnpm type-check && pnpm lint && pnpm format:check && pnpm test
   ```

   Auto-fix formatting issues with `pnpm format` if `format:check` fails.

2. Push and create PR:

   ```bash
   git push -u origin fix/<short-description>
   ```

3. Generate PR description. Use the template from `.github/PULL_REQUEST_TEMPLATE.md` if it exists. Include:
   - Description of the bug and root cause
   - The fix applied
   - Tests added
   - Related issue number (if applicable)

### CHECKPOINT: PR Description

Present the PR title and body. Wait for user approval.

4. Create the PR:

   ```bash
   gh pr create --title "<title>" --body "<body>"
   ```

5. Monitor CI:

   ```bash
   gh run list --branch fix/<short-description> --limit 1 --json databaseId --jq '.[0].databaseId'
   ```

   Then watch:

   ```bash
   gh run watch <run-id> --exit-status
   ```

6. If CI fails, diagnose and fix. Present the fix to the user before committing.

## Step 8: Hand Off

Present the completed hotfix summary:

- PR URL
- Files changed
- Tests added
- CI status
- Related issue (if applicable)

> You completed **`/hotfix`**. The PR is ready for merge. If there is a related GitHub issue, it will close automatically when the PR merges (if the PR body includes `Closes #N`).
