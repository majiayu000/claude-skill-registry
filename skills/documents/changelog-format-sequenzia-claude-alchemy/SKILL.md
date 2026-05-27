---
description: Keep a Changelog format guidelines and entry writing best practices
triggers:
  - changelog format
  - keep a changelog
  - changelog entry
  - write changelog
  - changelog categories
  - changelog best practices
---

# Keep a Changelog Format

This skill provides guidelines for writing and formatting changelogs following the [Keep a Changelog](https://keepachangelog.com/) specification.

## Core Principles

1. **Changelogs are for humans** - Write for users, not machines
2. **Every version gets a section** - Including `[Unreleased]` for upcoming changes
3. **Changes are grouped by type** - Consistent categorization
4. **Versions are linkable** - Each version header links to comparison
5. **Latest version comes first** - Reverse chronological order
6. **Release dates are shown** - ISO format: YYYY-MM-DD

## Change Categories

Use these categories in this order:

| Category | Description | When to Use |
|----------|-------------|-------------|
| **Added** | New features | New functionality users can now do |
| **Changed** | Changes in existing functionality | Behavior modifications, improvements |
| **Deprecated** | Soon-to-be removed features | Features marked for future removal |
| **Removed** | Removed features | Features that no longer exist |
| **Fixed** | Bug fixes | Corrections to existing functionality |
| **Security** | Security vulnerability fixes | Security-related changes |

### Category Guidelines

**Added**
- New user-facing features
- New API endpoints
- New configuration options
- New integrations

**Changed**
- Performance improvements
- UX/UI changes
- Default value changes
- Behavior modifications

**Deprecated**
- Features planned for removal
- APIs being replaced
- Include migration path when possible

**Removed**
- Breaking changes (removed functionality)
- Deleted APIs or features
- Always note what replaced it (if applicable)

**Fixed**
- Bug corrections
- Error handling improvements
- Edge case fixes

**Security**
- Vulnerability patches
- Security-related fixes
- Always include CVE if available

## Entry Writing Guidelines

### Use Imperative Mood

Start entries with imperative verbs:

| Do | Don't |
|----|-------|
| Add support for... | Added support for... |
| Fix crash when... | Fixed a crash that occurred when... |
| Remove deprecated... | Removed the deprecated... |
| Change default to... | Changed the default to... |

### Focus on User Impact

Write from the user's perspective:

| Good (User-focused) | Bad (Implementation-focused) |
|---------------------|------------------------------|
| Add dark mode toggle | Implement ThemeProvider context |
| Fix login failing silently | Add try-catch to auth handler |
| Speed up page load by 40% | Optimize database queries |

### Be Specific and Concise

| Good (Specific) | Bad (Vague) |
|-----------------|-------------|
| Fix crash when uploading files over 10MB | Fix upload bug |
| Add CSV export for transaction history | Add export feature |
| Change session timeout from 30 to 60 minutes | Update session settings |

### Include Context When Helpful

Use parenthetical context for clarity:

```markdown
- Add OAuth2 support (Google, GitHub)
- Fix timezone handling (UTC offset calculation)
- Change rate limit (100 → 500 requests/minute)
```

## Changelog Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- New entries go here

## [1.0.0] - 2024-01-15

### Added
- Initial public release
- Feature A with description
- Feature B with description

### Changed
- Improvement to existing feature

### Fixed
- Bug fix description

## [0.9.0] - 2024-01-01

### Added
- Beta release features

[Unreleased]: https://github.com/owner/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/owner/repo/compare/v0.9.0...v1.0.0
[0.9.0]: https://github.com/owner/repo/releases/tag/v0.9.0
```

## Semantic Versioning Connection

Changelog categories map to version bumps:

| Category | Version Impact |
|----------|----------------|
| Removed (after v1.0) | MAJOR bump |
| Removed (before v1.0) | MINOR bump |
| Added, Changed | MINOR bump |
| Deprecated, Fixed, Security | PATCH bump |

## What NOT to Include

- Internal refactoring (unless it affects users)
- Dependency updates (unless they affect functionality)
- Test changes
- CI/CD changes
- Documentation-only changes (unless user-facing docs)
- Code style/formatting changes

## Reference Files

- `references/entry-examples.md` - Examples of well-written vs poorly-written entries
