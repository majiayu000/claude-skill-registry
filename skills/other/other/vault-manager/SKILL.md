---
name: vault-manager
description: |
  General vault management operations. Organize files, clean up processed items,
  verify folder structure integrity, and manage the vault workflow. Use for vault
  maintenance, file organization, and workflow management tasks.
---

# Vault Manager

Manage and maintain the Obsidian vault structure and workflow.

## Available Operations

### 1. Verify Vault Structure
Ensure all required folders exist:
```
vault/
├── Inbox/              # Drop folder for new items (watched by FileSystemWatcher)
├── Needs_Action/       # Items awaiting processing
├── Done/               # Completed items archive
├── Plans/              # Action plans created by Claude
├── Logs/               # JSON action logs (YYYY-MM-DD.json)
├── Pending_Approval/   # Items needing human approval
├── Approved/           # Human-approved actions
├── Rejected/           # Human-rejected actions
├── Briefings/          # Generated briefing reports
├── Accounting/         # Financial tracking
├── Dashboard.md        # Real-time status dashboard
├── Company_Handbook.md # Rules of engagement
└── Business_Goals.md   # Business objectives and metrics
```

### 2. Move Processed Items to Done
For items in /Needs_Action with `status: completed` in frontmatter:
1. Read the file
2. Verify status is "completed"
3. Move the .md file to vault/Done/
4. Move any associated files (same name prefix) to vault/Done/
5. Log the move action

### 3. Clean Up Old Logs
- Logs older than 90 days can be archived
- Never delete logs, only move to an /Archive folder

### 4. Check Pending Approvals
List all items in vault/Pending_Approval/ that are waiting for human action.
Report their age and urgency.

### 5. Generate Status Report
Create a summary of the current vault state:
- Total items per folder
- Oldest pending item
- Processing throughput (items/day from logs)
- Any anomalies or issues

## Important Rules

- Never delete files from the vault without explicit human approval
- Always verify file frontmatter before moving
- Log every file operation
- Maintain .gitkeep files in empty directories
