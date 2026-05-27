---
name: decompose-branch
description: Reorganize a messy local branch into focused, atomic commits before sharing. Use when user says "decompose branch", "clean up commits", "reorganize my branch", or wants to restructure local work.
---

# Decompose Branch

Turn a messy local branch into a sequence of atomic commits ready for review.

## When to Use

- Branch has messy/WIP commits before PR
- Reviewer feedback says "hard to follow"
- Splitting a large change into reviewable chunks

**Note:** Commands below use `master` as base branch. Replace with your actual base if different.

## Phase 1: Analyze

Gather context and identify the distinct logical changes.

```bash
# See what commits exist on this branch vs base
git log --oneline master..HEAD

# See the full diff against base
git diff master...HEAD

# See changed files
git diff --stat master...HEAD
```

Read the diff and classify each modified section into one of these categories:

1. **Refactors** — Renames, extractions, reorganizations (these go first)
2. **Structural changes** — New types, new fields, new functions
3. **Behavioral changes** — Modified control flow, new conditions
4. **Bug fixes** — Isolated corrections
5. **Tests** — Often map 1:1 to behavioral changes

**Present to user:**

```
## Identified Changes

| # | Change | Files | Depends On |
|---|--------|-------|------------|
| 1 | Extract helper for validation | utils.ts | - |
| 2 | Add retry logic to client | client.ts | 1 |
| 3 | Fix timeout handling | client.ts | 2 |
| 4 | Tests for retry and timeout | client.test.ts | 2, 3 |
```

**Stop and ask:** "Does this decomposition look correct, or would you like to reorder, combine, or split changes?" Wait for confirmation before proceeding.

## Phase 2: Plan the Decomposition

Determine the commit order based on dependencies.

**Dependency rules:**

- Refactors before features that depend on them
- Types/interfaces before code that uses them
- Core logic before tests
- Changes to the same function ordered by logical progression

**For each commit, define:**

- Subject line (imperative mood, max 50 chars)
- Which files/sections to include (with line ranges if helpful)
- Whether it should build/pass lint

**Present the plan:**

```
## Commit Plan

1. "Extract validation helper from handler"
   - utils.ts: new validateInput function
   - handler.ts: use new helper
   - Builds: Yes

2. "Add retry logic to client"
   - client.ts: retry wrapper, config
   - Builds: Yes

3. "Fix timeout handling in retry loop"
   - client.ts: timeout check in retry
   - Builds: Yes

4. "Add tests for retry and timeout"
   - client.test.ts: new test cases
   - Builds: Yes
```

**Stop and ask:** "Ready to execute this plan?" Wait for confirmation before proceeding.

**On atomicity:** Prefer commits that build and pass lint. Group inseparable changes (e.g., signature changes with caller updates).

## Phase 3: Execute

Create a fresh branch and build commits incrementally.

```bash
# Save current branch name
ORIGINAL_BRANCH=$(git branch --show-current)

# Create working branch from base
git checkout -b ${ORIGINAL_BRANCH}-decomposed master

# Bring in all changes unstaged
git merge --squash ${ORIGINAL_BRANCH}
git reset HEAD
```

Now you have all changes as unstaged modifications. Build commits one at a time:

**For each planned commit:**

1. Stage only the relevant files/sections
2. Verify it builds (if plan says "Builds: Yes")
3. Commit with the planned message
4. Repeat

```bash
# Stage by file (for hunk-level control, edit files to isolate changes first)
git add <file>

# Verify build (required if plan says Builds: Yes)
# Ask user for build command if unknown

# Commit
git commit -m "<planned message>"
```

**After all commits:**

```bash
# Verify nothing left unstaged
git status

# If leftover changes exist:
# - Amend last commit if changes logically belong there
# - Create cleanup commit if unrelated to existing commits
# - Discard if debug/temp code (git checkout -- <file>)
```

## Phase 4: Verify

Ensure the decomposed branch matches the original.

```bash
# Compare final state to original branch (should be empty or whitespace-only)
git diff ${ORIGINAL_BRANCH}..HEAD
```

If differences exist:

- Acceptable: formatting, whitespace only
- Not acceptable: missing changes — add a commit or amend to include them

**Present summary:**

```
## Decomposition Complete

Original: feature-branch (5 messy commits)
Result: feature-branch-decomposed (4 atomic commits)

| # | Commit | Summary |
|---|--------|---------|
| 1 | abc123 | Extract validation helper |
| 2 | def456 | Add retry logic |
| 3 | ghi789 | Fix timeout handling |
| 4 | jkl012 | Add tests |

**Next steps:**
git log --oneline master..HEAD    # Review commits
git diff master..HEAD             # Verify full change
git branch -m feature-branch feature-branch-old  # Backup original
git branch -m feature-branch-decomposed feature-branch  # Rename
```

## HIL Pattern

- Ask for branch name if not on a feature branch
- Stop after Phase 1 and Phase 2 for user approval
- Confirm before any destructive action

## Guardrails

- Never modify master
- Never force push without approval
- Keep original branch until user confirms
- If build fails unexpectedly, stop and ask
- Prefer cohesive commits over fragmentation
