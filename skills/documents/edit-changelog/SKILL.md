---
name: edit-changelog
description:
  Edit changelog using git commit history. Use when the agent needs to
  edit the changelog.
---

# Edit changelog

Generate changelog entries from git commit history then update
`CHANGELOG.md`.

## Purpose

This skill dynamically generates changelog entries from git commits:

- Tracks last processed commit via `.last-aggregated-commit` pointer in
  repository root
- Queries git for new commits since last run
- Parses conventional commit messages
- Categorizes changes into Keep a Changelog sections
- `Deduplicates` by issue number
- Updates `CHANGELOG.md`

## When to use

Invoke this skill when the agent needs to update the changelog.

**Prerequisites:**

- `CHANGELOG.md` exists (invoke `init-changelog` first if missing)
- The project requires a git repository
- `.last-aggregated-commit` pointer exists (auto-initialized on first
  run)

**Behavior:**

- Processes only conventional commit format (`feat:`, `fix:`, etc.)
- Skips non-conventional commits
- Overwrites manual edits in Unreleased section
- Preserves manual edits in versioned sections

## Workflow

- Run `scripts/edit-changelog.sh`
- Verify `CHANGELOG.md` section updates
- Communicate success or failure to user

### Logic overview

The script performs the following steps:

1. **Verify prerequisites**: Checks for `CHANGELOG.md` and git
   repository.
2. **Read last aggregated commit**: Reads or bootstraps the
   `.last-aggregated-commit` pointer.
3. **Get new commits**: Queries `git log` for commits since the last
   run.
4. **Parse and categorize**: Parses Conventional Commits, filters types,
   and `deduplicates` by issue number.
5. **Reconstruct `CHANGELOG.md`**: Preserves header/history and inserts
   the new `[Unreleased]` section.
6. **Update pointer**: Updates `.last-aggregated-commit` to `HEAD`.

## Output

**Files modified:**

- `CHANGELOG.md` - Unreleased section regenerated with new entries
- `.last-aggregated-commit` - Updated to current `HEAD`

**Status communication:**

- Exit code `0`: Success or warning (no new commits)
- Exit code `1`: Failure (missing prerequisites)

**`Stdout` format:** first line contains status:

- `SUCCESS: Changelog updated with N new entries`
- `WARN: No new commits to process`
- `ERROR: CHANGELOG.md doesn't exist. Run 'init-changelog' first`

## References

See reference files for detailed specifications:

- `references/keep-a-changelog-spec.md` - Keep a Changelog format
  specification
- `references/changelog-templates.md` - Template variations and examples
- `references/changelog-structure.md` - Changelog structure
  documentation
- `references/aggregation-patterns.md` - Git-based aggregation patterns

## Success criteria

**Successful run:**

- ✓ Processes commits since last aggregation
- ✓ Updates `CHANGELOG.md` with categorized entries
- ✓ Updates `.last-aggregated-commit` pointer to `HEAD`
- ✓ `Deduplicates` entries by issue number

**Graceful exit without changes:**

- No new commits since last run
- Pointer missing (initializes and exits)
- Pointer corrupted (`reinitializes` and exits)
