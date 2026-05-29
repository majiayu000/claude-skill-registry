---
name: generate-changelog
description: Generate changelog entries from archived tickets grouped by category.
allowed-tools: Bash
user-invocable: false
---

# Changelog Generation

Generate changelog entries from archived tickets for a branch.

## When to Use

Use this skill to generate formatted changelog entries from archived tickets. The entries are grouped by category (Added, Changed, Removed) and formatted with links to commits and tickets.

## Instructions

Run the bundled script to generate changelog entries:

```bash
bash .claude/skills/generate-changelog/sh/generate.sh <branch-name> <repo-url>
```

The script outputs formatted markdown that can be inserted into CHANGELOG.md.

### Output Format

```markdown
### Added

- Title ([hash](commit-url)) - [ticket](ticket-path)

### Changed

- Title ([hash](commit-url)) - [ticket](ticket-path)

### Removed

- Title ([hash](commit-url)) - [ticket](ticket-path)
```

Only categories with entries are included.

## Entry Format

Each entry includes:

- **Title**: H1 heading from ticket file
- **hash**: Short commit hash linking to GitHub commit
- **ticket**: Relative path to archived ticket file
