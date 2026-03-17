---
name: edit-changelog
description: Edit changelog using git commit history via script.
---

# Edit changelog

**`GOAL`**: generate changelog entries from git history and update
`CHANGELOG.md`.

**`WHEN`**: the agent needs to update the changelog with recent commits.

**`NOTE`**: requires `CHANGELOG.md` and `.last-aggregated-commit`
(auto-initialized).

## Efficiency directives

- Optimize all operations for token and context efficiency
- Batch operations on file groups, avoid individual file processing
- Target only relevant files
- Reduce token usage

## Workflow

- Run `scripts/edit-changelog.sh`
- Capture status from first line of output
- Handle the status:
  - If `ERROR`: Stop and report to user
  - If `WARN`: Report no changes needed
  - If `SUCCESS`: Report success with entry count
- **`DONE`**

## Output

**Files modified:**

- `CHANGELOG.md` - Unreleased section updated
- `.last-aggregated-commit` - Updated to `HEAD`

**Status communication:**

First line of output indicates status:

- `SUCCESS: [message]` - Operation completed with changes
- `WARN: [message]` - Operation completed but no changes needed
- `ERROR: [message]` - Operation failed

## References

The following reference files serve as strict guidelines:

- **`references/keep-a-changelog-spec.md`**: Format specification
- **`references/changelog-templates.md`**: Template variations
- **`references/changelog-structure.md`**: Structure documentation
- **`references/aggregation-patterns.md`**: Aggregation patterns
