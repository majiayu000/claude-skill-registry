---
name: jj:squash
description: "Squash changes from working copy into relevant ancestor commits"
---

# Squash Changes Into Ancestors

Move changes from the current working copy into appropriate ancestor commits.

## Process

1. Run `jj diff --summary` and `jj diff --stat` for overview
2. Run `jj log -r ::@- --limit 15` to see candidate ancestor commits
3. Analyze changes:
   - Small (≤5 files, ≤200 lines): run `jj diff` directly
   - Large: use `/jj-context` for structured summary
4. Match changes to commits by path and commit descriptions
5. Execute squashes

## Basic Usage

Without options, `jj squash` moves all changes from `@` into its parent:
```bash
jj squash  # squash @ into @-
```

## Whole Files

```bash
jj squash --into <change-id> path/to/file.py   # -t is short for --into
jj squash --into <change-id> "src/**/*.py"     # glob pattern
jj squash --into @--                            # into grandparent
```

## Sub-File Chunks

For extracting specific hunks (not whole files):

1. Save original @ change ID:
   ```bash
   jj log -r @ --no-graph -T 'change_id'
   ```

2. Create intermediate commit:
   ```bash
   jj new --insert-before @
   ```

3. Write only the hunks for target commit (use Edit tool)

4. Squash into target:
   ```bash
   jj squash --into <target-change-id>
   ```

5. Return to rebased @ and remove duplicated hunks:
   ```bash
   jj edit <rebased-@-change-id>
   ```

6. Restore working copy:
   ```bash
   jj new
   ```

## Notes

- Always use change IDs (e.g., `ksrmwuon`) not commit IDs - they're stable across rewrites
- After squashing, @ remains as working copy (empty if all changes moved)
