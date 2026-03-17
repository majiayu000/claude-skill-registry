---
name: typescript-lsp
description: REQUIRED for searching code in *.ts, *.tsx, *.js, *.jsx files. Use INSTEAD of Grep for TypeScript/JavaScript - provides type-aware symbol search that understands imports, exports, and relationships. Activate before reading, editing, or searching TypeScript code to verify signatures and find references.
license: ISC
compatibility: Requires bun
allowed-tools: Bash
metadata:
  file-triggers: "*.ts,*.tsx,*.js,*.jsx"
  replaces-tools: Grep
---

# TypeScript LSP Skill

## Purpose

This skill provides TypeScript Language Server Protocol integration for **exploring and understanding** TypeScript/JavaScript codebases. 

**IMPORTANT**: Prefer LSP tools over Grep/Glob when working with `*.ts`, `*.tsx`, `*.js`, `*.jsx` files. LSP provides type-aware results that understand imports, exports, and symbol relationships.

Use these tools to:
- **Explore codebases** - Find symbols, understand module structure, discover implementations
- **Find references** - Type-aware search across the entire codebase (better than grep for symbols)
- **Understand types** - Get full type signatures, generics, and documentation
- **Verify before editing** - Check all usages before modifying or deleting exports
- **Navigate code** - Jump to definitions, find implementations

## When to Use LSP vs Grep/Glob

| Task | Use LSP | Use Grep/Glob |
|------|---------|---------------|
| Find all usages of a function/type | ✅ `lsp-references` | ❌ Misses re-exports, aliases |
| Search for a symbol by name | ✅ `lsp-find` | ❌ Matches strings, comments |
| Understand file exports | ✅ `lsp-analyze --exports` | ❌ Doesn't resolve re-exports |
| Get type signature | ✅ `lsp-hover` | ❌ Not possible |
| Find files by pattern | ❌ | ✅ `Glob` |
| Search non-TS files (md, json) | ❌ | ✅ `Grep` |
| Search for text in comments/strings | ❌ | ✅ `Grep` |

## When to Use

**Exploring code (prefer LSP):**
- Run `lsp-find` to search for symbols across the workspace
- Run `lsp-symbols` to get an overview of file structure
- Run `lsp-analyze --exports` to see what a module provides

**Before editing code:**
- Run `lsp-references` to find all usages of a symbol you plan to modify
- Run `lsp-hover` to verify current type signatures

**Before writing code:**
- Run `lsp-find` to search for similar patterns or related symbols
- Run `lsp-hover` on APIs you plan to use

## Path Resolution

All scripts accept three types of file paths:
- **Absolute paths**: `/Users/name/project/src/file.ts`
- **Relative paths**: `./src/file.ts` or `../other/file.ts`
- **Package export paths**: `my-package/src/module.ts` (resolved via `Bun.resolve()`)

Package export paths are recommended for portability and consistency with the package's exports field.

## Scripts

### Individual Scripts

#### lsp-hover
Get type information at a specific position.

```bash
bunx @plaited/development-skills lsp-hover <file> <line> <char>
```

**Arguments:**
- `file`: Path to TypeScript/JavaScript file
- `line`: Line number (0-indexed)
- `char`: Character position (0-indexed)

**Example:**
```bash
bunx @plaited/development-skills lsp-hover src/utils/parser.ts 42 10
```

#### lsp-symbols
List all symbols in a file.

```bash
bunx @plaited/development-skills lsp-symbols <file>
```

**Example:**
```bash
bunx @plaited/development-skills lsp-symbols src/utils/parser.ts
```

#### lsp-references
Find all references to a symbol.

```bash
bunx @plaited/development-skills lsp-refs <file> <line> <char>
```

**Example:**
```bash
bunx @plaited/development-skills lsp-refs src/utils/parser.ts 42 10
```

#### lsp-find
Search for symbols across the workspace.

```bash
bunx @plaited/development-skills lsp-find <query> [context-file]
```

**Arguments:**
- `query`: Symbol name or partial name
- `context-file`: Optional file to open for project context

**Example:**
```bash
bunx @plaited/development-skills lsp-find parseConfig
bunx @plaited/development-skills lsp-find validateInput src/lib/validator.ts
```

### Batch Script

#### lsp-analyze
Perform multiple analyses in a single session for efficiency.

```bash
bunx @plaited/development-skills lsp-analyze <file> [options]
```

**Options:**
- `--symbols, -s`: List all symbols
- `--exports, -e`: List only exported symbols
- `--hover <line:char>`: Get type info (repeatable)
- `--refs <line:char>`: Find references (repeatable)
- `--all`: Run symbols + exports analysis

**Examples:**
```bash
# Get file overview
bunx @plaited/development-skills lsp-analyze src/utils/parser.ts --all

# Check multiple positions
bunx @plaited/development-skills lsp-analyze src/utils/parser.ts --hover 50:10 --hover 75:5

# Before refactoring: find all references
bunx @plaited/development-skills lsp-analyze src/utils/parser.ts --refs 42:10
```

## Common Workflows

### Understanding a File

```bash
# 1. Get exports overview
bunx @plaited/development-skills lsp-analyze path/to/file.ts --exports

# 2. For specific type info, hover on interesting symbols
bunx @plaited/development-skills lsp-hover path/to/file.ts <line> <char>
```

### Before Modifying an Export

```bash
# 1. Find all references first
bunx @plaited/development-skills lsp-refs path/to/file.ts <line> <char>

# 2. Check what depends on it
# Review the output to understand impact
```

### Finding Patterns

```bash
# Search for similar implementations
bunx @plaited/development-skills lsp-find handleRequest
bunx @plaited/development-skills lsp-find parseConfig
```

### Pre-Implementation Verification

```bash
# Before writing code that uses an API, verify its signature
bunx @plaited/development-skills lsp-hover path/to/api.ts <line> <char>
```

## Output Format

All scripts output JSON to stdout. Errors go to stderr.

**Hover output:**
```json
{
  "contents": {
    "kind": "markdown",
    "value": "```typescript\nconst parseConfig: (options: Options) => Config\n```"
  },
  "range": { "start": {...}, "end": {...} }
}
```

**Symbols output:**
```json
[
  {
    "name": "symbolName",
    "kind": 13,
    "range": { "start": {...}, "end": {...} }
  }
]
```

**Analyze output:**
```json
{
  "file": "path/to/file.ts",
  "exports": [
    { "name": "exportName", "kind": "Constant", "line": 139 }
  ]
}
```

## Performance

Each script invocation:
1. Starts TypeScript Language Server (~300-500ms)
2. Initializes LSP connection
3. Opens document
4. Performs query
5. Closes and stops

For multiple queries on the same file, use `lsp-analyze` to batch operations in a single session.

## Related Skills

- **code-documentation**: TSDoc standards for documentation
