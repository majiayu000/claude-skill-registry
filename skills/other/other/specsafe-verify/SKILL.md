---
name: specsafe-verify
description: Run tests and validate implementation. Loops back to dev if tests fail. Moves spec from CODE to QA stage.
disable-model-invocation: true
---

Run tests and validate implementation (CODE → QA stage). Loops back to dev if tests fail.

**When to use:**
- Implementation appears complete
- Need to validate against spec requirements
- Preparing for QA review
- Before marking spec as complete

**Input**: The spec ID (e.g., SPEC-20260211-001)

**Steps**

1. **Validate CODE stage**

   Check `specs/active/<spec-id>.md`:
   - Status must be CODE stage
   - Implementation files exist
   - Previous test run was passing

2. **Run full test suite**

   Execute all tests with coverage:
   ```bash
   pnpm test --coverage  # or equivalent
   ```

3. **Analyze results**

   Check for:
   - ❌ **FAILING TESTS**: Loop back to dev
   - ⚠️ **LOW COVERAGE**: Flag for improvement
   - ✅ **ALL PASSING**: Proceed to validation

4. **If tests FAIL → Loop to dev**

   This is the critical feedback loop:

   ```
   ┌─────────────┐     FAIL     ┌─────────────┐
   │   VERIFY    │──────────────│    DEV      │
   └─────────────┘              └─────────────┘
          │                            │
          │ PASS                       │ Code fix
          ▼                            ▼
   ┌─────────────┐              ┌─────────────┐
   │     QA      │              │  Re-test    │
   └─────────────┘              └─────────────┘
   ```

   Actions:
   - Show failing test names
   - Analyze failure patterns
   - Suggest fixes
   - Prompt: `/specsafe:dev <id>` to fix

   **Do NOT proceed to QA with failing tests**

5. **If tests PASS → Validate against spec**

   Cross-reference implementation with requirements:
   - ✅ All P0 requirements satisfied?
   - ✅ All scenarios covered?
   - ✅ Edge cases handled?
   - ✅ No unintended side effects?

6. **Generate QA report**

   Document validation results:
   ```markdown
   ## QA Report: SPEC-YYYYMMDD-NNN
   
   ### Test Results
   - Total: 12
   - Passed: 12
   - Failed: 0
   - Coverage: 94%
   
   ### Requirements Validation
   - P0: 3/3 satisfied
   - P1: 3/3 satisfied
   - P2: 2/2 satisfied
   
   ### Recommendation: GO / NO-GO
   ```

7. **Move to QA stage**

   If validation passes:
   ```bash
   specsafe qa "<spec-id>"
   ```

   This:
   - Updates spec status to QA
   - Archives QA report
   - Updates PROJECT_STATE.md

8. **Show verification summary**

   Display:
   - Test results (pass/fail counts)
   - Coverage percentage
   - Requirements satisfaction
   - QA recommendation
   - Next: `/specsafe:done <id>` or back to `/specsafe:dev <id>`

**Output**

**If tests FAIL:**
- ❌ Test failure report
- 📋 Analysis of failures
- 🔧 Suggested fixes
- 📋 Prompt: "Fix issues and run `/specsafe:dev <id>` again"

**If tests PASS:**
- ✅ All tests passing
- ✅ Coverage report
- ✅ QA validation complete
- ✅ Status: QA stage
- 📋 Prompt: "Ready to complete? Run `/specsafe:done <id>`"

**Guardrails**
- ⛔ NEVER proceed to QA with failing tests
- ⛔ NEVER override test failures
- Coverage target: minimum 80% (prefer 90%+)
- All P0 requirements must be satisfied
- QA report must be generated for traceability
- If NO-GO, document specific issues to fix

**Example - FAIL**
```
User: /specsafe:verify SPEC-20260211-004
→ Running tests...
→ ❌ 2 tests FAILED
→ Coverage: 87%
→ 
→ Failures:
→   - should reject invalid token
→   - should handle rate limiting
→ 
→ 📋 Run `/specsafe:dev SPEC-20260211-004` to fix
```

**Example - PASS**
```
User: /specsafe:verify SPEC-20260211-004
→ Running tests...
→ ✅ All 12 tests PASSED
→ ✅ Coverage: 94%
→ ✅ All P0 requirements satisfied
→ ✅ QA Report generated
→ Status: QA
→ Next: /specsafe:done SPEC-20260211-004
```