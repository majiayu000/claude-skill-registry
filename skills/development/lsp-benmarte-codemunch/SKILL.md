---
description: Use Language Server Protocol operations directly for precise cross-file navigation. Find all references to a symbol, go to definition, get hover documentation, and rename symbols across the codebase. Only available when a language server is configured for the project language.
---

# LSP Direct Operations Skill

Use Claude Code's built-in `/lsp` tool for operations that require semantic understanding of the code — not just text matching.

## Pre-flight

```bash
# Check LSP config exists for this language
cat .claude/codemunch/config.json | jq '.engines'

# Verify Claude Code LSP tool is available
# Claude Code exposes /lsp for language server operations
```

If no LSP is configured for the file's language, fall back to ripgrep for references and skip hover/type info.

---

## Operation: Find all references

Find every place a symbol is used across the entire codebase.

```
/lsp tool call:
  method: textDocument/references
  params: {
    textDocument: { uri: "file:///path/to/file.ts" },
    position: { line: 141, character: 10 },  ← cursor on the symbol name
    context: { includeDeclaration: false }
  }
```

Format results compactly — do NOT read any of the reference files:
```
14 references to validateToken:

  src/api/auth.ts:23           → authRouter.post('/login', validateToken, loginHandler)
  src/api/invoices.ts:45       → export const getInvoice = [validateToken, async (req, res) =>
  src/api/invoices.ts:67       → export const createInvoice = [validateToken, async (req, res) =>
  src/middleware/index.ts:12   → app.use('/api', validateToken)
  ...
  tests/auth.test.ts:34        → await validateToken('expired-token')
  tests/auth.test.ts:56        → const result = await validateToken(mockToken)

Tokens used: ~45  (vs reading 14 files: ~42,000 tokens)
```

---

## Operation: Go to definition

Jump to where a symbol is defined, even if it's in a dependency or different file.

```
/lsp tool call:
  method: textDocument/definition
  params: {
    textDocument: { uri: "file:///path/to/file.ts" },
    position: { line: 23, character: 15 }
  }
```

Then use the fetch skill to read only that definition — not the whole file.

---

## Operation: Hover / documentation

Get the type signature and JSDoc/docstring for any symbol.

```
/lsp tool call:
  method: textDocument/hover
  params: {
    textDocument: { uri: "file:///path/to/file.ts" },
    position: { line: 141, character: 10 }
  }
```

Returns:
```
validateToken(token: string): Promise<User | null>

Validates a JWT token and returns the associated User, or null if invalid.
Throws TokenExpiredError if the token has expired.

@param token - JWT token string
@returns Promise resolving to User object or null
```

Token cost: ~15 tokens. No file read required.

---

## Operation: Rename symbol (cross-file)

Safely rename a symbol everywhere it's used.

```
/lsp tool call:
  method: textDocument/rename
  params: {
    textDocument: { uri: "file:///path/to/file.ts" },
    position: { line: 141, character: 10 },
    newName: "verifyToken"
  }
```

Returns a `WorkspaceEdit` with all files and positions to update. Apply with confirmation.

---

## Operation: Document outline

Get all symbols in a file without reading the file content.

```
/lsp tool call:
  method: textDocument/documentSymbol
  params: {
    textDocument: { uri: "file:///path/to/file.ts" }
  }
```

Returns full symbol tree with ranges. Use this to understand a file's structure in ~10 tokens.

---

## Ripgrep fallback for references (no LSP)

When LSP is unavailable, use ripgrep to find references by text:

```bash
SYMBOL="validateToken"
rg --json "$SYMBOL" \
  --glob "!node_modules" \
  --glob "!.git" \
  --glob "!.claude/codemunch" \
  | jq -r 'select(.type=="match") | "\(.data.path.text):\(.data.line_number)  \(.data.lines.text | rtrimstr("\n"))"' \
  | head -30
```

Less precise than LSP (will match strings, comments, and variable names containing the symbol), but works for any language.
