---
name: git-commit
description: This skill should be used when creating conventional commits for current changes. It groups related changes into logical commits, ensures all files are committed, and verifies the working directory is clean afterward.
allowed-tools: ["Bash"]
---

# Git Commit Workflow

Create conventional commits for current changes. Optional hint: $ARGUMENTS

## Workflow

### See what has changed

!git status
!git diff --stat

### Apply these requirements

1. **Branch Check**: If on `dev`, `staging`, or `main`, create a feature branch named after the changes
2. **Commit Strategy**: Group related changes into logical conventional commits (feat, fix, chore, docs, etc.)
3. **Commit ALL Files**: Every file must be assigned to a commit group - no file gets left out or unstaged
4. **Commit Creation**: Stage and commit each group with clear messages
5. **Verification**: Run `git status` to confirm working directory is clean - must show "nothing to commit"

### Use conventional commit format

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `chore:` for maintenance
- `style:` for formatting
- `refactor:` for code restructuring
- `test:` for test additions

### Never

- use `--no-verify` flag
- attempt to bypass tests or quality checks
- skip tests or quality checks
- stash changes - ALL changes must be committed
- skip or exclude any files from the commit - even if they're unrelated
- leave uncommitted changes in the working directory
- ask the user which files to commit - commit everything

## Execute

Execute the workflow now.
