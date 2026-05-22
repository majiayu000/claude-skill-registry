---
name: bash-development
description: 'This skill should be used when the user asks to "write a bash script", "create a shell script", "implement bash function", "parse arguments in bash", "handle errors in bash", or mentions bash development, shell scripting, script templates, or modern bash patterns.'
---

# Bash Development

Core patterns and best practices for Bash 5.1+ script development. Provides modern bash idioms, error handling, argument parsing, and pure-bash alternatives to external commands.

## Script Foundation

Every script starts with the essential header:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

**set options explained:**

- `-e` - Exit immediately on command failure
- `-u` - Treat unset variables as errors
- `-o pipefail` - Pipeline fails if any command fails

### Script Metadata Pattern

```bash
SCRIPT_NAME=$(basename "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
readonly SCRIPT_VERSION="1.0.0"
readonly SCRIPT_NAME SCRIPT_DIR
```

## Error Handling

Implement trap-based error handling for robust scripts:

```bash
handle_error() {
    local line="${1}"
    local exit_code="${2:-1}"
    printf '%s\n' "Error on line ${line}" >&2
    exit "${exit_code}"
}

trap 'handle_error ${LINENO} $?' ERR

cleanup() {
    # Cleanup logic here
    rm -f "${TEMP_FILE:-}"
}

trap cleanup EXIT
```

## Argument Parsing

Standard argument parsing template:

```bash
usage() {
    cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS] <argument>

Options:
    -h, --help      Show this help message
    -v, --version   Show version information
    -d, --debug     Enable debug mode
    -f, --file      Specify input file

Examples:
    ${SCRIPT_NAME} file.txt
    ${SCRIPT_NAME} --debug file.txt
EOF
}

main() {
    local debug=0
    local input_file=""

    while [[ $# -gt 0 ]]; do
        case "${1}" in
            -h|--help) usage; exit 0 ;;
            -v|--version) printf '%s version %s\n' "${SCRIPT_NAME}" "${SCRIPT_VERSION}"; exit 0 ;;
            -d|--debug) debug=1; set -x; shift ;;
            -f|--file) input_file="${2}"; shift 2 ;;
            -*) printf 'Unknown option: %s\n' "${1}" >&2; usage; exit 1 ;;
            *) break ;;
        esac
    done

    # Validate required arguments
    if [[ $# -lt 1 ]]; then
        printf 'Missing required argument\n' >&2
        usage
        exit 1
    fi

    # Main logic here
}

main "$@"
```

## Variable Best Practices

**Always use curly braces and quote variables:**

```bash
# Correct
"${variable}"
"${array[@]}"

# Incorrect
$variable
${array[*]}  # Use [@] for proper iteration
```

**Use readonly for constants:**

```bash
readonly CONFIG_FILE="/etc/app/config"
readonly -a VALID_OPTIONS=("opt1" "opt2" "opt3")
```

**Note:** Never use `readonly` in sourced scripts - it causes errors on re-sourcing.

## String Operations (Pure Bash)

Prefer native bash parameter expansion over external tools:

```bash
# Trim whitespace
trimmed="${string#"${string%%[![:space:]]*}"}"
trimmed="${trimmed%"${trimmed##*[![:space:]]}"}"

# Lowercase/Uppercase (Bash 4+)
lower="${string,,}"
upper="${string^^}"

# Substring extraction
substring="${string:0:10}"      # First 10 chars
suffix="${string: -5}"          # Last 5 chars

# Replace patterns
replaced="${string//old/new}"   # Replace all
replaced="${string/old/new}"    # Replace first

# Strip prefix/suffix
no_prefix="${string#prefix}"    # Shortest match
no_prefix="${string##*/}"       # Longest match (basename)
no_suffix="${string%suffix}"    # Shortest match
no_suffix="${string%%/*}"       # Longest match
```

## Array Operations

```bash
# Declaration
declare -a indexed_array=()
declare -A assoc_array=()

# Safe iteration with nullglob
shopt -s nullglob
for file in *.txt; do
    process "${file}"
done
shopt -u nullglob

# Array length
length="${#array[@]}"

# Append element
array+=("new_element")

# Iterate with index
for i in "${!array[@]}"; do
    printf '%d: %s\n' "${i}" "${array[i]}"
done
```

## File Operations

```bash
# Read file to string
content="$(<"${file}")"

# Read file to array (Bash 4+)
mapfile -t lines < "${file}"

# Check file conditions
[[ -f "${file}" ]]    # Regular file exists
[[ -d "${dir}" ]]     # Directory exists
[[ -r "${file}" ]]    # Readable
[[ -w "${file}" ]]    # Writable
[[ -x "${file}" ]]    # Executable
[[ -s "${file}" ]]    # Non-empty

# Safe temp file creation
temp_file=$(mktemp)
trap 'rm -f "${temp_file}"' EXIT
```

## Conditional Expressions

Use `[[ ]]` for conditionals (bash-specific, more powerful):

```bash
# String comparisons
[[ "${var}" == "value" ]]       # Equality
[[ "${var}" == pattern* ]]     # Glob matching
[[ "${var}" =~ ^regex$ ]]      # Regex matching

# Numeric comparisons
(( num > 10 ))                  # Arithmetic comparison
[[ "${num}" -gt 10 ]]          # Traditional syntax

# Compound conditions
[[ -f "${file}" && -r "${file}" ]]
[[ "${opt}" == "a" || "${opt}" == "b" ]]
```

## Utility Functions

```bash
# Check command existence
command_exists() {
    command -v "${1}" >/dev/null 2>&1
}

# Get script directory (resolves symlinks)
get_script_dir() {
    local source="${BASH_SOURCE[0]}"
    while [[ -L "${source}" ]]; do
        local dir=$(cd -P "$(dirname "${source}")" && pwd)
        source=$(readlink "${source}")
        [[ "${source}" != /* ]] && source="${dir}/${source}"
    done
    cd -P "$(dirname "${source}")" && pwd
}

# Conditional sudo
run_privileged() {
    if [[ "${EUID}" -eq 0 ]]; then
        "$@"
    elif command_exists sudo; then
        sudo "$@"
    else
        printf 'Error: root privileges required\n' >&2
        return 1
    fi
}
```

## Performance Guidelines

- Use builtins over external commands when possible
- Batch operations instead of loops for large datasets
- Use `printf` over `echo` for portability and control
- Avoid unnecessary subshells in tight loops
- Use `[[ ]]` over `[ ]` for string comparisons

## Additional Resources

### Reference Files

For detailed patterns and examples:

- **[bash_example_file.sh](./references/bash_example_file.sh)** - Complete script template
- **[bash_example_includes.bash](./references/bash_example_includes.bash)** - Reusable utility functions
- **[bash-agent-notes.markdown](./references/bash-agent-notes.markdown)** - Context-aware review guidance
- **[pure-bash-bible-strings.md](./references/pure-bash-bible-strings.md)** - String manipulation patterns
- **[pure-bash-bible-arrays.md](./references/pure-bash-bible-arrays.md)** - Array operations
- **[pure-bash-bible-files.md](./references/pure-bash-bible-files.md)** - File handling patterns
- **[pure-bash-bible-variables.md](./references/pure-bash-bible-variables.md)** - Parameter expansion reference
