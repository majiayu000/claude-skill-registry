---
name: specsafe-new
description: Create a new spec with PRD, tech stack, and rules. Initializes SPEC stage.
disable-model-invocation: true
---

Create a new SpecSafe specification (NEW → SPEC stage).

**When to use:**
- Starting a new feature
- Need to define requirements before coding
- Want to establish tech stack and rules upfront

**Input**: Feature name or brief description

**Steps**

1. **Validate project state**

   Check PROJECT_STATE.md exists (run `specsafe init` if not).
   Review current active specs to avoid conflicts.

2. **Create the spec**

   ```bash
   specsafe new "<feature-name>"
   ```

   This:
   - Generates a new spec file in `specs/active/`
   - Assigns a unique SPEC-ID (e.g., SPEC-20260211-001)
   - Sets status to SPEC stage
   - Updates PROJECT_STATE.md

3. **Initialize PRD structure**

   Open the new spec file and populate:
   - **Purpose (WHY)**: One paragraph explaining why this feature exists
   - **Scope (WHAT)**: In scope and out of scope sections
   - **Tech Stack**: Target frameworks, languages, tools
   - **Rules**: Coding standards, constraints, conventions

4. **Define initial requirements**

   Add to Requirements table:
   - Functional requirements (what the system must do)
   - Non-functional requirements (performance, security)
   - Priority levels (P0=must have, P1=should have, P2=nice to have)

5. **Show next steps**

   Display:
   - Spec file location
   - Current stage (SPEC)
   - Next command: `/specsafe:spec <id>` to flesh out details

**Output**

After creation:
- ✅ Spec file created at `specs/active/SPEC-YYYYMMDD-NNN-<feature-name>.md`
- ✅ Status set to SPEC stage
- ✅ PROJECT_STATE.md updated
- 📋 Prompt: "Edit the spec to add requirements, then run `/specsafe:spec <id>`"

**Guardrails**
- Feature name should be descriptive (kebab-case recommended)
- Check for naming conflicts with existing specs
- Tech stack decisions should reference existing project standards
- Never start coding without a spec in SPEC or later stage

**Example**
```
User: /specsafe:new "user-authentication"
→ Creates SPEC-20260211-004-user-authentication.md
→ Status: SPEC
→ Next: /specsafe:spec SPEC-20260211-004
```
