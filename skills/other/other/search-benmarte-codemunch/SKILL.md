---
description: Search the codemunch index for symbols matching a name, pattern, kind (function/class/method), or file. Returns a compact list of matches with location and signature — no source code read until you fetch. Use this to explore unfamiliar codebases token-efficiently.
---

# Search Skill

Find symbols without reading any files. Returns a compact index listing.

## Search modes

### By name (exact or fuzzy)
```bash
# Exact
jq '[.symbols[] | select(.name == "validateToken")]' .claude/codemunch/index.json

# Case-insensitive
jq '[.symbols[] | select(.name | ascii_downcase | contains("validate"))]' .claude/codemunch/index.json

# Fuzzy: split query into chars and find symbols containing all of them in order
# e.g. "vt" matches "validateToken", "visitTree"
```

### By kind
```bash
# Find all classes
jq '[.symbols[] | select(.kind == "class")]' .claude/codemunch/index.json

# Find all exported functions
jq '[.symbols[] | select(.kind == "function")]' .claude/codemunch/index.json

# Kinds vary by language:
# TypeScript: function, class, method, property, interface, type, enum, constant, variable
# Python: function, class, method, variable
# Go: function, struct, interface, method, constant, variable, type
# Rust: function, struct, enum, trait, impl, method, constant, type
# Ruby: method, class, module, constant
# Java/Kotlin: class, interface, method, field, enum, constructor
# C/C++: function, class, struct, enum, method, field, typedef
```

### By file
```bash
jq --arg f "auth" '[.symbols[] | select(.file | contains($f))]' .claude/codemunch/index.json
```

### By container (class/module)
```bash
jq --arg c "AuthService" '[.symbols[] | select(.container == $c)]' .claude/codemunch/index.json
```

### Combined
```bash
# All methods in a specific class
jq --arg c "Invoice" --arg k "method" \
  '[.symbols[] | select(.container == $c and .kind == $k)]' \
  .claude/codemunch/index.json
```

## Output format

Always return a compact list — never the full source. Source is fetched separately with the fetch skill:

```
Found 6 symbols matching "validate":

  1.  validateToken        function   src/auth/tokens.ts:142       AuthService
  2.  validateInvoice      function   src/lib/validation.ts:89     —
  3.  validateAmount       function   src/lib/validation.ts:112    —
  4.  validateEmail        method     src/models/user.ts:34        UserModel
  5.  validateExpense      function   convex/expenses.ts:67        —
  6.  validateDateRange    function   src/utils/dates.ts:23        —

Use /codemunch:fetch <name> to read the source of any symbol.
Tokens used: 12  (vs reading 6 files: ~18,000 tokens)
```

## LSP-enhanced search (when available)

If LSP is configured, additionally offer:

**Workspace symbol search** — searches across the entire project including symbols not yet in the index:
```
Use Claude Code's /lsp tool:
  workspace/symbol
  query: "[search term]"
```

This is the most powerful mode — LSP returns every symbol in the project matching the query, with full type information, even in files not yet indexed.

## Smart exploration helpers

When searching an unfamiliar codebase, these compound searches help:

**"Show me the shape of this file"**
```bash
jq --arg f "$FILENAME" '[.symbols[] | select(.file == $f) | {name, kind, start_line, container}]' \
  .claude/codemunch/index.json | jq 'sort_by(.start_line)'
```

**"What are the entry points?"**
```bash
# Find exported/public top-level functions
jq '[.symbols[] | select(.kind == "function" and (.container == null or .container == ""))]' \
  .claude/codemunch/index.json
```

**"Show me the class hierarchy"**
```bash
jq '[.symbols[] | select(.kind == "class" or .kind == "interface" or .kind == "struct")] | 
  group_by(.file) | 
  map({file: .[0].file, types: map(.name)})' \
  .claude/codemunch/index.json
```
