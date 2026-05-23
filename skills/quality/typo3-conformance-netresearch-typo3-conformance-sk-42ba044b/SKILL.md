---
name: typo3-conformance
description: "Agent Skill: Evaluate TYPO3 extensions for conformance to v12/v13/v14 standards. Use when assessing quality, generating reports, or planning modernization. By Netresearch."
file_triggers:
  - "ext_emconf.php"
  - "ext_localconf.php"
  - "**/Configuration/TCA/**/*"
  - "**/*.typoscript"
---

# TYPO3 Extension Conformance Checker

Evaluate TYPO3 extensions for standards compliance, architecture patterns, and best practices.

## Skill Delegation

When testing implementation details are needed, delegate to the `typo3-testing` skill.
When documentation validation is needed, delegate to the `typo3-docs` skill.

## Evaluation Workflow

To evaluate an extension, follow these steps in order:

1. **Initial Assessment** - Identify extension key, target TYPO3 version, and extension type
2. **File Structure** - Validate composer.json, ext_emconf.php, and required directories
3. **Coding Standards** - Check strict_types, type declarations, and PSR-12 compliance
4. **Prohibited Patterns** - Verify no `$GLOBALS` access, no `GeneralUtility::makeInstance()` for services
5. **PHP Architecture** - Validate constructor DI, Services.yaml, PSR-14 events, TcaSchemaFactory
6. **Backend Modules** - Check ES6 modules, Modal API, CSRF protection (v13+)
7. **Testing** - Verify PHPUnit setup, Playwright E2E, and coverage >70%
8. **Best Practices** - Confirm DDEV setup, runTests.sh, quality tools, and CI/CD
9. **TER Publishing** - Validate workflow, upload comment format, CI TER compatibility check

## Scoring System

**Base Score (0-100):**
- Architecture: 20 points
- Guidelines: 20 points
- PHP Patterns: 20 points
- Testing: 20 points
- Best Practices: 20 points

**Excellence Bonus (0-22):** Additional points for exceptional quality features.

## Running Conformance Checks

To run a complete conformance check on an extension:

```bash
scripts/check-conformance.sh /path/to/extension
```

To run individual checks:

```bash
# File structure validation
scripts/check-file-structure.sh /path/to/extension

# Coding standards validation
scripts/check-coding-standards.sh /path/to/extension

# PHP architecture validation
scripts/check-architecture.sh /path/to/extension

# Testing infrastructure validation
scripts/check-testing.sh /path/to/extension

# PHPStan baseline regression check
scripts/check-phpstan-baseline.sh /path/to/extension

# Generate final report
scripts/generate-report.sh /path/to/extension
```

## Using Reference Documentation

### Core Standards

When validating extension architecture, consult `references/extension-architecture.md` for directory structure, file hierarchy, and required files.

When checking coding standards, consult `references/coding-guidelines.md` for PSR-12 compliance, naming conventions, and TYPO3-specific style rules.

When validating PHP patterns, consult `references/php-architecture.md` for dependency injection, services, events, Extbase, and middleware patterns.

When checking testing infrastructure, consult `references/testing-standards.md` for PHPUnit and Playwright requirements. Delegate to `typo3-testing` skill for implementation details.

### File Validation

When validating composer.json, consult `references/composer-validation.md` for complete validation rules and required fields.

When validating ext_emconf.php, consult `references/ext-emconf-validation.md` for TER requirements and field specifications.

When validating ext_localconf.php, ext_tables.php, or SQL files, consult `references/ext-files-validation.md` for proper patterns.

When checking directory organization, consult `references/directory-structure.md` for separation of committed vs generated files.

### Version Compatibility

When checking TYPO3/PHP version requirements, consult `references/version-requirements.md` for the definitive compatibility matrix.

When supporting multiple TYPO3 versions, consult `references/dual-version-compatibility.md` for v12+v13 compatibility patterns.

When migrating from deprecated APIs, consult `references/v13-deprecations.md` for modern alternatives and migration paths.

### Backend Development

When modernizing backend modules, consult `references/backend-module-v13.md` for ES6 modules, Modal API, and accessibility compliance.

When implementing setup wizards, consult `references/backend-wizard-patterns.md` for multi-step configuration wizard patterns.

When working with hooks or events, consult `references/hooks-and-events.md` for PSR-14 event patterns and migration strategies.

### Advanced Patterns

When implementing complex configuration, consult `references/multi-tier-configuration.md` for Provider → Model → Config architecture.

When evaluating best practices, consult `references/best-practices.md` for organizational patterns from the Tea extension.

When scoring excellence features, consult `references/excellence-indicators.md` for bonus criteria beyond basic conformance.

### Publishing & Integration

When preparing for TER publication, consult `references/ter-publishing.md` for requirements and best practices.

When setting up translation management, consult `references/crowdin-integration.md` for Crowdin integration validation.

When configuring development environments, consult `references/development-environment.md` for DDEV and tooling setup.

When validating runTests.sh, consult `references/runtests-validation.md` for Tea extension reference patterns.

### Reporting

When generating conformance reports, consult `references/report-template.md` for the standard report structure.

## Using Asset Templates

### PHP Quality Tools

To configure PHPStan, copy from `assets/Build/phpstan/`:
- `phpstan.neon` - Base PHPStan configuration
- `phpstan-baseline.neon` - Baseline template for legacy code

To configure PHP-CS-Fixer, copy `assets/Build/php-cs-fixer/php-cs-fixer.php` for TYPO3-compliant code style.

To configure Rector, copy `assets/Build/rector/rector.php` for automated refactoring rules.

To detect unused Composer dependencies, copy `assets/Build/composer-unused/composer-unused.php`.

### Frontend Quality Tools

To configure ESLint for JavaScript, copy `assets/Build/eslint/.eslintrc.json`.

To configure Stylelint for CSS, copy `assets/Build/stylelint/.stylelintrc.json`.

### TypoScript Validation

To configure TypoScript linting, copy `assets/Build/typoscript-lint/TypoScriptLint.yml`.

## External Resources

When understanding TYPO3 core standards, consult the [TYPO3 Core API Reference](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/).

When seeking reference implementations, study the [Tea Extension](https://github.com/TYPO3BestPractices/tea).

When checking TER requirements, consult the [TYPO3 Extension Repository](https://extensions.typo3.org/).

---

> **Contributing:** https://github.com/netresearch/typo3-conformance-skill
