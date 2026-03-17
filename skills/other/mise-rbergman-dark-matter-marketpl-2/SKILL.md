---
name: mise
description: Modern dev tool version management with mise. Use PROACTIVELY when setting up repos, managing tool versions, or when users ask about nvm/pyenv/goenv alternatives. Covers project setup, direnv integration, and CI/CD patterns.
---

# Mise: Modern Dev Tool Management

[Mise](https://mise.jdx.dev) is a polyglot version manager that replaces nvm, pyenv, rbenv, and most Homebrew CLI tools with a single, fast, declarative system.

**Related skills:**
- **just-pro** - Build system setup (includes mise integration patterns)
- **cli-tools** - Power CLI tools (many installable via mise)

## Why Mise?

| Problem | Old Way | Mise Way |
|---------|---------|----------|
| Node versions | nvm, fnm, volta | `mise use node@22` |
| Python versions | pyenv, conda | `mise use python@3.12` |
| Go versions | goenv, manual | `mise use go@1.25` |
| CLI tools | Homebrew | `mise use jq ripgrep bat` |
| Per-project versions | `.nvmrc` + `.python-version` + ... | Single `.mise.toml` |

**Benefits:**
- 1000+ tools available (`mise registry | wc -l`)
- Parallel installs, prebuilt binaries
- Works on macOS and Linux
- Declarative config in repo = reproducible environments

---

## Quick Start

### Install Mise

```bash
curl https://mise.run | sh
```

### Shell Setup

Add to your shell rc file. If using both mise and direnv (recommended), load mise first:

```bash
# ~/.zshrc - recommended order
eval "$(mise activate zsh)"
eval "$(direnv hook zsh)"

# fish: ~/.config/fish/config.fish
mise activate fish | source
direnv hook fish | source
```

For faster startup, use shims instead of (or with) activation:

```bash
# zsh: add to ~/.zshrc
export PATH="$HOME/.local/share/mise/shims:$PATH"
eval "$(mise activate zsh)"
eval "$(direnv hook zsh)"

# fish: add to ~/.config/fish/config.fish
fish_add_path -p ~/.local/share/mise/shims
mise activate fish | source
direnv hook fish | source
```

### Install Tools

```bash
mise use node@22 python@3.12 go@latest  # Current directory
mise use -g jq ripgrep bat              # Global (all directories)
```

---

## Project Setup

### New Repo

```bash
# Pin language versions
mise use node@22 go@1.25

# Creates .mise.toml - commit it
git add .mise.toml
```

### Existing Repo (first clone)

```bash
mise trust      # Allow repo's .mise.toml
mise install    # Install pinned tools
```

### Example `.mise.toml`

```toml
[tools]
node = "22"
go = "1.25"
python = "3.12"

# Project-specific tools
just = "latest"
sqlc = "latest"
```

---

## Configuration Hierarchy

Mise merges configs from multiple levels:

```
~/.config/mise/config.toml     # Global defaults
  └── ~/projects/.mise.toml    # Workspace defaults
        └── ~/projects/foo/.mise.toml  # Project-specific
```

More specific configs override less specific ones.

### Global Config (`~/.config/mise/config.toml`)

Your daily-driver tools:

```toml
[tools]
# Languages
node = "lts"
python = "3.12"
go = "latest"

# CLI tools (replaces Homebrew)
jq = "latest"
yq = "latest"
ripgrep = "latest"
fd = "latest"
bat = "latest"
eza = "latest"
delta = "latest"
fzf = "latest"
gh = "latest"
lazygit = "latest"
just = "latest"
direnv = "latest"
starship = "latest"

[settings]
auto_install = true
```

---

## Direnv Integration

[Direnv](https://direnv.net) handles per-directory **environment variables**. Combined with mise:

- **Mise** → tool versions (node, go, python)
- **Direnv** → environment variables (DATABASE_URL, API keys)

> **Best Practice:** Keep a single source of truth:
> - `.mise.toml` → tool versions only (node, go, python)
> - `.envrc` → environment variables (DATABASE_URL, API_KEY, etc.)
>
> Don't use `[env]` section in `.mise.toml` - it creates confusion about where vars come from.

### Setup

1. Install direnv via mise:
   ```bash
   mise use -g direnv
   ```

2. Add direnv hook to shell rc:
   ```bash
   # zsh
   eval "$(direnv hook zsh)"

   # fish
   direnv hook fish | source
   ```

3. Create `.envrc` in your project:
   ```bash
   # Load mise tools for this directory
   if command -v mise &> /dev/null; then
     eval "$(mise hook-env -s bash)"
   fi

   # Project-specific environment
   export DATABASE_URL="postgres://localhost/myapp"
   export LOG_LEVEL="debug"
   ```

4. Allow the envrc:
   ```bash
   direnv allow
   ```

**Tip:** Use `.envrc.example` (committed) + `.envrc` (gitignored with secrets).

---

## Just Integration

[just](https://just.systems) and mise complement each other:
- **mise** → pins tool versions
- **just** → runs commands using those tools

**See the `just-pro` skill** for full patterns. Quick summary:

### Shell Override (recommended for teams)

```just
# Every recipe runs through mise automatically
set shell := ["mise", "exec", "--", "bash", "-c"]

build:
    npm run build

test:
    go test ./...
```

### Graceful Degradation (for open source)

```just
_exec cmd:
    #!/usr/bin/env bash
    if command -v mise &>/dev/null; then
        mise exec -- {{cmd}}
    else
        {{cmd}}
    fi

build: (_exec "npm run build")
```

### Setup Recipe

```just
setup:
    #!/usr/bin/env bash
    mise trust && mise install

    # Create .envrc from example if missing
    if [[ ! -f .envrc ]] && [[ -f .envrc.example ]]; then
        cp .envrc.example .envrc
        echo "Created .envrc from example - edit with your values"
        direnv allow
    fi

    echo "Toolchain ready"
```

---

## Mise vs Devcontainer

| Aspect | Mise + Direnv | Devcontainer |
|--------|---------------|--------------|
| **Isolation** | Shared host filesystem | Full container isolation |
| **Speed** | Native performance | Container overhead |
| **Setup time** | Seconds (`mise install`) | Minutes (image build) |
| **Works offline** | After first install | After first build |
| **IDE support** | Any editor, native | VS Code / JetBrains |
| **Team adoption** | Low friction | Requires Docker knowledge |
| **CI parity** | Good (mise in CI) | Excellent (same container) |

**Recommendation:** Use mise for fast local dev. Add devcontainer for hermetic reproducibility if needed. They're not mutually exclusive.

---

## Common Tools Available

```bash
mise registry | grep <tool>  # Search for a tool
```

| Category | Tools |
|----------|-------|
| **Languages** | node, python, go, rust, java, ruby, php, elixir, zig |
| **JSON/YAML** | jq, yq, gojq |
| **Search** | ripgrep, fd, fzf, ag |
| **Git** | gh, lazygit, delta, git-cliff |
| **Files** | bat, eza, tree, dust, duf |
| **HTTP** | httpie, curlie, xh |
| **Containers** | kubectl, helm, k9s, docker-compose |
| **Cloud** | awscli, terraform, opentofu, pulumi |
| **Dev** | just, make, watchexec, hyperfine |
| **Editors** | neovim, helix |

---

## Migration from Homebrew

**Keep in Homebrew:**
- `git` (system integration)
- Your shell (`fish`, `zsh`)
- GUI apps (casks)
- System utilities (`coreutils` if needed)

**Move to mise:**
- Language runtimes (node, python, go, rust)
- CLI dev tools (jq, ripgrep, bat, etc.)
- Cloud CLIs (awscli, kubectl, terraform)

```bash
# Check what mise can replace
brew leaves | while read pkg; do
  mise registry | grep -q "^$pkg " && echo "✓ $pkg"
done
```

---

## Troubleshooting

### Tools not in PATH

```bash
mise doctor  # Check activation status
```

Ensure mise activates **after** other PATH modifications in shell rc.

### Shims vs Activate

- **Shims** (`~/.local/share/mise/shims`): Wrapper scripts, always work
- **Activate**: Dynamic PATH modification, faster for frequent version switching

Use both for reliability:
```bash
# Shims first (fallback), then activate (dynamic)
export PATH="$HOME/.local/share/mise/shims:$PATH"
eval "$(mise activate zsh)"
```

### Direnv + Mise

Use `mise hook-env -s bash` in `.envrc`, not `mise activate`:
```bash
eval "$(mise hook-env -s bash)"  # Correct
eval "$(mise activate bash)"     # Wrong - generates shell hooks
```

---

## Quick Reference

```bash
# Install tools
mise use node@22              # Current directory
mise use -g ripgrep           # Global

# Manage versions
mise ls                       # List installed
mise ls-remote node           # Available versions
mise outdated                 # Check for updates

# Project setup
mise install                  # Install from .mise.toml
mise trust                    # Trust current directory's config

# Maintenance
mise prune                    # Remove unused versions
mise reshim                   # Rebuild shims
mise self-update              # Update mise itself
```

---

## Further Reading

- [Mise Documentation](https://mise.jdx.dev)
- [Mise Registry](https://mise.jdx.dev/registry.html) - All available tools
- [Direnv Documentation](https://direnv.net)
