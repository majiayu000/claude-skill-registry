---
name: commit-push-current
description: 'Commit working-tree changes and push to the current branch: no branch creation, no branch switch, no PR. Use when asked to push to the branch you are already on, including the default branch.'
---

# Git Commit and Push (Current Branch)

Ship the working tree on the branch that is checked out. This skill never creates or switches branches: invoking it on a branch (including `main`/`master`) is explicit authorization to push to that branch. For the guarded flow that auto-creates a feature branch off the default, use `commit-push` instead.

## Context

**On platforms other than Claude Code**, run the Context fallback below. **In Claude Code**, the labeled sections contain pre-populated data. Use them directly.

**Git status:**
!`git status`

**Working tree diff:**
!`git diff HEAD`

**Current branch:**
!`git branch --show-current`

**Recent commits:**
!`git log --oneline -10`

**Push-target state (current branch on origin):**
!`git rev-list --left-right --count origin/$(git branch --show-current)...HEAD 2>/dev/null || echo 'NO_REMOTE_BRANCH'`

### Context fallback

```bash
printf '=== STATUS ===\n'; git status; printf '\n=== DIFF ===\n'; git diff HEAD; printf '\n=== BRANCH ===\n'; git branch --show-current; printf '\n=== LOG ===\n'; git log --oneline -10; printf '\n=== PUSH_TARGET ===\n'; git rev-list --left-right --count origin/$(git branch --show-current)...HEAD 2>/dev/null || echo 'NO_REMOTE_BRANCH'
```

---

## Step 1: Resolve branch state

- **Detached HEAD** (current branch empty): there is no branch ref to push. Report that this skill pushes only the checked-out branch and stop; suggest `commit-push` if the user wants a feature branch created.
- **Any named branch**: continue. The default branch is not special here: invocation is consent to push where you stand.
- **Nothing to do** (clean tree AND no commits ahead of the push target; the push-target counts show `0` on the right side): report and stop. The push target is always `origin/<current-branch>`, regardless of any differently-configured upstream, because Step 4 pushes there.
- **Clean tree but commits ahead of the push target (or `NO_REMOTE_BRANCH`)**: skip to Step 4. (`NO_REMOTE_BRANCH` also fires in detached HEAD, where the branch expansion is empty; the detached-HEAD bullet above runs first and stops, so keep these bullets in this order.)

## Step 2: Determine conventions

Match repo style for commit messages (project instructions in context > recent commits > conventional commits as default). With conventional commits, default to `fix:` over `feat:` when ambiguous. Adding code to remedy broken or missing behavior is `fix:`. Reserve `feat:` for capabilities the user could not previously accomplish. The user may override.

## Step 3: Commit

Scan changed files for naturally distinct concerns. If they clearly group into separate logical changes, create separate commits (2-3 max). Group at file level only. No `git add -p`. When ambiguous, one commit is fine.

Stage and commit each group. **Avoid `git add -A` and `git add .`**: they sweep in `.env`, build artifacts, and generated files:

```bash
git add file1 file2 file3 && git commit -m "$(cat <<'EOF'
commit message here
EOF
)"
```

## Step 4: Detect remote and push

Run `git remote` to list configured remotes.

- **`origin` not in the list** — covers both a true local-only repo (empty output) and the rarer case where other remotes exist but none is named `origin`. Either way, do NOT attempt to push, and do NOT add, invent, or guess a remote to target. Report "local-only, no remote — commits only" (or, if non-`origin` remotes exist, that no `origin` remote is configured) and stop. Skip the push attempt entirely rather than attempting and failing — this is what keeps the step safe to run unattended.
- **`origin` is in the list** — push, one unconditional form. It always targets `origin` (even when the branch's configured upstream points at another remote) and sets the upstream if missing:

```bash
git push -u origin HEAD
```

Never `--force`, `--force-with-lease`, or any force variant without explicit user authorization. A rejected push (diverged remote branch) is reported as-is: include the divergence counts from `git rev-list --left-right --count origin/$(git branch --show-current)...HEAD` and left for the user to resolve.
