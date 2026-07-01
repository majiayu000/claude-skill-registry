---
name: commit-push
description: Commit working-tree changes and push to the remote — no PR. Use when asked to ship/publish commits without opening a PR, or when explicitly told not to create a PR.
---

# Git Commit and Push

**Asking the user:** When this skill says "ask the user", use the platform's blocking question tool: `AskUserQuestion` in Claude Code (call `ToolSearch` with `select:AskUserQuestion` first if its schema isn't loaded), `request_user_input` in Codex, `ask_question` in Antigravity CLI (`agy`), `ask_user` in Pi (requires the `pi-ask-user` extension). Fall back to presenting the question in chat only when no blocking tool exists in the harness or the call errors (e.g., Codex edit modes) — not because a schema load is required. Never silently skip the question.

## Context

**On platforms other than Claude Code**, run the Context fallback below. **In Claude Code**, the labeled sections contain pre-populated data — use them directly.

**Git status:**
!`git status`

**Working tree diff:**
!`git diff HEAD`

**Current branch:**
!`git branch --show-current`

**Recent commits:**
!`git log --oneline -10`

**Remote default branch:**
!`git rev-parse --abbrev-ref origin/HEAD 2>/dev/null || echo 'DEFAULT_BRANCH_UNRESOLVED'`

### Context fallback

```bash
printf '=== STATUS ===\n'; git status; printf '\n=== DIFF ===\n'; git diff HEAD; printf '\n=== BRANCH ===\n'; git branch --show-current; printf '\n=== LOG ===\n'; git log --oneline -10; printf '\n=== DEFAULT_BRANCH ===\n'; git rev-parse --abbrev-ref origin/HEAD 2>/dev/null || echo 'DEFAULT_BRANCH_UNRESOLVED'
```

---

## Step 1: Resolve branch state

The remote default branch returns something like `origin/main`; strip the `origin/` prefix. If it returned `DEFAULT_BRANCH_UNRESOLVED` or bare `HEAD`, try `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`. If both fail, fall back to `main`.

Branch routing:

- **Detached HEAD** — explain a branch is required and ask whether to create a feature branch. If yes, derive a name from the change content. If no, stop.
- **On default branch with work to do** (uncommitted, unpushed, or no upstream) — automatically create a feature branch (pushing the default directly is not supported). Derive a name from the change content and continue at Step 3. Do not ask whether to branch — committing on the default is not an option here.
- **On default branch with no work** — report no feature branch work and stop.
- **Feature branch** — continue.

## Step 2: Determine conventions

Match repo style for commit messages (project instructions in context > recent commits > conventional commits as default). With conventional commits, default to `fix:` over `feat:` when ambiguous — adding code to remedy broken or missing behavior is `fix:`. Reserve `feat:` for capabilities the user could not previously accomplish. The user may override.

## Step 3: Commit

When creating a feature branch off the default branch, make sure the new branch is based on an up-to-date default branch tip before committing — a stale or diverged local default silently forks the feature branch from old history.

Scan changed files for naturally distinct concerns. If they clearly group into separate logical changes, create separate commits (2-3 max). Group at file level only — no `git add -p`. When ambiguous, one commit is fine.

Stage and commit each group. **Avoid `git add -A` and `git add .`** — they sweep in `.env`, build artifacts, and generated files:

```bash
git add file1 file2 file3 && git commit -m "$(cat <<'EOF'
commit message here
EOF
)"
```

## Step 4: Detect remote and push

Run `git remote` to list configured remotes.

- **`origin` not in the list** — covers both a true local-only repo (empty output) and the rarer case where other remotes exist but none is named `origin`. Either way, do NOT attempt to push, and do NOT add, invent, or guess a remote to target. Report "local-only, no remote — commits only" (or, if non-`origin` remotes exist, that no `origin` remote is configured) and stop. Skip the push attempt entirely rather than attempting and failing — this is what keeps the step safe to run unattended.
- **`origin` is in the list** — push:

```bash
git push -u origin HEAD
```

Carry these safety constraints into the push: never `--force` or `--force-with-lease` without explicit user authorization; never push directly to protected branches (e.g., `main`, `master`, `release/*`) without explicit user authorization.

If the working tree is clean and all commits are already pushed, this step is a no-op.
