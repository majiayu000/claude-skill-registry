---
name: Serena Usage
description: This skill should be used when the user asks to "use serena", "semantic search", "symbol analysis", "find references", "code navigation", or needs Serena MCP guidance. Provides Serena tool usage patterns.
---

# Serena MCP Tool Patterns

## Core Tools

### Symbol Operations
- **get_symbols_overview** - Get high-level view of file symbols (start with depth=0, increase if needed)
- **find_symbol** - Find by name path (e.g., "MyClass/myMethod"), use `substring_matching` for partial names
- **find_referencing_symbols** - Find all references for dependency/impact analysis
- **search_for_pattern** - Regex search; use `restrict_search_to_code_files` and `relative_path` to scope

### Editing Operations
- **replace_symbol_body** - Replace entire symbol definition
- **insert_before_symbol** / **insert_after_symbol** - Add imports, decorators, new functions
- **rename_symbol** - Rename across codebase with automatic reference updates

### Memory Operations
- **list_memories** - Check existing patterns before implementation
- **read_memory** - Load project patterns (e.g., "nix-conventions")
- **write_memory** - Record new patterns for future reference
- **edit_memory** - Update specific parts using literal or regex mode
- **delete_memory** - Remove obsolete patterns (user request only)

### Reflection Tools (call after searches/before changes)
- **think_about_collected_information** - After non-trivial search sequences
- **think_about_task_adherence** - Before making code changes
- **think_about_whether_you_are_done** - When task appears complete

## Key Patterns

### File Exploration
1. `get_symbols_overview depth=0` - top-level structure
2. `get_symbols_overview depth=1` - class members
3. `find_symbol include_body=true` - specific implementation

### Dependency Tracing
1. `find_symbol` - locate the symbol
2. `find_referencing_symbols` - find all callers
3. Repeat for full dependency graph

### Memory Workflow
1. `list_memories` before implementation
2. `read_memory` for relevant patterns
3. `write_memory` after discovering new conventions

## Critical Rules
- Always check memories before implementing new features
- Use symbol operations over reading entire files
- Restrict searches by `relative_path` when scope is known
- Use `rename_symbol` for consistent renaming (not manual updates)
