---
name: process-inbox
description: |
  Process items in the vault's /Needs_Action folder. Read each pending action file,
  determine the appropriate response based on Company_Handbook.md rules, process the
  item, and move completed items to /Done. Use when there are pending items to process.
---

# Process Inbox Items

Process all pending items in the vault's /Needs_Action folder following Company Handbook rules.

## Workflow

1. **Read Company Handbook** for processing rules:
   ```
   Read vault/Company_Handbook.md
   ```

2. **List pending items** in /Needs_Action:
   ```
   List all .md files in vault/Needs_Action/ (ignore .gitkeep)
   ```

3. **For each pending item**:
   - Read the .md file and parse the YAML frontmatter
   - Determine priority from the `priority` field
   - Process high priority items first
   - Based on `type` field, take appropriate action:
     - `file_drop`: Review the associated file, categorize it, write a summary
     - `email`: Draft a response or flag for human review
     - `task`: Create a plan in /Plans

4. **After processing each item**:
   - Update the frontmatter `status` to `completed`
   - Add a processing summary to the file
   - Move the .md file and any associated files to vault/Done/
   - Log the action

5. **Update Dashboard**:
   After processing all items, update vault/Dashboard.md with:
   - Number of items processed
   - Any items requiring human attention
   - Updated stats

## Important Rules

- Follow the Company_Handbook.md rules strictly
- Never auto-approve actions listed as "Require approval" in the handbook
- If unsure about an action, create an approval request in vault/Pending_Approval/
- Always log actions to vault/Logs/
- Process items in priority order: high → medium → low

## Log Format

Write log entries as JSON to vault/Logs/YYYY-MM-DD.json:
```json
{
  "timestamp": "ISO-8601",
  "action_type": "item_processed",
  "actor": "claude_code",
  "target": "filename",
  "parameters": {},
  "result": "success"
}
```
