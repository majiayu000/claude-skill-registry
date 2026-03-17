---
name: unit-testing
description: Enforces project unit testing conventions for pure functions, validation schemas, and utility modules using Vitest with proper isolation and mocking.
---

# Unit Testing Skill

## Purpose

This skill provides unit testing conventions for isolated tests of pure functions, Zod validation schemas, and utility modules. Unit tests run without database or external service dependencies.

## Activation

This skill activates when:

- Creating or modifying files in `tests/unit/`
- Testing Zod validation schemas
- Testing pure utility functions
- Testing data transformers or formatters

## File Patterns

- `tests/unit/**/*.test.ts`

## Workflow

1. Detect unit test work (file path contains `tests/unit/`)
2. Load `references/Unit-Testing-Conventions.md`
3. Also load `testing-base` skill for shared conventions
4. Apply unit test patterns with proper isolation
5. Validate no database or external service dependencies

## Key Patterns (REQUIRED)

### Test Structure

- Use `describe`/`it` blocks (no imports - globals enabled)
- Follow Arrange-Act-Assert pattern
- Test pure functions in isolation
- Mock ALL external dependencies with `vi.mock()`

### Validation Schema Testing

- Test valid input scenarios
- Test invalid input scenarios with specific error expectations
- Test edge cases (empty strings, null, undefined, boundary values)
- Use `safeParse` for validation testing

### Isolation Requirements

- NO database access in unit tests
- NO MSW handlers needed (no API calls)
- Mock external imports with `vi.mock()`
- Tests should run without any external services

## References

- `references/Unit-Testing-Conventions.md` - Complete unit testing conventions
