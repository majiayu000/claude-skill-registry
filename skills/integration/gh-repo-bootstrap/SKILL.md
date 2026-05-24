---
name: gh-repo-bootstrap
description: Create a new GitHub repository with the gh CLI and bootstrap a local project in ~/projects with git init, README, remote setup, and initial push. Use when the user asks to create a repo (public/private) in their account, set up the local folder, add the upstream remote, and push the first commit.
---

# GH Repo Bootstrap

## Overview
Create a GitHub repo in the authenticated account and initialize a matching local project under `~/projects/<name>` with a git repo, initial commit, remote, and upstream push using the bundled script.

## Workflow

### 1) Collect inputs
- Require: repo name, visibility (`public` or `private`).
- Optional: description, owner/org (if not default account), gitignore template, license key, remote name, projects directory, README toggle, initial commit message.

### 2) Verify prerequisites
- Confirm `gh` is installed and authenticated (`gh auth status`).
- Confirm `git` is installed and `user.name` + `user.email` are configured.
- Confirm `~/projects` exists or can be created.

### 3) Run the script
Use the bundled script to create the local repo, commit, create the remote, and push.

```bash
python3 scripts/gh_repo_bootstrap.py <name> --visibility public|private [options]
```

### 4) Report results
Return the local path, remote URL, and current branch.

## Examples

Minimal public repo:
```bash
python3 scripts/gh_repo_bootstrap.py my-app --visibility public
```

Private repo with description:
```bash
python3 scripts/gh_repo_bootstrap.py my-app --visibility private --description "My new project"
```

Create repo in an organization:
```bash
python3 scripts/gh_repo_bootstrap.py my-app --visibility public --owner my-org
```

Add gitignore + license templates:
```bash
python3 scripts/gh_repo_bootstrap.py my-app --visibility public --gitignore Go --license mit
```

Skip README and customize initial commit message:
```bash
python3 scripts/gh_repo_bootstrap.py my-app --visibility public --no-readme --commit-message "Initial scaffold"
```

## Notes
- Fail safely if the target directory exists and is not empty, or if the GitHub repo already exists.
- Create `README.md` by default; use `--no-readme` to skip it.
- Fetch gitignore and license templates via `gh api` only when requested.
- Use `--projects-dir` to override the default `~/projects` root.

## Scripts
- `scripts/gh_repo_bootstrap.py`: canonical automation for local setup, remote creation, and initial push.
