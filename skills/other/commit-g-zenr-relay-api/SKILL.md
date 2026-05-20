---
name: commit
description: Smart commit — validate, stage, and commit with a conventional commit message
disable-model-invocation: true
---

Create a clean, validated commit for the current changes.

## Step 1 — Pre-commit Validation
Run the test and type-check commands (see project config).
If either fails: **STOP**. Fix the issues first — never commit broken code.

## Step 2 — Review Changes
```bash
git status
git diff --staged
git diff
```
Understand what changed, which files are affected, and which layer (core/service/api/tests).

## Step 3 — Stage Files
- Stage only relevant files — never `git add .` blindly
- NEVER stage `.env`, credentials, or secrets
- NEVER stage build artifacts (see stack concepts in project config for list)
- Verify `.gitignore` covers sensitive files

## Step 4 — Generate Commit Message
Use conventional commit format:
```
<type>(<scope>): <short description>

<optional body explaining why, not what>
```

**Types:**
- `feat` — New feature or endpoint
- `fix` — Bug fix
- `refactor` — Code restructuring without behavior change
- `test` — Adding or updating tests
- `docs` — Documentation changes
- `chore` — Config, dependencies, tooling
- `security` — Security-related changes

**Scopes:** `api`, `core`, `service`, `auth`, `config`, `middleware`, `tests`, `docker`

## Step 5 — Commit
```bash
git commit -m "<conventional message>"
```

## Step 6 — Verify
```bash
git log --oneline -1
git status
```
Confirm the commit was created and working tree is clean.