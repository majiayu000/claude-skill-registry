---
name: typo3-extension-upgrade
description: "Agent Skill: Systematic TYPO3 extension upgrades to newer LTS versions. Covers Extension Scanner, Rector, Fractor, PHPStan, and testing. Use when upgrading extensions to newer TYPO3 versions or fixing compatibility issues. By Netresearch."
---

# TYPO3 Extension Upgrade Skill

Systematic framework for upgrading TYPO3 extensions to newer LTS versions.

> **Scope**: Extension code upgrades only. NOT for TYPO3 project/core upgrades.

## Upgrade Toolkit

| Tool | Purpose | Files |
|------|---------|-------|
| Extension Scanner | Diagnose deprecated APIs | TYPO3 Backend |
| Rector | Automated PHP migrations | `.php` |
| Fractor | Non-PHP migrations | FlexForms, TypoScript, YAML, Fluid |
| PHPStan | Static analysis | `.php` |

## Core Workflow

To upgrade a TYPO3 extension, follow these steps:

1. Complete the planning phase (consult `references/pre-upgrade.md`)
2. Create feature branch (verify git is clean)
3. Update `composer.json` constraints for target version
4. Run `rector process --dry-run` → review → apply
5. Run `fractor process --dry-run` → review → apply
6. Run `php-cs-fixer fix`
7. Run `phpstan analyse` → fix errors
8. Run `phpunit` → fix tests
9. Test in target TYPO3 version(s)

## Using Reference Documentation

### Planning and Preparation

When starting an upgrade project, consult `references/pre-upgrade.md` for the planning checklist, including version audit, file inventory, and scope documentation.

When checking API changes for specific versions, consult `references/api-changes.md` for deprecated and removed APIs by TYPO3 version.

### Version-Specific Guides

When upgrading from TYPO3 v11 to v12, consult `references/upgrade-v11-to-v12.md` for version constraints, Rector configuration, and v12-specific changes.

When upgrading from TYPO3 v12 to v13, consult `references/upgrade-v12-to-v13.md` for version constraints, Rector configuration, and v13-specific changes.

When maintaining dual compatibility (v12 + v13), consult `references/dual-compatibility.md` for Rector configuration warnings and compatibility patterns.

### Patterns and Examples

When looking for real-world migration examples, consult `references/real-world-patterns.md` for common upgrade scenarios and solutions.

## Using Asset Templates

### Rector Configuration

To configure Rector for automated PHP migrations, copy `assets/rector.php` and adjust the target TYPO3/PHP version sets.

### Fractor Configuration

To configure Fractor for non-PHP migrations (FlexForms, TypoScript, YAML), copy `assets/fractor.php` and customize for your extension.

### PHPStan Configuration

To configure PHPStan for static analysis, copy `assets/phpstan.neon` and adjust paths and rules for your extension.

### PHPUnit Configuration

To configure PHPUnit for testing, copy `assets/phpunit.xml` and adjust test paths and bootstrap settings.

### PHP-CS-Fixer Configuration

To configure PHP-CS-Fixer for code style, copy `assets/.php-cs-fixer.php` and customize rules as needed.

## Quick Commands

To run the complete upgrade toolchain:

```bash
# Rector: automated PHP migrations
./vendor/bin/rector process --dry-run && ./vendor/bin/rector process

# Fractor: non-PHP migrations
./vendor/bin/fractor process --dry-run && ./vendor/bin/fractor process

# Quality checks
./vendor/bin/php-cs-fixer fix && ./vendor/bin/phpstan analyse && ./vendor/bin/phpunit
```

## Planning Phase (Required)

When performing major upgrades (PHP version drops, TYPO3 major versions), complete these steps before any code changes:

1. **List all files with hardcoded versions** (composer.json, CI, Docker, Rector)
2. **Document scope** - how many places need changes?
3. **Present plan to user** for approval
4. **Track progress** with todo list

## TYPO3 Changelogs

When checking for breaking changes and deprecations:

| Version | Changelog |
|---------|-----------|
| v14 | [Changelog-14](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-14.html) |
| v13 | [Changelog-13](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-13.html) |
| v12 | [Changelog-12](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-12.html) |

## Success Criteria

An upgrade is complete when:

- `rector process --dry-run` shows no changes
- `fractor process --dry-run` shows no changes
- `phpstan analyse` passes without errors
- All tests pass
- Extension works in target TYPO3 version

## External Resources

When understanding Rector rules for TYPO3, consult the [TYPO3 Rector Documentation](https://github.com/sabbelasichon/typo3-rector).

When understanding Fractor for non-PHP files, consult the [Fractor Documentation](https://github.com/andreaswolf/fractor).

When checking TYPO3 deprecations, consult the [TYPO3 Core Changelog](https://docs.typo3.org/c/typo3/cms-core/main/en-us/).

---

> **Contributing:** https://github.com/netresearch/typo3-extension-upgrade-skill
