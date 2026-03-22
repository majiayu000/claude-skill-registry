---
name: open-pull-request
description: Commits current changes and opens a pull request via GitHub CLI (gh). Use only when the user explicitly says "open a pull request", "open an pull request", or "create a pull request". Do not run this workflow for other requests.
---

# Open a Pull Request

## When to Use

Use this skill **only** when the user explicitly requests to open a pull request (e.g. "open a pull request", "open an pull request", "create a pull request"). Do not run git commit, push, or `gh pr create` for any other request.

## Preconditions

1. **Working tree**: Confirm that current changes (staged or unstaged) are what the user wants to commit. If the state is unclear or already on a feature branch with unpushed commits, ask before proceeding.
2. **GitHub CLI**: Require `gh` installed and authenticated. Run `gh auth status`; if not OK, instruct the user to install [GitHub CLI](https://cli.github.com/) and run `gh auth login`, then stop.

## Workflow

### 1. Create a new branch

- Create a new branch from current HEAD: `git checkout -b <branch-name>`.
- **Branch name**: Use user-provided name if given. Otherwise derive from the commit message: e.g. `feat/scope-short-desc`, `fix/short-desc`, `enhance/improve-x`, `ci/update-workflow`, or `(deps)/go-mod` (slug from the first line of the conventional commit). These patterns align with [.github/labeler.yml](.github/labeler.yml) so the labeler auto-applies PR labels (feature, bug, enhancement, github-actions, dependencies). For breaking changes, include `!` in the branch name to get the `breaking-change` label. Prefer lowercase, hyphens; avoid spaces.

### 2. Stage and commit

- Run `git add .`
- **Commit message**: Use conventional style per project (e.g. `feat(scope): description`, `fix(scope): description`). If the user provided a message, use it; otherwise generate from `git status` and `git diff` (or `git diff --staged` after add).
- Run `git commit -s -m "<message>"` so the commit includes a Signed-off-by line (DCO). Do not add a `Made-with: Cursor` or similar trailer to the commit message. The repo has the [DCO bot](https://github.com/apps/dco) enabled; PRs must have all commits signed off.

### 3. Push and create PR

- Push: `git push -u origin <branch-name>`
- Create PR: `gh pr create` using the repository’s [pull request template](.github/pull_request_template.md). Populate all sections (see **PR body** below). The `neptune` label is applied automatically; do not add it manually.

### 4. Safety

- Do not run `git push`, `git commit`, or `gh pr create` unless the user has explicitly requested to open a pull request.
- If the repo is in an unexpected state (e.g. already on a feature branch with unpushed commits, or detached HEAD), ask the user before creating a new branch or pushing.

## PR body (repo template)

The repo uses [.github/pull_request_template.md](.github/pull_request_template.md). When creating the PR (e.g. `gh pr create --body-file -` or by filling the template), populate:

- **What is this feature?** – Short description; correlates with issues.
- **Why do we need this feature?** – Problem or context (from commit/conversation).
- **Who is this feature for?** – Target user or use case.
- **Related issues** – e.g. `Fixes #123` or `Relates to #456` if applicable.
- **Notes for reviewers** – Optional; call out design decisions or areas to focus on.
- **Checklist** – Mark as appropriate: breaking changes (Yes/No/N/A), docs updated, tests added/updated.
- **AI Summary** – For AI reviewers; fill from changed files and context:
  - **Scope:** e.g. `lambda (config, webhooks, main)`, `docs`, `AGENTS.md`
  - **Type:** `feat` | `fix` | `docs` | `refactor`
  - **Key files/areas:** paths from `git diff --name-only` or conversation (e.g. `lambda/pkg/config/config.go`, `docs/github-app-and-lambda.md`)

Generate the body from the commit message and `git diff --name-only` (or equivalent) so the template sections are filled accurately.
