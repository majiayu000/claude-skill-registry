---
name: init-changelog
description:
  Create the foundational structure for changelog management via script.
---

# Initialize changelog

**`GOAL`**: create `CHANGELOG.md` and initialize commit pointer.

**`WHEN`**: the agent needs to start changelog management.

**`NOTE`**: exits gracefully if `CHANGELOG.md` already exists.

## Efficiency directives

- Optimize all operations for token and context efficiency
- Batch operations on file groups, avoid individual file processing
- Target only relevant files
- Reduce token usage

## Workflow

- Run `scripts/init-changelog.sh`
- Capture status from first line of output
- Handle the status:
  - If `ERROR`: Stop and report to user
  - If `WARN`: Report already exists
  - If `SUCCESS`: Report success
- **`DONE`**

## Output

**Files created:**

- `CHANGELOG.md` - Main changelog file
- `.last-aggregated-commit` - Pointer file

**Status communication:**

First line of output indicates status:

- `SUCCESS: [message]` - Operation completed
- `WARN: [message]` - No changes made
- `ERROR: [message]` - Operation failed

