---
name: release-cch
description: CCH release workflow automation. Use when asked to "release CCH", "create a release", "prepare release", "tag version", "hotfix release", or "publish CCH". Covers version management from Cargo.toml, changelog generation from conventional commits, PR creation, tagging, hotfix workflows, and GitHub Actions release monitoring.
metadata:
  version: "1.0.0"
  project: "cch"
  source_of_truth: "Cargo.toml"
---

# release-cch

## Contents

- [Overview](#overview)
- [Decision Tree](#decision-tree)
- [Phase 1: Prepare Release](#phase-1-prepare-release)
- [Phase 2: Execute Release](#phase-2-execute-release)
- [Phase 3: Verify Release](#phase-3-verify-release)
- [Phase 4: Hotfix Release](#phase-4-hotfix-release)
- [Scripts Reference](#scripts-reference)
- [References](#references)

## Overview

**Single Source of Truth**: Version is stored in `Cargo.toml` (workspace root):

```toml
[workspace.package]
version = "1.0.0"
```

**Release Trigger**: Pushing a tag like `v1.0.0` triggers `.github/workflows/release.yml`

**Build Targets**:

| Platform | Target | Asset |
|----------|--------|-------|
| Linux x86_64 | x86_64-unknown-linux-gnu | cch-linux-x86_64.tar.gz |
| Linux ARM64 | aarch64-unknown-linux-gnu | cch-linux-aarch64.tar.gz |
| macOS Intel | x86_64-apple-darwin | cch-macos-x86_64.tar.gz |
| macOS Apple Silicon | aarch64-apple-darwin | cch-macos-aarch64.tar.gz |
| Windows | x86_64-pc-windows-msvc | cch-windows-x86_64.exe.zip |

**Repository**: `SpillwaveSolutions/code_agent_context_hooks`

## Decision Tree

```
What do you need?
|
+-- Starting a new release? --> Phase 1: Prepare Release
|
+-- PR merged, ready to tag? --> Phase 2: Execute Release
|
+-- Tag pushed, checking status? --> Phase 3: Verify Release
|
+-- Need to patch an existing release? --> Phase 4: Hotfix Release
|
+-- Something went wrong? --> references/troubleshooting.md
```

---

## Phase 1: Prepare Release

### 1.1 Read Current Version

```bash
# Run from repo root
.opencode/skill/release-cch/scripts/read-version.sh
# Output: 1.0.0
```

### 1.2 Determine New Version

Follow semantic versioning:

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (x.Y.0): New features, backwards compatible
- **PATCH** (x.y.Z): Bug fixes only

**Update Cargo.toml** (manual step):

```toml
[workspace.package]
version = "1.1.0"  # <- Update this
```

### 1.3 Create Release Branch

```bash
VERSION=$(.opencode/skill/release-cch/scripts/read-version.sh)
git checkout -b release/v${VERSION}
```

### 1.4 Run Pre-flight Checks

```bash
.opencode/skill/release-cch/scripts/preflight-check.sh
```

This validates:

- [ ] Clean working directory (or only release files modified)
- [ ] All unit tests pass (`cargo test`)
- [ ] All integration tests pass (`task integration-test`)
- [ ] Clippy has no warnings
- [ ] Format check passes

**IMPORTANT:** Integration tests are REQUIRED before any release. They validate that CCH works correctly with the real Claude CLI end-to-end. If Claude CLI is not installed, the preflight check will warn but not block - however, you should ensure integration tests pass in CI before releasing.

### 1.5 Generate Changelog

```bash
VERSION=$(.opencode/skill/release-cch/scripts/read-version.sh)
.opencode/skill/release-cch/scripts/generate-changelog.sh ${VERSION}
```

Review the output and update `CHANGELOG.md` as needed. The script parses conventional commits (`feat:`, `fix:`, `docs:`, `chore:`).

### 1.6 Commit and Push

```bash
VERSION=$(.opencode/skill/release-cch/scripts/read-version.sh)
git add CHANGELOG.md Cargo.toml
git commit -m "chore: prepare v${VERSION} release"
git push -u origin release/v${VERSION}
```

### 1.7 Create Release PR

```bash
VERSION=$(.opencode/skill/release-cch/scripts/read-version.sh)
gh pr create \
  --title "chore: prepare v${VERSION} release" \
  --body "$(cat <<EOF
## Summary

Prepare for the v${VERSION} release of Claude Context Hooks (CCH).

## Changes

- Update version to ${VERSION} in Cargo.toml
- Add CHANGELOG.md entry for v${VERSION}

## Pre-merge Requirements

Before merging this PR, ensure:
- [ ] All CI checks pass (including integration tests)
- [ ] Integration tests verified locally: \`task integration-test\`

## Release Checklist

After this PR is merged:

1. Checkout main: \`git checkout main && git pull\`
2. Create tag: \`git tag v${VERSION}\`
3. Push tag: \`git push origin v${VERSION}\`

This will trigger the release workflow to build cross-platform binaries:
- Linux (x86_64, aarch64)
- macOS (x86_64, aarch64/Apple Silicon)
- Windows (x86_64)
EOF
)"
```

### 1.8 Wait for CI

```bash
gh pr checks <PR_NUMBER> --watch
```

All checks must pass before merging:

- Format, Clippy, Unit Tests, Code Coverage
- **Integration Tests** (CCH + Claude CLI end-to-end validation)
- Build Release (5 platforms)
- CI Success

**Note:** Integration tests validate that CCH hooks work correctly with the real Claude CLI. These are critical gate checks - do NOT skip them.

---

## Phase 2: Execute Release

### 2.1 Merge the Release PR

```bash
gh pr merge <PR_NUMBER> --merge --delete-branch
```

### 2.2 Sync Local Main

```bash
git checkout main
git pull
```

### 2.3 Create and Push Tag

```bash
VERSION=$(.opencode/skill/release-cch/scripts/read-version.sh)
git tag v${VERSION}
git push origin v${VERSION}
```

This triggers the release workflow automatically.

---

## Phase 3: Verify Release

### 3.1 Monitor Workflow

```bash
.opencode/skill/release-cch/scripts/verify-release.sh
```

Or manually:

```bash
gh run list --limit 3
gh run view <RUN_ID> --watch
```

### 3.2 Verify Release Assets

```bash
VERSION=$(.opencode/skill/release-cch/scripts/read-version.sh)
gh release view v${VERSION}
```

Expected assets (6 total):

- cch-linux-x86_64.tar.gz
- cch-linux-aarch64.tar.gz
- cch-macos-x86_64.tar.gz
- cch-macos-aarch64.tar.gz
- cch-windows-x86_64.exe.zip
- checksums.txt

### 3.3 Announce Release

Once verified, the release is live at:

```
https://github.com/SpillwaveSolutions/code_agent_context_hooks/releases/tag/v${VERSION}
```

---

## Phase 4: Hotfix Release

Use this when you need to release a patch (e.g., v1.0.1) from an existing release tag.

### 4.1 Create Hotfix Branch from Tag

```bash
# Checkout the tag you want to patch
git fetch --tags
git checkout v1.0.0

# Create hotfix branch
git checkout -b hotfix/v1.0.1
```

### 4.2 Apply Fix

Make the minimal fix needed, then run checks:

```bash
cd cch_cli && cargo fmt && cargo clippy --all-targets --all-features -- -D warnings && cargo test
```

### 4.3 Update Version

Edit `Cargo.toml` at the workspace root:

```toml
[workspace.package]
version = "1.0.1"
```

### 4.4 Update Changelog

Add entry to `CHANGELOG.md`:

```markdown
## [1.0.1] - YYYY-MM-DD

### Fixed

- Description of the hotfix
```

### 4.5 Commit and Push

```bash
git add -A
git commit -m "fix: <description of hotfix>

Hotfix for v1.0.0 addressing <issue description>"
git push -u origin hotfix/v1.0.1
```

### 4.6 Create PR to Main

```bash
gh pr create \
  --title "fix: hotfix v1.0.1" \
  --body "## Hotfix Release

Patches v1.0.0 with critical fix for <issue>.

### Changes
- <description>

### Release Steps After Merge
1. \`git checkout main && git pull\`
2. \`git tag v1.0.1\`
3. \`git push origin v1.0.1\`"
```

### 4.7 After PR Merge - Tag and Release

```bash
gh pr merge <PR_NUMBER> --merge --delete-branch
git checkout main && git pull
git tag v1.0.1
git push origin v1.0.1
```

### 4.8 Verify Hotfix Release

```bash
.opencode/skill/release-cch/scripts/verify-release.sh 1.0.1
```

---

## Integration Tests (Required)

Integration tests validate CCH works correctly with the real Claude CLI. **These must pass before any release.**

### Running Integration Tests

```bash
# Via Taskfile (recommended)
task integration-test

# Or directly
./test/integration/run-all.sh

# Quick mode (skip slow tests)
task integration-test-quick

# Single test
./test/integration/run-all.sh --test 01-block-force-push
```

### Test Cases

| Test | What It Validates |
|------|-------------------|
| `01-block-force-push` | CCH blocks dangerous git operations |
| `02-context-injection` | CCH injects context for file types |
| `03-session-logging` | CCH creates proper audit logs |
| `04-permission-explanations` | CCH provides permission context |

### Prerequisites

- Claude CLI installed and in PATH
- CCH binary built (auto-built by test runner)

### If Tests Fail

1. Check Claude CLI is installed: `which claude`
2. Check CCH builds: `cd cch_cli && cargo build --release`
3. Run with debug: `DEBUG=1 ./test/integration/run-all.sh`
4. Check logs: `~/.claude/logs/cch.log`

For details, see [Integration Test README](../../../test/integration/README.md).

---

## Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `read-version.sh` | Extract version from Cargo.toml | `./scripts/read-version.sh` |
| `generate-changelog.sh` | Generate changelog from commits | `./scripts/generate-changelog.sh [version]` |
| `preflight-check.sh` | Run all pre-release checks (includes integration tests) | `./scripts/preflight-check.sh [--json]` |
| `verify-release.sh` | Monitor release workflow status | `./scripts/verify-release.sh [version]` |

All scripts are located in `.opencode/skill/release-cch/scripts/`.

---

## References

- [release-workflow.md](references/release-workflow.md) - Standard release workflow diagram
- [hotfix-workflow.md](references/hotfix-workflow.md) - Hotfix release workflow diagram
- [troubleshooting.md](references/troubleshooting.md) - Common issues and solutions

---

## Quick Command Reference

### Standard Release

```bash
# 1. Update version in Cargo.toml manually
# 2. Create release branch
VERSION=$(.opencode/skill/release-cch/scripts/read-version.sh)
git checkout -b release/v${VERSION}

# 3. Run checks
.opencode/skill/release-cch/scripts/preflight-check.sh

# 4. Generate changelog, review, commit
.opencode/skill/release-cch/scripts/generate-changelog.sh ${VERSION}
# Edit CHANGELOG.md as needed
git add CHANGELOG.md Cargo.toml
git commit -m "chore: prepare v${VERSION} release"
git push -u origin release/v${VERSION}

# 5. Create and merge PR
gh pr create --title "chore: prepare v${VERSION} release" --body "..."
gh pr checks <PR> --watch
gh pr merge <PR> --merge --delete-branch

# 6. Tag and release
git checkout main && git pull
git tag v${VERSION}
git push origin v${VERSION}

# 7. Verify
.opencode/skill/release-cch/scripts/verify-release.sh
```

### Hotfix Release

```bash
# 1. Branch from tag
git checkout v1.0.0
git checkout -b hotfix/v1.0.1

# 2. Fix, update version, update changelog
# 3. Commit, push, PR, merge
# 4. Tag and release
git checkout main && git pull
git tag v1.0.1
git push origin v1.0.1
```
