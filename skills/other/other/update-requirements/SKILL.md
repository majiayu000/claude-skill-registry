---
name: update-requirements
description: Update requirements and cascade changes to specs and plans. Accepts natural language change descriptions to modify the full spec chain. Use when user wants to add, remove, or modify requirements.
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Update Requirements

## Skill Info

Part of the **spec-manager** agent. This skill updates requirements and cascades changes through specs and plans.

## Input

The user provides a change description as arguments: $ARGUMENTS

The change description is a natural language instruction describing what to add, remove, or modify in the requirements.

**Examples**:
- `/update-requirements Third requirements should be removed`
- `/update-requirements Add new requirements. API docs should be updated.`
- `/update-requirements Change FR-2 acceptance criteria to include error handling`
- `/update-requirements Performance requirement should be <200ms instead of <500ms`

If no arguments are provided, ask the user what changes they want to make.

## Process

### Step 1: Identify Target Spec Set

1. List all `*/requirements.md` files in `specs/` directory
2. If only one spec set exists, use it automatically
3. If multiple exist, ask the user which one to update
4. Read all three files for the selected slug:
   - `specs/{slug}/requirements.md`
   - `specs/{slug}/specs.md`
   - `specs/{slug}/plans.md`

### Step 2: Analyze the Change Request

Parse the user's natural language instruction to determine:

1. **Change type**: Add / Remove / Modify
2. **Target section**: Which part of requirements is affected (functional, non-functional, constraints, goals, etc.)
3. **Specific items**: Which FR-X, NFR, or section to change
4. **Scope of impact**: How this change ripples through specs and plans

Present a brief summary of understood changes to confirm with the user before applying:

```
Understood changes:
  - [Add/Remove/Modify]: {description}
  - Affected sections: {list}
  - Impact: {brief impact assessment}

Proceed with these changes?
```

### Step 3: Update Requirements

Apply changes to `specs/{slug}/requirements.md`:

- **Adding**: Insert new FR-X entries with proper numbering, or add to the relevant section
- **Removing**: Remove the specified requirement and renumber remaining ones
- **Modifying**: Update the specified content in place
- Update the metadata:
  - Add `> Updated: {YYYY-MM-DD}` (or update existing)
  - Keep Status as-is or change to "Updated" if it was "Final"

### Step 4: Update Specs

Read current `specs/{slug}/specs.md` and apply cascading changes:

- **If specs were already generated** (status is not "Pending"):
  1. Identify which TS-X entries are affected by the requirement change
  2. For **added requirements**: generate new TS-X entries following the existing format
  3. For **removed requirements**: remove corresponding TS-X entries and related sections (data models, API endpoints, etc.)
  4. For **modified requirements**: update affected TS-X entries and downstream sections
  5. Re-check architecture, data models, API design, and error handling for consistency
  6. Add entry to Clarification Log:
    ```
    | N | Requirement update: {brief description} | Applied via /update-requirements | {date} |
    ```
  7. Update `> Updated: {YYYY-MM-DD}`

- **If specs are still "Pending"**: Update status to note requirements have changed, no further action needed

### Step 5: Update Plans

Read current `specs/{slug}/plans.md` and apply cascading changes:

- **If plans were already generated** (status is not "Pending"):
  1. Identify which implementation steps are affected
  2. For **added requirements**: add new implementation steps in the appropriate order
  3. For **removed requirements**: remove corresponding steps, update step numbering, and clean up dependency references
  4. For **modified requirements**: update affected steps
  5. Update:
     - Implementation Steps (add/remove/modify)
     - Task Breakdown checklist
     - File Change Summary table
     - Dependencies Between Steps
     - Testing Strategy (if test coverage changes)
     - Progress Tracking table (preserve status of unaffected completed steps)
     - Acceptance Criteria Checklist
  6. Update `> Updated: {YYYY-MM-DD}`

- **If plans are still "Pending"**: Update status to note specs have changed, no further action needed

### Step 6: Report Changes

Display a summary of all changes made:

```
Requirements updated for: "{Original Task Title}"

Changes applied:
  Requirements (specs/{slug}/requirements.md):
    - {change description}

  Specs (specs/{slug}/specs.md):
    - {change description, or "No changes needed (still pending)"}

  Plans (specs/{slug}/plans.md):
    - {change description, or "No changes needed (still pending)"}

Change impact:
  - {N} requirements affected
  - {X} specs updated
  - {Y} plan steps updated
```

## Handling Edge Cases

### Conflicting changes
If the requested change conflicts with existing requirements:
- Identify the conflict
- Present both sides to the user
- Ask which takes priority
- Apply the resolution

### Completed implementation steps
If some plan steps are already marked as "Completed":
- Do NOT change completed steps unless the change directly invalidates them
- If a completed step is invalidated, warn the user explicitly:
  ```
  Warning: Step {N} was already completed but is affected by this change.
  The implementation may need to be revised. Please review.
  ```
- Add a note in the Progress Tracking table

### Ambiguous instructions
If the change description is ambiguous:
- Ask the user for clarification before making any changes
- Never guess which requirement to modify

## Important

- Always read all three files before making changes
- Confirm understood changes with the user before applying
- Preserve content that is not affected by the change
- Maintain proper numbering (FR-X, TS-X, Step N) after additions/removals
- Keep the Clarification Log updated in specs
- Never silently drop requirements or specs - always report what was removed
- Preserve completed step progress in plans unless explicitly invalidated
