---
name: release-version
description: 'Guide for creating new Orient releases with proper versioning, changelogs, and Docker image tags'
---

# Release Version

Guide for creating new Orient releases with proper versioning, changelogs, and Docker image tags.

## Triggers

- "create a release"
- "release version X.Y.Z"
- "tag a new version"
- "prepare release"

## Release Process

### 1. Update CHANGELOG.md

Before creating a release, ensure the changelog is up to date:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added

- New features

### Changed

- Modifications to existing features

### Fixed

- Bug fixes

### Migrations

- Database migrations (if any)
```

Move items from `[Unreleased]` to the new version section.

Add the version link at the bottom:

```markdown
[X.Y.Z]: https://github.com/orient-bot/orient/releases/tag/vX.Y.Z
```

Update the `[Unreleased]` link:

```markdown
[Unreleased]: https://github.com/orient-bot/orient/compare/vX.Y.Z...HEAD
```

### 2. Create the Release Tag

```bash
# Create annotated tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# Push tag to trigger release workflow
git push origin vX.Y.Z
```

### 3. Automated Actions

The `.github/workflows/release.yml` workflow automatically:

1. **Creates GitHub Release** - With auto-generated release notes from PRs
2. **Tags Docker Images** - Adds version tag to existing `:latest` images:
   - `ghcr.io/orient-bot/orient/opencode:vX.Y.Z`
   - `ghcr.io/orient-bot/orient/whatsapp-bot:vX.Y.Z`
   - `ghcr.io/orient-bot/orient/dashboard:vX.Y.Z`

## Pre-Release Checklist

Before tagging a release:

- [ ] All CI checks pass on main branch
- [ ] CHANGELOG.md updated with all changes
- [ ] Database migrations documented
- [ ] Breaking changes documented
- [ ] Docker images build successfully (`:latest` exists)

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR (X)**: Breaking changes
- **MINOR (Y)**: New features, backwards compatible
- **PATCH (Z)**: Bug fixes, backwards compatible

### Pre-release Tags

For testing releases before official publication:

```bash
# Alpha/beta releases
git tag -a v0.2.0-alpha.1 -m "Alpha release for testing"
git tag -a v0.2.0-beta.1 -m "Beta release for testing"

# Release candidates
git tag -a v0.2.0-rc.1 -m "Release candidate 1"
```

Pre-releases are marked automatically in GitHub based on the `-` in the tag.

## Docker Image Versioning

| Tag              | Description                        |
| ---------------- | ---------------------------------- |
| `:latest`        | Most recent build from main branch |
| `:vX.Y.Z`        | Specific release version           |
| `:vX.Y.Z-suffix` | Pre-release version                |

## Troubleshooting

### Docker tag job fails

If the Docker tagging job fails:

1. Ensure `:latest` images exist on GHCR
2. Check `GITHUB_TOKEN` has `packages: write` permission
3. Verify the repository name matches the image prefix

Manual recovery:

```bash
# Pull, tag, and push manually
docker pull ghcr.io/orient-bot/orient/opencode:latest
docker tag ghcr.io/orient-bot/orient/opencode:latest ghcr.io/orient-bot/orient/opencode:vX.Y.Z
docker push ghcr.io/orient-bot/orient/opencode:vX.Y.Z
```

### Release notes are empty

GitHub auto-generates notes from merged PRs. If empty:

1. Check PRs have proper titles (used as release note entries)
2. Manually edit the release to add notes
3. Reference CHANGELOG.md for the version's changes

### Wrong version tagged

```bash
# Delete local and remote tag
git tag -d vX.Y.Z
git push origin :refs/tags/vX.Y.Z

# Delete the GitHub release (if created)
gh release delete vX.Y.Z --yes

# Create correct tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

## Related Files

- `CHANGELOG.md` - Root changelog (Keep a Changelog format)
- `.github/workflows/release.yml` - Release automation workflow
- `releases/` - Historical release notes (archive)
