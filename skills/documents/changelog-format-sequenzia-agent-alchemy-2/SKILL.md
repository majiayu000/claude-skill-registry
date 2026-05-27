---
description: Keep a Changelog format guidelines and entry writing best practices. Use when writing changelog entries, updating CHANGELOG.md, or following Keep a Changelog specification.
user-invocable: false
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

## Entry Examples

OpenCode does not support a `references/` directory. The entry examples reference file has been inlined below.

### Added Category

#### Good Examples

```markdown
- Add user authentication with email/password and OAuth (Google, GitHub)
- Add bulk export of transactions to CSV and Excel formats
- Add keyboard shortcuts for common actions (Ctrl+S to save, Ctrl+Z to undo)
- Add dark mode with automatic system preference detection
- Add webhook support for order status changes
- Add rate limiting (100 requests/minute per API key)
```

#### Poor Examples (with corrections)

| Poor Entry | Why It's Poor | Better Version |
|------------|---------------|----------------|
| `Added new feature` | Too vague, no information | `Add invoice PDF generation` |
| `Implemented AuthService class` | Implementation detail, not user-facing | `Add user authentication` |
| `Added support for thing` | Unclear what "thing" is | `Add support for WebP image uploads` |
| `New button` | No context, incomplete | `Add "Export All" button to dashboard` |

---

### Changed Category

#### Good Examples

```markdown
- Improve search performance (3x faster for large datasets)
- Change default session timeout from 30 minutes to 2 hours
- Update password requirements: minimum 12 characters, 1 number required
- Redesign settings page with tabbed navigation
- Move API documentation to /docs endpoint
- Increase file upload limit from 5MB to 25MB
```

#### Poor Examples (with corrections)

| Poor Entry | Why It's Poor | Better Version |
|------------|---------------|----------------|
| `Refactored code` | Internal detail, no user impact | (Omit, or) `Improve page load speed by 40%` |
| `Updated dependencies` | Internal maintenance | (Omit unless user-facing change) |
| `Changed stuff` | Completely uninformative | `Change notification preferences to opt-in` |
| `Made improvements` | Too vague | `Improve error messages with specific guidance` |

---

### Fixed Category

#### Good Examples

```markdown
- Fix crash when uploading files larger than 10MB
- Fix incorrect tax calculation for international orders
- Fix login button not responding on mobile Safari
- Fix timezone display showing UTC instead of local time
- Fix memory leak causing slowdown after extended use
- Fix email notifications not sending for new comments
```

#### Poor Examples (with corrections)

| Poor Entry | Why It's Poor | Better Version |
|------------|---------------|----------------|
| `Fixed bug` | No description of what was fixed | `Fix duplicate orders created on retry` |
| `Bug fix` | Even less information | `Fix search returning stale results` |
| `Fixed issue #123` | Requires looking up issue | `Fix CSV export missing header row (#123)` |
| `Fixed null pointer exception in UserService.java:42` | Too technical | `Fix crash when viewing deleted user profile` |

---

### Removed Category

#### Good Examples

```markdown
- Remove deprecated /api/v1 endpoints (use /api/v2 instead)
- Remove support for Internet Explorer 11
- Remove "Classic" theme (migrate to "Modern" theme in settings)
- Remove automatic social media sharing (use manual share buttons)
- Remove legacy import format (use CSV import instead)
```

#### Poor Examples (with corrections)

| Poor Entry | Why It's Poor | Better Version |
|------------|---------------|----------------|
| `Removed old code` | What capability was lost? | `Remove legacy report generator` |
| `Deleted files` | Meaningless to users | (Omit if internal) |
| `Removed feature` | Which feature? | `Remove email digest option` |

---

### Deprecated Category

#### Good Examples

```markdown
- Deprecate /api/v1/users endpoint (use /api/v2/users, removal in v3.0)
- Deprecate XML export format (use JSON export, removal in 6 months)
- Deprecate "Classic" theme (will be removed in next major version)
- Deprecate basicAuth parameter (use apiKey authentication instead)
```

#### Poor Examples (with corrections)

| Poor Entry | Why It's Poor | Better Version |
|------------|---------------|----------------|
| `Deprecated old API` | No migration path | `Deprecate /legacy endpoint (use /api/v2, removal in v2.0)` |
| `Will remove soon` | No timeline or alternative | `Deprecate CSV import (use Excel import, removal March 2024)` |

---

### Security Category

#### Good Examples

```markdown
- Fix XSS vulnerability in comment rendering (CVE-2024-1234)
- Fix SQL injection in search query parameter
- Add Content-Security-Policy headers
- Update authentication to prevent session fixation attacks
- Fix CSRF vulnerability in account settings form
- Upgrade TLS minimum version to 1.2
```

#### Poor Examples (with corrections)

| Poor Entry | Why It's Poor | Better Version |
|------------|---------------|----------------|
| `Security fix` | No information about what was fixed | `Fix authentication bypass vulnerability` |
| `Fixed vulnerability` | Too vague | `Fix stored XSS in user profile bio field` |
| `Updated security` | Meaningless | `Add rate limiting to prevent brute force attacks` |

---

### Grouping Related Changes

When multiple related changes are made, group them thoughtfully:

#### Good Grouping

```markdown
### Added
- Add user profile customization
  - Profile picture upload
  - Bio and social links
  - Custom theme colors
- Add team collaboration features
  - Shared workspaces
  - Real-time presence indicators
  - Comment threads on items
```

#### Alternative: Separate Entries

```markdown
### Added
- Add profile picture upload with crop and resize
- Add customizable bio and social media links
- Add shared team workspaces
- Add real-time presence indicators for team members
```

---

### Entries with Technical Context

When technical details help users, include them appropriately:

#### Good Examples

```markdown
- Add GraphQL API alongside existing REST API
- Add WebSocket support for real-time updates (replaces polling)
- Fix N+1 query issue causing slow dashboard load
- Change database connection pooling (improves concurrent user handling)
```

#### Avoid Over-Technical Entries

| Too Technical | User-Friendly Version |
|---------------|----------------------|
| `Migrate from Redux to Zustand` | `Improve app responsiveness` (or omit) |
| `Refactor to use React hooks` | (Omit - internal change) |
| `Upgrade PostgreSQL 14 → 16` | (Omit unless user-facing) |
| `Add index on users.email column` | `Improve login speed` |

---

### Breaking Changes

Clearly indicate breaking changes:

```markdown
### Removed
- **BREAKING**: Remove support for Node.js 14 (minimum now Node.js 18)
- **BREAKING**: Remove /api/v1 endpoints (migrate to /api/v2)

### Changed
- **BREAKING**: Change config file format from YAML to TOML
- **BREAKING**: Rename `user.name` field to `user.displayName` in API responses
```
