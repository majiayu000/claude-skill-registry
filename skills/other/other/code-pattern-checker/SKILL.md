---
name: code-pattern-checker
description: "Use before committing code - validates Drupal coding standards, SOLID/DRY principles, security practices, and CSS standards. Trigger: 'check code quality', 'pre-commit check', 'lint Drupal code', 'validate standards'. Use proactively before ANY commit. Checks SOLID, DRY, security, and Drupal coding standards."
version: 2.1.0
---

# Code Pattern Checker

Validate code against Drupal standards and best practices.

## Required References

**Load these before checking code:**

| Reference | Checks |
|-----------|--------|
| `references/solid-drupal.md` | SOLID principles |
| `references/dry-patterns.md` | DRY patterns |
| `dev-guides: drupal/security/` | Security practices (online) |
| `dev-guides: drupal/sdc/ + drupal/js-development/` | CSS/JS/SDC standards (online) |
| `references/quality-gates.md` | Gate 1 requirements |

> For security and frontend checks, WebFetch from `https://camoa.github.io/dev-guides/` instead of reading bundled files.

## Activation

Activate when you detect:
- Before committing code
- After implementation, before task completion
- `/drupal-dev-framework:validate` command
- "Check my code" or "Review this"
- Invoked by `task-completer` skill

## Gate Enforcement

This skill enforces **Gate 1: Code Standards** from `references/quality-gates.md`.
Code CANNOT be committed until Gate 1 passes.

## Workflow

### 1. Identify Files to Check

Ask if not clear:
```
Which files should I check?
1. All changed files (git diff)
2. Specific file(s)
3. All files in a component

Your choice:
```

Use `Bash` with `git diff --name-only` to get changed files if option 1.

### 2. Read and Analyze Files

Use `Read` on each file. For each, check:

**PHP Files:**
- [ ] PSR-12 / Drupal coding standards
- [ ] Docblocks on classes and public methods
- [ ] Type hints on parameters and returns
- [ ] No deprecated functions
- [ ] Naming: PascalCase classes, camelCase methods

**SOLID Principles (references/solid-drupal.md):**
- [ ] Single Responsibility - one purpose per class
- [ ] Dependency Inversion - inject dependencies via services.yml
- [ ] No `\Drupal::service()` in new code (BLOCKING)
- [ ] Interfaces defined for services

**DRY Check (references/dry-patterns.md):**
- [ ] No duplicate code blocks (BLOCKING)
- [ ] Shared logic in services/traits
- [ ] Leverages Drupal base classes

**Security (dev-guides drupal/security/):**
- [ ] No raw SQL with user input (BLOCKING)
- [ ] Output escaped (Twig auto, Html::escape)
- [ ] Form tokens present (Form API handles)
- [ ] Access checks on routes (BLOCKING)
- [ ] Input validated via Form API

**CSS/SCSS (dev-guides drupal/sdc/ + drupal/js-development/):**
- [ ] Mobile-first media queries
- [ ] No `!important` (BLOCKING)
- [ ] No `@extend` (BLOCKING)
- [ ] BEM naming convention
- [ ] Drupal behaviors pattern for JS

### 3. Run Automated Tools

Suggest running (user executes):
```bash
# PHP CodeSniffer
ddev exec vendor/bin/phpcs --standard=Drupal,DrupalPractice {path}

# PHPStan (if configured)
ddev exec vendor/bin/phpstan analyze {path}

# SCSS Lint (if applicable)
npm run lint:scss
```

### 4. Report Findings

Format output as:
```
## Code Check: {file or component}

### Status: PASS / ISSUES FOUND

### Standards Check
| Check | Status | Notes |
|-------|--------|-------|
| PSR-12 | PASS | - |
| Docblocks | ISSUE | Missing on processData() |
| Type hints | PASS | - |

### SOLID Principles
| Principle | Status |
|-----------|--------|
| Single Responsibility | PASS |
| Dependency Inversion | PASS |

### Security
| Check | Status | Notes |
|-------|--------|-------|
| SQL Injection | PASS | Uses query builder |
| XSS | PASS | Output escaped |
| Access Control | ISSUE | Missing on /admin/custom route |

### DRY Check
| Issue | Location |
|-------|----------|
| Duplicate logic | lines 45-52 and 78-85 |

### Issues to Fix (Priority Order)
1. **Security**: Add access check to admin route
2. **Standards**: Add docblock to processData()
3. **DRY**: Extract duplicate logic to private method

### Recommendation
- [ ] Fix security issue before merge
- [ ] Other issues: fix now or create follow-up task

Approved for commit: NO (fix security first) / YES
```

### 5. Offer Fixes

For each issue, offer to help:
```
Issue: Missing docblock on processData()

Suggested fix:
/**
 * Process the input data and return results.
 *
 * @param array $data
 *   The input data array.
 *
 * @return array
 *   The processed results.
 */

Apply this fix? (yes/no/skip)
```

## Stop Points

STOP and wait for user:
- After asking which files to check
- After presenting findings
- Before applying each fix
- If security issues found (emphasize fixing)
