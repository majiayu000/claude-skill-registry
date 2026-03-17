---
name: commit-helper
description: Generate clear, conventional commit messages from git diffs. Use when writing commit messages, reviewing staged changes, or preparing commits.
---

# Commit Helper

Generate well-structured commit messages following conventional commit format.

## Instructions

1. Run `git diff --staged` to see staged changes
2. Analyze the changes to understand:
   - What files were modified
   - What type of change (feat, fix, refactor, docs, etc.)
   - The scope/component affected
3. Generate a commit message with:
   - Summary line under 50 characters
   - Type prefix (feat, fix, docs, refactor, test, chore)
   - Optional scope in parentheses
   - Detailed body explaining what and why

## Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code restructuring without behavior change
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## Best Practices

- Use present tense ("Add feature" not "Added feature")
- Explain what and why, not how
- Keep summary concise but descriptive
- Reference issue numbers when applicable

## Example Output

```
feat(auth): add OAuth2 support for GitHub login

- Implement OAuth2 flow with PKCE
- Add token refresh mechanism
- Store tokens securely in encrypted storage

Closes #123
```
