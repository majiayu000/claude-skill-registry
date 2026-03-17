---
name: ship
description: Quickly add, commit, and push changes to the current branch
---

# ship

Quickly add, commit, and push changes to the current branch.

## Arguments

- `message` (optional): Commit message. If not provided, will prompt the user for one.

## Instructions

1. Run `git status` to check the current state of the repository
2. If there are no changes to commit, inform the user and exit
3. Parse the commit message from args:
   - If args starts with `-m ` or `--message `, extract the message after the flag (removing quotes if present)
   - Otherwise, treat the entire args string as the message (removing surrounding quotes if present)
   - If args is empty or just whitespace, ask the user for a commit message using AskUserQuestion
4. Run `git add .` to stage all changes
5. Create a commit with the message using the git commit protocol from the system instructions:
   - Format the message properly with a Co-Authored-By line at the end
   - Use a heredoc for proper formatting: `git commit -m "$(cat <<'EOF'\n[message]\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>\nEOF\n)"`
6. Run `git push` to push the changes to the remote
7. Confirm success to the user with a summary of what was pushed (include commit message and branch)

## Example Usage

```
/ship "Add new printer case study"
/ship -m "Fix typography issues"
/ship
```

## Notes

- Always follow git safety protocols
- Show git status before committing
- Confirm successful push with the user
- If push fails, report the error clearly
