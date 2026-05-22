---
name: bash-portability
description: 'This skill should be used when the user asks about "POSIX compatibility", "portable shell scripts", "cross-shell compatibility", "bashisms", "shebang selection", or mentions writing scripts that work on different shells (bash, sh, dash, zsh) or different systems.'
---

# Bash Portability

Guidance for writing portable POSIX-compatible scripts and understanding when to leverage bash-specific features.

## Shebang Selection

### Use `#!/usr/bin/env bash` for Bash Scripts

```bash
#!/usr/bin/env bash
```

**Why:** Searches PATH for bash, works across systems where bash may be in different locations.

### Use `#!/bin/sh` for POSIX Scripts

```bash
#!/bin/sh
```

**Why:** Maximum portability when bash features aren't needed. On many systems, `/bin/sh` is dash or another POSIX shell.

### Direct Path When Required

```bash
#!/bin/bash
```

**Use only when:** System requirements guarantee bash location, or security policy requires absolute paths.

## POSIX vs Bash Feature Matrix

| Feature        | POSIX   | Bash | Recommendation                 |
| -------------- | ------- | ---- | ------------------------------ | ---- |
| `[[ ]]`        | No      | Yes  | Use `[ ]` for POSIX            |
| `(( ))`        | No      | Yes  | Use `[ ]` with `-eq` etc.      |
| Arrays         | No      | Yes  | Use positional params or files |
| `local`        | Partial | Yes  | Generally safe                 |
| `${var,,}`     | No      | 4+   | Use `tr` for POSIX             |
| `<<<`          | No      | Yes  | Use `echo                      | cmd` |
| `=~` regex     | No      | Yes  | Use `grep` or `expr`           |
| `source`       | No      | Yes  | Use `.` (dot) command          |
| `function f()` | No      | Yes  | Use `f()` only                 |
| `$'...'`       | No      | Yes  | Use `printf`                   |
| `{1..10}`      | No      | Yes  | Use `seq` or while loop        |

## POSIX-Compatible Patterns

### Conditionals

```bash
# POSIX - use [ ] with proper quoting
if [ -f "$file" ]; then
    echo "File exists"
fi

# String comparison
if [ "$var" = "value" ]; then
    echo "Match"
fi

# Numeric comparison
if [ "$num" -gt 10 ]; then
    echo "Greater"
fi

# Compound conditions
if [ -f "$file" ] && [ -r "$file" ]; then
    echo "Readable file"
fi
```

### Case Conversion (POSIX)

```bash
# Lowercase
lower=$(echo "$string" | tr '[:upper:]' '[:lower:]')

# Uppercase
upper=$(echo "$string" | tr '[:lower:]' '[:upper:]')
```

### Substring Operations (POSIX)

```bash
# Get substring - use expr or cut
substr=$(expr "$string" : '.\{3\}\(.\{5\}\)')  # chars 4-8
substr=$(echo "$string" | cut -c4-8)

# String length
length=$(expr length "$string")
length=${#string}  # This is actually POSIX
```

### Reading Files (POSIX)

```bash
# Line by line
while IFS= read -r line; do
    echo "$line"
done < "$file"

# Read entire file (without cat)
content=$(cat "$file")  # cat is POSIX
```

### Command Substitution

```bash
# Modern syntax (preferred even in POSIX)
result=$(command)

# Legacy syntax (avoid)
result=`command`

# Nested (why modern is better)
result=$(echo $(date))      # Clear
result=`echo \`date\``      # Escape nightmare
```

## Bash-Specific Features Worth Using

When portability isn't required, these bash features improve code quality:

### Extended Test `[[ ]]`

```bash
# Pattern matching
[[ "$file" == *.txt ]]

# Regex matching
[[ "$input" =~ ^[0-9]+$ ]]

# No word splitting worries
[[ -f $file ]]  # Quotes optional (but still recommended)

# Logical operators inside
[[ -f "$file" && -r "$file" ]]
```

### Arrays

```bash
# Indexed arrays
declare -a files=()
files+=("one.txt")
files+=("two.txt")
for f in "${files[@]}"; do
    process "$f"
done

# Associative arrays (Bash 4+)
declare -A config
config[host]="localhost"
config[port]="8080"
```

### Parameter Expansion

```bash
# Default value
"${var:-default}"

# Case conversion (Bash 4+)
"${var,,}"  # lowercase
"${var^^}"  # uppercase

# Substring
"${var:0:10}"  # first 10 chars
"${var: -5}"   # last 5 chars

# Search/replace
"${var//old/new}"
```

### Here Strings

```bash
# Bash
read -r var <<< "input string"

# POSIX equivalent
var=$(echo "input string")
```

### Process Substitution

```bash
# Bash - compare two command outputs
diff <(sort file1) <(sort file2)

# POSIX equivalent (with temp files)
sort file1 > /tmp/sorted1
sort file2 > /tmp/sorted2
diff /tmp/sorted1 /tmp/sorted2
```

## Detecting Shell Type

```bash
# Check if running in bash
if [ -n "${BASH_VERSION:-}" ]; then
    echo "Running in Bash"
fi

# Check bash version for features
if [ "${BASH_VERSINFO[0]:-0}" -ge 4 ]; then
    echo "Bash 4+ available"
fi

# Generic shell detection
case "${SHELL##*/}" in
    bash) echo "bash" ;;
    zsh)  echo "zsh" ;;
    *)    echo "other" ;;
esac
```

## Portable Utility Functions

```bash
# Command existence check (POSIX)
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Portable dirname
get_dirname() {
    case "$1" in
        */*) echo "${1%/*}" ;;
        *)   echo "." ;;
    esac
}

# Portable basename
get_basename() {
    case "$1" in
        */*) echo "${1##*/}" ;;
        *)   echo "$1" ;;
    esac
}

# Portable absolute path
get_abs_path() {
    (cd "$(dirname "$1")" && printf '%s/%s' "$(pwd)" "$(basename "$1")")
}
```

## Portability Decision Guide

**Use POSIX when:**

- Script runs on minimal systems (containers, embedded)
- Target includes dash, ash, or busybox sh
- Maximum compatibility is required
- Script is part of system initialization

**Use Bash when:**

- Target systems guaranteed to have bash
- Need arrays, associative arrays, or regex
- Complex string manipulation required
- Code clarity significantly improved
- Interactive features needed

## Common Portability Pitfalls

### echo vs printf

```bash
# Problematic - behavior varies
echo -n "no newline"
echo -e "with\ttabs"

# Portable
printf '%s' "no newline"
printf 'with\ttabs\n'
```

### Variable Assignment

```bash
# Works everywhere
var="value"

# May fail on some shells
var = "value"  # Spaces around = are wrong
```

### Export with Assignment

```bash
# POSIX - separate commands
var="value"
export var

# Bash/modern - combined (works most places)
export var="value"
```

### Array-like Operations Without Arrays

```bash
# Use positional parameters
set -- "item1" "item2" "item3"
for item in "$@"; do
    echo "$item"
done

# Or IFS-based splitting
items="item1:item2:item3"
IFS=':' read -r item1 item2 item3 <<EOF
$items
EOF
```
