---
name: bash-script
description: Write robust bash scripts with proper error handling. Use when the user says "write a script", "bash script", "shell script", "automate this", "create a backup script", or asks to script a task.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Bash Script

Write robust, maintainable bash scripts with proper error handling.

## Instructions

1. Understand the task requirements
2. Design the script structure
3. Write with safety options and error handling
4. Test and validate

## Script template

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Description: Brief description of what this script does
# Usage: ./script.sh [options] <args>

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# Default values
VERBOSE="${VERBOSE:-false}"

usage() {
    cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS] <argument>

Description of what the script does.

Options:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose output

Examples:
    ${SCRIPT_NAME} input.txt
    ${SCRIPT_NAME} --verbose /path/to/file
EOF
}

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >&2
}

error() {
    log "ERROR: $*"
    exit 1
}

cleanup() {
    # Remove temp files, restore state, etc.
    rm -f "${TEMP_FILE:-}"
}
trap cleanup EXIT

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help) usage; exit 0 ;;
            -v|--verbose) VERBOSE=true; shift ;;
            --) shift; break ;;
            -*) error "Unknown option: $1" ;;
            *) break ;;
        esac
    done

    [[ $# -lt 1 ]] && { usage; exit 1; }

    local input="$1"
    [[ -f "$input" ]] || error "File not found: $input"

    # Main logic here
    log "Processing $input"
}

main "$@"
```

## Safety options explained

| Option            | Purpose                             |
| ----------------- | ----------------------------------- |
| `set -e`          | Exit on error                       |
| `set -u`          | Error on undefined variables        |
| `set -o pipefail` | Pipeline fails if any command fails |
| `IFS=$'\n\t'`     | Safer word splitting                |

## Best practices

- MUST use `set -euo pipefail` at script start
- MUST quote all variables: `"$var"` not `$var`
- MUST use `[[` for conditionals (not `[`)
- MUST use `$()` for command substitution (not backticks)
- Use `readonly` for constants
- Use `local` for function variables
- Use `trap` for cleanup
- Use `mktemp` for temp files

## Common patterns

```bash
# Check if command exists
command -v docker &>/dev/null || error "docker not found"

# Default value
name="${1:-default}"

# Read file line by line
while IFS= read -r line; do
    echo "$line"
done < "$file"

# Process arguments
for arg in "$@"; do
    echo "$arg"
done

# Temp file with cleanup
TEMP_FILE="$(mktemp)"
trap 'rm -f "$TEMP_FILE"' EXIT
```

## Rules

- MUST include `set -euo pipefail`
- MUST quote all variable expansions
- MUST include usage function for scripts with arguments
- MUST use trap for cleanup of temp files
- Never use `eval` with user input
- Never assume current directory
- Always use absolute paths for cron scripts
