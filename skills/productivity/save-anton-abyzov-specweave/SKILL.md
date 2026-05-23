---
disable-model-invocation: true
description: Smart auto-commit with remote sync (handles pull/rebase/stash, auto-generates messages, supports multi-repo).
argument-hint: "[message]"
---

# /sw:save - Smart Save with Auto-Sync

## Project Overrides

!`s="save"; for d in .specweave/skill-memories .claude/skill-memories "$HOME/.claude/skill-memories"; do p="$d/$s.md"; [ -f "$p" ] && awk '/^## Learnings$/{ok=1;next}/^## /{ok=0}ok' "$p" && break; done 2>/dev/null; true`

## Usage

```bash
/sw:save           # Fully automatic - generates message, syncs, pushes
/sw:save "msg"     # Your message, auto-sync
/sw:save -i        # Interactive - asks before each step
/sw:save --dry-run # Preview without executing
```

## Execution Order (MANDATORY)

### 1. Scan for Nested Repos (ALWAYS FIRST)

```bash
for dir in repositories packages services apps libs; do
  [ -d "$dir" ] && for repo in "$dir"/*/; do
    [ -d "${repo}.git" ] && echo "Found: ${repo%/}"
  done
done
[ -d ".git" ] && echo "Found: . (parent project)"
```

**Three-tier detection**: (1) `umbrella.childRepos` from `.specweave/config.json` if configured, (2) git-scan of nested `.git` dirs up to 4 levels deep, (3) parent project `.git`.

### 2. Pre-Flight Check

```bash
git fetch origin
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "no-upstream")
BASE=$(git merge-base HEAD @{u} 2>/dev/null || echo "no-base")
```

Determine state: `up-to-date` | `ahead` | `behind` | `diverged` | `no-tracking`.

### 3. Smart Sync

- **behind/diverged**: Stash dirty files, `git pull --rebase`, unstash
- **no-tracking**: `git push -u origin HEAD`
- **up-to-date/ahead**: No sync needed, proceed

### 4. Auto-Commit Message (if none provided)

Run `git status --porcelain` and categorize files:

| Pattern | Type |
|---------|------|
| `src/**/*.ts` (not test) | `feat:` / `refactor:` |
| `*.test.ts`, `tests/` | `test:` |
| `*.md`, `docs/` | `docs:` |
| `package.json`, `*.config.*` | `chore:` |
| `.github/`, CI files | `ci:` |
| `.specweave/increments/*/` | use increment name |

**Format**: `type(scope): action description` -- scope from common path, action from most common status (add/update/remove). If active increment and increment files changed, reference it.

### 5. Commit and Push

```bash
git add -A
git commit -m "<message>"
git push origin <branch>
```

For multi-repo: generate per-repo messages and commit/push each repo with changes.

### 6. Report Summary

Show repos synced, committed, skipped, and commit messages used.

## Conflict Handling

**Auto-resolvable**: `package-lock.json`/`yarn.lock` (delete + reinstall), `.specweave/` metadata (keep LOCAL), `dist/`/`build/` (keep REMOTE).

**Manual resolution required**: Source code, config files, env files. Present options: resolve manually, try merge instead, abort, or force push (requires typing "FORCE").

**NEVER force push by default.** `--force` flag requires explicit "FORCE" confirmation.

## No Remote Configured

Prompt user with the **exact project name** in the dialog. Options: enter URL manually, skip push (commit only), or cancel. For umbrella: check if clone job is running first.

## Flags

| Flag | Description |
|------|-------------|
| `-i` / `--interactive` | Ask confirmation before each step |
| `--dry-run` | Preview without executing |
| `--sync=rebase` | (default) Pull --rebase before push |
| `--sync=merge` | Pull --merge instead |
| `--sync=none` | Skip auto-sync |
| `--no-push` | Commit only |
| `--force` | Force push (requires "FORCE" confirmation) |
| `--branch <name>` | Create new branch instead of force pushing |
| `--repos <list>` | Only save specific repos (comma-separated) |
| `--skip-no-remote` | Skip repos without remotes |
| `--all` | Include repos outside umbrella config |
