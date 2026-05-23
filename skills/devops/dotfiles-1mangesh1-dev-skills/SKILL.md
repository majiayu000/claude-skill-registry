---
name: dotfiles
description: Dotfile management with stow, chezmoi, or git bare repo for configuration sync across machines. Use when user asks to "manage dotfiles", "sync configs", "setup dotfiles", "backup shell config", or organize configuration files.
---

# Dotfiles

Manage and sync configuration files across machines.

## GNU Stow (Simple)

### Setup

```bash
# Install
brew install stow  # macOS
apt install stow   # Ubuntu

# Create dotfiles directory
mkdir -p ~/dotfiles
cd ~/dotfiles
```

### Structure

```
~/dotfiles/
├── zsh/
│   └── .zshrc
├── git/
│   └── .gitconfig
├── nvim/
│   └── .config/
│       └── nvim/
│           └── init.lua
└── tmux/
    └── .tmux.conf
```

### Usage

```bash
cd ~/dotfiles

# Symlink one package
stow zsh

# Symlink all
stow */

# Unlink
stow -D zsh

# Restow (update)
stow -R zsh

# Target different directory
stow -t ~ zsh
```

## Chezmoi (Advanced)

### Setup

```bash
# Install
brew install chezmoi  # or sh -c "$(curl -fsLS get.chezmoi.io)"

# Initialize
chezmoi init

# Or from existing repo
chezmoi init https://github.com/user/dotfiles.git
```

### Basic Usage

```bash
# Add file
chezmoi add ~/.zshrc
chezmoi add ~/.config/nvim/init.lua

# Edit
chezmoi edit ~/.zshrc

# See changes
chezmoi diff

# Apply changes
chezmoi apply

# Update from repo
chezmoi update
```

### Templates

```bash
# ~/.local/share/chezmoi/dot_gitconfig.tmpl
[user]
    name = {{ .name }}
    email = {{ .email }}

# ~/.config/chezmoi/chezmoi.toml
[data]
    name = "John Doe"
    email = "john@example.com"
```

### Secrets

```bash
# Use 1Password
{{ onepasswordRead "op://Personal/GitHub/token" }}

# Use pass
{{ pass "github/token" }}

# Prompt for value
{{ promptString "Enter API key" }}
```

## Git Bare Repo

### Setup

```bash
# Initialize
git init --bare $HOME/.dotfiles

# Alias
alias dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'

# Ignore untracked
dotfiles config --local status.showUntrackedFiles no
```

### Usage

```bash
# Add files
dotfiles add ~/.zshrc
dotfiles commit -m "Add zshrc"
dotfiles push

# Clone to new machine
git clone --bare git@github.com:user/dotfiles.git $HOME/.dotfiles
alias dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
dotfiles checkout
```

### Shell Config

```bash
# Add to ~/.zshrc or ~/.bashrc
alias dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
```

## Common Dotfiles

### Essential Files

```
~/.zshrc or ~/.bashrc    # Shell config
~/.gitconfig             # Git config
~/.ssh/config            # SSH config
~/.tmux.conf             # Tmux config
~/.config/nvim/          # Neovim config
~/.config/starship.toml  # Starship prompt
```

### .gitconfig

```ini
[user]
    name = Your Name
    email = your@email.com
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    lg = log --oneline --graph
[core]
    editor = nvim
[init]
    defaultBranch = main
[pull]
    rebase = true
```

### .zshrc Essentials

```bash
# History
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt SHARE_HISTORY

# Aliases
alias ll='ls -la'
alias g='git'
alias dc='docker compose'

# Path
export PATH="$HOME/.local/bin:$PATH"

# Editor
export EDITOR='nvim'
```

## Bootstrap Script

```bash
#!/bin/bash
# bootstrap.sh

set -e

# Install dependencies
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install stow git neovim
fi

# Clone dotfiles
git clone https://github.com/user/dotfiles.git ~/dotfiles

# Stow all
cd ~/dotfiles
for dir in */; do
    stow "$dir"
done

echo "Dotfiles installed!"
```

## Best Practices

1. **Version control**: Always use git
2. **README**: Document setup steps
3. **Modular**: Separate by application
4. **Secrets**: Never commit secrets; use templates or secret managers
5. **Bootstrap**: Create setup script for new machines
