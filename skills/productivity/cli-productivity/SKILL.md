---
name: cli-productivity
version: 1.0.0
description: Essential CLI tools and shell productivity patterns for efficient terminal workflows
author: workspace-hub
category: devtools
capabilities:
  - Shell aliases and functions
  - Modern CLI tools (jq, fzf, ripgrep, fd, bat, exa)
  - Pipeline patterns and data transformation
  - Fuzzy finding and interactive selection
  - History management and shell optimization
  - Integration workflows between tools
tools:
  - jq
  - fzf
  - ripgrep
  - fd
  - bat
  - exa
  - zoxide
  - starship
  - tmux
tags: [cli, shell, productivity, bash, zsh, terminal, tools]
platforms: [linux, macos]
related_skills:
  - docker
  - git-advanced
  - bash-cli-framework
---

# CLI Productivity Skill

Master essential CLI tools and shell patterns for efficient terminal workflows. This skill covers modern replacements for traditional Unix tools, fuzzy finding, pipeline patterns, and shell customization.

## When to Use This Skill

### USE when:
- Building efficient terminal workflows
- Processing text and JSON data
- Searching codebases quickly
- Navigating file systems efficiently
- Automating repetitive tasks
- Creating shell functions and aliases
- Building interactive scripts

### DON'T USE when:
- GUI-based workflows are more appropriate
- Processing binary data (use specialized tools)
- Complex data analysis (use Python/Pandas)
- Tasks requiring visual feedback

## Prerequisites

### Installation

**macOS (Homebrew):**
```bash
# Essential modern tools
brew install jq           # JSON processor
brew install fzf          # Fuzzy finder
brew install ripgrep      # Fast grep (rg)
brew install fd           # Fast find
brew install bat          # Better cat
brew install exa          # Better ls (or eza)
brew install zoxide       # Smart cd
brew install starship     # Shell prompt
brew install tmux         # Terminal multiplexer

# Install fzf keybindings
$(brew --prefix)/opt/fzf/install
```

**Linux (Ubuntu/Debian):**
```bash
# Update package list
sudo apt-get update

# Install from apt (may be older versions)
sudo apt-get install -y jq fzf ripgrep fd-find bat

# Note: fd is 'fdfind' on Debian/Ubuntu
sudo ln -s $(which fdfind) /usr/local/bin/fd

# bat may be 'batcat' on older systems
sudo ln -s $(which batcat) /usr/local/bin/bat

# Install exa/eza
sudo apt-get install -y exa  # or: cargo install eza

# Install zoxide
curl -sS https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | bash

# Install starship
curl -sS https://starship.rs/install.sh | sh
```

**Arch Linux:**
```bash
sudo pacman -S jq fzf ripgrep fd bat exa zoxide starship tmux
```

**Verification:**
```bash
# Verify installations
for cmd in jq fzf rg fd bat exa zoxide starship; do
    command -v $cmd && echo "$cmd: OK" || echo "$cmd: NOT FOUND"
done
```

## Core Capabilities

### 1. jq - JSON Processing

**Basic Operations:**
```bash
# Pretty print JSON
echo '{"name":"John","age":30}' | jq '.'

# Extract field
curl -s https://api.github.com/repos/nodejs/node | jq '.stargazers_count'

# Filter arrays
echo '[1,2,3,4,5]' | jq '.[] | select(. > 2)'

# Transform data
echo '{"first":"John","last":"Doe"}' | jq '{fullName: (.first + " " + .last)}'
```

**Common jq Patterns:**
```bash
# Extract multiple fields
jq '{name: .name, stars: .stargazers_count}'

# Array operations
jq '.items | length'                    # Count items
jq '.items | first'                     # First item
jq '.items | last'                      # Last item
jq '.items[0:5]'                        # Slice first 5

# Filtering
jq '.[] | select(.status == "active")'
jq '.[] | select(.count > 100)'
jq '.[] | select(.name | contains("test"))'

# Sorting
jq 'sort_by(.date)'
jq 'sort_by(.date) | reverse'

# Grouping
jq 'group_by(.category)'
jq 'group_by(.category) | map({key: .[0].category, count: length})'

# Mapping
jq '.[] | {id, name}'
jq 'map({id: .id, upper_name: (.name | ascii_upcase)})'
```

**Shell Functions for jq:**
```bash
# Pretty print JSON file
jqp() {
    jq '.' "$1" | bat --language json
}

# Extract field from JSON file
jqf() {
    local file="$1"
    local field="$2"
    jq -r ".$field" "$file"
}

# Count items in JSON array
jqcount() {
    jq 'if type == "array" then length else 1 end' "$1"
}

# Filter JSON by field value
jqfilter() {
    local file="$1"
    local field="$2"
    local value="$3"
    jq --arg val "$value" ".[] | select(.$field == \$val)" "$file"
}
```

### 2. fzf - Fuzzy Finder

**Basic Usage:**
```bash
# Find and edit file
vim $(fzf)

# Find with preview
fzf --preview 'bat --color=always {}'

# Multi-select
fzf --multi

# Filter with query
echo -e "apple\nbanana\norange" | fzf --query "an"
```

**fzf Configuration:**
```bash
# Add to ~/.bashrc or ~/.zshrc

# Default options
export FZF_DEFAULT_OPTS='
    --height 40%
    --layout=reverse
    --border
    --preview-window=right:50%:wrap
    --bind=ctrl-d:preview-page-down
    --bind=ctrl-u:preview-page-up
'

# Use fd for faster file finding
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'

# Preview settings
export FZF_CTRL_T_OPTS='--preview "bat --color=always --style=numbers --line-range=:500 {}"'
export FZF_ALT_C_OPTS='--preview "exa --tree --level=2 --color=always {}"'
```

**Powerful fzf Functions:**
```bash
# Fuzzy edit file
fe() {
    local file
    file=$(fzf --preview 'bat --color=always --style=numbers --line-range=:500 {}')
    [[ -n "$file" ]] && ${EDITOR:-vim} "$file"
}

# Fuzzy cd into directory
fcd() {
    local dir
    dir=$(fd --type d --hidden --follow --exclude .git | fzf --preview 'exa --tree --level=2 --color=always {}')
    [[ -n "$dir" ]] && cd "$dir"
}

# Fuzzy kill process
fkill() {
    local pid
    pid=$(ps aux | sed 1d | fzf --multi | awk '{print $2}')
    [[ -n "$pid" ]] && echo "$pid" | xargs kill -9
}

# Fuzzy git checkout branch
fco() {
    local branch
    branch=$(git branch -a --color=always | grep -v '/HEAD' | fzf --ansi | sed 's/^[* ]*//' | sed 's#remotes/origin/##')
    [[ -n "$branch" ]] && git checkout "$branch"
}

# Fuzzy git log
flog() {
    git log --oneline --color=always | fzf --ansi --preview 'git show --color=always {1}' | awk '{print $1}'
}

# Fuzzy history search
fh() {
    local cmd
    cmd=$(history | fzf --tac | sed 's/^[ ]*[0-9]*[ ]*//')
    [[ -n "$cmd" ]] && eval "$cmd"
}

# Fuzzy environment variable
fenv() {
    local var
    var=$(env | fzf | cut -d= -f1)
    [[ -n "$var" ]] && echo "${!var}"
}

# Fuzzy docker container
fdocker() {
    local container
    container=$(docker ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}' | fzf | awk '{print $1}')
    [[ -n "$container" ]] && docker exec -it "$container" sh
}
```

### 3. ripgrep (rg) - Fast Search

**Basic Usage:**
```bash
# Search for pattern
rg "function"

# Case insensitive
rg -i "error"

# Show line numbers
rg -n "TODO"

# Search specific file types
rg --type py "import"
rg -t js "require"

# Exclude patterns
rg "pattern" --glob '!*.min.js'
rg "pattern" --glob '!node_modules'
```

**Advanced ripgrep:**
```bash
# Context lines
rg -C 3 "error"        # 3 lines before and after
rg -B 2 "error"        # 2 lines before
rg -A 2 "error"        # 2 lines after

# Fixed strings (no regex)
rg -F "func()"

# Word boundaries
rg -w "log"            # Match "log" not "logging"

# Multiple patterns
rg -e "pattern1" -e "pattern2"

# Files matching pattern
rg -l "TODO"           # List files only
rg -c "TODO"           # Count matches per file

# Inverse match
rg -v "DEBUG"          # Lines NOT containing DEBUG

# Replace
rg "old" --replace "new"

# JSON output
rg --json "pattern" | jq '.'

# Statistics
rg --stats "pattern"
```

**ripgrep Functions:**
```bash
# Search and preview with fzf
rgs() {
    rg --color=always --line-number "$1" | fzf --ansi --preview 'bat --color=always $(echo {} | cut -d: -f1) --highlight-line $(echo {} | cut -d: -f2)'
}

# Search and open in editor
rge() {
    local selection
    selection=$(rg --color=always --line-number "$1" | fzf --ansi)
    if [[ -n "$selection" ]]; then
        local file=$(echo "$selection" | cut -d: -f1)
        local line=$(echo "$selection" | cut -d: -f2)
        ${EDITOR:-vim} "+$line" "$file"
    fi
}

# Search TODOs
todos() {
    rg --color=always "TODO|FIXME|HACK|XXX" "${1:-.}" | fzf --ansi
}

# Search function definitions
funcs() {
    rg --color=always "^(def |function |async function |const .* = |class )" "${1:-.}" | fzf --ansi
}
```

### 4. fd - Fast Find

**Basic Usage:**
```bash
# Find files by name
fd "readme"

# Find with extension
fd -e md
fd -e py -e js

# Find directories
fd -t d "src"

# Find files
fd -t f "config"

# Exclude patterns
fd -E node_modules -E .git

# Hidden files
fd -H "config"

# Execute command on results
fd -e log -x rm {}
fd -e py -x wc -l {}
```

**fd Functions:**
```bash
# Find and preview
fdp() {
    fd "$@" | fzf --preview 'bat --color=always {} 2>/dev/null || exa --tree --level=2 --color=always {}'
}

# Find and edit
fde() {
    local file
    file=$(fd -t f "$@" | fzf --preview 'bat --color=always {}')
    [[ -n "$file" ]] && ${EDITOR:-vim} "$file"
}

# Find large files
fdlarge() {
    local size="${1:-100M}"
    fd -t f -S +"$size" | xargs ls -lh | sort -k5 -h
}

# Find recent files
fdrecent() {
    local days="${1:-7}"
    fd -t f --changed-within "${days}d"
}

# Find duplicates by name
fddup() {
    fd -t f | sort | uniq -d
}
```

### 5. bat - Better cat

**Basic Usage:**
```bash
# Syntax highlighted output
bat file.py

# Show line numbers
bat -n file.py

# Show all non-printable chars
bat -A file.py

# Multiple files
bat file1.py file2.py

# Plain output (no decorations)
bat -p file.py

# Specific language
bat -l json data.txt

# Diff two files
bat --diff file1 file2
```

**bat Configuration:**
```bash
# Add to ~/.bashrc or ~/.zshrc

# Set bat as default pager
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
export PAGER="bat"

# Bat theme
export BAT_THEME="TwoDark"

# Bat style
export BAT_STYLE="numbers,changes,header"
```

**bat Aliases:**
```bash
# Replace cat with bat
alias cat='bat --paging=never'

# Preview alias for fzf
alias preview='fzf --preview "bat --color=always {}"'

# Pretty print JSON
alias json='bat -l json'

# Pretty print YAML
alias yaml='bat -l yaml'

# Diff with bat
alias diff='bat --diff'
```

### 6. exa/eza - Better ls

**Basic Usage:**
```bash
# Basic list
exa

# Long format
exa -l

# All files including hidden
exa -la

# Tree view
exa --tree
exa --tree --level=2

# Sort by modified
exa -l --sort=modified

# With git status
exa -l --git

# Group directories first
exa -l --group-directories-first

# Icons
exa -l --icons
```

**exa Aliases:**
```bash
# Add to ~/.bashrc or ~/.zshrc

# Replace ls with exa
alias ls='exa --group-directories-first'
alias ll='exa -l --group-directories-first --git'
alias la='exa -la --group-directories-first --git'
alias lt='exa --tree --level=2'
alias lta='exa --tree --level=2 -a'

# With icons (if supported)
alias li='exa -l --icons --group-directories-first --git'
```

### 7. zoxide - Smart cd

**Basic Usage:**
```bash
# Initialize (add to shell rc)
eval "$(zoxide init bash)"  # or zsh

# Use z instead of cd
z projects          # Jump to most frequent/recent match
z pro               # Partial match

# Interactive selection
zi                  # Opens fzf for selection

# Add directory manually
zoxide add /path/to/dir

# Query database
zoxide query projects
zoxide query -l     # List all entries
```

**zoxide Configuration:**
```bash
# Add to ~/.bashrc or ~/.zshrc

# Initialize zoxide
eval "$(zoxide init bash --cmd cd)"  # Replace cd

# Or use custom command
eval "$(zoxide init bash --cmd j)"   # Use 'j' for jump
```

### 8. Shell Aliases and Functions

**Essential Aliases:**
```bash
# Navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias ~='cd ~'
alias -- -='cd -'

# Safety
alias rm='rm -i'
alias mv='mv -i'
alias cp='cp -i'

# Shortcuts
alias c='clear'
alias h='history'
alias q='exit'
alias v='vim'
alias e='${EDITOR:-vim}'

# Git shortcuts
alias g='git'
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline -20'
alias gd='git diff'
alias gb='git branch'
alias gco='git checkout'

# Docker shortcuts
alias d='docker'
alias dc='docker compose'
alias dps='docker ps'
alias dimg='docker images'
alias dlog='docker logs -f'

# Common directories
alias proj='cd ~/projects'
alias docs='cd ~/Documents'
alias dl='cd ~/Downloads'
```

**Utility Functions:**
```bash
# Create directory and cd into it
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Extract any archive
extract() {
    if [[ -f "$1" ]]; then
        case "$1" in
            *.tar.bz2) tar xjf "$1" ;;
            *.tar.gz)  tar xzf "$1" ;;
            *.tar.xz)  tar xJf "$1" ;;
            *.bz2)     bunzip2 "$1" ;;
            *.rar)     unrar x "$1" ;;
            *.gz)      gunzip "$1" ;;
            *.tar)     tar xf "$1" ;;
            *.tbz2)    tar xjf "$1" ;;
            *.tgz)     tar xzf "$1" ;;
            *.zip)     unzip "$1" ;;
            *.Z)       uncompress "$1" ;;
            *.7z)      7z x "$1" ;;
            *)         echo "'$1' cannot be extracted" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}

# Get public IP
myip() {
    curl -s https://ifconfig.me
}

# Weather
weather() {
    curl -s "wttr.in/${1:-}"
}

# Quick note
note() {
    local notes_dir="${NOTES_DIR:-$HOME/notes}"
    local date=$(date +%Y-%m-%d)
    mkdir -p "$notes_dir"
    ${EDITOR:-vim} "$notes_dir/$date.md"
}

# Serve current directory
serve() {
    local port="${1:-8000}"
    python -m http.server "$port"
}

# Show disk usage for directory
duh() {
    du -h "${1:-.}" | sort -h | tail -20
}

# Find process by name
psg() {
    ps aux | grep -v grep | grep -i "$1"
}
```

## Integration Examples

### 1. Complete Shell Configuration

**~/.bashrc or ~/.zshrc:**
```bash
# ═══════════════════════════════════════════════════════════════
# CLI Productivity Configuration
# ═══════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────
# Environment
# ─────────────────────────────────────────────────────────────────

export EDITOR="vim"
export VISUAL="$EDITOR"
export PAGER="bat"
export MANPAGER="sh -c 'col -bx | bat -l man -p'"

# XDG Base Directory
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"

# ─────────────────────────────────────────────────────────────────
# History
# ─────────────────────────────────────────────────────────────────

HISTSIZE=50000
HISTFILESIZE=50000
HISTCONTROL=ignoreboth:erasedups
shopt -s histappend

# ─────────────────────────────────────────────────────────────────
# fzf Configuration
# ─────────────────────────────────────────────────────────────────

export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_DEFAULT_OPTS='
    --height 40%
    --layout=reverse
    --border
    --preview-window=right:50%:wrap
'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_CTRL_T_OPTS='--preview "bat --color=always --style=numbers --line-range=:500 {}"'
export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'
export FZF_ALT_C_OPTS='--preview "exa --tree --level=2 --color=always {}"'

# ─────────────────────────────────────────────────────────────────
# Tool Initialization
# ─────────────────────────────────────────────────────────────────

# fzf keybindings
[ -f ~/.fzf.bash ] && source ~/.fzf.bash

# zoxide
eval "$(zoxide init bash)"

# starship prompt
eval "$(starship init bash)"

# ─────────────────────────────────────────────────────────────────
# Aliases
# ─────────────────────────────────────────────────────────────────

# Modern replacements
alias ls='exa --group-directories-first'
alias ll='exa -l --group-directories-first --git'
alias la='exa -la --group-directories-first --git'
alias lt='exa --tree --level=2'
alias cat='bat --paging=never'
alias grep='rg'
alias find='fd'

# Navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# Git
alias g='git'
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline -20'
alias gd='git diff'

# Docker
alias d='docker'
alias dc='docker compose'
alias dps='docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'

# ─────────────────────────────────────────────────────────────────
# Functions
# ─────────────────────────────────────────────────────────────────

# Fuzzy edit
fe() {
    local file
    file=$(fzf --preview 'bat --color=always --style=numbers --line-range=:500 {}')
    [[ -n "$file" ]] && ${EDITOR:-vim} "$file"
}

# Fuzzy cd
fcd() {
    local dir
    dir=$(fd --type d | fzf --preview 'exa --tree --level=2 --color=always {}')
    [[ -n "$dir" ]] && cd "$dir"
}

# Search and edit
rge() {
    local selection
    selection=$(rg --color=always --line-number "$1" | fzf --ansi)
    if [[ -n "$selection" ]]; then
        local file=$(echo "$selection" | cut -d: -f1)
        local line=$(echo "$selection" | cut -d: -f2)
        ${EDITOR:-vim} "+$line" "$file"
    fi
}

# Create and cd
mkcd() {
    mkdir -p "$1" && cd "$1"
}
```

### 2. Data Processing Pipeline

```bash
# Process JSON API response
curl -s 'https://api.github.com/users/torvalds/repos?per_page=100' \
    | jq '.[] | {name: .name, stars: .stargazers_count}' \
    | jq -s 'sort_by(.stars) | reverse | .[0:10]'

# Find large log files and show preview
fd -e log -S +10M \
    | fzf --preview 'tail -100 {}' \
    | xargs -I{} bat --line-range=:50 {}

# Search code, preview matches, edit selected
rg --color=always -l "TODO" \
    | fzf --preview 'rg --color=always -C 3 "TODO" {}' \
    | xargs -o ${EDITOR:-vim}

# Git log with diff preview
git log --oneline --color=always \
    | fzf --ansi --preview 'git show --color=always {1}' \
    | awk '{print $1}' \
    | xargs git show
```

### 3. Interactive Script Template

```bash
#!/bin/bash
# ABOUTME: Interactive CLI script using fzf and modern tools
# ABOUTME: Template for building interactive shell tools

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# Check dependencies
check_deps() {
    local missing=()
    for cmd in fzf rg fd bat jq; do
        command -v "$cmd" >/dev/null || missing+=("$cmd")
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing dependencies: ${missing[*]}"
        exit 1
    fi
}

# Main menu using fzf
main_menu() {
    local options=(
        "Search files"
        "Search content"
        "Edit config"
        "Run tests"
        "Exit"
    )

    local selection
    selection=$(printf '%s\n' "${options[@]}" | fzf --header="Select action:")

    case "$selection" in
        "Search files") search_files ;;
        "Search content") search_content ;;
        "Edit config") edit_config ;;
        "Run tests") run_tests ;;
        "Exit") exit 0 ;;
    esac
}

search_files() {
    local file
    file=$(fd --type f | fzf --preview 'bat --color=always {}')
    [[ -n "$file" ]] && ${EDITOR:-vim} "$file"
}

search_content() {
    local query
    read -p "Search pattern: " query
    rge "$query"
}

edit_config() {
    local configs=("~/.bashrc" "~/.vimrc" "~/.gitconfig")
    local config
    config=$(printf '%s\n' "${configs[@]}" | fzf --header="Select config:")
    [[ -n "$config" ]] && ${EDITOR:-vim} "${config/#\~/$HOME}"
}

run_tests() {
    log_info "Running tests..."
    # Add test command here
}

# Main
check_deps
while true; do
    main_menu
done
```

## Best Practices

### 1. Tool Selection Guidelines

| Task | Tool | Why |
|------|------|-----|
| Find files by name | fd | Fast, intuitive syntax |
| Find files by content | rg | Faster than grep, better defaults |
| View files | bat | Syntax highlighting, line numbers |
| List files | exa | Icons, git status, tree view |
| Navigate directories | zoxide | Learns your patterns |
| Interactive selection | fzf | Fuzzy matching, preview |
| Process JSON | jq | Powerful, composable |

### 2. Performance Tips

```bash
# Use fd instead of find
fd "pattern"              # Instead of: find . -name "*pattern*"

# Use rg instead of grep
rg "pattern"              # Instead of: grep -r "pattern" .

# Limit search depth
fd --max-depth 3
rg --max-depth 3

# Exclude directories
fd -E node_modules -E .git
rg --glob '!node_modules'
```

### 3. Shell Startup Optimization

```bash
# Lazy load slow tools
nvm() {
    unset -f nvm
    [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
    nvm "$@"
}

# Cache expensive operations
_update_ps1_cache() {
    PS1_CACHE="$(expensive_command)"
}
```

## Troubleshooting

### Common Issues

**fzf not finding files:**
```bash
# Check FZF_DEFAULT_COMMAND
echo $FZF_DEFAULT_COMMAND

# Test fd directly
fd --type f

# Check for hidden files
fd -H
```

**Colors not working:**
```bash
# Check terminal capabilities
echo $TERM

# Force color output
export CLICOLOR_FORCE=1
```

**Slow shell startup:**
```bash
# Profile startup time
time bash -i -c exit

# Identify slow sources
for f in ~/.bashrc ~/.bash_profile; do
    echo "--- $f ---"
    time source "$f"
done
```

**zoxide not working:**
```bash
# Check initialization
type z

# Rebuild database
zoxide import --from=z
```

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Core CLI tools coverage (jq, fzf, ripgrep, fd, bat, exa)
  - Shell aliases and functions
  - Pipeline patterns
  - Integration examples
  - Shell configuration templates

---

**Use this skill to build efficient, productive terminal workflows with modern CLI tools!**
