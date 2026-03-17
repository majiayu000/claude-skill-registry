---
name: dev
description: Development workflows for WordPress ActivityPub plugin including wp-env setup, testing commands, linting, and build processes. Use when setting up development environment, running tests, checking code quality, building assets, or working with wp-env.
---

# ActivityPub Development Cycle

Quick reference for common development workflows in the WordPress ActivityPub plugin.

## Quick Reference

### Environment Management
```bash
npm run env-start    # Start WordPress at http://localhost:8888.
npm run env-stop     # Stop WordPress environment.
```

### Testing Commands
```bash
npm run env-test                      # Run all PHP tests.
npm run env-test -- --filter=pattern  # Run tests matching pattern.
npm run env-test -- path/to/test.php  # Run specific test file.
npm run env-test -- --group=name      # Run tests with @group annotation.
npm run test:e2e                      # Run Playwright E2E tests.
npm run test:e2e:debug                # Debug E2E tests.
```

### Code Quality
```bash
composer lint         # Check PHP coding standards.
composer lint:fix     # Auto-fix PHP issues.
npm run lint:js       # Check JavaScript.
npm run lint:css      # Check CSS styles.
npm run format        # Format all code (wp-scripts).
```

### Building Assets
```bash
npm run build         # Build for production (formatted and minified).
npm run dev           # Start development watch mode.
```

### Code Coverage
```bash
npm run env-start -- --xdebug=coverage    # Start with coverage support.
npm run env-test -- --coverage-text       # Generate text coverage report.
npm run env-test -- --coverage-html ./coverage  # Generate HTML report.
```

## Comprehensive Documentation

See [Development Environment Setup](../../../docs/development-environment.md) for detailed setup instructions.

See [Testing Reference](../../../tests/README.md) for comprehensive testing guidance.

See [Code Linting](../../../docs/code-linting.md) for linting configuration and standards.

## Pre-commit Hooks

The repository uses automated pre-commit hooks (`.githooks/pre-commit`) that run automatically on `git commit`:

1. **Sort PHP imports** - Automatically organizes use statements.
2. **Check unused imports** - Prevents unused use statements.
3. **Validate test patterns** - Blocks `remove_all_filters('pre_http_request')`.
4. **Run PHPCS auto-fix** - Applies coding standards automatically.
5. **Format JavaScript** - Runs wp-scripts formatter.

**IMPORTANT:** Hooks modify staged files automatically. Always review changes before committing. If hooks make changes, you'll need to stage them and commit again.

**Setup:** Hooks are installed by `npm run prepare` (runs automatically after `npm install`).

## Common Development Workflows

### Initial Setup
```bash
git clone git@github.com:Automattic/wordpress-activitypub.git
cd wordpress-activitypub
npm install           # Also runs 'npm run prepare' to install hooks.
composer install
npm run env-start     # WordPress at http://localhost:8888.
```

### Making Changes Workflow
```bash
# 1. Make code changes.

# 2. Run relevant tests.
npm run env-test -- --filter=FeatureName

# 3. Check code quality (optional - pre-commit hook does this).
composer lint
npm run lint:js

# 4. Commit (pre-commit hook runs automatically).
git add .
git commit -m "Description"
# Hook may modify files - review and stage again if needed.
```

### Before Creating PR
```bash
# Run full test suite.
npm run env-test

# Build assets.
npm run build

# Final lint check.
composer lint
npm run lint:js
```

### Debugging Failing Tests
```bash
# Run with verbose output.
npm run env-test -- --verbose --filter=test_name

# Run single test file to isolate issue.
npm run env-test -- tests/phpunit/tests/path/to/test.php

# Check test groups.
npm run env-test -- --list-groups
npm run env-test -- --group=specific_group
```

### Fresh Environment
```bash
npm run env-stop
npm run env-start
# wp-env automatically sets up WordPress with debug mode and test users.
```

## Key Files

- `package.json` - npm scripts and dependencies.
- `composer.json` - PHP dependencies and lint scripts.
- `.wp-env.json` - wp-env configuration.
- `phpcs.xml` - PHP coding standards (custom WordPress rules).
- `.githooks/pre-commit` - Pre-commit automation.
