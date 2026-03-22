---
name: specsafe-verify
description: Verify implementation and iterate
argument-hint: "[spec-id]"
disable-model-invocation: true
---

Verify implementation by running tests:
1. Execute test suite: npm test -- SPEC-ID
2. Analyze failures and map to requirements
3. Fix code (not tests) and re-run
4. Iterate until all tests pass
5. Check coverage meets requirements
6. Run full suite for regressions

Update PROJECT_STATE.md (TEST-APPLY → VERIFY).
Report: pass rate, coverage %, issues.
