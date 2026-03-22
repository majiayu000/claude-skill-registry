---
name: git
description: (ePost) Use when user says "commit", "push", "create a PR", "ship it", "done", "merge", or "open a pull request" — runs the appropriate git workflow (commit, push, or PR creation)
user-invocable: true
context: fork
agent: epost-git-manager
metadata:
  argument-hint: "[--commit | --push | --pr]"
  connections:
    enhances: []
---

# Git — Unified Git Workflow Command

**NEVER suggest `/git-commit`, `/git-push`, `/git-pr` as commands — use `/git --commit`, `/git --push`, `/git --pr` instead.**

## Aspect Files

| File | Purpose |
|------|---------|
| `references/commit.md` | Stage and commit with conventional commits |
| `references/push.md` | Commit changes and push to remote |
| `references/pr.md` | Create GitHub pull request from current branch |

## Step 0 — Flag / Intent Override

If `$ARGUMENTS` contains `--commit` or user said "commit": execute commit workflow immediately.
If `$ARGUMENTS` contains `--push` or user said "push": execute commit+push workflow immediately.
If `$ARGUMENTS` contains `--pr` or user said "pr" / "pull request": execute PR workflow immediately.
If `$ARGUMENTS` contains `--skip-build`: pass through to commit/push workflow — skips build verification gate (for WIP/draft commits).
Otherwise: continue to Step 1.

## Step 1 — Detect State

Run:
```bash
git status --short && echo "---AHEAD---" && git log --oneline @{u}..HEAD 2>/dev/null | wc -l | tr -d ' ' && echo "---PR---" && gh pr list --head "$(git branch --show-current)" --json number --jq length 2>/dev/null || echo 0
```

## Step 2 — Ask (Contextual, Natural Language)

Use `AskUserQuestion` with options based on git state. Examples:

**Changes detected (e.g., 26 modified + 14 untracked):**
- "Commit (26 modified, 14 new files)"
- "Commit and push"
- "Show changes (git diff)"
- "Describe what you want..."

**Clean tree, N commits ahead:**
- "Push (N commits to remote)"
- "Create pull request"
- "Show commits"
- "Describe what you want..."

**Clean and up-to-date:**
- "Create pull request"
- "Show recent commits"
- "Describe what you want..."

## Step 3 — Execute

Based on the user's answer, load and execute the matching workflow:
- Commit → `references/commit.md`
- Push → `references/push.md`
- PR → `references/pr.md`

## Build Gate

Build verification runs at two layers:

| Layer | Mechanism | When |
|-------|-----------|------|
| Skill instructions | `references/commit.md` tells agent to run build-gate | Agent follows skill |
| PreToolUse hook | `build-gate-hook.cjs` intercepts any `git commit` Bash call | Automatic enforcement |

The hook layer is automatic — it intercepts `git commit` regardless of whether the agent followed skill instructions. If the build fails, the commit is blocked with a clear error message.

**Bypasses** (for WIP/draft commits):
- Pass `--skip-build` flag: `git commit -m "wip" --skip-build`
- Set env: `EPOST_SKIP_BUILD=1 git commit -m "wip"`
- Disable via config: `{ "hooks": { "build-gate": { "enabled": false } } }` in `.epost-kit.json`
