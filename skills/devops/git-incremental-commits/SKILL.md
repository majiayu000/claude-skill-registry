---
name: git-incremental-commits
description: Create small, incremental Git commits from uncommitted changes using Conventional Commits. Use when asked to review git status and split changes into small commits (by file or chunk), especially when dependency changes require lockfiles, and to finish with a clean working tree.
---

# Git Incremental Commits

## Goal

Turn all uncommitted changes into a sequence of small, clear Conventional Commits, stopping when `git status` is clean.

## Workflow

1. Run `git status -sb` and `git diff --stat` to understand scope.
2. Identify logical groups: dependencies, config, feature code, tests, docs, refactors, fixes.
3. Commit in smallest safe slices:
   - Prefer single-purpose commits.
   - Use `git add -p` to stage hunks when files mix concerns.
   - Use whole-file staging when the file is cohesive.
4. After each commit, re-check `git status -sb` and repeat.
5. Stop only when the working tree is clean and no untracked files remain (unless explicitly told to leave them).

## Grouping Heuristics

- **Dependencies**: If package manifests change (e.g., `package.json`), commit them with their lockfiles in the same commit.
- **Config/Build**: Commit build or CI config separately (e.g., `tsconfig`, `eslint`, CI files).
- **Feature work**: Prefer one commit per feature slice.
- **Fixes**: Keep bug fixes isolated from refactors when possible.
- **Tests**: Pair tests with the change they validate, unless tests are a separate logical unit.
- **Docs**: Keep docs-only changes separate.

## Conventional Commit Rules

- Use `type(scope): subject` or `type: subject`.
- Keep subject short, imperative, and specific.
- Suggested types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `build`, `ci`.
- Dependency changes: prefer `build(deps): add <pkg>` or `chore(deps): bump <pkg>`.

## Safety Checks

- Do not include unrelated changes in the same commit.
- If a file mixes unrelated edits and hunk-splitting is ambiguous, ask before proceeding.
- If there are generated files or large diffs, confirm intent before committing.

## Command Pattern

- Inspect: `git status -sb`, `git diff --stat`, `git diff`.
- Stage: `git add -p` or `git add <file>`.
- Commit: `git commit -m "type(scope): subject"`.
- Repeat until clean.
