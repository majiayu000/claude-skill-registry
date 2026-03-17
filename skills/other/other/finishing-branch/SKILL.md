---
name: finishing-branch
model: fast
description: Complete development work by presenting structured options for merge, PR, or cleanup. Use when implementation is complete, all tests pass, and you need to decide how to integrate work. Triggers on finish branch, complete branch, merge branch, create PR, done with feature, implementation complete.
---

# Finishing a Development Branch

Complete development work by presenting clear options and executing the chosen workflow.

## WHAT This Skill Does

After implementation is complete, guides you through verifying tests, presenting integration options, and executing the chosen path (merge, PR, keep, or discard).

## WHEN To Use

- Implementation is complete
- All tests pass
- Ready to integrate work into the main branch

**KEYWORDS**: finish branch, complete branch, merge, PR, done with feature


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install finishing-branch
```


---

## The Process

### Step 1: Verify Tests

```bash
npm test / cargo test / pytest / go test ./...
```

**If tests fail:** Stop. Cannot proceed until tests pass.

```
Tests failing (N failures). Must fix before completing:
[Show failures]
```

**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or confirm: "This branch split from main - is that correct?"

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
<run tests again>
git branch -d <feature-branch>
```

Then: Cleanup worktree (Step 5)

#### Option 2: Push and Create PR

```bash
git push -u origin <feature-branch>

gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Then: Cleanup worktree (Step 5)

#### Option 3: Keep As-Is

Report: "Keeping branch `<name>`. Worktree preserved at `<path>`."

**Do NOT cleanup worktree.**

#### Option 4: Discard

**Confirm first:**

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation. If confirmed:

```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 5)

### Step 5: Cleanup Worktree

**For Options 1, 2, 4 only:**

```bash
# Check if in worktree
git worktree list | grep $(git branch --show-current)

# If yes:
git worktree remove <worktree-path>
```

**For Option 3:** Keep worktree.

---

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

---

## NEVER

- Proceed with failing tests
- Merge without verifying tests on the result
- Delete work without typed confirmation ("discard")
- Force-push without explicit request
- Skip presenting all 4 options
- Automatically cleanup worktree for Options 2 or 3
- Ask open-ended "What should I do next?" (use structured options)

---

## Integration

**Called by:**
- `subagent-development` (after all tasks complete)
- `executing-plans` (after all batches complete)

**Pairs with:**
- `git-worktrees` - Cleans up worktree created by that skill
