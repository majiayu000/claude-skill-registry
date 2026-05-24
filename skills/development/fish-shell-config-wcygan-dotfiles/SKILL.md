---
name: fish-shell-config
description: Expert Fish shell configuration including config files, functions, abbreviations, prompts, environment variables, and scripting. Use when setting up Fish, creating aliases/functions, writing Fish scripts, configuring prompts, or migrating from bash. Keywords: fish shell, fish config, alias, abbr, function, prompt, fish script, config.fish, autoload
---

# Fish Shell Configuration Expert

Expert guidance for Fish shell setup, configuration, scripting, and interactive features based on official Fish documentation.

## Core Principles

Fish philosophy differs fundamentally from bash:
- **Variables are lists** - all Fish variables contain string lists, not scalars
- **No word splitting** - `"$var"` and `$var` behave identically (already quoted)
- **Autoloading** - functions load on-demand from `~/.config/fish/functions/`
- **Universal variables** - persist across sessions via `-U` flag
- **Explicit syntax** - `set VAR value` instead of `VAR=value`

## Configuration File Structure

Fish reads configs in this order:

```
~/.config/fish/
├── config.fish          # Main config (keep minimal)
├── conf.d/              # Auto-sourced configs (lexical order)
│   ├── 10-nix.fish     # Early: PATH and environment
│   ├── 20-direnv.fish  # Middle: tool hooks
│   ├── 30-starship.fish # Late: prompt setup
│   └── 40-aliases.fish  # Last: shortcuts and abbrs
└── functions/           # Autoloaded function definitions
    ├── nix-try.fish
    └── my-function.fish
```

**Best practice**: Keep `config.fish` minimal; use `conf.d/*.fish` for modular configs.

## Functions vs Aliases vs Abbreviations

### Functions (Recommended)
**Where**: `~/.config/fish/functions/name.fish` for autoloading

```fish
# ~/.config/fish/functions/ll.fish
function ll --description 'list all files'
    eza -la $argv
end
```

**Benefits**: Autoloaded on demand, persistent, scriptable, full control

### Aliases (Creates Functions)
**Where**: `conf.d/40-aliases.fish`

```fish
# Creates a function under the hood
alias g='git'
alias k='kubectl'

# Better: guard with type check
function __maybe_alias --argument-names name target
    if type -q $target
        alias $name="$target"
    end
end

__maybe_alias g git
__maybe_alias ll eza
```

**Note**: In Fish, `alias` creates a function, so it's callable from scripts.

### Abbreviations (Interactive Only)
**Where**: `conf.d/40-aliases.fish`

```fish
# Expands on SPACE/ENTER in interactive shells
abbr -a gco 'git checkout'
abbr -a gst 'git status -sb'
abbr -a glg 'git log --oneline --graph --decorate --all'
abbr -a kctx 'kubectl config use-context'

# Conditional abbreviation
if type -q kubectl
    abbr -a k 'kubectl'
end
```

**Benefits**: See expansion before execution, learn command syntax, purely interactive

## Variable Scoping

### Scope Flags
- `-l` local: Current block/function only
- `-g` global: Current session
- `-U` universal: Persists across all sessions (stored in `~/.config/fish/fish_variables`)
- `-x` export: Visible to child processes (environment variable)

### Common Patterns

```fish
# Session-only global export
set -gx EDITOR nvim

# Universal (survives restarts)
set -U fish_greeting ""  # disable greeting

# Local function variable
function my_func
    set -l temp_var "local value"
    # temp_var dies when function exits
end

# PATH manipulation (Fish handles it as a list)
set -gx PATH $HOME/.local/bin $PATH

# Check if set before setting
set -q EDITOR; or set -gx EDITOR nvim
```

### Special Variables
- `$argv` - function/script arguments (replaces bash `$@`, `$1`, `$2`...)
- `$status` - last command exit code (replaces bash `$?`)
- `$fish_pid` - current shell PID (replaces bash `$$`)
- `$PATH` - automatically colon-delimited when exported

## Writing Functions

### Basic Structure

```fish
function name --description 'what it does'
    # $argv contains all arguments
    command $argv
end
```

### Function Options
- `--description 'text'` - shown in completions
- `--wraps command` - inherit completions from command
- `--argument-names var1 var2` - name positional args

### Advanced Example

```fish
function nix-try --description 'Try a package temporarily' \
                 --argument-names package
    if test (count $argv) -eq 0
        echo "Usage: nix-try <package>"
        return 1
    end

    # Command substitution with $()
    set -l store_path (nix build nixpkgs#$package --print-out-paths --no-link)

    if test $status -ne 0
        echo "Failed to build $package"
        return 1
    end

    $store_path/bin/$package
end
```

### Editing Functions Interactively

```fish
funced function_name    # Edit in $EDITOR
funcsave function_name  # Save to ~/.config/fish/functions/
```

## Control Flow

### Conditionals

```fish
# Using 'test' command
if test -e /path/to/file
    echo "exists"
else if test $count -gt 5
    echo "greater than 5"
else
    echo "other"
end

# Using command exit status
if command_that_might_fail
    echo "succeeded"
end

# Using 'and'/'or'
command1; and command2  # command2 only if command1 succeeds
command1; or command2   # command2 only if command1 fails
```

### Loops

```fish
# For loop over list
for file in *.txt
    echo "Processing $file"
end

# While loop
set -l count 0
while test $count -lt 10
    echo $count
    set count (math $count + 1)
end

# Iterate over command output (splits on newlines)
for line in (cat file.txt)
    echo "Line: $line"
end
```

### Switch Statement

```fish
switch $argv[1]
    case start
        echo "Starting..."
    case stop
        echo "Stopping..."
    case '*'
        echo "Unknown command"
end
```

## String Handling

### Command Substitution

```fish
# Two equivalent forms
set output $(command)
set output (command)

# Splits on newlines only (not spaces)
set lines (cat file.txt)  # Each line = one list element

# Split on custom delimiter
set fields (echo "a:b:c" | string split ':')  # ['a', 'b', 'c']
```

### String Operations (using `string` builtin)

```fish
# Split
echo "foo:bar:baz" | string split ':'

# Join
string join ',' a b c  # "a,b,c"

# Replace
string replace 'old' 'new' $var

# Match/regex
string match -q '*pattern*' $var; and echo "matched"

# Length
string length "hello"  # 5

# Case conversion
string upper "hello"   # HELLO
string lower "WORLD"   # world
```

### Quoting

```fish
# Single quotes - no expansion
echo 'literal $PATH'  # outputs: literal $PATH

# Double quotes - variables/commands expand, but NO word splitting
set var "hello world"
echo "$var"  # one argument: "hello world"
echo $var    # STILL one argument: "hello world" (Fish doesn't split!)

# No quote needed for variables (Fish doesn't word-split)
set files (ls)
for f in $files  # Safe! Each filename is one element
    echo $f
end
```

## Lists and Arrays

```fish
# All variables are lists
set mylist one two three

# Access elements (1-indexed!)
echo $mylist[1]      # "one"
echo $mylist[2]      # "two"
echo $mylist[-1]     # "three" (last element)

# Ranges
echo $mylist[1..2]   # "one two"
echo $mylist[2..-1]  # "two three"

# Append
set -a mylist four   # now: one two three four

# Prepend
set -p mylist zero   # now: zero one two three four

# Count
count $mylist        # 5

# Iterate
for item in $mylist
    echo $item
end
```

## Prompt Customization

Fish prompts are **functions**, not variables:

```fish
# ~/.config/fish/functions/fish_prompt.fish
function fish_prompt
    set -l last_status $status

    # Color codes
    set_color blue
    echo -n (prompt_pwd)

    if test $last_status -ne 0
        set_color red
        echo -n " [$last_status]"
    end

    set_color normal
    echo -n ' > '
end
```

### Using Starship (Recommended)

```fish
# ~/.config/fish/conf.d/30-starship.fish
if type -q starship
    starship init fish | source
end
```

## Event Handlers

```fish
# Run when changing directory
function on_cd --on-variable PWD
    if test -f .envrc
        direnv allow .
    end
end

# Run on Fish start
function on_start --on-event fish_startup
    echo "Welcome to Fish!"
end
```

## Migrating from Bash

### Common Bash → Fish Translations

| Bash | Fish | Notes |
|------|------|-------|
| `VAR=value` | `set VAR value` | Use `-gx` for export |
| `export VAR=value` | `set -gx VAR value` | Global + export |
| `$?` | `$status` | Exit code |
| `$@` | `$argv` | All arguments |
| `$1, $2` | `$argv[1], $argv[2]` | Positional args |
| `${VAR}` | `$VAR` or `{$VAR}` | Braces optional |
| `$((...))` | `math ...` | Arithmetic |
| `[[ ... ]]` | `test ...` | Conditionals |
| `for i in {1..10}` | `for i in (seq 1 10)` | Ranges |

### No Bash Features in Fish

- **No heredocs** (`<<EOF`): Use `echo` or files
- **No subshells**: Use `begin; ...; end` for grouping
- **No `until`**: Use `while not`
- **No `[[`**: Use `test` or `[`
- **No word splitting**: Fish never splits variables on whitespace

## Project Integration Patterns

### direnv Hook
```fish
# ~/.config/fish/conf.d/20-direnv.fish
if type -q direnv
    direnv hook fish | source
end
```

### Nix Integration
```fish
# ~/.config/fish/conf.d/10-nix.fish
if test -e /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.fish
    source /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.fish
end
```

## Debugging

```fish
# Print variable
echo $PATH

# Check if command exists
type -q command; and echo "exists"

# Show function definition
type function_name

# Show all functions
functions

# Show all variables
set

# Debug mode
fish -d 3 -c 'your command'
```

## Common Tasks

### Add to PATH
```fish
# Temporary (session only)
set -gx PATH $HOME/.local/bin $PATH

# Persistent (universal)
set -U fish_user_paths $HOME/.local/bin $fish_user_paths
```

### Create Wrapper Function
```fish
# ~/.config/fish/functions/gs.fish
function gs --wraps='git status' --description 'git status shortcut'
    git status -sb $argv
end
```

### Conditional Config
```fish
# Only set if not already set
set -q EDITOR; or set -gx EDITOR nvim

# Platform-specific
if test (uname) = Darwin
    set -gx HOMEBREW_PREFIX /opt/homebrew
end
```

## Output Instructions

When helping with Fish configuration:

1. **Determine what the user needs:**
   - New function? → Create in `~/.config/fish/functions/name.fish`
   - Alias/abbr? → Add to `conf.d/40-aliases.fish`
   - Environment var? → Use `set -gx` in appropriate `conf.d/` file
   - Prompt? → Suggest Starship or custom `fish_prompt` function

2. **Use appropriate tools:**
   - `Read` to check existing configs
   - `Edit` to modify existing files
   - `Write` to create new function files
   - `Bash(fish:*)` to test Fish commands

3. **Follow project conventions:**
   - Check `CLAUDE.md` for project-specific requirements
   - Respect existing `conf.d/*.fish` numbering (10, 20, 30, 40...)
   - Use autoloading for functions when possible
   - Guard tools with `type -q` checks

4. **Provide working examples:**
   - Include complete function definitions
   - Show proper scope flags (`-l`, `-g`, `-U`, `-x`)
   - Explain Fish-specific syntax differences from bash
   - Test commands work before suggesting

5. **Explain Fish idioms:**
   - Why `set -gx` instead of `export VAR=value`
   - Why variables don't need quotes (no word splitting)
   - Why `$argv` instead of `$1`, `$2`...
   - Why `test` instead of `[[`
   - 1-indexed lists vs 0-indexed in other languages

## Reference Documentation

For detailed information, refer to:
- Fish tutorial: https://fishshell.com/docs/current/tutorial.html
- Language reference: https://fishshell.com/docs/current/language.html
- Command reference: https://fishshell.com/docs/current/commands.html
- Bash migration: https://fishshell.com/docs/current/fish_for_bash_users.html
