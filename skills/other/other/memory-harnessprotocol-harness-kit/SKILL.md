---
name: memory
description: Use when user invokes /memory with a subcommand (search, trace, add, episode, status). Also triggers on "search my memory for X", "add to memory", "what do I know about X" (when membrain is available), "memory status", "memory trace". Searches and manages the membrain knowledge graph via MCP tools or HTTP API.
---

# membrain Memory

## Overview

Interface with the membrain knowledge graph — search entities, trace BFS traversals, add observations, create episodes, and check graph health.

**Graceful degradation:** If membrain MCP tools are not available, print install instructions and exit. If the HTTP server is not running, skip HTTP-dependent subcommands and say so.

## Subcommands

Parse the argument after `/memory` to determine which operation to run.

| Invocation | Operation |
|-----------|-----------|
| `/memory search <topic>` | Search the graph for entities matching the topic |
| `/memory trace <query>` | Run BFS traversal and display token savings |
| `/memory add <entity> <observation>` | Add an observation to an existing entity |
| `/memory episode <text>` | Create a timestamped episode from free text |
| `/memory status` | Show graph statistics (entity/relation counts) |
| `/memory` (no args) | Show usage and subcommand list |

---

## Step 1: Check MCP Availability

Before any graph operation, confirm membrain MCP tools are available.

**Test:** Can you call `search_nodes`? If the tool is missing from the tool list:
```
membrain MCP tools are not connected.

To connect them:
  1. Install mem: go install github.com/siracusa5/membrain/cmd/mem@latest
  2. Add to Claude Code settings (or via /plugin install membrain@harness-kit):
     {
       "mcpServers": {
         "membrain": { "command": "mem", "args": ["mcp"] }
       }
     }
  3. Restart Claude Code

For the desktop UI: mem serve   (opens http://localhost:3131)
```

---

## Step 2: Route to Subcommand

### `search <topic>`

Search the graph for entities and relations related to the topic.

1. Call `search_nodes` with the topic as the query
2. If results < 3, try decomposing the topic into individual keywords and search each (max 2 additional calls)
3. Format results:

```
## Memory: "<topic>"

Found N entities  ·  saved X% tokens vs full graph dump

### <EntityName> (Type)
- observation 1
- observation 2
- observation 3

### <EntityName> (Type)
...

Relations: A → relationType → B
```

**Caps:** Max 10 entities shown. Max 3 observations per entity. Max 3 `search_nodes` calls.

If no results: *"No entities found for '[topic]'. Try a broader term or check `/memory status` to confirm the graph has data."*

---

### `trace <query>`

Run a BFS traversal to show how topics connect through the graph.

**Requires:** membrain server running on `http://localhost:3131`

1. Call `GET http://localhost:3131/api/v1/trace?focus=<query>` (URL-encode the query)
2. Parse the response — it includes traversal frames and token stats
3. Display:

```
## Trace: "<query>"

Traversal: N nodes  ·  depth D  ·  saved X% vs full dump

Starting node → relation → Node B → relation → Node C
                                               → relation → Node D
...

Token savings: retrieved ~X tokens of ~Y total (Z% saved)

Open in browser: http://localhost:3131/trace?focus=<query>
```

If the server is not running:
*"membrain server is not running. Start it with: mem serve"*

---

### `add <entity> <observation>`

Add an observation to an existing entity in the graph.

Parse the argument: everything before the first quoted string or `:` is the entity name; the rest is the observation.

Examples:
- `/memory add Claude "ships membrain MCP integration"` → entity: Claude, obs: ships membrain MCP integration
- `/memory add Claude: ships membrain MCP integration` → same

1. Call `add_observations` with:
   ```json
   [{ "entityName": "<entity>", "contents": ["<observation>"] }]
   ```
2. On success: *"Added observation to **<entity>**."*
3. If entity not found: *"Entity '<entity>' not found. Create it first with `create_entities` or use `/memory episode` to capture a session."*

---

### `episode <text>`

Create a timestamped episode capturing a chunk of session knowledge.

1. Extract a short name from the text (first sentence or ≤60 chars)
2. Scan the text for entity names that exist in the graph (use recent `search_nodes` results if available)
3. Call `add_episode` with:
   ```json
   {
     "name": "<short-name> (YYYY-MM-DD)",
     "summary": "<full text>",
     "occurred_at": "<current ISO timestamp>",
     "mentioned_entities": ["Entity1", "Entity2"]
   }
   ```
   `mentioned_entities` auto-links the episode to existing graph entities — always include them when identifiable.
3. On success: *"Episode created: **<name>**"*

---

### `status`

Show graph health and statistics.

**Requires:** membrain server running on `http://localhost:3131`

1. Call `GET http://localhost:3131/api/v1/graph/stats`
2. Display:

```
## membrain Status

Entities:  N
Relations: N
Episodes:  N

Server:    http://localhost:3131  ✓
Graph:     <path to graph file>

Desktop UI:  http://localhost:3131/
```

If server not running: note that the server is offline and MCP-only stats are not available (membrain does not support entity count queries via MCP without the HTTP server).

---

### No args

Print usage:
```
## /memory — membrain knowledge graph

  /memory search <topic>          search entities
  /memory trace <query>           BFS traversal with token stats
  /memory add <entity> <obs>      add an observation
  /memory episode <text>          create timestamped episode
  /memory status                  graph health and counts
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Calling `read_graph` | NEVER. Use `search_nodes` for all queries. |
| Treating entity name as case-sensitive | membrain names are case-sensitive — match exact name from prior search results |
| Running HTTP calls when server might be down | Always note if server is unreachable; MCP tools still work offline |
| Showing raw JSON | Format output as human-readable markdown |
| Exceeding search caps | Max 3 `search_nodes` calls per `/memory search` invocation |
