---
name: committing-changes
description: Use this skill when committing code changes, creating git commits, staging files for commit, or when the user asks to commit, save changes, or make a commit. Handles conventional commit format, explicit file staging, and commit message crafting.
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Recent commit messages (for style reference): !`git log --oneline -10`
- User-provided message override (optional): $ARGUMENTS

## Your task

Commit the work from this chat session using best practice conventions.

### Step 1: Identify Changed Files

Review the git status output above. Only stage files that were actually modified during this conversation. Do NOT use `git add -A` or `git add .` blindly.

### Step 2: Stage Files Explicitly

Add only the specific files that changed:
```bash
git add path/to/file1 path/to/file2
```

### Step 3: Craft the Commit Message

Follow conventional commits format:
- **feat**: New feature
- **fix**: Bug fix
- **refactor**: Code change that neither fixes nor adds
- **docs**: Documentation only
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

Structure:
```
<type>(<scope>): <short description>

<optional body with details>
```

Guidelines:
- Keep the subject line under 72 characters
- Use imperative mood ("add" not "added")
- Focus on the "why" not just the "what"
- Reference any relevant context from the conversation

### Step 4: Create the Commit

If user provided a message override in $ARGUMENTS, use that instead of crafting one.

Use a HEREDOC for proper formatting:
```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

<optional body>
EOF
)"
```

### Step 5: Verify Success

After committing, run `git status` to confirm the commit succeeded.

## Important

- Never stage files that weren't part of this session's work
- Never commit secrets, credentials, or .env files
- If no changes exist to commit, inform the user instead of creating an empty commit
- You MUST complete all steps in a single response using parallel tool calls where appropriate
