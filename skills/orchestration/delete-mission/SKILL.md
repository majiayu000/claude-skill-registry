---
name: delete-mission
version: "1.0.0"
description: >
  Permanently delete a background mission and all its run history. This action
  cannot be undone. Use when the user explicitly asks to delete or remove a
  mission. Always confirm with the user before deleting.
  Keywords: mission, delete, remove, cancel, destroy, permanently.
metadata:
  domain: general
  category: missions
  requires-approval: true
  confidence: 0.95
  mcp-servers: []
---

# Delete Mission

Permanently deletes a background mission and all its run history.

## Preconditions

- A mission ID or title is provided
- The mission exists and belongs to the current user
- User has explicitly confirmed the deletion

## Actions

### 1. Resolve Mission ID

Fetch the mission to confirm it exists and show the user what they are deleting.

### 2. Confirm with User

Before deleting, always confirm:

```
⚠️  Are you sure you want to delete **Cluster health monitor** (mission-abc123)?

This will permanently remove the mission and all 47 run records.
This action cannot be undone.

Reply "yes" to confirm or "no" to cancel.
```

### 3. Delete the Mission

Only proceed after explicit confirmation:

```python
result = await temporal_client.execute_activity(
    "delete_mission_activity",
    {
        "mission_id": mission_id,
        "user_id": user_id,
    }
)
```

### 4. Confirm to User

```
🗑️  Mission deleted: **Cluster health monitor** (mission-abc123)

The mission and all its run history have been permanently removed.
```

## Success Criteria

- [ ] User confirmed the deletion
- [ ] Mission and run history deleted from database
- [ ] User receives confirmation

## Failure Handling

- If mission not found: inform the user
- If user cancels: acknowledge and do nothing

## Examples

**User:** "Delete the cluster health monitor"
**User:** "Remove mission mission-abc123"
**User:** "Cancel my daily news digest permanently"
