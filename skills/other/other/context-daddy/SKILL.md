---
name: context-daddy
description: Context management tools for Claude Code - provides intelligent codebase mapping with Python, Rust, and C++ parsing, duplicate detection, and MCP-powered symbol queries. Use this skill when working with large codebases that need automated indexing and context management.
---

# Context Tools for Claude Code

This skill provides intelligent context management for large codebases through:

- **Repository Mapping**: Parses Python, Rust, and C++ code to extract classes, functions, and methods
- **Duplicate Detection**: Identifies similar code patterns using fuzzy matching
- **MCP Symbol Server**: Enables fast symbol search via `search_symbols` and `get_file_symbols` tools
- **Automatic Indexing**: Background incremental updates as files change

## Using MCP Tools - PRIMARY CODE EXPLORATION METHOD

**⚡ DECISION TREE - Ask yourself BEFORE using Grep/Search/Bash:**

```
Am I searching for code symbols (functions, classes, enums, structs, types)?
├─ YES → Use MCP tools (search_symbols / get_symbol_content / get_file_symbols)
│         Example: Finding "enum InstructionData" → search_symbols("InstructionData")
│         Example: Finding "Phi" variant → get_symbol_content("InstructionData")
│
└─ NO → Am I searching for text/comments/strings/config values?
          └─ YES → Use Grep/Search
                   Example: Finding string literals, documentation, JSON values
```

**CRITICAL**: Use repo-map tools as your FIRST approach when you need to:
- **Find a function/class/method by name or pattern** → `search_symbols`
- **Understand how to use a function** (parameters, return type) → `search_symbols` or `get_symbol_content`
- **Get the source code of a specific function/class** → `get_symbol_content`
- **See all code in a file** → `get_file_symbols`
- **Discover what functionality exists** in the codebase → `search_symbols` with patterns

**Do NOT use Grep or Bash for these tasks** - the repo-map tools are:
- **Faster** (pre-indexed SQLite database)
- **More accurate** (AST-parsed, not regex)
- **More informative** (includes signatures, docstrings, line ranges)

**When to use Grep instead:**
- Searching for string literals, comments, or arbitrary text
- Searching in non-code files (markdown, config, etc.)
- Cross-file text pattern searches

**Tool availability check:**
Before attempting to use MCP tools (mcp__plugin_context-daddy_repo-map__*), check if `.claude/repo-map.db` exists:
- If YES: Try the MCP tool. If it fails (not available), use sqlite3 fallback.
- If NO: The project hasn't been indexed yet. Either wait for indexing or run `/context-daddy:repo-map` to generate it.

**Fallback order:**
1. Try MCP tool first
2. If tool not found, use sqlite3 fallback to still answer the question
3. Explain that session needs restart to load MCP server for future use

## Real-World Usage Examples

### Example 1: User asks "Can we compare against OSDI?"

**Inefficient approach** (DON'T DO THIS):
```bash
grep -r "setup_model\|setup_instance" jax_spice/devices/*.py
```
Problems: Slow, error-prone pattern matching, gets interrupted on large codebases.

**Efficient approach** (DO THIS):
```
mcp__plugin_context-daddy_repo-map__search_symbols
pattern: "setup_*"
```
Result: Instant list of all `setup_model`, `setup_instance`, etc. with locations and signatures.

### Example 2: User asks "How does the config loader work?"

**Inefficient approach** (DON'T DO THIS):
```bash
find . -name "*.py" -exec grep -l "class.*Config" {} \;
```

**Efficient approach** (DO THIS):
```
mcp__plugin_context-daddy_repo-map__search_symbols
pattern: "*Config*"
kind: "class"
```
Then get the source:
```
mcp__plugin_context-daddy_repo-map__get_symbol_content
name: "ConfigLoader"
```

### Example 3: User asks "What functions are in utils.py?"

**Inefficient approach** (DON'T DO THIS):
```bash
grep "^def " src/utils.py
```

**Efficient approach** (DO THIS):
```
mcp__plugin_context-daddy_repo-map__get_file_symbols
file: "src/utils.py"
```
Result: Complete list of all functions/classes with signatures and docstrings.

### Example 4: Finding Rust enum variants (Real user case)

User needs to check if it's `Phi` or `PhiNode` in `enum InstructionData`.

**Inefficient approach** (DON'T DO THIS):
```bash
grep -n "enum InstructionData" openvaf-py/vendor/OpenVAF/openvaf/mir/src
grep -n "Phi" openvaf-py/vendor/OpenVAF/openvaf/mir/src/instructions.rs
```
Problems: Multiple searches, manual parsing, easy to miss correct variant.

**Efficient approach** (DO THIS):
```
mcp__plugin_context-daddy_repo-map__search_symbols
pattern: "InstructionData"

mcp__plugin_context-daddy_repo-map__get_symbol_content
name: "InstructionData"
```
Result: Complete enum with all variants visible, including `PhiNode(_)`.

## First Time Setup

**IMPORTANT**: If the user has just installed this plugin:

> "I see you've installed the context-daddy plugin. The MCP server should auto-configure on restart. After restarting Claude Code, run `/mcp` to verify the `repo-map` server is loaded.
>
> If it doesn't load automatically, let me know and I can help troubleshoot using `/context-daddy:setup-mcp`."

The MCP server auto-configures from the plugin manifest. Only if auto-config fails should you run `/context-daddy:setup-mcp` for troubleshooting.

## Included Components

### Hooks
- **SessionStart**: Generates project manifest and displays status
- **PreCompact**: Refreshes context before compaction
- **SessionEnd**: Cleanup operations

Note: Indexing is now handled by the MCP server itself (no PreToolUse hook needed).

### MCP Server (repo-map)

**Database Schema (.claude/repo-map.db):**
```sql
symbols table columns:
- name (TEXT): Symbol name (function/class/method name)
- kind (TEXT): "function", "class", or "method"
- signature (TEXT): Full function/method signature with parameters and type hints
  Examples:
  - "extract_symbols_from_python(file_path: Path, relative_to: Path) -> list[Symbol]"
  - "analyze_files(files: list[Path], extractor, language: str, root: Path)"
- docstring (TEXT): First line of docstring or full docstring
- file_path (TEXT): Relative path from project root
- line_number (INTEGER): Start line (1-indexed)
- end_line_number (INTEGER): End line (1-indexed)
- parent (TEXT): For methods, the class name

metadata table (v0.7.0+):
- key (TEXT PRIMARY KEY): Metadata key
- value (TEXT): Metadata value
Keys:
- 'status': 'idle' | 'indexing' | 'completed' | 'failed'
- 'index_start_time': ISO8601 timestamp when indexing started
- 'last_indexed': ISO8601 timestamp when last completed
- 'symbol_count': Total symbols indexed (string)
- 'error_message': Error message if status='failed'
```

**Indexing Status and Auto-Wait (v0.7.0+):**
- The MCP server tracks indexing status in the metadata table
- Tools automatically wait (up to 60s) if indexing is in progress
- **Watchdog**: Detects hung indexing (>10 minutes) and resets status to 'failed'
- **First Use**: On first use in a new codebase, indexing starts automatically
- **Behavior**: Most tools wait for completion, repo_map_status does not (use to check progress)

**Available MCP Tools:**
- `mcp__plugin_context-daddy_repo-map__search_symbols` - Search symbols by pattern (supports glob wildcards)
  - Returns: name, kind, signature, file_path, line_number, docstring, parent
  - **AUTO-WAIT**: If indexing is in progress, automatically waits up to 60s for completion
- `mcp__plugin_context-daddy_repo-map__get_file_symbols` - Get all symbols in a specific file
  - Returns: All symbols with full metadata
  - **AUTO-WAIT**: If indexing is in progress, automatically waits up to 60s for completion
- `mcp__plugin_context-daddy_repo-map__get_symbol_content` - Get full source code of a symbol by exact name
  - Returns: symbol metadata + content (source code text) + location
  - **AUTO-WAIT**: If indexing is in progress, automatically waits up to 60s for completion
- `mcp__plugin_context-daddy_repo-map__list_files` - List all indexed files, optionally filtered by glob pattern
  - Returns: list of file paths matching pattern (e.g., "*.va", "*psp103*", "**/devices/*")
  - **MUCH faster than find/ls** - queries pre-built index instead of filesystem traversal
  - **AUTO-WAIT**: If indexing is in progress, automatically waits up to 60s for completion
- `mcp__plugin_context-daddy_repo-map__reindex_repo_map` - Trigger manual reindex
  - Does NOT auto-wait (use to force reindex)
- `mcp__plugin_context-daddy_repo-map__repo_map_status` - Check indexing status and staleness
  - Returns: index_status (idle/indexing/completed/failed), symbol_count, last_indexed, indexing_duration_seconds
  - Does NOT auto-wait (use to check status)
- `mcp__plugin_context-daddy_repo-map__wait_for_index` - Explicitly wait for indexing to complete
  - Takes: timeout_seconds (default: 60)
  - Returns: success (bool), message (str)
  - Use when you want to wait longer than the default 60s auto-wait timeout

**Fallback when MCP tools unavailable:**
Use sqlite3 directly on `.claude/repo-map.db`:
```bash
# Search symbols
sqlite3 .claude/repo-map.db "SELECT name, kind, signature, file_path, line_number FROM symbols WHERE name LIKE 'pattern%' LIMIT 20"

# Get symbol with source
sqlite3 .claude/repo-map.db "SELECT * FROM symbols WHERE name = 'function_name'"
# Then read file_path lines line_number to end_line_number
```

### Slash Commands
- `/context-daddy:repo-map` - Regenerate repository map
- `/context-daddy:manifest` - Refresh project manifest
- `/context-daddy:learnings` - Manage project learnings
- `/context-daddy:status` - Show plugin status

## Language Support

| Language | Parser | File Extensions |
|----------|--------|-----------------|
| Python | AST | `.py` |
| Rust | tree-sitter-rust | `.rs` |
| C++ | tree-sitter-cpp | `.cpp`, `.cc`, `.cxx`, `.hpp`, `.h`, `.hxx` |
