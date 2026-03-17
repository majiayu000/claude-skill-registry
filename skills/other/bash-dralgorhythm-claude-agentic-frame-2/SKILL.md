---
name: bash
description: Write Bash scripts following best practices. Use when creating shell scripts, automation, or CLI tools. Covers safe scripting patterns.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bash Scripting

## Script Template

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Script description
# Usage: ./script.sh <arg1> <arg2>

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

main() {
    local arg1="${1:-default}"

    # Script logic here
    echo "Running with: $arg1"
}

main "$@"
```

## Safety Settings

```bash
set -e          # Exit on error
set -u          # Error on undefined variables
set -o pipefail # Catch pipe failures
set -x          # Debug: print commands
```

## Variables

```bash
# Declaration
readonly CONST="immutable"
local var="function scoped"

# Default values
name="${1:-default}"      # Use default if unset
name="${1:?Error: missing}"  # Error if unset

# String operations
"${var^^}"    # Uppercase
"${var,,}"    # Lowercase
"${var#prefix}"  # Remove prefix
"${var%suffix}"  # Remove suffix
```

## Conditionals

```bash
# File tests
[[ -f "$file" ]]  # Is file
[[ -d "$dir" ]]   # Is directory
[[ -r "$file" ]]  # Is readable
[[ -x "$file" ]]  # Is executable

# String tests
[[ -z "$var" ]]   # Is empty
[[ -n "$var" ]]   # Is not empty
[[ "$a" == "$b" ]] # Equals

# Numeric tests
(( num > 5 ))     # Greater than
(( num == 5 ))    # Equals
```

## Functions

```bash
log() {
    local level="$1"
    local message="$2"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $message" >&2
}

die() {
    log "ERROR" "$1"
    exit 1
}

require_command() {
    command -v "$1" >/dev/null 2>&1 || die "Required command not found: $1"
}
```

## Error Handling

```bash
# Trap for cleanup
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

# Catch errors
if ! result=$(some_command 2>&1); then
    die "Command failed: $result"
fi
```

## Loops

```bash
# For loop
for item in "${array[@]}"; do
    echo "$item"
done

# While read
while IFS= read -r line; do
    echo "$line"
done < file.txt

# Process substitution
while read -r line; do
    echo "$line"
done < <(command)
```

## Best Practices

1. Quote all variables: `"$var"`
2. Use `[[` instead of `[`
3. Use `local` in functions
4. Use `readonly` for constants
5. Always use `set -euo pipefail`
6. Use shellcheck for linting
