---
name: testing
description: TDD/BDD testing principles. Use when writing tests, reviewing test coverage, setting up testing, or discussing test strategy and test architecture.
triggers:
  files: ["**/tests/**", "**/test/**", "**/__tests__/**", "**/spec/**", "*.test.*", "*.spec.*", "*Test*.*", "*_test.*"]
  keywords: ["test", "coverage", "TDD", "BDD", "mock", "assert", "unit test", "integration test", "e2e", "end-to-end", "fixture", "factory", "arrange act assert", "given when then", "red green refactor", "test pyramid"]
auto_suggest: true
---

# Testing - TDD/BDD Principles

This skill provides universal guidelines and best practices for testing across all technology stacks.

See @REFERENCE.md for detailed documentation.

## Quick Reference

- **TDD Cycle**: RED → GREEN → REFACTOR
- **Coverage Target**: >= 80%
- **Pyramid**: Unit (70%) > Integration (20%) > E2E (10%)
- **Pattern**: Arrange-Act-Assert (AAA)
- **Naming**: Descriptive test names that explain behavior
