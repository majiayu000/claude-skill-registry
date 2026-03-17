---
name: install-precommit
description: Install the pre-commit review hook that forces you to understand changes before committing. Use when you want to enable commit reviews or when setting up a new project.
tools: Read, Write, Bash
user-invocable: true
---

You are helping the user install the pre-commit review hook.

## What This Hook Does

The pre-commit review hook runs before every `git commit` and:
1. Shows files being committed with their status (added/modified/deleted)
2. Shows lines added and removed
3. Detects potentially sensitive files (.env, secrets, keys)
4. Detects debug statements (console.log, print, debugger, etc.)
5. Shows new dependencies being added
6. Shows TODOs being introduced
7. Requires user confirmation (y/n/d for diff) before proceeding

This prevents "vibe coding" - blindly committing AI-generated code without understanding it.

## Installation Steps

1. **Check prerequisites:**
   - Verify this is a git repository (`.git` directory exists)
   - Check if a pre-commit hook already exists

2. **Create the hook script:**
   If `.claude/hooks/pre-commit-review.sh` doesn't exist, create it with the standard implementation.

3. **Install as git hook:**
   - Create `.git/hooks/` directory if needed
   - Copy or symlink the script to `.git/hooks/pre-commit`
   - Make it executable

4. **Verify installation:**
   - Confirm the hook is in place
   - Show the user how to test it
   - Explain how to bypass if needed

## Hook Script Source

The pre-commit hook script is located at `.claude/hooks/pre-commit-review.sh`.

**Do NOT embed a copy here** - always use the canonical version from the hooks directory. This ensures updates to the hook are applied everywhere.

If `.claude/hooks/pre-commit-review.sh` doesn't exist in the user's project, they may need to copy it from a template or create it based on their needs.

## After Installation

Tell the user:
1. The hook is now active for all future commits
2. To skip the review (not recommended): `SKIP_PRE_COMMIT_REVIEW=1 git commit -m "message"`
3. To uninstall: `rm .git/hooks/pre-commit`

## Output Format

```
[OK] Pre-commit review hook installed

Location: .git/hooks/pre-commit
Source: .claude/hooks/pre-commit-review.sh

The hook will run before every commit, showing:
- Files being committed
- Lines added/removed
- Potential issues (sensitive files, debug statements)
- Requires your confirmation before proceeding

To test: stage some files and run `git commit`
To skip: SKIP_PRE_COMMIT_REVIEW=1 git commit -m "message"
To remove: rm .git/hooks/pre-commit
```
