---
name: commit-helper
description: Generates clear, conventional commit messages from git diffs
allowed-tools: Bash, Read
---

# Commit Message Generator Skill

## Purpose
Generate conventional commit messages that follow best practices.

## Instructions

When invoked, you should:

1. **Analyze the changes**: Run `git diff --staged` to see what files have changed
2. **Identify the type**: Determine if this is a feat, fix, docs, refactor, etc.
3. **Write the message**: Create a commit message with:
   - Type and scope: `type(scope): subject`
   - Subject line: Clear, imperative mood, no period, < 72 chars
   - Body (optional): Explain the "what" and "why", not the "how"
   - Footer (optional): Breaking changes or issue references

## Conventional Commit Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code restructuring without changing functionality
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependencies
