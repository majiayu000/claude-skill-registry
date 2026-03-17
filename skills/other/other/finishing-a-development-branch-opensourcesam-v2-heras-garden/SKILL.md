---
name: finishing-a-development-branch
description: Use when implementation complete and tests pass - closes bd epic, presents integration options (merge/PR/keep/discard), executes choice
---

<skill_overview>
Close bd epic, verify tests pass, present 4 integration options, execute choice, cleanup worktree appropriately.
</skill_overview>

<rigidity_level>
LOW FREEDOM - Follow the 6-step process exactly. Present exactly 4 options. Never skip test verification. Must confirm before discarding.
</rigidity_level>

<quick_reference>
| Step | Action | If Blocked |
|------|--------|------------|
| 1 | Close bd epic | Tasks still open → STOP |
| 2 | Verify tests pass (test-runner agent) | Tests fail → STOP |
| 3 | Determine base branch | Ask if needed |
| 4 | Present exactly 4 options | Wait for choice |
| 5 | Execute choice | Follow option workflow |
| 6 | Cleanup worktree (options 1,2,4 only) | Option 3 keeps worktree |

**Options:** 1=Merge locally, 2=PR, 3=Keep as-is, 4=Discard (confirm)
</quick_reference>

<when_to_use>
- Implementation complete and reviewed
- All bd tasks for epic are done
- Ready to integrate work back to main branch
- Called by hyperpowers:review-implementation (final step)

**Don't use for:**
- Work still in progress
- Tests failing
- Epic has open tasks
- Mid-implementation (use hyperpowers:executing-plans)
</when_to_use>

<the_process>
## Step 1: Close bd Epic

**Announce:** "I'm using hyperpowers:finishing-a-development-branch to complete this work."

**Verify all tasks closed:**

```bash
bd dep tree bd-1  # Show task tree
bd list --status open --parent bd-1  # Check for open tasks
```

**If any tasks still open:**
```
Cannot close epic bd-1: N tasks still open:
- bd-3: Task Name (status: in_progress)
- bd-5: Task Name (status: open)

Complete all tasks before finishing.
```

**STOP. Do not proceed.**

**If all tasks closed:**

```bash
bd close bd-1
```

---

## Step 2: Verify Tests

**IMPORTANT:** Use hyperpowers:test-runner agent to avoid context pollution.

Dispatch hyperpowers:test-runner agent:
```
Run: cargo test
(or: npm test / pytest / go test ./...)
```

Agent returns summary + failures only.

**If tests fail:**
```
Tests failing (N failures). Must fix before completing:

[Show failures]

Cannot proceed until tests pass.
```

**STOP. Do not proceed.**

**If tests pass:** Continue to Step 3.

---

## Step 3: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

---

## Step 4: Present Options

Present exactly these 4 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation.** Keep concise.

---

## Step 5: Execute Choice

### Option 1: Merge Locally

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify tests on merged result
Dispatch hyperpowers:test-runner: "Run: <test command>"

# If tests pass
git branch -d <feature-branch>
```

Then: Step 6 (cleanup worktree)

---

### Option 2: Push and Create PR

**Get epic info:**

```bash
bd show bd-1
bd dep tree bd-1
```

**Create PR:**

```bash
git push -u origin <feature-branch>

gh pr create --title "feat: <epic-name>" --body "$(cat <<'EOF'
## Epic

Closes bd-<N>: <Epic Title>

## Summary
<2-3 bullets from epic implementation>

## Tasks Completed
- bd-2: <Task Name>
- bd-3: <Task Name>

## Test Plan
- [ ] All tests passing
- [ ] <verification steps from epic>
EOF
)"
```

Then: Step 6 (cleanup worktree)

---

### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

---

### Option 4: Discard

**Confirm first:**

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact "discard" confirmation.

**If confirmed:**

```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: Step 6 (cleanup worktree)

---

## Step 6: Cleanup Worktree

**For Options 1, 2, 4 only:**

```bash
# Check if in worktree
git worktree list | grep $(git branch --show-current)

# If yes
git worktree remove <worktree-path>
```

**For Option 3:** Keep worktree (don't cleanup).
</the_process>

<examples>
<example>
<scenario>Developer skips test verification before presenting options</scenario>

<code>
# Step 1: Epic closed ✓
bd close bd-1

# Step 2: SKIPPED test verification
# Jump directly to presenting options

"Implementation complete. What would you like to do?
1. Merge back to main locally
2. Push and create PR
..."

User selects Option 1

git checkout main
git merge feature-branch
# Tests fail! Broken code now on main
</code>

<why_it_fails>
- Skipped mandatory test verification
- Merged broken code to main branch
- Other developers pull broken main
- CI/CD fails, blocks deployment
- Must revert, fix, merge again (wasted time)
</why_it_fails>

<correction>
**Follow Step 2 strictly:**

```bash
# After closing epic
bd close bd-1 ✓

# MANDATORY: Verify tests BEFORE presenting options
Dispatch hyperpowers:test-runner agent: "Run: cargo test"

# Agent reports
"Test suite passed (127 tests, 0 failures, 2.3s)"

# NOW present options
"Implementation complete. What would you like to do?
1. Merge back to main locally
..."
```

**What you gain:**
- Confidence tests pass before integration
- No broken code merged to main
- CI/CD stays green
- Other developers unblocked
- Professional workflow
</correction>
</example>

<example>
<scenario>Developer auto-cleans worktree for PR option</scenario>

<code>
# User selects Option 2: Create PR
git push -u origin feature-auth
gh pr create --title "feat: Add OAuth" --body "..."

# Developer immediately cleans up worktree
git worktree remove ../feature-auth-worktree

# PR gets feedback: "Please add rate limiting"
# User: "Can you address the PR feedback?"
# Worktree is gone! Have to recreate it
git worktree add ../feature-auth-worktree feature-auth
# Lost local state, uncommitted experiments, etc.
</code>

<why_it_fails>
- Cleaned worktree when PR still active
- User likely needs worktree for PR feedback
- Have to recreate worktree for changes
- Lost any local uncommitted work
- Inefficient workflow
</why_it_fails>

<correction>
**Option 2 workflow (correct):**

```bash
git push -u origin feature-auth
gh pr create --title "feat: Add OAuth" --body "..."

# Report PR created
"Pull request created: https://github.com/user/repo/pull/42

Keeping worktree at ../feature-auth-worktree for PR updates."

# NO worktree cleanup
# User can address PR feedback in same worktree
```

**Cleanup happens later when:**
- PR is merged
- User explicitly requests cleanup
- User uses finishing-a-development-branch again after PR merges

**What you gain:**
- Worktree available for PR feedback
- No need to recreate worktree
- Preserve local state and experiments
- Efficient PR iteration workflow
</correction>
</example>

<example>
<scenario>Developer discards work without confirmation</scenario>

<code>
# User says: "Actually, discard this work"

# Developer immediately executes
git checkout main
git branch -D feature-experimental
git worktree remove ../feature-experimental-worktree

# 50 commits deleted
# User: "Wait, I meant discard the LAST commit, not the whole branch!"
# Too late - work is gone
</code>

<why_it_fails>
- No confirmation before destructive action
- Misunderstood user intent
- Permanent data loss
- No way to recover work
- Catastrophic for user
</why_it_fails>

<correction>
**Option 4 workflow (correct):**

```
User: "Discard this work"

"This will permanently delete:
- Branch feature-experimental
- All commits:
  * a1b2c3d Add OAuth integration
  * d4e5f6g Add rate limiting
  * g7h8i9j Update tests
  ... (47 more commits)
- Worktree at ../feature-experimental-worktree

Type 'discard' to confirm."

# WAIT for exact confirmation
User types: "discard"

# NOW execute
git checkout main
git branch -D feature-experimental
git worktree remove ../feature-experimental-worktree

"Branch feature-experimental deleted."
```

**What you gain:**
- User sees exactly what will be deleted
- Explicit confirmation required
- Prevents accidental data loss
- Time to reconsider or clarify
- Safe destructive operations
</correction>
</example>
</examples>

<option_matrix>
| Option | Merge | Push | Keep Worktree | Cleanup Branch | Cleanup Worktree |
|--------|-------|------|---------------|----------------|------------------|
| 1. Merge locally | ✓ | - | - | ✓ | ✓ |
| 2. Create PR | - | ✓ | ✓ | - | - |
| 3. Keep as-is | - | - | ✓ | - | - |
| 4. Discard | - | - | - | ✓ (force) | ✓ |
</option_matrix>

<critical_rules>
## Rules That Have No Exceptions

1. **Never skip test verification** → Tests must pass before presenting options
2. **Present exactly 4 options** → No open-ended questions
3. **Require confirmation for Option 4** → Type "discard" exactly
4. **Keep worktree for Options 2 & 3** → PR and keep-as-is need worktree
5. **Verify tests after merge (Option 1)** → Merged result might break

## Common Excuses

All of these mean: **STOP. Follow the process.**

- "Tests passed earlier, don't need to verify" (Might have changed, verify now)
- "User knows what they want" (Present options, let them choose)
- "Obvious they want to discard" (Require explicit confirmation)
- "PR done, cleanup worktree" (PR likely needs updates, keep worktree)
- "Too many options" (Exactly 4, no more, no less)
</critical_rules>

<verification_checklist>
Before completing:

- [ ] bd epic closed (all child tasks closed)
- [ ] Tests verified passing (via test-runner agent)
- [ ] Presented exactly 4 options (no open-ended questions)
- [ ] Waited for user choice (didn't assume)
- [ ] If Option 4: Got typed "discard" confirmation
- [ ] Worktree cleaned for Options 1, 4 only (not 2, 3)
- [ ] If Option 1: Verified tests on merged result

**Can't check all boxes?** Return to process and complete missing steps.
</verification_checklist>

<integration>
**This skill is called by:**
- hyperpowers:review-implementation (final step after approval)

**Call chain:**
```
hyperpowers:executing-plans → hyperpowers:review-implementation → hyperpowers:finishing-a-development-branch
                         ↓
                   (if gaps found: STOP)
```

**This skill calls:**
- hyperpowers:test-runner agent (for test verification)
- bd commands (epic management)
- gh commands (PR creation)

**CRITICAL:** Never read `.beads/issues.jsonl` directly. Always use bd CLI commands.
</integration>

<resources>
**Detailed guides:**
- [Git worktree management](resources/worktree-guide.md)
- [PR description templates](resources/pr-templates.md)
- [bd epic reference in PRs](resources/bd-pr-integration.md)

**When stuck:**
- Tasks won't close → Check bd status, verify all child tasks done
- Tests fail → Fix before presenting options (can't proceed)
- User unsure → Explain options, but don't make choice for them
- Worktree won't remove → Might have uncommitted changes, ask user
</resources>
