---
name: test
description: Build and run analyzer tests, optionally filtered to a specific SPIRE rule. Use when asked to test, verify, or check analyzer behavior.
user-invocable: true
allowed-tools: Bash, Read, Grep
argument-hint: [optional:RuleId]
hooks:
  Stop:
    - command: "bash .claude/hooks/log-skill-usage.sh test"
---

# Build & Run Tests

Arguments: `$ARGUMENTS`

1. If `$ARGUMENTS` is empty, run all tests:
   ```
   dotnet test
   ```

2. If a rule ID is given (e.g., `{RuleId}`), run only that rule's tests:
   ```
   dotnet test --filter "FullyQualifiedName~$ARGUMENTS"
   ```

3. Report results concisely — pass/fail counts and any failure details.

## Constraints

- Do NOT modify test code to make tests pass
- Do NOT skip, ignore, or suppress failing tests
- Do NOT modify analyzer code — report failures as-is
- If the build fails, report the build error and stop — do not attempt fixes
