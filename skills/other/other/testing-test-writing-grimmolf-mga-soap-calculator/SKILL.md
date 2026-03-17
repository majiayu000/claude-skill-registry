---
name: Testing Test Writing
description: Follow TDD cycle (RED-GREEN-REFACTOR) writing failing tests first, covering edge cases and error states, using explicit fixtures, and maintaining fast test suites with coverage gates. Use this skill when writing unit tests, integration tests, contract tests, or any test code in test files. Applies to test directories, spec files, test runners (Jest, Vitest, pytest), mocking strategies, regression prevention, and ensuring statement/branch coverage thresholds that block merges when dropped.
---

# Testing Test Writing

## When to use this skill

- When creating test files like `*.test.ts`, `*.spec.js`, `test_*.py`, or working in `tests/`, `__tests__/`, `spec/` directories
- When practicing TDD by writing failing tests first (RED), implementing minimal code to pass (GREEN), then refactoring
- When covering edge cases, error states, validation failures, and boundary conditions in addition to happy paths
- When writing tests that express requirements and describe behavior rather than implementation details
- When using fixture factories or test builders to create explicit, maintainable test setups
- When adding integration tests or consumer-driven contract tests at module boundaries
- When mocking only true externals (network, filesystem, third-party APIs) and avoiding mocking internal code
- When keeping unit tests sub-second and integration tests parallelizable for fast feedback
- When adding regression tests for every discovered bug to prevent future recurrence
- When maintaining code coverage thresholds (statement/branch coverage) enforced by CI
- When writing test names that clearly describe the scenario being tested
- When configuring test runners like Jest, Vitest, pytest, or framework-specific testing tools
- When avoiding global test fixtures that hide magic and instead preferring explicit test setup

# Testing Test Writing

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle testing test writing.

## Instructions

For details, refer to the information provided in this file:
[testing test writing](../../../agent-os/standards/testing/test-writing.md)
