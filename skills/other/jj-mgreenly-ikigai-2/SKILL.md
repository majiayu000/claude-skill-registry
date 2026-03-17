---
name: jj
description: Jujutsu (jj) skill for the ikigai project
---

# Jujutsu (jj)

## Dedicated Checkout Workflow

**This checkout is yours alone.** No other work happens here. The workflow is:

1. **Start fresh**: `jj git fetch` then `jj new main@origin`
2. **Do work**: Create commits as needed
3. **Push PR**: Create ONE bookmark on HEAD, push ALL commits (main..HEAD)
4. **Iterate**: If PR needs updates, commit more, push same bookmark
5. **Done**: PR merges via GitHub, return to step 1

## CRITICAL Rules

- **ONE bookmark only** - Never create multiple bookmarks
- **Push ALL commits** - Always push the entire stack from main to HEAD
- **Never partial pushes** - Don't push just one commit when there are more
- **Bookmark on HEAD** - The bookmark always points to the top of your stack

## Starting Work

```bash
jj git fetch
jj new main@origin
```

This puts you on a fresh commit with main as parent. All your work builds from here.

## Committing

When user says "commit", use `jj commit -m "msg"`:

```bash
jj commit -m "Add feature X"
```

Commits stack automatically. After 3 commits you have: `main → A → B → C (@)`

## Creating a PR

When ready to push:

```bash
# Create bookmark on current commit (HEAD of your stack)
jj bookmark create feature-name

# Track the bookmark (required before first push)
jj bookmark track feature-name@origin

# Push the bookmark (pushes ALL commits from main to HEAD)
jj git push --bookmark feature-name
```

## Updating a PR

If PR needs changes:

```bash
# Make changes, commit
jj commit -m "Fix review feedback"

# Move bookmark to new HEAD
jj bookmark set feature-name

# Push updated bookmark
jj git push --bookmark feature-name
```

## Prohibited Operations

- Modifying `main` bookmark locally
- Merging into main locally (PRs only)
- Force pushing to main
- Creating multiple bookmarks
- Pushing partial commit stacks

## Squashing (Permission Required)

**NEVER squash without explicit user permission.**

```bash
jj edit <revision>
jj squash -m "Combined message"
```

After squashing, update and push bookmark:
```bash
jj bookmark set feature-name
jj git push --bookmark feature-name
```

## Recovery

All operations are logged:
```bash
jj op log
jj op restore <operation-id>
```

## Common Commands

| Task | Command |
|------|---------|
| Fetch remote | `jj git fetch` |
| Start fresh on main | `jj new main@origin` |
| Check status | `jj status` |
| View changes | `jj diff` |
| View log | `jj log` |
| Commit | `jj commit -m "msg"` |
| Create bookmark | `jj bookmark create <name>` |
| Move bookmark to HEAD | `jj bookmark set <name>` |
| Push bookmark | `jj git push --bookmark <name>` |
| Track new bookmark | `jj bookmark track <name>@origin` |

## Key Concepts

- **Working copy** (`@`): Always a commit being edited
- **Bookmarks**: Named pointers to commits (like git branches)
- **main@origin**: The remote main branch
- **Commit stack**: Your commits from main to HEAD, all pushed together
