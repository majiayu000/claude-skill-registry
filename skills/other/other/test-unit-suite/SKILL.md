---
name: test__unit_suite
description: Run unit tests for the API Service and Analyzers. Use this to verify business logic, individual components, and code analyzers.
---

To verify the logic, endpoints, and custom analyzers of the API Service:

1. **Run Service Unit Tests**
   - Navigate to `tests/ApiService/BookStore.ApiService.UnitTests`.
   - Run: `dotnet test`
   - **Purpose**: Verifies handlers, validation, and domain logic.

2. **Run Analyzer Unit Tests**
   - Navigate to `tests/ApiService/BookStore.ApiService.Analyzers.UnitTests`.
   - Run: `dotnet test`
   - **Purpose**: Verifies custom Roslyn analyzers (e.g., UUIDv7 enforcement).

// turbo
3. **Both (shortcut)**
   - To run both test suites in one command:
     ```bash
     dotnet test tests/ApiService/BookStore.ApiService.UnitTests/BookStore.ApiService.UnitTests.csproj && \
     dotnet test tests/ApiService/BookStore.ApiService.Analyzers.UnitTests/BookStore.ApiService.Analyzers.UnitTests.csproj
     ```

4. **Analyze Results**
   - **Pass**: Core logic and static analysis rules are correct.
   - **Fail**:
     - Check the specific failing test and project.
     - Analyzer tests often fail if code samples in tests don't match expected diagnostics.

## Related Skills

**Used By**:
- `/test__verify_feature` - Runs all tests including these unit tests

**Related**:
- `/test__integration_suite` - Run full integration test suite
- `/test__verify_feature` - Complete verification (build + format + all tests)

**See Also**:
- [testing-guide](../../../docs/guides/testing-guide.md) - TUnit testing patterns
- ApiService.UnitTests AGENTS.md - Unit test patterns
- Analyzers.UnitTests AGENTS.md - Analyzer testing patterns
