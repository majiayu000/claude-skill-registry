---
name: dprint
description: Use when working with dprint formatter - configuration, plugins, CLI commands, editor integration, or global setup.
---

# dprint

Fast pluggable code formatter.

## Config Resolution

**CC Misconception:** "dprint is project-local only." **Wrong.** dprint supports:

1. **Ancestor lookup** - walks UP directory tree for `dprint.json`
2. **Global fallback** - `~/.config/dprint/dprint.json` (or `DPRINT_CONFIG_DIR`)
3. **Explicit path** - `dprint fmt -c /path/to/config.json`

| Discovery Mode | Behavior |
|----------------|----------|
| `--config-discovery=true` | Default: ancestor + global |
| `--config-discovery=global` | Global only |
| `--config-discovery=false` | Require explicit `-c` |

No config found anywhere → dprint errors.

## Plugins

Plugins are WASM files loaded via URL in `dprint.json`:

```json
{
  "plugins": [
    "https://plugins.dprint.dev/typescript-0.95.13.wasm",
    "https://plugins.dprint.dev/json-0.21.1.wasm",
    "https://plugins.dprint.dev/markdown-0.20.0.wasm"
  ]
}
```

**Common plugins:**
- `typescript` - TS/JS/JSX/TSX
- `json` - JSON/JSONC
- `markdown` - Markdown
- `toml` - TOML
- `g-plane/pretty_yaml` - YAML
- `g-plane/malva` - CSS/SCSS/Less
- `g-plane/pretty_graphql` - GraphQL

**Plugin config** - top-level keys match plugin name:

```json
{
  "typescript": { "quoteStyle": "preferSingle", "semiColons": "asi" },
  "markdown": { "lineWidth": 100, "textWrap": "maintain" }
}
```

**Update plugins:** Check https://plugins.dprint.dev for latest versions.

## CLI Commands

```bash
dprint fmt                    # Format files, write to disk
dprint check                  # Check if files need formatting (CI)
dprint fmt --diff             # Show diff without writing
dprint fmt --staged           # Format only git staged files
dprint fmt --stdin ts         # Format stdin as TypeScript
dprint fmt "src/**/*.ts"      # Format specific patterns
dprint init                   # Create dprint.json
dprint config update          # Update plugin versions
dprint clear-cache            # Clear plugin cache
dprint lsp                    # Start language server
```

## Editor Integration

### Zed

```json
{
  "formatter": {
    "external": {
      "command": "dprint",
      "arguments": ["fmt", "--stdin", "{buffer_path}"]
    }
  }
}
```

### VS Code

Install "dprint" extension. It uses dprint LSP automatically.

### Neovim

Use `null-ls` or `conform.nvim` with dprint as formatter.

## Dotfiles Pattern

For consistent formatting across all projects:

```bash
# 1. Create config in dotfiles
~/<dotfiles>/dprint/dprint.json

# 2. Set global config location (in shell rc)
export DPRINT_CONFIG_DIR="$HOME/<dotfiles>/dprint"

# Alternative: symlink to default location
mkdir -p ~/.config/dprint
ln -s ~/<dotfiles>/dprint/dprint.json ~/.config/dprint/dprint.json
```

Projects with local `dprint.json` override global. Projects without use global.

## Excludes

```json
{
  "excludes": [
    "**/node_modules",
    "**/*-lock.json",
    "**/dist",
    "**/build"
  ]
}
```

## Reference

```bash
dprint help              # All commands
dprint help fmt          # Format command options
dprint output-resolved-config  # Debug: show effective config
```
