---
name: lsp-navigation
description: Semantic code navigation using LSP (Language Server Protocol). Find where functions/variables are defined, find all usages across the codebase, rename symbols safely, and get TypeScript diagnostics. ALWAYS use this instead of Grep for semantic operations. Use when the user says "rename variable", "find all usages", "where is this used", "go to definition", "find references", "rename function", "refactor name", or asks "où est utilisé", "renommer", "trouver les références". Much faster and more accurate than manual Grep searches.
---

# LSP Navigation (cclsp)

Use cclsp MCP tools for semantic code navigation.

## Tools

| Tool | Use Case |
|------|----------|
| `mcp__cclsp__find_definition` | Find where a symbol is defined |
| `mcp__cclsp__find_references` | Find all usages of a symbol |
| `mcp__cclsp__rename_symbol` | Rename symbol across codebase |
| `mcp__cclsp__get_diagnostics` | Get TypeScript errors for a file |

## Examples

```
mcp__cclsp__find_definition(file_path="src/api.ts", symbol_name="fetchUser")
mcp__cclsp__find_references(file_path="src/api.ts", symbol_name="fetchUser")
mcp__cclsp__rename_symbol(file_path="src/api.ts", symbol_name="fetchUser", new_name="getUser")
mcp__cclsp__get_diagnostics(file_path="src/app/page.tsx")
```
