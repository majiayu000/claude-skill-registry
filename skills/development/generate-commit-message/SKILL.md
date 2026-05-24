---
name: generate-commit-message
description: Generate a commit message for staged changes
disable-model-invocation: true
---

# Generate Commit Message

Analyze staged changes and generate a single-line commit message.

## Instructions

1. **Check for staged changes**
   - Run `git diff --cached` to see what's staged
   - If nothing is staged, check `git status` and suggest what to stage

2. **Check project conventions**
   - Run `git log --oneline -10` to see recent commit style
   - Match the existing format (conventional commits, prefixes, etc.)

3. **Generate a single-line commit message**

## Best Practices

- **50 characters or less** - keep it concise
- **Imperative mood** - "Add feature" not "Added feature" or "Adds feature"
- **Capitalize** the first letter
- **No period** at the end
- **What and why**, not how

If the project uses [Conventional Commits](https://www.conventionalcommits.org/), use the format:
```
type(scope): description
```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Output

Print the commit message in a code block:

```
Add user authentication endpoint
```
