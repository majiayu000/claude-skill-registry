# Git Safety Protocol

Critical rules to prevent accidental data loss from destructive git operations.

## Never use git checkout to revert changes

**MANDATORY RULES:**

- **NEVER run `git checkout -- <file>`** without first examining what you're about to destroy
- **ALWAYS use `git diff <file>`** to see exactly what changes will be lost
- **MANUALLY undo changes** by editing files to revert specific problematic sections
- **Preserve valuable work** - if user says changes are bad, ask which specific parts to revert
- **`git checkout` destroys ALL changes** - this can eliminate hours of valuable progress
- **When user asks to "undo" changes**: Read the current file, identify problematic sections, and manually edit to fix them

**Why this matters**: Using `git checkout` blindly can destroy sophisticated implementations, complex prompts, provider-specific logic, and other valuable work that took significant time to develop.

## Destructive commands requiring explicit approval

**NEVER run these commands without explicit user approval:**

| Command | Effect |
|---------|--------|
| `git reset --hard` | Destroys uncommitted changes permanently |
| `git checkout -- .` | Discards all working directory changes |
| `git clean -fd` | Deletes untracked files permanently |
| `git stash drop` | Deletes stashed changes |
| `git push --force` | Overwrites remote history (dangerous for shared branches) |

## Before any git operation

1. Run `git status` first to check for uncommitted changes
2. If there are uncommitted changes, STOP and ASK the user before proceeding
3. Suggest `git stash` to preserve changes if needed

## Handling revert requests

**If user asks to "revert" something:**

1. First clarify: revert committed changes or uncommitted changes?
2. Show what will be affected before doing anything
3. Get explicit confirmation for destructive operations

**If user says "undo my changes":**

1. Read the current file
2. Identify which specific sections are problematic
3. Manually edit to fix those sections
4. Preserve everything else

## Quick checklist

Before git operations:
- [ ] Have I run `git status` first?
- [ ] Are there uncommitted changes I might destroy?
- [ ] Have I used `git diff` to see what will be affected?
- [ ] Do I have explicit user approval for any destructive command?
- [ ] Am I preserving valuable work?

When asked to revert:
- [ ] Did I clarify what specifically should be reverted?
- [ ] Am I manually editing instead of using checkout?
- [ ] Am I preserving work not mentioned in the revert request?

## Why these rules exist

These rules exist because careless git operations can destroy days of work. A single `git checkout -- .` can eliminate sophisticated implementations, complex logic, and carefully crafted code that took significant time to develop.

**When in doubt, ask first.**
