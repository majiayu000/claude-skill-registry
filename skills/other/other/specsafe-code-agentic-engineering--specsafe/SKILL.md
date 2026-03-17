---
name: specsafe-code
description: Start implementation phase of SpecSafe TDD workflow. Moves spec from TEST to CODE stage.
license: MIT
metadata:
  author: Agentic Engineering
  version: "1.0"
---

Start implementation phase (TEST → CODE stage) following TDD red-green-refactor.

**When to use:**
- Tests are generated and ready for implementation
- Starting TDD development cycle
- Moving from TEST to CODE stage

**Input**: The spec ID (e.g., SPEC-20240204-001)

**Steps**

1. **Validate tests exist**

   Verify test files were generated for this spec.
   Check that tests exist (even if marked `.skip`).

2. **Move to CODE stage**

   ```bash
   specsafe code "<spec-id>"
   ```

   This updates the spec stage to CODE.

3. **Guide TDD implementation**

   Explain the TDD cycle:
   - Run tests (should fail - RED)
   - Write minimum code to pass one test (GREEN)
   - Refactor if needed
   - Repeat until all tests pass

4. **Provide implementation support**

   Offer to:
   - Help write the implementation
   - Review code
   - Suggest refactoring
   - Debug failing tests

**Output**

After moving to CODE stage:
- Confirmation of stage change
- TDD cycle reminder
- Current test status
- Prompt: "Let's implement the code. What would you like help with?"

**Guardrails**
- Spec must be in TEST stage
- Tests must exist
- Remind user to follow TDD (test first, then code)