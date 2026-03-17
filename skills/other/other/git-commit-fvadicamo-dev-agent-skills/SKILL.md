---
name: git-commit
description: Creates git commits following Conventional Commits format with type/scope/subject. Use when user wants to commit changes, create commit, save work, or stage and commit. Enforces project-specific conventions from CLAUDE.md.
---

# Git commit

Creates git commits following Conventional Commits format.

## Recent project commits

!`git log --oneline -5 2>/dev/null`

## Quick start

```bash
# 1. Stage changes
git add <files>

# 2. Create commit
git commit -m "type(scope): subject"
```

## Project conventions

- Scope is **required** (kebab-case): `validation`, `auth`, `cookie-service`, `api`
- Additional type beyond standard CC: `security` (vulnerability fixes or hardening)
- HEREDOC for multi-line commits:

```bash
git commit -m "$(cat <<'EOF'
feat(validation): add URLValidator with domain whitelist

Implement URLValidator class supporting:
- Domain whitelist enforcement
- Dangerous scheme blocking

Addresses Requirement 31
Part of Task 5.1
EOF
)"
```

## Important rules

- **ALWAYS** check CLAUDE.md conventions first - use project format if it differs
- **ALWAYS** include scope in parentheses
- **ALWAYS** use present tense imperative verb for the subject
- **NEVER** end subject with a period
- **NEVER** exceed 50 chars in the subject line
- **NEVER** use generic messages ("update code", "fix bug", "changes")
- Group related changes into a single focused commit

## References

- `references/commit_examples.md` - Extended examples by type, good/bad comparisons
