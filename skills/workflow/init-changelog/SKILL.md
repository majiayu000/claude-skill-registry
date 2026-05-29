---
name: init-changelog
description:
  Create the foundational structure for changelog management. Use when
  the agent needs to start changelog management by creating a new
  `CHANGELOG.md` file and the commit pointer to update the changelog.
---

# Initialize changelog

This skill creates the main `CHANGELOG.md` file in the repository root
and initializes the commit pointer for incremental updates.

## Purpose

This skill creates the foundational structure for changelog management:

- Main `CHANGELOG.md` file in repository root
- `.last-aggregated-commit` pointer for tracking last processed commit
- Proper Keep a Changelog format with standard sections
- Initial version detection from git tags or `package.json`
- Smart pointer initialization based on repository size

## When to use

Invoke this skill when the user or agent needs to create `CHANGELOG.md`
and start changelog management.

**Prerequisites:**

- Git repository initialized (optional but recommended)

**Behavior:**

- Exits gracefully if `CHANGELOG.md` already exists (no overwrite)
- Creates Keep a Changelog format structure (non-customizable)
- Auto-detects version from git tags, `package.json`, `Cargo.toml`, or
  `pyproject.toml`
- Smart pointer initialization: first commit if ≤100 commits, `HEAD~100`
  if >100

## Workflow

- Run `scripts/init-changelog.sh`
- Verify `CHANGELOG.md` and `.last-aggregated-commit` creation
- Communicate success or failure to user

### Logic overview

The script performs the following steps:

1. **Verify prerequisites**: Checks if `CHANGELOG.md` already exists. If
   it does, exits gracefully with a `WARN` message.

2. **Detect current version**: Checks for version in priority order:
   - Git tags (using `git describe --tags`)
   - `package.json` (Node projects)
   - `Cargo.toml` (Rust projects)
   - `pyproject.toml` (Python projects)
   - Default to "0.1.0" if no version found

3. **Create `CHANGELOG.md`**: Generates the main changelog file
   following Keep a Changelog format with all standard sections (Added,
   Changed, Deprecated, Removed, Fixed, Security). Includes both
   `[Unreleased]` section and a version section if the script detects a
   version.

4. **Initialize pointer**: Creates `.last-aggregated-commit` file with
   smart detection:
   - **≤100 commits**: Sets pointer to first commit (enables full
     history backfill)
   - **>100 commits**: Sets pointer to `HEAD~100` (`backfills` recent
     history, avoids slow initial run)
   - **Non-git repository**: Skips pointer creation

5. **Verify creation**: Ensures the script created `CHANGELOG.md`
   successfully and outputs appropriate message.

## Output

**Files created:**

- `CHANGELOG.md` - Main changelog file in repository root
- `.last-aggregated-commit` - Pointer file for incremental updates (if
  git repository)

**Status communication:**

- Exit code `0`: Success or warning (no action required)
- Exit code `1`: Failure

**`Stdout` format:** first line contains status:

- `SUCCESS: [message]` - Changelog initialized successfully
- `WARN: [message]` - Already exists, no changes made
- `ERROR: [message]` - Failed to create files (also exit 1)
