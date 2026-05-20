---
name: finish
description: >
  Use when implementation is complete and you need to merge, create a PR, or clean up —
  verifies tests pass, presents 4 structured integration options, executes chosen workflow,
  and cleans up worktrees. Pairs with code-forge:worktree.
---

# Code Forge — Finish

Complete a development branch by verifying tests, choosing an integration strategy, and cleaning up.

## When to Use

- Implementation is complete and all tasks are done
- After code-forge:impl finishes all tasks for a feature
- When you need to integrate a feature branch back to main
- When you want to discard experimental work cleanly

## Workflow

```
Verify Tests → Determine Base Branch → Present 4 Options → Execute Choice → Cleanup Worktree
```

### Step 1: Verify Tests

Run the full test suite before proceeding (following the `code-forge:verify` discipline — run fresh, read full output, confirm zero failures).

```bash
# Auto-detect and run test command
```

- **All pass:** Proceed to Step 2
- **Any fail:** **STOP.** Do not proceed. Report failures and suggest fixes.

### Step 2: Determine Base Branch

```bash
# Find the upstream branch this was created from
BASE_BRANCH=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null | sed 's|origin/||' || echo "main")
```

### Step 3: Present Exactly 4 Options

Present these options to the user using `AskUserQuestion`. Do NOT modify, add, or remove options:

**Option 1: Merge back to {base-branch} locally**
- `git checkout {base-branch} && git merge {feature-branch}`
- Best when: working solo, no review needed

**Option 2: Push and create Pull Request**
- `git push -u origin {feature-branch}` then `gh pr create`
- Best when: team workflow, review required

**Option 3: Keep branch as-is**
- No action taken, worktree preserved
- Best when: work in progress, will continue later

**Option 4: Discard this work**
- Requires typing "discard" to confirm
- Removes branch and all changes permanently

### Step 4: Execute Choice

**Option 1 — Merge:**
```bash
# If inside a worktree, cd to the main repo first
MAIN_REPO=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel 2>/dev/null)
if [ -n "$MAIN_REPO" ] && [ "$MAIN_REPO" != "$(git rev-parse --show-toplevel)" ]; then
  cd "$MAIN_REPO"
fi
git checkout {base-branch}
git merge {feature-branch} --no-ff
```

**Option 2 — Push + PR:**
```bash
git push -u origin {feature-branch}
gh pr create --title "{feature-name}: <summary>" --body "$(cat <<'EOF'
## Summary
<generated from commits>

## Test plan
- [ ] All tests pass

Generated with [code-forge](https://github.com/anthropics/claude-code)
EOF
)"
```
Report the PR URL to the user.

**Option 3 — Keep:**
No action. Report current branch and worktree location.

**Option 4 — Discard:**
Ask user to type "discard" to confirm. Then:
```bash
git checkout {base-branch}
git branch -D {feature-branch}
```

### Step 5: Cleanup Worktree

**Options 1, 2, 4:** Detect if inside a worktree and remove it:
```bash
# Detect worktree: if git-common-dir differs from git-dir, we are in a worktree
COMMON_DIR=$(git rev-parse --git-common-dir 2>/dev/null)
GIT_DIR=$(git rev-parse --git-dir 2>/dev/null)
if [ "$COMMON_DIR" != "$GIT_DIR" ]; then
  WORKTREE_PATH=$(pwd)
  cd $(git -C "$COMMON_DIR/.." rev-parse --show-toplevel)
  git worktree remove "$WORKTREE_PATH"
fi
```

**Option 3:** Do NOT clean up. The worktree stays.

### Step 6: Cleanup Temporary Plan Files

If the feature's plan was stored in `.code-forge/tmp/` (created with `--tmp`):

1. After successful merge (Option 1) or PR creation (Option 2) or discard (Option 4): delete `.code-forge/tmp/{feature_name}/`
2. If `.code-forge/tmp/` is now empty, remove `.code-forge/tmp/`. If `.code-forge/` is also now empty, remove it too.
3. Display: `Cleaned up temporary plan files: .code-forge/tmp/{feature_name}/`

**Option 3 (Keep):** Do NOT clean up — the tmp plan files stay for future `/impl` sessions.

### Completion Report

```
Branch finished:
  Feature:   {feature-name}
  Action:    {Merged / PR created / Kept / Discarded}
  PR URL:    {url} (Option 2 only)
  Worktree:  {removed / preserved}
  Tmp plan:  {cleaned up / preserved} (only shown for --tmp plans)
```

## Example

```
$ /code-forge:finish

Tests: 42/42 passing ✓

How would you like to integrate this branch?
  1. Merge back to main locally
  2. Push and create Pull Request
  3. Keep branch as-is
  4. Discard this work

> 2

Branch finished:
  Feature:   user-auth
  Action:    PR created
  PR URL:    https://github.com/org/repo/pull/47
  Worktree:  removed
```

## Common Mistakes

- Proceeding without verifying tests pass
- Modifying the 4 options (adding, removing, or reordering)
- Cleaning up worktree when user chose "Keep"
- Executing discard without explicit "discard" confirmation
