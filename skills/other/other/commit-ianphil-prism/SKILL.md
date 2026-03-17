---
name: commit
description: This skill should be used when the user asks to "commit changes", "push my code", "commit and push", "save my work", or wants to stage all changes and push to remote.
---

# Commit

Stage all changes, create a commit with a descriptive message, and push to the remote branch.

## Workflow

1. Run `git status` to review changes
2. Run `git diff` to understand what changed
3. Run `git log -3 --oneline` to match commit message style
4. Stage relevant files (prefer specific files over `git add -A`)
5. Create commit with descriptive message following repository conventions
6. Push to remote branch

## Commit Message Format

```
<type>: <short description>

<optional body explaining why>

Co-Authored-By: Claude <model>
```

Common types: feat, fix, chore, docs, refactor, test