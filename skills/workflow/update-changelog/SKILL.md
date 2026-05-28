---
name: update-changelog
description:
  Orchestrate complete changelog workflow. Invoke `init-changelog` (if
  needed), `edit-changelog`, and `cleanup-changelog` skills in sequence.
  Use when the user or agent needs to update the changelog.
---

# Update changelog

**`GOAL`**: orchestrate the complete changelog update workflow by
invoking `init-changelog`, `edit-changelog`, and `cleanup-changelog`
skills in sequence.

**`WHEN`**: use when the user requests to update the changelog or when
the agent needs to ensure the changelog reflects the latest commits.

## Purpose

This skill provides a single entry point for changelog management:

- Initializes `CHANGELOG.md` structure if missing (via `init-changelog`
  skill)
- Updates changelog from git commits (via `edit-changelog` skill)
- Cleans up formatting and removes empty sections (via
  `cleanup-changelog` skill)
- Handles dependencies and conditional logic intelligently

## Prerequisites

- Requires an initialized Git repository
- Conventional commit format for user-facing changes (`feat:`, `fix:`,
  etc.)

## Workflow

Follow these steps in sequence:

### Step 1: Check for `CHANGELOG.md`

- Check if `CHANGELOG.md` exists in the repository root.
- If missing: Invoke the `init-changelog` skill to create it.
  - Verify the output status (`SUCCESS`, `WARN`, or `ERROR`).
  - If `ERROR`: Stop and report the error to the user.
  - If `SUCCESS` or `WARN`: Continue to Step 2.
- If exists: Continue directly to Step 2.

### Step 2: Update from git commits

- Invoke the `edit-changelog` skill to update from git commits.
- Capture the status from the first line of output (`SUCCESS`, `WARN`,
  or `ERROR`).
- Handle the status:
  - If `ERROR`: Stop and report the error to the user.
  - If `WARN` (no new commits): Report to user that changelog already
    reflects latest commits. Skip Step 3 and proceed to Step 4.
  - If `SUCCESS` (changes made): Continue to Step 3.

### Step 3: Cleanup formatting (conditional)

- Only run this step if `edit-changelog` reported `SUCCESS`.
- Invoke the `cleanup-changelog` skill to clean up formatting.
- This step runs: `fix-markdown` → `remove-empty-headers.sh` →
  `fix-markdown`

### Step 4: Report completion

- Communicate a summary to the user indicating:
  - What actions the skill performed
  - Whether the changelog received updates
  - Any warnings or errors encountered during the process
- **`DONE`**

## Behavior

**Smart initialization:**

- Automatically invokes `init-changelog` if `CHANGELOG.md` does not
  exist
- Skips initialization if `CHANGELOG.md` already exists

**Conditional cleanup:**

- Only runs `cleanup-changelog` if `edit-changelog` made changes
  (`SUCCESS` status)
- Skips cleanup if the update requires no changes (`WARN` status)

**Error handling:**

- Stops immediately on `ERROR` from any sub-skill
- Reports errors to the user

## Output

**Files created/modified:**

- `CHANGELOG.md` - Created (if missing) or updated with new entries
- `.last-aggregated-commit` - Created (if missing) or updated to `HEAD`

**Status communication:**

- Reports initialization status when invoking `init-changelog`
- Reports update status from `edit-changelog`
- Reports cleanup status when invoking `cleanup-changelog`
- Provides final summary of all actions taken
