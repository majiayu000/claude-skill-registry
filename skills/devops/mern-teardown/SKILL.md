---
name: mern-teardown
description: Tear down a MERN project — delete local files and optionally delete the GitHub repo.
argument-hint: "[--delete-repo]"
allowed-tools: Bash, Read, Glob, Grep
---

## Purpose

Completely tear down a MERN project created by `/mern-kit`. Deletes all local
files. By default, keeps the GitHub repo for reference — use `--delete-repo` to
remove it too.

## Arguments

- `--delete-repo` — Also delete the GitHub repository (default: keep it)

## Prerequisites

- Must be run from inside the project directory (or provide the path)
- `gh` CLI authenticated (if `--delete-repo`)

## Teardown steps

### 1. Detect project

Confirm this is a MERN project by checking for:
- `turbo.json`
- `apps/web/`
- `packages/shared/`

If any are missing, warn and ask the user to confirm before proceeding.

Record the **project root** (absolute path) for later deletion.

### 2. Detect GitHub remote

```bash
git remote get-url origin 2>/dev/null
```

- If a remote exists, extract `owner/repo` from the URL
- If no remote, skip GitHub steps

### 3. Show summary and confirm

Display exactly what will happen:

```
Project: /path/to/my-app
GitHub:  owner/repo (will be DELETED | will be KEPT)

This will permanently delete:
  - All local files in /path/to/my-app
  [- GitHub repository owner/repo (if --delete-repo)]

Type the project name to confirm: _
```

**Do NOT proceed without explicit confirmation.**

### 4. Delete GitHub repo (if --delete-repo)

```bash
gh repo delete owner/repo --yes
```

If this fails (permissions, network), stop and report — do not continue to
local deletion so the user can retry.

### 5. Delete local project

```bash
cd ..
rm -rf /absolute/path/to/project
```

Use the absolute path recorded in step 1. Never use relative paths.

### 6. Confirm completion

Report what was deleted:
- Local directory: deleted
- GitHub repo: deleted / kept (with URL if kept)

## Safety

- Always confirm before destructive operations
- Show the full absolute path that will be deleted
- Never delete parent directories or anything outside the project root
- If GitHub deletion fails, stop — don't leave the user with a deleted
  local copy and a still-existing repo they can't find
