---
name: debugging-troubleshooting-2025
description: Comprehensive bash script debugging and troubleshooting techniques for 2025
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Bash Debugging & Troubleshooting (2025)

## Overview

Comprehensive debugging techniques and troubleshooting patterns for bash scripts following 2025 best practices.

## Debug Mode Techniques

### 1. Basic Debug Mode (set -x)

```bash
#!/usr/bin/env bash
set -euo pipefail

# Enable debug mode
set -x

# Your commands here
command1
command2

# Disable debug mode
set +x

# Continue without debug
command3
```

### 2. Enhanced Debug Output (PS4)

```bash
#!/usr/bin/env bash
set -euo pipefail

# Custom debug prompt with file:line:function
export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'

set -x
my_function() {
    local var="value"
    echo "$var"
}
my_function
set +x
```

**Output:**
```
+(script.sh:10): my_function(): local var=value
+(script.sh:11): my_function(): echo value
value
```

### 3. Conditional Debugging

```bash
#!/usr/bin/env bash
set -euo pipefail

# Enable via environment variable
DEBUG="${DEBUG:-false}"

debug() {
    if [[ "$DEBUG" == "true" ]]; then
        echo "[DEBUG] $*" >&2
    fi
}

# Usage
debug "Starting process"
process_data
debug "Process complete"

# Run: DEBUG=true ./script.sh
```

### 4. Debugging Specific Functions

```bash
#!/usr/bin/env bash
set -euo pipefail

# Debug wrapper
debug_function() {
    local func_name="$1"
    shift

    echo "[TRACE] Calling: $func_name $*" >&2
    set -x
    "$func_name" "$@"
    local exit_code=$?
    set +x
    echo "[TRACE] Exit code: $exit_code" >&2
    return $exit_code
}

# Usage
my_complex_function() {
    local arg1="$1"
    # Complex logic
    echo "Result: $arg1"
}

debug_function my_complex_function "test"
```

## Tracing and Profiling

### 1. Execution Time Profiling

```bash
#!/usr/bin/env bash
set -euo pipefail

# Profile function execution time
profile() {
    local start_ns end_ns duration_ms
    start_ns=$(date +%s%N)

    "$@"
    local exit_code=$?

    end_ns=$(date +%s%N)
    duration_ms=$(( (end_ns - start_ns) / 1000000 ))

    echo "[PROFILE] '$*' took ${duration_ms}ms (exit: $exit_code)" >&2
    return $exit_code
}

# Usage
profile slow_command arg1 arg2
```

### 2. Function Call Tracing

```bash
#!/usr/bin/env bash
set -euo pipefail

# Trace all function calls
trace_on() {
    set -o functrace
    trap 'echo "[TRACE] ${FUNCNAME[0]}() called from ${BASH_SOURCE[1]}:${BASH_LINENO[0]}" >&2' DEBUG
}

trace_off() {
    set +o functrace
    trap - DEBUG
}

# Usage
trace_on
function1
function2
trace_off
```

### 3. Variable Inspection

```bash
#!/usr/bin/env bash
set -euo pipefail

# Inspect all variables at any point
inspect_vars() {
    echo "=== Variable Dump ===" >&2
    declare -p | grep -v "^declare -[^ ]*r " | sort >&2
    echo "===================" >&2
}

# Inspect specific variable
inspect_var() {
    local var_name="$1"
    echo "[INSPECT] $var_name = ${!var_name:-<unset>}" >&2
}

# Usage
my_var="test"
inspect_var my_var
inspect_vars
```

## Error Handling and Recovery

### 1. Trap-Based Error Handler

```bash
#!/usr/bin/env bash
set -euo pipefail

# Comprehensive error handler
error_handler() {
    local exit_code=$?
    local line_number=$1

    echo "ERROR: Command failed with exit code $exit_code" >&2
    echo "  File: ${BASH_SOURCE[1]}" >&2
    echo "  Line: $line_number" >&2
    echo "  Function: ${FUNCNAME[1]:-main}" >&2

    # Print stack trace
    local frame=0
    while caller $frame; do
        ((frame++))
    done >&2

    exit "$exit_code"
}

trap 'error_handler $LINENO' ERR

# Your script logic
risky_command
```

### 2. Dry-Run Mode

```bash
#!/usr/bin/env bash
set -euo pipefail

DRY_RUN="${DRY_RUN:-false}"

# Safe execution wrapper
execute() {
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "[DRY-RUN] Would execute: $*" >&2
        return 0
    else
        "$@"
    fi
}

# Usage
execute rm -rf /tmp/data
execute cp file.txt backup/

# Run: DRY_RUN=true ./script.sh
```

### 3. Rollback on Failure

```bash
#!/usr/bin/env bash
set -euo pipefail

OPERATIONS=()

# Track operations for rollback
track_operation() {
    local rollback_cmd="$1"
    OPERATIONS+=("$rollback_cmd")
}

# Execute rollback
rollback() {
    echo "Rolling back operations..." >&2
    for ((i=${#OPERATIONS[@]}-1; i>=0; i--)); do
        echo "  Executing: ${OPERATIONS[$i]}" >&2
        eval "${OPERATIONS[$i]}" || true
    done
}

trap rollback ERR EXIT

# Example usage
mkdir /tmp/mydir
track_operation "rmdir /tmp/mydir"

touch /tmp/mydir/file.txt
track_operation "rm /tmp/mydir/file.txt"

# If script fails, rollback executes automatically
```

## Common Issues and Solutions

### 1. Script Works Interactively but Fails in Cron

**Problem:** Script runs fine manually but fails when scheduled.

**Solution:**
```bash
#!/usr/bin/env bash
set -euo pipefail

# Fix PATH for cron
export PATH="/usr/local/bin:/usr/bin:/bin"

# Set working directory
cd "$(dirname "$0")" || exit 1

# Log everything for debugging
exec 1>> /var/log/myscript.log 2>&1

echo "[$(date)] Script starting"
# Your commands here
echo "[$(date)] Script complete"
```

### 2. Whitespace in Filenames Breaking Script

**Problem:** Script fails when processing files with spaces.

**Debugging:**
```bash
#!/usr/bin/env bash
set -euo pipefail

# Show exactly what the script sees
debug_filename() {
    local filename="$1"
    echo "Filename: '$filename'" >&2
    echo "Length: ${#filename}" >&2
    hexdump -C <<< "$filename" >&2
}

# Proper handling
while IFS= read -r -d '' file; do
    debug_filename "$file"
    # Process "$file"
done < <(find . -name "*.txt" -print0)
```

### 3. Script Behaves Differently on Different Systems

**Problem:** Works on Linux but fails on macOS.

**Debugging:**
```bash
#!/usr/bin/env bash
set -euo pipefail

# Platform detection and debugging
detect_platform() {
    echo "=== Platform Info ===" >&2
    echo "OS: $OSTYPE" >&2
    echo "Bash: $BASH_VERSION" >&2
    echo "PATH: $PATH" >&2

    # Check tool versions
    for tool in sed awk grep; do
        if command -v "$tool" &> /dev/null; then
            echo "$tool: $($tool --version 2>&1 | head -1)" >&2
        fi
    done
    echo "====================" >&2
}

detect_platform

# Use portable patterns
case "$OSTYPE" in
    linux*)   SED_CMD="sed" ;;
    darwin*)  SED_CMD=$(command -v gsed || echo sed) ;;
    *)        echo "Unknown platform" >&2; exit 1 ;;
esac
```

### 4. Variable Scope Issues

**Problem:** Variables not available where expected.

**Debugging:**
```bash
#!/usr/bin/env bash
set -euo pipefail

# Show variable scope
test_scope() {
    local local_var="local"
    global_var="global"

    echo "Inside function:" >&2
    echo "  local_var=$local_var" >&2
    echo "  global_var=$global_var" >&2
}

test_scope

echo "Outside function:" >&2
echo "  local_var=${local_var:-<not set>}" >&2
echo "  global_var=${global_var:-<not set>}" >&2

# Subshell scope issue
echo "test" | (
    read -r value
    echo "In subshell: $value"
)
echo "After subshell: ${value:-<not set>}"  # Empty!
```

## Interactive Debugging

### 1. Breakpoint Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

# Interactive breakpoint
breakpoint() {
    local message="${1:-Breakpoint}"
    echo "$message" >&2
    echo "Variables:" >&2
    declare -p | grep -v "^declare -[^ ]*r " >&2

    read -rp "Press Enter to continue, 'i' for inspect: " choice
    if [[ "$choice" == "i" ]]; then
        bash  # Drop into interactive shell
    fi
}

# Usage
value=42
breakpoint "Before critical operation"
critical_operation "$value"
```

### 2. Watch Mode (Continuous Debugging)

```bash
#!/usr/bin/env bash

# Watch script execution in real-time
watch_script() {
    local script="$1"
    shift

    while true; do
        clear
        echo "=== Running: $script $* ==="
        echo "=== $(date) ==="
        bash -x "$script" "$@" 2>&1 | tail -50
        sleep 2
    done
}

# Usage: watch_script myscript.sh arg1 arg2
```

## Logging Best Practices

### 1. Structured Logging

```bash
#!/usr/bin/env bash
set -euo pipefail

readonly LOG_FILE="${LOG_FILE:-/var/log/myscript.log}"

log() {
    local level="$1"
    shift
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    echo "${timestamp} [${level}] $*" | tee -a "$LOG_FILE" >&2
}

log_info()  { log "INFO"  "$@"; }
log_warn()  { log "WARN"  "$@"; }
log_error() { log "ERROR" "$@"; }
log_debug() { [[ "${DEBUG:-false}" == "true" ]] && log "DEBUG" "$@"; }

# Usage
log_info "Starting process"
log_debug "Debug info"
log_error "Something failed"
```

### 2. Log Rotation Awareness

```bash
#!/usr/bin/env bash
set -euo pipefail

# Ensure log file exists and is writable
setup_logging() {
    local log_file="${1:-/var/log/myscript.log}"
    local log_dir
    log_dir=$(dirname "$log_file")

    if [[ ! -d "$log_dir" ]]; then
        mkdir -p "$log_dir" || {
            echo "Cannot create log directory: $log_dir" >&2
            return 1
        }
    fi

    if [[ ! -w "$log_dir" ]]; then
        echo "Log directory not writable: $log_dir" >&2
        return 1
    fi

    # Redirect all output to log
    exec 1>> "$log_file"
    exec 2>&1
}

setup_logging
```

## Performance Debugging

### 1. Identify Slow Commands

```bash
#!/usr/bin/env bash
set -euo pipefail

# Profile each command in script
profile_script() {
    export PS4='+ $(date +%s.%N) ${BASH_SOURCE}:${LINENO}: '
    set -x

    # Your commands here
    command1
    command2
    command3

    set +x
}

# Analyze output:
# + 1698765432.123456 script.sh:10: command1  (fast)
# + 1698765437.654321 script.sh:11: command2  (5 seconds - slow!)
```

### 2. Memory Usage Tracking

```bash
#!/usr/bin/env bash
set -euo pipefail

# Track memory usage
check_memory() {
    local pid=${1:-$$}
    ps -o pid,vsz,rss,comm -p "$pid" | tail -1
}

# Monitor during execution
monitor_memory() {
    while true; do
        check_memory
        sleep 1
    done &
    local monitor_pid=$!

    # Your commands here
    "$@"

    kill "$monitor_pid" 2>/dev/null || true
    wait "$monitor_pid" 2>/dev/null || true
}

monitor_memory ./memory_intensive_task.sh
```

## Testing Patterns

### 1. Unit Test Template

```bash
#!/usr/bin/env bash
# test_functions.sh

# Source the script to test
source ./functions.sh

# Test counter
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Assert function
assert_equals() {
    local expected="$1"
    local actual="$2"
    local test_name="${3:-Test}"

    ((TESTS_RUN++))

    if [[ "$expected" == "$actual" ]]; then
        echo "✓ $test_name" >&2
        ((TESTS_PASSED++))
    else
        echo "✗ $test_name" >&2
        echo "  Expected: $expected" >&2
        echo "  Actual:   $actual" >&2
        ((TESTS_FAILED++))
    fi
}

# Run tests
test_add_numbers() {
    local result
    result=$(add_numbers 2 3)
    assert_equals "5" "$result" "add_numbers 2 3"
}

test_add_numbers

# Summary
echo "========================================" >&2
echo "Tests run: $TESTS_RUN" >&2
echo "Passed: $TESTS_PASSED" >&2
echo "Failed: $TESTS_FAILED" >&2

[[ $TESTS_FAILED -eq 0 ]]
```

## ShellCheck Integration

```bash
#!/usr/bin/env bash
set -euo pipefail

# Validate script with ShellCheck
validate_script() {
    local script="$1"

    if ! command -v shellcheck &> /dev/null; then
        echo "ShellCheck not installed" >&2
        return 1
    fi

    echo "Running ShellCheck on $script..." >&2
    if shellcheck --severity=warning "$script"; then
        echo "✓ ShellCheck passed" >&2
        return 0
    else
        echo "✗ ShellCheck failed" >&2
        return 1
    fi
}

# Usage
validate_script myscript.sh
```

## Resources

- [Bash Hackers Wiki - Debugging](https://wiki.bash-hackers.org/scripting/debuggingtips)
- [ShellCheck](https://www.shellcheck.net/)
- [BATS Testing Framework](https://github.com/bats-core/bats-core)
- [Bash Reference Manual - Debugging](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)

---

**Effective debugging requires systematic approaches, comprehensive logging, and proper tooling. Master these techniques for production-ready bash scripts in 2025.**
