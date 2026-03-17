---
description: Start implementation phase (TEST → CODE stage).
---

Start TDD implementation following red-green-refactor.

**When to use:**
- Tests are generated and ready
- Starting TDD cycle

**Input**: The spec ID

**Steps:**

1. **Validate tests exist**

2. **Move to CODE stage**
   ```bash
   specsafe code "<spec-id>"
   ```

3. **Guide TDD**
   - Run tests (RED)
   - Write minimum code (GREEN)
   - Refactor
   - Repeat

4. **Offer help**
   - Write implementation
   - Review code
   - Debug tests

**Guardrails:**
- Spec must be in TEST stage
- Tests must exist