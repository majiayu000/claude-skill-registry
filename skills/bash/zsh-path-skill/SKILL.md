---
name: zsh-path-skill
description: Manage and troubleshoot PATH configuration in zsh. Use when adding tools to PATH (bun, nvm, Python venv, cargo, go), diagnosing "command not found" errors, validating PATH entries, or organizing shell configuration in .zshrc and .zshrc.local files.
---

# Zsh PATH Management Skill

This skill provides comprehensive guidance for managing PATH environment variables in zsh, including troubleshooting missing commands, adding new tools, and organizing shell configuration.

## When to Use This Skill

Use this skill when:
- Getting "command not found" errors for installed tools
- Adding new tools to PATH (bun, nvm, cargo, go, Python venv, etc.)
- Validating and auditing current PATH entries
- Organizing PATH configuration between .zshrc and .zshrc.local
- Troubleshooting shell startup issues related to PATH
- Setting up version managers (nvm, pyenv, rbenv)

## Diagnostic Commands

### Check Current PATH

```bash
# List all PATH entries
echo $PATH | tr ':' '\n'

# Check if specific command is in PATH
which bun 2>/dev/null || echo "bun not found in PATH"

# Find where a command is installed
command -v node
type -a python
```

### Validate PATH Entries

```bash
# Check for broken/non-existent PATH entries
echo $PATH | tr ':' '\n' | while read p; do
  [[ -d "$p" ]] || echo "MISSING: $p"
done

# Check for duplicate PATH entries
echo $PATH | tr ':' '\n' | sort | uniq -d
```

## Common Tool PATH Configurations

### Bun (JavaScript runtime)

```bash
# Add to .zshrc
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
```

Default location: `~/.bun/bin/bun`

### NVM (Node Version Manager)

```bash
# Add to .zshrc
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

Default location: `~/.nvm/`

**Note:** NVM is a shell function, not a binary. It modifies PATH dynamically to point to the active Node version.

### Python Virtual Environment

```bash
# Add to .zshrc for global tools venv
export PATH="$HOME/.venv/tools3/bin:$PATH"

# For pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

### Rust/Cargo

```bash
# Add to .zshrc
export PATH="$HOME/.cargo/bin:$PATH"
```

### Go

```bash
# Add to .zshrc
export GOPATH="$HOME/go"
export PATH="$GOPATH/bin:$PATH"
```

### Homebrew (macOS)

```bash
# Intel Mac
export PATH="/usr/local/bin:$PATH"

# Apple Silicon Mac
export PATH="/opt/homebrew/bin:$PATH"
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Local bin directories

```bash
# User-local binaries
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/bin:$PATH"
```

## File Organization Best Practices

### .zshrc (Team/Shared Configuration)

Keep in .zshrc:
- Oh My Zsh configuration
- Common team aliases
- Standard PATH additions (homebrew, local bin)
- Plugin configuration

```bash
# ===== ZSH-TOOL MANAGED SECTION BEGIN =====
# Team-wide PATH modifications
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/bin:$PATH"

# Bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
# ===== ZSH-TOOL MANAGED SECTION END =====

# Load local customizations
[[ -f ~/.zshrc.local ]] && source ~/.zshrc.local
```

### .zshrc.local (Personal/Machine-Specific)

Keep in .zshrc.local:
- Machine-specific PATH entries
- Personal tool configurations
- Experimental settings
- Integrations that may override keybindings

```bash
# Machine-specific tools
export PATH="/opt/custom-tool/bin:$PATH"

# Personal integrations
if command -v atuin >/dev/null 2>&1; then
  eval "$(atuin init zsh)"
fi
```

## PATH Order Matters

PATH is searched left-to-right. First match wins.

```bash
# This order means ~/.local/bin takes priority over system bins
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"
```

### Recommended PATH Order

1. Project-specific bins (added by direnv)
2. User local bins (`~/.local/bin`, `~/bin`)
3. Language version managers (nvm, pyenv, rbenv)
4. Package managers (homebrew, cargo)
5. System paths (`/usr/local/bin`, `/usr/bin`)

## Troubleshooting

### Command Not Found After Installation

```bash
# 1. Find where tool was installed
ls -la ~/.bun/bin/bun 2>/dev/null
ls -la ~/.cargo/bin/rustc 2>/dev/null
ls -la ~/.nvm/versions/node/*/bin/node 2>/dev/null

# 2. Check if PATH includes the directory
echo $PATH | tr ':' '\n' | grep -E "(bun|cargo|nvm)"

# 3. Add missing PATH entry to .zshrc

# 4. Reload shell
source ~/.zshrc
# or
exec $SHELL
```

### PATH Changes Not Taking Effect

```bash
# Check which file sets the variable
grep -r "export PATH" ~/.zshrc ~/.zshrc.local ~/.zprofile 2>/dev/null

# Source the correct file
source ~/.zshrc

# Or start fresh shell
exec $SHELL
```

### Startup Hook Errors

Common causes:
- Missing PATH entries for tools used in hooks
- Broken references to non-existent directories
- Version managers not finding expected versions

```bash
# Debug startup
zsh -x 2>&1 | head -100

# Check for errors in specific config
bash -n ~/.zshrc
```

### Duplicate PATH Entries

```bash
# Remove duplicates (add to .zshrc)
typeset -U PATH path
```

## Verification Commands

After making PATH changes:

```bash
# Reload configuration
source ~/.zshrc

# Verify tool is accessible
which bun && bun --version
which node && node --version
command -v nvm && nvm --version

# Verify PATH includes new entries
echo $PATH | tr ':' '\n' | grep -E "(bun|nvm|venv)"
```

## Quick Reference

| Tool | PATH Entry | Check Command |
|------|------------|---------------|
| bun | `$HOME/.bun/bin` | `bun --version` |
| nvm | `$NVM_DIR/versions/node/*/bin` | `nvm --version` |
| cargo | `$HOME/.cargo/bin` | `cargo --version` |
| go | `$GOPATH/bin` | `go version` |
| pyenv | `$PYENV_ROOT/bin` | `pyenv --version` |
| brew (ARM) | `/opt/homebrew/bin` | `brew --version` |
| brew (Intel) | `/usr/local/bin` | `brew --version` |

## Common Patterns

### Conditional PATH Addition

```bash
# Only add if directory exists
[[ -d "$HOME/.bun/bin" ]] && export PATH="$HOME/.bun/bin:$PATH"

# Only add if command not already available
command -v bun >/dev/null || export PATH="$HOME/.bun/bin:$PATH"
```

### Lazy Loading for Faster Startup

```bash
# Lazy load nvm (faster shell startup)
lazy_load_nvm() {
  unset -f nvm node npm npx
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
}
nvm() { lazy_load_nvm && nvm "$@"; }
node() { lazy_load_nvm && node "$@"; }
npm() { lazy_load_nvm && npm "$@"; }
npx() { lazy_load_nvm && npx "$@"; }
```
