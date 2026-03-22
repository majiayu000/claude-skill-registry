---
name: release
description: Release workflow — version bump, changelog generation, git tag, release notes. Use when preparing a new version for deployment.
disable-model-invocation: true
argument-hint: [version-number]
---

# Release

Structured workflow for preparing a release. Bumps version, generates changelog, creates git tag, and produces release notes.

## 1. Determine Release Type

Ask the user (or infer from commits since last release):

- **Major** (X.0.0): Breaking changes, removed APIs, major architecture shifts
- **Minor** (x.Y.0): New features, non-breaking API additions
- **Patch** (x.y.Z): Bug fixes, security patches, dependency updates

```
// turbo
git describe --tags --abbrev=0 2>/dev/null || echo "No tags found"
```

```
// turbo
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~20")..HEAD --oneline
```

## 2. Analyze Changes

Classify commits since last release:

| Type | Changelog Section |
|---|---|
| `feat` | ✨ Features |
| `fix` | 🐛 Bug Fixes |
| `perf` | ⚡ Performance |
| `refactor` | ♻️ Refactoring |
| `docs` | 📚 Documentation |
| `chore`/`ci` | 🔧 Maintenance |
| `BREAKING CHANGE` | ⚠️ Breaking Changes |

## 3. Bump Version

Update version in project files:

| Stack | Files to Update |
|---|---|
| Node.js | `package.json` (`version` field) |
| Java/Maven | `pom.xml` (`<version>`) |
| Java/Gradle | `build.gradle` (`version`) |
| Python | `pyproject.toml` (`version`) |
| .NET | `*.csproj` (`<Version>`) |
| Go | Git tag only (no version file) |

## 4. Generate Changelog

Add entry to `CHANGELOG.md` (create if not exists):

```markdown
## [X.Y.Z] - YYYY-MM-DD

### ⚠️ Breaking Changes
- Description (commit ref)

### ✨ Features
- Description (commit ref)

### 🐛 Bug Fixes
- Description (commit ref)

### ⚡ Performance
- Description (commit ref)

### 🔧 Maintenance
- Description (commit ref)
```

## 5. Create Release Commit

Present the changes for user review.

After approval, suggest:

```
git add -A
git commit -m "chore(release): vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

**⚠️ Do NOT run git commands without user confirmation.** This workflow explicitly overrides the "no git write ops" Hard Rule — git ops are permitted here only after user APPROVE.

## 6. Release Notes

Generate release notes for GitHub/GitLab:

```markdown
# Release vX.Y.Z

## Highlights
[1-3 sentence summary of the most important changes]

## What's Changed
[Changelog content from Step 4]

## Upgrade Guide
[If breaking changes — step-by-step migration instructions]

## Contributors
[List contributors from git log]
```

## 7. Next Steps

Suggest post-release actions:
- Push tag: `git push origin vX.Y.Z`
- Push branch: `git push`
- Create GitHub Release with release notes
- Deploy to staging: `/deploy-staging`
- Deploy to production: `/deploy-production`
- Announce release to team

## Integration

- **Preceded by**: `/code-review` (all PRs merged)
- **Followed by**: `/deploy-staging`, `/deploy-production`
