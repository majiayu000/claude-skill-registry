---
name: acc-changelog-template
description: Generates CHANGELOG.md files following Keep a Changelog format. Creates version history documentation.
---

# CHANGELOG Template Generator

Generate changelogs following the Keep a Changelog format.

## Standard Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Vulnerability fixes

## [1.0.0] - 2025-01-15

### Added
- Initial release

[Unreleased]: https://github.com/owner/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/owner/repo/releases/tag/v1.0.0
```

## Section Guidelines

### Added

New features and capabilities:

```markdown
### Added
- User authentication with JWT tokens
- Password reset via email
- Two-factor authentication support
- Rate limiting for API endpoints
- `UserService::createWithRole()` method
```

### Changed

Modifications to existing features:

```markdown
### Changed
- Improved error messages for validation failures
- Updated `Order::calculateTotal()` to include tax
- Refactored `PaymentService` for better testability
- Upgraded minimum PHP version from 8.4 to 8.5
```

### Deprecated

Features to be removed in future versions:

```markdown
### Deprecated
- `User::getFullName()` - use `User::name()` instead
- Legacy authentication endpoints (`/api/v1/auth/*`)
- `ArrayHelper` class - use native array functions
```

### Removed

Features that were removed:

```markdown
### Removed
- Support for PHP 8.2
- Deprecated `LegacyController` class
- Unused `debug` configuration option
- `api/v0/*` endpoints
```

### Fixed

Bug fixes:

```markdown
### Fixed
- Order total calculation rounding error (#123)
- Memory leak in long-running workers
- Race condition in concurrent order creation
- Null pointer exception when user has no address
```

### Security

Security-related changes:

```markdown
### Security
- Fixed SQL injection vulnerability in search (CVE-2025-1234)
- Updated dependencies with known vulnerabilities
- Added CSRF protection to all forms
- Implemented rate limiting to prevent brute force
```

## Version Entry Template

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Feature A with brief description
- Feature B with brief description

### Changed
- Change A with brief description

### Fixed
- Bug A with issue reference (#123)

### Security
- Security fix with CVE reference if applicable
```

## Complete Example

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GraphQL API support

## [2.1.0] - 2025-01-15

### Added
- Batch processing for bulk operations
- Webhook support for order events
- `OrderExporter` class for CSV/JSON export

### Changed
- Improved query performance for order listing
- Updated `Money` value object with better precision

### Fixed
- Pagination offset calculation (#234)
- Timezone handling in date filters

## [2.0.0] - 2025-01-01

### Added
- CQRS architecture with separate read/write models
- Event sourcing for order aggregate
- New `OrderProjection` for optimized queries

### Changed
- **BREAKING:** Renamed `OrderService` to `OrderCommandHandler`
- **BREAKING:** Changed `Order::create()` signature
- Minimum PHP version is now 8.5

### Removed
- **BREAKING:** Removed deprecated `LegacyOrderRepository`
- Support for MySQL 5.7

### Security
- Updated Symfony to 7.2 (security release)

## [1.2.1] - 2024-12-15

### Fixed
- Critical: Order duplication on timeout (#189)
- Email notification not sent for cancelled orders

## [1.2.0] - 2024-12-01

### Added
- Order cancellation workflow
- Email notifications for status changes
- Admin dashboard statistics

### Changed
- Improved order search with full-text indexing

## [1.1.0] - 2024-11-15

### Added
- Multi-currency support
- Tax calculation service
- Discount code feature

### Fixed
- Currency symbol display (#145)

## [1.0.0] - 2024-11-01

### Added
- Initial release
- Order creation and management
- Customer registration
- Basic reporting

[Unreleased]: https://github.com/vendor/package/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/vendor/package/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/vendor/package/compare/v1.2.1...v2.0.0
[1.2.1]: https://github.com/vendor/package/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/vendor/package/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/vendor/package/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/vendor/package/releases/tag/v1.0.0
```

## Semantic Versioning Guide

```
MAJOR.MINOR.PATCH

MAJOR - Breaking changes
MINOR - New features (backward compatible)
PATCH - Bug fixes (backward compatible)
```

### Version Decision Guide

| Change Type | Version Bump |
|-------------|--------------|
| Breaking API change | MAJOR |
| Remove feature | MAJOR |
| Change signature | MAJOR |
| Add new feature | MINOR |
| Add new method | MINOR |
| Deprecate feature | MINOR |
| Bug fix | PATCH |
| Performance improvement | PATCH |
| Documentation update | PATCH |

## Writing Guidelines

### Good Entry

```markdown
- Add `UserService::findByEmail()` method for user lookup (#123)
```

**Why it's good:**
- Starts with verb
- Specific about what changed
- References issue/PR

### Bad Entry

```markdown
- Fixed bug
```

**Why it's bad:**
- No specifics
- No reference
- Not helpful

### Entry Patterns

```markdown
# Pattern: Verb + What + Context

# Adding
- Add `ClassName::method()` for [purpose]
- Add support for [feature]
- Add [component] to handle [use case]

# Changing
- Change `method()` to return [type] instead of [type]
- Improve [feature] performance by [how]
- Update [component] to use [new approach]

# Fixing
- Fix [issue] when [condition] (#number)
- Fix [component] not [expected behavior]
- Fix memory leak in [component]

# Removing
- Remove deprecated `ClassName` class
- Remove support for [version/feature]
- Remove unused [component]

# Security
- Fix [vulnerability type] in [component] (CVE-XXXX-YYYY)
- Update [dependency] to patch [vulnerability]
```

## Generation Instructions

When generating CHANGELOG entries:

1. **Categorize changes** into correct sections
2. **Start with verb** (Add, Change, Fix, Remove)
3. **Be specific** about what changed
4. **Reference issues/PRs** when available
5. **Mark breaking changes** clearly
6. **Include migration notes** for breaking changes
7. **Update version links** at bottom
8. **Date format** YYYY-MM-DD
