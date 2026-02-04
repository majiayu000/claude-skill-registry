---
name: gh-updating-project-fields
description: Updates a field value for an item in a GitHub Project. Use to move items between statuses or set custom field data.
---

# Updating Project Fields

## Purpose

Edits project item data using the `gh project item-edit` command.

## 1. Safety & Verification

- **Mandatory Context**: Ensure `gh-verifying-context` has been run and confirmed by the user.
- **Human-in-the-Loop**: You MUST present the proposed field update (e.g., "Moving Status to Done") and the target item to the user before execution.
- **Verification**: Ensure the project and field IDs are correct by listing them first if not certain.

## 2. Common Workflows

### Workflow: Update Text Field

Sets a value for a text field.

**Command**:

```bash
gh project item-edit --id <item-id> --field-id <field-id> --project-id <project-id> --text "new value"
```

### Workflow: Update Status (Single Select)

Moves an item to a different status column.

**Command**:

```bash
gh project item-edit --id <item-id> --field-id <field-id> --project-id <project-id> --single-select-option-id <option-id>
```
