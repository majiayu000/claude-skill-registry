---
name: ln-020-codegraph
description: "Builds and queries code knowledge graph for dependency analysis, references, implementations, and architecture overview. Use when starting work on unfamiliar codebase or before refactoring."
license: MIT
allowed-tools: mcp__hex-graph__index_project, mcp__hex-graph__watch_project, mcp__hex-graph__search_symbols, mcp__hex-graph__get_symbol, mcp__hex-graph__trace_paths, mcp__hex-graph__find_references, mcp__hex-graph__find_implementations, mcp__hex-graph__find_dataflows, mcp__hex-graph__explain_resolution, mcp__hex-graph__get_architecture, mcp__hex-graph__find_clones, mcp__hex-graph__find_hotspots, mcp__hex-graph__find_unused_exports, mcp__hex-graph__find_cycles, mcp__hex-graph__get_module_metrics
---

> **Paths:** File paths are relative to skills repo root.

# Code Knowledge Graph

**Type:** Standalone Utility
**Category:** 0XX Dev Environment

Indexes codebase into a layered graph (tree-sitter AST → SQLite) and provides dependency analysis, path tracing, references, implementations, and architecture overview via MCP tools.

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `project_path` | yes | args or CWD | Project root to index |
| `command` | no | args | Specific action: `index`, `search`, `symbol`, `paths`, `refs`, `arch` |

## When to Use

- Starting work on an **unfamiliar codebase** → `index` + `architecture`
- Before **refactoring** a function/class → `search` + `get_symbol` + `trace_paths`
- Understanding **call flow** → `trace_paths`
- Finding a **symbol** quickly → `search`

## Workflow

### Phase 1: Index

Check if graph exists (`.hex-skills/codegraph/index.db` in project root).

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
| "Show dependencies" / "What uses X?" | `trace_paths` | `{ name: "X", file: "...", path_kind: "mixed", direction: "reverse", path: "{project_path}" }` |
| "Who calls X?" / "What does X call?" | `trace_paths` | `{ name: "X", file: "...", path_kind: "calls", direction: "reverse"\|"forward", path: "{project_path}" }` |
| "Tell me about X" / "Context of X" | `get_symbol` | `{ name: "X", file: "...", path: "{project_path}" }` |
| "Project structure" / "Architecture" | `get_architecture` | `{ path: "{project_path}", scope?: "src/" }` |
| "Find symbol X" | `search_symbols` | `{ query: "X" }` |
| "Watch for changes" | `watch_project` | `{ path: "{project_path}" }` |
| "Find duplicate code" | `find_clones` | `{ path: "{project_path}", type: "all" }` |
| "Risky hotspots" | `find_hotspots` | `{ path: "{project_path}", min_callers: 2, min_complexity: 5 }` |
| "Unused exports" | `find_unused_exports` | `{ path: "{project_path}" }` |
| "Circular dependencies" | `find_cycles` | `{ path: "{project_path}" }` |
| "Module coupling" | `get_module_metrics` | `{ path: "{project_path}", min_coupling: 0 }` |
| "Implementations / overrides" | `find_implementations` | `{ name: "X", file: "...", path: "{project_path}" }` |
| "Dataflow / propagation" | `find_dataflows` | `{ name: "X", file: "...", path: "{project_path}", depth: 2 }` |

**Canonical selector rule:** Semantic tools accept exactly one selector:
- `symbol_id`
- `workspace_qualified_name`
- `qualified_name`
- `name` + `file`

**Preferred flow:** use `search_symbols` first, then feed the returned `workspace_qualified_name` into `get_symbol`, `trace_paths`, `find_references`, or `find_implementations` for exact follow-up queries.

**Precision controls:** `get_symbol`, `trace_paths`, and `find_references` support `min_confidence` (`low`, `inferred`, `exact`, `precise`) when the caller wants to suppress weaker parser-only facts.

### Phase 3: Present Results

1. Show MCP tool output directly (markdown tables)
2. For code snippets referenced in results, use `hex-line read_file` with line ranges
3. Suggest follow-up queries based on results:
   - After `search_symbols` → suggest `get_symbol` with `workspace_qualified_name` for the top exact match
   - After `get_symbol` → suggest `trace_paths` if refactoring
   - After `trace_paths` → suggest `find_references` or `find_implementations` depending on symbol kind

## Supported Languages

| Language | Extensions | Coverage |
|---|---|---|
| JavaScript | .js, .mjs, .cjs, .jsx | Strongest semantic coverage |
| TypeScript / TSX | .ts, .tsx | Strongest semantic coverage |
| Python | .py | Workspace-aware definitions, calls, imports, unused exports; optional precise overlay when provider is installed |
| C# | .cs | Workspace-aware definitions, calls, project/namespace ownership, type relations; optional precise overlay when provider is installed |
| PHP | .php | Workspace-aware definitions, calls, PSR-4 namespace imports, unused exports; optional precise overlay when provider is installed |

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
