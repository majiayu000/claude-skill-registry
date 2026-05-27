---
name: dev-reset-workspace
description: Clean the workspace of finished-work vestiges so new work can start from a fresh main branch
argument-hint: "[--force]"
disable-model-invocation: false
---

Reset the workspace to a clean state on `main` with no leftover branches,
uncommitted files, or background agents from previous work. Run this between
tasks to start fresh.

**When to use this skill:**

- After merging a PR and before starting new work
- When the workspace has accumulated stale branches or uncommitted files
- When background agents from a previous session may still be running
- Any time `git status` or `git diff` is not clean and you want a fresh start

## Arguments

- `--force` (optional): Skip interactive prompts — auto-delete safe-to-remove
  files and stale branches without asking. Still preserves files that appear to
  contain meaningful uncommitted work.

## Workflow

Work through each phase **in order**. Report findings at each phase before
acting. Unless `--force` is given, ask the user before destructive actions.

---

### Phase 1 — Stop background agents

Check for running background tasks (agents, shells, builds) from previous work.

1. **List running tasks:** Use the TaskList tool (or `/tasks` output) to find
   any in-progress background agents or shells.

2. **For each running task:**
   - Identify what it is doing (build, test, agent work, etc.)
   - Determine if it is safe to stop — a task is safe to stop if:
     - It belongs to a completed/merged PR
     - It is idle or stuck
     - It is a stale monitoring or polling loop
   - A task is NOT safe to stop if:
     - It is actively writing files that haven't been committed
     - It is mid-push or mid-merge

3. **Stop safe tasks** using TaskStop. Report any tasks you chose not to stop
   and why.

4. **If no tasks are running**, report "No background tasks found" and proceed.

---

### Phase 2 — Analyze uncommitted changes

Examine the working tree for any modifications or untracked files.

1. **Run diagnostics in parallel:**

   ```bash
   git status --short
   git diff --stat
   git diff --cached --stat
   git log --oneline -10
   git branch -vv
   ```

2. **If the working tree is clean** (no output from status/diff), skip to
   Phase 3.

3. **For each uncommitted or untracked file**, classify it:

   | Classification | Action | Examples |
   |---|---|---|
   | **Belongs to a merged PR** | Should have been committed — warn user | Source files matching recent PR topics |
   | **Build artifact / generated file** | Safe to delete or add to `.gitignore` | `build/`, `*.o`, `*.spv`, `shaders/compiled/` |
   | **Editor / OS junk** | Add to `.git/info/exclude` (local only) | `.DS_Store`, `*.swp`, `.vscode/settings.json` |
   | **Meaningful new work** | Stash or warn — do NOT delete | New lesson files, library changes |
   | **Unknown** | Ask the user | Anything ambiguous |

4. **To classify files, check recent context:**

   ```bash
   # Recent merged PRs
   gh pr list --state merged --limit 5

   # Recent branches (local and remote)
   git branch -a --sort=-committerdate | head -20

   # What the current branch was working on
   git log --oneline HEAD...origin/main 2>/dev/null
   ```

5. **Report findings** in a table:

   ```text
   Uncommitted files analysis:
   ──────────────────────────────────────────────
   M  lessons/gpu/17-normal-maps/main.c   → Belongs to merged PR #42 (stale edit)
   ?? build/CMakeCache.txt                 → Build artifact (safe to delete)
   ?? .DS_Store                            → OS junk (add to local exclude)
   A  lessons/gpu/30-new-lesson/main.c     → New work (stash? ask user)
   ```

6. **Take action per classification:**
   - **Merged-PR leftovers:** Warn the user. These may be edits that should
     have been in the PR. Offer to discard them (`git checkout -- <file>`) or
     stash them.
   - **Build artifacts already in `.gitignore`:** Delete with `git clean -fd`
     for those paths only (not a blanket clean).
   - **Build artifacts NOT in `.gitignore`:** Offer to add them to `.gitignore`
     and then delete.
   - **Editor/OS junk:** Add patterns to `.git/info/exclude` (not `.gitignore`,
     since these are personal and shouldn't be committed).
   - **Meaningful new work:** `git stash push -m "dev-reset: uncommitted work"`.
     Report the stash entry so the user can recover it.
   - **Unknown:** Ask the user with AskUserQuestion (options: delete, stash,
     gitignore, local exclude, skip).

---

### Phase 3 — Switch to main and pull latest

1. **If not on `main`:**

   ```bash
   git checkout main
   ```

   If checkout fails due to uncommitted changes, go back to Phase 2 — something
   was missed.

2. **Pull latest:**

   ```bash
   git pull origin main
   ```

3. **Verify:**

   ```bash
   git status --short
   git diff --stat
   ```

   Both should produce no output. If not, investigate and resolve.

---

### Phase 4 — Remove stale local branches

Find and delete local branches whose work has been merged into `origin/main`.

1. **Fetch latest remote state:**

   ```bash
   git fetch --prune origin
   ```

2. **Find merged branches:**

   ```bash
   git branch --merged origin/main \
     | sed 's/^[* ]*//' \
     | grep -v '^main$'
   ```

3. **Find branches whose remote tracking branch is gone** (PR was merged and
   remote branch deleted):

   ```bash
   git branch -vv | grep ': gone]' | awk '{print $1}'
   ```

4. **Combine both lists** (deduplicate). For each branch:
   - Confirm it is not the current branch
   - Confirm it has been merged or its remote is gone
   - Delete it:

     ```bash
     git branch -d <branch-name>
     ```

   - If `-d` fails (not fully merged), report it and skip — do NOT use `-D`
     unless the user explicitly confirms or `--force` was given AND the remote
     tracking branch is gone (meaning the PR was merged and the remote branch
     was deleted by GitHub).

5. **Report what was removed:**

   ```text
   Removed stale branches:
     ✓ lesson-17-normal-maps (merged, remote deleted)
     ✓ lesson-18-scene-loading (merged, remote deleted)
     ⏭ experiment-wip (not merged, kept)
   ```

---

### Phase 5 — Clean up worktrees

Check for leftover Claude Code worktrees from previous sessions.

```bash
git worktree list
```

If any worktrees exist under `.claude/worktrees/`:

- Check if they have uncommitted changes (`git -C <path> status --short`)
- If clean: `git worktree remove <path>`
- If dirty: warn the user and skip

---

### Phase 6 — Final verification

Run a final check to confirm everything is clean.

```bash
git status
git diff
git branch
git log --oneline -3
```

**Expected state:**

- On branch `main`
- Working tree clean (nothing to commit)
- `git diff` produces no output
- Only `main` (and any intentionally kept branches) remain
- HEAD matches `origin/main`

**Report final state:**

```text
Workspace Reset Complete
════════════════════════
Branch:          main (up to date with origin/main)
Working tree:    clean
Stale branches:  3 removed, 0 kept
Background tasks: 0 running
Stashed work:    1 entry (use `git stash list` to see)

Ready for new work.
```

---

## Error handling

- **Merge conflicts during pull:** Report the conflict and exit — user must
  resolve manually.
- **Protected branches:** Never force-delete `main` or `master`.
- **Network errors on fetch/pull:** Report and continue with local cleanup.
- **`gh` CLI not authenticated:** Skip PR-related analysis, proceed with
  git-only checks.

## Safety guarantees

- **Never runs `git clean -fdx` on the entire repo.** Only cleans specific
  identified paths.
- **Never runs `git reset --hard`** unless the user explicitly confirms.
- **Never deletes branches with `-D`** without user confirmation (or `--force`
  with remote-gone confirmation).
- **Always stashes rather than deletes** when in doubt about uncommitted work.
- **Never modifies `.gitignore`** without showing the user what will be added.
- **Reports everything** before acting — the user sees the plan first.
