---
name: resolve-conflicts
description: Use when git reports merge conflicts during rebase, merge, cherry-pick, or revert operations.
effort: medium
argument-hint: 
---



# Resolve Conflicts

## Purpose

Intelligent git conflict resolution. Detects conflict type, categorizes files by resolution strategy, and resolves conflicts with awareness of both sides' intent. Handles lock files, migrations, and code conflicts differently.

## Trigger

- Command: `/ai-resolve-conflicts`
- Context: git operation resulted in conflicts (rebase, merge, cherry-pick, revert).
- Auto-detect: `git status` shows "Unmerged paths" or "both modified".

## Procedure

1. **Detect conflict type** -- determine the operation that caused conflicts:

   ```bash
   # Check which operation is in progress
   test -d .git/rebase-merge || test -d .git/rebase-apply  # rebase
   test -f .git/MERGE_HEAD                                  # merge
   test -f .git/CHERRY_PICK_HEAD                            # cherry-pick
   test -f .git/REVERT_HEAD                                 # revert
   ```

2. **List conflicted files** -- `git diff --name-only --diff-filter=U`

3. **Categorize each file** by resolution strategy:

   | Category | File patterns | Strategy |
   |----------|--------------|----------|
   | Lock files | `*.lock`, `poetry.lock`, `Cargo.lock`, `package-lock.json`, `uv.lock` | Accept theirs, regenerate |
   | Migrations | `migrations/`, `alembic/versions/` | Ask user (order matters) |
   | Generated | `*.min.js`, `*.min.css`, `dist/`, `build/` | Accept theirs, rebuild |
   | Config | `*.yml`, `*.toml`, `*.json` (non-lock) | AI merge with validation |
   | Code | everything else | AI analysis |

4. **Resolve by category**:

   **Lock files**: accept incoming version, then regenerate:
   ```bash
   git checkout --theirs <lockfile>
   # Then regenerate: npm install / cargo generate-lockfile / uv lock / etc.
   ```

   **Migrations**: present both sides to user with context. Migration ordering is semantic -- never auto-resolve. Show the migration graph and ask which order to apply.

   **Generated files**: accept theirs, rebuild from source after resolution.

   **Config files**: read both versions, merge intelligently preserving both sides' additions. Validate result against schema if available.

   **Code conflicts**: for each conflict hunk:
   a. Read surrounding context (50 lines each side)
   b. Identify intent of each change (what was the goal?)
   c. Check commit messages for both sides
   d. Propose resolution preserving both intents
   e. If intents conflict, present options to user

5. **Stacked PR detection** -- if resolving conflicts between branches in a stack:
   a. Compare base, HEAD, and incoming for similarity
   b. If high overlap, likely a stacked PR rebase -- prefer incoming (later branch)
   c. Warn user about potential cascade to downstream branches

6. **Validate resolution**:
   - Run `git diff` to review all resolutions
   - Run stack-specific checks (build, lint, test)
   - Present summary before continuing the operation

7. **Continue operation**:
   ```bash
   git add <resolved-files>
   git rebase --continue   # or merge --continue, etc.
   ```

## Common Mistakes

| Mistake | Why it is wrong |
|---------|----------------|
| Auto-resolving migration conflicts | Migration order is semantic; wrong order corrupts data |
| Keeping both sides of a lock file | Lock files must be regenerated from the manifest |
| Resolving without reading commit messages | Loses context about intent |

## Quick Reference

```
/ai-resolve-conflicts     # auto-detect and resolve current conflicts
```

No arguments needed -- the skill reads git state directly.

$ARGUMENTS
