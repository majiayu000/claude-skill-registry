---
name: shell-prompt
description: Modern shell prompt configuration with Powerlevel10k and Zsh Vi Mode. Use when configuring shell prompts, setting up vi/vim keybindings in zsh, customizing cursor styles per mode, adding mode indicators, optimizing prompt performance, or troubleshooting slow prompts. Covers P10k instant prompt, vi mode plugins, and cursor customization.
---

# Shell Prompt Skill

Configure high-performance shell prompts with Powerlevel10k and Zsh Vi Mode.

## Overview

Modern shell prompts provide:
- Git status with branch, dirty state, and remote tracking
- Environment indicators (Python venv, Node version, K8s context)
- Execution time for long-running commands
- Exit code visualization
- Async updates for responsive experience
- Vi mode indicators and cursor changes

## Zsh Vi Mode

Zsh supports vi-style line editing with visual feedback through cursor changes and mode indicators.

### Quick Setup (Built-in)

```zsh
# ~/.zshrc
bindkey -v  # Enable vi mode

# Reduce key timeout for faster mode switching (default 400ms)
export KEYTIMEOUT=10  # 100ms - don't go below 10
```

### Cursor Style by Mode

Change cursor shape based on current mode:

```zsh
# Add to ~/.zshrc
cursor_mode() {
    # Beam cursor for insert mode
    cursor_beam='\e[6 q'
    # Block cursor for normal mode
    cursor_block='\e[2 q'

    function zle-keymap-select {
        if [[ ${KEYMAP} == vicmd ]] ||
           [[ $1 = 'block' ]]; then
            echo -ne $cursor_block
        elif [[ ${KEYMAP} == main ]] ||
             [[ ${KEYMAP} == viins ]] ||
             [[ ${KEYMAP} = '' ]] ||
             [[ $1 = 'beam' ]]; then
            echo -ne $cursor_beam
        fi
    }

    zle-line-init() {
        echo -ne $cursor_beam
    }

    zle -N zle-keymap-select
    zle -N zle-line-init
}
cursor_mode
```

### Cursor Escape Codes

| Code | Style |
|------|-------|
| `\e[1 q` | Blinking block |
| `\e[2 q` | Steady block |
| `\e[3 q` | Blinking underline |
| `\e[4 q` | Steady underline |
| `\e[5 q` | Blinking bar/beam |
| `\e[6 q` | Steady bar/beam |

## Vi Mode Plugins

### Oh My Zsh vi-mode Plugin

```zsh
# ~/.zshrc
plugins=(... vi-mode)

# Configuration (before sourcing oh-my-zsh.sh)
VI_MODE_SET_CURSOR=true
VI_MODE_RESET_PROMPT_ON_MODE_CHANGE=true

# Cursor styles (0-6)
VI_MODE_CURSOR_NORMAL=2   # Solid block
VI_MODE_CURSOR_INSERT=6   # Solid beam
VI_MODE_CURSOR_VISUAL=6   # Solid beam
VI_MODE_CURSOR_OPPEND=0   # Blinking block

# Mode indicators
MODE_INDICATOR="%F{red}<<<NORMAL%f"
INSERT_MODE_INDICATOR="%F{green}<<<INSERT%f"
```

### softmoth/zsh-vim-mode

Full-featured vi mode with text objects and surround bindings.

**Installation:**
```bash
# Clone
git clone https://github.com/softmoth/zsh-vim-mode.git ~/.zsh/zsh-vim-mode

# Source in .zshrc (after other plugins)
source ~/.zsh/zsh-vim-mode/zsh-vim-mode.plugin.zsh
```

**Load order matters:** zsh-autosuggestions -> zsh-syntax-highlighting -> zsh-vim-mode

**Configuration:**
```zsh
# Cursor styles (supports colors!)
MODE_CURSOR_VIINS="#00ff00 blinking bar"
MODE_CURSOR_VICMD="green block"
MODE_CURSOR_REPLACE="red block"
MODE_CURSOR_SEARCH="#ff00ff steady underline"
MODE_CURSOR_VISUAL="$MODE_CURSOR_VICMD steady bar"
MODE_CURSOR_VLINE="$MODE_CURSOR_VISUAL #00ffff"

# Mode indicators (auto-added to RPS1 if unset)
MODE_INDICATOR_VIINS='%F{15}<%F{8}INSERT>%f'
MODE_INDICATOR_VICMD='%F{10}<%F{2}NORMAL>%f'
MODE_INDICATOR_REPLACE='%F{9}<%F{1}REPLACE>%f'
MODE_INDICATOR_SEARCH='%F{13}<%F{5}SEARCH>%f'
MODE_INDICATOR_VISUAL='%F{12}<%F{4}VISUAL>%f'
MODE_INDICATOR_VLINE='%F{12}<%F{4}V-LINE>%f'

# Other options
VIM_MODE_VICMD_KEY='^['          # Default escape key
VIM_MODE_TRACK_KEYMAP=true       # Enable mode tracking
VIM_MODE_INITIAL_KEYMAP=viins    # Start in insert mode
```

**Features:**
- Text objects: `ci"`, `da(`, `vi[`
- Surround: `cs"'` (change surrounding " to ')
- Visual mode selection
- Emacs bindings in insert mode (Ctrl-A, Ctrl-E)

### jeffreytse/zsh-vi-mode

Modern vi mode with operator-pending mode support.

**Installation:**
```bash
# With zinit
zinit ice depth=1
zinit light jeffreytse/zsh-vi-mode

# Manual
git clone https://github.com/jeffreytse/zsh-vi-mode.git ~/.zsh/zsh-vi-mode
source ~/.zsh/zsh-vi-mode/zsh-vi-mode.plugin.zsh
```

**Configuration:**
```zsh
# Cursor styles
ZVM_NORMAL_MODE_CURSOR=$ZVM_CURSOR_BLOCK
ZVM_INSERT_MODE_CURSOR=$ZVM_CURSOR_BEAM
ZVM_VISUAL_MODE_CURSOR=$ZVM_CURSOR_BLOCK
ZVM_VISUAL_LINE_MODE_CURSOR=$ZVM_CURSOR_BLOCK
ZVM_OPPEND_MODE_CURSOR=$ZVM_CURSOR_UNDERLINE

# Mode indicator in prompt
function zvm_after_select_vi_mode() {
  case $ZVM_MODE in
    $ZVM_MODE_NORMAL)
      # Update prompt for normal mode
      ;;
    $ZVM_MODE_INSERT)
      # Update prompt for insert mode
      ;;
    $ZVM_MODE_VISUAL)
      # Update prompt for visual mode
      ;;
  esac
}

# Disable cursor style changes (if using another method)
ZVM_CURSOR_STYLE_ENABLED=false
```

## Key Bindings Reference

### Mode Switching

| Key | Action |
|-----|--------|
| `ESC` or `Ctrl-[` | Enter Normal mode |
| `i` | Insert before cursor |
| `a` | Append after cursor |
| `I` | Insert at line start |
| `A` | Append at line end |
| `v` | Enter Visual mode |
| `V` | Enter Visual Line mode |

### Navigation (Normal Mode)

| Key | Action |
|-----|--------|
| `h/l` | Left/right |
| `j/k` | Down/up in history |
| `w/W` | Forward word |
| `b/B` | Backward word |
| `e/E` | End of word |
| `0` | Start of line |
| `^` | First non-blank |
| `$` | End of line |
| `f{char}` | Find char forward |
| `F{char}` | Find char backward |
| `t{char}` | Till char forward |
| `T{char}` | Till char backward |

### Editing (Normal Mode)

| Key | Action |
|-----|--------|
| `x` | Delete char |
| `dd` | Delete line |
| `D` | Delete to end |
| `cc` | Change line |
| `C` | Change to end |
| `yy` | Yank line |
| `p/P` | Paste after/before |
| `u` | Undo |
| `Ctrl-r` | Redo |

### Text Objects

| Key | Action |
|-----|--------|
| `ciw` | Change inner word |
| `daw` | Delete a word (with space) |
| `ci"` | Change inside quotes |
| `da(` | Delete around parens |
| `vi[` | Select inside brackets |

## KEYTIMEOUT Considerations

The `KEYTIMEOUT` variable affects multi-key sequences:

```zsh
# Default is 40 (400ms)
export KEYTIMEOUT=10  # 100ms - good balance

# Too low (<10) breaks multi-key bindings
# Too high (>40) feels sluggish on ESC
```

**Workarounds for escape delay:**
```zsh
# Option 1: Use Ctrl-[ instead of Escape
# (Ctrl-[ sends ESC immediately)

# Option 2: Bind jk or jj to escape
bindkey -M viins 'jk' vi-cmd-mode
bindkey -M viins 'jj' vi-cmd-mode
```

## Powerlevel10k

### Installation

```bash
# With Oh My Zsh
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
  ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

# Set in .zshrc
ZSH_THEME="powerlevel10k/powerlevel10k"

# Run configuration wizard
p10k configure
```

### Instant Prompt Setup

Add at the **very top** of `~/.zshrc` (before anything else):

```zsh
# Enable Powerlevel10k instant prompt
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
```

Add at the **end** of `~/.zshrc`:

```zsh
# Source Powerlevel10k config
[[ -f ~/.p10k.zsh ]] && source ~/.p10k.zsh
```

### Configuration Options

Key settings in `~/.p10k.zsh`:

```zsh
# Left prompt segments
typeset -g POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
  os_icon
  dir
  vcs
  newline
  prompt_char
)

# Right prompt segments
typeset -g POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(
  status
  command_execution_time
  background_jobs
  virtualenv
  kubecontext
  azure
  aws
  vi_mode      # Show vi mode indicator!
  context
  time
)

# Transient prompt (clean up previous prompts)
typeset -g POWERLEVEL9K_TRANSIENT_PROMPT=always

# Directory truncation
typeset -g POWERLEVEL9K_SHORTEN_STRATEGY=truncate_to_unique
typeset -g POWERLEVEL9K_SHORTEN_DIR_LENGTH=3

# Vi mode indicator styling
typeset -g POWERLEVEL9K_VI_INSERT_MODE_STRING=''
typeset -g POWERLEVEL9K_VI_COMMAND_MODE_STRING='NORMAL'
typeset -g POWERLEVEL9K_VI_MODE_NORMAL_FOREGROUND=0
typeset -g POWERLEVEL9K_VI_MODE_NORMAL_BACKGROUND=2
```

### Performance Tuning

```zsh
# Disable slow segments
typeset -g POWERLEVEL9K_DISABLE_GITSTATUS=false  # Keep enabled!

# Large repo optimization
typeset -g POWERLEVEL9K_VCS_MAX_INDEX_SIZE_DIRTY=1000

# Async git status (default, don't change)
typeset -g POWERLEVEL9K_VCS_BACKENDS=(git)

# Reduce segment count for speed
typeset -g POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status command_execution_time vi_mode)
```

## Performance Summary

### Benchmark Results (zsh-bench)

| Metric | Target | Powerlevel10k |
|--------|--------|---------------|
| First prompt lag | <50ms | **24ms** |
| Command lag | <10ms | **15ms** |
| Git status (small) | <30ms | <10ms |
| Git status (large) | <100ms | Async/instant |

### Architecture

**Powerlevel10k (gitstatus daemon)**:
```
┌─────────────┐     pipes      ┌─────────────┐
│    Zsh      │ <============> │  gitstatusd │
│  (prompt)   │                │   (C++ daemon)
└─────────────┘                └─────────────┘
       │                              │
       │ async                        │ keeps state
       │ never blocks                 │ in memory
       ▼                              ▼
   Instant prompt              Fast git queries
```

## Benchmarking Your Setup

### Using zsh-bench

```bash
# Install
git clone https://github.com/romkatv/zsh-bench ~/zsh-bench

# Run benchmark
~/zsh-bench/zsh-bench

# Key metrics to watch:
# - first_prompt_lag_ms: <50ms ideal
# - command_lag_ms: <10ms ideal
```

### Manual Timing

```bash
# Zsh startup time
time zsh -i -c exit

# Per-command timing
TIMEFMT='%*E seconds'
time (for i in {1..10}; do zsh -i -c 'print -P "$PROMPT"' >/dev/null; done)
```

## Troubleshooting

### Slow Prompt

```bash
# Check segment timing
zsh -xv  # Verbose trace

# Common culprits:
# - git_status in large repos
# - python/node version detection
# - cloud context (aws/azure/gcloud)
```

### P10k: gitstatus Failed

```bash
# Reinstall gitstatusd
rm -rf ~/.cache/gitstatus

# Restart zsh
exec zsh
```

### Vi Mode Not Working

```bash
# Verify vi mode is enabled
bindkey -l | grep vi

# Check current keymap
echo $KEYMAP

# Reset bindings
bindkey -v
```

### Cursor Not Changing

1. Verify terminal supports cursor escape codes
2. Check `zle-keymap-select` is defined: `whence -f zle-keymap-select`
3. Some terminals (like Apple Terminal) have limited cursor support
4. Try iTerm2 or Alacritty for full support

## References

- [references/powerlevel10k-config.md](references/powerlevel10k-config.md) - Complete P10k configuration
- [references/zsh-vim-mode.md](references/zsh-vim-mode.md) - softmoth/zsh-vim-mode details
- [references/performance-tuning.md](references/performance-tuning.md) - Advanced optimization
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues and fixes

## External Links

- Powerlevel10k: https://github.com/romkatv/powerlevel10k
- softmoth/zsh-vim-mode: https://github.com/softmoth/zsh-vim-mode
- jeffreytse/zsh-vi-mode: https://github.com/jeffreytse/zsh-vi-mode
- Oh My Zsh vi-mode: https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/vi-mode
- zsh-bench: https://github.com/romkatv/zsh-bench
- gitstatus: https://github.com/romkatv/gitstatus
