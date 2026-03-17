---
name: bash-master
description: "Expert bash/shell scripting system across ALL platforms. PROACTIVELY activate for: (1) ANY bash/shell script task, (2) System automation, (3) DevOps/CI/CD scripts, (4) Build/deployment automation, (5) Script review/debugging, (6) Converting commands to scripts. Provides: Google Shell Style Guide compliance, ShellCheck validation, cross-platform compatibility (Linux/macOS/Windows/containers), POSIX compliance, security hardening, error handling, performance optimization, testing with BATS, and production-ready patterns. Ensures professional-grade, secure, portable scripts every time."
---

# Bash Scripting Mastery

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

Comprehensive guide for writing professional, portable, and maintainable bash scripts across all platforms.

---

## TL;DR QUICK REFERENCE

**Essential Checklist for Every Bash Script:**
```bash
#!/usr/bin/env bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures
IFS=$'\n\t'        # Safe word splitting

# Use: shellcheck your_script.sh before deployment
# Test on target platform(s) before production
```

**Platform Compatibility Quick Check:**
```bash
# Linux/macOS: ✓ Full bash features
# Git Bash (Windows): ✓ Most features, ✗ Some system calls
# Containers: ✓ Depends on base image
# POSIX mode: Use /bin/sh and avoid bashisms
```

---

## Overview

This skill provides expert bash/shell scripting knowledge for ANY scripting task, ensuring professional-grade quality across all platforms.

**MUST use this skill for:**
- ✅ ANY bash/shell script creation or modification
- ✅ System automation and tooling
- ✅ DevOps/CI/CD pipeline scripts
- ✅ Build and deployment automation
- ✅ Script review, debugging, or optimization
- ✅ Converting manual commands to automated scripts
- ✅ Cross-platform script compatibility

**What this skill provides:**
- **Google Shell Style Guide compliance** - Industry-standard formatting and patterns
- **ShellCheck validation** - Automatic detection of common issues
- **Cross-platform compatibility** - Linux, macOS, Windows (Git Bash/WSL), containers
- **POSIX compliance** - Portable scripts that work everywhere
- **Security hardening** - Input validation, injection prevention, privilege management
- **Error handling** - Robust `set -euo pipefail`, trap handlers, exit codes
- **Performance optimization** - Efficient patterns, avoiding anti-patterns
- **Testing with BATS** - Unit testing, integration testing, CI/CD integration
- **Debugging techniques** - Logging, troubleshooting, profiling
- **Production-ready patterns** - Templates and best practices for real-world use

**This skill activates automatically for:**
- Any mention of "bash", "shell", "script" in task
- System automation requests
- DevOps/CI/CD tasks
- Build/deployment automation
- Command line tool creation

---

## Core Principles

### 1. Safety First

**ALWAYS start scripts with safety settings:**

```bash
#!/usr/bin/env bash

# Fail fast and loud
set -e          # Exit on any error
set -u          # Exit on undefined variable
set -o pipefail # Exit on pipe failure
set -E          # ERR trap inherited by functions

# Optionally:
# set -x        # Debug mode (print commands before execution)
# set -C        # Prevent file overwrites with redirection

# Safe word splitting
IFS=$'\n\t'

# Script metadata
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
```

**Why this matters:**
- `set -e`: Prevents cascading failures
- `set -u`: Catches typos in variable names
- `set -o pipefail`: Catches failures in the middle of pipes
- `IFS=$'\n\t'`: Prevents word splitting on spaces (security issue)

### 2. POSIX Compatibility vs Bash Features

**Know when to use which:**

```bash
# POSIX-compliant (portable across shells)
#!/bin/sh
# Use: [ ] tests, no arrays, no [[ ]], no <(process substitution)

# Bash-specific (modern features, clearer syntax)
#!/usr/bin/env bash
# Use: [[ ]], arrays, associative arrays, <(), process substitution
```

**Decision matrix:**
- Need to run on any UNIX system → Use `#!/bin/sh` and POSIX only
- Control the environment (modern Linux/macOS) → Use `#!/usr/bin/env bash`
- Need advanced features (arrays, regex) → Use `#!/usr/bin/env bash`

### 3. Quoting Rules (Critical)

```bash
# ALWAYS quote variables to prevent word splitting and globbing
bad_cmd=$file_path          # ✗ WRONG - word splitting
good_cmd="$file_path"       # ✓ CORRECT

# Arrays: Quote expansion
files=("file 1.txt" "file 2.txt")
process "${files[@]}"       # ✓ CORRECT - each element quoted
process "${files[*]}"       # ✗ WRONG - all elements as one string

# Command substitution: Quote the result
result="$(command)"         # ✓ CORRECT
result=$(command)           # ✗ WRONG (unless you want word splitting)

# Exception: When you WANT word splitting
# shellcheck disable=SC2086
flags="-v -x -z"
command $flags              # Intentional word splitting
```

### 4. Use ShellCheck

**ALWAYS run ShellCheck before deployment:**

```bash
# Install
# Ubuntu/Debian: apt-get install shellcheck
# macOS: brew install shellcheck
# Windows: scoop install shellcheck

# Usage
shellcheck your_script.sh
shellcheck -x your_script.sh  # Follow source statements

# In CI/CD
find . -name "*.sh" -exec shellcheck {} +
```

**ShellCheck catches:**
- Quoting issues
- Bashisms in POSIX scripts
- Common logic errors
- Security vulnerabilities
- Performance anti-patterns

---

## Platform-Specific Considerations


### Windows (Git Bash) Path Conversion - CRITICAL

**ESSENTIAL KNOWLEDGE:** Git Bash/MINGW automatically converts Unix-style paths to Windows paths. This is the most common source of cross-platform scripting errors on Windows.

**Complete Guide:** See `references/windows-git-bash-paths.md` for comprehensive documentation.

**Quick Reference:**

```bash
# Automatic conversion happens for:
/foo → C:/Program Files/Git/usr/foo
--dir=/tmp → --dir=C:/msys64/tmp

# Disable conversion when needed
MSYS_NO_PATHCONV=1 command /path/that/should/not/convert

# Manual conversion with cygpath
unix_path=$(cygpath -u "C:\Windows\System32")  # Windows to Unix
win_path=$(cygpath -w "/c/Users/username")        # Unix to Windows

# Shell detection (fastest method)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "mingw"* ]]; then
    echo "Git Bash detected"
    # Use path conversion
fi

# Or check $MSYSTEM variable (Git Bash/MSYS2 specific)
case "${MSYSTEM:-}" in
    MINGW64|MINGW32|MSYS)
        echo "MSYS2/Git Bash environment: $MSYSTEM"
        ;;
esac
```

**Common Issues:**

```bash
# Problem: Flags converted to paths
command /e /s  # /e becomes C:/Program Files/Git/e

# Solution: Use double slashes or dashes
command //e //s  # OR: command -e -s

# Problem: Spaces in paths
cd C:\Program Files\Git  # Fails

# Solution: Quote paths
cd "C:\Program Files\Git"  # OR: cd /c/Program\ Files/Git
```


### Linux

**Primary target for most bash scripts:**

```bash
# Linux-specific features available
/proc filesystem
systemd integration
Linux-specific commands (apt, yum, systemctl)

# Check for Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux-specific code
fi
```

### macOS

**BSD-based utilities (different from GNU):**

```bash
# macOS differences
sed -i ''                    # macOS requires empty string
sed -i                       # Linux doesn't need it

# Use ggrep, gsed, etc. for GNU versions
if command -v gsed &> /dev/null; then
    SED=gsed
else
    SED=sed
fi

# Check for macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS-specific code
fi
```

### Windows (Git Bash / WSL)

**Git Bash limitations:**

```bash
# Available in Git Bash:
- Most core utils
- File operations
- Process management (limited)

# NOT available:
- systemd
- Some signals (SIGHUP behavior differs)
- /proc filesystem
- Native Windows path handling issues

# Path handling
# Git Bash uses Unix paths: /c/Users/...
# Convert if needed:
winpath=$(cygpath -w "$unixpath")  # Unix → Windows
unixpath=$(cygpath -u "$winpath")  # Windows → Unix

# Check for Git Bash
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Git Bash / Cygwin code
fi
```

**WSL (Windows Subsystem for Linux):**
```bash
# WSL is essentially Linux, but:
# - Can access Windows filesystem at /mnt/c/
# - Some syscalls behave differently
# - Network configuration differs

# Check for WSL
if grep -qi microsoft /proc/version 2>/dev/null; then
    # WSL-specific code
fi
```

### Containers (Docker/Kubernetes)

**Container-aware scripting:**

```bash
# Minimal base images may not have bash
# Use #!/bin/sh or install bash explicitly

# Container detection
if [ -f /.dockerenv ] || grep -q docker /proc/1/cgroup 2>/dev/null; then
    # Running in Docker
fi

# Kubernetes detection
if [ -n "$KUBERNETES_SERVICE_HOST" ]; then
    # Running in Kubernetes
fi

# Best practices:
# - Minimize dependencies
# - Use absolute paths or PATH
# - Don't assume user/group existence
# - Handle signals properly (PID 1 issues)
```

### Cross-Platform Template

```bash
#!/usr/bin/env bash
set -euo pipefail

# Detect platform
detect_platform() {
    case "$OSTYPE" in
        linux-gnu*)   echo "linux" ;;
        darwin*)      echo "macos" ;;
        msys*|cygwin*) echo "windows" ;;
        *)            echo "unknown" ;;
    esac
}

PLATFORM=$(detect_platform)

# Platform-specific paths
case "$PLATFORM" in
    linux)
        SED=sed
        ;;
    macos)
        SED=$(command -v gsed || echo sed)
        ;;
    windows)
        # Git Bash specifics
        ;;
esac
```

---

## Best Practices

### Function Design

```bash
# Good function structure
function_name() {
    # 1. Local variables first
    local arg1="$1"
    local arg2="${2:-default_value}"
    local result=""

    # 2. Input validation
    if [[ -z "$arg1" ]]; then
        echo "Error: arg1 is required" >&2
        return 1
    fi

    # 3. Main logic
    result=$(some_operation "$arg1" "$arg2")

    # 4. Output/return
    echo "$result"
    return 0
}

# Use functions, not scripts-in-scripts
# Benefits: testability, reusability, namespacing
```

### Variable Naming

```bash
# Constants: UPPER_CASE
readonly MAX_RETRIES=3
readonly CONFIG_FILE="/etc/app/config.conf"

# Global variables: UPPER_CASE or lower_case (be consistent)
GLOBAL_STATE="initialized"

# Local variables: lower_case
local user_name="john"
local file_count=0

# Environment variables: UPPER_CASE (by convention)
export DATABASE_URL="postgres://..."

# Readonly when possible
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```

### Error Handling

```bash
# Method 1: Check exit codes explicitly
if ! command_that_might_fail; then
    echo "Error: Command failed" >&2
    return 1
fi

# Method 2: Use || for alternative actions
command_that_might_fail || {
    echo "Error: Command failed" >&2
    return 1
}

# Method 3: Trap for cleanup
cleanup() {
    local exit_code=$?
    # Cleanup operations
    rm -f "$TEMP_FILE"
    exit "$exit_code"
}
trap cleanup EXIT

# Method 4: Custom error handler
error_exit() {
    local message="$1"
    local code="${2:-1}"
    echo "Error: $message" >&2
    exit "$code"
}

# Usage
[[ -f "$config_file" ]] || error_exit "Config file not found: $config_file"
```

### Input Validation

```bash
validate_input() {
    local input="$1"

    # Check if empty
    if [[ -z "$input" ]]; then
        echo "Error: Input cannot be empty" >&2
        return 1
    fi

    # Check format (example: alphanumeric only)
    if [[ ! "$input" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        echo "Error: Input contains invalid characters" >&2
        return 1
    fi

    # Check length
    if [[ ${#input} -gt 255 ]]; then
        echo "Error: Input too long (max 255 characters)" >&2
        return 1
    fi

    return 0
}

# Validate before use
read -r user_input
if validate_input "$user_input"; then
    process "$user_input"
fi
```

### Argument Parsing

```bash
# Simple argument parsing
usage() {
    cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS] <command>

Options:
    -h, --help          Show this help
    -v, --verbose       Verbose output
    -f, --file FILE     Input file
    -o, --output DIR    Output directory

Commands:
    build               Build the project
    test                Run tests
EOF
}

main() {
    local verbose=false
    local input_file=""
    local output_dir="."
    local command=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage
                exit 0
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            -f|--file)
                input_file="$2"
                shift 2
                ;;
            -o|--output)
                output_dir="$2"
                shift 2
                ;;
            -*)
                echo "Error: Unknown option: $1" >&2
                usage >&2
                exit 1
                ;;
            *)
                command="$1"
                shift
                break
                ;;
        esac
    done

    # Validate required arguments
    if [[ -z "$command" ]]; then
        echo "Error: Command is required" >&2
        usage >&2
        exit 1
    fi

    # Execute command
    case "$command" in
        build) do_build ;;
        test)  do_test ;;
        *)
            echo "Error: Unknown command: $command" >&2
            usage >&2
            exit 1
            ;;
    esac
}

main "$@"
```

### Logging

```bash
# Logging levels
readonly LOG_LEVEL_DEBUG=0
readonly LOG_LEVEL_INFO=1
readonly LOG_LEVEL_WARN=2
readonly LOG_LEVEL_ERROR=3

# Current log level
LOG_LEVEL=${LOG_LEVEL:-$LOG_LEVEL_INFO}

log_debug() { [[ $LOG_LEVEL -le $LOG_LEVEL_DEBUG ]] && echo "[DEBUG] $*" >&2; }
log_info()  { [[ $LOG_LEVEL -le $LOG_LEVEL_INFO  ]] && echo "[INFO]  $*" >&2; }
log_warn()  { [[ $LOG_LEVEL -le $LOG_LEVEL_WARN  ]] && echo "[WARN]  $*" >&2; }
log_error() { [[ $LOG_LEVEL -le $LOG_LEVEL_ERROR ]] && echo "[ERROR] $*" >&2; }

# With timestamps
log_with_timestamp() {
    local level="$1"
    shift
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $*" >&2
}

# Usage
log_info "Starting process"
log_error "Failed to connect to database"
```

---

## Security Best Practices

### Command Injection Prevention

```bash
# NEVER use eval with user input
# ✗ WRONG - DANGEROUS
eval "$user_input"

# NEVER use dynamic variable names from user input
# ✗ WRONG - DANGEROUS
eval "var_$user_input=value"

# NEVER concatenate user input into commands
# ✗ WRONG - DANGEROUS
grep "$user_pattern" file.txt  # If pattern contains -e flag, injection possible

# ✓ CORRECT - Use arrays
grep_args=("$user_pattern" "file.txt")
grep "${grep_args[@]}"

# ✓ CORRECT - Use -- to separate options from arguments
grep -- "$user_pattern" file.txt
```

### Path Traversal Prevention

```bash
# Sanitize file paths
sanitize_path() {
    local path="$1"

    # Remove .. components
    path="${path//..\/}"
    path="${path//\/..\//}"

    # Remove leading /
    path="${path#/}"

    echo "$path"
}

# Validate path is within allowed directory
is_safe_path() {
    local file_path="$1"
    local base_dir="$2"

    # Resolve to absolute path
    local real_path
    real_path=$(readlink -f "$file_path" 2>/dev/null) || return 1
    local real_base
    real_base=$(readlink -f "$base_dir" 2>/dev/null) || return 1

    # Check if path starts with base directory
    [[ "$real_path" == "$real_base"/* ]]
}

# Usage
if is_safe_path "$user_file" "/var/app/data"; then
    process_file "$user_file"
else
    echo "Error: Invalid file path" >&2
    exit 1
fi
```

### Privilege Management

```bash
# Check if running as root
if [[ $EUID -eq 0 ]]; then
    echo "Error: Do not run this script as root" >&2
    exit 1
fi

# Drop privileges if needed
drop_privileges() {
    local user="$1"

    if [[ $EUID -eq 0 ]]; then
        exec sudo -u "$user" "$0" "$@"
    fi
}

# Run specific command with elevated privileges
run_as_root() {
    if [[ $EUID -ne 0 ]]; then
        sudo "$@"
    else
        "$@"
    fi
}
```

### Temporary File Handling

```bash
# Create secure temporary files
readonly TEMP_DIR=$(mktemp -d)
readonly TEMP_FILE=$(mktemp)

# Cleanup on exit
cleanup() {
    rm -rf "$TEMP_DIR"
    rm -f "$TEMP_FILE"
}
trap cleanup EXIT

# Secure temporary file (only readable by owner)
secure_temp=$(mktemp)
chmod 600 "$secure_temp"
```

---

## Performance Optimization

### Avoid Unnecessary Subshells

```bash
# ✗ SLOW - Creates subshell for each iteration
while IFS= read -r line; do
    count=$(echo "$count + 1" | bc)
done < file.txt

# ✓ FAST - Arithmetic in bash
count=0
while IFS= read -r line; do
    ((count++))
done < file.txt
```

### Use Bash Built-ins

```bash
# ✗ SLOW - External commands
dirname=$(dirname "$path")
basename=$(basename "$path")

# ✓ FAST - Parameter expansion
dirname="${path%/*}"
basename="${path##*/}"

# ✗ SLOW - grep for simple checks
if echo "$string" | grep -q "pattern"; then

# ✓ FAST - Bash regex
if [[ "$string" =~ pattern ]]; then

# ✗ SLOW - awk for simple extraction
field=$(echo "$line" | awk '{print $3}')

# ✓ FAST - Read into array
read -ra fields <<< "$line"
field="${fields[2]}"
```

### Process Substitution vs Pipes

```bash
# When you need to read multiple commands' output
# ✓ GOOD - Process substitution
while IFS= read -r line1 <&3 && IFS= read -r line2 <&4; do
    echo "$line1 - $line2"
done 3< <(command1) 4< <(command2)

# Parallel processing
command1 &
command2 &
wait  # Wait for all background jobs
```

### Array Operations

```bash
# ✓ FAST - Native array operations
files=(*.txt)
echo "Found ${#files[@]} files"

# ✗ SLOW - Parsing ls output
count=$(ls -1 *.txt | wc -l)

# ✓ FAST - Array filtering
filtered=()
for item in "${array[@]}"; do
    [[ "$item" =~ ^[0-9]+$ ]] && filtered+=("$item")
done

# ✓ FAST - Array joining
IFS=,
joined="${array[*]}"
IFS=$'\n\t'
```

---

## Testing

### Unit Testing with BATS

```bash
# Install BATS
# git clone https://github.com/bats-core/bats-core.git
# cd bats-core && ./install.sh /usr/local

# test/script.bats
#!/usr/bin/env bats

# Load script to test
load '../script.sh'

@test "function returns correct value" {
    result=$(my_function "input")
    [ "$result" = "expected" ]
}

@test "function handles empty input" {
    run my_function ""
    [ "$status" -eq 1 ]
    [ "${lines[0]}" = "Error: Input cannot be empty" ]
}

@test "function validates input format" {
    run my_function "invalid@input"
    [ "$status" -eq 1 ]
}

# Run tests
# bats test/script.bats
```

### Integration Testing

```bash
# integration_test.sh
#!/usr/bin/env bash
set -euo pipefail

# Setup
setup() {
    export TEST_DIR=$(mktemp -d)
    export TEST_FILE="$TEST_DIR/test.txt"
}

# Teardown
teardown() {
    rm -rf "$TEST_DIR"
}

# Test case
test_file_creation() {
    ./script.sh create "$TEST_FILE"

    if [[ ! -f "$TEST_FILE" ]]; then
        echo "FAIL: File was not created"
        return 1
    fi

    echo "PASS: File creation works"
    return 0
}

# Run tests
main() {
    setup
    trap teardown EXIT

    test_file_creation || exit 1

    echo "All tests passed"
}

main
```

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install shellcheck
        run: sudo apt-get install -y shellcheck

      - name: Run shellcheck
        run: find . -name "*.sh" -exec shellcheck {} +

      - name: Install bats
        run: |
          git clone https://github.com/bats-core/bats-core.git
          cd bats-core
          sudo ./install.sh /usr/local

      - name: Run tests
        run: bats test/
```

---

## Debugging Techniques

### Debug Mode

```bash
# Method 1: set -x (print commands)
set -x
command1
command2
set +x  # Turn off

# Method 2: PS4 for better output
export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
set -x

# Method 3: Conditional debugging
DEBUG=${DEBUG:-false}
debug() {
    if [[ "$DEBUG" == "true" ]]; then
        echo "[DEBUG] $*" >&2
    fi
}

# Usage: DEBUG=true ./script.sh
```

### Tracing and Profiling

```bash
# Trace function calls
trace() {
    echo "[TRACE] Function: ${FUNCNAME[1]}, Args: $*" >&2
}

my_function() {
    trace "$@"
    # Function logic
}

# Execution time profiling
profile() {
    local start=$(date +%s%N)
    "$@"
    local end=$(date +%s%N)
    local duration=$(( (end - start) / 1000000 ))
    echo "[PROFILE] Command '$*' took ${duration}ms" >&2
}

# Usage
profile slow_command arg1 arg2
```

### Common Issues and Solutions

```bash
# Issue: Script works in bash but not in sh
# Solution: Check for bashisms
checkbashisms script.sh

# Issue: Works locally but not on server
# Solution: Check PATH and environment
env
echo "$PATH"

# Issue: Whitespace in filenames breaking script
# Solution: Always quote variables
for file in *.txt; do
    process "$file"  # Not: process $file
done

# Issue: Script behaves differently in cron
# Solution: Set PATH explicitly
PATH=/usr/local/bin:/usr/bin:/bin
export PATH
```

---

## Advanced Patterns

### Configuration File Parsing

```bash
# Simple key=value config
load_config() {
    local config_file="$1"

    if [[ ! -f "$config_file" ]]; then
        echo "Error: Config file not found: $config_file" >&2
        return 1
    fi

    # Source config (dangerous if not trusted)
    # shellcheck source=/dev/null
    source "$config_file"
}

# Safe config parsing (no code execution)
read_config() {
    local config_file="$1"

    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^[[:space:]]*# ]] && continue
        [[ -z "$key" ]] && continue

        # Trim whitespace
        key=$(echo "$key" | tr -d ' ')
        value=$(echo "$value" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

        # Export variable
        declare -g "$key=$value"
    done < "$config_file"
}
```

### Parallel Processing

```bash
# Simple background jobs
process_files_parallel() {
    local max_jobs=4
    local job_count=0

    for file in *.txt; do
        # Start background job
        process_file "$file" &

        # Limit concurrent jobs
        ((job_count++))
        if [[ $job_count -ge $max_jobs ]]; then
            wait -n  # Wait for any job to finish
            ((job_count--))
        fi
    done

    # Wait for remaining jobs
    wait
}

# GNU Parallel (if available)
parallel_with_gnu() {
    parallel -j 4 process_file ::: *.txt
}
```

### Signal Handling

```bash
# Graceful shutdown
shutdown_requested=false

handle_sigterm() {
    echo "Received SIGTERM, shutting down gracefully..." >&2
    shutdown_requested=true
}

trap handle_sigterm SIGTERM SIGINT

main_loop() {
    while [[ "$shutdown_requested" == "false" ]]; do
        # Do work
        sleep 1
    done

    echo "Shutdown complete" >&2
}

main_loop
```

### Retries with Exponential Backoff

```bash
retry_with_backoff() {
    local max_attempts=5
    local timeout=1
    local attempt=1
    local exitCode=0

    while [[ $attempt -le $max_attempts ]]; do
        if "$@"; then
            return 0
        else
            exitCode=$?
        fi

        echo "Attempt $attempt failed! Retrying in $timeout seconds..." >&2
        sleep "$timeout"
        attempt=$((attempt + 1))
        timeout=$((timeout * 2))
    done

    echo "Command failed after $max_attempts attempts!" >&2
    return "$exitCode"
}

# Usage
retry_with_backoff curl -f https://api.example.com/health
```

---

## Resources for Additional Information

### Official Documentation

1. **Bash Reference Manual**
   - URL: https://www.gnu.org/software/bash/manual/
   - The authoritative source for bash features and behavior

2. **POSIX Shell Command Language**
   - URL: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html
   - For writing portable scripts

### Style Guides

1. **Google Shell Style Guide**
   - URL: https://google.github.io/styleguide/shellguide.html
   - Industry-standard practices from Google

2. **Defensive Bash Programming**
   - URL: https://kfirlavi.herokuapp.com/blog/2012/11/14/defensive-bash-programming
   - Best practices for robust scripts

### Tools

1. **ShellCheck**
   - URL: https://www.shellcheck.net/
   - GitHub: https://github.com/koalaman/shellcheck
   - Static analysis tool for shell scripts

2. **BATS (Bash Automated Testing System)**
   - GitHub: https://github.com/bats-core/bats-core
   - Unit testing framework for bash

3. **shfmt**
   - GitHub: https://github.com/mvdan/sh
   - Shell script formatter

### Learning Resources

1. **Bash Academy**
   - URL: https://www.bash.academy/
   - Comprehensive bash learning resource

2. **Bash Guide for Beginners**
   - URL: https://tldp.org/LDP/Bash-Beginners-Guide/html/
   - From The Linux Documentation Project

3. **Advanced Bash-Scripting Guide**
   - URL: https://tldp.org/LDP/abs/html/
   - In-depth coverage of advanced topics

4. **Bash Pitfalls**
   - URL: https://mywiki.wooledge.org/BashPitfalls
   - Common mistakes and how to avoid them

5. **explainshell.com**
   - URL: https://explainshell.com/
   - Interactive tool to explain shell commands

### Platform-Specific Resources

1. **GNU Coreutils Manual**
   - URL: https://www.gnu.org/software/coreutils/manual/
   - For Linux-specific commands

2. **FreeBSD Manual Pages**
   - URL: https://www.freebsd.org/cgi/man.cgi
   - For macOS (BSD-based) differences

3. **Git for Windows**
   - URL: https://gitforwindows.org/
   - Git Bash documentation and issues

4. **WSL Documentation**
   - URL: https://docs.microsoft.com/en-us/windows/wsl/
   - Windows Subsystem for Linux specifics

### Community Resources

1. **Stack Overflow - Bash Tag**
   - URL: https://stackoverflow.com/questions/tagged/bash
   - Community Q&A

2. **Unix & Linux Stack Exchange**
   - URL: https://unix.stackexchange.com/
   - Shell scripting expertise

3. **Reddit - r/bash**
   - URL: https://www.reddit.com/r/bash/
   - Community discussions

### Quick Reference

1. **Bash Cheat Sheet**
   - URL: https://devhints.io/bash
   - Quick syntax reference

2. **ShellCheck Wiki**
   - URL: https://www.shellcheck.net/wiki/
   - Explanations of ShellCheck warnings

---

## Reference Files

For deeper coverage of specific topics, see the reference files:

- **[references/platform_specifics.md](references/platform_specifics.md)** - Detailed platform differences and workarounds
- **[references/best_practices.md](references/best_practices.md)** - Comprehensive industry standards and guidelines
- **[references/patterns_antipatterns.md](references/patterns_antipatterns.md)** - Common patterns and pitfalls with solutions

---

## When to Use This Skill

**Always activate for:**
- Writing new bash scripts
- Reviewing/refactoring existing scripts
- Debugging shell script issues
- Cross-platform shell scripting
- DevOps automation tasks
- CI/CD pipeline scripts
- System administration automation

**Key indicators:**
- User mentions bash, shell, or script
- Task involves automation
- Platform compatibility is a concern
- Security or robustness is important
- Performance optimization needed

---

## Success Criteria

A bash script using this skill should:

1. ✓ Pass ShellCheck with no warnings
2. ✓ Include proper error handling (set -euo pipefail)
3. ✓ Quote all variable expansions
4. ✓ Include usage/help text
5. ✓ Use functions for reusable logic
6. ✓ Include appropriate comments
7. ✓ Handle edge cases (empty input, missing files, etc.)
8. ✓ Work across target platforms
9. ✓ Follow consistent style (Google Shell Style Guide)
10. ✓ Include cleanup (trap EXIT)

**Quality checklist:**
```bash
# Run before deployment
shellcheck script.sh              # No errors or warnings
bash -n script.sh                 # Syntax check
bats test/script.bats             # Unit tests pass
./script.sh --help                # Usage text displays
DEBUG=true ./script.sh            # Debug mode works
```

---

## Troubleshooting

### Script fails on different platform
1. Check for bashisms: `checkbashisms script.sh`
2. Verify commands exist: `command -v tool_name`
3. Test command flags: `sed --version` (GNU) vs `sed` (BSD)

### ShellCheck warnings
1. Read the explanation: `shellcheck -W SC2086`
2. Fix the issue (don't just disable)
3. Only disable with justification: `# shellcheck disable=SC2086 reason: intentional word splitting`

### Script works interactively but fails in cron
1. Set PATH explicitly
2. Use absolute paths
3. Redirect output for debugging: `./script.sh >> /tmp/cron.log 2>&1`

### Performance issues
1. Profile with `time command`
2. Enable tracing: `set -x`
3. Avoid unnecessary subshells and external commands
4. Use bash built-ins where possible

---

This skill provides comprehensive bash scripting knowledge. Combined with the reference files, you have access to industry-standard practices and platform-specific guidance for any bash scripting task.
