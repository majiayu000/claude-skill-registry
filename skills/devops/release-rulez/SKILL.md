---
name: release-rulez
description: RuleZ release workflow automation. Use when asked to "release RuleZ", "create a release", "prepare release", "tag version", "hotfix release", or "publish RuleZ". Covers version management from Cargo.toml, changelog generation from conventional commits, PR creation, tagging, hotfix workflows, and GitHub Actions release monitoring.
metadata:
  version: "1.0.0"
  project: "rulez"
  source_of_truth: "Cargo.toml"
---

# release-rulez

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
| Linux x86_64 | x86_64-unknown-linux-gnu | rulez-linux-x86_64.tar.gz |
| Linux ARM64 | aarch64-unknown-linux-gnu | rulez-linux-aarch64.tar.gz |
| macOS Intel | x86_64-apple-darwin | rulez-macos-x86_64.tar.gz |
| macOS Apple Silicon | aarch64-apple-darwin | rulez-macos-aarch64.tar.gz |
| Windows | x86_64-pc-windows-msvc | rulez-windows-x86_64.exe.zip |

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
.claude/skills/release-rulez/scripts/read-version.sh
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
VERSION=$(.claude/skills/release-rulez/scripts/read-version.sh)
git checkout -b release/v${VERSION}
```

### 1.4 Run Pre-flight Checks

```bash
.claude/skills/release-rulez/scripts/preflight-check.sh
```

This validates:

- [ ] Clean working directory (or only release files modified)
- [ ] All unit tests pass (`cargo test`)
- [ ] All integration tests pass (`task integration-test`)
- [ ] Clippy has no warnings
- [ ] Format check passes

**IMPORTANT:** Integration tests are REQUIRED before any release.

### 1.5 Generate Changelog

```bash
VERSION=$(.claude/skills/release-rulez/scripts/read-version.sh)
.claude/skills/release-rulez/scripts/generate-changelog.sh ${VERSION}
```

### 1.6 Commit and Push

```bash
VERSION=$(.claude/skills/release-rulez/scripts/read-version.sh)
git add CHANGELOG.md Cargo.toml
git commit -m "chore: prepare v${VERSION} release"
git push -u origin release/v${VERSION}
```

### 1.7 Create Release PR

```bash
VERSION=$(.claude/skills/release-rulez/scripts/read-version.sh)
gh pr create --title "chore: prepare v${VERSION} release" --body "..."
```

### 1.8 Monitor CI and Auto-Merge

Use `/loop` to poll PR checks every 5 minutes. When all checks pass, automatically merge and continue to Phase 2 (tag and push).

```
/loop 5m check PR #<PR_NUMBER> status: run `gh pr checks <PR_NUMBER>`. If all checks pass, merge with `gh pr merge <PR_NUMBER> --squash --delete-branch`, then sync main (`git checkout main && git pull`), tag (`git tag v<VERSION> && git push origin v<VERSION>`), and verify the release workflow started. If checks are still pending, report status and wait. If any check failed, report the failure details and stop.
```

**What the loop does each cycle:**
1. Runs `gh pr checks <PR_NUMBER>` to get current status
2. If all checks pass -> auto-merges the PR, syncs main, creates and pushes the tag, verifies the release workflow triggered, then cancels the loop
3. If checks are pending -> reports progress (N/M passing) and waits for next cycle
4. If any check failed -> reports the failure, cancels the loop, and alerts the user

**Important:** The loop handles the full Phase 1.8 -> Phase 2 transition automatically. Once the tag is pushed, proceed to Phase 3 (verify) manually or set up another loop.

---

## Phase 2: Execute Release

> **Note:** If you used the `/loop` auto-merge in Phase 1.8, Phase 2 is already done. Skip to Phase 3.

### 2.1 Merge the Release PR

```bash
gh pr merge <PR_NUMBER> --squash --delete-branch
```

### 2.2 Sync Local Main

```bash
git checkout main
git pull
```

### 2.3 Create and Push Tag

```bash
VERSION=$(.claude/skills/release-rulez/scripts/read-version.sh)
git tag v${VERSION}
git push origin v${VERSION}
```

---

## Phase 3: Verify Release

### 3.1 Monitor Workflow

```bash
.claude/skills/release-rulez/scripts/verify-release.sh
```

### 3.2 Verify Release Assets

```bash
VERSION=$(.claude/skills/release-rulez/scripts/read-version.sh)
gh release view v${VERSION}
```

---

## Phase 4: Hotfix Release

See [hotfix-workflow.md](references/hotfix-workflow.md) for detailed steps.

---

## Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `read-version.sh` | Extract version from Cargo.toml | `./scripts/read-version.sh` |
| `generate-changelog.sh` | Generate changelog from commits | `./scripts/generate-changelog.sh [version]` |
| `preflight-check.sh` | Run all pre-release checks | `./scripts/preflight-check.sh [--json]` |
| `verify-release.sh` | Monitor release workflow status | `./scripts/verify-release.sh [version]` |

All scripts are located in `.claude/skills/release-rulez/scripts/`.

---

## References

- [release-workflow.md](references/release-workflow.md) - Standard release workflow diagram
- [hotfix-workflow.md](references/hotfix-workflow.md) - Hotfix release workflow diagram
- [troubleshooting.md](references/troubleshooting.md) - Common issues and solutions
