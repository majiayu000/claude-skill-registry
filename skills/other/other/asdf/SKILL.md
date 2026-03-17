---
name: asdf
description: Use this skill whenever the user wants to install, configure, or use asdf (asdf-vm), the universal version manager. Trigger for any mention of asdf, .tool-versions files, managing runtime versions, switching between versions of Node.js, Python, Ruby, Go, Terraform, kubectl, Java, Erlang, Elixir, or any other tool managed by asdf. Also trigger when migrating from nvm, pyenv, rbenv, goenv, tfenv, or similar single-language version managers. Use this skill for help with asdf plugins, asdf install, asdf set/global/local, troubleshooting shims, Fish/Bash/Zsh shell configuration, and multi-project version isolation workflows.
license: MIT
compatibility: opencode
---

# asdf Version Manager Skill

asdf is a universal CLI version manager — one tool to replace nvm, pyenv, rbenv, tfenv, goenv and more. It manages per-project versions via `.tool-versions` files and switches versions automatically as you navigate directories.

---

## When to Use This Skill

Use this skill when the user is:

- **Installing or setting up asdf** on a new machine (any OS, any shell)
- **Adding plugins** for a language or tool (Node.js, Python, Go, Terraform, kubectl, Helm, etc.)
- **Installing or switching versions** of any tool managed by asdf
- **Managing `.tool-versions` files** — creating, editing, or understanding version resolution
- **Migrating from single-language version managers** like nvm, pyenv, rbenv, goenv, tfenv, or sdkman
- **Configuring shell integration** for Bash, Zsh, Fish, or Elvish
- **Debugging version resolution** — wrong version active, shims not working, `command not found` errors
- **Onboarding to a project** that uses `.tool-versions` for reproducible environments
- **Setting up CI/CD pipelines** that need deterministic tool versions via asdf
- **Configuring `.asdfrc`** for legacy file support, concurrency, or plugin repository settings

---

## Core Concepts

- **Plugin**: Adapter for a specific tool (nodejs, python, terraform, kubectl, etc.)
- **Tool**: The actual runtime/binary managed (e.g., Node.js 20.11.0)
- **.tool-versions**: Project-level file declaring exact versions; asdf resolves it by traversing up the directory tree to `$HOME`
- **Shims**: Lightweight wrappers in `~/.asdf/shims/` that intercept tool invocations and dispatch to the right version
- **Version scopes**: project (`.tool-versions` in cwd) → parent dirs → `$HOME/.tool-versions` → env var `ASDF_${TOOL}_VERSION`

---

## Installation

### Dependencies (all platforms)

```bash
# Debian/Ubuntu
sudo apt install -y git curl

# macOS
brew install git curl
```

### Install asdf binary (recommended: binary download)

```bash
# Download latest release from https://github.com/asdf-vm/asdf/releases
# Or via git clone (classic method):
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.16.7
```

### Shell Configuration

**Fish shell** (Jean-Jacques' setup):

```fish
# Add to ~/.config/fish/config.fish
source ~/.asdf/asdf.fish

# Install completions
mkdir -p ~/.config/fish/completions
ln -s ~/.asdf/completions/asdf.fish ~/.config/fish/completions/asdf.fish
```

**Bash**:

```bash
# Add to ~/.bashrc or ~/.bash_profile
. "$HOME/.asdf/asdf.sh"
. "$HOME/.asdf/completions/asdf.bash"
```

**Zsh**:

```zsh
# Add to ~/.zshrc
. "$HOME/.asdf/asdf.sh"
```

After configuration, restart shell or `source` the config file.

---

## Essential Commands

### Plugin Management

```bash
asdf plugin list all              # Browse all available plugins
asdf plugin list all | grep terra # Search for specific plugins
asdf plugin add nodejs            # Add plugin by shortname (from registry)
asdf plugin add nodejs https://github.com/asdf-vm/asdf-nodejs.git  # Add by URL
asdf plugin list                  # List installed plugins
asdf plugin update nodejs         # Update a plugin
asdf plugin update --all          # Update all plugins
asdf plugin remove nodejs         # Remove plugin + all its installs
```

### Version Management

```bash
asdf list all nodejs              # List all installable versions
asdf list all nodejs 20           # List versions matching prefix
asdf install nodejs latest        # Install latest version
asdf install nodejs 20.11.0       # Install specific version
asdf install                      # Install all versions in .tool-versions
asdf list nodejs                  # List installed versions
asdf uninstall nodejs 18.0.0      # Remove a version
```

### Setting Versions

```bash
asdf set nodejs 20.11.0           # Set version in ./.tool-versions (project)
asdf set -u nodejs 20.11.0        # Set version in ~/.tool-versions (global/user default)
asdf set -p nodejs 20.11.0        # Set in nearest parent .tool-versions
asdf set nodejs latest            # Resolve and write latest version
asdf current                      # Show active version for all tools in cwd
asdf current nodejs               # Show active version for one tool
asdf where nodejs                 # Show install path for active version
asdf which node                   # Show shim path for a command
```

> **Note**: `asdf set` replaced the older `asdf local` / `asdf global` commands in asdf v0.15+. Both still work but `asdf set` is the modern API.

### Environment Variable Override

```bash
# Temporarily override without editing .tool-versions
ASDF_NODEJS_VERSION=18.0.0 node --version
```

---

## .tool-versions Format

```
nodejs 20.11.0
python 3.12.2
terraform 1.7.4
kubectl 1.29.2
golang 1.22.1
```

- One tool per line, `<name> <version>`
- Multiple versions separated by spaces (fallback chain): `python 3.12.2 2.7.18`
- Special keywords: `system` (use OS-installed version), `path:~/my/custom/build`
- Commit to version control — this is the contract for the project's tool versions

---

## .asdfrc Configuration

Located at `~/.asdfrc`:

```ini
# Support .nvmrc, .ruby-version, etc. (per-plugin support required)
legacy_version_file = yes

# Keep downloaded archives (useful for slow connections)
always_keep_download = no

# Concurrency for parallel installs
concurrency = auto

# Plugin repository refresh interval in minutes
plugin_repository_last_check_duration = 60
```

---

## Common Plugins for DevOps/Cloud (Jean-Jacques' stack)

| Tool | Plugin add command |
|------|-------------------|
| Node.js | `asdf plugin add nodejs` |
| Python | `asdf plugin add python` |
| Go | `asdf plugin add golang` |
| Terraform | `asdf plugin add terraform` |
| kubectl | `asdf plugin add kubectl` |
| Helm | `asdf plugin add helm` |
| gcloud CLI | `asdf plugin add gcloud` |
| Skaffold | `asdf plugin add skaffold` |
| Java | `asdf plugin add java` |
| Ruby | `asdf plugin add ruby` |
| Erlang | `asdf plugin add erlang` |
| Elixir | `asdf plugin add elixir` |

Many plugins may require system dependencies — always check the plugin's README before installing.

---

## Migration from Other Version Managers

Enable legacy file support in `~/.asdfrc`:

```ini
legacy_version_file = yes
```

| Old file | Tool |
|----------|------|
| `.nvmrc` | nodejs (via asdf-nodejs) |
| `.node-version` | nodejs |
| `.ruby-version` | ruby (via asdf-ruby) |
| `.python-version` | python (via asdf-python) |

---

## Troubleshooting

### Shims not working / command not found

```bash
asdf reshim nodejs          # Regenerate shims for a plugin
asdf reshim                 # Regenerate all shims
echo $PATH                  # Verify ~/.asdf/shims is early in PATH
type -a node                # Fish: check which binary is resolved
```

### Version not being picked up

```bash
asdf current                # See what version is resolved and from where
# Look for "No version set" warnings
# Check .tool-versions exists in project dir or a parent
```

### Plugin install failures

- Check plugin README for system dependency requirements
- Ensure git is installed and accessible
- For nodejs: may need `gnupg` for keyring verification

### Data directory

Default: `~/.asdf/` — override with `export ASDF_DATA_DIR=/custom/path` in shell config.

---

## Typical Project Onboarding Workflow

```bash
# 1. Clone project
git clone <repo> && cd <repo>

# 2. Add plugins for each tool in .tool-versions (if not already added)
asdf plugin add nodejs
asdf plugin add python

# 3. Install all versions specified in .tool-versions
asdf install

# 4. Verify
asdf current
```

---

## Reference

- Full docs: https://asdf-vm.com/
- Plugin list: https://github.com/asdf-vm/asdf-plugins
- All commands: `asdf --help` or `asdf <command> --help`
