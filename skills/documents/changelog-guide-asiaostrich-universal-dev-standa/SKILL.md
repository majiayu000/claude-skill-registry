---
name: changelog
scope: partial
description: |
  Write and maintain CHANGELOG.md following Keep a Changelog format.
  Use when: creating changelog entries, preparing releases, documenting changes.
  Keywords: changelog, release notes, CHANGELOG.md, keep a changelog, 變更日誌, 發布說明.
---

# Changelog Guide

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/changelog-guide/SKILL.md)

**Version**: 1.0.0
**Last Updated**: 2025-12-30
**Applicability**: Claude Code Skills

---

> **Core Standard**: This skill implements [Changelog Standards](../../core/changelog-standards.md). For comprehensive methodology documentation, refer to the core standard.

## Purpose

This skill helps write and maintain CHANGELOG.md files following the Keep a Changelog format, ensuring clear communication of changes to users.

## Quick Reference

### File Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.2.0] - 2025-12-15

### Added
- Feature description

### Changed
- Change description

### Fixed
- Bug fix description

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
```

### Change Categories

| Category | When to Use | Example |
|----------|-------------|---------|
| **Added** | New features | Add dark mode support |
| **Changed** | Modifications to existing features | Improve search performance by 50% |
| **Deprecated** | Features to be removed | Deprecate legacyParse() |
| **Removed** | Removed features | Remove Node.js 14 support |
| **Fixed** | Bug fixes | Fix login timeout issue |
| **Security** | Security patches | Fix XSS vulnerability |

### Commit Type to Changelog Mapping

| Commit Type | Changelog Category | Notes |
|-------------|-------------------|-------|
| `feat` | **Added** | New features |
| `fix` | **Fixed** | Bug fixes |
| `perf` | **Changed** | Performance improvements |
| `security` | **Security** | Security patches |
| `BREAKING CHANGE` | **Changed** or **Removed** | With **BREAKING** prefix |
| `refactor`, `docs`, `style`, `test`, `chore` | *(usually omit)* | No user impact |

## Entry Format

### Standard Format

```markdown
- [Action verb] [what changed] ([reference])
```

### Examples

```markdown
### Added
- Add user dashboard with customizable widgets (#123)
- Add support for PostgreSQL 15 (PR #456)

### Changed
- **BREAKING**: Change API response format from XML to JSON (#789)
- Update minimum Node.js version to 18.0 (#101)

### Fixed
- Fix memory leak when processing large files (#112)
- Fix incorrect date formatting in reports (#134)

### Security
- Fix SQL injection vulnerability in search endpoint (HIGH, CVE-2025-12345)
```

## Detailed Guidelines

For complete standards, see:
- [Changelog Standards](../../core/changelog-standards.md)

### AI-Optimized Format (Token-Efficient)

For AI assistants, use the YAML format files for reduced token usage:
- Base standard: `ai/standards/changelog.ai.yaml`

## Writing Guidelines

### Write for Users, Not Developers

| ✅ Good | ❌ Bad | Why |
|---------|--------|-----|
| Add dark mode theme option | Implement ThemeProvider with context | User-facing benefit |
| Fix login timeout on slow networks | Fix race condition in AuthService | Impact description |
| Improve page load speed by 40% | Optimize SQL queries with indexes | Measurable outcome |

### Breaking Changes

Always mark breaking changes clearly:

```markdown
### Changed
- **BREAKING**: Remove deprecated `getUserById()` method, use `getUser()` instead
- **BREAKING**: Change configuration file format from YAML to TOML

### Removed
- **BREAKING**: Remove support for Node.js 14
```

### Security Advisories

Include severity and CVE if available:

```markdown
### Security
- Fix SQL injection vulnerability in search endpoint (HIGH, CVE-2025-12345)
- Fix XSS vulnerability in comment rendering (MEDIUM)
- Update dependency `lodash` to patch prototype pollution (LOW)
```

## Version Header Format

```markdown
## [VERSION] - YYYY-MM-DD
```

Examples:
```markdown
## [2.0.0] - 2025-12-15
## [1.5.0-beta.1] - 2025-12-01
## [Unreleased]
```

## Exclusion Rules

The following should **NOT** be recorded in CHANGELOG:

| Category | Examples | Reason |
|----------|----------|--------|
| Build outputs | `dist/`, `build/` | Generated files |
| Dependencies | `node_modules/`, lock files | Auto-managed |
| Local config | `.env`, `*.local.json` | Environment-specific |
| IDE settings | `.vscode/`, `.idea/` | Developer preference |
| Internal refactoring | Code style, variable names | No user impact |

## Common Mistakes

| ❌ Mistake | ✅ Correct |
|-----------|-----------|
| No dates | Include dates in ISO format |
| Missing version links | Add comparison links at bottom |
| Internal jargon | Use user-friendly language |
| Too technical | Focus on user impact |
| No categories | Use standard categories |

---

## Configuration Detection

This skill supports project-specific configuration.

### Detection Order

1. Check for existing `CHANGELOG.md` format
2. Check `CONTRIBUTING.md` for changelog guidelines
3. If not found, **default to Keep a Changelog format**

### First-Time Setup

If no CHANGELOG.md exists:

1. Suggest creating one with the standard template
2. Suggest documenting guidelines in `CONTRIBUTING.md`:

```markdown
## Changelog Guidelines

- Update CHANGELOG.md for all user-facing changes
- Add entries to [Unreleased] section during development
- Use standard categories: Added, Changed, Deprecated, Removed, Fixed, Security
- Reference issue/PR numbers: `Fix bug (#123)`
- Mark breaking changes with **BREAKING** prefix
```

---

## Related Standards

- [Changelog Standards](../../core/changelog-standards.md)
- [Versioning Standard](../../core/versioning.md)
- [Commit Message Guide](../../core/commit-message-guide.md)
- [Release Standards Skill](../release-standards/SKILL.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-30 | Initial release |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
