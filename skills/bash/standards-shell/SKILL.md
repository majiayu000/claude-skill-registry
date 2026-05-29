---
name: standards-shell
description: This skill provides Shell/Bash coding standards and is automatically loaded for shell projects. It includes defensive scripting patterns, best practices, and recommended tooling.
type: context
applies_to: [bash, sh, shell, zsh, shellcheck, bats]
file_extensions: [".sh", ".bash"]
---

# Shell/Bash Coding Standards

## Core Principles

1. **Simplicity**: Simple, understandable scripts
2. **Readability**: Readability over cleverness
3. **Maintainability**: Scripts that are easy to maintain
4. **Testability**: Scripts that are easy to test
5. **DRY**: Don't Repeat Yourself - but don't overdo it
6. **Defensiveness**: Fail early, fail loudly

## General Rules

- **Defensive Header**: Always use `set -euo pipefail`
- **Quote Variables**: Always quote variables `"$var"`
- **Descriptive Names**: Meaningful names for variables and functions
- **Minimal Changes**: Only change relevant code parts
- **No Over-Engineering**: No unnecessary complexity
- **ShellCheck Clean**: All scripts must pass ShellCheck

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Variables | snake_case | `user_name`, `file_count` |
| Functions | snake_case | `get_user_by_id`, `validate_input` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| Files | kebab-case or snake_case | `deploy-app.sh`, `run_tests.sh` |
| Environment Vars | UPPER_SNAKE_CASE | `API_URL`, `DATABASE_HOST` |

## Script Template

```bash
#!/bin/bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# Cleanup on exit
cleanup() {
    rm -f "$SCRIPT_DIR"/*.tmp 2>/dev/null || true
}
trap cleanup EXIT

# Error handler
error_handler() {
    echo "Error on line $1" >&2
    exit 1
}
trap 'error_handler $LINENO' ERR

main() {
    # Script logic here
    echo "Running $SCRIPT_NAME"
}

main "$@"
```

## Defensive Scripting

```bash
# REQUIRED: Always start with this
set -euo pipefail
# -e: Exit on error
# -u: Error on undefined variables
# -o pipefail: Pipe fails if any command fails

# RECOMMENDED: Safer IFS
IFS=$'\n\t'

# REQUIRED: Quote all variables
echo "$var"                     # Good
echo $var                       # Bad - word splitting

# REQUIRED: Use [[ ]] for conditionals (Bash)
if [[ -f "$file" ]]; then       # Good
if [ -f "$file" ]; then         # POSIX only
```

## Parameter Expansion

```bash
# Defaults and validation
${var:-default}             # Use default if unset
${var:=default}             # Assign default if unset
${var:?error message}       # Error if unset

# String manipulation
${var#pattern}              # Remove prefix (shortest)
${var##pattern}             # Remove prefix (longest)
${var%pattern}              # Remove suffix (shortest)
${var%%pattern}             # Remove suffix (longest)
${var/old/new}              # Replace first
${var//old/new}             # Replace all
${#var}                     # Length

# Examples
file="document.txt"
echo "${file%%.*}"          # "document" (remove extension)
echo "${file##*.}"          # "txt" (get extension)
```

## Functions

```bash
# REQUIRED: Use local variables
get_user_name() {
    local user_id=$1
    local name
    name=$(grep "^${user_id}:" /etc/passwd | cut -d: -f5)
    echo "$name"
}

# Return values via stdout
result=$(get_user_name "1000")

# Return status codes
validate_file() {
    local file=$1
    if [[ ! -f "$file" ]]; then
        echo "Error: File not found: $file" >&2
        return 1
    fi
    return 0
}

if validate_file "$input_file"; then
    process_file "$input_file"
fi
```

## Arrays

```bash
# Indexed arrays
files=("file1.txt" "file2.txt" "file3.txt")
echo "${files[0]}"          # First element
echo "${files[@]}"          # All elements
echo "${#files[@]}"         # Array length

# Iterate safely
for file in "${files[@]}"; do
    echo "Processing: $file"
done

# Associative arrays (Bash 4+)
declare -A config
config[host]="localhost"
config[port]="8080"
echo "${config[host]}:${config[port]}"
```

## File Operations

```bash
# Read file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < "input.txt"

# Read into array
mapfile -t lines < "input.txt"

# Write to file (heredoc)
cat > output.txt <<EOF
Line 1
Line 2
EOF

# Temp files with cleanup
temp_file=$(mktemp)
trap 'rm -f "$temp_file"' EXIT
```

## Error Handling

```bash
# Trap for cleanup
cleanup() {
    echo "Cleaning up..."
    rm -f "$temp_file"
}
trap cleanup EXIT

# Trap for errors
error_handler() {
    local line=$1
    echo "Error occurred on line $line" >&2
}
trap 'error_handler $LINENO' ERR

# Check command exists
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 not found" >&2
    exit 1
fi

# Conditional execution
command1 && command2        # Run command2 only if command1 succeeds
command1 || command2        # Run command2 only if command1 fails
```

## Argument Parsing with getopts

```bash
usage() {
    echo "Usage: $0 [-v] [-o output] [-h]"
    echo "  -v        Verbose mode"
    echo "  -o FILE   Output file"
    echo "  -h        Show help"
    exit 1
}

verbose=false
output_file=""

while getopts "vo:h" opt; do
    case $opt in
        v) verbose=true ;;
        o) output_file="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done
shift $((OPTIND - 1))

# Remaining args in $@
```

## Logging

```bash
log() {
    local level=$1
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" >&2
}

log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }

# Usage
log_info "Starting process"
log_error "Failed to connect"
```

## Debugging

```bash
# Enable debugging
set -x                      # Print commands
PS4='+ ${BASH_SOURCE}:${LINENO}: '  # Better debug output

# Debug specific section
set -x
# code to debug
set +x

# Run script with debug
bash -x script.sh
bash -n script.sh           # Syntax check only
```

## Common Patterns

```bash
# Check if root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" >&2
    exit 1
fi

# Safe directory change
cd "$target_dir" || exit 1

# Process files safely (handles spaces)
find . -name "*.txt" -print0 | while IFS= read -r -d '' file; do
    echo "Processing: $file"
done

# Retry pattern
retry() {
    local max_attempts=$1
    local delay=$2
    shift 2
    local attempt=1

    while [[ $attempt -le $max_attempts ]]; do
        if "$@"; then
            return 0
        fi
        log_warn "Attempt $attempt failed, retrying in ${delay}s..."
        sleep "$delay"
        ((attempt++))
    done
    return 1
}

retry 3 5 curl -f "https://api.example.com/health"
```

## Recommended Tooling

| Tool | Purpose |
|------|---------|
| `shellcheck` | Static analysis (required) |
| `shfmt` | Code formatting |
| `bats-core` | Testing framework |
| `bash 5.x` | Modern features (avoid macOS default 3.2) |

## ShellCheck Usage

```bash
# Run ShellCheck
shellcheck script.sh

# Disable specific warning (sparingly)
# shellcheck disable=SC2086
echo $UNQUOTED_VAR

# Follow sourced files
shellcheck -x script.sh
```

## Testing with bats-core

```bash
#!/usr/bin/env bats
# File: test_script.bats

source ./script.sh

@test "add function returns correct sum" {
    result=$(add 5 3)
    [ "$result" = "8" ]
}

@test "validate_file fails on missing file" {
    run validate_file "nonexistent.txt"
    [ "$status" -eq 1 ]
}
```

Run tests:
```bash
bats tests/
```

## POSIX Compatibility

For maximum portability (sh, dash, ash):

```sh
#!/bin/sh
# Use [ ] instead of [[ ]]
if [ -f "file.txt" ]; then
    echo "File exists"
fi

# No arrays, use positional parameters
set -- "apple" "banana" "cherry"
echo "First: $1"

# No $() in older shells, use backticks
current_date=`date +%Y-%m-%d`
```

## Production Best Practices

1. **Defensive header** - Always `set -euo pipefail`
2. **Quote everything** - Prevent word splitting and glob expansion
3. **Local variables** - Use `local` in functions
4. **ShellCheck clean** - No warnings before commit
5. **Cleanup traps** - Always clean up temp files
6. **Meaningful exit codes** - 0 for success, non-zero for errors
7. **Logging to stderr** - Keep stdout for data, stderr for logs
8. **Check dependencies** - Verify required commands exist
9. **Handle signals** - Trap SIGTERM for graceful shutdown
10. **Document usage** - Include `--help` option

---

## References

- Based on [moai-lang-shell](https://github.com/AJBcoding/claude-skill-eval/tree/main/skills/moai-lang-shell) by AJBcoding
