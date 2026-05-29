---
name: spool-commit
description: Create atomic git commits aligned to Spool changes. Use when you want to commit work after applying a change, optionally with auto-mode.
---

Create atomic git commits aligned to Spool changes.

**Concept:** In Spool-driven workflows, you typically make progress by creating/applying a change. After applying and verifying a change, you should usually create a git commit that corresponds to that change.

**Key behavior**

- Prefer 1 commit per applied Spool change (or a small number of commits if the change is large).
- Include the Spool change id in the commit message when practical (e.g. `001-02_add-tasks`).
- Use Spool inspection commands to anchor the commit to what was actually applied.

## Parameters

When invoking this skill, check for these parameters in context:

- **auto_mode**: boolean flag
  - `true`: create commits immediately without asking for confirmation
  - `false` or missing: ask for confirmation of each commit message
  - CRITICAL: this only applies to the current invocation and is reset afterwards

- **change_id**: optional, a Spool change id (recommended)
  - If missing, prompt the user to pick from `spool list --json`

- **stacked_mode**: optional boolean
  - If `true`, create stacked branches per commit (only if tooling exists)
  - If `false` or missing, commit on current branch

- **ticket_id**: optional identifier to include in commit messages

## Prerequisites

1. Verify repo has changes:
   - `git status --short`
   - If no changes, stop with: "No changes found to commit"

2. Identify Spool change context:
   - If `change_id` not provided, run `spool list --json` and ask user to select
   - Then inspect the change: `spool status --change "<change-id>"`

3. Confirm the change is in a good commit state:
   - Ensure artifacts/tasks are complete enough that a commit makes sense
   - If the change is unfinished, ask user whether to commit "WIP" or wait

## Commit Message Format

Use conventional commit format:

- Format: `type(scope): description`
- Prefer scope = Spool module name or ticket id
- Description should mention the change goal
- Include Spool change id at end, in parentheses, when practical

Examples:

- `feat(todo): add task model and parsing (001-02_add-task-core)`
- `fix(storage): persist tasks atomically (002-01_storage-save)`

## Procedure

1. Read diffs: `git diff` and `git status --short`

2. Stage files for the selected change (prefer staging only files touched by that change)

3. Decide commit messages:
   - If `auto_mode` is true: commit immediately
   - Otherwise: present recommended message + alternatives, ask user to confirm

4. Verify after each commit: `git status --short`

## Output

After committing, show:

- Change committed: <change-id>
- Commit SHA + message (`git log -1 --oneline`)
- Remaining uncommitted changes (if any)
