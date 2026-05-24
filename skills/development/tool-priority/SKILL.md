---
description: Use when choosing between search tools (LSP, grep, glob) or need tool reference - covers when to use each tool and detailed syntax
---

# Tool Priority Skill

## Priority Order

**LSP tools → grep → glob**

1. **LSP tools** - Semantic code intelligence (10 tools)
2. `grep` - Text search (logs, config, code patterns, strings)
3. `glob` - File discovery by name pattern
4. `read`, `edit`, `write` - File operations

**Rule**: Always `read` before `edit` to verify content.

## Choosing the Right Tool

Ask: **"Am I looking for semantic understanding or just text?"**

### Code Understanding (Use LSP)

| Need             | Tool                        | Example                              |
| ---------------- | --------------------------- | ------------------------------------ |
| Symbol type info | `lsp_lsp_hover`             | Type signature at cursor             |
| Definition jump  | `lsp_lsp_goto_definition`   | Source location                      |
| All usages       | `lsp_lsp_find_references`   | Before refactoring                   |
| File structure   | `lsp_lsp_document_symbols`  | What functions/classes in this file? |
| Safe rename      | `lsp_lsp_rename`            | Update symbol across codebase        |
| Workspace search | `lsp_lsp_workspace_symbols` | Where is UserService defined?        |

### Text Search (Use grep)

| Need              | Tool   | Example pattern        |
| ----------------- | ------ | ---------------------- |
| Function calls    | `grep` | `functionName\(`       |
| Import statements | `grep` | `import.*from.*module` |
| Error messages    | `grep` | `FATAL\|ERROR`         |
| Config values     | `grep` | `API_KEY`              |
| TODO comments     | `grep` | `TODO\|FIXME`          |
| Hook usage        | `grep` | `useState(`            |
| Debug logs        | `grep` | `console\.log\(`       |

### Workflow Pattern

```
# Step 1: Find it
grep "functionName" src/

# Step 2: Understand it
read src/file.ts
lsp_lsp_document_symbols(filePath="src/file.ts", line=1, character=1)

# Step 3: Trace it
lsp_lsp_goto_definition(filePath="src/file.ts", line=42, character=10)
lsp_lsp_find_references(filePath="src/file.ts", line=42, character=10)

# Step 4: Modify it (if needed)
lsp_lsp_hover(filePath="src/file.ts", line=42, character=10)
```

## LSP Tools Reference

Semantic code intelligence via Language Server Protocol. **Uses `lsp_lsp_*` prefix** (built-in experimental).

### Navigation & Understanding

| Tool                                                 | Purpose                               | When to Use                       |
| ---------------------------------------------------- | ------------------------------------- | --------------------------------- |
| `lsp_lsp_hover(filePath, line, character)`           | Type info and docs at cursor          | "What type is this variable?"     |
| `lsp_lsp_goto_definition(filePath, line, character)` | Jump to where symbol is defined       | "Where is this function defined?" |
| `lsp_lsp_find_references(filePath, line, character)` | Find all usages of a symbol           | "What uses this function?"        |
| `lsp_lsp_document_symbols(filePath)`                 | File outline (classes, functions)     | "What's in this file?"            |
| `lsp_lsp_workspace_symbols(query, filePath)`         | Fuzzy search symbols across workspace | "Where is UserService defined?"   |

### Diagnostics

| Tool                                       | Purpose                              | When to Use              |
| ------------------------------------------ | ------------------------------------ | ------------------------ |
| `lsp_lsp_diagnostics(filePath, severity?)` | Errors/warnings from language server | "Are there type errors?" |

### Refactoring

| Tool                                                                     | Purpose                       | When to Use                        |
| ------------------------------------------------------------------------ | ----------------------------- | ---------------------------------- |
| `lsp_lsp_rename(filePath, line, character, newName)`                     | Rename symbol across codebase | "Rename this function safely"      |
| `lsp_lsp_code_actions(filePath, startLine, startChar, endLine, endChar)` | Get available refactorings    | "What refactorings are available?" |
| `lsp_lsp_code_action_apply(...)`                                         | Apply a specific code action  | Execute chosen refactoring         |
| `lsp_lsp_organize_imports(filePath)`                                     | Clean up and sort imports     | "Fix imports"                      |

**Caveat**: LSP tools modify files directly. Re-read files before further edits.

## grep Reference

Fast, text-based search using ripgrep.

### Basic Patterns

```bash
# Find function definitions
grep "function\|const.*=.*(" src/

# Find imports
grep "import.*from" src/

# Find React hooks
grep "useState\|useEffect" src/

# Find console logs
grep "console\.log" src/

# Search for errors
grep "Error\|Exception\|Throw" src/

# Multiple patterns
grep -e "TODO" -e "FIXME" src/

# Case insensitive
grep -i "test" src/

# Specific file types
grep -r "API_KEY" --include="*.ts" --include="*.js"
```

### grep vs LSP

| Scenario           | Use                       | Why                                             |
| ------------------ | ------------------------- | ----------------------------------------------- |
| "Find all X"       | `grep`                    | Fast text search, everything including comments |
| "Where is X used?" | `lsp_lsp_find_references` | Semantic, only code usage, tracks dependencies  |
| "What type is X?"  | `lsp_lsp_hover`           | Type system intelligence                        |
| "Find TODOs"       | `grep`                    | Text search across all files                    |
| "Rename X"         | `lsp_lsp_rename`          | Safe semantic refactoring                       |

### Common Gotchas

**grep finds everything:**

```bash
grep "fetchUser"  # Matches: function fetchUser(), "fetchUser" string, // fetchUser comment
```

**LSP finds only code:**

```bash
lsp_lsp_find_references  # Only actual usages in code, not strings/comments
```

**When to use grep first:**

- Quick exploration ("are there any X?")
- Finding error patterns, logs, configs
- Searching across file types (JSON, YAML, etc.)

**When to use LSP first:**

- Understanding code structure
- Before refactoring
- Tracing dependencies
- Getting type information

## glob Reference

Find files by pattern.

```bash
# All TypeScript files
glob "**/*.ts"

# All test files
glob "**/*.test.ts"

# Specific directory
glob "src/**/*.ts"

# Multiple patterns
glob ["src/**/*.ts", "tests/**/*.ts"]
```

## Research Tools

| Tool           | Use When                                                |
| -------------- | ------------------------------------------------------- |
| **context7**   | Library docs (try first). Fast, external APIs.          |
| **websearch**  | Docs not in Context7, recent releases, troubleshooting. |
| **codesearch** | Real implementation patterns from GitHub.               |
| **webfetch**   | Specific URL user provided.                             |
