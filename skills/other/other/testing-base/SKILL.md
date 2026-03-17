---
name: testing-base
description: Enforces project shared testing conventions for test structure, file naming, description patterns, assertions, and anti-patterns. This base skill is loaded by all test-type specialists.
---

# Testing Base Skill

## Purpose

This skill provides shared testing conventions used across all test types (unit, component, integration, E2E). It establishes consistent patterns for test structure, file organization, naming conventions, and common anti-patterns to avoid.

## Activation

This skill activates when:

- Creating or modifying any test file (`.test.ts`, `.test.tsx`, `.spec.ts`)
- Working with test setup files in `tests/setup/`
- Implementing test factories or mock handlers

## Workflow

1. Detect testing work (file path contains `tests/` or matches test file patterns)
2. Load `references/Testing-Base-Conventions.md`
3. Apply shared conventions to all test code
4. Validate against common anti-patterns
5. Report any violations found

## Key Patterns (REQUIRED)

### Test Structure

- Follow the project's test directory organization
- Use correct file naming patterns for each test type
- Keep test files close to their corresponding source files in the test hierarchy

### Description Conventions

- Use `describe`/`it` blocks with clear, behavior-focused descriptions
- Organize tests: positive cases first, edge cases, then error cases
- Use globals (no imports needed for `describe`/`it`/`expect`/`vi`)

### Assertion Patterns

- Use semantic assertions (`toBeInTheDocument`, `toHaveLength`, etc.)
- Prefer specific matchers over generic `toBe(true)`
- Use `async/await` properly with async assertions

### Anti-Patterns to Avoid

- Never test implementation details
- Never use `test.only` in committed code
- Never skip test cleanup
- Never use arbitrary timeouts
- Never hardcode test data (use factories)
- Never test multiple behaviors in one test

## References

- `references/Testing-Base-Conventions.md` - Complete shared testing conventions
