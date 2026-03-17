---
name: finishing-a-development-branch
description: Git branch completion workflow. Use when implementation is complete, tests pass, and a feature branch needs to be integrated via merge, pull request, or cleanup.
---

# Finishing a Development Branch

## The Process

### Step 1: Verify Tests

Determine test runner from project structure:
- `package.json` → `npm test` or `yarn test`
- `Cargo.toml` → `cargo test`
- `pyproject.toml` / `setup.py` → `pytest`
- `go.mod` → `go test ./...`
- `Makefile` with `test` target → `make test`

Run tests. If any fail, report `⊘ BLOCKED:TESTS` with failure count and stop. Do not proceed to Step 2.

### Step 2: Determine Base Branch

Find the branch this feature diverged from:

```bash
# Check which branch has the closest merge-base
for candidate in main master develop; do
  if git rev-parse --verify "$candidate" >/dev/null 2>&1; then
    MERGE_BASE=$(git merge-base HEAD "$candidate" 2>/dev/null)
    if [ -n "$MERGE_BASE" ]; then
      echo "Candidate: $candidate (merge-base: $MERGE_BASE)"
    fi
  fi
done
```

Select the candidate with the most recent merge-base (closest ancestor). If multiple branches share the same merge-base or detection is ambiguous, ask: "This branch could target `main` or `develop`. Which should it merge into?"

**Store the result** - subsequent steps reference `<base-branch>` meaning this determined value.

### Step 3: Present Options

Present exactly these 4 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

### Step 4: Execute Choice

#### Option 1: Merge Locally

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
```

**If merge conflicts:**
```
⊘ BLOCKED:CONFLICTS

Merge conflicts in:
- <conflicted files>

Cannot auto-resolve. User must:
1. Resolve conflicts manually
2. Run tests
3. Re-run this workflow
```
Stop. Do not proceed.

**If merge succeeds:**
```bash
# Verify tests on merged result
<test command>

# If tests pass, delete feature branch
git branch -d <feature-branch>
```

Then: Cleanup worktree (Step 5). Report `✓ MERGED`.

#### Option 2: Push and Create PR

**Verify `gh` CLI is available:**
```bash
if ! command -v gh &>/dev/null; then
  echo "gh CLI not installed. Install from https://cli.github.com/ or push manually and create PR via web."
  exit 1
fi
gh auth status || echo "gh not authenticated. Run: gh auth login"
```

Extract title from first commit on branch (original intent):

```bash
MERGE_BASE=$(git merge-base HEAD <base-branch>)
TITLE=$(git log --reverse --format=%s "$MERGE_BASE"..HEAD | head -1)
git push -u origin <feature-branch>
gh pr create --title "$TITLE" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Report `✓ PR_CREATED` with PR URL. **Keep worktree intact** for continued work during review.

#### Option 3: Keep As-Is

Report `✓ PRESERVED` with branch name and worktree path.

**Do not cleanup worktree.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation. If not received, abort.

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 5). Report `✓ DISCARDED`.

### Step 5: Cleanup Worktree

**For Options 1 and 4 only:**

```bash
# Check if currently in a worktree (not main repo)
if [ "$(git rev-parse --git-common-dir)" != "$(git rev-parse --git-dir)" ]; then
  # Get worktree root (handles invocation from subdirectory)
  WORKTREE_ROOT=$(git rev-parse --show-toplevel)
  cd "$(git rev-parse --git-common-dir)/.."
  git worktree remove "$WORKTREE_ROOT"
fi
```

**For Options 2 and 3:** Keep worktree intact.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

## Terminal States

On completion, report exactly one:

| State | Output | Meaning |
|-------|--------|---------|
| `✓ MERGED` | Branch merged to `<base>`, worktree cleaned | Option 1 success |
| `✓ PR_CREATED` | PR #N at URL | Option 2 success |
| `✓ PRESERVED` | Branch kept at path | Option 3 success |
| `✓ DISCARDED` | Branch deleted, worktree cleaned | Option 4 success |
| `⊘ BLOCKED:TESTS` | N test failures | Cannot proceed |
| `⊘ BLOCKED:CONFLICTS` | Merge conflict in files | Cannot proceed |

## Guardrails

**Blocking conditions (stop immediately):**
- Tests failing → `⊘ BLOCKED:TESTS`
- Merge conflicts → `⊘ BLOCKED:CONFLICTS`

**Mandatory confirmations:**
- Option 4 (Discard): Require typed "discard" confirmation

**Cleanup rules:**
- Options 1, 4: Clean up worktree and branch
- Options 2, 3: Preserve worktree

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without typed confirmation
- Force-push without explicit request

## Integration

**Called by:**
- **subagent-driven-development** (Step 7) - After all tasks complete
- **executing-plans** (Step 5) - After all batches complete

**Pairs with:**
- **using-git-worktrees** - Cleans up worktree created by that skill
