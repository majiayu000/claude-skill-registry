---
name: agent-ops-versioning
description: "Manage semantic versioning, changelog generation, and release notes. Auto-generates entries from completed issues or git diff."
license: MIT
compatibility: [opencode, claude, cursor]

metadata:
  category: docs
  related: [agent-ops-state, agent-ops-git]

---

# Versioning & Release Management

## Purpose
Manage semantic versioning, generate changelogs from completed issues or git history, and coordinate releases.

## Input Sources

Changelog entries can be generated from multiple sources:

| Source | Command | Best For |
|--------|---------|----------|
| **Issues** (default) | `/agent-version bump minor` | Teams using issue-first workflow |
| **Git diff** | `/agent-version bump minor --from main` | Teams not using AgentOps issues |
| **Git tags** | `/agent-version bump minor --from v2.0.0` | Compare against specific release |
| **Hybrid** | `/agent-version bump minor --include-git` | Catch commits without issues |

## Semantic Versioning Rules

Follow [SemVer 2.0.0](https://semver.org/):

| Bump | When | Example |
|------|------|---------|
| **MAJOR** | Breaking changes, incompatible API changes | 1.0.0 → 2.0.0 |
| **MINOR** | New features, backward compatible | 1.0.0 → 1.1.0 |
| **PATCH** | Bug fixes, backward compatible | 1.0.0 → 1.0.1 |

### Pre-release Tags
- `-alpha.1` — Early development, unstable
- `-beta.1` — Feature complete, testing
- `-rc.1` — Release candidate, final testing

### Build Metadata
- `+build.123` — CI build number
- `+20260115` — Build date

## Operations

### 1. Version Bump

```
`agent-version` bump {major|minor|patch} [--prerelease {alpha|beta|rc}]
```

**Procedure:**
1. Read current version from README.md badge or package.json
2. Calculate new version based on bump type
3. Scan `issues/history.md` for issues since last version tag
4. Generate changelog entries
5. Update files:
   - CHANGELOG.md — Add new version section
   - README.md — Update version badge and history table
   - package.json (if exists) — Update version field
6. Suggest git tag command (never auto-create)

**Output:**
```
📦 Version Bump: 2.0.0 → 2.1.0

Changes detected (12 issues):
- Added: 5 features
- Fixed: 4 bugs  
- Changed: 2 enhancements
- Security: 1 fix

Files to update:
- [x] CHANGELOG.md
- [x] README.md (badge + history)
- [ ] package.json (not found)

Preview CHANGELOG entry? [Y/n]
```

### 2. Changelog Generation

Auto-generate changelog entries from completed issues.

**Mapping issue types to changelog sections:**

| Issue Type | Changelog Section |
|------------|-------------------|
| `FEAT` | Added |
| `ENH` | Changed |
| `BUG` | Fixed |
| `SEC` | Security |
| `PERF` | Performance |
| `DOCS` | Documentation |
| `REFAC` | Changed |
| `CHORE` | Maintenance |
| `TEST` | Testing |

**Entry format:**
```markdown
### Added
- **FEAT-0042**: Add dark mode support ([details](issues/references/FEAT-0042.md))
- **FEAT-0038**: Implement OAuth login

### Fixed
- **BUG-0023**: Fix login timeout after 30s idle
- **BUG-0019**: Resolve null pointer in UserService
```

### 3. Release Notes

Generate user-friendly release notes (less technical than changelog).

```
`agent-version` release-notes
```

**Output format:**
```markdown
# Release Notes: v2.1.0

## 🎉 What's New

### Dark Mode
You can now switch to dark mode! Go to Settings → Appearance → Theme.

### OAuth Login  
Sign in with Google or GitHub for faster access.

## 🐛 Bug Fixes

- Fixed an issue where sessions would timeout too quickly
- Resolved crashes on the user profile page

## 🔒 Security

- Updated authentication to prevent session hijacking

---
*Full technical changelog: [CHANGELOG.md](CHANGELOG.md)*
```

### 4. Version Validation

Check that versions are consistent across files.

```
`agent-version` check
```

**Validates:**
- README.md badge matches CHANGELOG.md latest version
- package.json version matches (if exists)
- Git tags exist for released versions
- No unreleased issues in history older than 30 days

**Output:**
```
✅ Version Check

Current: v2.0.0
- README.md badge: ✅ 2.0.0
- CHANGELOG.md latest: ✅ 2.0.0
- package.json: ⚠️ not found
- Git tag v2.0.0: ✅ exists

Unreleased issues: 3 (since 2026-01-10)
Suggestion: Consider v2.0.1 or v2.1.0 release
```

### 5. What's Unreleased

Show issues completed since last release.

```
`agent-version` unreleased
```

**Output:**
```
📋 Unreleased Changes (since v2.0.0)

Added:
- FEAT-0045: Add export to PDF
- FEAT-0044: Implement search filters

Fixed:
- BUG-0048: Fix date picker timezone issue

Suggested version: 2.1.0 (new features, no breaking changes)
```

### 6. Changelog from Git Diff

Generate changelog entries from git commits between branches or tags.

```
`agent-version` from-git {base} [target]
```

**Examples:**
```bash
`agent-version` from-git main              # Compare current branch to main
`agent-version` from-git v2.0.0            # Compare HEAD to tag v2.0.0
`agent-version` from-git main feature/xyz  # Compare two branches
`agent-version` from-git v1.0.0 v2.0.0     # Compare two tags
```

**Procedure:**
1. Run `git log {base}..{target} --oneline`
2. Parse commit messages using conventional commits format
3. Group by type (feat, fix, chore, etc.)
4. Generate changelog entries
5. Flag commits without conventional format for manual review

**Conventional Commit Parsing:**

| Commit Prefix | Changelog Section |
|---------------|-------------------|
| `feat:` `feat(scope):` | Added |
| `fix:` `fix(scope):` | Fixed |
| `docs:` | Documentation |
| `perf:` | Performance |
| `refactor:` | Changed |
| `chore:` | Maintenance |
| `test:` | Testing |
| `BREAKING CHANGE:` | ⚠️ Breaking |

**Output:**
```
📋 Git Diff Analysis: main..HEAD (23 commits)

Parsed (conventional commits):
- feat: 5 commits → Added
- fix: 8 commits → Fixed
- chore: 4 commits → Maintenance
- docs: 2 commits → Documentation

Unparsed (needs manual review):
- "Update stuff" (abc1234)
- "WIP" (def5678)
- "misc fixes" (ghi9012)

Suggested version: MINOR (new features detected)

Generate changelog from these? [Y/n]
```

**Hybrid Mode:**

Combine issues and git for comprehensive changelog:

```
`agent-version` bump minor --include-git
```

1. Start with issues from `history.md`
2. Run git diff to find additional commits
3. Flag commits that don't have matching issues
4. User reviews and approves additions

```
📋 Hybrid Changelog Generation

From issues (12 entries):
- FEAT-0045: Add export to PDF
- BUG-0048: Fix date picker issue
...

From git (not in issues):
⚠️ 3 commits found without matching issues:
- abc1234: feat: add keyboard shortcuts
- def5678: fix: resolve memory leak
- ghi9012: chore: update dependencies

Include these in changelog? [A]ll / [S]elect / [N]one
```

## Version File Locations

| File | Version Location |
|------|------------------|
| README.md | Badge: `![Version](https://img.shields.io/badge/version-X.Y.Z-blue.svg)` |
| CHANGELOG.md | Header: `## [X.Y.Z] - YYYY-MM-DD` |
| package.json | Field: `"version": "X.Y.Z"` |
| pyproject.toml | Field: `version = "X.Y.Z"` |
| Cargo.toml | Field: `version = "X.Y.Z"` |
| *.csproj | Tag: `<Version>X.Y.Z</Version>` |

## Changelog Format

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
# Changelog

## [Unreleased]

## [2.1.0] - 2026-01-20

### Added
- New feature X

### Changed
- Updated feature Y

### Deprecated
- Feature Z will be removed in 3.0.0

### Removed
- Deleted legacy API

### Fixed
- Bug in feature W

### Security
- Patched vulnerability in auth
```

## Git Tag Suggestions

After version bump, suggest (never auto-execute):

```
Suggested commands:

git add CHANGELOG.md README.md
git commit -m "chore: release v2.1.0"
git tag -a v2.1.0 -m "Release v2.1.0"
git push origin main --tags

Create these commits/tags? This will invoke agent-ops-git.
```

## Integration

- **agent-ops-git**: Coordinates commit and tag creation
- **agent-ops-report**: Can include version in reports
- **agent-ops-housekeeping**: Warns about stale unreleased changes
