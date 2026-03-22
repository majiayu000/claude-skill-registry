---
name: git-workflow-patterns
description: >
  Use this skill when working on branching, PRs, commits, or releases. Triggers on: branch
  naming, PR workflow, commit messages, release strategy, or mentions of "branch", "PR",
  "commit", "release", "versioning", "changelog", or "git workflow".
---

# Git Workflow — DoclingOptimisation

## Branching (GitHub Flow)
- `main` is always deployable
- Short-lived feature branches: `feature/`, `fix/`, `chore/`, `docs/`
- Branch from main, merge back to main
- Delete branches after merge

## Commits (Conventional)
- Format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore
- Enforced by `commit-message.sh` hook
- Body explains WHY, not what

## Pull Requests
- Keep PRs small and focused
- Squash merge to main
- Include What/Why/How/Testing sections in description

## Releases
- Semantic versioning in pyproject.toml
- Docker image tags follow semver
- Git tags trigger CI/CD deployment
