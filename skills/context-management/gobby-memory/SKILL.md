---
name: gobby-memory
description: This skill should be used when the user asks to "/gobby-memory", "remember", "recall", "forget memory". Manage persistent memories across sessions - store, search, delete, update, and list memories.
---

# /gobby-memory - Memory Management Skill

This skill manages persistent memories via the gobby-memory MCP server. Parse the user's input to determine which subcommand to execute.

## Subcommands

### `/gobby-memory remember <content>` - Store a memory
Call `gobby-memory.create_memory` with:
- `content`: (required) The memory content to store
- `memory_type`: Optional type categorization
- `importance`: Importance score 0-1 (default 0.5, use higher for critical facts)
- `tags`: Comma-separated tags (e.g., "testing,security")
- `project_id`: Optional project scope (defaults to current)

Example: `/gobby-memory remember Always use pytest fixtures for test setup`
→ `create_memory(content="Always use pytest fixtures for test setup", tags="testing")`

Example: `/gobby-memory remember [critical] Never commit .env files`
→ `create_memory(content="Never commit .env files", tags="critical,security", importance="0.9")`

### `/gobby-memory recall <query>` - Search/recall memories
Call `gobby-memory.recall_memory` with:
- `query`: Search query text
- `limit`: Max results (default 10)
- `min_importance`: Minimum importance threshold
- `tags_all`: Require all these tags (comma-separated)
- `tags_any`: Match any of these tags
- `tags_none`: Exclude these tags
- `project_id`: Optional project scope

Returns memories matching the query, ranked by relevance.

Example: `/gobby-memory recall testing best practices` → `recall_memory(query="testing best practices")`
Example: `/gobby-memory recall tag:security` → `recall_memory(tags_any="security")`

### `/gobby-memory forget <memory-id>` - Delete a memory
Call `gobby-memory.delete_memory` with:
- `memory_id`: (required) The memory ID to delete

Example: `/gobby-memory forget mm-abc123` → `delete_memory(memory_id="mm-abc123")`

### `/gobby-memory list` - List all memories
Call `gobby-memory.list_memories` with:
- `limit`: Max results (default 20)
- `memory_type`: Filter by type
- `min_importance`: Minimum importance threshold
- `tags_all`: Require all these tags
- `tags_any`: Match any of these tags
- `tags_none`: Exclude these tags
- `project_id`: Optional project scope

Returns all stored memories, most recent first.

Example: `/gobby-memory list` → `list_memories(limit="20")`
Example: `/gobby-memory list tag:workflow` → `list_memories(tags_any="workflow")`

### `/gobby-memory show <memory-id>` - Get memory details
Call `gobby-memory.get_memory` with:
- `memory_id`: (required) The memory ID to retrieve

Returns full memory details including content, tags, importance, and metadata.

Example: `/gobby-memory show mm-abc123` → `get_memory(memory_id="mm-abc123")`

### `/gobby-memory update <memory-id>` - Update a memory
Call `gobby-memory.update_memory` with:
- `memory_id`: (required) The memory ID to update
- `content`: New content (optional)
- `importance`: New importance score (optional)
- `tags`: New tags (optional)

Example: `/gobby-memory update mm-abc123 importance=0.9` → `update_memory(memory_id="mm-abc123", importance="0.9")`

### `/gobby-memory related <memory-id>` - Get related memories
Call `gobby-memory.get_related_memories` with:
- `memory_id`: (required) The memory ID to find relations for
- `limit`: Max results
- `min_similarity`: Minimum similarity threshold

Returns memories related via cross-references.

Example: `/gobby-memory related mm-abc123` → `get_related_memories(memory_id="mm-abc123")`

### `/gobby-memory stats` - Show memory statistics
Call `gobby-memory.memory_stats` to retrieve:
- Total memory count
- Memories by type
- Storage usage
- Recent activity

Example: `/gobby-memory stats` → `memory_stats()`

### `/gobby-memory export` - Export memory graph
Call `gobby-memory.export_memory_graph` with:
- `title`: Optional graph title
- `output_path`: Optional output file path
- `project_id`: Optional project scope

Exports memories as an interactive HTML knowledge graph.

Example: `/gobby-memory export` → `export_memory_graph()`

## Response Format

After executing the appropriate MCP tool, present the results clearly:
- For remember/create: Confirm storage with memory ID
- For recall: List matching memories with ID, content snippet, and relevance
- For forget/delete: Confirm deletion
- For list: Display memories with ID, content, tags, and creation date
- For show: Full memory details
- For update: Confirm update
- For related: List related memories with similarity scores
- For stats: Show statistics in a readable summary
- For export: Confirm export with file path

## Tag Extraction

When storing memories, extract implicit tags from content:
- `[tag]` syntax → explicit tag
- `testing`, `test` → tag: testing
- `security`, `auth` → tag: security
- `workflow`, `process` → tag: workflow
- `code`, `implementation` → tag: code

## Error Handling

If the subcommand is not recognized, show available subcommands:
- remember, recall, forget, list, show, update, related, stats, export
