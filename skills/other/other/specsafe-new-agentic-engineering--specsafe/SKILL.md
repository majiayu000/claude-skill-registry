---
description: Create a new SpecSafe specification using the TDD workflow.
---

Create a new SpecSafe specification.

**When to use:**
- Starting a new feature
- Beginning a bug fix with TDD
- Creating a new project specification

**Input**: A spec name (kebab-case) or description of what to build.

**Steps:**

1. **If no clear input, ask what to build**
   > "What spec do you want to create? Describe what you want to build or fix."

2. **Check specsafe is initialized**
   Verify `specsafe.config.json` exists. If not, advise running `specsafe init`.

3. **Create the spec**
   ```bash
   specsafe new "<name>"
   ```

4. **Show results**
   - Spec ID and location
   - Current stage: SPEC
   - Next: Edit requirements, then run `specsafe test <id>`

**Guardrails:**
- Require valid kebab-case name
- Ensure project is initialized first