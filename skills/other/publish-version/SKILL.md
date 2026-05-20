---
name: Publish Version
description: Automates the version publishing workflow for npm packages from a feature branch. Auto-detects base branch, lint, and test availability. Supports versioned releases (patch/minor/major) and no-version merges.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Publish Version

This skill automates the version publishing workflow preparation for npm packages from a feature branch. It supports both versioned releases that trigger npm publishing and no-version merges for accumulating changes.

## Features

- **Auto-detects base branch** from git remote default (main, master, release/*, etc.)
- **Auto-detects available scripts** (lint, test) and runs them if present
- **Monorepo support** - automatically syncs version across all tracked package.json files
- **Works in Claude Code web** via github skill wrapper scripts

## Architecture

The skill is split into three scripts for better control:

1. **validate.sh** - Pre-publish validation (read-only except npm install)
2. **finalize.sh** - Version bump and publish preparation
3. **publish.sh** - Wrapper that runs validate then finalize

This split allows manual test triage when resource contention causes test failures.

## What it does

### Validation Phase (validate.sh):

**Pre-flight checks:**
1. Auto-detect base branch from git remote
2. Verify current branch is a feature branch off base and is up to date

**Dependency updates & fixes (may modify files):**
3. Update all `@apexdesigner/*` dependencies (`npm update`)
   - Updates within semver range specified in package.json
   - Updates package-lock.json to latest compatible versions
4. Install dependencies (`npm install`) - may update package-lock.json
5. Build package (`npm run build`) - if build script exists (generates code first)
6. Run formatting (`npm run format`) - if format script exists (continues on error)
7. Run linting with auto-fix (`npm run lint -- --fix`) - if lint script exists

**Commit checkpoint:**
8. Check for uncommitted changes from steps 3-7
   - If files were modified, stop and prompt user to commit before continuing
   - This ensures all automated fixes (including formatted generated code) are captured before running tests

**Test validation:**
9. Run full test suite (`npm test`) - if test script exists

**Exit behavior:**
- Success: Suggests running finalize.sh
- Uncommitted changes: Lists modified files and suggests commit command
- Test failure: Provides guidance on re-running failed tests individually

### Finalization Phase (finalize.sh):

**Pre-flight checks:**
1. Verify clean working directory
2. Verify on feature branch
3. If run directly (not from publish.sh): Confirm failed tests were verified individually

### Version mode (patch/minor/major/X.Y.Z):

**Version update:**
4. Get current version from package.json and increment
5. Update version in all tracked package.json files (monorepo support)
6. Merge any Unreleased CHANGELOG entries + new commits into versioned entry
7. Create git tag (v{version}) - **triggers npm publish on merge**

**PR preparation:**
8. Commit version changes
9. Push changes and tags to remote
10. Create PR using github skill wrapper (works in Claude Code web)

### None mode (no version bump):

**No version update:**
4. Skip version increment in package.json
5. Add commits to Unreleased section in CHANGELOG.md
6. Skip git tag creation - **will NOT trigger npm publish**

**PR preparation:**
7. Commit all changes
8. Push changes to remote
9. Create PR indicating no version bump

## Usage

### Automatic workflow (validation passes):

Default (patch):
```bash
bash .claude/skills/publish-version/scripts/publish.sh" patch
```

Other increment types:
```bash
bash .claude/skills/publish-version/scripts/publish.sh" minor
bash .claude/skills/publish-version/scripts/publish.sh" major
bash .claude/skills/publish-version/scripts/publish.sh" 0.7.0  # exact version
bash .claude/skills/publish-version/scripts/publish.sh" none   # no version bump
```

### Manual workflow (test triage needed):

When tests fail due to resource contention:

**Step 1: Validate**
```bash
bash .claude/skills/publish-version/scripts/validate.sh"
```

**Step 2: Re-run failed tests individually (REQUIRED)**

> **CRITICAL:** You MUST re-run each failed test individually and verify it passes before proceeding to finalize. Do NOT skip this step.

```bash
npm test -- <test-file> -t "<test-name>"
```

Run each failed test one at a time. Only after ALL failed tests pass individually can you proceed.

**Step 3: Finalize** (ONLY after confirming ALL tests pass individually)
```bash
bash .claude/skills/publish-version/scripts/finalize.sh" patch
```

### Individual script usage:

**validate.sh** - Run validation only (no side effects):
```bash
bash .claude/skills/publish-version/scripts/validate.sh"
```

**finalize.sh** - Skip validation and finalize:
```bash
bash .claude/skills/publish-version/scripts/finalize.sh" [none|patch|minor|major|VERSION]
```

**publish.sh** - Run both in sequence:
```bash
bash .claude/skills/publish-version/scripts/publish.sh" [none|patch|minor|major|VERSION]
```

## Notes

**All modes:**
- Requires clean working directory
- Must be on a feature branch tracking the base branch
- All available validation steps must pass
- PR is created using github skill (works with GITHUB_TOKEN or gh CLI)

**Version mode (patch/minor/major/X.Y.Z):**
- Creates git tag (v{version}) that triggers npm publish on merge
- GitHub Actions auto-publishes to npm when tagged commit is merged to release branch
- Merges any Unreleased CHANGELOG entries into the new version
- Updates all tracked package.json files (monorepo support)

**None mode:**
- Does NOT create git tag - will NOT trigger npm publish
- Adds changes to Unreleased section in CHANGELOG.md
- Only works when there are actual code changes to commit
- Use this to accumulate multiple changes before publishing a version

**Resource contention handling:**
- Tests sometimes fail when run in full suite due to resource contention
- These same tests pass when run individually
- Use validate.sh → manual test triage → finalize.sh workflow
- validate.sh provides clear guidance on next steps when tests fail
- **CRITICAL:** You MUST re-run each failed test individually and confirm it passes BEFORE running finalize.sh. Never skip the test triage step.

## Output Presentation

**PR Creation:**
- finalize.sh creates the PR using the github skill wrapper
- PR URL is displayed at the end of the script output
- The PR URL is the most important actionable item for the user

## Post-Merge Cleanup

After the PR is created and the user merges it, offer to:

1. Switch to the base branch and pull latest:
   ```bash
   git checkout main && git pull
   ```

2. Delete the feature branch (optional):
   ```bash
   git branch -d <feature-branch>
   ```

This prevents accidentally adding commits to a merged branch.
