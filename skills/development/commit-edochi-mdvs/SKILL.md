---
name: commit
description: Use when the user asks to commit, commit and push, or make a git commit. Covers branching, commit workflow, conventional commits, TODO updates, and push/PR rules.
---

# Commit & Branching Conventions

## Branching

**Never push directly to `main`.** All work goes through feature branches + PRs.

- One branch per TODO or feature: `feat/description`, `fix/description`, `docs/description`
- Branch off `main`: `git checkout -b feat/my-feature main`
- Always ask the user before creating a branch
- Merge via PR (regular merge, not squash)

## When to Commit

**Never commit unless the user explicitly asks.** No autonomous commits. Wait for "commit", "commit and push", or similar.

## Before Committing

- If the work corresponds to a spec TODO, update its status to `done` before committing (use the `todo` skill). This lets the user review the TODO update as part of the same diff.
- Verify tests pass, clippy is clean, and fmt is applied.

## Commit Workflow

Run `git add`, `git commit`, and `git push` as **separate commands** — never chained together.

### Staging

- Stage specific files by name — never use `git add -A` or `git add .`
- Don't stage files that contain secrets (`.env`, credentials)

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/) format. A `commit-msg` hook (cocogitto) enforces this.

Format: `<type>[optional scope]: <description>`

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `perf`, `style`

```bash
git commit -m "$(cat <<'EOF'
feat: add enum constraints on string fields
EOF
)"
```

### Push

**Only push when the user explicitly asks.** "Commit" does not imply "push". Wait for "push", "commit and push", or similar.

### Pull Requests

After pushing a feature branch, create a PR to `main` when the user asks. Use `gh pr create` with a clear title and summary. CI must pass before merging. Use regular merge (not squash).

## Safety Rules

- Never push directly to `main`
- Never amend, force-push, or skip hooks — unless the user explicitly asks
- Never rebase interactively (`git rebase -i`)
- If a pre-commit hook fails, fix the issue and create a **new** commit (don't amend)
