---
name: zsh-completions
description: Write zsh completion scripts with descriptions, colors, and dynamic completions. This skill should be used when creating _command completion files, using _arguments/_describe/_values functions, configuring ZLS_COLORS for colored completions, building subcommand trees (like git/kubectl), generating dynamic completions from external commands, understanding compinit/compdef/fpath, configuring fzf-tab previews and grouping, writing fzf.zsh preview scripts, or debugging completion issues. Output completions to ~/.config/zsh/completions/.
---

# ZSH Completion Authoring

Write zsh completion scripts with rich descriptions, colors, and dynamic completions.

## Output Location

Place completion files in `~/.config/zsh/completions/` with `_commandname` naming.

## Quick Start

```zsh
#compdef mycommand

_mycommand() {
    _arguments \
        '-h[Show help]' \
        '--verbose[Enable verbose output]' \
        '1:action:(start stop restart)' \
        '*:files:_files'
}

_mycommand "$@"
```

## Core Functions

| Function | Purpose | Reference |
|----------|---------|-----------|
| `_arguments` | Flags + positional args | `references/arguments.md` |
| `_describe` | Lists with descriptions | `references/describe.md` |
| `_values` | Comma-separated values | `references/arguments.md` |
| `_alternative` | Multiple completion types | `references/patterns.md` |

## Completion with Descriptions

```zsh
# Static options with descriptions
_arguments \
    '-f[Force operation without confirmation]' \
    '-v[Verbose output]' \
    '--config[Config file path]:file:_files'

# Dynamic list with descriptions
local -a commands
commands=(
    'start:Start the service'
    'stop:Stop the service'
    'status:Show current status'
)
_describe 'command' commands
```

## Dynamic Completions

```zsh
# Query external command
_mycommand_targets() {
    local -a targets
    targets=(${(f)"$(mycommand list-targets 2>/dev/null)"})
    _describe 'target' targets
}

# With descriptions from JSON
local -a items
items=($(mycommand --json | jq -r '.[] | "\(.name):\(.desc)"'))
_describe 'item' items
```

## Colors

See `references/colors.md` for ZLS_COLORS configuration.

```zsh
# In zstyle (completions.zsh)
zstyle ':completion:*:descriptions' format '%F{green}-- %d --%f'
zstyle ':completion:*:warnings' format '%F{red}No matches%f'

# Color by file type
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
```

## Subcommand Trees

For nested commands like `git remote add`, see `references/patterns.md`.

```zsh
_arguments -C \
    '1:command:->cmd' \
    '*::arg:->args'

case $state in
    cmd) _describe 'command' commands ;;
    args)
        case $words[1] in
            start) _mycommand_start ;;
            stop) _mycommand_stop ;;
        esac ;;
esac
```

## fzf-tab Integration

See `references/fzf-tab.md` for full configuration.

```zsh
# Group completions using tags
_describe -t commands 'command' commands
_describe -t options 'option' options

# Enable group switching
zstyle ':fzf-tab:*' show-group full
zstyle ':fzf-tab:*' switch-group '<' '>'

# Command-specific preview using fzf.zsh
zstyle ':fzf-tab:complete:mycommand:*' fzf-preview 'fzf.zsh $realpath'
```

## compinit Integration

See `references/compinit.md` for initialization details.

```zsh
# Ensure fpath includes your completions dir
fpath=(~/.config/zsh/completions $fpath)

# Initialize (in .zshrc or completions.zsh)
autoload -Uz compinit && compinit

# With zinit (turbo mode)
zinit ice wait lucid atinit"zicompinit; zicdreplay"
zinit light zdharma-continuum/fast-syntax-highlighting
```

## References

- `references/arguments.md` - _arguments syntax and optspecs
- `references/describe.md` - _describe for dynamic lists
- `references/colors.md` - ZLS_COLORS and styling
- `references/compinit.md` - Completion system internals
- `references/patterns.md` - Subcommand and complex patterns
- `references/fzf-tab.md` - fzf-tab grouping, previews, fzf.zsh script
