---
name: rewrite-history
description: 'Restructure branch into clean, reviewer-friendly commits. Analyzes total diff since main, groups files by concern, and rewrites with conventional commit messages.'
---

# Rewrite History Command

Restructures messy branch history into a clean, reviewer-friendly progression of logical commits.

## Overview

This command:
1. Analyzes total diff since divergence from main/master (ignores existing commits)
2. Groups files by single concern
3. Arranges in logical order (foundations first, features second, polish last)
4. Generates Conventional Commit messages
5. Rewrites history: `git reset --soft` → `git add` + `git commit` for each group

**Modes**:
- **Interactive** (default): Shows proposal, allows adjustment/approval via AskUserQuestion
- **Automatic** (`--auto`): Skips proposal, executes directly

## Steps

### 1. Precondition Checks

Before any destructive operations, verify:

1. **Not on main branch**: Check current branch is not `main` or `master`
   - If on main: Error "Cannot rewrite history on main/master branch. Checkout a feature branch first."

2. **Clean working tree**: Run `git status --porcelain`
   - If uncommitted changes: Error "Uncommitted changes detected. Commit or stash changes before rewriting history."

3. **Identify base branch and fetch**:
   - Try `git fetch origin main` or `git fetch origin master` (whichever exists)
   - If fetch succeeds: use `origin/main` or `origin/master` as base
   - If fetch fails (no remote, offline): fall back to local `main` or `master`
   - Report which base is being used: "Using origin/main as base" or "Using local main as base (no remote)"

4. **Has commits to rewrite**: Find merge-base with base branch, count commits
   - Run `git merge-base HEAD {base-branch}`
   - Run `git rev-list --count {merge-base}..HEAD`
   - If 0 commits: Error "No commits to rewrite. Branch is up to date with main."

### 2. Create Backup Branch

**Always create backup before destructive operations.**

```bash
git branch {current-branch}-backup-{YYYYMMDD-HHMM}
```

Report: "Created backup: {backup-branch-name}"

### 3. Analyze Diff

Get the full diff since divergence:

1. **Get merge-base**: `git merge-base HEAD {base-branch}` (using origin/main or local main from step 1)
2. **Get full diff**: `git diff {merge-base}..HEAD`

**Analysis goals** (based solely on the diff):
- Identify distinct concerns/features in the changes
- Group related files together
- Determine logical ordering (dependencies, foundations before features)

Do NOT investigate individual commits or commit history—only analyze the diff content.

### 4. Generate Proposal

Create a restructuring proposal:

```
Proposed commits:

1. {type}({scope}): {description}
   - Files: {key files affected}

2. {type}({scope}): {description}
   - Files: {key files affected}

[...]
```

**Grouping principles**:
- One concern per commit
- Logical order: setup/config -> core features -> secondary features -> tests -> docs
- Atomic commits that could theoretically be reverted independently

### 5. Interactive Approval (unless --auto)

If `$ARGUMENTS` does NOT contain `--auto`:

Use AskUserQuestion to present proposal and get approval:

```
Proceed with this restructuring?
- [Yes] Execute as proposed
- [Adjust] Describe changes to the proposal
- [Cancel] Abort without changes
```

**If "Adjust"**: Parse user feedback, regenerate proposal, ask again.

**If "Cancel"**: Report "Cancelled. No changes made. Backup branch preserved: {backup-name}" and exit.

**If "Yes"** or `--auto` mode: Proceed to execution.

### 6. Execute Rewrite

Perform the history rewrite:

1. **Soft reset to merge-base**:
   ```bash
   git reset --soft {merge-base}
   ```
   This preserves all changes in the working directory but removes all commits.

2. **Create new commits** - for each group in the proposal, execute:
   ```bash
   git add {files-for-this-commit}
   git commit -m "{message}"
   ```
   Repeat for each logical commit group until all changes are committed.

3. **Verify result**:
   ```bash
   git log --oneline {merge-base}..HEAD
   git diff {backup-branch}..HEAD  # should be empty
   ```

Report: "History rewritten into {new-count} commits"

### 7. Push Prompt

After successful rewrite, prompt about pushing:

Use AskUserQuestion:
```
Push rewritten history to remote?
- [Yes] Push with --force-with-lease (safe force push)
- [No] Keep changes local (you can push manually later)
```

**If "Yes"**:
```bash
git push --force-with-lease
```
Report: "Pushed to remote with --force-with-lease"

**If "No"**:
Report: "Changes kept local. Push manually when ready: git push --force-with-lease"

### 8. Summary

Report final summary:

```
History rewrite complete.

Commits: {M}
Backup: {backup-branch-name}

New history:
{git log --oneline output}
```

## Important Guidelines

- **Diff-only analysis** - only look at the full diff, never investigate individual commits
- **Always use `--force-with-lease`** instead of `--force` for push safety
- **Backup branch is permanent** - only delete manually after confirming rewrite is correct
- **Verify no code changes** - diff between backup and new HEAD should be empty
- **Conventional Commits** - use standard types (feat, fix, docs, refactor, test, chore)
- **One concern per commit** - resist urge to combine unrelated changes

## Edge Cases

| Scenario | Handling |
|----------|----------|
| On main/master branch | Error: "Cannot rewrite history on main/master branch. Checkout a feature branch first." |
| Uncommitted changes | Error: "Uncommitted changes detected. Commit or stash changes before rewriting history." |
| No remote available | Fall back to local main/master. Report: "Using local main as base (no remote)" |
| No commits since main | Error: "No commits to rewrite. Branch is up to date with main." |
| Single commit only | Proceed normally (may reorganize or improve commit message) |
| Conflicts during commit creation | Should not occur (soft reset preserves all changes). If staging issues, report specific files. |
| Push rejected despite --force-with-lease | Error: "Push rejected. Remote has new commits. Fetch and review before retrying." |
| User cancels mid-execution | Backup branch preserved. User can: `git reset --hard {backup-branch}` to restore. |

## Example Usage

```bash
# Interactive mode (default)
/rewrite-history

# Automatic mode (skip proposal approval)
/rewrite-history --auto
```

## Example Output

**Interactive mode**:
```
Using origin/main as base.
Analyzing diff...

Created backup: feature-auth-backup-20260107-1430

Proposed commits:

1. feat(auth): add JWT authentication middleware
   - Files: src/middleware/auth.ts, src/utils/jwt.ts

2. feat(auth): implement login and logout endpoints
   - Files: src/routes/auth.ts, src/controllers/auth.ts

3. test(auth): add authentication test suite
   - Files: tests/auth/*.test.ts

4. docs(auth): add authentication documentation
   - Files: docs/auth.md, README.md

Proceed with this restructuring?
- [Yes] Execute as proposed
- [Adjust] Describe changes to the proposal
- [Cancel] Abort without changes

> Yes

History rewritten into 4 commits.

Push rewritten history to remote?
- [Yes] Push with --force-with-lease
- [No] Keep changes local

> Yes

Pushed to remote with --force-with-lease

History rewrite complete.

Commits: 4
Backup: feature-auth-backup-20260107-1430

New history:
a1b2c3d docs(auth): add authentication documentation
e4f5g6h test(auth): add authentication test suite
i7j8k9l feat(auth): implement login and logout endpoints
m0n1o2p feat(auth): add JWT authentication middleware
```
