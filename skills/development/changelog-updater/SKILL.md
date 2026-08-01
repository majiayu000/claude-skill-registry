---
name: changelog-updater
description: 更新 CHANGELOG.md。觸發：changelog、變更、版本、發布、改了什麼。
---

---
name: changelog-updater
description: Maintain and update CHANGELOG.md following Keep a Changelog format. Use when: updating changelog, version documentation, release notes, semver versioning, categorizing changes (Added/Changed/Fixed/Security).
---

# Changelog Updater

Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/) format.

## Structure

```markdown
# Changelog

## [Unreleased]

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Features to be removed

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security fixes

## [X.Y.Z] - YYYY-MM-DD
...
```

## Update Process

1. Run `git log v2.1.0..HEAD --oneline` to see changes
2. Categorize each significant commit
3. Write user-facing descriptions
4. Update version number per semver
5. Move entries from [Unreleased] to version section

## Version Guidelines

**MAJOR** (X.0.0): Breaking changes
**MINOR** (X.Y.0): New features, backwards compatible
**PATCH** (X.Y.Z): Bug fixes, backwards compatible

## Entry Format

```markdown
### Added
- Brief description in user-facing language
- Reference issue: #123
```

## Good Examples

```markdown
### Added
- Browser node connection pooling for 60% faster execution
- PostgreSQL async support with connection pooling

### Fixed
- Variable resolution in nested workflows (#234)
- Memory leak in browser resource manager
```
