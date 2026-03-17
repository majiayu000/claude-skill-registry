---
name: lisa-integration-test
description: This skill should be used when integration testing Lisa against a downstream project. It applies Lisa templates, verifies the project still builds, and if anything breaks, fixes the templates upstream in Lisa and retries until the project passes all checks.
---

# Lisa Integration Test

Apply Lisa templates to a downstream project and verify it works end-to-end. If anything breaks, fix the upstream templates in Lisa and retry until the project passes all checks.

This must be run FROM the Lisa repository directory.

## Prerequisites

- Running from the Lisa repo (has `src/core/lisa.ts`)
- The target project has Lisa applied (has `.lisa-manifest`)
- The target project's working directory is clean (no uncommitted changes)

## Instructions

### Step 1: Validate Environment

1. Confirm running from Lisa by checking for `src/core/lisa.ts`
2. Extract project path from `$ARGUMENTS`. If not provided, ask the user.
3. Validate the project path exists and has `.lisa-manifest`
4. Check the project's working directory is clean: `git -C <project-path> status --porcelain`
   - If dirty, tell the user and stop: "The project has uncommitted changes. Please commit or stash them first."

### Step 2: Record Baseline

Before applying Lisa, record the project's current state:

1. Read `<project-path>/.lisa-manifest` to note the current Lisa version
2. Run `git -C <project-path> log --oneline -1` to note the current HEAD
3. Note the project's branch and whether there's an open PR: `git -C <project-path> branch --show-current`

### Step 3: Apply Lisa

Run from the Lisa directory:

```bash
bun run dev <project-path>
```

If Lisa fails, report the error and stop.

### Step 4: Check What Changed

Run `git -C <project-path> status --short` to see what Lisa modified.

If nothing changed, report "Lisa applied cleanly with no changes" and stop.

### Step 5: Verify the Project

Run the project's verification commands in order. Stop at the first failure:

1. **Typecheck**: `cd <project-path> && bun run typecheck` (or `npm run typecheck` based on package manager)
2. **Lint**: `cd <project-path> && bun run lint` (or equivalent)
3. **Test**: `cd <project-path> && bun run test` (or equivalent)

Determine the package manager by checking which lockfile exists:
- `bun.lockb` → bun
- `pnpm-lock.yaml` → pnpm
- `yarn.lock` → yarn
- `package-lock.json` → npm

### Step 6: Handle Failures

If any verification step fails:

1. **Diagnose**: Analyze the error output to determine root cause
2. **Determine fix location**:
   - If the fix belongs in Lisa templates (the upstream change broke something), fix it in Lisa and go to Step 6a
   - If the fix belongs in the project's `*.local.*` files (project-specific override needed), fix it in the project and go to Step 6b
3. **Report** what failed and what you're fixing

#### Step 6a: Fix Upstream in Lisa

1. Make the fix in the Lisa template files
2. Run Lisa's own checks: `bun run typecheck && bun run lint && bun run test`
3. If Lisa's checks pass, go back to **Step 3** (re-apply Lisa to the project)
4. If Lisa's checks fail, fix those too, then retry

#### Step 6b: Fix in Project Local Files

1. Make the fix in the project's local override files (e.g., `tsconfig.local.json`, `eslint.config.local.ts`, `jest.config.local.ts`)
2. Go to **Step 5** (re-verify the project)

### Step 7: Commit and Push

Once all verification passes:

1. Stage all changes in the project: `git -C <project-path> add <changed-files>`
2. Commit with message: `chore: apply Lisa <version> templates`
3. Push to the project's remote
4. If upstream Lisa changes were made, commit and push those too

### Step 8: Report Results

Output a summary:

```
## Lisa Integration Test: PASSED

**Project:** <project-path>
**Lisa version:** <version>
**Branch:** <branch>

### Changes Applied
- <list of changed files>

### Verification
- Typecheck: PASSED
- Lint: PASSED
- Tests: PASSED

### Upstream Fixes (if any)
- <list of Lisa template fixes made>

### Commits
- <project-commit-hash> chore: apply Lisa <version> templates
- <lisa-commit-hash> fix: <description> (if upstream fixes were needed)
```

## Important Notes

- **Never skip verification** — the whole point is proving it works empirically
- **Fix upstream when possible** — if Lisa broke something, fix the template, not the project
- **Use local overrides for project-specific needs** — `tsconfig.local.json`, `eslint.config.local.ts`, etc.
- **Retry loop is bounded** — if you've tried 3 fix-and-retry cycles without success, stop and report the situation to the user
- **Preserve project conventions** — check the project's commit message style before committing
