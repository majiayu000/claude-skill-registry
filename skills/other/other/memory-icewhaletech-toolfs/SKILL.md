---
name: toolfs-memory
description: Persistent key-value storage for session data, conversation context, and agent state. Use this skill when the user requests storing or retrieving memory entries such as "Store this in memory", "Remember this preference", "Recall the previous conversation", or "List all memory entries".
metadata:
  author: toolfs
  version: "1.0.0"
  module: memory
---

# ToolFS Memory

Persistent key-value storage for session data, conversation context, and agent state. Memory entries can store any JSON-serializable data with optional metadata for categorization and organization.

## How It Works

1. **Memory Store**: Stores entries in a key-value format with optional metadata
2. **Session Persistence**: Entries persist across agent sessions
3. **Metadata Support**: Each entry can include metadata for categorization and search
4. **CRUD Operations**: Full create, read, update, delete operations supported

## Usage

### Read Memory Entry

**ToolFS Path:**
```
/toolfs/memory/<entry_id>
```

**Example:**
```json
GET /toolfs/memory/user-preferences-123

// Response
{
  "id": "user-preferences-123",
  "content": "User prefers dark mode and compact layout",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "metadata": {
    "category": "preferences",
    "priority": "high"
  }
}
```

### Write Memory Entry

**ToolFS Path:**
```
/toolfs/memory/<entry_id>
```

**Example:**
```json
PUT /toolfs/memory/conversation-456
Content-Type: application/json

{
  "content": "Discussed ToolFS architecture and skill system",
  "metadata": {
    "topic": "toolfs",
    "participants": ["user", "agent"],
    "timestamp": "2024-01-15T14:20:00Z"
  }
}

// Response
{
  "success": true,
  "message": "Memory entry written"
}
```

### List Memory Entries

**ToolFS Path:**
```
/toolfs/memory
```

**Example:**
```json
LIST /toolfs/memory

// Response
[
  "user-preferences-123",
  "conversation-456",
  "session-state-789"
]
```

## When to Use This Skill

Use Memory skill when you need to:

- **Store Context**: Save conversation summaries, user preferences, or agent state
- **Persist Data**: Keep information across sessions or conversations
- **Organize Information**: Use metadata to categorize and retrieve related entries
- **Recall Information**: Retrieve previously stored data by entry ID

Common use cases:
- "Store this conversation summary in memory"
- "Remember that the user prefers dark mode"
- "Save the current session state"
- "List all stored memories"
- "Retrieve the previous conversation context"

## Entry Structure

Each memory entry contains:

- **id**: Unique identifier for the entry
- **content**: Main content of the entry (string)
- **created_at**: Timestamp when entry was created
- **updated_at**: Timestamp when entry was last updated
- **metadata**: Optional JSON object for additional information

## Output Format

Memory operations return standardized result structures:

```json
{
  "type": "memory",
  "source": "<entry_id>",
  "content": {
    "id": "<entry_id>",
    "content": "...",
    "created_at": "...",
    "updated_at": "...",
    "metadata": {}
  },
  "success": true,
  "error": "error message if failed"
}
```

## Present Results to User

When presenting memory results:

```
✓ Memory entry retrieved

ID: user-preferences-123
Content: User prefers dark mode and compact layout
Category: preferences
Priority: high
Created: 2024-01-15T10:30:00Z
Updated: 2024-01-15T10:30:00Z
```

```
✓ Memory entry stored

ID: conversation-456
Topic: toolfs
Stored successfully at 2024-01-15T14:20:00Z
```

## Troubleshooting

### Entry Not Found

If reading a memory entry fails:

1. Verify the entry ID is correct
2. Check if the entry exists using `LIST /toolfs/memory`
3. Ensure the session has access to memory operations

### Write Permission Error

If writing fails:

1. Verify the session has write permissions
2. Check memory store configuration
3. Ensure entry ID is valid

## Best Practices

1. **Use Descriptive IDs**: Choose meaningful entry IDs for easy retrieval
2. **Include Metadata**: Use metadata for categorization and filtering
3. **Update Timestamps**: The system automatically tracks created_at and updated_at
4. **Organize by Category**: Use metadata.category to group related entries
5. **Regular Cleanup**: Periodically review and clean up old entries

---

*This skill is part of ToolFS. See [main SKILL.md](../SKILL.md) for overview.*

