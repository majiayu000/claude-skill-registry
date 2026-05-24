---
name: install-tool
description: "Use when a tool, CLI, or package is needed but not installed, or when the user asks to install/add a tool. Prefers mise for all installations."
argument-hint: "[tool[@version] | package-name...]"
model: haiku
allowed-tools:
  - Bash(mise search:*)
  - Bash(mise registry:*)
  - Bash(mise ls-remote:*)
  - Bash(mise tool:*)
  - Bash(mise ls:*)
  - Bash(mise backends:*)
  - Bash(mise use --dry-run:*)
  - Bash(mise which:*)
  - Bash(which:*)
  - Bash(command -v:*)
  - Bash(chezmoi source-path:*)
  - Bash(pwd:*)
  - Bash(realpath:*)
  - Read
  - Glob
  - Grep
---

# Install Tool

## Arguments
```
$ARGUMENTS
```

## Instructions

### 1. Identify the Tool

Parse the arguments for tool names and optional versions. If no version is specified, default to `@latest`.

### 2. Check If Already Installed

```bash
mise which <tool> 2>/dev/null || command -v <tool> 2>/dev/null
```

If the tool is already available, report its location and version. Stop unless the user explicitly wants a different version.

### 3. Search the Mise Registry

```bash
mise search <tool>
mise registry <tool>
```

- `mise search` — fuzzy-searches the registry for matching tools
- `mise registry <tool>` — shows the full backend path (e.g., `core:node`, `aqua:jqlang/jq`)

If no results, check alternate names or ask the user.

### 4. Choose Scope

**CRITICAL: Global installs must happen in dotfiles**

Before proceeding, determine if this is a global install:
- Arguments include `--global` or `-g`
- User explicitly asks for global install
- Tool is general-purpose (jq, ripgrep, etc.) and no local `mise.toml` exists

If global install is requested:

1. Check if we're in the chezmoi source directory:
```bash
chezmoi_source=$(chezmoi source-path 2>/dev/null)
current_dir=$(pwd)
# Check if current directory is within chezmoi source directory
```

2. If NOT in dotfiles (current dir not within `chezmoi source-path`):
   - **REFUSE the install**
   - Tell the user: "Global tool installs must be done from your dotfiles repository to ensure they're tracked and reproducible. Please run `chezmoi cd` first, then run `/install-tool` again."
   - Stop execution

3. If in dotfiles:
   - Proceed with `mise use --global`
   - This will update `home/dot_config/mise/config.toml` (the chezmoi source file)
   - Remind user to apply changes: `chezmoi apply ~/.config/mise/config.toml`

Decision tree for project-local installs:
- **Inside a project directory with `mise.toml`** → project-local (default)
- **No `mise.toml` exists** → create one with `mise use <tool>@<version>`

### 5. Preview the Install

Always dry-run first:

```bash
mise use --dry-run <tool>@<version>
```

Report what will be installed and where the config will be written.

### 6. Execute

```bash
# Project-local (default)
mise use <tool>@<version>

# Global (only from within dotfiles)
mise use --global <tool>@<version>
# Then apply via chezmoi:
chezmoi apply ~/.config/mise/config.toml

# Pinned exact version (project-local)
mise use --pin <tool>@<version>
```

After global install, remind the user that the tool is now configured in their dotfiles and will be available everywhere after chezmoi apply.

### 7. Verify

```bash
mise which <tool>
<tool> --version  # or equivalent
```

Confirm the tool is available and report the installed version.

## When Mise Cannot Provide the Tool

If `mise search` and `mise registry` return no results:

1. **Stop and tell the user** — do not fall back to brew/apt/npm/pipx
2. Suggest alternatives:
   - Check if it's available via a different name
   - Use `ubi` backend: `mise use ubi:owner/repo`
   - Use `aqua` backend: `mise use aqua:owner/repo`
   - Use language-specific backend (see reference below)
3. If mise truly cannot provide it, ask the user for approval before using any other installer

## Mise Discovery Subcommands

| Command | Purpose |
|---------|---------|
| `mise search <name>` | Fuzzy-search the tool registry |
| `mise registry <name>` | Show full backend path for a tool |
| `mise registry --backend <be>` | List all tools for a specific backend |
| `mise ls-remote <tool>` | List available versions for a tool |
| `mise ls-remote <tool>@<prefix>` | Filter versions by prefix (e.g., `node@20`) |
| `mise tool <name>` | Show info: backend, installed/active versions, config source |
| `mise ls` | List all installed and active tool versions |
| `mise backends ls` | List all available backends |

## Mise Backends Reference

| Backend | Prefix | Installs from | Example |
|---------|--------|---------------|---------|
| **core** | `core:` | Built-in support (node, python, go, etc.) | `mise use node@22` |
| **aqua** | `aqua:` | [aqua registry](https://github.com/aquaproj/aqua-registry) — GitHub releases | `mise use aqua:jqlang/jq` |
| **asdf** | `asdf:` | asdf plugin ecosystem | `mise use asdf:mise-plugins/mise-poetry` |
| **cargo** | `cargo:` | Rust crates (crates.io) | `mise use cargo:ripgrep` |
| **go** | `go:` | Go modules | `mise use go:golang.org/x/tools/gopls` |
| **npm** | `npm:` | npm packages | `mise use npm:prettier` |
| **pipx** | `pipx:` | Python packages (isolated envs) | `mise use pipx:black` |
| **gem** | `gem:` | Ruby gems | `mise use gem:rubocop` |
| **ubi** | `ubi:` | GitHub releases (universal) | `mise use ubi:BurntSushi/ripgrep` |
| **vfox** | `vfox:` | vfox plugin ecosystem | `mise use vfox:version-fox/vfox-node` |
| **conda** | `conda:` | Conda/mamba packages | `mise use conda:scipy` |
| **dotnet** | `dotnet:` | .NET tools | `mise use dotnet:fantomas` |
| **spm** | `spm:` | Swift packages | `mise use spm:nicklockwood/SwiftFormat` |
| **http** | `http:` | Direct URL download | `mise use http:https://example.com/tool.tar.gz` |

### Backend Selection Guide

1. **Check `mise search` first** — most tools have a default backend
2. **Core** for major languages (node, python, ruby, go, java, etc.)
3. **Aqua** for most CLI tools distributed as GitHub releases
4. **npm/pipx/cargo/go/gem** for language-ecosystem packages
5. **ubi** as a fallback for any GitHub release not in aqua

## Examples

```
/install-tool jq                      → search, preview, install jq
/install-tool node@22                 → install Node.js 22.x
/install-tool --global ripgrep        → install ripgrep globally
/install-tool terraform jq go         → install multiple tools
/install-tool cargo:stylua            → install via cargo backend
/install-tool ubi:BurntSushi/ripgrep  → install via ubi backend
```
