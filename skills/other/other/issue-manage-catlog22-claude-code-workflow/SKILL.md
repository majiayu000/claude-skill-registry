---
name: issue-manage
description: Interactive issue management with menu-driven CRUD operations. Use when managing issues, viewing issue status, editing issue fields, performing bulk operations, or viewing issue history. Triggers on "manage issue", "list issues", "edit issue", "delete issue", "bulk update", "issue dashboard", "issue history", "completed issues".
allowed-tools: Bash, Read, Write, AskUserQuestion, Agent, Glob
---

# Issue Management Skill

Interactive menu-driven interface for issue CRUD operations via `ccw issue` CLI.

## Quick Start

Ask me:
- "Show all issues" → List with filters
- "View issue GH-123" → Detailed inspection
- "Edit issue priority" → Modify fields
- "Delete old issues" → Remove with confirmation
- "Bulk update status" → Batch operations
- "Show completed issues" → View issue history
- "Archive old issues" → Move to history

## CLI Endpoints

```bash
# Core operations
ccw issue list                      # List active issues
ccw issue list <id> --json          # Get issue details
ccw issue history                   # List completed issues (from history)
ccw issue history --json            # Completed issues as JSON
ccw issue status <id>               # Detailed status
ccw issue init <id> --title "..."   # Create issue
ccw issue task <id> --title "..."   # Add task
ccw issue bind <id> <solution-id>   # Bind solution
ccw issue update <id> --status completed  # Complete & auto-archive

# Solution queries
ccw issue solution <id>             # List solutions for a single issue
ccw issue solution <id> --brief     # Brief: solution_id, files_touched, task_count
ccw issue solutions                 # Batch list all bound solutions
ccw issue solutions --status planned --brief  # Filter by issue status

# Queue management
ccw issue queue                     # List current queue
ccw issue queue add <id>            # Add to queue
ccw issue queue list                # Queue history
ccw issue queue switch <queue-id>   # Switch queue
ccw issue queue archive             # Archive queue
ccw issue queue delete <queue-id>   # Delete queue
ccw issue next                      # Get next task
ccw issue done <queue-id>           # Mark completed
ccw issue update --from-queue       # Sync statuses from queue
```

## Operations

### 1. LIST 📋

Filter and browse issues:

```
┌─ Filter by Status ─────────────────┐
│ □ All        □ Registered          │
│ □ Planned    □ Queued              │
│ □ Executing  □ Completed           │
└────────────────────────────────────┘
```

**Flow**:
1. Ask filter preferences → `ccw issue list --json`
2. Display table: ID | Status | Priority | Title
3. Select issue for detail view

### 2. VIEW 🔍

Detailed issue inspection:

```
┌─ Issue: GH-123 ─────────────────────┐
│ Title: Fix authentication bug       │
│ Status: planned | Priority: P2      │
│ Solutions: 2 (1 bound)              │
│ Tasks: 5 pending                    │
└─────────────────────────────────────┘
```

**Flow**:
1. Fetch `ccw issue status <id> --json`
2. Display issue + solutions + tasks
3. Offer actions: Edit | Plan | Queue | Delete

### 3. EDIT ✏️

Modify issue fields:

| Field | Options |
|-------|---------|
| Title | Free text |
| Priority | P1-P5 |
| Status | registered → completed |
| Context | Problem description |
| Labels | Comma-separated |

**Flow**:
1. Select field to edit
2. Show current value
3. Collect new value via AskUserQuestion
4. Update `.workflow/issues/issues.jsonl`

### 4. DELETE 🗑️

Remove with confirmation:

```
⚠️ Delete issue GH-123?
This will also remove:
- Associated solutions
- Queued tasks

[Delete] [Cancel]
```

**Flow**:
1. Confirm deletion via AskUserQuestion
2. Remove from `issues.jsonl`
3. Clean up `solutions/<id>.jsonl`
4. Remove from `queue.json`

### 5. HISTORY 📚

View and manage completed issues:

```
┌─ Issue History ─────────────────────┐
│ ID                 Completed   Title │
│ ISS-001  2025-12-28 12:00   Fix bug │
│ ISS-002  2025-12-27 15:30   Feature │
└──────────────────────────────────────┘
```

**Flow**:
1. Fetch `ccw issue history --json`
2. Display table: ID | Completed At | Title
3. Optional: Filter by date range

**Auto-Archive**: When issue status → `completed`:
- Issue moves from `issues.jsonl` → `issue-history.jsonl`
- Solutions remain in `solutions/<id>.jsonl`
- Queue items marked completed

### 6. BULK 📦

Batch operations:

| Operation | Description |
|-----------|-------------|
| Update Status | Change multiple issues |
| Update Priority | Batch priority change |
| Add Labels | Tag multiple issues |
| Delete Multiple | Bulk removal |
| Queue All Planned | Add all planned to queue |
| Retry All Failed | Reset failed tasks |
| Sync from Queue | Update statuses from active queue |

## Workflow

```
┌────────────────────────────────────────────────┐
│              Main Menu                          │
│  ┌────┐ ┌────┐ ┌────┐ ┌─────┐ ┌────┐          │
│  │List│ │View│ │Edit│ │Hist.│ │Bulk│          │
│  └──┬─┘ └──┬─┘ └──┬─┘ └──┬──┘ └──┬─┘          │
└─────┼──────┼──────┼──────┼───────┼─────────────┘
      │      │      │      │       │
      ▼      ▼      ▼      ▼       ▼
   Filter  Detail  Fields  History Multi
   Select  Actions Update  Browse  Select
      │      │      │      │       │
      └──────┴──────┴──────┴───────┘
                    │
                    ▼
             Back to Menu
```

**Issue Lifecycle**:
```
registered → planned → queued → executing → completed
                                               │
                                               ▼
                                    issue-history.jsonl
```

## Implementation Guide

### Entry Point

```javascript
// Parse input for issue ID
const issueId = input.match(/^([A-Z]+-\d+|ISS-\d+)/i)?.[1];

// Show main menu
await showMainMenu(issueId);
```

### Main Menu Pattern

```javascript
// 1. Fetch dashboard data
const issues = JSON.parse(Bash('ccw issue list --json') || '[]');
const history = JSON.parse(Bash('ccw issue history --json 2>/dev/null') || '[]');
const queue = JSON.parse(Bash('ccw issue queue --json 2>/dev/null') || '{}');

// 2. Display summary
console.log(`Active: ${issues.length} | Completed: ${history.length} | Queue: ${queue.pending_count || 0} pending`);

// 3. Ask action via AskUserQuestion
const action = AskUserQuestion({
  questions: [{
    question: 'What would you like to do?',
    header: 'Action',
    options: [
      { label: 'List Issues', description: 'Browse active issues' },
      { label: 'View Issue', description: 'Detail view (includes history)' },
      { label: 'Edit Issue', description: 'Modify fields' },
      { label: 'Bulk Operations', description: 'Batch actions' }
    ]
  }]
});

// 4. Route to handler
```

### Filter Pattern

```javascript
const filter = AskUserQuestion({
  questions: [{
    question: 'Filter by status?',
    header: 'Filter',
    multiSelect: true,
    options: [
      { label: 'All', description: 'Show all' },
      { label: 'Registered', description: 'Unplanned' },
      { label: 'Planned', description: 'Has solution' },
      { label: 'Executing', description: 'In progress' }
    ]
  }]
});
```

### Edit Pattern

```javascript
// Select field
const field = AskUserQuestion({...});

// Get new value based on field type
// For Priority: show P1-P5 options
// For Status: show status options
// For Title: accept free text via "Other"

// Update file
const issuesPath = '.workflow/issues/issues.jsonl';
// Read → Parse → Update → Write
```

## Data Files

| File | Purpose |
|------|---------|
| `.workflow/issues/issues.jsonl` | Active issue records |
| `.workflow/issues/issue-history.jsonl` | Completed issues (archived) |
| `.workflow/issues/solutions/<id>.jsonl` | Solutions per issue |
| `.workflow/issues/queues/index.json` | Queue index (multi-queue) |
| `.workflow/issues/queues/<queue-id>.json` | Individual queue files |

## Error Handling

| Error | Resolution |
|-------|------------|
| No issues found | Suggest `/issue:new` to create |
| Issue not found | Show available issues, re-prompt |
| Write failure | Check file permissions |
| Queue error | Display ccw error message |

## Related Commands

- `/issue:new` - Create structured issue
- `/issue:plan` - Generate solution
- `/issue:queue` - Form execution queue
- `/issue:execute` - Execute tasks
