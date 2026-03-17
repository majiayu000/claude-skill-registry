---
name: using-lsp-tools
description: Use when mcp-language-server tools are available and you need semantic code intelligence for navigation, refactoring, or type analysis
---

# Using LSP Tools

<ROLE>
Language Tooling Expert. Reputation depends on leveraging semantic analysis over text matching for accurate, complete code navigation and refactoring.
</ROLE>

## Invariant Principles

1. **Semantic > Lexical**: LSP understands scope, types, inheritance. Grep sees text.
2. **LSP for Symbols, Grep for Strings**: Symbols = definitions, references, types. Strings = TODOs, comments, literals.
3. **Verify Before Fallback**: Empty LSP result? Check file saved. Then try text-based.
4. **Atomic Operations Preferred**: `rename_symbol` handles all files. Manual Edit misses references.

## Reasoning Schema

<analysis>
- Is target a symbol (function, class, variable) or literal text?
- Is LSP server active for this language?
- Does task need semantic understanding (types, scope, inheritance)?
</analysis>

<reflection>
- Did LSP return expected results? If empty: file saved? Feature supported?
- Did fallback find matches LSP missed? Indicates LSP limitation vs. saved state.
</reflection>

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `filePath` | Yes | Absolute path to file being analyzed |
| `line` | Context | 1-indexed line number for position-based queries |
| `column` | Context | 1-indexed column for position-based queries |
| `symbolName` | Context | Fully-qualified name for definition/references |
| `language` | No | Language identifier if ambiguous |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Symbol locations | Inline | File paths and positions from navigation queries |
| Type information | Inline | Hover/signature data for understanding |
| Refactoring edits | Applied | Direct code modifications from rename/actions |
| Diagnostics | Inline | Errors and warnings for debugging |

## Tool Priority Matrix

| Task | LSP Tool | Fallback |
|------|----------|----------|
| Find definition | `definition` | Grep `func X\|class X\|def X` |
| Find usages | `references` | Grep symbol name |
| Understand symbol | `hover` | Read + infer |
| Rename | `rename_symbol` | Multi-file Edit (risky) |
| File outline | `document_symbols` | Grep definitions |
| Callers | `call_hierarchy` incoming | Grep + analyze |
| Callees | `call_hierarchy` outgoing | Read function |
| Type hierarchy | `type_hierarchy` | Grep extends/implements |
| Workspace search | `workspace_symbol_resolve` | Glob + Grep |
| Refactorings | `code_actions` | Manual |
| Signature | `signature_help` | Hover or read |
| Diagnostics | `diagnostics` | Build command |
| Format | `format_document` | Formatter CLI |
| Edit by line | `edit_file` | Built-in Edit |

## Parameters

Required: `filePath` (absolute), `line`/`column` (1-indexed), `symbolName` (fully-qualified for definition/references).

## Decision Rules

**Use LSP when:**
- Finding true definition (not text match)
- Refactoring (rename, extract, inline)
- Understanding type relationships
- Finding semantic usages
- Cross-file navigation via imports

**Use Grep/Glob when:**
- Literal strings, comments, non-code text
- Regex patterns
- LSP returns empty but code exists
- Unsupported languages
- Non-symbols (TODOs, URLs, magic strings)

## Workflows

**Exploration:** `document_symbols` (structure) -> `hover` (types) -> `definition` (jump) -> `references` (usage)

**Refactoring:** `code_actions` (discover) -> `rename_symbol` (execute) OR `references` (assess impact) -> manual

**Type debugging:** `hover` (inferred) -> `type_hierarchy` (inheritance) -> `diagnostics` (errors)

**Call analysis:** `call_hierarchy` incoming = "who calls?" | outgoing = "what calls?"

## Anti-Patterns

<FORBIDDEN>
- Using Grep for symbol rename (misses scoped references, hits false positives)
- Skipping LSP for "simple" refactors (simple becomes complex with inheritance)
- Trusting empty LSP results without checking file saved state
- Manual multi-file edits when `rename_symbol` available
- Ignoring `diagnostics` output when debugging type errors
</FORBIDDEN>

## Fallback Protocol

1. LSP error/empty -> Check file saved (LSP reads disk)
2. Try table fallback
3. Persistent failure -> Feature unsupported by server

## Self-Check

Before completing:
- [ ] Used semantic LSP tool for symbol-based queries (not text search)
- [ ] Verified file saved if LSP returned empty/unexpected results
- [ ] Applied atomic refactoring operations where available
- [ ] Documented fallback rationale if LSP bypassed

If ANY unchecked: STOP and reconsider approach.
