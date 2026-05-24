---
name: jj
description: Reference guide for jj (Jujutsu) version control operations
---

# jj Reference Guide

Reference for common jj operations, conventions, and patterns used in this codebase.

## Commit Description Format

All commit descriptions MUST be a single line following this format:

```
<project-prefix>: <short description>
```

**IMPORTANT**: Always use a one-line commit message. Never use multi-line descriptions or bullet points.

**Project prefix** is the descriptive folder path identifying the subsystem (e.g., `src/auth`, `lib/utils`, `services/api`).

**Description** starts with a lowercase verb: add, update, fix, refactor, remove, etc.

### Examples

```
src/auth: add JWT token refresh logic
lib/utils: fix date parsing for ISO formats
services/api: add rate limiting middleware
db/migrations: add users table
docs: update installation instructions
tests/integration: add checkout flow tests
```

## Analyzing Changes

### Overview Commands

```bash
# Files changed with change type (modified/added/deleted)
jj diff --summary
jj show <rev> --summary

# Lines changed per file histogram
jj diff --stat
jj diff -r <rev> --stat

# Full diff
jj diff
jj diff -r <rev>
```

### Size-Based Approach

- **Small changes** (≤5 files, ≤200 lines): read the diff directly
- **Large changes** (>5 files or >200 lines): use `/jj-context` to get a structured summary

## Common Operations

### Creating a Commit (`jj commit`)

Creates a new commit from working copy changes:

```bash
jj commit -m "<project-prefix>: <description>"
```

After committing, `@` becomes an empty working copy on top of the new commit.

### Describing a Commit (`jj describe`)

Sets or updates the description of an existing commit:

```bash
# Describe parent commit (most common)
jj describe @- -m "<project-prefix>: <description>"

# Describe any commit
jj describe <rev> -m "<description>"
```

### Creating a Bookmark (`jj bookmark`)

Bookmarks use `john/<descriptive-name>` format with kebab-case:

```bash
# On parent commit (if @ is empty)
jj bookmark create john/<name> -r @-

# On current commit
jj bookmark create john/<name>

# List bookmarks
jj bookmark list
```

**Naming**: Use 2-4 word kebab-case names describing the work:
- `john/s3-inventory-download`
- `john/fix-auth-refresh`
- `john/refactor-poller-config`

### Splitting a Commit (`jj split`)

Splits a commit into multiple commits by file:

```bash
# Split specific files into a new commit
jj split -r <rev> -m "<description>" path/to/file1 path/to/file2

# Last group: just describe the remainder
jj describe -r @- -m "<description>"
```

**Note**: After each split, the revision ID changes. Use `@-` to refer to the result.

**Grouping suggestions**:
- Core feature + its tests together
- Configuration/infrastructure separate
- Database migrations separate
- Refactoring/cleanup separate

### Squashing Changes (`jj squash`)

Moves changes from working copy into ancestor commits.

Without options, squashes all changes from `@` into its parent (`@-`):
```bash
jj squash  # @ → @-
```

With `--into` (or `-t`), squash into a specific commit:
```bash
jj squash --into <change-id> path/to/file.py  # specific files
jj squash --into <change-id> "src/**/*.py"    # glob pattern
jj squash --into @--                           # grandparent
```

**For sub-file chunks** (specific hunks, not whole files):

1. Save original @ change ID: `jj log -r @ --no-graph -T 'change_id'`
2. Create intermediate: `jj new --insert-before @`
3. Write only the hunks for target commit
4. Squash: `jj squash --into <target-change-id>`
5. Return to rebased @: `jj edit <rebased-@-change-id>`
6. Remove duplicated hunks
7. Restore working copy: `jj new`

**Always use change IDs** (e.g., `ksrmwuon`) not commit IDs - they're stable across rewrites.

## Revision Syntax

| Syntax | Meaning |
|--------|---------|
| `@` | Current working copy commit |
| `x-` | Parent(s) of x (e.g., `@-` = parent of working copy) |
| `x+` | Children of x |
| `@--` | Grandparent (`@-` then `-` again) |
| `trunk()` | Main branch (main/master) |
| `::x` | All ancestors of x, including x |
| `x::` | All descendants of x, including x |
| `x..y` | Ancestors of y that are NOT ancestors of x |
| `x::y` | Descendants of x that are also ancestors of y |
| `<change-id>` | Specific commit by change ID (e.g., `ksrmwuon`) |

## Working Copy Behavior

- In jj, `@` (working copy) is often an empty commit on top of your actual work
- Check `jj log` for "(empty)" to know if @ has changes
- `jj commit` creates commit and leaves @ empty
- `jj describe` modifies existing commit, doesn't change @
