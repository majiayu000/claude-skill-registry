---
name: release-stable
description: Release a stable version (non-beta) - bumps versions in both package.json files, commits, tags, and pushes. Use when cutting a stable release, promoting from beta, or shipping a new version.
---

# Release Stable Version

Use this skill to release a stable (non-beta) version after beta testing is complete.

## Version Convention

Stable versions follow semantic versioning: `X.Y.Z`

- Remove beta suffix when promoting: `3.2.2-beta.8` → `3.2.2`
- Or increment version for new release: `3.2.2` → `3.2.3` or `3.3.0`

## Pre-Flight Checks

1. Ensure you're on `main` branch and it's up to date
2. Check current version: look at `client/package.json` version field
3. Determine target version (remove beta suffix or increment)

## Release Steps

### Step 1: Update Versions

Edit BOTH files to the SAME new version:
- `client/package.json` - update `"version"` field
- `server/package.json` - update `"version"` field

**CRITICAL**: Both files must have identical version strings.

### Step 2: Commit

```bash
git add client/package.json server/package.json
git commit -m "chore: bump version to X.Y.Z"
```

### Step 3: Push to Main

```bash
git push origin main
```

### Step 4: Create and Push Tag

The tag MUST match the version with a `v` prefix:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

**Example**: Version `3.2.2` → Tag `v3.2.2`

## Common Mistakes to Avoid

- Forgetting to update one of the package.json files
- Tag doesn't match version (missing `v` prefix or typo)
- Pushing tag before pushing commit
- Creating tag on wrong branch
- Leaving beta suffix in version string
