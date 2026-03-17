---
name: test__integration_suite
description: Run the full suite of integration tests for the BookStore application. Use this to verify system-wide behavior.
---

To verify the application's end-to-end functionality using the Aspire AppHost tests:

1. **Navigate** to the test project:
   ```bash
   cd tests/BookStore.AppHost.Tests
   ```

// turbo
2. **Run Integration Tests**
   Run `dotnet test` to execute the full integration suite.

3. **Analyze Results**
   - **Pass**: Confirm to the user that all integration scenarios are working.
   - **Fail**: Look at the failed test names and stack traces.
     - Use `read_file` to read the failing test source code.
     - Check the test logs (often captured in `TestResults` or standard output) for specific error details like assertion failures or timeouts.

## Related Skills

**Used By**:
- `/test__verify_feature` - Runs all tests including integration tests
- `/test__integration_scaffold` - Creates integration tests that this skill runs

**Related**:
- `/test__unit_suite` - Run unit tests only
- `/test__verify_feature` - Complete verification workflow

**See Also**:
- [integration-testing-guide](../../../docs/guides/integration-testing-guide.md) - Aspire testing details
- [scaffold-test](../test__integration_scaffold/SKILL.md) - Creating integration tests
- AppHost.Tests AGENTS.md - Integration test patterns
