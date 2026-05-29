---
name: update-dashboard
description: |
  Update the vault Dashboard.md with current system status, recent activity,
  and statistics. Use when the dashboard needs refreshing after processing items
  or on a scheduled basis.
---

# Update Dashboard

Refresh the vault/Dashboard.md with current system state and statistics.

## Workflow

1. **Count items** in each vault folder:
   ```
   Count files in: vault/Inbox/, vault/Needs_Action/, vault/Done/
   ```

2. **Read recent logs** from vault/Logs/ (today's log file)

3. **Read current Dashboard.md** to preserve structure

4. **Update Dashboard.md** with:

### Frontmatter
```yaml
---
last_updated: <current ISO-8601 datetime>
auto_refresh: true
---
```

### Content Structure
```markdown
# AI Employee Dashboard

## Status
- **System Status**: Active
- **Watcher**: File System Watcher - Active
- **Last Check**: <timestamp>

## Pending Actions
<list items from /Needs_Action, or "No pending actions.">

## Recent Activity
<list recent log entries, most recent first, max 10>

## Quick Stats
| Metric | Value |
|--------|-------|
| Items in Inbox | <count> |
| Items Needs Action | <count> |
| Items Done (Today) | <count from today's logs> |
| Items Done (This Week) | <count from this week's logs> |
```

## Important Rules

- Always update the `last_updated` frontmatter field
- Show a maximum of 10 recent activity entries
- Include any pending approval items in the Pending Actions section
- Keep the formatting clean and consistent
