---
name: ln-020-codegraph
description: "Builds and queries code knowledge graph for dependency analysis, impact checking, and architecture overview. Use when starting work on unfamiliar codebase or before refactoring."
license: MIT
allowed-tools: mcp__hex-graph__index_project, mcp__hex-graph__search_symbols, mcp__hex-graph__get_impact, mcp__hex-graph__trace_calls, mcp__hex-graph__get_context, mcp__hex-graph__get_architecture, mcp__hex-graph__watch_project
---

> **Paths:** File paths are relative to skills repo root.

# Code Knowledge Graph

**Type:** Standalone Utility
**Category:** 0XX Dev Environment

Indexes codebase into a knowledge graph (tree-sitter AST → SQLite) and provides dependency analysis, impact checking, and architecture overview via MCP tools.

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `project_path` | yes | args or CWD | Project root to index |
| `command` | no | args | Specific action: `index`, `impact`, `trace`, `context`, `architecture`, `search` |

## When to Use

- Starting work on an **unfamiliar codebase** → `index` + `architecture`
- Before **refactoring** a function/class → `impact` + `context`
- Understanding **call flow** → `trace`
- Finding a **symbol** quickly → `search`

## Workflow

### Phase 1: Index

Check if graph exists (`.codegraph/index.db` in project root).

**If NOT exists:**
```
Call: index_project({ path: "{project_path}" })
```

**If exists** (re-index on demand):
```
Call: index_project({ path: "{project_path}" })
```
Idempotent — skips unchanged files automatically.

### Phase 2: Query

Route based on user intent:

| User says | Tool | Parameters |
|---|---|---|
| "Show dependencies" / "What uses X?" | `get_impact` | `{ symbol: "X" }` |
| "Who calls X?" / "What does X call?" | `trace_calls` | `{ symbol: "X", direction: "callers"\|"callees" }` |
| "Tell me about X" / "Context of X" | `get_context` | `{ symbol: "X" }` |
| "Project structure" / "Architecture" | `get_architecture` | `{ path?: "src/" }` |
| "Find symbol X" | `search_symbols` | `{ query: "X" }` |
| "Watch for changes" | `watch_project` | `{ path: "{project_path}" }` |

### Phase 3: Present Results

1. Show MCP tool output directly (markdown tables)
2. For code snippets referenced in results, use `hex-line read_file` with line ranges
3. Suggest follow-up queries based on results:
   - After `search` → suggest `get_context` for top result
   - After `get_context` → suggest `get_impact` if refactoring
   - After `get_impact` → list files in blast radius for review

## Supported Languages

| Language | Extensions | Call Edges |
|---|---|---|
| JavaScript | .js, .mjs, .cjs, .jsx | Yes (import-aware) |
| TypeScript | .ts, .tsx | Yes (import-aware) |
| Python | .py | Yes (import-aware) |
| C# | .cs | Definitions + imports |
| PHP | .php | Definitions + imports |

## MCP Server Setup

Add to `.mcp.json`:
```json
{
  "mcpServers": {
    "hex-graph": {
      "command": "node",
      "args": ["{skills_repo}/mcp/hex-graph-mcp/server.mjs"]
    }
  }
}
```

## Definition of Done

- [ ] Project indexed (index_project returns success)
- [ ] Query results shown to user
- [ ] Follow-up suggestions provided

---
**Version:** 0.1.0
**Last Updated:** 2026-03-20
