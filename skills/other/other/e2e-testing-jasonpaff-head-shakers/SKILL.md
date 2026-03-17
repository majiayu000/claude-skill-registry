---
name: e2e-testing
description: Enforces project E2E testing conventions using Playwright with custom fixtures, Page Object Model, and authentication contexts.
---

# E2E Testing Skill

## Purpose

This skill provides end-to-end testing conventions using Playwright. E2E tests validate complete user flows with browser automation.

## Activation

This skill activates when:

- Creating or modifying files in `tests/e2e/specs/`
- Testing complete user flows
- Working with Playwright
- Creating or modifying Page Object Model classes
- Working with authentication contexts

## File Patterns

- `tests/e2e/specs/**/*.spec.ts`
- `tests/e2e/pages/**/*.page.ts`

## Workflow

1. Detect E2E test work (file path contains `tests/e2e/`)
2. Load `references/E2E-Testing-Conventions.md`
3. Also load `testing-base` skill for shared conventions
4. Apply Playwright patterns with custom fixtures
5. Use Page Object Model for reusable interactions

## Key Patterns (REQUIRED)

### Custom Fixtures

- Use fixtures from `tests/e2e/fixtures/base.fixture.ts`
- Available: `adminPage`, `userPage`, `newUserPage` (authenticated contexts)
- Available: `adminFinder`, `userFinder`, `newUserFinder` (ComponentFinder instances)

### Page Object Model

- Extend `BasePage` class for page objects
- Define `url` property for navigation
- Use `byTestId` helper for data-testid lookups

### ComponentFinder

- Use for standardized `data-testid` lookups
- Methods: `feature()`, `form()`, `ui()`, `layout()`, `tableCell()`

### Test Organization

- Place in appropriate `tests/e2e/specs/{category}/` folder
- Categories: smoke, public, user, admin, onboarding

## References

- `references/E2E-Testing-Conventions.md` - Complete E2E testing conventions
