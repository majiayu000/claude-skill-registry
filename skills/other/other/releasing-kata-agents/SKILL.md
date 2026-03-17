---
name: releasing-kata-agents
description: Use this skill when releasing a new version of Kata Agents, bumping versions, updating changelogs, or creating release PRs. Triggers include "release", "bump version", "publish", "create release PR", "ship it", "cut a release".
---

# Releasing Kata Agents

Guide the release process for the Kata Agents Electron desktop application.

## Release Flow Overview

```
1. Run tests locally
2. Bump version in apps/electron/package.json
3. Update CHANGELOG.md
4. Create release branch and PR
5. Merge PR to main
6. CI automatically: detects version → builds all platforms → code signs/notarizes macOS → creates GitHub Release
```

## Step 1: Pre-Release Verification

Before starting a release, ensure the codebase is ready:

```bash
# Run all tests
bun test

# Build the app
bun run electron:build

# Test local production build (run from apps/electron directory)
cd apps/electron && bun run dist:mac

# Check for uncommitted changes
git status
```

**Stop if tests fail.** Fix issues before proceeding.

## Step 2: Determine Version Bump

Ask the user what type of release this is:

| Type    | When to Use                       | Example        |
| ------- | --------------------------------- | -------------- |
| `patch` | Bug fixes, small improvements     | 0.4.9 → 0.4.10 |
| `minor` | New features, backward compatible | 0.4.9 → 0.5.0  |
| `major` | Breaking changes                  | 0.4.9 → 1.0.0  |

## Step 3: Bump Version

Update the version in `apps/electron/package.json`:

```bash
# Get current version
cat apps/electron/package.json | grep '"version"'

# After updating, verify
cat apps/electron/package.json | grep '"version"'
```

## Step 4: Update Docs

### 1: Update CHANGELOG

Add entry to `CHANGELOG.md` following Keep a Changelog format:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature descriptions

### Fixed
- Bug fix descriptions

### Changed
- Modification descriptions
```

**Guidelines:**
- Use today's date
- Group changes by type (Added, Fixed, Changed, Removed)
- Write user-facing descriptions (what changed, not how)
- Reference issue numbers if applicable

### 2: Update README (if needed)

If there are significant changes affecting usage, update `README.md` accordingly.

## Step 5: Run Tests Again

After version bump, rebuild and test:

```bash
bun run electron:build && bun test
```

## Step 6: Create Release PR

```bash
# Create release branch
git checkout -b release/vX.Y.Z

# Stage release files
git add apps/electron/package.json CHANGELOG.md

# Commit with conventional format
git commit -m "chore(release): bump version to X.Y.Z"

# Push and create PR
git push -u origin release/vX.Y.Z
gh pr create --title "Release vX.Y.Z" --body "## Release vX.Y.Z

### Changes
- [List key changes from CHANGELOG]

### Checklist
- [ ] Version bumped in apps/electron/package.json
- [ ] CHANGELOG updated
- [ ] Tests passing
- [ ] Local production build tested"
```

## Step 7: Merge and Monitor CI

```bash
# Merge the PR (after review if required)
gh pr merge --merge --delete-branch

# Monitor CI workflows
gh run list --limit 5
gh run watch  # Watch the latest run
```

**CI Pipeline:**
1. `release.yml` triggers on push to main
2. Detects version change (compares package.json to existing tags)
3. Builds for macOS (arm64 + x64), Windows (x64), Linux (x64)
4. Code signs and notarizes macOS builds
5. Creates GitHub Release with all platform artifacts

## Step 8: Verify Release

After CI completes (~10-15 minutes for all platforms), verify the release.

### 8a. Verify GitHub Release

```bash
# Verify GitHub Release created with tag
gh release view vX.Y.Z

# Check all artifacts are attached
gh release view vX.Y.Z --json assets --jq '.assets[].name'
```

Expected artifacts:
- `Kata-Agents-arm64.dmg` (macOS Apple Silicon)
- `Kata-Agents-x64.dmg` (macOS Intel)
- `Kata-Agents-arm64.zip` / `Kata-Agents-x64.zip`
- `Kata-Agents-x64.exe` (Windows)
- `Kata-Agents-x64.AppImage` (Linux)

### 8b. Verify CI Workflow Success

```bash
# Check release workflow ran successfully
gh run list --workflow=release.yml --limit 3
```

### 8c. Manual App Test

**This is the one test that can't be fully automated.** Download and test the released app:

```bash
# Download the release artifact
gh release download vX.Y.Z --pattern "Kata-Agents-arm64.dmg" --dir /tmp

# Mount and test
open /tmp/Kata-Agents-arm64.dmg
```

**Verify:**
- App launches without errors
- Sessions load and display correctly
- Agent execution works
- No code signing warnings

```bash
# Cleanup
rm /tmp/Kata-Agents-arm64.dmg
```

## Local Production Builds

For testing production builds without releasing:

```bash
# IMPORTANT: Run from apps/electron directory, not repo root
cd apps/electron && bun run dist:mac          # Apple Silicon
cd apps/electron && bun run dist:mac:x64      # Intel
cd apps/electron && bun run dist:win          # Windows
```

Output: `apps/electron/release/Kata-Agents-{arch}.dmg`

**Testing the local build:**
```bash
# Clear stale window state first
rm ~/.kata-agents/window-state.json

# Open the built app
open "apps/electron/release/mac-arm64/Kata Agents.app"
```

## Troubleshooting

See `./release-troubleshooting.md` for common issues:
- CI workflow failures
- Build path errors (must run from `apps/electron`)
- Code signing issues
- Sessions not displaying after build

## Acceptance Criteria

**Pre-release:**
- [ ] apps/electron/package.json version updated
- [ ] CHANGELOG.md has entry for new version
- [ ] All tests pass locally (`bun test`)
- [ ] Local production build works (`cd apps/electron && bun run dist:mac`)

**Release:**
- [ ] PR merged to main
- [ ] GitHub Release created with correct tag (`gh release view vX.Y.Z`)

**Post-release verification:**
- [ ] GitHub Release created with tag (`gh release view vX.Y.Z`)
- [ ] All platform artifacts attached to release
- [ ] Manual app test passes (download, launch, verify sessions)
