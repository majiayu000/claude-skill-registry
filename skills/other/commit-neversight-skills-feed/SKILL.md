---
name: commit
description: Create semantically correct, granular git commits by analyzing staged and unstaged changes
allowed-tools:
  - Bash
---

# Commit Skill

Create semantically correct, granular git commits by analyzing staged and unstaged changes.

**Auto-staging**: All tracked changes are staged automatically. Use `--dry-run` to preview first.

## Model

Use `haiku` for all operations unless complex reasoning is required.

## Arguments

- `(none)`: Auto-commit without confirmation
- `-v` or `--verify`: Show plan and ask for confirmation before committing
- `--dry-run`: Show commit plan without executing
- `--amend`: Amend last commit (always requires -v verification for safety)
- `push`: After committing, push to current remote branch
- `push -v` / `push --verify`: Push with verification prompt

## Workflow

1. Check for merge conflicts - abort if found
2. Check current branch - warn if committing to main/master
3. Run `git status` and `git diff` to understand current changes
4. Run `git diff --cached` to see already staged changes
5. Analyze changes and group them logically
6. Create atomic commits with clear messages
7. If `push` argument: push to remote

## Grouping Strategy

Prefer **more commits over fewer**. Group by:

- **Feature/functionality**: Related changes that implement one thing
- **File type**: Config changes, test files, types, etc.
- **Scope**: Single module/component changes together
- **Nature**: Refactors separate from features separate from fixes

Never combine unrelated changes. When in doubt, split.

## Commit Message Format

```text
<type>(<scope>): <description>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring without behavior change
- `chore`: Maintenance, deps, config
- `docs`: Documentation only
- `test`: Adding/updating tests
- `style`: Formatting, whitespace
- `perf`: Performance improvement

### Rules

- Subject line: max 72 chars, imperative mood, no period
- Body: only if necessary to explain **why**, not **what**
- No body for obvious changes (typos, simple additions, config tweaks)

### Good Examples

```text
feat(auth): add JWT refresh token rotation
fix(api): handle null response from payment provider
refactor(utils): extract date formatting helpers
chore: upgrade typescript to 5.4
test(cart): add edge cases for discount calculation
```

## Execution Steps

1. **Check safety**: Detect conflicts, warn on protected branches (main/master)
2. **Analyze**: `git diff --stat` and `git diff` for full context
3. **Plan**: Determine commit groups with files and messages
4. **Verify** (if `-v`/`--verify`/`--dry-run`/`--amend`): Show plan, wait for confirmation
   - `--dry-run`: Exit after showing plan
   - `--amend`: Modify last commit instead of creating new
5. **Execute**: For each commit:
   ```bash
   git add <files>
   git commit -m "<message>"
   # or for --amend:
   git add <files>
   git commit --amend -m "<message>"
   ```
6. **Push** (only if `push` argument): Run `git push origin HEAD`
   - On failure: show git error, stop (user handles manually)

## Example Session

```text
User: /commit

Claude: Analyzing 7 changed files...

✓ feat(api): add user preferences endpoint
  - src/routes/preferences.ts, src/types/preferences.ts

✓ test(api): add preferences endpoint tests
  - tests/preferences.test.ts

✓ chore: add zod dependency
  - package.json, package-lock.json

4 commits created.
```

**With `-v`**: Shows plan, asks "Proceed? (y/n/edit)" before executing

**With `--dry-run`**: Shows plan, exits without executing

**With `--amend -v`**: Shows plan to amend last commit, asks for confirmation

**With `push`**: Adds "Pushing to origin/main... ✓ Pushed successfully." at end

## Edge Cases

- **Protected branches**: Warn if committing directly to main/master
- **Merge conflicts**: Abort and instruct user to resolve first
- **Single file**: Still analyze if it contains multiple logical changes
- **Large refactors**: May warrant a single commit if truly atomic
- **Mixed changes**: Always split features from fixes from refactors
- **Already staged files**: Respect existing staging, offer to commit separately or include
