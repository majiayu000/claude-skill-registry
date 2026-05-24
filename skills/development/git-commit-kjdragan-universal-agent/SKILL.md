---
name: git-commit
description: "Stage all changes, create a helpful commit message, and push to remote. Use this when the user wants to quickly commit and push their changes without manually staging files or writing a commit message."
---

# Git Commit Skill

Quickly stage all changes, create a helpful commit message, and push to remote.

## Usage

When user invokes this skill, execute the following steps:

1. **Check git status** - See what files have changed
2. **Stage all changes** - Add all modified/new files
3. **Write a helpful commit message** - Based on the actual changes
4. **Push to remote** - Push to the current branch's upstream

## Commands

```bash
# Check current status and changes
git status
git diff --staged
git diff

# Stage all changes
git add -A

# Commit with helpful message (use HEREDOC for multi-line)
git commit -m "$(cat <<'EOF'
<summary line>

<optional detailed description>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Push to remote (uses current branch's upstream)
git push
```

## Commit Message Guidelines

- **Summary line**: 50 chars or less, describes what changed and why
- **Imperative mood**: "Add feature" not "Added feature" or "Adds feature"
- **Focus on the why**: Explain the reason for changes, not just the mechanics


## Examples

```
feat: Add slash command for quick git commits

Implements a new skill that stages all changes, generates
a helpful commit message based on git diff, and pushes
to remote repository.

Co-Authored-By: Claude <noreply@anthropic.com>
```

```
fix: Resolve Pydantic V2 deprecation warnings

Updated model definitions to use Pydantic V2 syntax
and removed deprecated field() calls.

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Safety Checks

Before committing, verify:
- No sensitive files (`.env`, credentials, secrets)
- No generated binaries or large artifacts accidentally staged
- Branch is correct for the changes being made

If any issues are found, warn the user and ask before proceeding.