---
name: testing-strategies
description: Provides test design patterns, coverage strategies, and best practices for comprehensive test suite development
version: 1.0.0
---

## Overview

This skill provides strategies for test design, test coverage, test organization, and testing best practices across different testing types and frameworks.

## Test Coverage Targets

- **Critical Code** (auth, payment, security): 100%
- **Business Logic**: 90-100%
- **Utilities**: 80-90%
- **UI Components**: 70-80%
- **Overall Project**: 80%+

## Test Types

### Unit Tests
- Test individual functions/methods in isolation
- Use mocks for dependencies
- Fast execution (<1ms per test)
- Cover happy path, edge cases, errors

### Integration Tests
- Test component interactions
- Use real dependencies where reasonable
- Test API endpoints, database operations
- Moderate execution time

### End-to-End Tests
- Test complete user workflows
- Use real system components
- Critical paths only (slower execution)

## Test Case Pattern

For each function, create tests for:
1. **Happy Path**: Normal, expected inputs
2. **Edge Cases**: Boundary values, empty inputs
3. **Error Cases**: Invalid inputs, exceptions
4. **Special Cases**: Nulls, zeros, large values

## Test Organization

```
tests/
├── unit/
│   ├── test_module1.py
│   └── test_module2.py
├── integration/
│   └── test_api.py
└── e2e/
    └── test_workflows.py
```

## When to Apply

Use when creating test suites, improving coverage, fixing failing tests, or designing test strategies.
