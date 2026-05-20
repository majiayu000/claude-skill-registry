---
name: commit
description: Git commit guidelines. Use when creating, amending, squashing, or rewording git commits, staging files, or writing commit messages.
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(git status:*)
---

# Git Commit Guidelines

Follow Conventional Commits with these overrides:

- Allowed types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `ci`
- Message format: `<type>: <lowercase imperative description>`
- No scopes — do not use `<type>(scope):` form
- Add body, separated by blank line, only when subject line insufficient

## Additional Guidelines

- Always sign commits with `git commit -S`
- Do NOT include AI co-authoring information
- Do NOT use `git -C <path>` when the current directory is already the repository root
