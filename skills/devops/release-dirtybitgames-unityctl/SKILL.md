---
name: release
description: Create a new release of unityctl. Analyzes changes since last tag, determines version bump type (major/minor/patch), updates version, builds, commits, tags, and creates a draft GitHub release with changelog.
---

# unityctl Release Workflow

Create a new release of the unityctl project.

## Process Overview

1. Analyze changes since last version tag to determine release type
2. Bump version in `Directory.Build.props`
3. Run `./dev-install.sh` to build and update artifacts
4. Commit version bump and build artifacts
5. Push commit and version tag
6. Create draft GitHub release with changelog

## Step 1: Analyze Changes

Get the latest tag and diff to determine version type:

```bash
# Get latest version tag
git describe --tags --abbrev=0 --match "v*"

# View commit log since last tag
git log $(git describe --tags --abbrev=0 --match "v*")..HEAD --oneline

# View full diff since last tag
git diff $(git describe --tags --abbrev=0 --match "v*")..HEAD --stat
```

### Version Bump Guidelines

- **Major (X.0.0)**: Breaking API changes, protocol incompatibilities, removed features
- **Minor (0.X.0)**: New features, new commands, significant enhancements
- **Patch (0.0.X)**: Bug fixes, documentation updates, minor improvements

Review the changes and propose a version bump type to the user.

## Step 2: Update Version

Edit `Directory.Build.props` to update the `<Version>` element:

```xml
<Version>X.Y.Z</Version>
```

## Step 3: Build and Install

Run the dev-install script to build the solution and update artifacts:

```bash
./dev-install.sh
```

This will update:
- `UnityCtl.UnityPackage/Plugins/UnityCtl.Protocol.dll`
- `UnityCtl.UnityPackage/package.json` (version synced automatically)

## Step 4: Commit Changes

Stage and commit the version changes:

```bash
git add Directory.Build.props
git add UnityCtl.UnityPackage/Plugins/UnityCtl.Protocol.dll
git add UnityCtl.UnityPackage/package.json
git commit -m "bump X.Y.Z"
```

## Step 5: Push and Tag

```bash
git push origin main
git tag vX.Y.Z
git push origin vX.Y.Z
```

## Step 6: Create Draft GitHub Release

Generate a changelog from commits since the last tag and create a draft release:

```bash
# Generate changelog
git log $(git describe --tags --abbrev=0 --match "v*" HEAD^)..HEAD --pretty=format:"- %s" --no-merges

# Create draft release
gh release create vX.Y.Z --draft --title "vX.Y.Z" --notes "CHANGELOG_CONTENT"
```

### Changelog Format

Organize the changelog by category:

```markdown
## What's Changed

### Features
- New feature description

### Improvements
- Enhancement description

### Bug Fixes
- Fix description

### Documentation
- Doc update description

**Full Changelog**: https://github.com/DirtybitGames/unityctl/compare/vPREVIOUS...vX.Y.Z
```

## Interaction Guidelines

1. **Always show the diff analysis first** and propose a version type (major/minor/patch)
2. **Wait for user approval** of the version number before proceeding
3. **Show the proposed changelog** before creating the GitHub release
4. **Confirm success** by showing the release URL at the end

## Files Modified

The release process modifies these tracked files:
- `Directory.Build.props` - Version number
- `UnityCtl.UnityPackage/Plugins/UnityCtl.Protocol.dll` - Built protocol assembly
- `UnityCtl.UnityPackage/package.json` - Unity package version (auto-synced)
