---
name: tunit
description: Run TUnit tests with Playwright. Use when user asks to run tests, execute tests, or check if tests pass.
---

# Running TUnit Tests

This project uses TUnit with Playwright for testing. Tests are located in `tests/SummitUI.Tests.Playwright/`.

## Run All Tests

```bash
dotnet run --project tests/SummitUI.Tests.Playwright
```

## Run Tests with Limited Parallelism (Recommended)

To prevent system overload when running Playwright tests, limit parallel test execution:

```bash
# Run with maximum 1 parallel test (sequential)
dotnet run --project tests/SummitUI.Tests.Playwright -- --maximum-parallel-tests 1

# Run with maximum 8 parallel tests
dotnet run --project tests/SummitUI.Tests.Playwright -- --maximum-parallel-tests 8
```
## Run Tests with Filters

TUnit uses `--treenode-filter` with path pattern: `/assembly/namespace/class/test`

Filter by class name:
```bash
dotnet run --project SummitUI.Tests.Playwright -- --treenode-filter '/*/*/ClassName/*'
```

Filter by exact test name:
```bash
dotnet run --project SummitUI.Tests.Playwright -- --treenode-filter '/*/*/*/TestName'
```

Examples:
```bash
# Run all Select accessibility tests
dotnet run --project tests/SummitUI.Tests.Playwright -- --treenode-filter '/*/*/SelectAccessibilityTests/*'

# Run specific test by name
dotnet run --project tests/SummitUI.Tests.Playwright -- --treenode-filter '/*/*/*/Trigger_ShouldHave_RoleCombobox'

# Run tests matching pattern (wildcard in test name)
dotnet run --project tests/SummitUI.Tests.Playwright -- --treenode-filter '/*/*/*/Keyboard*'

# Run all tests in namespace
dotnet run --project tests/SummitUI.Tests.Playwright -- --treenode-filter '/*/SummitUI.Tests.Playwright/*/*'
```

## Run Tests in Debug Mode

When a debugger is attached, Playwright will run in debug mode (`PWDEBUG=1`) automatically via the `Hooks.cs` setup.

## View Test Output

Add `--report` flags for different output formats:
```bash
# Console output with details
dotnet run --project tests/SummitUI.Tests.Playwright -- --output-format console-detailed

# Generate TRX report
dotnet run --project tests/SummitUI.Tests.Playwright -- --report-trx
```

## Flakiness Mitigation

The test project includes several features to reduce flakiness:

1. **Automatic Retries**: Tests are automatically retried up to 2 times on failure (`[Retry(2)]` in GlobalSetup.cs)
2. **Fully Sequential Execution**: All tests run sequentially via `[assembly: NotInParallel]` in GlobalSetup.cs
3. **Server Readiness Check**: `Hooks.cs` waits for the Blazor server to be fully ready before tests start
4. **Extended Timeouts**: Configured via `tunit.json` for longer test and hook timeouts

## Project Structure

- `GlobalSetup.cs` - Assembly-level test configuration (retries, parallelism)
- `Hooks.cs` - Test session setup/teardown (starts Blazor server)
- `BlazorWebApplicationFactory.cs` - WebApplicationFactory for hosting the test server
- `tunit.json` - TUnit configuration file
- `*AccessibilityTests.cs` - Accessibility test classes inheriting from `PageTest`

## Test Conventions

- Tests inherit from `TUnit.Playwright.PageTest` to get `Page` access
- Use `[Before(Test)]` for per-test setup
- Use `[Before(TestSession)]` / `[After(TestSession)]` for session-wide setup
- Access the running server via `Hooks.ServerUrl`
