---
name: completions
description: ZSH completion system patterns and conventions. Use when implementing custom completion handling, writing completion files, or working with zsh autocomplete. Do not use when installing packages from homebrew, since that typically installs completions automatically.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Completions

Guide for writing and managing custom ZSH completion files in this dotfiles repository.

## When to Use

- Implementing custom completions for CLI tools
- Fixing or updating existing completion files
- Understanding how completions are loaded in this repo

**Do NOT use** when installing homebrew packages - they handle completions automatically.

## Repository Conventions

### File Naming

Completion files in this repo use: `<topic>/completion.zsh`

Example: `claude/completion.zsh`

### Loading Process

From `zsh/zshrc.symlink`:

1. `compinit` is called to initialize the completion system
2. All `*/completion.zsh` files are sourced
3. Files are sourced directly, NOT added to `fpath`

### File Structure

```zsh
#!/usr/bin/env zsh

# Define completion function
_toolname() {
  local line state

  # Define options
  local -a options=(
    '-h[Display help]'
    '--help[Display help]'
  )

  # Define subcommands
  local -a subcommands=(
    'command:Description'
  )

  _arguments -C \
    "${options[@]}" \
    '1: :->command' \
    '*::arg:->args'

  case $state in
    command)
      _describe -t commands 'tool command' subcommands
      ;;
    args)
      # Handle subcommand args
      ;;
  esac
}

# Register completion
compdef _toolname toolname
```

## Key Patterns

### Registration

Use `compdef` at the end of the file:

```zsh
compdef _toolname toolname
```

**NOT** the `#compdef` directive (that's for files in `fpath`).

### Options Format

```zsh
local -a options=(
  '-h[Display help]'
  '--help[Display help]'
  '--flag[Description]'
  '--option[Description]:value:'
  '--file[Description]:file:_files'
  '--dir[Description]:directory:_directories'
)
```

### Subcommands

```zsh
local -a subcommands=(
  'command:Description'
  'subcommand:What it does'
)

_describe -t commands 'tool command' subcommands
```

### Argument Handling

```zsh
_arguments -C \
  "${options[@]}" \
  '1: :->command' \
  '*::arg:->args'

case $state in
  command)
    _describe -t commands 'tool command' subcommands
    ;;
  args)
    case ${line[1]} in
      subcommand)
        _arguments \
          '--subcommand-option[Description]' \
          '1:arg:'
        ;;
    esac
    ;;
esac
```

### Nested Subcommands

For tools like `git` or `docker` with deep command hierarchies:

```zsh
_tool_subcommand() {
  local line state

  local -a sub_subcommands=(
    'action:Description'
  )

  _arguments -C \
    '1: :->command' \
    '*::arg:->args'

  case $state in
    command)
      _describe -t commands 'tool subcommand command' sub_subcommands
      ;;
  esac
}
```

## Common Completers

Built-in zsh completion functions:

- `_files` - File paths
- `_directories` - Directory paths
- `_values` - Predefined values
- `_describe` - Command descriptions
- `_arguments` - Argument parsing

### File Completion

```zsh
'--config[Config file]:file:_files'
```

### Choice Completion

```zsh
'--format[Output format]:format:(json yaml text)'
```

### Multiple Values

```zsh
'--env[Environment variables]:env:'  # Free form
'--scope[Scope]:scope:(local user project)'  # Fixed choices
```

## Testing

After creating/modifying a completion file:

1. Reload shell: `source ~/.zshrc`
2. Test completion: `tool <TAB>`
3. Test subcommands: `tool subcommand <TAB>`
4. Test options: `tool --<TAB>`

## Generating Completions

Steps to create completions for a new tool:

1. Run `tool --help` to see main options
2. Run `tool subcommand --help` for each subcommand
3. Create `<topic>/completion.zsh`
4. Define `_toolname()` function with all discovered options
5. Register with `compdef _toolname toolname`
6. Test thoroughly

## Common Issues

### "command not found: _arguments"

The completion function is being executed instead of sourced. Ensure:
- File is named `completion.zsh` (not `completions.zsh`)
- Using `compdef` (not `#compdef`)
- File is in a topic directory that gets sourced

### "can only be called from completion function"

Using `#compdef` directive when file is sourced directly. Use `compdef` registration instead.

### Completions Not Loading

1. Check file naming: `*/completion.zsh`
2. Verify file is being sourced: `echo $ZSH/**/*.zsh | grep completion`
3. Check for syntax errors: `zsh -n path/to/completion.zsh`

## Examples

See existing completion files:
- `claude/completion.zsh` - Complex multi-level subcommands
- `gcloud/completions.zsh` - Third-party completion sourcing
