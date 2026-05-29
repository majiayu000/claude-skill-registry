---
name: ios-teardown
description: Tear down an iOS project created by /ios-kit. Removes local files, git hooks, and optionally deletes the GitHub repo.
argument-hint: "[--keep-repo] [--keep-local] [--dry-run]"
allowed-tools: Bash, Read, Glob, Grep
---

## Purpose

Reverse the setup performed by `/ios-kit` (`/ios-scaffold` → `/github-hooks` → `/github-secure`). Removes local project files, git hooks, and optionally deletes the GitHub repo.

## Arguments

- `--keep-repo` — Keep the GitHub repo (default: **delete** the repo)
- `--keep-local` — Keep local files, only clean up remote resources
- `--dry-run` — Show what would be deleted without doing it

## Workflow

### 1. Detect project

Verify the current directory is an ios-kit project:

1. Check for `project.yml`, `App/Sources/`, and `CLAUDE.md`
2. Read `project.yml` to extract the project name
3. Detect GitHub remote: `git remote get-url origin`
4. Extract `owner/repo` from the remote URL

If any check fails, abort with a clear message about what's missing.

### 2. Pre-flight safety checks

Before proceeding, check for uncommitted or unpushed work:

1. **Uncommitted changes** — Run `git status --porcelain`. If output is non-empty, warn the user and list the changes. Require explicit confirmation to continue.
2. **Unpushed commits** — Run `git log @{upstream}..HEAD --oneline 2>/dev/null`. If there are unpushed commits, warn the user and list them. Require explicit confirmation to continue.
3. **`gh` auth** — Run `gh auth status`. If not authenticated and repo deletion is needed (no `--keep-repo`), abort and instruct the user to run `gh auth login`.

### 3. Dry-run report

**Always display this report before any destructive action**, regardless of `--dry-run`:

```
=== Teardown Plan ===

Project: <project-name>
GitHub:  <owner/repo>

Will delete:
  ☐ GitHub repo: <owner/repo>          (skip: --keep-repo)
  ☐ Branch protection on main           (skip: --keep-repo)
  ☐ Local project directory: <path>     (skip: --keep-local)
  ☐ Git hooks path config               (skip: --keep-local)

Will keep:
  ☐ <anything skipped by flags>
```

- If `--dry-run`, print the report and **stop here**.
- Otherwise, ask: **"Proceed with teardown? (yes/no)"** — require the user to confirm.

### 4. Remove GitHub resources (unless `--keep-repo`)

Execute in this order (protections must be removed before repo deletion):

1. Remove branch protection:
   ```bash
   gh api -X DELETE /repos/{owner}/{repo}/branches/main/protection
   ```
2. Delete the repo:
   ```bash
   gh repo delete {owner}/{repo} --yes
   ```

If `--keep-repo`:
- Skip all repo operations
- Suggest archiving: "Consider archiving with `gh repo archive {owner}/{repo} --yes`"
- Print the GitHub URL for future reference

### 5. Clean up local (unless `--keep-local`)

1. Reset git hooks path (if configured):
   ```bash
   git config --unset core.hooksPath
   ```
2. Capture the project directory path and navigate to the parent:
   ```bash
   PROJECT_DIR=$(pwd)
   cd ..
   ```
3. Delete the project directory:
   ```bash
   rm -rf "$PROJECT_DIR"
   ```

### 6. Confirm

Print a summary of what was deleted:

```
=== Teardown Complete ===

Deleted:
  ✓ GitHub repo: <owner/repo>
  ✓ Local directory: <path>
  ✓ Git hooks config

Kept:
  — <anything preserved by flags>
```

If the repo was kept, include: `GitHub: https://github.com/<owner>/<repo>`

## Safety guardrails

- **Never run without confirmation** — always show the dry-run report and require explicit "yes"
- **Check for uncommitted changes** — warn and require override
- **Check for unpushed commits** — warn and require override
- **Verify `gh auth`** before GitHub operations
- **No `--force` flag** — destructive actions always require confirmation
- **Order matters** — remove branch protection before repo deletion
- **No `Write` tool** — this skill only deletes, never creates files
