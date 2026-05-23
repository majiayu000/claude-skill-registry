---
name: typo3-extension-upgrade
description: "Agent Skill: Systematic TYPO3 extension upgrades to newer LTS versions. Covers Extension Scanner, Rector, Fractor, PHPStan, and testing. Use when upgrading extensions to newer TYPO3 versions or fixing compatibility issues. By Netresearch."
---

# TYPO3 Extension Upgrade Skill

Systematic framework for upgrading TYPO3 extensions to newer LTS versions.

> **Scope**: Extension code upgrades only. NOT for TYPO3 project/core upgrades.

## Understand Your Situation First

Before running any automated tools, answer these questions:

### Current State
- **Current TYPO3 support**: What versions does `composer.json` currently support?
- **Current PHP requirement**: What `php` constraint is in `composer.json`?
- **Test status**: Do tests pass on the current version? (If not, fix first)
- **Known issues**: Any open bugs or technical debt?

### Target State
- **Target TYPO3 version(s)**: Which LTS version(s) will you support?
- **Target PHP version(s)**: What PHP versions must the extension run on?
- **Dropping support?**: Will you drop support for older TYPO3/PHP versions?

### Why Upgrade?
- **Business driver**: Client requirement? Security? End-of-life support?
- **Timeline**: Hard deadline or flexible?
- **Dependencies**: Do other extensions/projects depend on this one?

### Risk Assessment
Ask these questions:
- Does this extension have tests? (No tests = high risk)
- Does it use complex APIs (DBAL, Extbase, Fluid ViewHelpers)?
- Does it hook into TYPO3 internals (PSR-15, signals/slots)?
- How much custom JavaScript/CSS? (May need build system updates)

**If any answer raises concerns, document them before proceeding.**

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

## Understanding Rector/Fractor Output

**CRITICAL: Always run with `--dry-run` first and review the output before applying changes.**

### Reading Rector Dry-Run Output

```bash
./vendor/bin/rector process --dry-run
```

The output shows:
- **File path**: Which file will be modified
- **Rule name**: Which Rector rule triggered (e.g., `ExtbaseControllerActionsMustReturnResponseInterfaceRector`)
- **Diff**: Exact changes that will be made (red = removed, green = added)

**Before applying, check:**
1. Does the rule apply correctly to your code context?
2. Are there edge cases Rector might miss?
3. Will this break dual-version compatibility? (See `references/dual-compatibility.md`)

### Reading Fractor Dry-Run Output

```bash
./vendor/bin/fractor process --dry-run
```

Fractor modifies non-PHP files. Watch for:
- **TypoScript**: Removed/renamed options
- **FlexForms**: Changed XML structures
- **YAML configurations**: Service definitions, routes

### When NOT to Apply Automatically

Do NOT blindly apply Rector if:
- You need dual-version compatibility (v12 + v13)
- The extension has no tests to verify changes
- The diff shows changes you don't understand

Instead: Apply specific rules manually, test between each change.

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

## Troubleshooting

### Rector Broke My Code

If Rector applied changes that broke the extension:

**Immediate Recovery:**
```bash
# Option 1: Revert all Rector changes
git checkout -- .

# Option 2: Revert specific files
git diff --name-only | xargs git checkout --

# Option 3: If already committed
git revert HEAD
```

**Diagnose the Problem:**
1. Run Rector on a single file to isolate: `./vendor/bin/rector process path/to/file.php --dry-run`
2. Check which rule caused the issue (look at rule name in output)
3. Exclude problematic rules in `rector.php`:

```php
return static function (RectorConfig $rectorConfig): void {
    $rectorConfig->skip([
        // Skip a specific rule globally
        \Ssch\TYPO3Rector\Rector\v12\SomeProblematicRector::class,

        // Skip a rule for specific files
        \Ssch\TYPO3Rector\Rector\v12\SomeRector::class => [
            __DIR__ . '/Classes/Problematic.php',
        ],
    ]);
};
```

**Common Rector Failures:**
- **Extbase action return types**: May break if controller has custom response handling
- **Dependency injection**: May fail with complex factory patterns
- **Signal/slot to PSR-14**: Requires manual event class creation

### PHPStan Errors After Upgrade

If PHPStan reports many errors after Rector:

1. **Baseline approach**: Create a baseline for pre-existing issues:
   ```bash
   ./vendor/bin/phpstan analyse --generate-baseline
   ```

2. **Incremental fix**: Fix errors file by file, not all at once

3. **Common post-upgrade errors**:
   - Missing return types (add them manually)
   - Deprecated method calls Rector missed (check changelog)
   - Type mismatches from changed TYPO3 APIs

### Tests Fail After Upgrade

1. **Identify scope**: How many tests fail? All? Some?
2. **Check test framework**: Is `typo3/testing-framework` compatible with target TYPO3?
3. **Check test fixtures**: Do fixtures use deprecated APIs?
4. **Update test bootstrap**: May need new bootstrap for changed TYPO3 internals

### Extension Installs But Doesn't Work

If the extension installs without errors but functionality is broken:

1. **Check backend logs**: TYPO3 Admin Tools > Log
2. **Check PHP error log**: Often reveals missing classes/methods
3. **Clear all caches**: Admin Tools > Maintenance > Flush TYPO3 and PHP Caches
4. **Verify database**: Extension Manager may need to update database schema

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

An upgrade is complete when ALL of these are verified:

### Tool Verification
- [ ] `rector process --dry-run` shows no changes
- [ ] `fractor process --dry-run` shows no changes
- [ ] `phpstan analyse` passes without errors
- [ ] `php-cs-fixer fix --dry-run` shows no changes
- [ ] All unit tests pass
- [ ] All functional tests pass (if any)

### Real-World Testing (Required)

**Do NOT skip this step.** Automated tools cannot catch all issues.

1. **Create a fresh TYPO3 instance** matching target version:
   ```bash
   # Example with DDEV
   ddev config --project-type=typo3 --php-version=8.3
   ddev start
   ddev composer create typo3/cms-base-distribution:^13.4
   ```

2. **Install the upgraded extension** via Composer (from local path or packagist)

3. **Verify core functionality**:
   - [ ] Extension installs without errors
   - [ ] Backend module loads (if applicable)
   - [ ] Frontend plugin renders (if applicable)
   - [ ] All content elements work (if applicable)
   - [ ] Form finishers execute (if applicable)
   - [ ] Scheduled tasks run (if applicable)

4. **Check browser console** for JavaScript errors

5. **Test with real content** if possible (import from existing site)

### Documentation Updated
- [ ] `README.md` reflects new version requirements
- [ ] `CHANGELOG.md` documents the upgrade
- [ ] `composer.json` constraints are correct

## External Resources

When understanding Rector rules for TYPO3, consult the [TYPO3 Rector Documentation](https://github.com/sabbelasichon/typo3-rector).

When understanding Fractor for non-PHP files, consult the [Fractor Documentation](https://github.com/andreaswolf/fractor).

When checking TYPO3 deprecations, consult the [TYPO3 Core Changelog](https://docs.typo3.org/c/typo3/cms-core/main/en-us/).

---

> **Contributing:** https://github.com/netresearch/typo3-extension-upgrade-skill
