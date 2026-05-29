---
name: release
scope: universal
description: |
  Semantic versioning and changelog formatting for software releases.
  Use when: preparing releases, updating version numbers, writing changelogs.
  Keywords: version, release, changelog, semver, major, minor, patch, 版本, 發布, 變更日誌.
---

# Release Standards

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/release-standards/SKILL.md)

**Version**: 1.1.0
**Last Updated**: 2026-01-02
**Applicability**: Claude Code Skills

---

> **Core Standard**: This skill implements [Versioning](../../core/versioning.md). For comprehensive methodology documentation, refer to the core standard.

## Purpose

This skill provides semantic versioning and changelog formatting standards.

## Quick Reference

### Semantic Versioning Format

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Examples:
2.3.1
1.0.0-alpha.1
3.2.0-beta.2+20250112
```

### Version Incrementing Rules

| Component | When to Increment | Example |
|-----------|-------------------|----------|
| **MAJOR** | Breaking changes | 1.9.5 → 2.0.0 |
| **MINOR** | New features (backward-compatible) | 2.3.5 → 2.4.0 |
| **PATCH** | Bug fixes (backward-compatible) | 3.1.2 → 3.1.3 |

### Pre-release Identifiers

| Identifier | Stability | Audience |
|------------|-----------|----------|
| `alpha` | Unstable | Internal team |
| `beta` | Mostly stable | Early adopters |
| `rc` | Stable | Beta testers |

### CHANGELOG Categories

| Category | Usage |
|----------|-------|
| **Added** | New features |
| **Changed** | Changes in existing functionality |
| **Deprecated** | Soon to be removed |
| **Removed** | Removed features |
| **Fixed** | Bug fixes |
| **Security** | Vulnerability fixes |

## Detailed Guidelines

For complete standards, see:
- [Semantic Versioning Guide](./semantic-versioning.md)
- [Changelog Format](./changelog-format.md)
- [Release Workflow Guide](./release-workflow.md) - Complete release process for this project

### AI-Optimized Format (Token-Efficient)

For AI assistants, use the YAML format file for reduced token usage:
- Changelog: `ai/standards/changelog.ai.yaml`

## CHANGELOG Entry Format

```markdown
## [VERSION] - YYYY-MM-DD

### Added
- Add user dashboard with customizable widgets (#123)

### Changed
- **BREAKING**: Change API response format from XML to JSON

### Fixed
- Fix memory leak when processing large files (#456)

### Security
- Fix SQL injection vulnerability (CVE-2025-12345)
```

## Breaking Changes

Mark breaking changes with **BREAKING** prefix:

```markdown
### Changed
- **BREAKING**: Remove deprecated `getUserById()`, use `getUser()` instead
```

## Git Tagging

```bash
# Create annotated tag (recommended)
git tag -a v1.2.0 -m "Release version 1.2.0"

# Push tag to remote
git push origin v1.2.0
```

## Version Ordering

```
1.0.0-alpha.1 < 1.0.0-alpha.2 < 1.0.0-beta.1 < 1.0.0-rc.1 < 1.0.0
```

---

## Configuration Detection

This skill supports project-specific configuration.

### Detection Order

1. Check `CONTRIBUTING.md` for "Disabled Skills" section
   - If this skill is listed, it is disabled for this project
2. Check `CONTRIBUTING.md` for "Release Standards" section
3. If not found, **default to Semantic Versioning and Keep a Changelog format**

### First-Time Setup

If no configuration found and context is unclear:

1. Ask the user: "This project hasn't configured release standards. Would you like to use Semantic Versioning?"
2. After user selection, suggest documenting in `CONTRIBUTING.md`:

```markdown
## Release Standards

### Versioning
This project uses **Semantic Versioning** (MAJOR.MINOR.PATCH).

### Changelog
This project follows **Keep a Changelog** format.
```

### Configuration Example

In project's `CONTRIBUTING.md`:

```markdown
## Release Standards

### Versioning
This project uses **Semantic Versioning** (MAJOR.MINOR.PATCH).

### Changelog
This project follows **Keep a Changelog** format.

### Release Process
1. Update version in package.json
2. Update CHANGELOG.md
3. Create git tag with `v` prefix (e.g., v1.2.0)
4. Push tag to trigger release workflow
```

---

## Related Standards

- [Versioning](../../core/versioning.md) - Core semantic versioning standard
- [Changelog Standards](../../core/changelog-standards.md) - Keep a Changelog format
- [Git Workflow](../../core/git-workflow.md) - Git tagging and release branches

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-01-02 | Added: Release Workflow Guide with complete release process |
| 1.0.0 | 2025-12-24 | Added: Standard sections (Purpose, Related Standards, Version History, License) |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
