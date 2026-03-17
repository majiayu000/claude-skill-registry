---
name: toolfs-snapshot
description: Create point-in-time snapshots of filesystem state and restore to previous states. Use this skill when the user requests state management such as "Create a snapshot", "Save current state", "Restore previous state", or "Rollback changes".
metadata:
  author: toolfs
  version: "1.0.0"
  module: snapshot
---

# ToolFS Snapshot

Create point-in-time snapshots of filesystem state and restore to previous states. Snapshots enable safe experimentation, rollback capabilities, and state management for ToolFS operations.

## How It Works

1. **Snapshot Creation**: Captures complete filesystem state at a point in time
2. **Copy-on-Write**: Uses efficient copy-on-write mechanisms for storage
3. **State Restoration**: Restores all files and directories to snapshot state
4. **Metadata Tracking**: Maintains metadata about snapshots (size, file count, creation time)

## Usage

### Create Snapshot

**ToolFS Path:**
```
POST /toolfs/snapshots/create
```

**Example:**
```json
POST /toolfs/snapshots/create
Content-Type: application/json

{
  "name": "before-migration-001",
  "description": "Snapshot before database migration"
}

// Response
{
  "success": true,
  "snapshot": {
    "name": "before-migration-001",
    "created_at": "2024-01-15T15:30:00Z",
    "size": 1048576,
    "file_count": 42
  }
}
```

### Rollback Snapshot

**ToolFS Path:**
```
POST /toolfs/snapshots/rollback
```

**Example:**
```json
POST /toolfs/snapshots/rollback
Content-Type: application/json

{
  "name": "before-migration-001"
}

// Response
{
  "success": true,
  "message": "Rolled back to snapshot 'before-migration-001'",
  "files_restored": 42,
  "rollback_time": "2024-01-15T16:00:00Z"
}
```

### List Snapshots

**ToolFS Path:**
```
GET /toolfs/snapshots
```

**Example:**
```json
GET /toolfs/snapshots

// Response
{
  "snapshots": [
    {
      "name": "before-migration-001",
      "created_at": "2024-01-15T15:30:00Z",
      "size": 1048576,
      "file_count": 42
    },
    {
      "name": "initial-state",
      "created_at": "2024-01-15T10:00:00Z",
      "size": 512000,
      "file_count": 25
    }
  ]
}
```

### Get Snapshot Metadata

**ToolFS Path:**
```
GET /toolfs/snapshots/<name>
```

**Example:**
```json
GET /toolfs/snapshots/before-migration-001

// Response
{
  "name": "before-migration-001",
  "created_at": "2024-01-15T15:30:00Z",
  "size": 1048576,
  "file_count": 42,
  "base_snapshot": "initial-state",
  "changes_since_base": 17
}
```

### Delete Snapshot

**ToolFS Path:**
```
DELETE /toolfs/snapshots/<name>
```

**Example:**
```json
DELETE /toolfs/snapshots/old-snapshot-001

// Response
{
  "success": true,
  "message": "Snapshot 'old-snapshot-001' deleted"
}
```

## When to Use This Skill

Use Snapshot skill when you need to:

- **Safe Experimentation**: Create snapshots before making major changes
- **Rollback Capability**: Restore to a known good state
- **State Management**: Track filesystem state over time
- **Recovery**: Recover from errors or unwanted changes
- **Testing**: Test changes with ability to revert

Common use cases:
- "Create a snapshot before making changes"
- "Save the current state"
- "Restore to the previous snapshot"
- "Rollback all changes"
- "List all available snapshots"

## Snapshot Lifecycle

1. **Create**: Capture current filesystem state
2. **Use**: Continue working; snapshot remains unchanged
3. **Rollback**: Restore filesystem to snapshot state
4. **Delete**: Remove snapshot when no longer needed

## Snapshot Metadata

Each snapshot includes:

- **name**: Unique identifier for the snapshot
- **created_at**: Timestamp when snapshot was created
- **size**: Size of snapshot in bytes
- **file_count**: Number of files in snapshot
- **base_snapshot**: Parent snapshot (if using copy-on-write)
- **changes_since_base**: Number of changes from base snapshot

## Output Format

Snapshot operations return standardized result structures:

```json
{
  "type": "snapshot",
  "source": "/toolfs/snapshots/<name>",
  "content": {
    "name": "...",
    "created_at": "...",
    "size": 0,
    "file_count": 0
  },
  "success": true,
  "error": "error message if failed"
}
```

## Present Results to User

When presenting snapshot results:

```
✓ Snapshot created successfully

Name: before-migration-001
Created: 2024-01-15T15:30:00Z
Files: 42
Size: 1.0 MB
Description: Snapshot before database migration
```

```
✓ Rollback completed

Restored to: before-migration-001
Files restored: 42
Rollback time: 2024-01-15T16:00:00Z
```

```
Available snapshots (2):

1. before-migration-001
   Created: 2024-01-15T15:30:00Z
   Files: 42 | Size: 1.0 MB

2. initial-state
   Created: 2024-01-15T10:00:00Z
   Files: 25 | Size: 500 KB
```

## Troubleshooting

### Snapshot Creation Fails

If snapshot creation fails:

1. Check available disk space
2. Verify snapshot name doesn't already exist
3. Ensure filesystem state is valid
4. Check for file system errors

### Rollback Fails

If rollback fails:

1. Verify snapshot exists before rollback
2. Check filesystem permissions
3. Ensure no files are locked or in use
4. Verify filesystem state is valid

### Snapshot Not Found

If snapshot operations fail:

1. Verify snapshot name is correct
2. List snapshots to see available names
3. Check if snapshot was deleted
4. Ensure snapshot exists in the system

## Best Practices

1. **Snapshot Before Major Changes**: Always create snapshots before significant modifications
2. **Descriptive Names**: Use meaningful snapshot names (e.g., "before-migration-001")
3. **Regular Cleanup**: Delete old snapshots to save storage space
4. **Document Snapshots**: Use descriptions to explain snapshot purpose
5. **Verify Before Rollback**: Check snapshot metadata before rollback operations

## Copy-on-Write Optimization

ToolFS uses copy-on-write for efficient snapshot storage:

- **Base Snapshots**: First snapshot stores complete state
- **Incremental Snapshots**: Later snapshots only store changes
- **Space Efficient**: Reduces storage requirements significantly
- **Fast Restoration**: Quick rollback through delta application

---

*This skill is part of ToolFS. See [main SKILL.md](../SKILL.md) for overview.*

