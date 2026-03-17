---
name: finishing-a-development-branch
description: "Use when implementation is complete, all tests pass, and you need to decide how to integrate the work"
---

# Finishing a Development Branch

<ROLE>
Release Engineer. Your reputation depends on clean integrations that never break main or lose work. A merge that breaks the build is a public failure. A discard without confirmation is unforgivable.
</ROLE>

**Announce:** "Using finishing-a-development-branch skill to complete this work."

## Invariant Principles

1. **Tests Gate Everything** - Never present options until tests pass. Never merge without verifying tests on merged result.
2. **Structured Choice Over Open Questions** - Present exactly 4 options, never "what should I do?"
3. **Destruction Requires Proof** - Option 4 (Discard) demands typed "discard" confirmation. No shortcuts. No excuses.
4. **Worktree Lifecycle Matches Work State** - Cleanup only for Options 1 (merged) and 4 (discarded). Keep for Options 2 (PR pending) and 3 (user will handle).

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Passing test suite | Yes | Tests must pass before this skill can proceed |
| Feature branch | Yes | Current branch with completed implementation |
| Base branch | No | Branch to merge into (auto-detected if unset) |
| `post_impl` setting | No | Autonomous mode directive (auto_pr, offer_options, stop) |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Integration result | Action | Merge, PR, preserved branch, or discarded branch |
| PR URL | Inline | GitHub PR URL (Option 2 only) |
| Worktree state | State | Removed (Options 1,4) or preserved (Options 2,3) |

---

## Autonomous Mode

Check your context for autonomous mode indicators:
- "Mode: AUTONOMOUS" or "autonomous mode"
- `post_impl` preference specified (e.g., "auto_pr", "offer_options", "stop")

| `post_impl` value | Behavior |
|-------------------|----------|
| `auto_pr` | Skip Step 3 (present options), go directly to Option 2 (Push and Create PR) |
| `offer_options` | Present options normally (this is the interactive fallback) |
| `stop` | Skip Step 3, just report completion without action |
| (unset in autonomous) | Default to Option 2 - safest autonomous choice. Document: "Autonomous mode: defaulting to PR creation" |

<CRITICAL>
**Circuit breakers (always pause):**
- Tests failing - NEVER proceed
- Option 4 (Discard) selected - ALWAYS require typed confirmation, never auto-execute
</CRITICAL>

---

## Branch-Relative Documentation

<CRITICAL>
Changelogs, PR titles, PR descriptions, commit messages, and code comments describe the delta between the current branch HEAD and the merge base with the target branch. **Nothing else exists.**
</CRITICAL>

The only reality is `git diff $(git merge-base HEAD <target>)...HEAD`. If it's not in that diff, it didn't happen.

**Required behavior:**

- When writing or updating changelogs, PR descriptions, or PR titles, always derive content from the merge base diff at the moment of writing. Treat the branch as if it materialized in its current form all at once.
- When HEAD changes (new commits, rebases, amends), re-evaluate all of the above against the current merge base. Actively delete and rewrite stale entries from prior iterations.
- Never accumulate changelog entries session-by-session. A changelog is not a development diary.

**Code comments must never be historical narratives:**

- No "changed from X to Y", "previously did Z", "refactored from old approach", "CRITICAL FIX: now does X instead of Y".
- If the comment references something that only existed in a prior iteration of the branch and is not on the target branch, it describes fiction. Delete it.
- Comments that are only meaningful to someone who read a prior version of the branch are wrong. **Test: "Does this comment make sense to someone reading the code for the first time, with no knowledge of any prior implementation?"** If no, delete it.
- Comments describe the present. Git describes the past.

**The rare exception:** A comment may reference external historical facts that explain non-obvious constraints (e.g., "SQLite < 3.35 doesn't support RETURNING"). Even then, reframe as a present-tense constraint, not a narrative of change.

---

## The Process

### Step 1: Verify Tests

<analysis>
Before presenting options:
- Do tests pass on current branch?
- What is the base branch?
- Am I in a worktree?
</analysis>

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

STOP. Do not proceed to Step 2.

**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

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

**Don't add explanation** - keep options concise.

### Step 4: Execute Choice

**Dispatch subagent** with command: `finish-branch-execute`

Provide context: chosen option number, feature branch name, base branch name, worktree path (if applicable).

### Step 5: Cleanup Worktree

**Dispatch subagent** with command: `finish-branch-cleanup`

Provide context: chosen option number, worktree path. Note: Option 3 skips cleanup entirely.

---

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | Yes | - | - | Yes |
| 2. Create PR | - | Yes | Yes | - |
| 3. Keep as-is | - | - | Yes | - |
| 4. Discard | - | - | - | Yes (force) |

---

## Anti-Patterns

<FORBIDDEN>
- Proceeding with failing tests
- Merging without post-merge test verification
- Deleting branches without typed "discard" confirmation
- Force-pushing without explicit user request
- Presenting open-ended questions instead of structured options
- Cleaning up worktrees for Options 2 or 3
- Accepting partial confirmation for Option 4
</FORBIDDEN>

---

## Self-Check

<reflection>
Before completing:
- [ ] Tests pass on current branch
- [ ] Tests pass after merge (Option 1 only)
- [ ] User explicitly selected one of the 4 options
- [ ] Typed "discard" received (Option 4 only)
- [ ] Worktree cleaned only for Options 1 or 4

IF ANY unchecked: STOP and fix.
</reflection>

---

## Integration

**Called by:**
- **executing-plans** (Step 5) - After all batches complete
- **executing-plans --mode subagent** (Step 7) - After all tasks complete in subagent mode

**Pairs with:**
- **using-git-worktrees** - Cleans up worktree created by that skill
