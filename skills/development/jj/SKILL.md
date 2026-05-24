---
name: jj
description: Jujutsu (jj) skill for the ikigai project
---

# Jujutsu (jj)

## Description
Standard jj operations for day-to-day development work.

## Configuration

- **Remote**: origin (github.com:mgreenly/ikigai.git)
- **Primary branch**: main (bookmark)

## Commit Policy

**When user says "commit": use `jj commit -m "msg"` (NOT `jj describe`)**

Run `make check` periodically to catch issues early.

## Prohibited Operations

This skill does NOT permit:
- Modifying the `main` bookmark locally
- Merging into main locally
- Force pushing to main

**Merges to main only happen via GitHub PRs.** All work is done on feature bookmarks, pushed to origin, and merged through pull requests on GitHub. Never merge locally.

## Permitted Operations

- Commit to feature/fix bookmarks
- Push feature/fix bookmarks to remote
- Create new bookmarks
- Create and push tags
- Fetch from remote
- Rebase commits
- Create new commits on any mutable revision

## Common Commands

| Task | Command |
|------|---------|
| Check status | `jj status` |
| View changes | `jj diff` |
| View log | `jj log` |
| **Commit all files** | **`jj commit -m "msg"`** |
| Squash into parent | `jj squash` |
| Create bookmark | `jj bookmark create <name>` |
| Update bookmark to @ | `jj bookmark set <name>` |
| Push bookmark | `jj git push --bookmark <name>` |
| Fetch from remote | `jj git fetch` |
| Restore working copy | `jj restore` |
| Edit existing commit | `jj edit <revision>` |
| Create commit on revision | `jj new <revision>` |
| Rebase | `jj rebase -d <destination>` |
| Create tag | `jj tag set <name> -r <revision>` |
| Push tag | `git push origin <tag>` |
| List tags | `jj tag list` |

## Key Concepts

### Working Copy is Always a Commit
In jj, `@` (working copy) is always a commit being edited. There's no staging area.

### Bookmarks vs Branches
jj "bookmarks" are equivalent to git "branches". They're just named pointers to commits.

### Immutable vs Mutable
- `◆` = immutable (protected, can't change)
- `○` = mutable (can still edit)
- `@` = current working copy

### "Update the bookmark"
When the user says "update the bookmark", find the most recent bookmark in `@`'s ancestry and move it to `@` using `jj bookmark set <name>`.
