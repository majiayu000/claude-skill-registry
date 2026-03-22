---
argument-hint: '[--all] [--deep] [--push]'
disable-model-invocation: false
name: commit
user-invocable: true
description: This skill should be used when the user asks to "commit changes", "craft a commit message", "stage and commit", "commit only session edits", or run a commit workflow with flags like --all, --deep, or --push. Creates atomic git commits with heuristic analysis, conventional-commit formatting, staging rules, optional deep analysis, and optional push.
---

# Git Commit

Create atomic commits by staging the right files, analyzing the staged diff, composing a conventional commit message, and optionally pushing.

## Workflow

### 1) Pre-flight + context (single call)

Run all checks and context collection in one bash call:

```bash
git rev-parse --is-inside-work-tree \
  && ! test -d "$(git rev-parse --git-dir)/rebase-merge" \
  && ! test -f "$(git rev-parse --git-dir)/MERGE_HEAD" \
  && ! test -f "$(git rev-parse --git-dir)/CHERRY_PICK_HEAD" \
  && git symbolic-ref HEAD \
  && git status --short --branch
```

If any check fails, stop with a clear error and suggested fix.

Arguments: `$ARGUMENTS`

### 2) Parse arguments

- Flags:
  - `--all` commit all changes
  - `--deep` deep analysis, breaking changes, concise body
  - `--push` push after commit
- Value arguments:
  - Type keyword (any conventional type) overrides inferred type
  - Quoted text overrides inferred description

### 3) Stage + read diff

- If `--all`:
  - If no changes at all: error "No changes to commit"
  - If unstaged changes exist: `git add -A`
  - If already staged: proceed
- Otherwise (atomic commits):
  - Session-modified files = files edited in this session
  - Currently staged files: `git diff --cached --name-only`
  - For staged files NOT in session-modified set: `git restore --staged <file>`
  - For session-modified files with changes: `git add <file>`
  - If none: error "No files modified in this session"
- **Unrelated changes**: session-modified files may contain pre-existing uncommitted changes (hunks not from this session). Include the entire file—partial staging is impractical. Never revert, discard, or `git checkout` unrelated changes.
- Read the staged diff once: `git diff --cached`
- Log staged files with status (A/M/D)

### 4) Analyze + compose message

Read the staged diff and produce the commit message in a single pass.

**Type inference** — determine from behavior:

| Behavior | Type |
|---|---|
| New functionality | `feat` |
| Bug fix / error handling | `fix` |
| Code reorganization, no behavior change | `refactor` |
| Documentation | `docs` |
| Tests | `test` |
| Build system (webpack, vite, esbuild) | `build` |
| CI/CD pipelines | `ci` |
| Dependencies | `chore(deps)` |
| Formatting / whitespace only | `style` |
| Performance | `perf` |
| Reverting previous commit | `revert` |
| AI config (CLAUDE.md, .claude/, .gemini/, .codex/) | `ai` |
| Other maintenance | `chore` |

Explicit type keyword in arguments takes precedence over inference.

**Scope** — infer only when path makes it obvious (lowercase).

**Unrelated hunks** — ignore pre-existing changes when determining type/scope/description. If unrelated changes are in the same file as session changes, they are included in the commit scope but should not influence the message.

**Message format:**

- Subject line (<= 50 chars): `type(scope): description` or `type: description`
- Imperative mood ("add" not "added"), lowercase, no period
- Describe what the change does, not which files changed
- Body: hyphenated lines for distinct changes; skip for trivial changes

**If `--deep`:**

- Deep semantic analysis; detect breaking changes
- Infer scope from code structure even when path isn't clear
- Body: 2-3 hyphenated lines max, focus on WHY
- Breaking change: `BREAKING CHANGE:` + one-line migration note
- Check for GitHub issues in the chat transcript; add `Closes #123`

### 5) Commit

- Use `git commit -m "subject"` (add `-m "body"` only if body is non-empty)
- Output: commit hash + subject + file count summary
- If failed: show error + suggest fix

### 6) Push (if `--push`)

- If upstream exists: `git push`
- If no upstream: `git push -u origin HEAD`
- If failed: show error + suggest fix (pull/rebase first, set upstream, check auth)
