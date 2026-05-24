---
name: git-commit-creator
description: "Creates properly formatted Git commits following conventional commit standards for the MCPSpy project. Use when asked to commit changes, stage files, or manage git workflows. Has access to git status, diff, checkout, add, and commit commands."
allowed-tools:
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git diff-index:*)
  - Bash(git add:*)
  - Bash(git checkout:*)
  - Bash(git commit:*)
  - Bash(git show:*)
---

# Git Commit Creator Skill

Automates the creation of well-structured Git commits for the MCPSpy project.

## Workflow

You should STRICTLY follow the following steps:

1. Understand the commit status through `git status`, `git diff` and `git diff --staged`.
2. Analyze the scope and nature of changes
3. Using `git checkout -b <branch-name>`, create concise branch name with standard prefixes (e.g., `feat`, `chore`, `fix`).
4. Using `git commit -m "<commit-message>"`, create a conventional commit message that accurately reflects the changes.

## Commit Message Convention

- Use standard prefixes: `feat(component):`, `chore:`, `fix(component):`
- Component examples: `library-manager`, `ebpf`, `mcp`, `http`, `output`
- Brackets are optional but recommended for clarity
- Keep titles concise and descriptive

### Examples

- `feat(library-manager): add support for container runtime detection`
- `chore: update dependencies to latest versions`
- `fix(ebpf): handle kernel version compatibility issues`
