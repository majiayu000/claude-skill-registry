---
name: releasing-kata
description: Use this skill when releasing a new version of Kata, bumping versions, updating changelogs, creating release PRs, or publishing to NPM and the plugin marketplace. Triggers include "release", "bump version", "publish", "create release PR", "ship it", "cut a release".
---

# Releasing Kata

Guide the release process for Kata's dual-channel distribution (NPM + Plugin marketplace).

## Release Flow Overview

```
1. Run tests locally
2. Bump version in package.json and plugin.json
3. Update CHANGELOG.md
4. Create release branch and PR
5. Merge PR to main
6. CI automatically: tests → build → publish NPM → create GitHub Release → push to marketplace
```

## Step 1: Pre-Release Verification

Before starting a release, ensure the codebase is ready:

```bash
# Run all tests
npm test && npm run test:smoke

# Build and verify both distributions
npm run build

# Check for uncommitted changes
git status
```

**Stop if tests fail.** Fix issues before proceeding.

## Step 2: Determine Version Bump

Ask the user what type of release this is:

| Type    | When to Use                       | Example       |
| ------- | --------------------------------- | ------------- |
| `patch` | Bug fixes, small improvements     | 1.0.5 → 1.0.6 |
| `minor` | New features, backward compatible | 1.0.5 → 1.1.0 |
| `major` | Breaking changes                  | 1.0.5 → 2.0.0 |

## Step 3: Bump Versions

**Both files must have matching versions:**

1. Read current version from package.json
2. Calculate new version based on bump type
3. Update `package.json` version field
4. Update `.claude-plugin/plugin.json` version field

```bash
# Get current version
cat package.json | jq -r '.version'

# After updating both files, verify they match
diff <(jq -r '.version' package.json) <(jq -r '.version' .claude-plugin/plugin.json)
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

### 3: Update Website (if needed)

If there are significant changes affecting documentation, update the website docs accordingly.
`~/Users/gannonhall~/dev/oss/kata-site/src`

## Step 5: Run Tests Again

After version bump, rebuild and test:

```bash
npm run build && npm test && npm run test:smoke
```

## Step 6: Create Release PR

```bash
# Create release branch
git checkout -b release/vX.Y.Z

# Stage release files
git add package.json .claude-plugin/plugin.json CHANGELOG.md

# Commit with conventional format
git commit -m "chore: bump version to X.Y.Z"

# Push and create PR
git push -u origin release/vX.Y.Z
gh pr create --title "Release vX.Y.Z" --body "## Release vX.Y.Z

### Changes
- [List key changes from CHANGELOG]

### Checklist
- [ ] Version bumped in package.json
- [ ] Version bumped in plugin.json
- [ ] CHANGELOG updated
- [ ] Tests passing"
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
1. `publish.yml` triggers on version change detection
2. Runs tests → Builds → Publishes to NPM → Creates GitHub Release
3. `plugin-release.yml` triggers on publish completion
4. Builds plugin → Pushes to kata-marketplace

## Step 8: Verify Release

After CI completes (~2-3 minutes), verify both distribution channels.

### 8a. Automated Smoke Tests

Run the automated smoke tests against the published version:

```bash
# Test against published NPM package
KATA_VERSION=X.Y.Z npm run test:smoke

# Optional: Include Claude CLI integration tests
TEST_CLI=1 KATA_VERSION=X.Y.Z npm run test:smoke
```

**What smoke tests verify:**
- NPX install creates correct directory structure
- VERSION file matches expected version
- Skills have correct path references
- Plugin build has transformed paths
- @ references resolve to existing files

### 8b. Verify NPM and GitHub Release

```bash
# Verify NPM package published
npm view @gannonh/kata version

# Verify GitHub Release created
gh release view vX.Y.Z
```

### 8c. Verify Plugin Marketplace Updated

```bash
# Check marketplace version (bypasses CDN cache)
gh api repos/gannonh/kata-marketplace/contents/.claude-plugin/marketplace.json --jq '.content' | base64 -d | jq -r '.plugins[0].version'

# Verify plugin-release workflow ran successfully
gh run list --workflow=plugin-release.yml --limit 3
```

### 8d. Manual Plugin Installation Test

**This is the one test that can't be fully automated.** Test actual plugin installation:

```bash
# Create temporary test directory
mkdir -p /tmp/kata-plugin-test && cd /tmp/kata-plugin-test

# Start Claude Code and test interactively
claude
```

In Claude Code:
```
/plugin install kata@kata-marketplace
/kata:providing-help
/kata:showing-whats-new
```

**Verify:**
- Plugin installs without errors
- `/kata:providing-help` shows all commands
- `/kata:showing-whats-new` shows new version changelog
- No path resolution errors

```bash
# Cleanup
cd - && rm -rf /tmp/kata-plugin-test
```

## Troubleshooting

See `./release-troubleshooting.md` for common issues:
- CI workflow failures
- Plugin marketplace not updating
- Version mismatch errors

## Acceptance Criteria

**Pre-release:**
- [ ] package.json version updated
- [ ] plugin.json version matches package.json
- [ ] CHANGELOG.md has entry for new version
- [ ] All tests pass locally (`npm test && npm run test:smoke`)

**Release:**
- [ ] PR merged to main
- [ ] GitHub Release created with correct tag (`gh release view vX.Y.Z`)

**Post-release verification:**
- [ ] NPM shows new version (`npm view @gannonh/kata version`)
- [ ] Smoke tests pass against published version (`KATA_VERSION=X.Y.Z npm run test:smoke`)
- [ ] Marketplace shows new version (`gh api` check)
- [ ] Manual plugin test passes (`/plugin install kata@kata-marketplace` + `/kata:providing-help`)
