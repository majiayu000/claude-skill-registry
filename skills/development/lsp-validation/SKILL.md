---
name: lsp-validation
description: Use Language Server Protocol tools for code validation, navigation, and refactoring. Essential for maintaining code quality.
---

# LSP Validation Skill

Use the LSP (Language Server Protocol) tools to validate code quality, find references, navigate definitions, and perform safe refactoring.

## Available LSP Tools

### 1. `lsp_diagnostics` - Get Errors and Warnings

**When to use:** After writing or modifying code to check for errors.

```
lsp_diagnostics(filePath: "/path/to/file.ts", severity: "error")
```

**Severity levels:**
- `error` - Only errors (compilation failures)
- `warning` - Errors and warnings
- `information` - Includes informational messages
- `hint` - All diagnostics including hints
- `all` - Everything

**Example output:**
```
Line 42: Cannot find name 'undefined_variable' (error)
Line 58: 'foo' is declared but never used (warning)
```

### 2. `lsp_goto_definition` - Jump to Definition

**When to use:** To find where a symbol is defined.

```
lsp_goto_definition(filePath: "/path/to/file.ts", line: 10, character: 15)
```

Returns the file and location where the symbol at that position is defined.

### 3. `lsp_find_references` - Find All Usages

**When to use:** Before refactoring to understand impact.

```
lsp_find_references(filePath: "/path/to/file.ts", line: 10, character: 15, includeDeclaration: true)
```

Returns all locations where the symbol is used across the workspace.

### 4. `lsp_rename` - Safe Refactoring

**When to use:** To rename a symbol across the entire codebase.

```
lsp_rename(filePath: "/path/to/file.ts", line: 10, character: 15, newName: "betterName")
```

Applies the rename across all files that reference the symbol.

## Validation Workflow

### After Writing Code

```
1. Write/edit code
2. Run lsp_diagnostics with severity: "error"
3. If errors found:
   - Fix the errors
   - Re-run diagnostics
4. Run lsp_diagnostics with severity: "warning"
5. Address warnings if appropriate
```

### Before Committing

```
1. Run lsp_diagnostics on all modified files
2. Ensure no errors
3. Review warnings
4. Proceed with commit only if clean
```

### Before Refactoring

```
1. Use lsp_find_references to understand impact
2. Review all usages
3. If safe, use lsp_rename for symbol renaming
4. Or manually edit with confidence knowing all locations
```

## Agent Integration

### Agents That MUST Use LSP

| Agent | LSP Usage |
|-------|-----------|
| **tdd-guide** | Run `lsp_diagnostics` after implementation |
| **code-reviewer** | Check for diagnostics during review |
| **build-error-resolver** | Use diagnostics to identify issues |
| **refactor-cleaner** | Use `lsp_find_references` before removing code |

### Agents That SHOULD Use LSP

| Agent | LSP Usage |
|-------|-----------|
| **orchestrator** | Verify no errors after delegated work |
| **architect** | Use `lsp_goto_definition` for codebase navigation |
| **security-reviewer** | Trace data flow with references |

## Best Practices

1. **Always validate after editing** - Run diagnostics after any code change
2. **Check before declaring done** - Ensure zero errors before completing a task
3. **Use references before deleting** - Never remove code without checking references
4. **Prefer lsp_rename over find-replace** - It's safer and handles all cases
5. **Check the right severity** - Use "error" for blockers, "warning" for quality

## Error Handling

If LSP is unavailable for a file type:
- Fall back to running the appropriate type checker (tsc, pyright, etc.)
- Use build commands to verify compilation
- Note the limitation in your response

## Supported Languages

The LSP tools work with any language that has a configured language server:
- TypeScript/JavaScript (tsserver)
- Python (pyright, pylsp)
- Go (gopls)
- Rust (rust-analyzer)
- And many more...
