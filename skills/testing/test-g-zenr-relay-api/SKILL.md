---
name: test
description: Write comprehensive tests for a module or feature (Priya Sharma's workflow)
---

Write tests for: $ARGUMENTS

Follow Priya Sharma's testing standards:

1. **Identify scope**: Read the source code being tested. Understand every public method, edge case, and error path.

2. **Choose test file**: Use the test file mapping in project config to find the corresponding test file for the module being tested.

3. **Write three-path tests** for every endpoint or method:
   - **Success path**: Valid input → expected output, verify response body not just status code
   - **Validation error path**: Invalid input → 422 or the not-found exception
   - **Service/device error path**: External resource unavailable → 503 or the connection error exception

4. **Test conventions**:
   - Class names: `Test<Feature>`
   - Method names: `test_<action>_<expected_outcome>`
   - Use proper type hints on test fixtures
   - Configure test HTTP client for proper error testing (no automatic error propagation)
   - DI overrides (see stack concepts) with cleanup in teardown
   - Audit log assertions via log capture mechanism (see stack concepts) at the correct logger level (see project config for logger name)
   - No `time.sleep()`, no shared mutable state, no execution order dependence

5. **Edge cases to always consider**:
   - Below minimum identifier values
   - Above maximum identifier values
   - Invalid state values
   - External resource disconnected mid-operation
   - Concurrent access patterns
   - Empty/null request bodies

6. **Verify**: Run the test command (see project config) — all tests must pass