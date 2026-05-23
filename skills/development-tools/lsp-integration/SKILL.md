---
name: lsp-integration
description: LSP (Language Server Protocol) integration expert. Provides semantic code understanding using language servers for TypeScript, JavaScript, Python, Go, Rust, and more. Handles code navigation (go to definition, find references), symbol search, hover information, diagnostics, refactoring. 100x faster than grep for code exploration. Activates for LSP, language server, TypeScript, JavaScript, Python, Go, Rust, Java, C#, code navigation, go to definition, find references, find all references, hover type, type information, symbol search, document symbols, workspace symbols, diagnostics, code errors, type errors, refactoring, rename symbol, code actions, auto import, semantic analysis, code intelligence, intellisense, autocomplete context, type inference.
allowed-tools: Read, Bash, Glob, Grep
---

# LSP Integration Skill

You are an expert in leveraging Language Server Protocol (LSP) for semantic code understanding. LSP provides 100x faster and more accurate code exploration than text-based grep searches.

## Overview

LSP servers understand code semantically - they know about types, symbols, references, and relationships between code elements. This enables precise navigation and refactoring that text search cannot achieve.

## Supported Languages

| Language | LSP Server | Install |
|----------|-----------|---------|
| TypeScript/JavaScript | `typescript-language-server` | `npm install -g typescript-language-server typescript` |
| Python | `python-lsp-server` (pylsp) | `pip install python-lsp-server` |
| Go | `gopls` | `go install golang.org/x/tools/gopls@latest` |
| Rust | `rust-analyzer` | Via rustup or standalone |
| Java | `jdtls` | Eclipse JDT Language Server |
| C# | `omnisharp` | .NET SDK |

## Key Operations

### 1. Go to Definition
Navigate to where a symbol is defined.

```bash
# Using TypeScript language server
npx ts-node --eval "
const ts = require('typescript');
// Find definition of symbol at position
"
```

**Use case**: "Where is this function defined?" → Find exact location in codebase.

### 2. Find All References
Find every place a symbol is used.

**Critical for refactoring**: Before renaming or changing a function, ALWAYS find all references to understand impact.

```bash
# Find all usages of a function/variable/class
# LSP tracks semantic references, not just text matches
```

**Use case**: "What will break if I change this interface?" → Find all implementations and usages.

### 3. Document Symbols
Get structured view of all symbols in a file.

**Use case**: "What functions/classes are in this file?" → Get hierarchy without parsing.

### 4. Hover Information
Get type information and documentation for any symbol.

**Use case**: "What type does this variable have?" → Get inferred or declared type.

### 5. Diagnostics
Get compilation errors and warnings.

**Use case**: "Are there any type errors?" → Real-time error checking.

## When to Use LSP vs Grep

| Task | Use LSP | Use Grep |
|------|---------|----------|
| Find function definition | ✅ Precise | ⚠️ May find wrong match |
| Find all references | ✅ Semantic | ⚠️ Misses renamed imports |
| Search for text pattern | ❌ Not designed for this | ✅ Fast text search |
| Understand type hierarchy | ✅ Full inheritance chain | ❌ Cannot determine |
| Check for type errors | ✅ Compiler-accurate | ❌ Impossible |
| Find files by name | ❌ Overkill | ✅ Use Glob |

## Best Practices

### 1. Always Use findReferences Before Refactoring
```
❌ WRONG: Grep for function name → rename → hope nothing breaks
✅ RIGHT: LSP findReferences → understand all usages → safe rename
```

### 2. Use goToDefinition Instead of Grep
```
❌ WRONG: grep -r "function processOrder" .
✅ RIGHT: LSP goToDefinition → exact location, handles imports/exports
```

### 3. Combine with Explore Agent
For complex exploration tasks, combine LSP operations with the Explore agent:
```
1. LSP: Find all references to deprecated function
2. Explore: Understand migration patterns in codebase
3. LSP: Navigate to each usage for refactoring
```

## TypeScript/JavaScript Specific

### Setup
```bash
# Install globally
npm install -g typescript-language-server typescript

# Verify installation
typescript-language-server --version
```

### Common Operations

**Find where interface is implemented:**
```typescript
// LSP findReferences on interface → shows all implementing classes
```

**Check type at position:**
```typescript
// LSP hover → shows inferred type, even for complex generics
```

**Find unused exports:**
```typescript
// LSP diagnostics + findReferences → exports with 0 references
```

## Python Specific

### Setup
```bash
pip install python-lsp-server
# Optional: Add type checking
pip install pylsp-mypy
```

### Common Operations

**Find class hierarchy:**
```python
# LSP can show base classes and subclasses
```

**Check import resolution:**
```python
# LSP resolves imports even with complex __init__.py structures
```

## Integration with SpecWeave

### In CLAUDE.md (already documented)
LSP operations are recommended in the SpecWeave workflow:
- Use `findReferences` before any refactoring
- Use `goToDefinition` for code navigation
- Use `getDiagnostics` to check for errors

### Workflow Example

1. **Before implementing**: Use LSP to understand existing code structure
2. **During implementation**: Use diagnostics to catch errors early
3. **Before commit**: Use findReferences to verify no broken usages
4. **Code review**: Use LSP to trace data flow through system

## Troubleshooting

### LSP Server Not Starting
```bash
# Check if server is installed
which typescript-language-server
which pylsp
which gopls

# Check for initialization errors
typescript-language-server --stdio 2>&1 | head -20
```

### Slow Performance
- Exclude `node_modules` and build directories
- Ensure `tsconfig.json` or equivalent is properly configured
- Increase memory limits for large projects

### Missing References
- Ensure project is properly typed
- Check that all dependencies have type definitions
- Verify language server has indexed the project

## Token Budget

- **LSP setup instructions**: 200-300 tokens
- **Single operation explanation**: 100-200 tokens
- **Full workflow**: 400-600 tokens

**NEVER exceed 2000 tokens per response!**
