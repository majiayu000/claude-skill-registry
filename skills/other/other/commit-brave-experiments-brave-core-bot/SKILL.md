---
name: commit
description: "Commit changes without Co-Authored-By attribution. Creates logical, atomic commits."
argument-hint: "[branch] [push]"
---

# Commit Without Attribution

Create git commits without the Co-Authored-By attribution line. Each commit should be a logical unit of work.

## Arguments

Parse the arguments string for these keywords (order doesn't matter):

| Keyword | Effect |
|---------|--------|
| `branch` | Create a new branch off the current branch before committing (descriptive name based on changes) |
| `push` | Push after all commits succeed |

Examples:
- `/commit` — commit on current branch, no push
- `/commit push` — commit on current branch, then push
- `/commit branch push` — create new branch, commit, then push
- `/commit branch` — create new branch, commit, no push

## Current State

- Branch: !`git branch --show-current`
- Status: !`git status --short`

## Steps

1. If `branch` was passed, create a new branch off the current branch before proceeding (use a descriptive branch name based on the changes).
2. Run `git diff` to review the changes.
3. Identify logical units of work (may require multiple commits).
4. For each logical unit:
   - Draft an appropriate commit message
   - Stage only the files relevant to that unit with `git add`
   - Commit with the message **WITHOUT** the Co-Authored-By line
   - **DO NOT** use any flags like `--no-verify`, `--no-gpg-sign`, etc.
5. Run `git status` to verify all commits succeeded.
6. If `push` was passed, run `git push` (with `-u origin <branch>` if the branch has no upstream) after all commits succeed.

## Multiple Commits

If the changes span multiple logical units, create separate commits:
- **Good**: One commit for refactoring, another for the new feature
- **Good**: One commit per file if they serve different purposes
- **Bad**: All changes lumped into one commit when they're unrelated

Each commit should be atomic and self-contained.

## Fixup Commits

For unpushed commits, you can use fixup commits and rebase to keep history clean:

```bash
# Make a fix to an earlier commit
git add src/component.ts
git commit --fixup=abc1234

# Squash fixups into their parent commits (non-interactive)
git rebase --autosquash HEAD~5
```

Only use fixup commits when:
- The original commit has **NOT** been pushed to remote
- The fix logically belongs to the original commit
- It makes sense to keep them as a single logical unit

## Post-Commit Formatting Fixes

If formatting or linting fixes are needed after committing:
- **Single commit**: Use `git commit --amend` to fold the fix into the existing commit
- **Multiple commits**: Use `git commit --fixup=<sha>` and then `git rebase --autosquash HEAD~N`

## Important

- **DO NOT** include any `Co-Authored-By` line
- **DO NOT** use flags like `--no-verify` or `--no-gpg-sign` unless using `--fixup`
- **DO NOT** use `git rebase -i` (interactive rebase is not supported)
- Follow normal commit message conventions (concise, descriptive, imperative mood)
- Only commit files that are relevant to the logical unit of work
- Never commit sensitive files (.env, credentials, etc.)
- Each commit should stand alone and make sense independently

## Commit Message Guidelines

- Keep it concise (under 72 characters for the subject line)
- Use imperative mood ("Add feature" not "Added feature")
- Focus on what and why, not how
- No period at the end of the subject line
- Be specific and descriptive

## Examples

### Single Logical Unit

```bash
git add src/component.ts src/component.test.ts
git commit -m "Fix validation logic in user form"
git status
```

### Multiple Logical Units

```bash
# First logical unit: refactoring
git add src/utils/parser.ts
git commit -m "Extract parsing logic to separate utility"

# Second logical unit: new feature using the refactored code
git add src/component.ts src/component.test.ts
git commit -m "Add email validation to signup form"

git status
```

### Fixup Commit

```bash
# Original commit
git add src/component.ts
git commit -m "Add email validation to signup form"

# Later, discovered a typo in that same commit
git add src/component.ts
git commit --fixup=HEAD

# Squash the fixup before pushing (non-interactive)
git rebase --autosquash HEAD~2
```
