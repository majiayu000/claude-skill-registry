---
name: specsafe-qa
description: Run QA validation on completed implementation. Moves spec from CODE to QA stage.
license: MIT
metadata:
  author: Agentic Engineering
  version: "1.0"
---

Run QA validation on implementation (CODE → QA stage).

**When to use:**
- All tests are passing
- Ready for quality validation
- Preparing for completion

**Input**: The spec ID (e.g., SPEC-20240204-001)

**Steps**

1. **Validate implementation is complete**

   Verify all tests are passing.
   Check that code meets requirements.

2. **Move to QA stage**

   ```bash
   specsafe qa "<spec-id>"
   ```

   This:
   - Runs full test suite
   - Generates coverage report
   - Creates QA report
   - Updates PROJECT_STATE.md

3. **Show QA results**

   Display:
   - Test results (pass/fail)
   - Coverage metrics
   - QA recommendation (GO/NO-GO)
   - Any issues found

**Output**

After QA validation:
- Test results summary
- Coverage report
- QA recommendation
- If GO: Prompt to complete
- If NO-GO: List issues to fix

**Guardrails**
- Spec must be in CODE stage
- All tests should pass before QA
- If NO-GO, must fix issues before completing
- Do NOT complete with NO-GO recommendation