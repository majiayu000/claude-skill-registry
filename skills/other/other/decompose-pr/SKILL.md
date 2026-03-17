---
name: decompose-pr
description: Break down a complex PR into focused, atomic commits for learning. Creates a temporary branch with one commit per logical change, making it easier to study how each piece works.
---

# Decompose PR for Learning

Turn a multi-concern PR into a sequence of focused commits that each do one thing.

## Why This Exists

Complex PRs are hard to understand because changes interleave. A single function might have three modifications serving different purposes. By decomposing into atomic commits, you can:

- Study each change in isolation
- Understand the dependency order (what enables what)
- See which tests correspond to which changes
- Build intuition for the codebase incrementally

## When to Use

- You're reviewing a PR and can't follow the logic
- You're onboarding and want to understand a feature's implementation
- You're debugging and need to isolate which change caused an issue
- You're learning a codebase through its PRs

## Phase 1: Analyze

Gather context and identify the distinct logical changes.

```bash
# Get PR metadata
gh pr view <NUMBER> --json title,body,baseRefName,headRefName,additions,deletions,changedFiles

# Get the diff
gh pr diff <NUMBER>
```

**Identify logical changes by looking for:**

1. **Explicit claims** — What does the PR description say it fixes/adds?
2. **Structural changes** — New types, new fields, new functions
3. **Behavioral changes** — Modified control flow, new conditions
4. **Test changes** — New tests often map 1:1 to behavioral changes
5. **Refactors** — Renames, extractions, reorganizations that enable other changes

**Present to user:**

```
## Identified Changes

| # | Change | Files | Depends On |
|---|--------|-------|------------|
| 1 | Add Cursor type for pagination | types.ts | - |
| 2 | Update query builder to accept cursor | query.ts | 1 |
| 3 | Add cursor encoding/decoding | cursor.ts, query.ts | 1 |
| 4 | Tests for pagination | query.test.ts | 2, 3 |
```

**Get user approval before proceeding.** They may want to reorder, combine, or split changes differently.

## Phase 2: Plan the Decomposition

Determine the commit order based on dependencies:

**Dependency rules:**

- Types/structs before code that uses them
- Refactors before features that depend on them
- Core logic before tests
- Changes to the same function should be ordered by logical progression

**For each commit, define:**

- Subject line (imperative mood, ≤50 chars)
- Which hunks from the diff to include
- Whether it should compile (see note on atomicity below)

**Present the plan:**

```
## Commit Plan

1. "Add Cursor type for pagination"
   - types.ts: lines 20-35 (new interface)
   - Builds: Yes

2. "Update query builder to accept cursor"
   - query.ts: lines 45-80 (modified buildQuery)
   - Builds: Yes

3. "Add cursor encoding/decoding helpers"
   - cursor.ts: lines 1-40 (new file)
   - query.ts: lines 81-95 (use helpers)
   - Builds: Yes

4. "Add tests for cursor pagination"
   - query.test.ts: lines 120-200 (new tests)
   - Builds: Yes
```

**On atomicity and buildability:**

Prefer commits that compile and pass lint — these are stable checkpoints. However, some changes are **inseparable**: changing a function signature requires updating all callers in the same commit. When planning, identify these coupling points and group them.

For larger refactors or base type changes, non-buildable intermediate commits may better tell the learning story. That's acceptable — the goal is understanding, not a pristine git history.

**Showing contrast:**

Consider what helps the learner understand _why_ each change matters:

- **Bug fixes**: A `legacy_*` function demonstrating the bug makes the fix concrete
- **Refactors**: Old structure → migration → deletion as separate commits
- **Performance**: Slow version → fast version (if instructive)
- **Features**: Incremental build-up (no "before" to contrast)

This is optional — use when it aids understanding.

## Phase 3: Execute

Create the learning branch and apply changes incrementally.

```bash
# Fetch the PR branch
git fetch origin <pr-branch>

# Create learning branch from base (naming convention: decompose/<pr-branch>)
git checkout -b <user>/decompose/<pr-branch> origin/<base-branch>
```

**For each planned commit:**

1. Apply only the relevant hunks (use `git apply --cached` with patch, or manual edits)
2. Verify it compiles (if expected)
3. Commit with the planned message
4. Move to next commit

**Techniques for partial application:**

```bash
# Option A: Cherry-pick with manual reset
git cherry-pick -n <pr-commit>  # Apply without committing
git reset HEAD                   # Unstage everything
# Then manually stage just the hunks you want

# Option B: Apply specific hunks from diff
gh pr diff <NUMBER> > /tmp/full.patch
# Manually extract relevant hunks to /tmp/partial.patch
git apply --cached /tmp/partial.patch

# Option C: Manual edits
# Just make the edits by hand, referencing the PR diff
```

**After each commit:**

```bash
# Run formatter/linter first to avoid pre-commit surprises
# (prettier, cargo fmt, black, gofmt, etc.)

# Verify it builds (if applicable)
# (npm run build, cargo check, make build, go build, etc.)

# Commit
git add -A && git commit -m "<planned message>"
```

## Phase 4: Verify & Summarize

Ensure the final state matches the original PR.

```bash
# Compare final state to PR branch
git diff <pr-branch>
```

If there are differences, either:

- They're acceptable (whitespace, comment tweaks)
- Something was missed — add a final "cleanup" commit

**Present summary to user:**

```
## Decomposition Complete

Branch: user/decompose/feature-branch
Commits: 4

| # | Commit | What to Study |
|---|--------|---------------|
| 1 | abc123 | New type — examine the interface shape |
| 2 | def456 | Integration — how existing code adapts |
| 3 | ghi789 | Helpers — encoding logic isolated |
| 4 | jkl012 | Tests — edge cases and expected behavior |

**To explore:**
git log --oneline user/decompose/feature-branch
git show <commit>  # See individual changes
```

## Important Notes

- **This branch is for learning only** — don't push or PR it
- **Prefer buildable commits when possible** — but non-buildable intermediate states are fine when they tell a clearer story
- **Tests may fail in intermediate commits** — that's expected
- **The goal is understanding, not perfection** — approximate decomposition is fine

## Anti-patterns

- Decomposing without understanding the PR first (do Phase 1 thoroughly)
- Making commits too granular (one line each) — group logically related changes
- Making commits too coarse (defeats the purpose)
- Spending hours on perfect decomposition — good enough is good enough
- Modifying the original PR branch

---

Enter decomposition mode now. Ask which PR to decompose, then begin Phase 1.
