---
name: prd-status
description: Check and update PRD status through lifecycle
argument-hint: <prd-file> [--set <status>]
---

# prd-status

**Category**: Product & Strategy

## Usage

```bash
prd-status <prd-file> <new-status> [--comment "reason for change"]
```

## Arguments

- `<prd-file>`: Required - Path to the PRD file to update
- `<new-status>`: Required - New status (draft, review, approved, active, complete, archived)
- `--comment`: Optional - Comment explaining the status change

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. Validate that the PRD file exists
2. Validate that the new status is one of the allowed values
3. Read the current PRD metadata
4. Check if the status transition is valid according to the lifecycle rules
5. Update the PRD metadata:
   - Change `status` field to new status
   - Update `last_updated` to current date
   - If moving to APPROVED: prompt for `approved_by` name and set `approved_date`
   - If moving to ARCHIVED: add archive metadata section
6. Add status change to a history section in the PRD (create if doesn't exist)
7. Determine the new directory location based on status
8. Move the file to the appropriate directory (using git mv if in git repo)
9. Update any relative path references in the moved PRD
10. Report the changes made

## Status Transition Rules

Valid transitions:
- DRAFT → REVIEW, ARCHIVED
- REVIEW → APPROVED, DRAFT, ARCHIVED
- APPROVED → ACTIVE, REVIEW, ARCHIVED
- ACTIVE → COMPLETE, ARCHIVED
- COMPLETE → ARCHIVED
- ARCHIVED → (no transitions allowed)

## Metadata Updates

### Moving to APPROVED
```yaml
status: APPROVED
approved_by: [Prompt for name]
approved_date: 2025-01-06
```

### Moving to ARCHIVED
```yaml
status: ARCHIVED
archive_date: 2025-01-06
archive_reason: [Use --comment or prompt]
final_task_completion: [Calculate if task file exists]
```

### Status History Section
Add or update in PRD:
```markdown
## Status History

- 2025-01-06: DRAFT → REVIEW (Ready for stakeholder feedback)
- 2025-01-07: REVIEW → APPROVED (Approved by Jane Smith)
- 2025-01-08: APPROVED → ACTIVE (Development started)
```

## Output Format

```
📝 Updating PRD Status...

Current Status: REVIEW
New Status: APPROVED

✅ Metadata updated:
   - status: APPROVED
   - approved_by: Jane Smith
   - approved_date: 2025-01-06
   - last_updated: 2025-01-06

📄 Moving file:
   From: ./feature-auth-frd.md
   To: product-docs/prds/approved/feature-auth-frd.md

✅ Status change complete!
   Comment: "All stakeholders have reviewed and approved the requirements"
```

## Error Handling

- If file doesn't exist: Exit with error message
- If invalid status: Show valid status options and exit
- If invalid transition: Show allowed transitions from current status
- If destination file exists: Prompt to overwrite or abort
- If no write permissions: Report error and suggest using sudo

## Example

```bash
# Move PRD to review status
prd-status feature-auth-frd.md review --comment "Ready for stakeholder review"

# Approve a PRD (will prompt for approver name)
prd-status feature-auth-frd.md approved

# Archive a completed PRD
prd-status old-feature-frd.md archived --comment "Feature deprecated in v2.0"

# Mark PRD as active development
prd-status feature-auth-frd.md active
```

## Implementation Tips for Claude Code

1. **Transition Validation**: Implement a state machine to validate transitions
2. **Interactive Prompts**: Ask for required fields like approver name when needed
3. **History Preservation**: Append to status history, don't overwrite
4. **Path Resolution**: Handle both absolute and relative paths for PRD files
5. **Atomic Operations**: Update metadata and move file in a transaction-like manner
6. **Progress Integration**: If moving to COMPLETE, calculate final task completion percentage
