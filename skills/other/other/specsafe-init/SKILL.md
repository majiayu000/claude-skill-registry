---
name: specsafe-init
description: Initialize a new SpecSafe project in the current directory.
license: MIT
metadata:
  author: Agentic Engineering
  version: "1.0"
---

Initialize a new SpecSafe project with directory structure and configuration.

**When to use:**
- Starting a new project with SpecSafe
- Setting up TDD workflow
- First time using SpecSafe in a project

**Input**: Project name (optional, defaults to current directory name)

**Steps**

1. **Run init command**

   ```bash
   specsafe init [project-name]
   ```

   This creates:
   - `specs/active/` directory
   - `specs/completed/` directory
   - `specs/archive/` directory
   - `specs/template.md`
   - `specsafe.config.json`
   - `PROJECT_STATE.md`

2. **Verify initialization**

   Check all directories and files were created.

3. **Show next steps**

   Guide user to:
   - Create first spec with `/specsafe:new`
   - Review the spec template
   - Understand the workflow

**Output**

After initialization:
- Confirmation of created structure
- Location of key files
- Next steps guidance
- Prompt: "Ready to create your first spec? Run `/specsafe:new <name>`"

**Guardrails**
- Check if already initialized (prevent double-init)
- Ensure write permissions in current directory
- Create all required directories