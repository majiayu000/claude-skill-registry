---
name: nean-teardown
description: Tear down a NEAN project — drop database, delete local files, and optionally delete the GitHub repo.
argument-hint: "[--delete-repo] [--keep-db]"
allowed-tools: Bash, Read, Glob, Grep
---

## Purpose

Completely tear down a NEAN project created by `/nean-kit`. Drops the PostgreSQL
database, kills running dev servers, and deletes all local files. By default,
keeps the GitHub repo for reference — use `--delete-repo` to remove it too.
Use `--keep-db` to preserve the database.

## Arguments

- `--delete-repo` — Also delete the GitHub repository (default: keep it)
- `--keep-db` — Skip database deletion (default: drop it)

## Prerequisites

- Must be run from inside the project directory (or provide the path)
- `gh` CLI authenticated (if `--delete-repo`)
- PostgreSQL 14 running via Homebrew (if dropping database)

## Teardown steps

### 1. Detect project

Confirm this is a NEAN project by checking for:
- `nx.json`
- `apps/api/`
- `libs/shared/`

If any are missing, warn and ask the user to confirm before proceeding.

Record the **project root** (absolute path) for later deletion.

### 2. Detect GitHub remote

```bash
git remote get-url origin 2>/dev/null
```

- If a remote exists, extract `owner/repo` from the URL
- If no remote, skip GitHub steps

### 3. Detect database

Determine the database name:

1. Read `.env` for `DATABASE_NAME=...`
2. Fall back to the project directory name with `-` replaced by `_`
   (e.g., `hello-nean` → `hello_nean`)

Verify the database exists:

```bash
/opt/homebrew/opt/postgresql@14/bin/psql -U postgres -lqt | grep <db_name>
```

If the database doesn't exist, note it and skip database steps.

### 4. Show summary and confirm

Check for running dev servers first:

```bash
lsof -ti:3000,4200 2>/dev/null
```

If processes are found on ports 3000 or 4200, warn the user.

Display exactly what will happen:

```
Project:  /path/to/my-app
GitHub:   owner/repo (will be DELETED | will be KEPT)
Database: hello_nean (will be DROPPED | will be KEPT | not found)

⚠ Dev servers detected on ports 3000, 4200 — they will be killed.

This will permanently delete:
  - All local files in /path/to/my-app
  [- GitHub repository owner/repo (if --delete-repo)]
  [- PostgreSQL database hello_nean (unless --keep-db)]

Type the project name to confirm: _
```

**Do NOT proceed without explicit confirmation.**

### 5. Kill dev servers

If processes were detected on ports 3000 or 4200:

```bash
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:4200 | xargs kill -9 2>/dev/null
```

### 6. Delete GitHub repo (if --delete-repo)

```bash
gh repo delete owner/repo --yes
```

If this fails (permissions, network), stop and report — do not continue to
local deletion so the user can retry.

### 7. Drop database (unless --keep-db)

```bash
/opt/homebrew/opt/postgresql@14/bin/psql -U postgres -c 'DROP DATABASE IF EXISTS <db_name>;'
```

If this fails, warn but continue to local deletion — the database may already
be gone or in use.

**Never stop the postgresql@14 Homebrew service.** Other projects may depend on it.

### 8. Delete local project

```bash
cd ..
rm -rf /absolute/path/to/project
```

Use the absolute path recorded in step 1. Never use relative paths.

### 9. Confirm completion

Report what was deleted or kept:
- Dev servers: killed / none found
- GitHub repo: deleted / kept (with URL if kept)
- Database: dropped / kept / not found
- Local directory: deleted

## Safety

- Always confirm before destructive operations
- Show the full absolute path that will be deleted
- Never delete parent directories or anything outside the project root
- If GitHub deletion fails, stop — don't leave the user with a deleted
  local copy and a still-existing repo they can't find
- If database drop fails, warn but continue to local deletion
- Never stop the PostgreSQL Homebrew service (other projects may use it)
- Check for running dev servers and warn before killing them
