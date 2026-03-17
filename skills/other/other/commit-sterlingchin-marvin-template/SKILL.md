---
name: commit
description: |
  Review changes and create clean git commits. Use when user types /commit or asks to commit changes. Creates well-structured commits with proper messages.
license: MIT
compatibility: marvin
metadata:
  marvin-category: work
  user-invocable: true
  slash-command: /commit
  model: default
  proactive: false
---

# Commit Skill

Review changes and create clean, well-structured git commits.

## When to Use

- User types `/commit`
- User asks to "commit changes" or "save to git"
- After completing a piece of work

## Process

### Step 1: Check Current Status
```bash
git status --short
git diff --stat
```

Review what's changed:
- New files
- Modified files
- Deleted files

### Step 2: Review Changes
```bash
git diff
```

Understand what changed and why. Group related changes.

### Step 3: Check Recent History
```bash
git log --oneline -5
```

Match the repository's commit style.

### Step 4: Create Logical Commits

Group files by type and create separate commits:

| Category | Files | Commit Type |
|----------|-------|-------------|
| Features | New functionality | `feat:` |
| Bug fixes | Fixes | `fix:` |
| Documentation | `*.md`, docs | `docs:` |
| Configuration | Config files | `chore:` |
| State/Sessions | `state/`, `sessions/` | `chore:` |

### Step 5: Stage and Commit

For each group:
```bash
git add <specific files>
git commit -m "$(cat <<'EOF'
<type>: <short description>

<optional longer description>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 6: Push (if requested)
```bash
git push
```

## Commit Message Guidelines

**Format:**
```
<type>: <description>

[optional body]

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:**
- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation
- `chore:` — Maintenance, config, state updates
- `refactor:` — Code restructuring
- `test:` — Tests

**Good examples:**
- `feat: add email notification system`
- `fix: resolve login timeout issue`
- `docs: update API documentation`
- `chore: session log and state update`

**Bad examples:**
- `update` (too vague)
- `fixed stuff` (not descriptive)
- `WIP` (don't commit work in progress)

## Output Format

```
**Changes:**
- {file 1}: {what changed}
- {file 2}: {what changed}

**Commits created:**
1. `<type>: <message>`
2. `<type>: <message>`

{Pushed to origin/main | Ready to push}
```

---

*Skill created: 2026-01-22*
