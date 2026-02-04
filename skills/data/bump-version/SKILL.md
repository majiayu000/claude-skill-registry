---
name: bump-version
description: Bump version numbers for a new release. Use when releasing, updating version, or preparing a new version.
---

# Bump Version

Update the version string in **both** of these files (they must match):

1. `pyproject.toml` line 7:
   ```toml
   version = "X.Y.Z"
   ```

2. `pytest_claude_agent_sdk/__init__.py` line 27:
   ```python
   __version__ = "X.Y.Z"
   ```

## Steps

1. Ask user for the new version if not provided
2. Read both files to confirm current version
3. Update both files with new version
4. Show diff of changes
5. Suggest commit message: `Bump version to X.Y.Z`

## Version Format

Use semantic versioning: `MAJOR.MINOR.PATCH`
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible
