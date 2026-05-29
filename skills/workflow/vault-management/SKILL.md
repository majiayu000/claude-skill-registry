---
name: vault-management
description: Manages the Obsidian vault structure, file operations, and folder organization for the Personal AI Employee. Use when creating, moving, or organizing files in the vault, managing folder structures, or maintaining the knowledge base.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Vault Management Skill

This skill provides comprehensive management of the Obsidian vault that serves as the Personal AI Employee's knowledge base and operational dashboard.

## Vault Structure

The standard vault structure for the AI Employee:

```
AI_Employee_Vault/
├── Dashboard.md              # Real-time status overview
├── Company_Handbook.md       # Rules and guidelines
├── Business_Goals.md         # Objectives and KPIs
│
├── Inbox/                    # Raw incoming items
├── Needs_Action/             # Triaged items requiring processing
├── Plans/                    # Task plans and workflows
├── Pending_Approval/         # HITL approval queue
├── Approved/                 # Cleared for execution
├── Rejected/                 # Denied actions
├── Done/                     # Completed and archived
│
├── Accounting/               # Financial records
│   ├── Current_Month.md
│   ├── Budget_Status.md
│   └── Subscriptions.md
│
├── Briefings/                # Generated reports
│   └── YYYY-MM-DD_*.md
│
├── Logs/                     # Audit logs
│   └── YYYY-MM-DD.json
│
├── Contacts/                 # Contact information
│   └── *.md
│
└── Templates/                # Document templates
    └── *.md
```

## Core Operations

### File Creation
When creating files, always include proper frontmatter:

```markdown
---
type: [type]
created: [ISO timestamp]
status: [status]
---
```

### File Movement
Move files between folders to indicate status changes:
- `Needs_Action/` → `Plans/` (planning started)
- `Plans/` → `Pending_Approval/` (needs human review)
- `Pending_Approval/` → `Approved/` (cleared to execute)
- `Approved/` → `Done/` (execution complete)

### Dashboard Updates
Keep Dashboard.md current with:
- Pending action count
- Approval queue status
- Recent activity log
- Current financial summary

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Email | `EMAIL_[id].md` | `EMAIL_abc123.md` |
| WhatsApp | `WHATSAPP_[contact]_[date].md` | `WHATSAPP_john_2026-01-07.md` |
| Finance | `FINANCE_[type]_[date].md` | `FINANCE_transaction_2026-01-07.md` |
| Plan | `PLAN_[subject].md` | `PLAN_invoice_client_a.md` |
| Approval | `[TYPE]_[subject]_[date].md` | `PAYMENT_Client_A_2026-01-07.md` |

## Reference Documentation

For detailed API and operations, see [reference.md](reference.md)

For usage examples, see [examples.md](examples.md)

## Helper Scripts

- `scripts/init_vault.py` - Initialize vault structure
- `scripts/cleanup.py` - Archive old completed items
- `scripts/backup.py` - Create vault backup
