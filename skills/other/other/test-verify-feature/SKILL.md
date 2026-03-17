---
name: test__verify_feature
description: Strict verification for new features. Runs compilation, formatting, and all tests to ensure the "Definition of Done".
---

Use this skill to verify that a feature implementation is complete and correct. It enforces code style, compilation, and test passing.

## Verification Steps

1. **Compilation**
   - Run `dotnet build` in the root directory.
   - **Check**: If the build fails, STOP. Report the errors using `read_file` to show the relevant code.
   - **Tip**: For clean rebuild, use `/ops__rebuild_clean`

2. **Code Formatting**
   - Run `dotnet format --verify-no-changes`.
   - **Check**: If this fails, it means the code violates style rules.
   - *Action*: You can offer to fix it for the user by running `dotnet format` (without --verify-no-changes).

3. **Background Services Check**
   - Ensure you are not running tests if the AppHost is already locking ports (if running locally).
   - *Action*: Stop any running `dotnet` processes if needed.

// turbo
4. **Run Tests (Unit & Integration)**
   - Run `dotnet test` to execute all test suites.
   - **Check**: All tests must pass.
   - *Action*: If tests fail, analyze the results. Focus on any NEW failures related to the recent changes.
   - **Granular Options**:
     - `/test__unit_suite` - Unit tests only
     - `/test__integration_suite` - Integration tests only

5. **Completion**
   - If all steps pass, report: "✅ Feature verified: Builds, follows style guide, and passes all tests."

## Related Skills

**Typically Used After**:
- `/wolverine__create_operation`, `/marten__list_query`, `/frontend__feature_scaffold` - After implementing features
- `/test__integration_scaffold` - After creating tests
- `/frontend__debug_sse`, `/cache__debug_cache` - After fixing issues

**Component Skills** (for granular verification):
- `/ops__rebuild_clean` - Clean build if compilation issues
- `/test__unit_suite` - Run only unit tests
- `/test__integration_suite` - Run only integration tests

**See Also**:
- [test__unit_suite](../test__unit_suite/SKILL.md) - Unit test details
- [test__integration_suite](../test__integration_suite/SKILL.md) - Integration test details
- [ops__rebuild_clean](../ops__rebuild_clean/SKILL.md) - Clean build process
- [testing-guide](../../../docs/guides/testing-guide.md) - TUnit testing patterns
- [integration-testing-guide](../../../docs/guides/integration-testing-guide.md) - Aspire testing
