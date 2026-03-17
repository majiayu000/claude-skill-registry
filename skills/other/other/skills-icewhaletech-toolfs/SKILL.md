---
name: toolfs
description: Unified virtual filesystem framework for LLM agents. Provides access to files, memory, RAG, skills, and snapshots through a single interface. Use this skill when the user requests file operations, memory storage, semantic search, skill execution, or state management tasks.
metadata:
  author: toolfs
  version: "1.0.0"
---

# ToolFS

ToolFS is a unified virtual filesystem framework for LLM agents that provides access to files, memory, RAG systems, skills, and snapshots through a single `/toolfs` namespace.

## Overview

ToolFS integrates multiple data sources and operations into one virtual filesystem:

- **Memory**: Persistent key-value storage for session data and context
- **RAG**: Semantic search over vector databases for document retrieval  
- **Filesystem**: Access to mounted local directories
- **Skills**: Execute WASM-based skills mounted to virtual paths
- **Snapshots**: Create point-in-time snapshots and restore previous states

All operations respect session isolation, permission control, and audit logging for safe execution in sandboxed environments.

## Available Skills

ToolFS is organized into functional modules. Each module provides specific capabilities:

| Module | Path | Description | Documentation |
|--------|------|-------------|---------------|
| **Memory** | `/toolfs/memory` | Persistent storage for session data and context | [Memory Skill](memory/SKILL.md) |
| **RAG** | `/toolfs/rag` | Semantic search over vector databases | [RAG Skill](rag/SKILL.md) |
| **Filesystem** | `/toolfs/<mount>` | Access to mounted local directories | [Filesystem Skill](filesystem/SKILL.md) |
| **Code** | `/toolfs/<skill>` | Execute WASM or native skills | [Code Skill](code/SKILL.md) |
| **Snapshots** | `/toolfs/snapshots` | Filesystem state snapshots and rollback | [Snapshot Skill](snapshot/SKILL.md) |

## Quick Start

### Memory Operations
```bash
# Read memory entry
GET /toolfs/memory/<entry_id>

# Write memory entry  
PUT /toolfs/memory/<entry_id>

# List memory entries
LIST /toolfs/memory
```

See [Memory Skill](memory/SKILL.md) for details.

### RAG Search
```bash
# Semantic search
GET /toolfs/rag/query?text=<query>&top_k=<number>
```

See [RAG Skill](rag/SKILL.md) for details.

### Filesystem Access
```bash
# Read file
GET /toolfs/<mount_point>/<relative_path>

# Write file
PUT /toolfs/<mount_point>/<relative_path>

# List directory
LIST /toolfs/<mount_point>/<relative_path>
```

See [Filesystem Skill](filesystem/SKILL.md) for details.

### Skill Execution
```bash
# Execute skill
GET /toolfs/<skill_mount_path>?text=<query>
```

See [Skill Skill](skill/SKILL.md) for details.

### Snapshot Management
```bash
# Create snapshot
POST /toolfs/snapshots/create

# Rollback snapshot
POST /toolfs/snapshots/rollback

# List snapshots
GET /toolfs/snapshots
```

See [Snapshot Skill](snapshot/SKILL.md) for details.

## Skill API (Chained Operations)

Chain multiple operations in a single request:

```json
POST /toolfs/skills/chain
Content-Type: application/json

{
  "operations": [
    {
      "type": "search_memory",
      "query": "user preferences"
    },
    {
      "type": "search_rag",
      "query": "ToolFS configuration",
      "top_k": 5
    },
    {
      "type": "read_file",
      "path": "/toolfs/data/config/settings.json"
    }
  ]
}
```

## Common Use Cases

- **File Operations**: "Read the config file from the project directory"
- **Memory Persistence**: "Store this conversation summary in memory"
- **Semantic Search**: "Search documents for information about X"
- **Skill Execution**: "Execute the RAG skill to find relevant content"
- **State Management**: "Create a snapshot before making changes"
- **Recovery**: "Restore the previous state"

## Output Format

All operations return standardized result structures:

```json
{
  "type": "memory|rag|file|skill|snapshot",
  "source": "identifier (ID, path, command, skill_name)",
  "content": "string content or data",
  "metadata": {},
  "success": true|false,
  "error": "error message if failed"
}
```

## Error Handling

Errors are returned with structured responses:

```json
{
  "success": false,
  "error": "Detailed error message",
  "type": "error_type",
  "source": "operation_identifier"
}
```

Common error types:
- `access_denied`: Session does not have permission
- `not_found`: Resource not found
- `skill_error`: Skill execution failed
- `validation_error`: Invalid input parameters
- `filesystem_error`: Filesystem operation failed

## Best Practices

1. **Use Sessions**: Always create sessions with appropriate `allowed_paths` for security
2. **Chain Operations**: Use `ChainOperations` to minimize round trips
3. **Snapshot Before Changes**: Create snapshots before major filesystem modifications
4. **Handle Errors**: Check `success` field in results and provide fallback strategies
5. **Leverage Metadata**: Use metadata fields to pass context between operations

## Module Documentation

For detailed information about each module, see:

- [Memory Skill](memory/SKILL.md) - Persistent storage operations
- [RAG Skill](rag/SKILL.md) - Semantic search operations
- [Filesystem Skill](filesystem/SKILL.md) - File and directory operations
- [Skill Skill](skill/SKILL.md) - Skill execution and management
- [Snapshot Skill](snapshot/SKILL.md) - State management operations

---

*This documentation describes ToolFS version 1.0.0. Each module has its own detailed SKILL.md for specific operations.*
