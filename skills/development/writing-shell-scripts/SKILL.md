---
name: writing-shell-scripts
description: Use this before writing any shell scripts - establishes fish shell syntax, gum integration patterns, and script organization conventions
---

# Writing Shell Scripts

You are writing shell scripts for personal developer tooling and system automation. All scripts use **fish shell** (not bash/POSIX) and **gum** for interactive components. The target environment is macOS with fish as the default shell.

## Core Principles

1. **Fish-first** — Never use bash syntax. Fish has different control flow, variable handling, and string manipulation.
2. **Gum for all interaction** — Any user input, selection, confirmation, or styled output goes through gum. No fallbacks.
3. **Fail fast, fail loud** — Check preconditions early. Exit with clear errors rather than silent failures.
4. **No over-engineering** — These are personal scripts. Don't add configurability, help systems, or abstractions you don't need yet.

## Fish Syntax Guide

### Variables

```fish
# Fish
set myvar "value"
set -x EXPORTED_VAR "value"    # export
set -e myvar                    # unset

# NOT fish (bash)
myvar="value"
export EXPORTED_VAR="value"
```

### Conditionals

```fish
# Fish uses `test` or direct commands
if test -f "$file"
    echo "exists"
else if test -d "$dir"
    echo "is directory"
end

# Status checks
if command -q git
    # git is available
end

# NOT fish
if [ -f "$file" ]; then ... fi
if [[ ... ]]; then ... fi
```

### Loops

```fish
# Fish
for item in $list
    echo $item
end

while read -l line
    echo $line
end < file.txt

# NOT fish
for item in "${list[@]}"; do ... done
```

### String Manipulation

Use `string`, not sed/awk:

```fish
string replace "old" "new" $text
string split ":" $PATH
string match -q "*.txt" $filename
string trim $input
```

### Command Substitution

```fish
# Fish uses ( )
set result (command)

# NOT fish
result=$(command)
result=`command`
```

### No Word Splitting

Fish doesn't split variables on whitespace. `"$var"` and `$var` behave the same for single values. Lists are explicit.

## Gum Patterns

### User Input

```fish
set name (gum input --placeholder "Project name")
set password (gum input --password --placeholder "Enter password")
```

### Selection (Single)

```fish
set choice (gum choose "Option A" "Option B" "Option C")
set file (gum file /path/to/start)  # file picker
```

### Selection (Multiple)

```fish
set choices (gum choose --no-limit "one" "two" "three")
# $choices is now a fish list
```

### Confirmation

```fish
if gum confirm "Delete all logs?"
    rm -rf logs/
end
```

### Styled Output

```fish
gum style --foreground 212 --bold "Success!"
gum style --border rounded --padding "1 2" "Boxed message"
```

### Progress/Spinners

```fish
gum spin --title "Installing..." -- long_running_command
# or for pipeline progress:
some_command | gum pager
```

### Formatted Output

```fish
gum format --type markdown < README.md
```

### Combining Patterns

```fish
set action (gum choose "deploy" "rollback" "cancel")
if test "$action" = "cancel"
    exit 0
end
if gum confirm "Proceed with $action?"
    do_the_thing $action
end
```

## Error Handling & Safety

### Precondition Checks

```fish
# Check required commands exist
for cmd in gum jq curl
    if not command -q $cmd
        fatal "$cmd is required but not installed"
    end
end

# Check required env vars
if not set -q API_TOKEN
    fatal "API_TOKEN environment variable not set"
end

# Check file exists
if not test -f "$config_file"
    fatal "Config file not found: $config_file"
end
```

### Status Checks After Commands

```fish
if not curl -s "$url" -o "$output"
    error "Failed to download from $url"
    exit 1
end
```

### Confirm Before Destructive Actions

```fish
if gum confirm "Delete all files in $target_dir?"
    rm -rf "$target_dir"/*
    success "Cleaned $target_dir"
else
    info "Aborted"
end
```

### Output Helpers

These functions are globally installed in `~/.config/fish/functions/`:

- `success` — green ✓, for completed actions
- `info` — blue •, for neutral status
- `warn` — yellow ⚠, for non-fatal issues
- `error` — orange ✗, for failures (stderr)
- `fatal` — red ✗, for failures that exit (stderr + exit 1)

## Script Organization

### Where Scripts Live

| Location                    | Purpose                                  |
| --------------------------- | ---------------------------------------- |
| `~/.config/fish/functions/` | Reusable functions (auto-loaded by fish) |
| `~/.local/bin/`             | Standalone executable scripts            |
| `<project>/bin/`            | Project-specific scripts                 |

### Naming Conventions

- Lowercase, hyphens for separators: `deploy-staging`, `cleanup-logs`
- Functions match their filename: `foo.fish` contains `function foo`
- No `.fish` extension for standalone scripts in `~/.local/bin/` or `<project>/bin/` (use shebang)

### Shebang

```fish
#!/usr/bin/env fish
```

### Script Structure Template

```fish
#!/usr/bin/env fish

# --- Preconditions ---
if not command -q gum
    fatal "gum is required"
end

# --- Configuration ---
set -l target_dir ~/Downloads
set -l max_age 30

# --- Main logic ---
# ... your code here ...
```

### Multi-File Tools

For larger tools, keep a main entry point and source helpers:

```
~/.local/bin/mytool                      # main script
~/.local/bin/helpers/mytool-helpers.fish # supporting helpers (sourced)
```

Or keep it self-contained with local functions defined at the top of the script.

## Style Guide

### Formatting

Use `fish_indent` to format scripts:

```fish
fish_indent -w script.fish
```

### Variable Naming

```fish
set -l local_var "value"      # snake_case for locals
set -g global_var "value"     # snake_case for globals
set -x EXPORTED_VAR "value"   # UPPER_SNAKE for exports/env vars
```

### Function Naming

```fish
function do_something          # snake_case
function mytool_helper         # prefix with tool name for helpers
```

### Quoting

Always quote variables in arguments, even though fish doesn't word-split:

```fish
# Preferred
echo "$myvar"
test -f "$file"

# Avoid (works, but inconsistent)
echo $myvar
```

### Line Length

Keep lines under 100 characters. Break long pipelines:

```fish
cat "$file" \
    | string match -r 'pattern' \
    | sort -u
```

### Blank Lines

- One blank line between logical sections
- One blank line before `end` in longer functions

## Documentation

Every script must have `--help`:

```fish
#!/usr/bin/env fish

argparse 'help' 'force' 'verbose' -- $argv
or return

function usage
    echo '
script-name

Brief description of what this script does.

USAGE:
  script-name [OPTIONS] <required-arg>

ARGUMENTS:
  required-arg    What this argument is for

OPTIONS:
  --force      Override existing files
  --verbose    Show detailed output
  --help       Show this usage description

REQUIRES:
  - gum
  - any other dependencies

OUTPUTS:
  - What the script produces
'
end

if set -q _flag_help
    usage
    exit 0
end

# ... rest of script
```

### Help Text Sections (in order)

1. Script name (header line)
2. Brief description
3. `USAGE:` — command syntax
4. `ARGUMENTS:` — positional args (if any)
5. `OPTIONS:` — all flags with descriptions
6. `REQUIRES:` — dependencies (optional)
7. `OUTPUTS:` — what it produces (optional)
