---
name: commit
description: Create a git commit with well-structured message and push to remote following BetterPortal project standards
disable-model-invocation: true
argument-hint: [message or description]
allowed-tools: Bash(git *)
---

# Git Commit Skill

Create a git commit for staged changes following BetterPortal project standards and push to remote.

## Commit Message Format

Follow the project's existing pattern:
- **First line**: Brief summary starting with a verb (max 72 chars)
  - Examples: "Add", "Fix", "Update", "Remove", "Eliminate"
- **Blank line**
- **Body**: Detailed bullet points explaining changes (if needed)
- **Footer**: `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`

## Process

1. **Review changes**: Run `git status` and `git diff --cached` to see what will be committed
2. **Review recent commits**: Run `git log --oneline -5` to match the project's message style
3. **Generate message**:
   - If argument provided: Use it as the first line
   - If no argument: Analyze the diff and create appropriate message
   - Add detailed body with bullet points for multiple changes
   - Always add Co-Authored-By footer
4. **Create commit**: Use heredoc format for multi-line messages:
   ```bash
   git commit -m "$(cat <<'EOF'
   First line summary

   - Detailed point 1
   - Detailed point 2

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   EOF
   )"
   ```
5. **Verify**: Run `git log -1 --stat` to confirm commit was created correctly
6. **Push to remote**: Run `git push` to push the commit to the remote repository

## Examples from BetterPortal History

Good commit messages from this project:
- `Add configurable history limit and bookmark conversion feature`
- `Eliminate redirect flash for same-directory navigation`
- `Fix tenant switching to use correct GUID and preserve query parameters`
- `Remove token extraction and add privacy documentation for Chrome Web Store`

## Usage

```bash
# With message argument
/commit Add keyboard shortcut for search

# Without argument (analyze diff and generate message)
/commit

# Complex change (will generate detailed body)
/commit Refactor history pruning logic
```

## Important Notes

- **Always include Co-Authored-By footer** for commits made with Claude
- **Follow existing verb patterns**: Add, Fix, Update, Remove, Eliminate, Refactor
- **Be specific**: "Fix tenant switching logic" not "Fix bug"
- **No emoji** unless explicitly requested
- **Check staged changes first**: Don't commit if nothing is staged
- **Automatically pushes to remote**: After committing, the changes will be pushed to the remote repository
- **Bump the version**: When committing feature or bug fix changes, bump the version in both `src/manifest.json` and `package.json` (keep them in sync). Use patch version increments (e.g., 1.0.64 → 1.0.65). Include the version bump in the same commit as the changes.
