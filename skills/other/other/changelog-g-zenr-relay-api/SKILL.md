---
name: changelog
description: Generate a changelog from git history for release notes
disable-model-invocation: true
---

Generate a changelog: $ARGUMENTS

## Step 1 — Gather Commits
```bash
# Since last tag:
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Or between two tags:
git log v<from>..v<to> --oneline
```

## Step 2 — Categorize
Group commits by type using conventional commit prefixes:

| Category | Commit Types |
|----------|-------------|
| Added | `feat` |
| Changed | `refactor`, `chore` |
| Fixed | `fix` |
| Security | `security` |
| Documentation | `docs` |
| Testing | `test` |

## Step 3 — Format Changelog
```markdown
## [<version>] - <YYYY-MM-DD>

### Added
- <description of new features>

### Changed
- <description of changes>

### Fixed
- <description of bug fixes>

### Security
- <description of security improvements>
```

## Step 4 — Write to Changelog File
Prepend the new entry to the changelog file (see project config for path).
Keep the existing changelog entries below the new one.

## Step 5 — Summary
```
Changelog for v<version>:
  Added:    X items
  Changed:  X items
  Fixed:    X items
  Security: X items
  Total commits: X
```

## Rules
- Use past tense for descriptions ("Added support for..." not "Add support for...")
- Group related changes under one bullet point
- Don't include merge commits or chore commits in the changelog unless significant
- Link to issues or PRs where relevant