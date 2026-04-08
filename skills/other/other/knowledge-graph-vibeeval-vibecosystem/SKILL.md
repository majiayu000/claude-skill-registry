---
name: knowledge-graph
description: "Knowledge graph integration for token-efficient codebase understanding. Uses codebase-memory MCP for AST indexing, dependency graphs, and smart context selection. 6-71x token savings vs raw file reading."
---

# Knowledge Graph Integration

## Overview

Transform any codebase into a queryable knowledge graph using codebase-memory MCP server. Instead of reading entire files, query the graph for exactly the context you need.

**Token savings:** 6-71x reduction compared to raw file reading.

## Setup

### Prerequisites
- codebase-memory MCP server installed (`~/bin/codebase-memory-mcp` or via npm)
- MCP config in `~/.mcp.json`:
```json
{
  "mcpServers": {
    "codebase-memory": {
      "command": "/path/to/codebase-memory-mcp",
      "args": []
    }
  }
}
```

## Core Operations

### 1. Index a Repository
```
mcp__codebase-memory__index_repository
  project_name: "my-project"
  repo_path: "/path/to/repo"
```
First index takes 30-120s depending on repo size. Subsequent updates are incremental.

### 2. Check Index Status
```
mcp__codebase-memory__index_status
  project_name: "my-project"
```

### 3. Search Code
```
mcp__codebase-memory__search_code
  project_name: "my-project"
  query: "authentication middleware"
```
Returns relevant code snippets without reading entire files.

### 4. Get Architecture Overview
```
mcp__codebase-memory__get_architecture
  project_name: "my-project"
```
Returns high-level architecture: modules, dependencies, entry points.

### 5. Trace Call Paths
```
mcp__codebase-memory__trace_call_path
  project_name: "my-project"
  from_symbol: "handleLogin"
  to_symbol: "validateToken"
```

### 6. Query Dependency Graph
```
mcp__codebase-memory__query_graph
  project_name: "my-project"
  query: "what depends on auth module?"
```

## When to Use

| Scenario | Without Graph | With Graph |
|----------|--------------|------------|
| Code review | Read all changed files + imports | Query impact of changes |
| Bug investigation | Read 10-20 files manually | Trace call path to bug |
| Refactoring | Read entire module | Query all dependents |
| Architecture review | Read project top-down | Get architecture overview |

## Integration with Agents

### code-reviewer
Before reviewing, query the graph for the blast radius of changes:
```
search_code("functions that call {changed_function}")
```

### architect
Get architecture overview before proposing changes:
```
get_architecture("project")
```

### sleuth
Trace call paths to understand bug propagation:
```
trace_call_path("buggy_function", "entry_point")
```

## Token Savings Examples

| Operation | Raw Reading | Graph Query | Savings |
|-----------|-----------|-------------|---------|
| Find all callers of function | ~50K tokens | ~700 tokens | 71x |
| Architecture overview | ~200K tokens | ~3K tokens | 67x |
| Impact analysis for PR | ~30K tokens | ~2K tokens | 15x |
| Find related tests | ~20K tokens | ~1.5K tokens | 13x |
