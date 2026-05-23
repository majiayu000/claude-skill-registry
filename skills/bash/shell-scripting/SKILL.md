---
name: shell-scripting
description: Practical bash scripting guidance emphasising defensive programming, ShellCheck compliance, and simplicity. Use when writing shell scripts that need to be reliable and maintainable.
---

# Bash Scripting Best Practices

Guidance for writing reliable, maintainable bash scripts following modern best practices. Emphasises simplicity, automated tooling, and defensive programming without over-engineering.

## When to Use Shell (and When Not To)

### Use Shell For:
- Small utilities and simple wrapper scripts (<100 lines)
- Orchestrating other programmes and tools
- Simple automation tasks
- Build/deployment scripts with straightforward logic
- Quick data transformation pipelines

### Do NOT Use Shell For:
- Complex business logic or data structures
- Performance-critical code
- Scripts requiring extensive error handling
- Anything over ~100 lines or with non-straightforward control flow
- When you need proper data structures beyond arrays

**Critical**: If your script grows too large (1000+ lines) or complex, consider offering to rewrite it in a proper language (Python, Go, etc.) before it becomes unmaintainable.

## Mandatory Foundations

Every bash script must have these elements:

### 1. Proper Shebang
```bash
#!/usr/bin/env bash
```
**Why**: Portable across systems where bash may not be at `/bin/bash` (e.g., macOS, BSD, NixOS).

**Alternative**: `#!/bin/bash` if you know the script only runs on Linux and prefer explicit paths.

### 2. Strict Mode
```bash
set -euo pipefail
```
**What each flag does:**
- `-e`: Exit immediately if any command fails (non-zero exit)
- `-u`: Treat unset variables as errors
- `-o pipefail`: Pipe fails if ANY command in pipeline fails (not just the last)

**When to add `-x`**: Only for debugging, not in production scripts (makes output noisy).

### 3. ShellCheck Compliance
Run ShellCheck on EVERY script before committing:
```bash
shellcheck script.sh
```

Fix all warnings. ShellCheck catches:
- Unquoted variables
- Deprecated syntax
- Common bugs and pitfalls
- Portability issues

### 4. Basic Script Structure
```bash
#!/usr/bin/env bash
set -euo pipefail

# Brief description of what this script does

# Simple error reporting
die() {
    echo "Error: ${1}" >&2
    exit 1
}

# Your code here
```

## Core Safety Patterns

### Always Quote Variables
**Why**: Prevents word splitting and globbing disasters.

```bash
# Wrong - dangerous
cp $source $destination
rm -rf $prefix/bin

# Correct - safe
cp "${source}" "${destination}"
rm -rf "${prefix}/bin"

# Special case: Always use braces with variables
echo "${var}"      # Good
echo "$var"        # Acceptable but less consistent
echo $var          # Bad - unquoted
```

### Check Required Variables
```bash
# Fail fast if required variables aren't set
: "${REQUIRED_VAR:?REQUIRED_VAR must be set}"

# Or with custom message
: "${DATABASE_URL:?DATABASE_URL is required. Set it in .env}"
```

### Validate Inputs
```bash
# Check file exists before operating on it
[[ -f "${config_file}" ]] || die "Config file not found: ${config_file}"

# Check command exists before using it
command -v jq >/dev/null 2>&1 || die "jq is required but not installed"

# Validate directory before cd
[[ -d "${target_dir}" ]] || die "Directory does not exist: ${target_dir}"
```

## Essential Patterns

### Pattern 1: Simple Script Template
Use this for straightforward scripts:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Description: Process log files and extract errors

die() {
    echo "Error: ${1}" >&2
    exit 1
}

# Check dependencies
command -v jq >/dev/null 2>&1 || die "jq required"

# Validate arguments
[[ $# -eq 1 ]] || die "Usage: ${0} <logfile>"
logfile="${1}"
[[ -f "${logfile}" ]] || die "File not found: ${logfile}"

# Main logic
grep ERROR "${logfile}" | jq -r '.message'
```

### Pattern 2: Cleanup on Exit
Use trap for guaranteed cleanup:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Create temp directory and ensure cleanup
tmpdir=$(mktemp -d)
trap 'rm -rf "${tmpdir}"' EXIT

# Now use tmpdir safely - cleanup happens automatically
echo "Working in: ${tmpdir}"
```

### Pattern 3: Safe Function Definition
Functions should be simple and focused:

```bash
# Good: Simple, single-purpose function
check_dependency() {
    local cmd="${1}"
    command -v "${cmd}" >/dev/null 2>&1 || die "${cmd} not installed"
}

# Good: Local variables, clear purpose
process_file() {
    local file="${1}"
    local output="${2}"

    [[ -f "${file}" ]] || die "Input file missing: ${file}"

    # Do processing
    sed 's/foo/bar/g' "${file}" > "${output}"
}
```

**Important**: Declare and set variables from command substitution separately to catch errors:

```bash
# Wrong - hides errors
local result="$(failing_command)"

# Correct - catches errors
local result
result="$(failing_command)"  # Will fail properly with set -e
```

### Pattern 4: Safe Array Handling
Arrays are useful for handling lists with spaces:

```bash
# Create array
declare -a files=("file one.txt" "file two.txt" "file three.txt")

# Iterate safely - always quote with [@]
for file in "${files[@]}"; do
    echo "Processing: ${file}"
done

# Build command arguments safely
declare -a flags=(--verbose --output "${output_file}")
mycommand "${flags[@]}" "${input}"

# Read command output into array
mapfile -t lines < <(grep pattern "${file}")
```

### Pattern 5: Conditional Testing
Use `[[ ]]` for bash (safer and more features):

```bash
# File tests
[[ -f "${file}" ]]          # File exists
[[ -d "${dir}" ]]           # Directory exists
[[ -r "${file}" ]]          # File readable
[[ -w "${file}" ]]          # File writable
[[ -x "${binary}" ]]        # File executable

# String tests
[[ -z "${var}" ]]           # String is empty
[[ -n "${var}" ]]           # String is not empty
[[ "${a}" == "${b}" ]]      # String equality (use ==, not =)

# Numeric comparison (use (( )) for numbers)
(( count > 0 ))
(( total >= minimum ))

# Combined conditions
[[ -f "${file}" && -r "${file}" ]] || die "File not readable: ${file}"
```

### Pattern 6: Simple Argument Handling
For simple scripts, prefer positional arguments:

```bash
#!/usr/bin/env bash
set -euo pipefail

# For 1-3 arguments, just use positional parameters
[[ $# -eq 2 ]] || die "Usage: ${0} <source> <dest>"

source="${1}"
dest="${2}"

[[ -f "${source}" ]] || die "Source not found: ${source}"
```

For scripts needing flags, keep it simple:

```bash
# Use environment variables instead of complex flag parsing
VERBOSE="${VERBOSE:-false}"
DRY_RUN="${DRY_RUN:-false}"

# Run like: VERBOSE=true DRY_RUN=true ./script.sh input.txt
```

### Pattern 7: Process Substitution Over Temp Files
Avoid creating temporary files when possible:

```bash
# Instead of:
first_command > /tmp/output.txt
second_command < /tmp/output.txt
rm /tmp/output.txt

# Use process substitution:
second_command <(first_command)

# For multiple inputs:
diff <(sort file1.txt) <(sort file2.txt)
```

### Pattern 8: Prefer Builtins Over External Commands
Builtins are faster and more reliable:

```bash
# Use bash parameter expansion over sed/awk for simple cases
filename="${path##*/}"           # basename
dirname="${path%/*}"             # dirname
extension="${filename##*.}"      # get extension
name="${filename%.*}"            # remove extension

# Use (( )) for arithmetic over expr
count=$(( count + 1 ))           # Not: count=$(expr ${count} + 1)

# Use [[ ]] over [ ] or test
[[ -f "${file}" ]]               # Not: test -f "${file}"

# Use ${#var} for string length
length="${#string}"              # Not: length=$(echo "${string}" | wc -c)
```

## Intermediate Patterns

### Pattern 9: Structured Logging
Keep logging simple and consistent:

```bash
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ${1}" >&2
}

error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: ${1}" >&2
}

# Usage
log "Starting process"
error "Failed to connect to database"
```

### Pattern 10: Main Function Pattern
For longer scripts (50+ lines), use a main function:

```bash
#!/usr/bin/env bash
set -euo pipefail

setup() {
    # Dependency checks, variable initialisation
    command -v jq >/dev/null 2>&1 || die "jq required"
}

process() {
    # Main logic here
    log "Processing data"
}

cleanup() {
    # Cleanup if needed
    log "Cleanup complete"
}

main() {
    setup
    process
    cleanup
}

# Call main with all script arguments
main "${@}"
```

### Pattern 11: Idempotent Operations
Scripts should be safe to run multiple times:

```bash
# Check before creating
if [[ ! -d "${target_dir}" ]]; then
    mkdir -p "${target_dir}"
fi

# Check before writing config
if [[ ! -f "${config_file}" ]]; then
    echo "DEFAULT_VALUE=true" > "${config_file}"
fi

# Use atomic operations
mv "${source}" "${dest}"  # Atomic on same filesystem
```

### Pattern 12: Safe While Loop Reading
Don't pipe to while (creates subshell):

```bash
# Wrong - variables modified in subshell are lost
count=0
cat file.txt | while read -r line; do
    (( count++ ))
done
echo "${count}"  # Will be 0!

# Correct - use process substitution
count=0
while read -r line; do
    (( count++ ))
done < <(cat file.txt)
echo "${count}"  # Correct count

# Or use mapfile for simple cases
mapfile -t lines <file.txt
count="${#lines[@]}"
```

## Style Guidelines

### Formatting
- **Indentation**: 2 spaces, never tabs
- **Line length**: Maximum 120 characters
- **Long strings**: Use here-documents or embedded newlines

```bash
# Long command - break at logical points
docker run \
    --name my-container \
    --volume "${PWD}:/data" \
    --env "FOO=bar" \
    my-image:latest

# Long string - use here-doc
cat <<EOF
This is a long message
that spans multiple lines
and is more readable this way.
EOF
```

### Naming Conventions
```bash
# Functions: lowercase with underscores
check_dependencies() { ... }
process_files() { ... }

# Local variables: lowercase with underscores
local input_file="${1}"
local line_count=0

# Constants/environment variables: UPPERCASE with underscores
readonly MAX_RETRIES=3
readonly CONFIG_DIR="/etc/myapp"

# Source files: lowercase with underscores
# my_library.sh
```

### File Extensions
- **Executables**: `.sh` extension OR no extension (prefer no extension for user-facing commands)
- **Libraries**: Always `.sh` extension and NOT executable

## Function Documentation

Document functions that aren't obvious:

```bash
# Good: Simple function, no comment needed (name says it all)
check_file_exists() {
    [[ -f "${1}" ]]
}

# Good: Complex function, documented
# Processes log files and extracts error messages
# Arguments:
#   $1 - Input log file path
#   $2 - Output directory
# Returns:
#   0 on success, 1 on failure
process_logs() {
    local logfile="${1}"
    local output_dir="${2}"
    # Implementation
}
```

## What to Avoid

### Don't Use These
```bash
# Don't use backticks - use $()
output=`command`          # Old style
output=$(command)         # Correct

# Don't use eval - almost always wrong
eval "${user_input}"      # Dangerous!

# Don't use expr - use (( ))
result=$(expr 5 + 3)      # Old style
result=$(( 5 + 3 ))       # Correct

# Don't use [ ] when [[ ]] is available
[ -f "${file}" ]          # POSIX compatible, less features
[[ -f "${file}" ]]        # Bash, safer and more features

# Don't use $[ ] for arithmetic - deprecated
result=$[5 + 3]           # Deprecated
result=$(( 5 + 3 ))       # Correct

# Don't use function keyword unnecessarily
function foo() { ... }    # Redundant
foo() { ... }             # Cleaner
```

### Anti-Patterns
```bash
# Don't glob or split unquoted
rm ${files}               # DANGEROUS
rm "${files}"             # Safe

# Don't use ls output in scripts
for file in $(ls); do     # Breaks with spaces
for file in *; do         # Correct

# Don't pipe yes to commands
yes | risky-command       # Bypasses important prompts

# Don't ignore error codes
make build                # Did it work?
make build || die "Build failed"  # Better
```

## Complexity Warning Signs

If your script has any of these, consider rewriting in Python/Go:

- More than 100 lines
- Complex data structures beyond simple arrays
- Nested loops over arrays of arrays
- Heavy string manipulation logic
- Complex state management
- Mathematical calculations beyond basic arithmetic
- Need for unit testing individual functions
- JSON/YAML parsing beyond simple jq queries

## Advanced: Dry-Run Pattern

For scripts that modify things:

```bash
DRY_RUN="${DRY_RUN:-false}"

run() {
    if [[ "${DRY_RUN}" == "true" ]]; then
        echo "[DRY RUN] ${*}" >&2
        return 0
    fi
    "${@}"
}

# Usage
run cp "${source}" "${dest}"
run rm -f "${old_file}"

# Run script: DRY_RUN=true ./script.sh
```

## Quick Reference Checklist

Before considering a bash script complete:

- [ ] ShellCheck passes with no warnings
- [ ] Has proper shebang (`#!/usr/bin/env bash`)
- [ ] Has strict mode (`set -euo pipefail`)
- [ ] All variables quoted (`"${var}"`)
- [ ] Required dependencies checked
- [ ] Proper error messages to stderr
- [ ] Cleanup trap if using temp files
- [ ] Script is idempotent where possible
- [ ] Under 100 lines (or has strong justification)
- [ ] Uses `command -v` not `which`
- [ ] Arrays used for lists with spaces
- [ ] No `eval`, `ls` parsing, or backticks
- [ ] Functions have local variables

## Summary

1. **Start simple**: Don't over-engineer. Most scripts should be <50 lines.
2. **Use ShellCheck**: It catches most problems automatically.
3. **Quote everything**: `"${var}"` not `$var`.
4. **Fail fast**: `set -euo pipefail` and validate inputs.
5. **Know when to stop**: If it's getting complex, use a real language.
6. **Compose don't complicate**: Use pipes and process substitution.
7. **Be idempotent**: Scripts should be safe to run multiple times.
8. **Test error paths**: Make sure your script fails safely.

Remember: Shell scripts are for gluing things together, not building complex logic. Keep them simple, safe, and focused.
