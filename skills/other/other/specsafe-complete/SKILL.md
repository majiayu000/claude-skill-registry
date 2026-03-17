---
name: specsafe-complete
description: Complete a SpecSafe specification. Moves spec from QA to COMPLETE stage.
license: MIT
metadata:
  author: Agentic Engineering
  version: "1.0"
---

Complete a SpecSafe specification (QA → COMPLETE stage).

**When to use:**
- QA validation passed with GO recommendation
- Ready to mark as production-ready
- Finalizing the spec

**Input**: The spec ID (e.g., SPEC-20240204-001)

**Steps**

1. **Validate QA passed**

   Verify QA report shows GO recommendation.
   Check that all critical issues are resolved.

2. **Complete the spec**

   ```bash
   specsafe complete "<spec-id>"
   ```

   This:
   - Moves spec to COMPLETE stage
   - Moves spec file to `specs/completed/`
   - Archives QA report
   - Updates PROJECT_STATE.md

3. **Show completion summary**

   Display:
   - Spec completion confirmation
   - Metrics (time to complete, coverage, etc.)
   - Location of completed spec
   - Next steps

**Output**

After completion:
- ✅ Completion confirmation
- Spec moved to `specs/completed/`
- PROJECT_STATE.md updated
- Prompt: "Ready to start a new spec? Run `specsafe new`"

**Guardrails**
- Spec must be in QA stage
- QA report must recommend GO
- Do NOT complete if NO-GO
- Confirm all requirements met