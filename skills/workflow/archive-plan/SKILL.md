---
name: archive-plan
description: Archive completed plan documents by moving them to the plans/archived folder. Use when a plan has been fully implemented, all to-do items are completed, or when the user requests to archive a plan.
---

# Plan Archiving

After a plan has been fully implemented or all to-do items have been completed, prompt the user to archive the plan.

## When to Archive

Archive a plan when:
- All steps show 🟩 Done status
- Overall progress is 100%
- The plan has been fully implemented
- The user explicitly requests archiving

## Archiving Process

1. **Check completion status**: Verify all tasks are marked as 🟩 Done and progress is 100%
2. **Prompt the user**: Ask if they would like to archive the completed plan
   - Example: "All tasks in this plan are complete. Would you like to archive it?"
3. **If user confirms**:
   - Move the plan file from `plans/` to `plans/archived/`
   - Preserve the original filename (including the numeric prefix)
   - Create the `plans/archived/` directory if it doesn't exist
4. **If user declines**: Leave the plan in `plans/` directory

## File Operations

- **Source**: `plans/XXX-plan-name.md`
- **Destination**: `plans/archived/XXX-plan-name.md`
- Maintain the numeric prefix in the archived filename
- Do not modify the plan content when archiving

## Important Notes

- Always ask for user confirmation before archiving
- Only archive plans that are 100% complete
- Preserve the original file structure and naming
- If the user wants to keep working on the plan, do not archive it
