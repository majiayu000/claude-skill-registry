---
description: Generate tests from a SpecSafe specification (SPEC → TEST stage).
---

Generate tests from a SpecSafe specification.

**When to use:**
- Requirements are defined and ready for tests
- Moving from SPEC to TEST stage

**Input**: The spec ID (e.g., SPEC-20240204-001)

**Steps:**

1. **Validate spec exists and is in SPEC stage**
   Check that the spec file exists in `specs/active/` with requirements.

2. **Generate tests**
   ```bash
   specsafe test "<spec-id>"
   ```

3. **Show results**
   - Test files created
   - Number of tests
   - Location
   - Next: Implement code, run `specsafe-code <id>`

**Guardrails:**
- Spec must be in SPEC stage
- Requirements must be defined