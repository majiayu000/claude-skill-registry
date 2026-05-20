---
name: specsafe-test-create
description: Create tests from spec scenarios
argument-hint: "[spec-id]"
disable-model-invocation: true
---

Generate comprehensive test suite:
1. Read spec from specs/active/SPEC-ID.md
2. Create test files in src/__tests__/SPEC-ID/
3. Map Given/When/Then scenarios to test cases
4. Include happy path and edge cases
5. Update PROJECT_STATE.md (SPEC → TEST-CREATE)

Report test count and coverage expectations.
