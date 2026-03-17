---
name: release
description: Version management and release processes using Jetpack Changelogger. Use when creating releases, managing changelogs, bumping versions, or preparing patch releases.
---

# ActivityPub Release Process

Quick reference for managing releases and changelogs for the WordPress ActivityPub plugin.

## Quick Reference

### Release Commands
```bash
npm run release              # Create major/minor release PR.
```

### Version File Locations
When updating versions manually, change these files:
- `activitypub.php` - Plugin header (`Version: X.Y.Z`).
- `readme.txt` - WordPress.org readme (`Stable tag: X.Y.Z`).
- `package.json` - npm version (`"version": "X.Y.Z"`).
- `CHANGELOG.md` - Changelog file (auto-updated by release script).

## Comprehensive Release Guide

See [Release Process](../../../docs/release-process.md) for complete release workflow and detailed steps.

## Release Workflow

### Major/Minor Releases

**Quick workflow:**
```bash
# 1. Run release script from plugin root.
npm run release

# Script automatically:
# - Determines version from changelog entries.
# - Updates version numbers in all files.
# - Updates CHANGELOG.md.
# - Creates PR for review.

# 2. Review and merge the release PR.

# 3. Create GitHub release from trunk using the new tag.
```

See [Release Process - Major/Minor](../../../docs/release-process.md) for detailed steps.

### Patch Releases

**Quick workflow:**
```bash
# 1. Create branch from the tag to patch.
git fetch --tags
git checkout -b tags/5.3.1 5.3.0  # Patch 5.3.0 -> 5.3.1

# 2. Cherry-pick merge commits from trunk (note -m 1 flag).
git cherry-pick -m 1 <commit-hash>

# 3. Update changelog and versions.
composer changelog:write

# Manually update versions in:
# - activitypub.php
# - readme.txt
# - package.json

# 4. Push branch and create GitHub release.
git push -u origin tags/5.3.1
```

**Important:** Use `-m 1` flag when cherry-picking merge commits to select the mainline parent.

See [Release Process - Patch Releases](../../../docs/release-process.md#patch-releases) for detailed steps.

## Changelog Management

### How It Works

Changelogs are managed automatically through the PR workflow:

1. **PR Template** (`.github/PULL_REQUEST_TEMPLATE.md`):
   - Check "Automatically create a changelog entry" checkbox.
   - Select significance: Patch/Minor/Major.
   - Select type: Added/Fixed/Changed/Deprecated/Removed/Security.
   - Write message **ending with punctuation!**

2. **GitHub Action** (`.github/workflows/changelog.yml`):
   - Creates changelog file from PR description.
   - Validates proper punctuation.
   - Saves to `.github/changelog/` directory.

3. **Release Process**:
   - `npm run release` aggregates all entries.
   - Updates `CHANGELOG.md` and `readme.txt` automatically.

### Critical Requirements

**Always end changelog messages with punctuation:**
```
✅ Add support for custom post types.
✅ Fix signature verification bug.
❌ Add support for custom post types
❌ Fix signature verification bug
```

**Write end-user friendly messages:**
- Focus on user benefit, not implementation details.
- Avoid technical jargon where possible.
- Describe what users can now do, not how it works internally.
```
✅ Add pre-built block patterns for easy profile and sidebar setup.
✅ Fix follow button not appearing on author pages.
❌ Add register_patterns() method to class-blocks.php.
❌ Refactor User class to use Actors collection.
```

**Never mention AI tools or coding assistants in changelog messages.**

See [PR Workflow - Changelog](../pr/SKILL.md#changelog-management) for complete changelog requirements.

## Version Numbering

**Semantic versioning:**
- **Major (X.0.0)** - Breaking changes.
- **Minor (0.X.0)** - New features, backward compatible.
- **Patch (0.0.X)** - Bug fixes only.

The release script determines version automatically from changelog entry significance levels.
