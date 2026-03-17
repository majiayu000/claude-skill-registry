---
name: superspec:finish-branch
description: |
  Use when implementation is complete, all tests pass, and you need to integrate the work.
  Guides completion by presenting structured options for merge, PR, or cleanup.
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finish-branch skill to complete this work."

## When to Use

- After `/superspec:verify` passes
- After all tasks in plan are complete
- Before archiving the change

## Prerequisites

- [ ] All tests pass
- [ ] `superspec verify [change-id]` passes
- [ ] Final code review approved

## The Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    Finish Branch Flow                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   1. Verify Tests                                                 │
│      └─→ All tests must pass                                     │
│      └─→ superspec verify must pass                              │
│                                                                   │
│   2. Determine Base Branch                                        │
│      └─→ Usually main or master                                  │
│                                                                   │
│   3. Present Options                                              │
│      └─→ 4 structured choices                                    │
│                                                                   │
│   4. Execute Choice                                               │
│      └─→ Merge / PR / Keep / Discard                             │
│                                                                   │
│   5. Cleanup Worktree (if applicable)                            │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Step 1: Verify Tests

**Before presenting options:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...

# Run SuperSpec verification
superspec verify [change-id]
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 2.

## Step 2: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

## Step 3: Present Options

Present exactly these 4 options:

```
Implementation complete. Verification passed. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

## Step 4: Execute Choice

### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge feature/<change-id>

# Verify tests on merged result
<test command>

# If tests pass
git branch -d feature/<change-id>
```

**Then:** Cleanup worktree (Step 5) → Archive change

### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin feature/<change-id>

# Create PR with SuperSpec reference
gh pr create --title "feat(<capability>): <description>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## SuperSpec Reference
- Change: `superspec/changes/<change-id>/`
- Specs: `superspec/changes/<change-id>/specs/`

## Test Plan
- [ ] All tests pass
- [ ] `superspec verify <change-id>` passes
- [ ] Code review approved

## Verification
- Requirements: X/X implemented
- Scenarios: Y/Y tested
EOF
)"
```

**Then:** Cleanup worktree (Step 5) - branch stays for PR

### Option 3: Keep As-Is

Report: "Keeping branch feature/<change-id>. Worktree preserved at <path>."

**Don't cleanup worktree.**

### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch feature/<change-id>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
git checkout <base-branch>
git branch -D feature/<change-id>
```

Then: Cleanup worktree (Step 5)

## Step 5: Cleanup Worktree

**For Options 1, 2, 4:**

Check if in worktree:
```bash
git worktree list | grep feature/<change-id>
```

If yes:
```bash
# Navigate out of worktree first
cd <project-root>

# Remove worktree
git worktree remove .worktrees/<change-id>
```

**For Option 3:** Keep worktree.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | - | Keep for PR |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

## After Finishing

**Next steps:**

For Options 1 & 2 (code integrated):
```
Branch finished. Next: /superspec:archive to complete the change.
```

For Option 3:
```
Branch preserved. Run /superspec:finish-branch again when ready.
```

For Option 4:
```
Work discarded. Consider deleting superspec/changes/<change-id>/ if not needed.
```

## Red Flags

**Never:**
- Proceed with failing tests
- Proceed without verification passing
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request

**Always:**
- Verify tests before offering options
- Verify `superspec verify` passes
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only

## Integration

**Called by:**
- `subagent-development` - After final review passes
- After `verify` passes

**Pairs with:**
- `git-worktree` - Cleans up worktree created by that skill
- `archive` - Archive change after branch finished
- `verification-before-completion` - Evidence before claims

**Must use:**
- `verification-before-completion` - Before presenting completion options, verify fresh test results exist
