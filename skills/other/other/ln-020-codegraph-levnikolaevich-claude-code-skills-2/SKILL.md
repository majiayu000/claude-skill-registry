---
name: ln-020-codegraph
description: "Builds and queries code knowledge graph for dependency analysis, references, implementations, and architecture overview. Use when starting work on unfamiliar codebase or before refactoring."
license: MIT
allowed-tools: mcp__hex-graph__index_project, mcp__hex-graph__find_symbols, mcp__hex-graph__inspect_symbol, mcp__hex-graph__trace_paths, mcp__hex-graph__find_references, mcp__hex-graph__find_implementations, mcp__hex-graph__trace_dataflow, mcp__hex-graph__analyze_changes, mcp__hex-graph__analyze_edit_region, mcp__hex-graph__analyze_architecture, mcp__hex-graph__audit_workspace, mcp__hex-line__grep_search, mcp__hex-line__read_file
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
- Before **refactoring** a function/class → `find_symbols` + `inspect_symbol` + `trace_paths`
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
| "Tell me about X" / "Context of X" | `inspect_symbol` | `{ name: "X", file: "...", path: "{project_path}" }` |
| "Project structure" / "Architecture" | `analyze_architecture` | `{ path: "{project_path}", scope?: "src/" }` |
| "Find symbol X" | `find_symbols` | `{ query: "X" }` |
| "Find `app.get(...)` / `router.use(...)` / `server.registerTool(...)` pattern" | `grep_search` | `{ path: "{project_path}", pattern: "app\\.get\\(|router\\.use\\(|server\\.registerTool\\(" }` |
| "Find duplicate code / hotspots / unused exports" | `audit_workspace` | `{ path: "{project_path}", scope?: "src/", verbosity: "full" }` |
| "Circular dependencies / module coupling" | `analyze_architecture` | `{ path: "{project_path}", verbosity: "full" }` |
| "Implementations / overrides" | `find_implementations` | `{ name: "X", file: "...", path: "{project_path}" }` |
| "Dataflow / propagation" | `trace_dataflow` | `{ source: { symbol: { name: "X", file: "..." }, anchor: { kind: "param", name: "input" } }, sink?: { symbol: { name: "X", file: "..." }, anchor: { kind: "return" } }, path: "{project_path}" }` |
| "Review a diff / worktree" | `analyze_changes` | `{ path: "{project_path}", base_ref: "origin/main" }` |
| "Check what editing this range affects" | `analyze_edit_region` | `{ path: "{project_path}", file: "src/file.ts", line_start: 10, line_end: 40 }` |

**Canonical selector rule:** Semantic tools accept exactly one selector:
- `symbol_id`
- `workspace_qualified_name`
- `qualified_name`
- `name` + `file`

**Preferred flow:** use `find_symbols` first, then feed the returned `workspace_qualified_name` into `inspect_symbol`, `trace_paths`, `find_references`, or `find_implementations` for exact follow-up queries.

**Query boundary rule:** `find_symbols` is name-based discovery only. For code fragments like `export function` or unresolved member-call patterns like `app.get(...)`, use `grep_search` instead of treating them as symbols.

**Path rule:** `path` may be the indexed project root or any file/subdirectory inside that indexed project.

**Dataflow anchors:** `trace_dataflow` requires `source.anchor` and optional `sink.anchor`. Use:
- `param` for function parameters
- `local` for local variables
- `return` for function returns
- `property` with `access_path` for bounded property flow

**Precision controls:** `inspect_symbol`, `trace_paths`, and `find_references` support `min_confidence` (`low`, `inferred`, `exact`, `precise`) when the caller wants to suppress weaker parser-only facts.

### Phase 3: Present Results

1. Show MCP tool output directly (markdown tables)
2. For code snippets referenced in results, use `hex-line read_file` with line ranges; add `edit_ready=true, verbosity="full"` only when you intend to carry revision/checksums into an edit
3. Suggest follow-up queries based on results:
   - After `find_symbols` → suggest `inspect_symbol` with `workspace_qualified_name` for the top exact match
   - After `inspect_symbol` → suggest `trace_paths` if refactoring
   - After `trace_paths` → suggest `find_references` or `find_implementations` depending on symbol kind
   - After empty `trace_paths` from a broad or module-level selector → suggest `inspect_symbol` or `analyze_architecture` instead of assuming there are no dependencies

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
