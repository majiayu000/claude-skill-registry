---
name: php-modernization
description: "Agent Skill: PHP 8.x modernization patterns. Use when upgrading to PHP 8.1/8.2/8.3/8.4/8.5, implementing type safety, or achieving PHPStan level 10. By Netresearch."
---

# PHP Modernization Skill

Modernize PHP applications to PHP 8.x with type safety, PSR compliance, and static analysis.

## Expertise Areas

- **PHP 8.x**: Constructor promotion, readonly, enums, match, attributes, union types
- **PSR/PER Compliance**: Active PHP-FIG standards
- **Static Analysis**: PHPStan (level 9+), PHPat, Rector, PHP-CS-Fixer
- **Type Safety**: DTOs/VOs over arrays, generics via PHPDoc

## Using Reference Documentation

### PHP Version Features

When implementing PHP 8.0-8.5 features (constructor promotion, readonly properties, enums, match expressions, attributes), consult `references/php8-features.md`.

### Standards Compliance

When ensuring PSR/PER compliance or configuring PHP-CS-Fixer with `@PER-CS`, consult `references/psr-per-compliance.md` for active PHP-FIG standards.

When configuring PHPStan levels or understanding level requirements, consult `references/phpstan-compliance.md` for level overview and production configuration.

### Static Analysis Tools

When setting up PHPStan, PHPat, Rector, or PHP-CS-Fixer, consult `references/static-analysis-tools.md` for configuration examples and integration patterns.

### Type Safety

When implementing type-safe code or migrating from arrays to DTOs, consult `references/type-safety.md` for type system strategies and best practices.

When creating request DTOs or handling safe integer conversion, consult `references/request-dtos.md` for DTO patterns and validation approaches.

### Architecture Patterns

When implementing adapter registry patterns for multiple external services, consult `references/adapter-registry-pattern.md` for dynamic adapter instantiation from database configuration.

When using Symfony DI, events, or modern framework patterns, consult `references/symfony-patterns.md` for architecture best practices.

### Migration Planning

When planning PHP version upgrades or modernization projects, consult `references/migration-strategies.md` for assessment phases, compatibility checks, and migration workflows.

## Running Scripts

### Project Verification

To verify a PHP project meets modernization requirements:

```bash
scripts/verify-php-project.sh /path/to/project
```

This script checks:
- PHPStan level compliance
- PHP-CS-Fixer configuration
- Type declaration coverage
- DTO usage patterns

## Required Tools

When setting up a modernized PHP project, ensure these tools are configured:

| Tool | Requirement |
|------|-------------|
| PHPStan | **Level 9 minimum**, level 10 recommended |
| PHPat | Required for defined architectures |
| Rector | Required for automated modernization |
| PHP-CS-Fixer | Required with `@PER-CS` ruleset |

## Core Rules

### DTOs Required

When passing structured data, always use DTOs instead of arrays:

```php
// Bad: public function createUser(array $data): array
// Good: public function createUser(CreateUserDTO $dto): UserDTO
```

### Enums Required

When defining fixed value sets, always use backed enums instead of constants:

```php
// Bad: const STATUS_DRAFT = 'draft'; function setStatus(string $s)
// Good: enum Status: string { case Draft = 'draft'; }
```

### PSR Interface Compliance

When type-hinting dependencies, use PSR interfaces (PSR-3, PSR-6, PSR-7, PSR-11, PSR-14, PSR-18).

## Migration Checklist

When modernizing a PHP project, verify these requirements:

- [ ] `declare(strict_types=1)` in all files
- [ ] PER Coding Style via PHP-CS-Fixer (`@PER-CS`)
- [ ] PHPStan level 9+ (level 10 for new projects)
- [ ] PHPat architecture tests
- [ ] Return types and parameter types on all methods
- [ ] DTOs for data transfer, no array params/returns
- [ ] Backed enums for all status/type values
- [ ] Type-hint against PSR interfaces

## Scoring Criteria

| Criterion | Requirement |
|-----------|-------------|
| PHPStan | Level 9 minimum |
| PHP-CS-Fixer | `@PER-CS` zero violations |
| DTOs/VOs | No array params/returns for structured data |
| Enums | Backed enums for fixed value sets |

---

> **Contributing:** https://github.com/netresearch/php-modernization-skill
