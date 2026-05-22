---
name: testing-process
description: Guidelines describing how to test the code. Use whenever writing new or updating existing code, for example after implementing a new feature or fixing a bug.
---

# Testing & Quality Assurance Process

## Guidelines

1. Always try to add tests for any new functionality, and make sure to cover all cases and code branches, according to requirements.
2. Always try to add tests for any bug-fixes, if the discovered bug is not already covered by tests. If the bug was already covered by tests, fix the existing tests as needed.
3. Always run all existing tests after you are done with a given implementation or bug-fix.

Use the following guidelines when working with tests:

- Ensure comprehensive testing
- Use table-/data-driven tests and test generation
- Benchmark tests and performance regression detection
- Integration testing with test containers
- Mock generation with %LANGUAGE% best practices and well-establised %LANGUAGE% mocking tools
- Property-based testing with %LANGUAGE% best practices and well-establised %LANGUAGE% testing tools
- Propose end-to-end testing strategies if automated e2e testing is not feasible
- Code coverage analysis and reporting
