---
name: lsp
description: Multi-language code navigation via persistent LSP daemons. Supports Python (pyright), TypeScript/JS, Rust, Go, C/C++, Bash, Java, CSS, HTML, JSON. Auto-detects language from file extension and lazy-starts the appropriate server. Use instead of grep for definitions, references, hover, symbols, and diagnostics.
metadata: {"clawdbot":{"emoji":"","requires":{"bins":["python3"]}}}
---

# LSP Code Navigation

Multi-language LSP client that manages per-language background daemons. Auto-detects the language from file extension and routes queries to the correct server. Each server lazy-starts on first use and idles out after 5 minutes of inactivity.

**Use this instead of grep/read when you need to:**
- Find where something is defined
- Find all usages of a symbol
- Get type signatures or docstrings
- List all classes/functions in a file
- Check for type errors before running code
- Search for a symbol across an entire workspace

## Supported Languages

| Language | Server | Extensions | Install |
|----------|--------|------------|---------|
| Python | `pyright-langserver` | .py, .pyi, .pyx | `npm install -g pyright` |
| TypeScript/JS | `typescript-language-server` | .ts, .tsx, .js, .jsx, .mjs, .cjs | `npm install -g typescript-language-server typescript` |
| Rust | `rust-analyzer` | .rs | `rustup component add rust-analyzer` |
| Go | `gopls` | .go | `go install golang.org/x/tools/gopls@latest` |
| C/C++ | `clangd` | .c, .h, .cpp, .cc, .hpp | `apt install clangd` or `brew install llvm` |
| Bash | `bash-language-server` | .sh, .bash, .zsh | `npm install -g bash-language-server` |
| Java | `jdtls` | .java | [eclipse.jdt.ls](https://github.com/eclipse-jdtls/eclipse.jdt.ls) |
| CSS | `vscode-css-language-server` | .css, .scss, .less | `npm install -g vscode-langservers-extracted` |
| HTML | `vscode-html-language-server` | .html, .htm | `npm install -g vscode-langservers-extracted` |
| JSON | `vscode-json-language-server` | .json, .jsonc | `npm install -g vscode-langservers-extracted` |

Only install the servers you need. The skill auto-detects which are available and reports helpful install commands for missing ones.

## Setup

### Prerequisites

- Python 3.10+ (for the client script itself -- stdlib only, no pip deps)
- At least one language server installed (see table above)

### Installation

The skill includes a Python script at `{baseDir}/scripts/lsp-query.py`. This is the LSP client -- it manages background daemons and handles all queries.

To make it callable as `lsp-query` from anywhere, symlink it into your PATH:

```bash
ln -sf {baseDir}/scripts/lsp-query.py /usr/local/bin/lsp-query
# or:
ln -sf {baseDir}/scripts/lsp-query.py ~/.npm-global/bin/lsp-query
```

Alternatively, invoke it directly:

```bash
{baseDir}/scripts/lsp-query.py <command> [args...]
```

### Configuration

Set `LSP_WORKSPACE` to the repo root before querying. If unset, defaults to the git root or cwd.

## Commands

All line and column numbers are **1-indexed** (human-friendly, matching editor display).

### Go to Definition

```bash
lsp-query definition /path/to/file.py <line> <col>
```

### Find References

```bash
lsp-query references /path/to/file.py <line> <col>
```

### Hover (Type Info)

```bash
lsp-query hover /path/to/file.py <line> <col>
```

### Document Symbols

```bash
lsp-query symbols /path/to/file.py
```

### Workspace Symbol Search

```bash
lsp-query workspace-symbols "ClassName"
```

### Diagnostics

```bash
lsp-query diagnostics /path/to/file.py
```

### Completions

```bash
lsp-query completions /path/to/file.py <line> <col>
```

### Signature Help

```bash
lsp-query signature /path/to/file.py <line> <col>
```

### Rename Preview

```bash
lsp-query rename /path/to/file.py <line> <col> new_name
```

### Server Management

```bash
lsp-query languages                    # Show all supported languages + install status
lsp-query servers                      # List running language daemons
lsp-query shutdown                     # Stop all daemons
lsp-query shutdown python              # Stop just the Python daemon
```

## What's Included

```
{baseDir}/
├── SKILL.md              # This file
└── scripts/
    └── lsp-query.py      # Python script -- multi-language LSP client + daemon manager
```

`lsp-query.py` is a self-contained Python script (~850 lines, stdlib only, no pip dependencies). It:
1. Forks a single background daemon process on first use
2. The daemon lazy-starts language servers as needed (e.g., pyright for .py, typescript-language-server for .ts)
3. Communicates with the daemon over a Unix socket (`~/.cache/lsp-query/daemon.sock`)
4. Translates CLI commands into LSP JSON-RPC requests and prints human-readable results
5. Each language server auto-stops after 5 minutes idle; the daemon itself stops when all servers are idle

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LSP_WORKSPACE` | git root or cwd | Workspace root for LSP servers |
| `LSP_SERVER` | auto per language | Override server command for ALL languages |
| `LSP_LANG` | auto from extension | Force a specific language (bypass detection) |
| `LSP_TIMEOUT` | `300` | Server idle timeout in seconds |
| `LSP_SOCK` | `~/.cache/lsp-query/daemon.sock` | Unix socket path |

## Examples

```bash
export LSP_WORKSPACE=/path/to/repo

# Python
lsp-query symbols src/model.py
lsp-query hover src/model.py 42 10
lsp-query references src/model.py 42 10

# TypeScript (auto-detected from .ts extension)
lsp-query symbols src/index.ts
lsp-query definition src/app.tsx 15 8

# Rust
lsp-query symbols src/main.rs
lsp-query diagnostics src/lib.rs

# Check what's available
lsp-query languages
lsp-query servers
```

## Troubleshooting

- **"Server not found for X"**: The language server binary isn't installed. The error message includes the install command.
- **"could not connect to LSP daemon"**: Daemon failed to start. Verify Python 3.10+ is available.
- **Import errors in diagnostics**: Expected when packages aren't installed in the current Python environment. These resolve on machines with the correct venv.
- **Stale results**: Run `lsp-query shutdown` to restart all servers fresh.
- **Slow first query per language**: Each server takes 1-2 seconds to cold-start. Subsequent queries to the same language are ~200ms.
- **Wrong language detected**: Use `LSP_LANG=rust lsp-query symbols myfile` to force.
