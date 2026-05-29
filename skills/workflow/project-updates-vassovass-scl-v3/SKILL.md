---
name: project-updates
description: How to update roadmap, changelog, and Kanban when completing features. Use after finishing any feature, bug fix, or improvement to ensure proper documentation and tracking. Keywords: changelog, roadmap, kanban, feedback, documentation, completion, tracking, MCP.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.1"
  project: "stepleague"
---

# Project Updates Skill

## Overview

**MANDATORY:** Every completed feature must be tracked in:

1. **CHANGELOG.md** - What changed (file)
2. **Roadmap/Kanban** - Feature status (database via API or MCP)
3. **AGENTS.md** - If it's a key pattern (optional, file)

---

## The Feedback/Roadmap/Kanban System

StepLeague has a modular system for tracking features and feedback:

| Component | Purpose | Table | Public Page |
|-----------|---------|-------|-------------|
| **Feedback** | User-submitted issues and ideas | `feedback` | `/feedback` |
| **Roadmap** | Public feature timeline | `feedback` (filtered) | `/roadmap` |
| **Kanban** | Internal task tracking | `feedback` (admin view) | `/admin/kanban` |

**Key insight:** These share the same `feedback` table but are filtered by `board_status` and `is_public`.

---

## 1. Updating CHANGELOG.md

### Location
`CHANGELOG.md` in project root

### Format

```markdown
## [Date] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Modified behavior description

### Fixed
- Bug fix description

### Removed
- Removed feature description
```

---

## 2. Updating via API (Preferred for Code)

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/agent/current-work` | POST | Mark feature as in-progress |
| `/api/agent/current-work` | DELETE | Clear in-progress flag |
| `/api/admin/kanban` | POST | Create new kanban item |
| `/api/admin/kanban` | PUT | Update existing item |
| `/api/admin/kanban` | GET | List kanban items |
| `/api/admin/feedback` | GET/POST/PUT | Feedback management |

### Step 1: When Starting Work

```typescript
await fetch("/api/agent/current-work", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    subject: "Feature Name",
    description: "What you are building",
    type: "feature"  // or "improvement", "bug"
  })
});
```

### Step 2: When Completing Work

```typescript
// Clear current work flag
await fetch("/api/agent/current-work", { method: "DELETE" });

// Mark kanban item as done
await fetch("/api/admin/kanban", {
  method: "PUT",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    id: "<existing-kanban-item-id>",
    board_status: "done",
    completed_at: "2026-01-16"  // Current date YYYY-MM-DD!
  })
});
```

---

## 3. Updating via Supabase MCP (Preferred for Verification)

Use the Supabase MCP to directly query and update the database.

### Reference the `supabase-patterns` skill for MCP usage.

### Verify Current State

```
// Check existing feedback/kanban items
mcp_supabase-mcp-server_execute_sql({
  project_id: "your-project-id",
  query: `
    SELECT id, subject, board_status, completed_at 
    FROM feedback 
    WHERE subject ILIKE '%feature name%'
    LIMIT 5
  `
})
```

### Create New Item via MCP

```
mcp_supabase-mcp-server_execute_sql({
  project_id: "your-project-id",
  query: `
    INSERT INTO feedback (subject, description, type, board_status, is_public)
    VALUES (
      'Skills System Implementation',
      'Created 8 agent skills for improved AI assistance',
      'feature',
      'done',
      true
    )
    RETURNING id, subject, board_status
  `
})
```

### Update Existing Item via MCP

```
mcp_supabase-mcp-server_execute_sql({
  project_id: "your-project-id",
  query: `
    UPDATE feedback 
    SET board_status = 'done', 
        completed_at = '2026-01-16'
    WHERE id = 'item-uuid-here'
    RETURNING id, subject, board_status, completed_at
  `
})
```

### Verify Update Applied

```
mcp_supabase-mcp-server_execute_sql({
  project_id: "your-project-id",
  query: `
    SELECT id, subject, board_status, completed_at 
    FROM feedback 
    WHERE id = 'item-uuid-here'
  `
})
```

---

## 4. Verification Checklist

After updating, **verify the changes were applied:**

### Via MCP (Recommended)

```
// Check the item was updated
mcp_supabase-mcp-server_execute_sql({
  project_id: "your-project-id",
  query: `
    SELECT id, subject, board_status, completed_at, updated_at
    FROM feedback
    WHERE board_status = 'done'
    ORDER BY completed_at DESC
    LIMIT 5
  `
})
```

### Via API

```typescript
const response = await fetch("/api/admin/kanban?status=done");
const { items } = await response.json();
// Verify your item is in the list
```

---

## Database Schema Reference

### `feedback` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | Primary key |
| `subject` | text | Title/name of item |
| `description` | text | Detailed description |
| `type` | text | 'feature', 'bug', 'improvement', 'question' |
| `board_status` | text | 'backlog', 'now', 'next', 'later', 'future', 'done' |
| `is_public` | boolean | Shown on public roadmap |
| `completed_at` | date | When marked done |
| `priority` | text | 'low', 'medium', 'high', 'critical' |
| `votes` | integer | User vote count |
| `created_at` | timestamp | Creation time |
| `updated_at` | timestamp | Last update time |

### Board Status Values

| Status | Column on Roadmap | Description |
|--------|-------------------|-------------|
| `backlog` | Hidden | Not started |
| `now` | Now (with glow if agent working) | In progress |
| `next` | Next | Coming soon |
| `later` | Later | Planned |
| `future` | Future | Ideas |
| `done` | Completed section | Finished |

---

## 5. Complete Workflow

### Example: Completing "Proxy Claim" Feature

#### 1. Update CHANGELOG.md (file)

```markdown
## [2026-01-16]

### Added
- Proxy profile claiming via unique invite codes
- Profile switcher for "Act As" functionality
```

#### 2. Clear Current Work (API)

```typescript
await fetch("/api/agent/current-work", { method: "DELETE" });
```

#### 3. Mark as Done (MCP - with verification)

```
// First, find the item
mcp_supabase-mcp-server_execute_sql({
  query: "SELECT id, subject FROM feedback WHERE subject ILIKE '%proxy%claim%' LIMIT 5"
})

// Update it
mcp_supabase-mcp-server_execute_sql({
  query: `
    UPDATE feedback 
    SET board_status = 'done', completed_at = '2026-01-16'
    WHERE id = 'found-uuid'
    RETURNING id, subject, board_status, completed_at
  `
})

// Verify
mcp_supabase-mcp-server_execute_sql({
  query: "SELECT * FROM feedback WHERE id = 'found-uuid'"
})
```

#### 4. Update AGENTS.md Recent Features (file)

```markdown
### 2026-01-16

- ✅ **Proxy Claim System** (PRD 41)
  - Unique invite codes for proxy profiles
  - "Act As" context switching
```

---

## Common Issues

| Problem | Solution |
|---------|----------|
| Item not found | Search with ILIKE and wildcards |
| MCP timeout | Add LIMIT to queries |
| Update didn't apply | Check for typos in UUID, verify with SELECT |
| Duplicate entries | Search before creating new |

---

## Checklist Before Considering Work Complete

- [ ] CHANGELOG.md updated with all changes
- [ ] Current work flag cleared (`DELETE /api/agent/current-work`)
- [ ] Kanban item marked as done (verified via MCP or API)
- [ ] AGENTS.md updated if adding key patterns
- [ ] TypeScript build passes (`npx tsc --noEmit`)
- [ ] Code committed with descriptive message

---

## Related Skills

- `supabase-patterns` - MCP usage and database operations
- `prd-creation` - PRDs should reference kanban items
- `architecture-philosophy` - Document new patterns in AGENTS.md
