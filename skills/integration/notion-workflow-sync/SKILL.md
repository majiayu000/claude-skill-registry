---
name: notion-workflow-sync
description: "Sync workflows between Odoo, BIR systems, and Notion with external ID upsert and deduplication"
---

# Notion Workflow Sync
Automate task management using Notion with atomic upsert operations.

## What This Does
- Month-end closing checklists
- BIR filing schedules  
- Approval workflow tracking
- External ID deduplication
- Real-time sync

## Quick Example
```python
notion.upsert_by_external_id(
    database_id=month_end_db,
    external_id=f'CLOSE-2025-10-{task_id}',
    properties={'Task': 'Post accruals', 'Status': 'In Progress'}
)
```

## Getting Started
"Create month-end tasks for October all agencies"
"Sync BIR filing schedule to Notion"
