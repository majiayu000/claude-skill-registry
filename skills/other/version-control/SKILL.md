---
name: version-control
description: "Manage Git repositories and collaborative workflows — branching strategies, commit hygiene, conflict resolution, pull requests, hooks, and .gitignore management. Use when the user requests version control or provides relevant inputs for this workflow."
license: "MIT"
metadata:
  author: "awesome-ai-agent-skills contributors"
  version: "1.1.0"
---

# Version Control with Git

This skill equips an AI agent to perform the full spectrum of Git-based version control tasks, from initializing a repository and crafting atomic commits to orchestrating branching strategies, resolving merge conflicts, and configuring automation with hooks. It covers both everyday workflows and advanced operations needed for professional team collaboration.

## Workflow

1. **Assess Repository State**: Run `git status`, `git log --oneline -10`, and `git branch -a` to understand the current branch, uncommitted changes, recent history, and available remotes. This context determines which operations are safe to perform.

2. **Stage and Commit Changes**: Group related changes into atomic commits. Write commit messages that start with a concise summary line (50 characters or fewer), followed by a blank line and an explanatory body when the change is non-trivial. Follow the project's commit convention (Conventional Commits, Angular style, etc.) if one exists.

3. **Branch Management**: Create feature, bugfix, or release branches from the appropriate base. Use a consistent naming convention such as `feat/short-description`, `fix/issue-123`, or `release/1.2.0`. Delete stale branches after merging to keep the branch list clean.

4. **Synchronize with Remote**: Fetch and pull regularly to stay up to date. Push feature branches with the `-u` flag on first push. Before merging, rebase or merge the base branch into the feature branch to resolve conflicts early in an isolated context.

5. **Resolve Conflicts**: When conflicts arise, inspect the conflicting files, understand both sides of the change, choose the correct resolution (or combine both), mark the file as resolved with `git add`, and complete the merge or rebase. Always run tests after resolution to confirm correctness.

6. **Automate with Hooks and CI**: Set up Git hooks (pre-commit for linting/formatting, commit-msg for message validation, pre-push for test runs) and ensure `.gitignore` covers build artifacts, environment files, and OS metadata. Integrate with CI pipelines to enforce quality gates on every push.

## Supported Technologies

- **Git** (CLI, libgit2)
- **Platforms**: GitHub, GitLab, Bitbucket, Azure DevOps
- **CLI tools**: `gh` (GitHub CLI), `glab` (GitLab CLI)
- **Hook frameworks**: Husky, pre-commit, Lefthook
- **Branching models**: GitFlow, GitHub Flow, trunk-based development

## Usage

Ask the agent to perform any Git operation by describing what you need in plain language. Examples:

- "Create a feature branch for the new auth module and commit my staged changes."
- "Resolve the merge conflicts in `src/config.ts` and complete the merge."
- "Set up a `.gitignore` for a Python project with a virtual environment."
- "Rebase my branch onto main and force-push the cleaned-up history."

The agent will verify the repository state before every destructive operation and confirm with you before running commands like `reset --hard`, `push --force`, or `rebase` that rewrite history.

## Examples

### Example 1 — Resolving a Merge Conflict

**Scenario**: You are on branch `feat/user-profile` and want to merge `main`, but there is a conflict in `src/utils/format.ts`.

```bash
# Attempt the merge
git merge main
# Output: CONFLICT (content): Merge conflict in src/utils/format.ts

# Inspect the conflict markers
git diff --name-only --diff-filter=U
# src/utils/format.ts
```

The conflicting file contains:
```typescript
function formatDate(date: Date): string {
<<<<<<< HEAD
  return date.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
=======
  return new Intl.DateTimeFormat("en-US", { dateStyle: "medium" }).format(date);
>>>>>>> main
}
```

**Resolution**: The `main` version uses the modern `Intl.DateTimeFormat` API, which is preferred. Accept that version, remove the conflict markers, and complete the merge:

```typescript
function formatDate(date: Date): string {
  return new Intl.DateTimeFormat("en-US", { dateStyle: "medium" }).format(date);
}
```

```bash
# Mark resolved and commit
git add src/utils/format.ts
git commit -m "merge main into feat/user-profile, adopt Intl.DateTimeFormat"
```

### Example 2 — Setting Up a Branching Strategy (GitHub Flow)

**Scenario**: A small team wants a lightweight branching model for continuous deployment.

```bash
# Ensure main is the default and protected branch
gh repo edit --default-branch main

# Create a feature branch from main
git checkout main && git pull
git checkout -b feat/dark-mode

# ... develop and commit ...
git add .
git commit -m "feat: add dark-mode toggle to settings page

Reads user preference from localStorage and applies the
'dark' class to <html>. Falls back to OS preference via
prefers-color-scheme media query."

# Push and open a pull request
git push -u origin feat/dark-mode
gh pr create \
  --title "feat: add dark-mode toggle" \
  --body "## Summary
- Adds a toggle in Settings that persists to localStorage
- Respects OS-level dark mode preference as default

## Test plan
- [ ] Toggle switches theme immediately
- [ ] Preference persists across page reloads
- [ ] Falls back to OS preference for new users"

# After review and CI pass, merge via GitHub
gh pr merge --squash --delete-branch
```

**Key points**: `main` is always deployable, every change goes through a PR with review and CI, and branches are deleted after merge to avoid clutter.

## Best Practices

- **Write atomic commits.** Each commit should represent one logical change that compiles and passes tests on its own. This makes `bisect`, `revert`, and `cherry-pick` reliable.
- **Never commit secrets.** Add `.env`, credentials files, and private keys to `.gitignore` before the first commit. Use tools like `git-secrets` or `trufflehog` to scan for accidental leaks.
- **Rebase feature branches, merge to main.** Rebasing keeps feature branch history linear and easy to review; merging into main preserves the merge commit as a clear integration point.
- **Use `--force-with-lease` instead of `--force`.** It prevents overwriting teammates' work by failing if the remote has commits you haven't fetched.
- **Tag releases.** Use annotated tags (`git tag -a v1.2.0 -m "Release 1.2.0"`) for every production release so you can always trace deployed code back to a specific commit.
- **Keep `.gitignore` comprehensive.** Start from a template (github/gitignore) for your language/framework and add project-specific entries for build output, editor config, and local environment files.

## Edge Cases

- **Detached HEAD state**: If the user has checked out a tag or specific commit, warn them before committing. Suggest creating a branch first to avoid orphaned commits.
- **Large binary files**: Git is not designed for large binaries. Recommend Git LFS for assets like images, models, or videos, and add the relevant LFS tracking rules.
- **Shallow clones**: Operations like `blame`, `log`, and `bisect` may fail on shallow clones (`--depth 1`). Run `git fetch --unshallow` before performing history-dependent operations.
- **Submodules and monorepos**: When the project uses submodules, ensure `git submodule update --init --recursive` is part of the setup instructions. For monorepos, respect per-package change boundaries during commits.
- **Diverged branches after force-push**: If a teammate force-pushed a shared branch, advise `git fetch` followed by `git reset --hard origin/<branch>` only after confirming no local work will be lost. Coordinate with the team first.
