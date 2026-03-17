---
name: release
description: Create a new version release with git tag and GitHub Release. Use when user asks to release, publish, create a new version, or ship a release. (project)
---

# Release Skill

Create a new version release using prefixed tag-based workflow for monorepo plugins.

## When to Use

- User explicitly asks to "release" or "create a release"
- User asks to "publish" or "ship" a new version
- User asks to "tag" a version
- User says "let's release v0.2.0" or similar

## Plugin Identification

This is a **monorepo** with multiple plugins. First, identify which plugin to release:

| Plugin | Version File | Tag Format | Example |
|--------|-------------|------------|---------|
| **Stash Downloader** | `plugins/stash-downloader/package.json` | `downloader-vX.Y.Z` | `downloader-v0.5.2` |
| **Stash Browser** | `plugins/stash-browser/package.json` | `browser-vX.Y.Z` | `browser-v0.1.0` |

If the user doesn't specify, ask which plugin to release. If both changed, release each separately.

## Pre-Release Checklist

Before creating a release, verify:
1. On dev branch: `git branch --show-current`
2. No uncommitted changes: `git status`
3. Type-check passes: `npm run type-check`
4. Lint passes: `npm run lint`
5. Tests pass: `npm test -- --run`
6. Build succeeds: `npm run build`

## Release Process (Tag-Based)

### Step 1: Determine Version Bump

1. **Check current version**: Read the plugin's `package.json` version field
2. **Review commits since last tag**: `git log $(git describe --tags --match "downloader-v*" --abbrev=0)..HEAD --oneline` (or `browser-v*` for Browser)
3. **Determine bump type**:

| Commit Types | Bump | Example |
|--------------|------|---------|
| Breaking changes (`feat!:`, `BREAKING CHANGE`) | MAJOR | 0.1.0 → 1.0.0 |
| New features (`feat:`) | MINOR | 0.1.0 → 0.2.0 |
| Bug fixes, patches (`fix:`, `docs:`, `chore:`) | PATCH | 0.1.0 → 0.1.1 |

### Step 2: Merge dev to main and Release

**For Stash Downloader:**
```bash
# From dev branch, checkout main and merge
git checkout main
git merge dev

# Update version in plugin's package.json
cd plugins/stash-downloader
npm version patch  # or minor/major

# Commit the version bump
git add .
git commit -m "$(cat <<'COMMIT'
🔖 chore: release downloader-vX.Y.Z

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
COMMIT
)"

# Create and push tag (with downloader- prefix!)
git tag downloader-vX.Y.Z
git push origin main --tags
```

**For Stash Browser:**
```bash
# From dev branch, checkout main and merge
git checkout main
git merge dev

# Update version in plugin's package.json
cd plugins/stash-browser
npm version patch  # or minor/major

# Commit the version bump
git add .
git commit -m "$(cat <<'COMMIT'
🔖 chore: release browser-vX.Y.Z

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
COMMIT
)"

# Create and push tag (with browser- prefix!)
git tag browser-vX.Y.Z
git push origin main --tags
```

### Step 3: Wait and Sync Dev

**⚠️ CRITICAL: Do NOT push to dev immediately!**

GitHub Pages uses a concurrency group. If you push to dev before the stable workflow finishes, the stable deploy gets CANCELLED.

```bash
# 1. Wait for workflow to complete
#    Check: https://github.com/Codename-11/Stash-Downloader/actions

# 2. AFTER workflow completes, sync dev with main
git checkout dev
git merge main
git push origin dev
```

## What Happens After Tag Push

GitHub Actions automatically:
1. Runs CI (type-check, lint, tests)
2. Builds the plugin
3. Updates GitHub Pages (Stash plugin index)
4. Generates AI release notes (if GOOGLE_API_KEY configured)
5. Creates GitHub Release with:
   - Auto-generated changelog
   - Installation instructions
   - ZIP file attached

## If Release Was Cancelled

If you accidentally pushed to dev too early and cancelled the stable deploy:

```bash
# Re-push the tag to trigger the workflow again
git push origin --delete downloader-vX.Y.Z  # or browser-vX.Y.Z
git push origin downloader-vX.Y.Z
```

## PR-Based Release (Optional)

For significant releases where you want Claude review before merging:

```bash
# Create release branch from dev
git checkout -b release/downloader-vX.Y.Z dev

# Update version in plugin's package.json, commit
cd plugins/stash-downloader
npm version patch
git add .
git commit -m "🔖 chore: release downloader-vX.Y.Z"

# Push and create PR to main
git push -u origin release/downloader-vX.Y.Z
gh pr create --base main --title "🔖 Release downloader-vX.Y.Z" --body "Release notes..."

# After PR merge, checkout main and tag
git checkout main
git pull origin main
git tag downloader-vX.Y.Z
git push origin downloader-vX.Y.Z
```

## Important Notes

- Tag format MUST include plugin prefix: `downloader-vX.Y.Z` or `browser-vX.Y.Z`
- Version in the plugin's `package.json` must match tag version (without prefix)
- **Always start from dev branch** - never commit directly to main
- **Wait for workflow to complete** before syncing dev
- Push to `main` without a tag triggers NOTHING
- Verify release succeeded in GitHub Actions after pushing tag
- **Release plugins separately** - if both plugins changed, create separate tags
