---
name: release-beta
description: Release a new beta version - bumps versions in both package.json files, commits, tags, and pushes
---

# Release Beta Version

## Version Convention

Beta versions follow this pattern: `X.Y.Z-beta.N`

- Increment beta number (e.g., `3.2.2-beta.3` → `3.2.2-beta.4`)
- For new minor/patch, reset to beta.1 (e.g., `3.2.2-beta.3` → `3.2.3-beta.1`)

## Pre-Flight Checks

1. Ensure you're on `main` branch and it's up to date
2. Check current version: look at `client/package.json` version field
3. Determine next version based on convention above

## Release Steps

### Step 1: Update Versions

Edit BOTH files to the SAME new version:
- `client/package.json` - update `"version"` field
- `server/package.json` - update `"version"` field

**CRITICAL**: Both files must have identical version strings.

### Step 2: Commit

```bash
git add client/package.json server/package.json
git commit -m "chore: bump version to X.Y.Z-beta.N"
```

### Step 3: Push to Main

```bash
git push origin main
```

### Step 4: Create and Push Tag

The tag MUST match the version with a `v` prefix:

```bash
git tag vX.Y.Z-beta.N
git push origin vX.Y.Z-beta.N
```

**Example**: Version `3.2.3-beta.1` → Tag `v3.2.3-beta.1`

## Common Mistakes to Avoid

- ❌ Forgetting to update one of the package.json files
- ❌ Tag doesn't match version (missing `v` prefix or typo)
- ❌ Pushing tag before pushing commit
- ❌ Creating tag on wrong branch
