---
name: commit
description: Create a git commit with proper message format and co-authorship
disable-model-invocation: true
argument-hint: [optional commit message hint]
---

# Git Commit Skill

Create a well-formatted git commit for staged changes.

## Process

1. **Analyze Changes**
   - Run `git status` to see all untracked and modified files (never use -uall flag)
   - Run `git diff --cached` to see staged changes
   - Run `git diff` to see unstaged changes
   - Run `git log --oneline -5` to see recent commit message style

2. **Draft Commit Message**
   - Summarize the nature of changes (new feature, enhancement, bug fix, refactoring, test, docs)
   - Use correct verb: "add" for new features, "update" for enhancements, "fix" for bugs
   - Keep message concise (1-2 sentences) focusing on "why" not "what"
   - Follow repository's existing commit message style

3. **Safety Checks**
   - DO NOT commit files containing secrets (.env, credentials.json, etc.)
   - Warn user if they request to commit sensitive files
   - Stage specific files by name, avoid `git add -A` or `git add .`

4. **Create Commit**
   Use HEREDOC format for proper formatting:
   ```bash
   git commit -m "$(cat <<'EOF'
   Your commit message here.

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
   EOF
   )"
   ```

5. **Verify Success**
   - Run `git status` after commit to confirm

## Rules

- NEVER update git config
- NEVER use destructive commands (push --force, reset --hard, checkout ., clean -f)
- NEVER skip hooks (--no-verify, --no-gpg-sign)
- NEVER amend commits unless explicitly requested
- NEVER use -i flag (interactive mode not supported)
- NEVER push unless explicitly requested
- If pre-commit hook fails, fix issues and create NEW commit (don't amend)

## User Request
$ARGUMENTS
