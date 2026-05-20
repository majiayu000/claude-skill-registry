---
name: shared-tdd
description: TDD policy — red-green-refactor workflow and evidence requirements for all platforms.
---

## Purpose

Mandate test-driven development across all platforms. Platform coding standards reference this for the TDD workflow, then add platform-specific test tooling and conventions.

## TDD workflow (mandatory)

For any new behavior or bug fix:

1. **Red** — Write failing test(s) first
   - Derive test cases from acceptance criteria
   - Run tests to confirm failure
   - Do NOT write implementation code yet

2. **Green** — Write minimum code to pass
   - No feature creep beyond test requirements
   - Run tests after each change

3. **Refactor** — Clean up while tests stay green
   - Improve code quality without changing behavior

## Bug fixes

Bug fixes require a failing test that reproduces the issue *before* the fix is written.

## Completion gate

Stories cannot be marked complete without test files. Test files must exist before marking a story done.

## TDD evidence

When implementing features, document in commit or PR:
- Which tests were written first
- Confirmation that tests failed before implementation
