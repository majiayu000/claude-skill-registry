---
name: rewrite-history
description: 'Rewrite branch into clean, narrative-quality commits. Creates backup, reimplements on fresh branch, verifies byte-identical, then replaces original branch history.'
---

Rewrite the current branch's history into clean, narrative-quality commits suitable for code review.

## Goal

Transform messy development history into a logical story reviewers can follow commit-by-commit. Original branch is rewritten; backup preserved for rollback.

## Arguments

`$ARGUMENTS` = optional flags (`--auto` skips interactive approval)

## Preconditions

Abort with clear error if:

- On main/master branch
- Uncommitted changes exist
- No commits to rewrite (branch matches main)

## Execution

1. **Create backup branch**: `{branch}-backup-{timestamp}` — permanent until manually deleted
2. **Analyze the diff** between current branch and main—understand the complete change set
3. **Create temp branch** from main for clean reimplementation
4. **Plan the narrative**—structure changes into logical, self-contained commits (foundations → features → polish)
5. **Reimplement** by recreating changes commit-by-commit with conventional commit messages; use `--no-verify` for intermediate commits
6. **Verify byte-identical**: `git diff {original-branch}` MUST be empty—abort if any difference
7. **Replace original branch**: point original branch to clean history (final commit runs hooks normally)
8. **Offer to push** with `--force-with-lease`

## Verification Requirement

The byte-identical check is non-negotiable. If `git diff {backup-branch}` shows ANY difference after reimplementation:

- Abort immediately
- Report exactly what differs
- Leave backup branch intact for recovery

## Constraints

- Analyze the complete diff only—ignore original commit history
- One concern per commit—atomic, independently revertible
- Conventional commit messages: `type(scope): description`
- Never add "Co-Authored-By" or "Generated with Claude Code"
- Always use `--force-with-lease` for push (never `--force`)

## Interactive Mode

Unless `$ARGUMENTS` contains `--auto`:

- Present proposed commit plan before execution
- Allow adjustment or cancellation

## Rollback

If anything goes wrong: `git reset --hard {branch}-backup-{timestamp}`

## Output

Report commit count, backup branch name, and the new commit log.
