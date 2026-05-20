---
name: git-commit
description: 'Use when user says "commit", "commit changes", "git commit", "make a commit", "create a commit", or mentions "/commit". Also use when user asks to stage and commit, write a commit message, or split changes into multiple commits.'
license: MIT
allowed-tools: Bash
model: sonnet
---

# Git Commit with Conventional Commits

Create standardized git commits using Conventional Commits. Analyze the diff and follow the interactive confirmation workflow below.

## Workflow

1. **Analyze**: Run `git diff --staged` (or `git diff` if nothing staged) and `git status --porcelain`
2. **Draft**: Generate commit message from the diff (type, scope, description)
3. **Present**: Show a single confirmation summary with both the files to stage and the commit message, then **wait for user approval**
4. **Execute**: After approval, run `git add` and `git commit` together in one step

### Confirmation Summary Format

Present the summary in this format before asking for approval:

```
Files to stage:
  A path/to/new-file
  M path/to/changed-file
  D path/to/removed-file
  R old/path → new/path

Commit message:
  <type>(<scope>): <description>

  <optional body>

  Co-Authored-By: ...
```

## Grouping Changes

If the diff contains multiple unrelated changes, propose splitting into separate commits:

- Stage specific files per logical group: `git add path/to/file1 path/to/file2`
- Use `git add -p` for partial file staging
- One logical change per commit
- Show a separate confirmation summary for each commit

## Interactive Confirmation (Required)

Show the files to stage and the commit message together in a single confirmation. Never stage or commit without explicit user approval.

## Co-Authored-By

Include in the commit footer using the current agent name and model name:

```
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```
