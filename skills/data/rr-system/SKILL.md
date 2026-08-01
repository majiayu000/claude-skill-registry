---
name: rr-system
description: System setup, tool information, and AI configuration management for development
  environments. Use when setting up new machines, explaining available tools (shell-config,
  ai-rules, wt), managing AI ass
---

---
name: rr-system
description: System setup, tool information, and AI configuration management for development environments. Use when setting up new machines, explaining available tools (shell-config, ai-rules, wt), managing AI assistant configurations (Claude/Codex/Gemini/OpenCode), checking system configuration, or troubleshooting environment issues. Also triggers when working with configuration files (.json, .toml, .fish, .zsh, .bash), Brewfiles, or installation scripts. Example triggers: "Set up my development environment", "Install tools on new machine", "Configure AI assistant", "What tools do I have?", "Update my shell config", "Add MCP server to Claude", "Check system configuration"
---

# System Setup & Configuration

Comprehensive system setup automation and tool reference for the rr- development environment. Provides automated installation scripts, AI configuration management, and modern CLI tools for macOS and Linux.

**⚠️ IMPORTANT: ALWAYS CHECK OFFICIAL DOCUMENTATION ONLINE**

Tools evolve rapidly. Before providing commands or configuration changes:

1. Load `references/tools-reference.md` for official documentation URLs
2. Search online for latest official documentation
3. Verify CLI options and flags are current
4. Use official docs as source of truth - this skill may be outdated

## When to Use This Skill

- Setting up new macOS or Linux machines
- Explaining available tools (shell commands, aliases, modern CLI tools)
- Managing AI assistant configurations (Claude Code, Codex, Gemini, OpenCode)
- Editing, validating, or updating AI configuration files
- Adding/removing MCP servers across AI platforms
- Checking if tool or configuration exists
- Troubleshooting environment issues
- Updating existing installations

## Progress Reporting Requirements

**CRITICAL: Provide continuous progress updates for all installation tasks.**

**Before ANY task:**

1. Use TodoWrite tool to create task list
2. Explain what you're about to do
3. Show exact command you'll run

**During execution:**

1. Report real-time progress
2. Show relevant output
3. Explain warnings/errors immediately

**After each step:**

1. Mark task as completed
2. Summarize accomplishments
3. Note issues or next steps

**Never run commands silently** - always inform user what and why.

## Quick Installation

**Complete 4-step setup on macOS or Linux:**

```bash
cd .claude/skills/rr-system

# 1. Install tools (includes Homebrew)
bash scripts/install-tools.sh

# 2. Upgrade all packages (MANDATORY)
brew upgrade

# 3. Install shell configs
bash scripts/install-shell-config.sh

# 4. Install AI configs
bash scripts/install-ai-configs.sh

# 5. Restart terminal
```

**For detailed instructions, see `references/installation-guide.md`**

## Core Capabilities

### 1. System Installation

**4 automated scripts for zero-interaction setup:**

**install-tools.sh** - Development tools via Homebrew

- Installs Homebrew (macOS & Linux)
- CLI tools from `Brewfile` (cross-platform)
- macOS apps from `Brewfile.macos` (auto-skipped on Linux)
- Verifies critical tools installed

**brew upgrade** - MANDATORY after installing Homebrew

- Upgrades all packages to latest versions
- Ensures security patches and features
- Must run before other installation scripts

**install-shell-config.sh** - Shell configurations

- Fish/Zsh/Bash configs with modular conf.d structure
- Starship prompt + Ghostty terminal (macOS)
- wt function (Fish only - git worktree manager)
- Registers shells in /etc/shells (requires sudo)
- Fixes Zsh permissions (requires sudo)
- Enables Touch ID for sudo (macOS, requires sudo)

**install-ai-configs.sh** - AI assistant configurations

- Claude Code, Codex, Gemini, OpenCode configs
- Validates JSON/TOML syntax
- Creates directories, overwrites existing configs

All scripts are idempotent (safe to run multiple times) with automatic verification.

### 2. Brewfile Structure

**Two Brewfiles for organized package management:**

**`Brewfile`** - Shared CLI tools (macOS & Linux):

- Shells (Fish, Zsh, Bash)
- Modern CLI (bat, eza, fd, ripgrep, fzf, jq, yq, btop)
- Development (git, neovim, node, go, python, mkcert)
- Cloud (AWS, Azure, GCloud, kubectl, helm, k9s)
- Terminal (tmux, zellij, lazygit, lazydocker)
- AI CLIs (gemini-cli, opencode)

**`Brewfile.macos`** - macOS-only applications:

- Password & Security (1Password, 1Password CLI)
- Communication (Slack, Zoom, Linear)
- Development (Cursor, Ghostty, Tower)
- AI Assistants (Claude, ChatGPT, Codex, Claude Code)
- Productivity (Raycast, Granola, Shottr)

**Adding tools:**

- Edit `Brewfile` for CLI: `brew "tool-name"`
- Edit `Brewfile.macos` for macOS apps: `cask "app-name"`
- Run: `bash scripts/install-tools.sh`

### 3. AI Configuration Management

Manage AI assistant configs with automated installation or manual editing.

**Supported platforms:**

- Claude Code (`~/.claude/settings.json`)
- Codex CLI (`~/.codex/config.toml`)
- Gemini CLI (`~/.gemini/settings.json`)
- OpenCode (`~/.config/opencode/opencode.json`)
- Cursor (`~/.cursor/mcp.json`)

**Quick install (recommended):**

```bash
bash scripts/install-ai-configs.sh
```

**Manual editing workflow:**

1. Read current config file
2. Reference `assets/ai-configs/<platform>-*` templates
3. Make changes with Edit tool
4. Validate syntax:
   - JSON: `jq empty <file>`
   - TOML: `python3 -c "import tomllib; tomllib.load(open('<file>', 'rb'))"`
5. Restart AI assistant

**Common tasks:**

- Add MCP server: Modify mcpServers section, validate, restart
- Update environment variables: Edit env section, validate, restart
- Modify hooks (Claude): Edit hooks array, validate, restart

**Feature Parity Principle:**

Maintain near-identical configs across all platforms:

- Keep same MCP servers on all platforms
- Adapt only syntax for each platform's format
- When adding/removing MCP servers, update ALL platforms
- Only deviate when feature unavailable or platform requires different approach

**For detailed schemas and patterns, see `references/ai-config-schemas.md`**

### 4. Tool Reference

**⚠️ Load `references/tools-reference.md` for complete documentation links**

Modern CLI tools installed:

- File operations: bat, eza, fd, ripgrep
- Development: neovim, lazygit, lazydocker, fzf, ast-grep
- Linting: actionlint, shellcheck
- Navigation: zoxide, atuin, direnv
- Version managers: fnm (Node.js), uv (Python)
- System: procs, hexyl, broot, git-delta, difftastic
- Cloud: kubectl, helm, gh, aws-cli, azure-cli, gcloud
- Blockchain: foundry (forge, cast, anvil, chisel)
- Terminal: tmux, zellij
- AI CLIs: Claude Code, OpenCode, Codex, Gemini CLI
- Package managers: Homebrew, Bun

**Configuration locations:**

- Fish: `~/.config/fish/` (config.fish + conf.d/)
- Zsh: `~/.zshrc` + `~/.config/zsh/conf.d/`
- Bash: `~/.bashrc`, `~/.bash_profile` + `~/.config/bash/conf.d/`
- Neovim: `~/.config/nvim/` (LazyVim with Catppuccin)
- Starship: `~/.config/starship.toml`
- Claude: `~/.claude/`
- Codex: `~/.codex/`
- Gemini: `~/.gemini/`
- Cursor: `~/.cursor/`

**Git Worktree Manager (wt):**

- Installation: Included in Fish config (via `install-shell-config.sh`)
- Location: `~/.config/fish/functions/wt.fish`
- Availability: Fish shell only (use `fish -c "wt <cmd>"` from bash/zsh)
- Commands: new, switch, list, remove, clean, status
- Auto package manager detection
- Storage: `~/.wt/<repo-name>/`

**Key aliases:**

- `ls` → `eza`, `cat` → `bat`, `grep` → `rg`
- File finder: `fd`
- Navigation: `z dirname`, `zi` (zoxide)
- Git: 60+ abbreviations (`g`, `ga`, `gc`, `gp`, `gl`, `gs`, etc.)
- Tools: `lzg` (lazygit), `lzd` (lazydocker), `ff` (fzf preview)

## Essential Workflows

### Setting Up New Machine

```bash
cd .claude/skills/rr-system

# 1. Install development tools (includes Homebrew)
bash scripts/install-tools.sh

# 2. Upgrade all packages (MANDATORY)
brew upgrade

# 3. Install shell configs
bash scripts/install-shell-config.sh

# 4. Install AI configs
bash scripts/install-ai-configs.sh

# 5. Restart terminal, then:
fish                              # Start Fish shell
chsh -s $(which fish)            # Optional: make Fish default
```

**Verify:**

```bash
bat --version
fish --version
ls ~/.config/fish/config.fish
ls ~/.claude/settings.json
fish -c "wt help"
```

### Updating Existing Installation

```bash
# ALWAYS upgrade Homebrew first (MANDATORY)
brew upgrade

# Then update components
bash scripts/install-tools.sh
bash scripts/install-shell-config.sh
bash scripts/install-ai-configs.sh

# Restart terminal
```

### Adding MCP Server to All Platforms

To maintain feature parity:

1. Load `references/ai-config-schemas.md` for formats
2. For each platform (Claude, Codex, Gemini, OpenCode):
   - Read current config
   - Add server definition (adapt syntax for platform)
   - Validate: JSON (`jq empty`), TOML (`python3 tomllib`)
3. Verify all 4 configs have server
4. Restart each AI assistant
5. Test server on each platform

### Checking System Status

**Verify tool installation:**

```bash
command -v <tool>                # Check if exists
which <tool>                     # Show location
<tool> --version                 # Check version
```

**For wt (Fish function):**

```bash
ls ~/.config/fish/functions/wt.fish   # Check file exists
fish -c "wt help"                      # Test from any shell
```

**Check configurations:**

```bash
# Shell configs
ls ~/.config/fish/conf.d/
ls ~/.config/zsh/conf.d/

# AI configs
ls ~/.claude/settings.json
ls ~/.codex/config.toml
```

## Troubleshooting

### Homebrew

**Not in PATH (macOS):**

```bash
# Apple Silicon
eval "$(/opt/homebrew/bin/brew shellenv)"

# Intel
eval "$(/usr/local/bin/brew shellenv)"
```

### Shell

**Shell not found:**

```bash
sudo sh -c "echo $(which fish) >> /etc/shells"
sudo sh -c "echo $(which zsh) >> /etc/shells"
```

**Config not loading:**

```bash
source ~/.config/fish/config.fish    # Fish
source ~/.zshrc                      # Zsh
source ~/.bashrc                     # Bash
```

### Tools

**Tool not working:**

```bash
command -v <tool>                    # Check exists
brew list | grep <tool>              # Check installed
brew reinstall <tool>                # Reinstall
source ~/.config/fish/config.fish    # Reload config
```

### wt

**Command not found:**

```bash
ls ~/.config/fish/functions/wt.fish  # Check file
fish -c "wt help"                    # Test from any shell
fish                                 # Or switch to Fish
wt help
```

**Note:** wt is Fish-only. Use `fish -c "wt <cmd>"` from bash/zsh.

### AI Configs

**Syntax error:**

```bash
# Validate JSON
jq empty ~/.claude/settings.json

# Validate TOML
python3 -c "import tomllib; tomllib.load(open('~/.codex/config.toml', 'rb'))"
```

**Common errors:**

- Trailing commas (JSON)
- Missing quotes around keys
- Mismatched brackets/braces
- Unescaped special characters

**Config missing:**

```bash
bash scripts/install-ai-configs.sh   # Reinstall
```

**For detailed troubleshooting, see `references/installation-guide.md`**

## Best Practices

### Installation

- Run scripts in order: tools → brew upgrade → shell → AI
- Always `brew upgrade` after installing Homebrew
- Restart terminal after installation

### Shell Selection

- **Fish (recommended):** Best autosuggestions, modular structure, wt integration
- **Zsh:** Good plugin ecosystem, bash-compatible
- **Bash:** Universal compatibility, enhanced features

### Tool Usage

- Use modern alternatives: `bat` (cat), `eza` (ls), `rg` (grep), `fd` (find)
- Use `z` instead of `cd` for frequent directories
- Use `wt` for git worktrees (Fish only)

## Resources

**⚠️ ALWAYS START WITH OFFICIAL DOCUMENTATION**

Before using skill resources:

1. Load `references/tools-reference.md` for official doc URLs
2. Search online for current documentation
3. Verify commands with official sources
4. Use skill as baseline only - official docs are source of truth

### references/

- `installation-guide.md` - Complete installation instructions, troubleshooting, verification
- `tools-reference.md` - Official documentation URLs, quick reference (verify online first)
- `ai-config-schemas.md` - Config schemas, MCP patterns, validation, merge strategies

### scripts/

- `install-tools.sh` - Install development tools via Homebrew
- `install-shell-config.sh` - Install shell configurations
- `install-ai-configs.sh` - Install AI assistant configurations

All scripts are idempotent with verification.

### assets/

- `Brewfile` - CLI tools package list (cross-platform)
- `Brewfile.macos` - macOS-only applications
- `ai-configs/` - AI configuration templates
- `shell-config/` - Shell configuration files

## Common Scenarios

**"What tools do I have?"**

- Load `references/tools-reference.md` for organized list by category

**"How do I install on new machine?"**

- Run 4 scripts in order (see Quick Installation)
- Restart terminal, verify with `bat --version`, `fish`, `wt help`

**"How do I update everything?"**

- Run `brew upgrade` (MANDATORY first step)
- Run all install scripts
- Restart terminal

**"Where is X configured?"**

- Shell: `~/.config/<shell>/`
- AI: `~/.claude/`, `~/.codex/`, `~/.gemini/`
- Neovim: `~/.config/nvim/`
- Starship: `~/.config/starship.toml`

**"Tool not working after install?"**

- Check PATH: `command -v <tool>`
- Reload config: `source ~/.config/fish/config.fish`
- Reinstall: `brew reinstall <tool>`
- For wt: Check `~/.config/fish/functions/wt.fish`, use `fish -c "wt help"`
