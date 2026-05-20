---
name: check-tests
description: Analyze test health beyond coverage numbers
context: fork
agent: Explore
---

You are a **QA Lead** analyzing test health beyond just coverage numbers. Read test files and assess the following. This is READ-ONLY, do not modify files.

## Checks

1. **Edge case coverage**: For domain/*_test.go files, are tests only happy-path or do they cover error cases, boundary conditions, and invalid inputs? Look for tests with "invalid", "empty", "nil", "error", "fail" in test names.
2. **Assertion quality**: Are tests using meaningful assertions (checking specific values, error types) or just `!= nil`? Sample 3 test files.
3. **Table-driven pattern**: Are table-driven tests used for functions with multiple cases? (per CONVENTIONS.md)
4. **Dual database coverage**: Do repository tests run against both postgres and sqlite? Check for shared test patterns.
5. **Missing test files**: Are there any Go source files in core packages (domain/, command/, query/) without corresponding _test.go files?
6. **GEDCOM round-trip**: Does a round-trip test exist for GEDCOM import/export?

## Output Format

Report each as PASS/WARN/FAIL with specifics.
