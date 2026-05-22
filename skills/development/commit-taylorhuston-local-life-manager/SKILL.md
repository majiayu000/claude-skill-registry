---
name: commit
description: "Create git commits in spaces/[project]/ with conventional message format. Use for saving progress with quality checks and proper commit messages."
model: claude-sonnet-4-20250514
allowed-tools: Read, Glob, Grep, Bash
---

# /commit

Create git commits in `spaces/[project]/` with quality checks and conventional message formatting.

## Usage

```bash
/commit yourbench                     # Interactive commit
/commit yourbench "feat: add auth"    # Direct with message
/commit coordinatr --amend            # Amend last commit (safety checks)
/commit yourbench "fix: typo" --no-verify  # Skip hooks
```

## Two Repos Involved

```
Meta-repo (ideas/):          spaces/yourbench/
├── ideas/yourbench/         ├── src/
│   ├── specs/               ├── tests/
│   └── issues/              └── .git/  <- Project git
├── .claude/
└── .git/  <- Meta-repo git
```

**Auto-detect behavior:**
- Only `spaces/[project]/` changed -> commit in project repo
- Only `ideas/` or meta-repo changed -> commit in meta-repo
- Both changed -> ask: "Commit to both repos? (project/meta/both)"

## Execution Flow

### 1. Detect Changes

```bash
# Check meta-repo
git status --porcelain ideas/ .claude/ shared/ resources/

# Check project repo
git -C spaces/[project] status --porcelain
```

### 2. Run Quality Checks (unless --no-verify)

```bash
npm test  # or pytest, cargo test, etc.
npm run lint
```

### 3. Review Changes

```bash
git status
git diff --staged
```

### 4. Generate Commit Message

**Conventional commit format:**
```
type(scope): description

[optional body]

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance

**Auto-detect type from changes:**
- New files in `src/` -> `feat`
- Changes to existing behavior -> `fix` or `refactor`
- Only test files -> `test`
- Only docs -> `docs`

### 5. Link to Issue (if applicable)

If on feature branch like `feature/001-auth`:
```
feat(001): implement user authentication

Refs: TASK-001
```

### 6. Execute Commit

```bash
cd spaces/yourbench
git add .
git commit -m "message..."
```

## Amend Mode

**Safety checks before amending:**
1. Not pushed to remote: `git log @{u}..HEAD`
2. You're the author: `git log -1 --format='%ae'`

## Branch-Aware Messages

| Branch | Commit Type |
|--------|-------------|
| `feature/001-auth` | `feat(001): ...` |
| `bugfix/002-login` | `fix(002): ...` |
| `main` / `develop` | No issue reference |

## Error Handling

| Error | Resolution |
|-------|------------|
| Project not found | Check `spaces/[project]/` exists |
| Not a git repo | Run `git init` in project |
| Tests failing | Fix tests before committing |
| Nothing to commit | No staged/unstaged changes |
| Amend pushed commit | Cannot amend, create new commit |
