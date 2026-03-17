---
name: commit
description: Stage changes and create git commits with conventional commit messages. Use when asked to "commit", "stage and commit", "save changes", or after completing implementation tasks. Alias for /git/cm.
allowed-tools: Bash, Read, Glob, Grep
---

# Git Commit Skill

Stage changes and create well-structured git commits following Conventional Commits format.

## Workflow

### Step 1: Analyze Changes

```bash
# Check current status (never use -uall flag)
git status

# See staged changes
git diff --cached

# See unstaged changes
git diff

# Check recent commit style
git log --oneline -5
```

### Step 2: Stage Changes

```bash
# Stage all changes
git add .

# Or stage specific files
git add <file-path>
```

### Step 3: Generate Commit Message

Analyze staged changes and generate message following **Conventional Commits**:

```
<type>(<scope>): <subject>
```

#### Type Detection

| Change Pattern | Type |
|----------------|------|
| New file/feature | `feat` |
| Bug fix, error handling | `fix` |
| Code restructure | `refactor` |
| Documentation only | `docs` |
| Tests only | `test` |
| Dependencies, config | `chore` |
| Performance improvement | `perf` |
| Formatting only | `style` |

#### Scope Rules

Extract from file paths:
- `src/auth/` → `auth`
- `.claude/skills/` → `claude-skills`
- `libs/platform-core/` → `platform-core`
- Multiple unrelated areas → omit scope

#### Subject Rules

- Imperative mood ("add" not "added")
- Lowercase start
- No period at end
- Max 50 characters

### Step 4: Commit

Use HEREDOC for proper formatting:

```bash
git commit -m "$(cat <<'EOF'
type(scope): subject

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Step 5: Verify

```bash
git status
git log -1
```

## Examples

```
feat(employee): add department filter to list
fix(validation): handle empty date range
refactor(auth): extract token validation to service
chore(deps): update Angular to v19
chore(claude-skills): add commit skill
docs(readme): update installation instructions
```

## Critical Rules

- **DO NOT push** to remote unless explicitly requested
- **Review staged changes** before committing
- **Never commit** secrets, credentials, or .env files
- **Never use** `git commit --amend` unless explicitly requested AND the commit was created in this session AND not yet pushed
- **Never skip** hooks with `--no-verify` unless explicitly requested
- Include attribution footer: `Generated with [Claude Code](https://claude.com/claude-code)`
