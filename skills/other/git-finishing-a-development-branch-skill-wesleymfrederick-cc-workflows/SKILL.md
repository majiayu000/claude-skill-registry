---
name: git-finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the git-finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Check Dirty State and Commit

**Check for unstaged/uncommitted changes:**

```bash
git status --porcelain
```

**If dirty (has unstaged/uncommitted changes):**

```bash
# Stage all changes
git add .

# Create final commit
git commit -m "feat: final changes before merge

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**If clean:** Continue to Step 2.

### Step 2: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**

```text
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 3.

**If tests pass:** Continue to Step 3.

### Step 3: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 4: Present Options

Present exactly these 4 options:

```text
Implementation complete. What would you like to do?

1. Merge back to {{base-branch}} locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 5: Execute Choice

#### Option 1: Merge Locally

```bash
# Switch to base branch (typically feature branch)
git checkout {{base-branch}}

# Pull latest
git pull

# Merge worktree branch (regular merge, NOT squash)
git merge {{worktree-branch}}

# Verify tests on merged result
{{test-command}}

# If tests pass
git branch -d {{worktree-branch}}
```

**Note:** This is a regular merge (NOT squash) because you're merging worktree → feature branch. Use `merging-feature-branches-to-main` skill later to squash merge feature branch → main after human review.

Then: Cleanup worktree (Step 6)

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin {{feature-branch}}

# Create PR
gh pr create --title "{{title}}" --body "$(cat <<'EOF'
## Summary
{{summary-bullets}}

## Test Plan
- [ ] {{test-steps}}
EOF
)"
```

Then: Cleanup worktree (Step 6)

#### Option 3: Keep As-Is

Report: "Keeping branch {{branch-name}}. Worktree preserved at {{worktree-path}}."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**

```text
This will permanently delete:
- Branch {{branch-name}}
- All commits: {{commit-list}}
- Worktree at {{worktree-path}}

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:

```bash
git checkout {{base-branch}}
git branch -d {{feature-branch}}
```

**If deletion fails (branch not merged):**

```text
❌ Branch {{feature-branch}} is not fully merged.
Use 'git branch -D {{feature-branch}}' to force delete if you're certain.

Confirm force delete? (yes/no)
```

Then: Cleanup worktree (Step 6)

### Step 6: Cleanup Worktree

**For Options 1, 2, 4:**

Check if in worktree:

```bash
git worktree list | grep $(git branch --show-current)
```

If yes, try to remove:

```bash
git worktree remove {{worktree-path}}
```

**If removal fails due to dirty state:**

Report error and stop. **NEVER use --force to delete dirty worktrees.**

```text
❌ Cannot remove worktree - contains uncommitted changes
Worktree path: {{path}}
Branch: {{branch-name}}

This indicates uncommitted work was not properly saved.
Please investigate manually before removing.
```

**For Option 3:** Keep worktree.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (safe delete, confirm if force needed) |

## Common Mistakes

### Skipping test verification

- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

### Open-ended questions

- **Problem:** "What should I do next?" → ambiguous
- **Fix:** Present exactly 4 structured options

### Automatic worktree cleanup

- **Problem:** Remove worktree when might need it (Option 2, 3)
- **Fix:** Only cleanup for Options 1 and 4

### No confirmation for discard

- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request
- Use --force to remove dirty worktrees
- Skip committing unstaged changes before merge

**Always:**
- Check for and commit dirty state in Step 1
- Verify tests before offering options
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only
- Stop if worktree removal fails (indicates uncommitted work)

## Integration

**Called by:**
- **subagent-driven-development** (Step 7) - After all tasks complete
- **executing-plans** (Step 5) - After all batches complete

**Pairs with:**
- **git-using-worktrees** - Cleans up worktree created by that skill
