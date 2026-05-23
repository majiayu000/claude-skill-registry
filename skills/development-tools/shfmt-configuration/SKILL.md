---
name: shfmt-configuration
description: Use when configuring shfmt for shell script formatting including .shfmt.toml setup, EditorConfig integration, and project-specific settings.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# shfmt Configuration

Master shfmt configuration for consistent shell script formatting across projects, including configuration files, EditorConfig integration, and team standardization.

## Overview

shfmt is a shell parser, formatter, and interpreter that supports POSIX Shell, Bash, and mksh. Configuration allows you to define consistent formatting rules for your shell scripts.

## Configuration Methods

shfmt supports multiple configuration approaches, in order of precedence:

1. Command-line flags (highest precedence)
2. EditorConfig settings
3. `.shfmt.toml` or `shfmt.toml` file

## TOML Configuration File

### Basic Configuration

Create `.shfmt.toml` or `shfmt.toml` in your project root:

```toml
# Shell dialect (posix, bash, mksh, bats)
shell = "bash"

# Indent with spaces (0 for tabs)
indent = 2

# Binary operators at start of line
binary-next-line = true

# Switch cases indented
switch-case-indent = true

# Redirect operators followed by space
space-redirects = false

# Keep column alignment paddings
keep-padding = false

# Function opening brace on next line
func-next-line = false
```

### Configuration Options Explained

#### shell

Specifies the shell dialect for parsing:

```toml
# POSIX-compliant shell (most portable)
shell = "posix"

# Bash (default for .bash files)
shell = "bash"

# MirBSD Korn Shell
shell = "mksh"

# Bats (Bash Automated Testing System)
shell = "bats"
```

Auto-detection based on shebang if not specified:

- `#!/bin/sh` -> posix
- `#!/bin/bash` or `#!/usr/bin/env bash` -> bash
- `#!/bin/mksh` -> mksh

#### indent

Controls indentation style:

```toml
# 2 spaces (common)
indent = 2

# 4 spaces
indent = 4

# Tabs (use 0)
indent = 0
```

#### binary-next-line

Controls binary operator positioning:

```toml
# Operators at end of line (default)
binary-next-line = false
```

```bash
# Result:
if [ "$a" = "foo" ] &&
   [ "$b" = "bar" ]; then
    echo "match"
fi
```

```toml
# Operators at start of next line
binary-next-line = true
```

```bash
# Result:
if [ "$a" = "foo" ] \
    && [ "$b" = "bar" ]; then
    echo "match"
fi
```

#### switch-case-indent

Controls case statement indentation:

```toml
# Cases at same level as switch (default)
switch-case-indent = false
```

```bash
# Result:
case "$1" in
start)
    do_start
    ;;
stop)
    do_stop
    ;;
esac
```

```toml
# Cases indented inside switch
switch-case-indent = true
```

```bash
# Result:
case "$1" in
    start)
        do_start
        ;;
    stop)
        do_stop
        ;;
esac
```

#### space-redirects

Controls spacing around redirections:

```toml
# No space before redirect (default)
space-redirects = false
```

```bash
# Result:
echo "hello" >file.txt
cat <input.txt
```

```toml
# Space before redirect
space-redirects = true
```

```bash
# Result:
echo "hello" > file.txt
cat < input.txt
```

#### keep-padding

Preserves alignment padding:

```toml
# Remove extra alignment spaces (default)
keep-padding = false
```

```bash
# Input with alignment:
short="value"
longer_var="another"

# Result (alignment removed):
short="value"
longer_var="another"
```

```toml
# Preserve alignment
keep-padding = true
```

```bash
# Result (alignment kept):
short=     "value"
longer_var="another"
```

#### func-next-line

Controls function brace placement:

```toml
# Opening brace on same line (default)
func-next-line = false
```

```bash
# Result:
my_function() {
    echo "hello"
}
```

```toml
# Opening brace on next line
func-next-line = true
```

```bash
# Result:
my_function()
{
    echo "hello"
}
```

## EditorConfig Integration

shfmt respects EditorConfig settings. Create or update `.editorconfig`:

```ini
# EditorConfig is awesome: https://EditorConfig.org

root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.sh]
indent_style = space
indent_size = 2

# shfmt-specific options
shell_variant = bash
binary_next_line = true
switch_case_indent = true
space_redirects = false
keep_padding = false
function_next_line = false
```

### EditorConfig Option Mapping

| shfmt flag | EditorConfig key |
|------------|------------------|
| `-i` | `indent_size` (0 for tabs) |
| `-ln` | `shell_variant` |
| `-bn` | `binary_next_line` |
| `-ci` | `switch_case_indent` |
| `-sr` | `space_redirects` |
| `-kp` | `keep_padding` |
| `-fn` | `function_next_line` |

## Command-Line Flags

### Basic Usage

```bash
# Format file in place
shfmt -w script.sh

# Show diff of changes
shfmt -d script.sh

# List files that need formatting
shfmt -l .

# Format and output to stdout
shfmt script.sh
```

### Formatting Options

```bash
# Set indent to 4 spaces
shfmt -i 4 script.sh

# Use tabs for indentation
shfmt -i 0 script.sh

# Specify shell dialect
shfmt -ln bash script.sh

# Binary operators on next line
shfmt -bn script.sh

# Indent switch cases
shfmt -ci script.sh

# Space after redirects
shfmt -sr script.sh

# Preserve padding
shfmt -kp script.sh

# Function brace on next line
shfmt -fn script.sh
```

### Combined Example

```bash
# Common configuration
shfmt -i 2 -ci -bn -w script.sh
```

## Project Configuration Patterns

### Minimal Bash Project

```toml
# .shfmt.toml
shell = "bash"
indent = 2
```

### POSIX-Compliant Scripts

```toml
# .shfmt.toml
shell = "posix"
indent = 4
binary-next-line = false
switch-case-indent = false
```

### Modern Bash with All Features

```toml
# .shfmt.toml
shell = "bash"
indent = 2
binary-next-line = true
switch-case-indent = true
space-redirects = false
func-next-line = false
```

### Team Standardization

```toml
# .shfmt.toml - enforce team standards
shell = "bash"
indent = 2
binary-next-line = true
switch-case-indent = true
keep-padding = false
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Shell Format Check
on: [push, pull_request]
jobs:
  shfmt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install shfmt
        run: |
          curl -sS https://webinstall.dev/shfmt | bash
          export PATH="$HOME/.local/bin:$PATH"
      - name: Check formatting
        run: shfmt -d .
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/scop/pre-commit-shfmt
    rev: v3.8.0-1
    hooks:
      - id: shfmt
        args: ["-w"]
```

### Makefile Target

```makefile
.PHONY: fmt-check fmt

fmt-check:
 shfmt -d .

fmt:
 shfmt -w .
```

## Best Practices

1. **Commit Configuration** - Always commit `.shfmt.toml` for team consistency
2. **Match Dialect** - Set `shell` to match your script shebangs
3. **EditorConfig First** - Use EditorConfig for IDE integration
4. **CI Enforcement** - Run `shfmt -d` in CI to catch formatting issues
5. **Consistent Indentation** - Pick 2 or 4 spaces and stick with it
6. **Document Choices** - Add comments explaining non-default options
7. **Version Lock** - Pin shfmt version in CI for reproducibility

## Troubleshooting

### Configuration Not Applied

Check precedence order:

1. Command-line flags override everything
2. EditorConfig in file's directory
3. `.shfmt.toml` in project root

### Wrong Shell Dialect

Verify shebang matches configuration:

```bash
# If using shell = "bash", ensure scripts have:
#!/usr/bin/env bash
# or
#!/bin/bash
```

### EditorConfig Not Detected

Ensure EditorConfig file is in parent directory chain and has correct section:

```ini
[*.sh]
shell_variant = bash
```

## When to Use This Skill

- Setting up shfmt in new projects
- Configuring team-wide formatting standards
- Integrating shfmt with CI/CD pipelines
- Troubleshooting configuration issues
- Migrating between configuration methods
- Setting up EditorConfig for shell scripts
