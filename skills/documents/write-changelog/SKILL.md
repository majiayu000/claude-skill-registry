---
name: write-changelog
description: Generate and format changelog entries for CHANGELOG.md from archived tickets.
allowed-tools: Bash
user-invocable: false
---

# Write Changelog

Generate and update CHANGELOG.md with entries from archived tickets.

## Generate Entries

Run the bundled script to generate changelog entries:

```bash
bash .claude/skills/generate-changelog/sh/generate.sh <branch-name> <repo-url>
```

The script outputs formatted markdown grouped by category (Added, Changed, Removed).

## Derive Issue URL

From branch name:

- Extract issue number from branch (e.g., `i111-20260113-1832` → `111`)
- Branch format: `i<issue>-<date>-<time>` or `feat-<date>-<time>` (no issue)

## Update CHANGELOG.md

Add a new section at the top of the changelog (after the `# Changelog` header):

```markdown
## [branch-name](issue-url)

<entries from script>
```

If no issue number exists in branch name, use just the branch name without link:

```markdown
## branch-name
```

## Verify Structure

Ensure the changelog maintains proper structure:

- Title line at top: `# Changelog`
- Newest section first
- Blank lines between sections
