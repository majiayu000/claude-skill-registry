---
name: quality
description: Run project quality gates. Executes lint and tests based on project placeholder mappings.
---

# Quality

Run project quality gates and report results.

## Inputs

Ask the user for scope:
- **Default (recommended):** lint + unit tests (fast feedback)
- **Full:** all tests + smoke tests
- **Dry-run:** print commands without executing

## Workflow

1. **Load commands** from project placeholder mappings:
   - `{{LINT_COMMAND}}`
   - `{{RUN_UNIT_TESTS_COMMAND}}` (optional)
   - `{{RUN_ALL_TESTS_COMMAND}}`
   - `{{SMOKE_TEST_COMMAND}}` (optional)

2. **Execute** in order: lint → tests → smoke (if full scope).

3. **Report:**
   ```
   ## Quality Gate Results
   Scope: <default|full|dry-run>

   Results:
   ✅/❌ Lint: passed | failed
   ✅/❌ Tests: X passed, Y failed
   ✅/❌ Smoke: passed | failed | skipped

   [If failures: show failing test names and relevant log lines]

   Next: Fix failures | Proceed with PR
   ```

## Notes

- Stop immediately if lint or tests fail.
- Do not modify test files.
- For CI/PR workflows, always run at least lint + tests before marking ready.
