---
description: Build or refresh the codemunch symbol index for the current project. Walks every source file, extracts all symbols (functions, classes, methods, constants, types) with their exact file location and line range, and writes a fast-lookup index to .claude/codemunch/index.json. Uses LSP when available, falls back to ctags, then ripgrep patterns.
---

# Index Skill

Build the symbol index. Run once before using fetch or search, and re-run when code changes significantly.

## Pre-flight

```bash
# Check config exists
cat .claude/codemunch/config.json 2>/dev/null || echo "NOT_CONFIGURED"
# If missing, run detect-lsp skill first

# Create index directory
mkdir -p .claude/codemunch

# Add to gitignore
grep -q ".claude/codemunch" .gitignore 2>/dev/null || echo ".claude/codemunch" >> .gitignore
```

---

## Engine A — LSP Indexing (primary, when available)

LSP doesn't have a batch "index all files" API, but we can use it for on-demand precise symbol lookup. For the index build, use `textDocument/documentSymbol` on each file.

For each source file in the project:

```bash
# Get list of source files (respects .gitignore)
rg --files --type [lang] 2>/dev/null || \
  find . -name "*.[ext]" \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    -not -path "*/target/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/.claude/codemunch/*"
```

Use Claude Code's built-in LSP tool (`/lsp`) to call `textDocument/documentSymbol` for each file. This returns all symbols with:
- Name
- Kind (function, class, method, variable, constant, etc.)
- Range (start line, end line)
- Detail (type signature for typed languages)

**Filter noise kinds**: Skip noise kinds: constant, property, variable, enumerator. These inflate the index 15x without adding useful navigation value. Only keep symbols where kind is one of: function, method, class, interface, type, enum, namespace.

Store each kept symbol as:
```json
{
  "name": "validateToken",
  "kind": "function",
  "file": "src/auth/tokens.ts",
  "start_line": 142,
  "end_line": 163,
  "signature": "validateToken(token: string): Promise<User | null>",
  "container": "AuthService"
}
```

---

## Engine B — ctags Indexing (fallback)

When LSP is unavailable for a language:

```bash
# Universal ctags — generates precise symbol table
universal-ctags \
  --recurse \
  --output-format=json \
  --fields=+n+e+K+S \
  --extras=+q \
  --exclude=node_modules \
  --exclude=.git \
  --exclude=target \
  --exclude=__pycache__ \
  --exclude=.claude/codemunch \
  --languages=[detected_languages] \
  -f .claude/codemunch/ctags.json \
  . 2>/dev/null

# Parse ctags output into codemunch index format
# ctags JSON fields: name, path, pattern, kind, line, end, signature
# Filter: skip noise kinds (constant, property, variable, enumerator)
# Only keep: function, method, class, interface, type, enum, namespace
```

ctags supports 40+ languages natively:
ActionScript, Ada, Ant, Bash, C, C++, C#, Clojure, CoffeeScript, D, Elixir, Erlang, Fortran, Go, Groovy, Haskell, HTML, Java, JavaScript, JSON, Julia, Kotlin, Lisp, Lua, Make, Matlab, ObjectiveC, OCaml, Perl, PHP, PowerShell, Python, R, Rake, Ruby, Rust, Scala, Scheme, Shell, SQL, Swift, Tcl, TypeScript, Verilog, VHDL, Vim, YAML, Zig

```bash
# Verify ctags found symbols
wc -l .claude/codemunch/ctags.json
```

---

## Engine C — Ripgrep Pattern Indexing (last resort)

When neither LSP nor ctags is available. Uses language-aware regex patterns to find symbol declarations:

```bash
# TypeScript/JavaScript
rg --json "^(export\s+)?(async\s+)?function\s+(\w+)|^(export\s+)?(abstract\s+)?class\s+(\w+)|^\s+(async\s+)?(\w+)\s*\([^)]*\)\s*[:{]" \
  --type ts --type js \
  --glob "!node_modules" \
  --glob "!.git" \
  > .claude/codemunch/rg-ts.jsonl

# Python
rg --json "^(async\s+)?def\s+(\w+)|^class\s+(\w+)" \
  --type py \
  > .claude/codemunch/rg-py.jsonl

# Go
rg --json "^func\s+(\(.*?\)\s+)?(\w+)|^type\s+(\w+)\s+(struct|interface)" \
  --type go \
  > .claude/codemunch/rg-go.jsonl

# Rust
rg --json "^(pub(\(.*?\))?\s+)?(async\s+)?fn\s+(\w+)|^(pub(\(.*?\))?\s+)?(struct|enum|trait|impl)\s+(\w+)" \
  --type rust \
  > .claude/codemunch/rg-rs.jsonl

# Ruby
rg --json "^\s*(def\s+(\w+)|class\s+(\w+)|module\s+(\w+))" \
  --type ruby \
  > .claude/codemunch/rg-rb.jsonl

# Java/Kotlin
rg --json "(public|private|protected|internal)?\s*(static\s+)?\w+\s+(\w+)\s*\(" \
  --type java --type kotlin \
  > .claude/codemunch/rg-jvm.jsonl

# C/C++
rg --json "^\w[\w\s\*]+\s+(\w+)\s*\([^;]*\)\s*\{|^(class|struct|enum)\s+(\w+)" \
  --type c --type cpp \
  > .claude/codemunch/rg-c.jsonl

# PHP
rg --json "^(public|private|protected)?\s*(static\s+)?function\s+(\w+)|^class\s+(\w+)" \
  --type php \
  > .claude/codemunch/rg-php.jsonl
```

**Filter noise kinds**: Skip noise kinds: constant, property, variable, enumerator. These inflate the index 15x without adding useful navigation value. The rg patterns should only match function/class/interface/type declarations, not `const`/`let`/`var` assignments unless they are arrow functions. Only keep: function, method, class, interface, type, enum, namespace.

Parse the ripgrep JSONL output to extract symbol name, file, and line number. End line is estimated as start + average function length (20 lines) — this is the only imprecise step. LSP and ctags give exact end lines.

---

## Step: Build unified index

Merge results from whichever engines ran into a single `.claude/codemunch/index.json`:

```json
{
  "version": "2.0",
  "generated": "2026-03-11T02:14:00Z",
  "engine": "lsp|ctags|rg",
  "project_root": "/path/to/project",
  "stats": {
    "total_symbols": 1247,
    "files_indexed": 89,
    "languages": ["typescript", "python", "go"]
  },
  "file_hashes": {
    "src/auth/tokens.ts": "a3f2b1c",
    "src/lib/validation.ts": "e7d4f9a",
    "convex/expenses.ts": "b1c3d5e"
  },
  "symbols": [
    {
      "name": "validateToken",
      "kind": "function",
      "file": "src/auth/tokens.ts",
      "start_line": 142,
      "end_line": 163,
      "signature": "validateToken(token: string): Promise<User | null>",
      "container": "AuthService",
      "engine": "lsp"
    }
  ]
}
```

The `file_hashes` field maps each indexed file to its git blob hash (`git hash-object <file>`). This enables incremental re-indexing — only files whose hash changed need to be re-processed.

```bash
# Generate file hashes for all indexed files
for file in $(rg --files --type [lang]); do
  echo "\"$file\": \"$(git hash-object "$file" 2>/dev/null || md5 -q "$file")\""
done
```

Also build a fast name-lookup dictionary:
```json
{
  "validateToken": [0],
  "AuthService": [1, 5, 23],
  "getUserById": [2]
}
```
(values are indexes into the symbols array)

## Incremental mode

When called with a list of changed files (from the staleness-gate skill), only re-index those files:

1. Remove all symbols where `symbol.file` is in the changed file list
2. Run the engine pipeline (LSP → ctags → rg) on only the changed files
3. Append new symbols to the existing index
4. Update `file_hashes` for the changed files
5. Remove entries from `file_hashes` for deleted files
6. Update `generated` timestamp and `stats`

This is much faster than a full re-index for typical edits (1-5 files changed).

If more than 50 files have changed, fall back to a full re-index — it's faster than incremental at that scale.

---

## Report

```
✅ codemunch index built

  Files indexed:    89
  Symbols found:    1,247
  Engine used:      LSP (TypeScript), ctags (Python, Go), rg (Bash)
  Index size:       142 KB
  Index written to: .claude/codemunch/index.json

  Top files by symbol count:
    src/api/invoices.ts      — 34 symbols
    src/lib/auth.ts          — 28 symbols
    convex/schema.ts         — 19 symbols

Run /codemunch:find <name> to look up any symbol.
```
