---
name: code-navigation
description: "Serena LSP vs native tool routing for code navigation. Defines when to use find_symbol, get_symbols_overview, replace_symbol_body vs Read/Edit/Grep. Use when reading, searching, or modifying Rust source code."
---

# Code Navigation

## Decision Tree: Serena vs Native Tools

| Task | Use | Not |
|------|-----|-----|
| Reading code structure | Serena `get_symbols_overview` → read only needed bodies | Don't read full files |
| Finding definitions | Serena `find_symbol` | Don't use Grep for symbol defs |
| Finding callers | Serena `find_referencing_symbols` | Don't use Grep for who-calls-what |
| Replacing functions | Serena `replace_symbol_body` (entire function) | Use Edit for line-level changes |
| Non-code files | Read/Edit/Grep | Serena only works with LSP languages |
| Config/markdown/TOML | Read/Edit | Serena has limited non-code support |

## Serena Capabilities

### Symbol Navigation
- **`find_symbol`**: Locate symbol definitions across the codebase
- **`get_symbols_overview`**: Get file structure without reading full content (50-75% token savings)

### Impact Analysis
- **`find_referencing_symbols`**: Find all callers/users of any symbol across the codebase

### Precise Edits
- **`replace_symbol_body`**: Replace entire function/method bodies
- **`insert_before_symbol`**: Insert code before a symbol definition
- **`insert_after_symbol`**: Insert code after a symbol definition

### Rename Refactoring
- **`rename_symbol`**: Rename symbols with automatic reference updates across entire codebase

### Pattern Search
- **`search_for_pattern`**: Regex search across project files

### Project Memory
- **`read_memory`**: Retrieve project-specific code structure and conventions
- **`write_memory`**: Store project-specific code structure and conventions

## Progressive Disclosure Pattern

1. Start with `get_symbols_overview` for a file (50-75% token savings vs full read)
2. Read only the function bodies you actually need with `find_symbol` + `include_body=True`
3. Use `find_referencing_symbols` to trace callers before modifying any symbol
4. Fall back to Read/Edit for non-Rust files

## Token Budget

- `get_symbols_overview` saves 50-75% tokens compared to reading full source files
- Always prefer symbol-level reads over full-file reads for Rust code
- A single `find_symbol` call is cheaper than reading and searching a full file
