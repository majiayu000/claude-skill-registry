---
description: Detect which Language Server Protocol (LSP) servers are available for the current project and configure codemunch to use them. Checks for installed language servers across all major languages and writes the LSP config to .claude/codemunch/config.json.
---

# LSP Detection Skill

Detect available language servers and configure codemunch to use them for precise symbol extraction.

## Step 1 — Detect project languages

```bash
# Identify languages present in the project
find . -maxdepth 4 \( \
  -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
  -o -name "*.py" \
  -o -name "*.go" \
  -o -name "*.rs" \
  -o -name "*.rb" \
  -o -name "*.java" -o -name "*.kt" \
  -o -name "*.cs" \
  -o -name "*.cpp" -o -name "*.c" -o -name "*.h" \
  -o -name "*.php" \
  -o -name "*.swift" \
  -o -name "*.lua" \
  -o -name "*.zig" \
  -o -name "*.ex" -o -name "*.exs" \
  -o -name "*.hs" \
  -o -name "*.ml" -o -name "*.mli" \
\) -not -path "*/node_modules/*" -not -path "*/.git/*" \
  -not -path "*/target/*" -not -path "*/__pycache__/*" \
  2>/dev/null | \
  sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20
```

## Step 2 — Check for installed language servers

For each detected language, check if a server is installed:

```bash
# TypeScript / JavaScript
which typescript-language-server 2>/dev/null && echo "LSP:typescript=typescript-language-server --stdio"
which tsserver 2>/dev/null && echo "LSP:typescript-alt=tsserver"
# Check via npx as fallback
npx --yes typescript-language-server --version 2>/dev/null && echo "LSP:typescript-npx=npx typescript-language-server --stdio"

# Python
which pylsp 2>/dev/null && echo "LSP:python=pylsp"
which pyright-langserver 2>/dev/null && echo "LSP:python=pyright-langserver --stdio"
which pyright 2>/dev/null && echo "LSP:python-alt=pyright --stdio"
which jedi-language-server 2>/dev/null && echo "LSP:python-alt2=jedi-language-server"

# Go
which gopls 2>/dev/null && echo "LSP:go=gopls"

# Rust
which rust-analyzer 2>/dev/null && echo "LSP:rust=rust-analyzer"

# Ruby
which solargraph 2>/dev/null && echo "LSP:ruby=solargraph stdio"
which ruby-lsp 2>/dev/null && echo "LSP:ruby-alt=ruby-lsp"

# Java
which jdtls 2>/dev/null && echo "LSP:java=jdtls"
which java-language-server 2>/dev/null && echo "LSP:java-alt=java-language-server"

# Kotlin
which kotlin-language-server 2>/dev/null && echo "LSP:kotlin=kotlin-language-server"

# C / C++
which clangd 2>/dev/null && echo "LSP:c=clangd"
which ccls 2>/dev/null && echo "LSP:c-alt=ccls"

# C#
which omnisharp 2>/dev/null && echo "LSP:csharp=omnisharp -lsp"
which csharp-ls 2>/dev/null && echo "LSP:csharp-alt=csharp-ls"

# PHP
which phpactor 2>/dev/null && echo "LSP:php=phpactor language-server"
which intelephense 2>/dev/null && echo "LSP:php-alt=intelephense --stdio"

# Swift
which sourcekit-lsp 2>/dev/null && echo "LSP:swift=sourcekit-lsp"

# Lua
which lua-language-server 2>/dev/null && echo "LSP:lua=lua-language-server"

# Zig
which zls 2>/dev/null && echo "LSP:zig=zls"

# Elixir
which elixir-ls 2>/dev/null && echo "LSP:elixir=elixir-ls"
which lexical 2>/dev/null && echo "LSP:elixir-alt=lexical"

# Haskell
which haskell-language-server 2>/dev/null && echo "LSP:haskell=haskell-language-server-wrapper --lsp"
which haskell-language-server-wrapper 2>/dev/null && echo "LSP:haskell=haskell-language-server-wrapper --lsp"

# OCaml
which ocamllsp 2>/dev/null && echo "LSP:ocaml=ocamllsp"

# Bash / Shell
which bash-language-server 2>/dev/null && echo "LSP:bash=bash-language-server start"

# YAML
which yaml-language-server 2>/dev/null && echo "LSP:yaml=yaml-language-server --stdio"

# JSON
which vscode-json-language-server 2>/dev/null && echo "LSP:json=vscode-json-language-server --stdio"

# CSS / HTML
which vscode-css-language-server 2>/dev/null && echo "LSP:css=vscode-css-language-server --stdio"
which vscode-html-language-server 2>/dev/null && echo "LSP:html=vscode-html-language-server --stdio"
```

## Step 3 — Check for ctags fallback

```bash
which universal-ctags 2>/dev/null && echo "CTAGS=universal-ctags"
which ctags 2>/dev/null && ctags --version 2>&1 | grep -q "Universal" && echo "CTAGS=ctags (universal)"
which ctags 2>/dev/null && echo "CTAGS=ctags (exuberant or basic)"
```

## Step 4 — Check for ripgrep

```bash
which rg 2>/dev/null && echo "RG=rg $(rg --version | head -1)"
which grep 2>/dev/null && echo "GREP=grep (fallback)"
```

## Step 5 — Write .claude/codemunch/config.json

Create or update `.claude/codemunch/config.json` in the project root:

```json
{
  "version": "1.0",
  "engines": {
    "[language]": {
      "primary": "lsp",
      "lsp_cmd": "[detected command]",
      "fallback": "ctags",
      "last_resort": "rg"
    }
  },
  "index_path": ".claude/codemunch/index.json",
  "last_indexed": null,
  "stats": {
    "total_symbols": 0,
    "files_indexed": 0
  }
}
```

Add one entry per detected language. For languages with no LSP, set `primary` to `ctags` or `rg` directly.

## Step 6 — Report to user

```
✅ codemunch LSP detection complete

Engines configured:
  TypeScript   → typescript-language-server (LSP) ✅
  Python       → pylsp (LSP) ✅
  Go           → gopls (LSP) ✅
  Rust         → rust-analyzer (LSP) ✅

Fallback chain for unlisted languages:
  ctags        → [installed ✅ / not found ⚠️]
  ripgrep      → [installed ✅ / not found ⚠️]

Run /codemunch:index to build the symbol index.
```

If a language has no LSP and ctags is missing, suggest install commands:
- macOS: `brew install universal-ctags ripgrep`
- Ubuntu/Debian: `apt install universal-ctags ripgrep`
- Windows: `scoop install ctags ripgrep`
