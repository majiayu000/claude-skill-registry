---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project's test suite
make test / npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 3: Detect Spool Change

Check if working on a spool change:

```bash
# Check for in-progress spool changes
ls .spool/changes/ 2>/dev/null | head -5
```

**If spool change detected:** Include Option 5 (Archive) in the options.

### Step 4: Present Options

Present the options (5 if spool change detected, otherwise 4):

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work
5. Archive spool change (integrates specs, marks complete)  ← if spool change

Which option?
```

**If spool change detected:** Highlight option 5: "Recommended for spool changes: archives completed work into specs."

**Don't add explanation** - keep options concise.

### Step 5: Execute Choice

#### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>

# If tests pass
git branch -d <feature-branch>
```

Then: Cleanup worktree (Step 6)

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Then: Cleanup worktree (Step 6)

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 6)

#### Option 5: Archive Spool Change (if spool change detected)

Invoke the `spool-archive` skill:

```bash
spool agent instruction archive --change <change-id>
```

Follow the printed instructions to:
- Integrate change specs into main specs
- Mark change as completed
- Clean up change directory

Then: Cleanup worktree (Step 6)

### Step 6: Cleanup Worktree

**For Options 1, 2, 4, 5:**

Check if in worktree:
```bash
git worktree list | grep $(git branch --show-current)
```

If yes:
```bash
git worktree remove <worktree-path>
```

**For Option 3:** Keep worktree.

## Quick Reference

| Option | Merge | Push | Archive | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | - | ✓ |
| 2. Create PR | - | ✓ | - | ✓ | - |
| 3. Keep as-is | - | - | - | ✓ | - |
| 4. Discard | - | - | - | - | ✓ (force) |
| 5. Archive spool | - | - | ✓ | - | ✓ |

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" → ambiguous
- **Fix:** Present structured options

**Automatic worktree cleanup**
- **Problem:** Remove worktree when might need it (Option 2, 3)
- **Fix:** Only cleanup for Options 1, 4, and 5

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

**Missing archive option for spool**
- **Problem:** User forgets to archive completed spool changes
- **Fix:** Detect spool changes and present archive option

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request

**Always:**
- Verify tests before offering options
- Detect spool changes and include archive option
- Present structured options (not open-ended)
- Get typed confirmation for Option 4
- Clean up worktree for Options 1, 4, 5 only

## Integration

**Called by:**
- **spool-subagent-driven-development** (after all tasks complete)
- **spool-apply-change-proposal** (after all batches complete)

**Pairs with:**
- **spool-using-git-worktrees** - Cleans up worktree created by that skill
- **spool-archive** - Used by Option 5 to archive spool changes
