---
argument-hint: '[--all] [--deep] [--push]'
disable-model-invocation: false
name: commit
user-invocable: true
description: This skill should be used when the user asks to "commit changes", "craft a commit message", "stage and commit", "commit only session edits", or run a commit workflow with flags like --all, --deep, or --push. Creates atomic git commits with heuristic analysis, conventional-commit formatting, staging rules, optional deep analysis, and optional push.
---

# Git Commit

## Overview

Create atomic commits by staging the right files, analyzing the staged diff, composing a conventional commit message, and optionally pushing.

## Workflow

### 0) Pre-flight checks

- Verify inside a git worktree: `git rev-parse --is-inside-work-tree`
- Verify not detached: `git symbolic-ref HEAD`
- Verify not in rebase/merge/cherry-pick state: check for `.git/rebase-merge`, `.git/MERGE_HEAD`, `.git/CHERRY_PICK_HEAD`
- If any check fails, stop with a clear error and suggested fix.

### 1) Collect context

- Current branch: `git branch --show-current`
- Git status: `git status --short --branch`
- Initial staged diff: `git diff --cached`
- Arguments: `$ARGUMENTS`

Note: The staged diff may become stale after staging changes; re-read `git diff --cached` after STEP 2.

### 2) Handle staging

- If `--all`:
  - If no changes at all: error "No changes to commit"
  - If unstaged changes exist: `git add -A`
  - If already staged: proceed
  - Log staged files with status (A/M/D)
- Otherwise (atomic commits):
  - Session-modified files = files edited in this session
  - Currently staged files: `git diff --cached --name-only`
  - For staged files NOT in session-modified set: `git restore --staged <file>`
  - For session-modified files with changes: `git add <file>`
  - Log staged files with status (A/M/D)
  - If none: error "No files modified in this session"
- **Unrelated changes**: session-modified files may contain pre-existing uncommitted changes (hunks not from this session). Include the entire file—partial staging is impractical. Never revert, discard, or `git checkout` unrelated changes.
- Re-read staged diff: `git diff --cached`

### 3) Parse arguments

- Flags:
  - `--all` commit all changes
  - `--deep` deep analysis, breaking changes, concise body
  - `--push` push after commit
- Value arguments:
  - Type keyword (any conventional type) overrides inferred type
  - Quoted text overrides inferred description
- Precedence:
  1. Explicit type keyword in arguments
  2. Heuristic inference from diff
  3. Quoted text in arguments
  4. Heuristic inference from diff

### 4) Analyze changes

- Default:
  - Read the staged diff
  - Ignore unrelated hunks (pre-existing changes not from this session) when determining type, scope, and description. If unrelated changes are in the same file as session changes, they are included in the commit scope but should not influence the commit message.
  - Determine change type from behavior:
    - New functionality -> `feat`
    - Bug fix or error handling -> `fix`
    - Code reorganization without behavior change -> `refactor`
    - Documentation changes -> `docs`
    - Test additions/changes -> `test`
    - Build system (webpack, vite, esbuild configs) -> `build`
    - CI/CD pipelines (.github/workflows, .gitlab-ci) -> `ci`
    - Dependencies -> `chore(deps)`
    - Formatting/whitespace only -> `style`
    - Performance improvements -> `perf`
    - Reverting previous commit -> `revert`
    - Other maintenance -> `chore`
    - AI config (CLAUDE.md, AGENTS.md, .claude/, .gemini/, .codex/) -> `ai`
  - Infer scope only when path makes it obvious (lowercase)
  - Extract a specific description of what changed (not just which files)
- If `--deep`:
  - Deep semantic analysis; detect breaking changes
  - Infer scope from code structure even when path isn't clear
  - Check for GitHub issues in the chat transcript
  - Keep output concise

Conventional types: feat, fix, docs, style, refactor, test, chore, build, ci, perf, revert, ai

### 5) Compose message

- Subject line (\<= 50 chars): `type(scope): description` or `type: description`
- Imperative mood ("add" not "added"), lowercase, no period
- Describe what the change does, not which files changed
- Default mode:
  - Subject line required
  - Body: hyphenated lines for distinct changes
  - Skip body for trivial changes
- If `--deep`:
  - Body: 2-3 hyphenated lines max, focus on WHY
  - Breaking change: `BREAKING CHANGE:` + one-line migration note
  - GitHub issues: `Closes #123`

### 6) Commit

- Use `git commit -m "subject"` (add `-m "body"` only if body is non-empty)
- Output: commit hash + subject + file count summary
- If failed: show error + suggest fix

### 7) Push (if `--push`)

- If upstream exists: `git push`
- If no upstream: `git push -u origin HEAD`
- If failed: show error + suggest fix (pull/rebase first, set upstream, check auth)

## Examples

Trivial changes (subject only):

```
fix: correct typo in error message
style: format config file
chore(deps): bump lodash to 4.17.21
```

Default (subject + brief body):

```
feat(auth): add oauth2 login support

- Add Google and GitHub OAuth providers
- Integrate alongside existing password auth
```

Deep mode (concise, focused on WHY):

```
feat(webhooks): add retry mechanism for failed deliveries

- Prevent data loss when downstream services are temporarily unavailable
```
