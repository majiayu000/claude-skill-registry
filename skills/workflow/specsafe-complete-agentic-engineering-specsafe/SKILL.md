---
description: Complete a SpecSafe specification (QA → COMPLETE stage).
---

Complete a SpecSafe specification.

**When to use:**
- QA passed with GO
- Ready to mark production-ready

**Input**: The spec ID

**Steps:**

1. **Validate QA passed**
   Verify QA report shows GO.

2. **Complete**
   ```bash
   specsafe complete "<spec-id>"
   ```

3. **Show summary**
   - Completion confirmation
   - Metrics
   - Location

**Guardrails:**
- Spec must be in QA stage
- Must have GO recommendation