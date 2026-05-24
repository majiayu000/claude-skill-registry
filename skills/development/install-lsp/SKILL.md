---
name: install-lsp
description: Install and configure LSP (Language Server Protocol) for Claude Code to enable go-to-definition, find-references, and real-time diagnostics
argument-hint: "[native|cclsp] [--language <lang>]"
---

# Install LSP for Claude Code

Enable Language Server Protocol integration to give Claude Code IDE-like code intelligence: go-to-definition, find-references, rename-symbol, and real-time diagnostics.

## Why LSP?

LSP provides semantic code understanding instead of text-based grep searches:
- **50ms** to find function call sites with LSP vs **45 seconds** with text search
- Exact symbol locations with line/column numbers
- Cross-file navigation and refactoring support

## Setup Options

### Option 1: Native LSP Tool (Recommended)

Claude Code has built-in LSP support that requires activation.

**Enable permanently** (add to `~/.zshrc` or `~/.bashrc`):
```bash
export ENABLE_LSP_TOOL=1
```

**Install language plugins** from the community marketplace:
```bash
# Add the LSP plugin marketplace
/plugin marketplace add boostvolt/claude-code-lsps

# Install language-specific plugins
/plugin install pyright@claude-code-lsps        # Python
/plugin install vtsls@claude-code-lsps          # TypeScript/JavaScript
/plugin install gopls@claude-code-lsps          # Go
/plugin install rust-analyzer@claude-code-lsps  # Rust
/plugin install clangd@claude-code-lsps         # C/C++
/plugin install jdtls@claude-code-lsps          # Java
/plugin install omnisharp@claude-code-lsps      # C#
/plugin install intelephense@claude-code-lsps   # PHP
/plugin install kotlin-language-server@claude-code-lsps  # Kotlin
/plugin install solargraph@claude-code-lsps     # Ruby
/plugin install vscode-html-css@claude-code-lsps # HTML/CSS
```

### Option 2: cclsp MCP Server

Community MCP server with interactive setup wizard.

**Automated setup**:
```bash
npx cclsp@latest setup          # Project-level config
npx cclsp@latest setup --user   # User-wide config
```

The wizard:
1. Scans project files to detect languages
2. Pre-selects appropriate LSP servers
3. Shows installation instructions for each server
4. Optionally auto-installs LSP binaries
5. Configures MCP integration

## LSP Server Requirements by Language

| Language | Binary | Installation |
|----------|--------|--------------|
| **Python** | pyright | `pip install pyright` or `npm i -g pyright` |
| **TypeScript/JS** | vtsls | `npm i -g @vtsls/language-server typescript` |
| **Go** | gopls | `go install golang.org/x/tools/gopls@latest` |
| **Rust** | rust-analyzer | `rustup component add rust-analyzer` |
| **C/C++** | clangd | `brew install llvm` or `xcode-select --install` |
| **Java** | jdtls | `brew install jdtls` (requires Java 21+) |
| **C#** | omnisharp | `brew install omnisharp/omnisharp-roslyn/omnisharp-mono` |
| **PHP** | intelephense | `npm i -g intelephense` |
| **Kotlin** | kotlin-language-server | `brew install kotlin-language-server` |
| **Ruby** | solargraph | `gem install solargraph` |
| **HTML/CSS** | vscode-langservers | `npm i -g vscode-langservers-extracted` |

## cclsp Configuration File

Location: `.claude/cclsp.json` (project) or `~/.config/claude/cclsp.json` (global)

```json
{
  "servers": [
    {
      "extensions": ["py", "pyi"],
      "command": ["pyright-langserver", "--stdio"],
      "rootDir": ".",
      "restartInterval": 30
    },
    {
      "extensions": ["ts", "tsx", "js", "jsx"],
      "command": ["typescript-language-server", "--stdio"],
      "rootDir": "."
    }
  ]
}
```

## Available LSP Tools

After setup, Claude Code gains these capabilities:

| Tool | Description |
|------|-------------|
| `find_definition` | Navigate to symbol definition |
| `find_references` | Find all usages of a symbol |
| `rename_symbol` | Rename symbol across all files |
| `get_diagnostics` | Get type errors and warnings |
| `restart_server` | Restart the language server |

## Troubleshooting

### "No LSP server available for file type"
```bash
# Verify plugin is installed
/plugin

# Reinstall if needed
/plugin uninstall pyright@claude-code-lsps
/plugin install pyright@claude-code-lsps
```

### "Executable not found in $PATH"
```bash
# Check binary exists
which pyright
which gopls

# For Go, ensure GOPATH/bin is in PATH
export PATH=$PATH:$(go env GOPATH)/bin
```

### Plugin installed but inactive
```bash
# Clear cache and reinstall
rm -rf ~/.claude/plugins/cache
/plugin install pyright@claude-code-lsps
```

### Windows Users
Use `cmd /c` wrapper for cclsp:
```json
{
  "servers": [{
    "extensions": ["py"],
    "command": ["cmd", "/c", "pyright-langserver", "--stdio"]
  }]
}
```

## Verification

After setup, test by asking Claude Code to:
- "Go to definition of `functionName`"
- "Find all references to `ClassName`"
- "Show diagnostics for this file"

A working setup provides exact file:line locations instead of grep-based text search results.

## Best Practice

Combine LSP with traditional search:
- **Use LSP** for: go-to-definition, diagnostics, rename
- **Use Grep** for: find all usages, text patterns, comments

LSP provides precision; Grep provides coverage.

## Execution Instructions

When the user runs this command:

1. **Determine approach** from arguments:
   - `native` - Use built-in LSP tool with plugins
   - `cclsp` - Use cclsp MCP server
   - No argument - Ask user which approach they prefer

2. **For native approach**:
   - Check if `ENABLE_LSP_TOOL` is already set
   - Add marketplace if not present
   - Install requested language plugin(s)
   - Verify with `/plugin` command

3. **For cclsp approach**:
   - Run `npx cclsp@latest setup` interactively
   - Guide user through language server installation
   - Verify MCP server is added with `/mcp`

4. **Inform user** to restart Claude Code after installation

## Sources

- [cclsp GitHub](https://github.com/ktnyt/cclsp)
- [Claude Code LSP Setup Guide](https://www.aifreeapi.com/en/posts/claude-code-lsp)
