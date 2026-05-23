---
name: release
description: Create a versioned release with git tag and CHANGELOG update
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(grep *), Read, Edit, Write
argument-hint: "[patch|minor|major] [--message 'Description']"
---

# Create Release

Create a new version release with semantic versioning, git tag, and CHANGELOG update.

## Arguments

- `patch` (default): Bug fixes, minor improvements (0.9.0 → 0.9.1)
- `minor`: New features, non-breaking changes (0.9.0 → 0.10.0)
- `major`: Breaking changes (0.9.0 → 1.0.0)
- `--message "Description"`: Optional release description

## Steps

### 1. Check Current State

```bash
# Ensure on main and up to date
git checkout main
git pull origin main

# Check for uncommitted changes
git status

# Get current version (check common locations)
grep -h "version" pyproject.toml | head -1
# or
grep "__version__" */__init__.py 2>/dev/null | head -1
```

Fail if there are uncommitted changes. All work must be committed first.

### 2. Calculate New Version

Parse current version and calculate new version:

| Current | Bump Type | New Version |
|---------|-----------|-------------|
| 1.1.0 | patch | 1.1.1 |
| 1.1.0 | minor | 1.2.0 |
| 1.1.0 | major | 2.0.0 |

### 3. Update Version Files

Update version in `pyproject.toml`:

```toml
version = "X.Y.Z"
```

If project has `__init__.py` with `__version__`, update that too.

### 4. Update CHANGELOG.md

Add new entry at top of CHANGELOG.md (create if doesn't exist):

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- [New features if any]

### Changed
- [Changes if any]

### Fixed
- [Bug fixes if any]
```

If release message was provided, include it.

### 5. Commit Release

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore: release vX.Y.Z

[Release description]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### 6. Create Git Tag

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z

[Release description]"
```

### 7. Push Release

```bash
git push origin main
git push origin vX.Y.Z
```

### 8. Confirm Release

Show:
- New version number
- Tag created
- CHANGELOG entry
- Next steps (e.g., PyPI publish if applicable)

## When to Release

- **Patch (x.y.Z)**: Bug fixes, documentation updates
- **Minor (x.Y.0)**: New features, new skills added
- **Major (X.0.0)**: Breaking API changes

## Related Skills

- `/done` - Complete work (should consider version bump)
