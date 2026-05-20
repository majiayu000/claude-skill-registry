---
name: commit
description: Commit staged changes using Graphite. Checks if on trunk and creates a new branch if needed. Updates PR title and summary after each commit.
allowed-tools: Bash(gt:*), Bash(git:status), Bash(git:diff), Bash(git:branch), Bash(gh:*), Bash(pnpm:*), Read
---

# Commit Skill

Commits changes using Graphite, ensuring proper branch management and PR metadata.

## Usage

Invoke with `/commit` or `/commit <message>`.

- `/commit` — auto-generates a conventional commit message from the diff
- `/commit fix: resolve auth redirect loop` — uses the provided message
- `/commit --new-branch` — forces creation of a new branch even if already on a feature branch
- `/commit --new-branch fix: resolve auth redirect loop` — combines both

## Autonomous Execution

This skill runs **fully autonomously** without user interaction. When invoked:

- **Do NOT ask for user confirmation** at any step
- **Do NOT pause** between tasks or wait for approval
- **Proceed directly** through all workflow steps
- **Only stop** if a critical error occurs

## Workflow

### Step 1: Check Current Branch

Determine the current branch:

```bash
git branch --show-current
```

If the `--new-branch` flag was passed, **always create a new branch** regardless of the current branch. Proceed to Step 2a.

If the current branch is `main` or `staging` (a trunk branch), you are on trunk and **must create a new branch** before committing. Proceed to Step 2a.

If already on a feature branch (and `--new-branch` was not passed), skip to Step 3.

### Step 2a: Create a New Branch

Create a new feature branch. First, examine the staged and unstaged changes to determine an appropriate branch name:

```bash
git diff --stat
git diff --staged --stat
```

Generate a descriptive kebab-case branch name based on the changes (e.g., `fix/auth-redirect-loop`, `feat/add-user-avatar`, `chore/update-dependencies`).

Create the branch with Graphite:

```bash
gt create <branch-name>
```

`gt create` automatically stacks the new branch on top of the current branch. This means:
- If on trunk (`main`/`staging`), the new branch's parent is trunk
- If on a feature branch (e.g., via `--new-branch`), the new branch stacks on top of that feature branch

### Step 2b: Track Parent (only when creating from trunk)

If the new branch was created from `main` or `staging` (i.e., NOT via `--new-branch` from a feature branch), ensure it targets staging:

```bash
gt track --parent staging
```

**Skip this step** when `--new-branch` was used from a feature branch — the branch is already correctly stacked on the current branch by `gt create`.

### Step 3: Stage Changes

Check for unstaged changes:

```bash
git status
```

If there are unstaged changes, stage all of them:

```bash
gt add .
```

If the user specified specific files, stage only those files instead.

### Step 4: Review the Diff

Get the full diff of staged changes:

```bash
git diff --staged
```

Analyze the diff to understand:
- What type of change this is (feat/fix/refactor/docs/chore/test/style)
- What scope/area is affected
- What the changes accomplish

### Step 5: Run Pre-Commit Checks

Run formatting and tests on changed files:

```bash
pnpm pre-commit
```

If pre-commit fails:
1. Review the failures
2. Fix any formatting issues automatically
3. Re-stage the fixed files with `gt add .`
4. Re-run `pnpm pre-commit`
5. If tests fail, report the failures and stop — do not commit broken code

### Step 6: Create the Commit

Generate a conventional commit message if one was not provided. The message format:

```
type(scope): concise description

Optional body with more detail if the change is complex.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

**Type**: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `style`, `perf`
**Scope**: The affected package or area (e.g., `landing`, `web`, `mobile`, `orpc`, `ui`)

Create the commit:

```bash
gt modify -c -m "$(cat <<'EOF'
type(scope): concise description

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

Use a HEREDOC to preserve multi-line formatting.

### Step 7: Submit PR

Create or update the PR with Graphite:

```bash
gt submit
```

This will create a new PR if one doesn't exist, or update the existing one.

### Step 8: Update PR Title and Summary

After submitting, get the full commit history for this branch:

```bash
gh pr view --json number,title,body,headRefName,commits
```

And get the full diff against the base branch:

```bash
gh pr diff
```

Analyze ALL commits and the full diff to generate:

1. **PR Title** — conventional commit format covering the overall change:
   - `feat(scope): description` for new features
   - `fix(scope): description` for bug fixes
   - `refactor(scope): description` for refactoring
   - `docs(scope): description` for documentation
   - `chore(scope): description` for maintenance
   - If the PR has mixed types, use the most significant one

2. **PR Summary** — structured markdown body:

```markdown
## Summary
<1-3 bullet points describing what this PR does>

## Changes
<Bulleted list of specific changes made>

## Test Plan
<How to verify the changes work>

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

Update the PR:

```bash
gh pr edit --title "type(scope): description" --body "$(cat <<'EOF'
## Summary
...

## Changes
...

## Test Plan
...

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Step 9: Report Result

Output a summary to the user:

```
✓ Committed: type(scope): description
✓ PR #<number> updated: <title>
  <PR URL>
```

## Edge Cases

- **No changes to commit**: If `git status` shows no changes, report "Nothing to commit" and stop
- **Branch already exists**: If `gt create` fails because the branch exists, use `gt branch checkout <name>` instead
- **PR submit fails**: If `gt submit` fails, report the error — the commit was still made successfully
- **Pre-commit hook failure**: Fix formatting issues and retry. If tests fail, stop and report

## Important Rules

- **Always use `gt` commands** for branch/commit operations (never raw `git commit`)
- **Always run `pnpm pre-commit`** before committing
- **Always include `Co-Authored-By`** trailer in commit messages
- **Always update PR title and summary** after each commit using the full diff
- **Branch names** use kebab-case with type prefix (e.g., `feat/thing`, `fix/bug`)
- **New branches target staging** via `gt track --parent staging`
