---
name: commit-code
description: >
  Commit code following HMIS project conventions. Use when committing changes with
  proper issue closing keywords, message format, and co-author attribution.
disable-model-invocation: true
allowed-tools: Bash, Read, Grep
argument-hint: "[issue-number]"
---

# Commit Code with HMIS Conventions

Commit staged changes following the project's commit message conventions.

## Arguments

- `$0` - GitHub issue number (optional, for closing keyword)

## Commit Message Format

```
<Summary of change in imperative mood>

Closes #<issue-number>

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Issue Closing Keywords

- `Closes #N` - for general issue resolution
- `Fixes #N` - for bug fixes
- `Resolves #N` - alternative to closes

## Steps

1. Run `git status` to see what's staged
2. Run `git diff --staged` to review changes
3. Compose commit message following the format above
4. If issue number provided, include closing keyword
5. Commit with the formatted message
6. Report the commit hash and summary

## Rules

- **NEVER push** unless explicitly asked
- **NEVER amend** previous commits unless explicitly asked
- **Check persistence.xml** - if it's in the staged files, verify it uses environment variables
- **No credentials** - warn if .env or credentials files are staged
- JSF-only changes (XHTML only, no Java) do not require compilation
