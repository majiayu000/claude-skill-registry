---
description: Run QA validation (CODE → QA stage).
---

Run QA validation on implementation.

**When to use:**
- All tests passing
- Ready for quality validation

**Input**: The spec ID

**Steps:**

1. **Validate implementation complete**

2. **Run QA**
   ```bash
   specsafe qa "<spec-id>"
   ```

3. **Show results**
   - Test results
   - Coverage metrics
   - GO/NO-GO recommendation
   - Issues if any

**Guardrails:**
- Spec must be in CODE stage
- Do NOT complete if NO-GO