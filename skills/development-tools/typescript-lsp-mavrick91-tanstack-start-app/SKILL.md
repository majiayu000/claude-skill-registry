---
name: typescript-lsp
description: Use TypeScript LSP for code intelligence instead of grep. Always prioritize LSP tools for go-to-definition, find references, type checking, and code navigation in TypeScript/JavaScript files.
---

# TypeScript LSP Priority

## ⛔ CRITICAL RULE

**NEVER use Grep or search tools to find symbol definitions, references, or type information in TypeScript/JavaScript files.**

When a user asks about a symbol (function, variable, type, class, etc.):

1. **DO NOT** use Grep first to "find" it
2. **DO NOT** use Glob to locate files containing it
3. **IMMEDIATELY** use the LSP tool with the appropriate operation

This is a hard requirement, not a preference. Violating this wastes tokens and provides inferior results.

---

**IMPORTANT**: This project has the TypeScript LSP plugin installed. Always prefer LSP tools over grep/glob for code exploration.

## Prerequisites

The TypeScript language server must be installed globally:

```bash
yarn global add typescript-language-server typescript
```

Then restart Claude Code to activate the LSP tools.

## When to Use LSP vs Grep

| Task                               | Use LSP                     | Use Grep |
| ---------------------------------- | --------------------------- | -------- |
| Find where function is defined     | ✅ `LSP goToDefinition`     | ❌ NEVER |
| Find all usages of a symbol        | ✅ `LSP findReferences`     | ❌ NEVER |
| Get function signature/types       | ✅ `LSP hover`              | ❌ NEVER |
| List symbols in a file             | ✅ `LSP documentSymbol`     | ❌ NEVER |
| Search symbols across workspace    | ✅ `LSP workspaceSymbol`    | ❌ NEVER |
| Find implementations               | ✅ `LSP goToImplementation` | ❌ NEVER |
| Search for text pattern in strings | ❌                          | ✅ Grep  |
| Find files by name                 | ❌                          | ✅ Glob  |
| Search in non-TS files (JSON, MD)  | ❌                          | ✅ Grep  |

## LSP Tool Operations

Use the native `LSP` tool with these operations:

### goToDefinition

Find where a symbol is defined:

```
LSP(operation: "goToDefinition", filePath: "src/file.ts", line: 10, character: 5)
```

Use when: "Where is X defined?", "Jump to X", "Find the source of X"

### findReferences

Find all usages of a symbol:

```
LSP(operation: "findReferences", filePath: "src/file.ts", line: 10, character: 5)
```

Use when: "Where is X used?", "Find all calls to X", "What uses X?"

### hover

Get type information and documentation:

```
LSP(operation: "hover", filePath: "src/file.ts", line: 10, character: 5)
```

Use when: "What type is X?", "What does X return?", "Show signature of X"

### documentSymbol

List all symbols in a file:

```
LSP(operation: "documentSymbol", filePath: "src/file.ts", line: 1, character: 1)
```

Use when: "What's in this file?", "List functions in X", "Show file structure"

### workspaceSymbol

Search for symbols across the entire workspace:

```
LSP(operation: "workspaceSymbol", filePath: "src/any.ts", line: 1, character: 1)
```

Use when: "Find symbol X in codebase", "Where is X defined?" (when you don't know the file)

### goToImplementation

Find implementations of interfaces/abstract methods:

```
LSP(operation: "goToImplementation", filePath: "src/file.ts", line: 10, character: 5)
```

Use when: "What implements X?", "Find concrete implementations"

## Priority Order for Code Exploration

1. **First**: Use LSP tools for TypeScript/JavaScript files (.ts, .tsx, .js, .jsx)
2. **Second**: Use Read tool to view file contents
3. **Third**: Use Grep only for text search patterns or non-TS files
4. **Fourth**: Use Glob for finding files by name pattern

## Examples

### User asks: "Find formatTaxAmount and show me all references"

❌ **WRONG (what you must NOT do):**

```
1. Use Grep to search for "formatTaxAmount"
2. Then use LSP on the results
```

✅ **CORRECT (do this immediately):**

```
1. LSP(operation: "workspaceSymbol", ...) to find the symbol
2. LSP(operation: "findReferences", filePath: "src/lib/tax.ts", line: 21, character: 17)
3. LSP(operation: "hover", ...) for type info
```

### User asks: "Where is validateSession defined?"

❌ **WRONG:**

```
Grep for "function validateSession" or "const validateSession"
```

✅ **CORRECT:**

```
LSP(operation: "goToDefinition", filePath: "file-where-its-used.ts", line: X, character: Y)
```

### User asks: "What uses the hashPassword function?"

❌ **WRONG:**

```
Grep for "hashPassword" across codebase
```

✅ **CORRECT:**

```
LSP(operation: "findReferences", filePath: "src/lib/auth.ts", line: 10, character: 17)
```

### User asks: "What type does calculateTax return?"

❌ **WRONG:**

```
Read the entire file to find the type definition
```

✅ **CORRECT:**

```
LSP(operation: "hover", filePath: "src/lib/tax.ts", line: 15, character: 17)
```

## Supported File Extensions

The LSP works with:

- `.ts` - TypeScript
- `.tsx` - TypeScript React
- `.js` - JavaScript
- `.jsx` - JavaScript React
- `.mts`, `.cts` - ES/CommonJS TypeScript
- `.mjs`, `.cjs` - ES/CommonJS JavaScript

## When Grep is Still Appropriate

- Searching for text in non-code files (JSON, Markdown, etc.)
- Finding TODO/FIXME comments
- Searching for string literals or patterns
- When LSP tools don't return results (symbol not typed)
