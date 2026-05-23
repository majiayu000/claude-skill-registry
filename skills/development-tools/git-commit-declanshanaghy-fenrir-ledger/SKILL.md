---
name: git-commit
description: "Git commit convention for all Fenrir Ledger team members. Use this skill whenever committing code, docs, or any artifacts to the repository. Defines the commit message format, .gitignore rules, and pre-commit checklist."
---

# Git Commit Convention

All team members must follow this commit format when committing to the Fenrir Ledger repository.

## Commit Message Format

```
<one-line description under 80 characters>

# Summary of changes

## Summary

- One-liner describing change 1
- One-liner describing change 2
- One-liner describing change 3
```

### Rules

1. **First line**: Imperative mood, under 80 characters, lowercase start. Describes *what* the commit does.
2. **Blank line**: Exactly one blank line after the first line.
3. **H1 header**: `# Summary of changes` — always this exact text.
4. **H2 section**: `## Summary` — bullet list of one-liner descriptions of each change.
5. Each bullet should be a single line, starting with `- `.
6. No trailing blank lines after the last bullet.

### Examples

**Good:**
```
add Sprint 1 architecture ADRs and system design

# Summary of changes

## Summary

- Add ADR-001 integration architecture
- Add ADR-002 frontend technology choice
- Add ADR-003 deployment architecture
- Add system design doc with Mermaid component diagram
- Add API contracts
```

**Good:**
```
implement user authentication service

# Summary of changes

## Summary

- Add AuthService class with token validation
- Register API endpoint for login
- Add constants file with auth defaults
- Wire up event listener for session expiry
```

**Bad:**
```
Updated stuff    ← vague, no detail

changes          ← useless

Add ADR-001 integration architecture for the project's custom integration setup
                 ← over 80 characters
```

## Post-Commit: Always Push to GitHub

After every successful commit, immediately push to the remote:

```bash
git push origin <current-branch>
```

This is mandatory — no exceptions. Every commit must be pushed. The repo should never have local-only commits sitting unpushed. If the push fails (auth, network, etc.), report it immediately and do not continue with further work until the push succeeds.

If no remote is configured yet, set one up first:
```bash
git remote add origin <repo-url>
git push -u origin <branch>
```

## Pre-Commit Checklist

Before every commit, verify:

- [ ] `.env` is NOT staged (check `git status`)
- [ ] No secrets, tokens, or credentials in any staged file
- [ ] `.gitignore` includes: `.env`, `*.env`, `.env.*`, `!.env.example`
- [ ] All Mermaid diagrams render correctly (valid syntax)
- [ ] No TODO/FIXME/HACK comments unless intentional and tracked
- [ ] Files are in the correct sprint/team directory structure

## .gitignore Baseline

Every repo must have at minimum:

```
# Secrets - NEVER commit
.env
*.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/

# Node/Frontend
node_modules/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## Branch Workflow (mandatory)

**NEVER commit directly to `main`.** All work — features, fixes, docs, chores — happens on a branch.

### Before starting any work
1. Ensure you are on `main` and it is up to date:
   ```bash
   git checkout main && git pull origin main
   ```
2. Create a branch:
   ```bash
   git checkout -b <type>/<short-description>
   ```
3. Do your work, commit, and push the branch.
4. Open a PR against `main`.
5. Merge only via PR — never `git push origin main` directly.

### Branch naming convention
- `feat/short-description` — new feature or story work
- `fix/short-description` — bug fix
- `chore/short-description` — maintenance, config, tooling
- `docs/short-description` — documentation only

### Examples
```
feat/loki-mode-easter-egg
fix/card-form-scroll-on-error
chore/update-gitignore-playwright
docs/adr-007-storage-strategy
```
