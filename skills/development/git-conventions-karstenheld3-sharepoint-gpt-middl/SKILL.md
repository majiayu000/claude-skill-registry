---
name: git-conventions
description: Apply when committing code, writing commit messages, or configuring .gitignore
---

# Git Conventions

## Verb Mapping

This skill implements:
- [COMMIT] - Create conventional commits
- [MERGE] - Merge branches following conventions

**Phases**: IMPLEMENT, DELIVER

## MUST-NOT-FORGET

- Use Conventional Commits: `<type>(<scope>): <description>`
- Types: feat, fix, docs, refactor, test, chore, style, perf
- Imperative mood, <72 chars, no period
- NEVER commit secrets: .env, *.cer, *.pfx, *.pem, *.key

## Commit Message Format

Use **Conventional Commits**: `<type>(<scope>): <description>`

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependencies, build changes
- **style**: Formatting, whitespace (no code logic change)
- **perf**: Performance improvement

### Guidelines

1. Use imperative mood ("add" not "added" or "adds")
2. Keep description under 72 characters
3. No period at the end
4. Scope should match module/folder name when applicable

### Examples

```
feat(crawler): add incremental crawl mode
fix(auth): handle expired tokens
docs: update README installation steps
refactor(domains): simplify source validation logic
chore: update dependencies to latest versions
```

## Safe Undo Commit

**CRITICAL**: Choose the right reset mode to avoid data loss.

### Undo Last Commit (Keep Files)

```bash
git reset --soft HEAD~1   # Undo commit, keep files STAGED
git reset HEAD~1          # Undo commit, keep files UNSTAGED
```

### Undo Last Commit (Discard Files) - DESTRUCTIVE

```bash
git reset --hard HEAD~1   # Undo commit AND DELETE all changes
```

**WARNING**: `--hard` deletes uncommitted files permanently (unless recoverable via reflog).

### Recovery After Accidental --hard Reset

If files were committed before reset, recover from reflog:

```bash
git reflog                              # Find commit hash (e.g., abc1234)
git checkout abc1234 -- path/to/file    # Recover specific file
git checkout abc1234 -- .               # Recover all files from that commit
```

### Recovery From Remote

If commit was pushed before local reset:

```bash
git fetch origin                        # Get latest from remote
git log --oneline origin/master -5      # Check what's on remote
git checkout origin/master -- path/to   # Recover file from remote
```

### Amend Last Commit (Not Yet Pushed)

```bash
git add <files>
git commit --amend -m "new message"     # Replace last commit
```

### Force Push After Amend/Reset (Remote Has Old Commit)

```bash
git push --force-with-lease             # Safer than --force
```

**Use `--force-with-lease`**: Fails if remote changed since last fetch (prevents overwriting others' work).

## .gitignore Rules

1. **NEVER commit secrets**: `.env` files, certificates (*.cer, *.pfx, *.pem, *.key), API keys
2. **Exclude large binaries**: Reinstallable tools (poppler, node_modules, .venv/) - save repo size
3. **Exclude build artifacts**: Generated files (dist/, __pycache__/, *.pyc)
4. **Track shared config**: `.vscode/`, `Set-*-Env.bat` (environment setup scripts)
5. **Use negation pattern**: Keep specific files with `!` prefix when excluding folders
6. **Add comments**: Document non-obvious exclusions in .gitignore

## Template

```gitignore
# Secrets (NEVER commit)
*.env
.env.*
*.cer
*.pfx
*.pem
*.key

# Python
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/

# Node.js
node_modules/
dist/
lib/
*.log

# IDE (keep .vscode/)
.vs/
bin/
obj/

# OS
.DS_Store

# Tools (reinstallable)
.tools/poppler/

# Temporary
*.tmp
.tmp_*
*.bak
```
