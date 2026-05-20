---
name: graph-query
description: Queries the code graph database to understand component relationships, dependencies, and the impact of changes. Use when the user asks to "find callers", "check dependencies", "what uses this", or when exploring codebase structure to avoid breaking changes.
allowed-tools: Bash
compatibility: Requires AI Maestro (aimaestro.dev) with Bash shell access
metadata:
  author: 23blocks
  version: 1.0.0
---

# AI Maestro Code Graph Query

## CRITICAL: AUTOMATIC BEHAVIOR - READ THIS FIRST

**THIS IS NOT OPTIONAL. THIS IS YOUR DEFAULT BEHAVIOR.**

Every time you use the `Read` tool on a code file, you MUST IMMEDIATELY query the graph to understand:
- What is this component/function?
- What depends on it? (callers, serializers, child classes)
- What does it depend on? (callees, parent classes, associations)

**DO NOT:**
- Wait for the user to ask you to query the graph
- Skip the graph query because "it seems simple"
- Assume you understand the impact without checking
- Make changes before understanding dependencies

**ALWAYS:**
- Query the graph IMMEDIATELY after reading any code file
- Query BEFORE making any modifications
- Query when you find files via search (grep/glob)
- Include graph findings in your analysis to the user

### The Rule: Read File → Query Graph → Then Proceed

```
1. You read a file with Read tool
2. IMMEDIATELY run graph queries (describe, find-callers, find-serializers, etc.)
3. NOW you understand the full context
4. NOW you can analyze, modify, or discuss the code
```

**Example - Reading a Model:**
```bash
# After reading app/models/user.rb, IMMEDIATELY run:
graph-describe.sh User
graph-find-serializers.sh User
graph-find-associations.sh User
```

**Example - Reading a Function:**
```bash
# After reading a file with process_payment function, IMMEDIATELY run:
graph-find-callers.sh process_payment
graph-find-callees.sh process_payment
```

---

## Available Commands

All commands auto-detect your agent ID from the tmux session. Just run them:

### Query Commands
| Command | Description |
|---------|-------------|
| `graph-describe.sh <name>` | Describe a component or function |
| `graph-find-callers.sh <function>` | Find all functions that call this function |
| `graph-find-callees.sh <function>` | Find all functions called by this function |
| `graph-find-related.sh <component>` | Find related components (extends, includes, etc.) |
| `graph-find-by-type.sh <type>` | Find all components of a type (model, controller, etc.) |
| `graph-find-serializers.sh <model>` | Find serializers for a model |
| `graph-find-associations.sh <model>` | Find model associations (belongs_to, has_many) |
| `graph-find-path.sh <from> <to>` | Find call path between two functions |

### Indexing Commands
| Command | Description |
|---------|-------------|
| `graph-index-delta.sh [project-path]` | **Delta index** - only re-index changed files |

## Delta Indexing (New)

When files change in your codebase, use delta indexing to quickly update the graph:

```bash
# Delta index - only process changed files
graph-index-delta.sh

# Delta index a specific project
graph-index-delta.sh /path/to/project
```

**First Run Behavior:**
- First time: Does a full index + initializes file tracking metadata
- Subsequent runs: Only indexes new/modified/deleted files

> **Note:** There is no separate `graph-index.sh` script. `graph-index-delta.sh` handles both full indexing (on first run) and incremental updates (on subsequent runs).

**Output shows:**
- New files added
- Modified files re-indexed
- Deleted files removed
- Unchanged files skipped

**Performance:**
- Full index: 30-120 seconds (1000+ files)
- Delta index: 1-5 seconds (5-10 changed files)

## What to Query Based on What You Read

| File Type | IMMEDIATELY Query |
|-----------|-------------------|
| Model | `graph-describe.sh`, `graph-find-serializers.sh`, `graph-find-associations.sh` |
| Controller | `graph-describe.sh`, `graph-find-callees.sh` |
| Service | `graph-describe.sh`, `graph-find-callers.sh` |
| Function | `graph-find-callers.sh`, `graph-find-callees.sh` |
| Serializer | `graph-describe.sh` |
| Any class | `graph-find-related.sh` |

## Why This Matters

Without querying the graph, you will:
- Miss serializers that need updating when you change a model
- Break callers when you change a function signature
- Miss child classes that inherit your changes
- Overlook associations that depend on this model

**The graph query takes 1 second. A broken deployment takes hours to fix.**

## Component Types

Use with `graph-find-by-type.sh`:
- `model` - Database models
- `serializer` - JSON serializers
- `controller` - API controllers
- `service` - Service objects
- `job` - Background jobs
- `concern` - Shared modules
- `component` - React/Vue components
- `hook` - React hooks

## Helper Scripts

This skill relies on an internal helper script that provides shared utility functions:

- **`graph-helper.sh`** - Sourced by the `graph-*.sh` tool scripts. Provides graph-specific API functions (`graph_query`, `init_graph`) and initialization logic. Located alongside the tool scripts in `~/.local/bin/` (installed) or `plugin/src/scripts/` (source). If tool scripts fail with "common.sh not found", re-run the installer (`~/ai-maestro/install-graph-tools.sh`).

## Error Handling

**Script not found:**
- Check PATH: `which graph-describe.sh`
- Verify scripts installed: `ls -la ~/.local/bin/graph-*.sh`
- Scripts are installed to `~/.local/bin/` which should be in your PATH
- If not found, run the installer from the AI Maestro project root: `~/ai-maestro/install-graph-tools.sh`

**API connection fails:**
- Ensure AI Maestro is running: `curl http://127.0.0.1:23000/api/hosts/identity`
- Ensure your agent is registered (scripts auto-detect from tmux session)
- Check exact component names (case-sensitive)

**Graph is unavailable:**
- Inform the user: "Graph unavailable, proceeding with manual analysis - increased risk of missing dependencies."

## Installation

If commands are not found, run the installer from the AI Maestro project root:
```bash
~/ai-maestro/install-graph-tools.sh
```

This installs scripts to `~/.local/bin/`.
