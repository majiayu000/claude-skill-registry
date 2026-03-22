---
name: dk-merge-resolve
description: >
  Resolve merge conflicts in the current branch. Only invoke when the user
  explicitly runs /dk-merge-resolve. Do NOT auto-trigger on mentions of merge
  conflicts, conflict markers, or similar keywords.
allowed-tools: Bash, Read, Edit, Grep, Glob, AskUserQuestion
---

# Resolve Merge Conflicts

Your job is to resolve all merge conflicts in the current branch of the current repo.

Conflicts can come from many sources — `git merge`, `git rebase`, `git stash pop`, `git cherry-pick`, or any operation that combines divergent changes. This skill handles all of them.

## Step 0: Diagnose the Situation

Before changing anything, understand what state git is in and what caused the conflicts.

1. **Snapshot the state** — Run these to understand what's happening:
   ```bash
   git status
   git rev-parse HEAD
   ```
   Print the HEAD sha to the user: "Safety checkpoint: HEAD is at `<sha>`."

2. **Identify the conflict source** — Check which operation is in progress:
   - `git rev-parse MERGE_HEAD 2>/dev/null` → merge in progress
   - `test -d .git/rebase-merge || test -d .git/rebase-apply` → rebase in progress
   - `git stash list` + check `git status` for "Unmerged paths" without MERGE_HEAD → stash pop conflict

   This matters because the abort/recovery command differs:
   | Source | Abort command |
   |--------|--------------|
   | merge | `git merge --abort` |
   | rebase | `git rebase --abort` |
   | cherry-pick | `git cherry-pick --abort` |
   | stash pop | `git checkout -- .` (stash stays in list, nothing lost) |

   Print the appropriate abort command to the user so they have an escape hatch.

3. **Protect unstashed work** — If there are uncommitted changes **beyond** the conflicted files (tracked modified files that aren't part of the conflict), warn the user. These are at risk during resolution. Suggest committing or stashing them separately before proceeding, and **wait for confirmation**.

   Do NOT blindly `git stash` when conflicts are already present — git won't allow it, and if the conflicts came from a `stash pop`, the user's changes are already in the working tree as the conflicted content. Stashing again would lose them.

## Step 1: Build Context

Understand what both sides of the conflict were trying to do:

1. **Identify the two sides** — Based on the conflict source:
   - **Merge**: "ours" = current branch, "theirs" = the branch being merged in
   - **Stash pop**: "ours" = current working tree (post-pull), "theirs" = the stashed changes (the user's local work)
   - **Rebase**: "ours" = the branch being rebased onto, "theirs" = the commits being replayed

   Understanding which side is which is critical — especially for stash pop conflicts where "theirs" is the user's own work and should generally be preserved.

2. **Find all conflicts** — Use Grep to search for `<<<<<<<` across the repo. This gives you the full list of files and locations.

3. **Triage** — Group conflicts before diving in:
   - **Trivial**: Lock files, auto-generated files, whitespace-only — resolve mechanically.
   - **Straightforward**: Both sides changed different things in the same region — combine them.
   - **Requires judgment**: Both sides changed the same logic — need to understand intent.

## Step 2: Resolve Each Conflict

For each conflicted file, read the file (or at minimum the conflicted region with surrounding context), then decide:

1. **Keep ours** — when the incoming changes are superseded
2. **Keep theirs** — when the incoming side has the better version
3. **Combine both** — the most common case; merge both sides' intent into correct code

**For stash pop conflicts**: The user's stashed changes are their in-progress work. Default to preserving the user's intent — their local changes are the "important" side. The pulled/merged content is the "environment" that the user's work needs to be adapted to.

Correctness matters more than cleverness. When combining:
- Understand what each side was trying to do
- Write the result that achieves both goals
- Make sure imports, variable names, and types are consistent across the merged result

For each conflict:
1. Read the file to see the full conflict region with context
2. Edit the file to the desired final state — remove ALL conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
3. Stage the resolved file with `git add <file>`

After resolving all conflicts in a file, do a quick sanity check: does the file still make sense? Are imports consistent? Are there dangling references?

## Step 3: Verify — Close the Loop

After all conflicts are resolved, verification is **mandatory**, not optional. A merge that compiles is not a merge that works.

### 3a. Confirm clean state

```bash
git diff --check          # No conflict markers remain
grep -rn '<<<<<<<' .      # Belt-and-suspenders: grep for stray markers
```

If either finds markers, go back and fix them before proceeding.

### 3b. Determine affected projects

Check which parts of the monorepo were touched by the merge. Run:

```bash
# For merge: diff between merge base and current state
git diff --name-only $(git merge-base HEAD MERGE_HEAD) HEAD 2>/dev/null || \
  git diff --name-only HEAD~1 HEAD  # fallback for rebase/cherry-pick
```

Map changed files to projects:

| Path prefix | Project | Check commands |
|-------------|---------|---------------|
| `taskit/taskit-frontend/` | Frontend | `npm run build` (TypeScript + Vite), `npm run lint` |
| `taskit/taskit-backend/` | Backend | `cd taskit/taskit-backend && python manage.py check --deploy 2>/dev/null || python manage.py check` |
| `odin/` | Odin | `cd odin && python -m pytest tests/unit/ -v` |
| `harness_usage_status/` | Harness Usage | `cd harness_usage_status && python -m pytest tests/ -v 2>/dev/null` |

### 3c. Run check commands for affected projects

Run **only** the checks for projects that had conflicted files or files changed by the merge. Do not run checks for unaffected projects — that wastes time and may surface pre-existing issues unrelated to the merge.

**Execution order:**
1. **Type checks / build** first — catches structural problems (missing imports, type errors, broken references). These are the most likely merge casualties.
2. **Lint** second — catches style issues introduced by conflict resolution.
3. **Fast tests** last — unit tests for the affected project. Skip integration/e2e tests (too slow for merge verification; those belong in CI).

For each check:
- Run the command
- If it **passes**: note it and move on
- If it **fails**: analyze the failure. If it's clearly caused by the merge resolution (missing import, type mismatch, duplicated declaration), fix it immediately and re-run. If it's a pre-existing failure unrelated to the merge, note it for the user but don't block on it.

**Frontend-specific** (most common merge casualty in this repo):
```bash
cd taskit/taskit-frontend && npm run build
```
This runs TypeScript type-checking AND Vite bundling — it catches duplicate imports, missing exports, type mismatches, and broken references. This single command is the highest-value check for frontend merges.

**Backend-specific:**
```bash
cd taskit/taskit-backend && python manage.py check
```
Catches model inconsistencies, migration conflicts, and configuration problems.

**Odin-specific:**
```bash
cd odin && python -m pytest tests/unit/ -v --tb=short
```
Fast unit tests only. Mock and integration tests are too slow for merge verification.

### 3d. Report results

After all checks complete, print a summary:

```
Merge verification:
  ✓ No conflict markers remaining
  ✓ Frontend build passed (TypeScript + Vite)
  ✓ Frontend lint passed
  ✗ Backend check failed — missing migration (see output above)
  — Odin tests skipped (no odin/ files in merge)
```

If any check failed due to the merge, fix it before completing the merge operation (`git merge --continue`, `git rebase --continue`, etc.). Do NOT finalize a merge with known check failures — that defeats the purpose of conflict resolution.

### 3e. Complete the merge operation

Only after all checks pass (or pre-existing failures are identified and noted):

- **Merge**: `git commit` (git usually has the merge commit staged already)
- **Rebase**: `git rebase --continue`
- **Cherry-pick**: `git cherry-pick --continue`
- **Stash pop**: No git command needed — files are already in working tree

Ask the user before running the finalization command.

## When You're Not Sure

If a conflict involves complex logic where both sides made substantial changes to the same code, and you're not confident about the correct resolution — **stop and ask**.

Show the user:
1. The conflicting chunks (both sides)
2. Your understanding of what each side intended
3. Your proposed resolution (or the options you see)

Then wait for confirmation before editing. A wrong merge is worse than a slow merge.
