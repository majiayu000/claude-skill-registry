---
name: test-infrastructure
description: Enforces project test infrastructure conventions for factories, MSW handlers, mock data, Page Objects, and shared test utilities.
---

# Test Infrastructure Skill

## Purpose

This skill provides test infrastructure conventions for creating reusable testing foundations including factories, MSW handlers, mock data, and Page Object Model classes.

## Activation

This skill activates when:

- Creating or modifying files in `tests/fixtures/`
- Creating or modifying files in `tests/mocks/`
- Creating or modifying files in `tests/helpers/`
- Creating or modifying Page Objects in `tests/e2e/pages/`
- Creating or modifying E2E helpers in `tests/e2e/helpers/`

## File Patterns

- `tests/fixtures/**/*.factory.ts`
- `tests/mocks/**/*.handlers.ts`
- `tests/mocks/**/*.mock.ts`
- `tests/mocks/data/**/*.mock.ts`
- `tests/e2e/pages/**/*.page.ts`
- `tests/e2e/helpers/**/*.ts`
- `tests/helpers/**/*.ts`

## Workflow

1. Detect infrastructure work (file path matches patterns above)
2. Load `references/Test-Infrastructure-Conventions.md`
3. Also load `testing-base` skill for shared conventions
4. Apply infrastructure patterns for the specific type
5. Ensure consistent naming and export patterns

## Key Patterns (REQUIRED)

### Factories

- Async functions returning database entities
- Accept `overrides` parameter for customization
- Generate unique IDs using timestamps
- Export named factory functions

### MSW Handlers

- Use `http` from MSW for route handlers
- Return `HttpResponse.json()` for JSON responses
- Export handlers array for server setup

### Page Objects

- Extend `BasePage` class
- Define abstract `url` property
- Use `byTestId` helper for element location

### Mock Data

- Export typed mock objects
- Use realistic data patterns
- Include edge case variations

## References

- `references/Test-Infrastructure-Conventions.md` - Complete infrastructure conventions
