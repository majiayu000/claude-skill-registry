---
description: Initialize a new SpecSafe project.
---

Initialize a SpecSafe project.

**When to use:**
- Starting new project with SpecSafe
- First time setup

**Input**: Project name (optional)

**Steps:**

1. **Run init**
   ```bash
   specsafe init [project-name]
   ```

2. **Verify created**
   - specs/active/, completed/, archive/
   - specs/template.md
   - specsafe.config.json
   - PROJECT_STATE.md

3. **Show next steps**
   Guide to create first spec.

**Guardrails:**
- Check not already initialized
- Ensure write permissions