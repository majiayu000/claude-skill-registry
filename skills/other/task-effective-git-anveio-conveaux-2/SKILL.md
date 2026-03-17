---
name: task-effective-git
description: Git workflow patterns for agents. Invoke at session start when working in a git repository, before any git operations (status, add, commit, push, rebase), when making code changes, or when the user asks to commit, create PRs, or manage branches. Covers atomic commits, intentional staging, history restructuring, and safe parallel work patterns.
---

# Effective Git for Agents

Git is our shared notebook and alarm system. Treat every command as communication to teammates and future you: explain the why, isolate the what, and leave a trail that is easy to audit.

## Cardinal Rules: Protect Others' Work

**NEVER discard, stash, or revert changes you don't recognize.** Another agent or the user may have made them.

### Forbidden Commands (unless explicitly instructed by user)

| Command | Why Forbidden |
|---------|---------------|
| `git stash` | Hides uncommitted work - may lose parallel agent's changes |
| `git checkout -- <file>` | Discards uncommitted changes permanently |
| `git restore <file>` | Same as above - destroys working changes |
| `git reset --hard` | Nuclear option - destroys ALL uncommitted work |
| `git clean -fd` | Removes untracked files - may delete new work |

### When You See Unrecognized Changes

**Default action: LEAVE THEM ALONE.**

```
Unrecognized change in git status
    │
    ├─► Is this blocking your current task?
    │       │
    │       ├─► NO → LEAVE IT ALONE. Continue your work.
    │       │
    │       └─► YES → ASK THE USER what to do. Never discard silently.
    │
    └─► Even if it looks wrong, preserve it.
        Lost work is worse than messy state.
```

### Safe Alternatives

Instead of discarding:
- **Commit it**: `git add -A && git commit -m "WIP: checkpoint unrecognized changes"`
- **Branch it**: `git checkout -b preserve-unknown-changes`
- **Leave it**: Just work around it - uncommitted changes won't affect your commits if you stage selectively

### Why This Matters

Multiple agents may work in the same session. Stashing or reverting "unknown" changes can destroy hours of work. The reflog won't help if changes were never committed. **When in doubt, preserve.**

## Core Principles

- **One idea per commit**: Each commit carries one idea and a reason; unrelated threads belong in separate commits.
- **Keep history safe**: Prefer additive fixes (`git revert`) over destructive rewrites (`git reset --hard`), and avoid editing others' changes.
- **Build and test**: The final commit series should pass verification; intermediate WIP commits are checkpoints, not deliverables.
- **Topic branches**: Work in small steps on a topic branch; keep main clean for integration.

## Two-Phase Development

Development happens in two phases: speed first, clarity second.

### Phase 1: Develop (Speed)

During implementation, commit checkpoints freely:

```bash
git commit -m "WIP: rough implementation"
git commit -m "WIP: fix that thing"
git commit -m "WIP: cleanup"
```

These are throwaway commits for safety, not communication. Don't waste time crafting messages—focus on making it work.

**Rules for Phase 1:**
- Commit frequently (every 15-30 minutes of work)
- Use "WIP:" prefix to mark throwaway commits
- Don't worry about atomic boundaries yet
- Verification not required on every commit

### Phase 2: Restructure (Clarity)

Before creating a PR, restructure into atomic commits:

```bash
# 1. Start interactive rebase against main
git rebase -i main

# 2. Squash WIP commits, split large commits, reorder for logical flow
# 3. Write meaningful messages for each atomic commit
# 4. Verify the final state
./verify.sh --agent
```

The final history tells a story a reviewer can follow.

**Rules for Phase 2:**
- Each commit tells one story
- Final commit series must pass verification
- Review your own history: `git log --oneline main..HEAD`

## The Atomic Commit Standard

### What Makes a Commit Atomic?

- **One logical change**: Add a function, fix a bug, refactor a module
- **Reviewable**: Can be understood in 5-10 minutes
- **Revertable**: Can be reverted without side effects
- **Self-contained**: Doesn't depend on "the next commit to fix it"

### Size Guidance

| Commit Type | Typical Lines | Example |
|-------------|---------------|---------|
| Typo/config | 1-10 | "Fix typo in README" |
| Bug fix | 5-50 | "Handle null case in parser" |
| Refactor | 20-100 | "Extract validation to helper" |
| New function | 30-150 | "Add createUser endpoint" |
| Large feature | Split into above | N/A - restructure it |

### Bad vs Good Examples

**Bad** (sweeping commit):
```
Add user authentication

- Add User model
- Add auth middleware
- Add login endpoint
- Add logout endpoint
- Add session management
- Fix typo in unrelated file
- Update tests
```

**Good** (atomic series):
```
1. Add User model with validation
2. Add session management utilities
3. Add auth middleware
4. Add login endpoint
5. Add logout endpoint
6. Add auth integration tests
```

Each commit in the good example can be reviewed independently, reverted if needed, and tells a clear story.

## Interactive Rebase

Interactive rebase is your primary tool for restructuring history.

### When to Use

| Scenario | Safe to Rewrite? |
|----------|------------------|
| Your feature branch before PR | ✅ YES |
| Local commits not yet pushed | ✅ YES |
| After `git commit --amend` (if not pushed) | ✅ YES |
| Anything on `main` | ❌ NO |
| Commits others are working on | ❌ NO |
| After PR is merged | ❌ NO |

### The Restructuring Workflow

```bash
# 1. Start interactive rebase against main
git rebase -i main

# 2. Editor opens with commit list - modify as needed
# 3. Save and close - git applies changes
# 4. Resolve any conflicts
# 5. Verify final state
./verify.sh --agent
```

### Rebase Commands

| Command | Effect | Use When |
|---------|--------|----------|
| `pick` | Keep commit as-is | Default, commit is good |
| `reword` | Keep commit, edit message | Message needs improvement |
| `edit` | Stop at commit | Need to split or modify content |
| `squash` | Combine with previous | Merge related commits, keep both messages |
| `fixup` | Combine with previous | Merge commits, drop this message |
| `drop` | Delete commit | Remove WIP or mistake |

### Example: Restructuring WIP Commits

Before (commit list in editor):
```
pick a1b2c3d WIP: start auth
pick e4f5g6h WIP: more auth stuff
pick i7j8k9l WIP: fix tests
pick m0n1o2p WIP: cleanup
```

After (restructured):
```
pick a1b2c3d WIP: start auth
squash e4f5g6h WIP: more auth stuff
squash i7j8k9l WIP: fix tests
squash m0n1o2p WIP: cleanup
```

Result: One clean commit with combined changes. Git will prompt you to reword the message.

## Splitting a Commit

When a commit contains multiple logical changes, split it during rebase:

### Step-by-Step

```bash
# 1. Start rebase, mark commit to split with 'edit'
git rebase -i main

# 2. When stopped at the commit, undo it but keep changes
git reset HEAD^

# 3. Now all changes are unstaged - stage first logical unit
git add -p  # Select only related hunks

# 4. Commit first unit
git commit -m "Add User model"

# 5. Stage and commit next unit
git add -p
git commit -m "Add auth middleware"

# 6. Continue until all changes committed
git add -p
git commit -m "Add login endpoint"

# 7. Continue the rebase
git rebase --continue
```

### Combining Commits

In the rebase editor, use `fixup` to absorb commits into the previous one:

```
pick a1b2c3d Add User model
fixup e4f5g6h Fix User model typo    # This gets absorbed
fixup i7j8k9l Add missing field      # This too
pick m0n1o2p Add auth middleware
```

## Safe History Rewriting

### The Golden Rule

**Only rewrite commits that haven't been shared.**

### Safe to Rewrite

- Local commits not yet pushed
- Your feature branch before PR creation
- After `git commit --amend` (if not pushed)

### Never Rewrite

- Anything on `main`
- Commits others have based work on
- After PR is merged
- Shared branches with collaborators

### Recovery from Mistakes

If rebase goes wrong:

```bash
# Abort current rebase (restores pre-rebase state)
git rebase --abort

# Or find previous state in reflog
git reflog
git reset --hard HEAD@{n}  # n = steps back to desired state
```

The reflog keeps everything for ~90 days. You can always recover.

### Resolving Divergent Branches After PR Merge

When local main diverges from origin/main after a PR merge (because local had unpushed commits that got squashed into the PR):

```bash
# Discard local unpushed commits and align with merged state
git fetch origin
git reset --hard origin/main
```

This discards the local WIP commits (now redundant since they were squashed into the PR) and aligns with the merged state.

### Recovery When npm install Breaks Types

When vitest types break (e.g., ".not does not exist on Assertion<T>"), the issue is often a package-lock.json mismatch:

```bash
# Restore known-good dependency resolution from main
rm -rf node_modules package-lock.json
git checkout main -- package-lock.json
npm install
```

This restores the dependency resolution that was working on main.

## Working Loop

### During Development (Phase 1)

1. **Learn the current state**: Run `git status` and `git diff HEAD` to see all changes.
2. **Work in checkpoints**: Commit frequently with "WIP:" prefix.
3. **Focus on making it work**: Don't worry about perfect commits yet.

### Before PR (Phase 2)

1. **Restructure history**: `git rebase -i main` to create atomic commits.
2. **Stage intentionally**: Use `git add -p` to build clean commits.
3. **Write meaningful messages**: Each commit explains why, not just what.
4. **Verify**: Run `./verify.sh --agent` on final state.
5. **Review your work**: `git log --oneline main..HEAD` should tell a clear story.

## Stage with Intent

- Use `git add -p` / `git add --patch` to select only the hunks that belong in the current commit.
- If you over-stage, recover with `git restore --staged <file>` or `git reset -p` to push lines back to unstaged.
- For mixed concerns in one file, stage one idea, commit, then stage the next. Do not let unrelated changes hitch a ride.
- Before committing, read the staged diff (`git diff --cached`) as if reviewing someone else's patch.

## Craft Messages That Speak

Structure your commit message with:
- **Subject line**: Imperative, ≤ 72 characters, states the action (e.g., "Add sandbox smoke guardrails").
- **Body** (when needed):
  - **Why**: The problem or goal.
  - **How**: Key decisions or noteworthy implementation notes.
  - **Tests**: Commands run or "Tests: not run (<reason>)".
  - **Follow-ups**: Known gaps, TODOs, or links to related issues.

### Example Commit Message

```
Add sandbox smoke guardrails

Why: prevent accidental writes during drills.
How: block non-sandbox ARNs and log rejections via audit port.
Tests: npm test -- workspace=core-domain
Follow-ups: wire audit log into CLI output.
```

## Keep History Healthy

- **Avoid destructive commands**: Use `git revert <sha>` over rewriting shared history.
- **Amend carefully**: Only amend before sharing and only when allowed by project rules; otherwise make a new commit that corrects the previous one.
- **Experiment safely**: Use throwaway branches and clean commits when you return to the main line.
- **Split changes after the fact**: Use `git reset -p` to unstage chunks, then restage and commit them separately.

## Investigate Before Reverting

**Never undo changes you don't understand.** Unexpected changes in `git status` deserve investigation, not reflexive reverting.

### The Anti-Pattern

```bash
# WRONG - Haphazard revert without investigation
git status
# Shows: modified: packages/some-package/src/index.ts
# Thought: "I don't remember changing that, revert it"
git checkout -- packages/some-package/src/index.ts  # DANGEROUS
```

### Why This Is Dangerous

Unexpected changes may come from:
- **Another agent** working on a related task in the same session
- **Pre-commit hooks** that auto-format or fix code
- **Build tools** that generate or modify files
- **A task you forgot about** earlier in the session
- **Intentional work** that hasn't been committed yet

Blindly reverting can:
- Destroy hours of work from parallel processes
- Break functionality that was just added
- Create confusing state where "something worked, now it doesn't"

### The Right Pattern

```bash
# RIGHT - Investigate first
git status
# Shows: modified: packages/some-package/src/index.ts

# Step 1: What changed?
git diff packages/some-package/src/index.ts

# Step 2: Does this change make sense given recent context?
# - Is this related to the current task?
# - Could another agent have made this?
# - Does this look like generated/auto-formatted code?

# Step 3: Only revert if you UNDERSTAND the change AND it's wrong
# If unsure: ASK THE USER before reverting
```

### Decision Tree

```
Unexpected change in git status
    │
    ├─► Is this file related to current/recent work?
    │       │
    │       ├─► YES → Likely intentional, investigate the diff
    │       │
    │       └─► NO → Could be parallel work, ASK before reverting
    │
    └─► Does the diff look intentional (new features, fixes)?
            │
            ├─► YES → DO NOT REVERT - commit or preserve it
            │
            └─► NO (looks like accidental/broken change) → Safe to revert
```

### Rule of Thumb

**When in doubt, preserve the change.** It's easier to revert later than to recover lost work. If you're unsure whether a change should exist, ask the user rather than making assumptions.

## Parallel Work on Shared Branches

When working on a branch where parallel work may occur (human or other agents), **never discard uncommitted changes**. See [Cardinal Rules](#cardinal-rules-protect-others-work) above.

### Switching Branches Safely

If you need to switch branches:

```bash
# WRONG - loses parallel work
git stash && git checkout main

# RIGHT - preserves everything
git add -A && git commit -m "WIP: checkpoint before context switch"
git checkout -b new-task
```

### Safe Patterns

1. **Leave unrecognized changes alone**: If it's not blocking you, ignore it
2. **Commit before switching**: `git add -A && git commit -m "WIP: checkpoint"`
3. **New branch preserves state**: `git checkout -b my-new-work` keeps everything
4. **Ask before any destructive action**: Never discard without explicit user approval

## Quick Reference

| Task | Command |
|------|---------|
| See what changed | `git status`, `git diff`, `git diff --cached`, `git show HEAD` |
| Stage carefully | `git add -p`, `git restore --staged <path>`, `git reset -p` |
| Review history | `git log --oneline -n 5`, `git show <sha>` |
| Review branch history | `git log --oneline main..HEAD` |
| Undo safely | `git revert <sha>` (preferred), `git restore <path>` for workspace edits |
| Restructure history | `git rebase -i main` |
| Split a commit | `git rebase -i` → edit → `git reset HEAD^` → stage/commit parts |
| Combine commits | `git rebase -i` → squash/fixup |
| Abort rebase | `git rebase --abort` |
| Find lost commits | `git reflog` |

## Sandbox-Safe Commits

When running in a sandboxed environment, heredocs (`<<EOF`) fail because they create temp files in `/tmp`, which is blocked. Use these patterns instead.

### Problem: Heredocs Fail in Sandbox

```bash
# FAILS - heredoc needs /tmp write access
git commit -m "$(cat <<'EOF'
feat: add feature

Body text here
EOF
)"
# Error: can't create temp file for here document: operation not permitted
```

### Solution 1: Multiple -m Flags (Recommended)

Each `-m` flag adds a paragraph to the commit message:

```bash
# Simple commit
git commit -m "feat: add user authentication"

# With body (empty -m creates blank line)
git commit -m "feat: add user authentication" \
  -m "" \
  -m "Why: users need secure login" \
  -m "How: JWT tokens with refresh rotation"

# With trailer
git commit -m "feat: add user authentication" \
  -m "" \
  -m "Implements secure JWT-based auth flow" \
  -m "" \
  -m "🤖 Generated with Claude Code" \
  -m "" \
  -m "Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Solution 2: Temp File in Allowed Directory

Write the message to `/tmp/claude/` which is sandbox-allowed:

```bash
# Write multi-line message to allowed temp location
cat > /tmp/claude/commit-msg.txt << 'COMMIT'
feat: add user authentication

Why: users need secure login
How: JWT tokens with refresh rotation

🤖 Generated with Claude Code
COMMIT

# Commit using the file
git commit -F /tmp/claude/commit-msg.txt

# Clean up
rm /tmp/claude/commit-msg.txt
```

**Note**: The outer heredoc writing to `/tmp/claude/` succeeds because that path is in the sandbox allowlist.

### Quick Reference

| Pattern | Use When |
|---------|----------|
| Single `-m "msg"` | Simple one-line commits |
| Multiple `-m` flags | Multi-paragraph messages |
| `-F /tmp/claude/file` | Complex messages with special characters |

## Checklist Before PR

### Phase 1 Complete?
- [ ] Feature implemented and working?
- [ ] All changes committed (even as WIP)?

### Phase 2 Complete?
- [ ] History restructured with `git rebase -i main`?
- [ ] Each commit is atomic (one logical change)?
- [ ] Commit messages explain why, not just what?
- [ ] `git log --oneline main..HEAD` tells a clear story?
- [ ] `./verify.sh --agent` passes on final state?
