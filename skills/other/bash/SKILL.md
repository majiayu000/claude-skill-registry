---
name: scripting-bash
description: Master defensive Bash scripting for production automation, CI/CD pipelines, and system utilities. Expert in safe, portable, and testable shell scripts with POSIX compliance, modern Bash 5.x features, and comprehensive error handling. Use when writing shell scripts, bash automation, CI/CD scripts, system utilities, or mentions "bash", "shell script", "automation", "defensive programming", or needs production-grade shell code.
---

# Bash Scripting Mastery

You are an expert in defensive Bash scripting for production environments. Create safe, portable, and testable shell scripts following modern best practices.

## 10 Focus Areas

1. **Defensive Programming** - Strict error handling with proper exit codes and traps
2. **POSIX Compliance** - Cross-platform portability (Linux, macOS, BSD variants)
3. **Safe Argument Parsing** - Robust input validation and `getopts` usage
4. **Robust File Operations** - Temporary resource management with cleanup traps
5. **Process Orchestration** - Pipeline safety and subprocess management
6. **Production Logging** - Structured logging with timestamps and verbosity levels
7. **Comprehensive Testing** - bats-core/shellspec with TAP output
8. **Static Analysis** - ShellCheck compliance and shfmt formatting
9. **Modern Bash 5.x** - Latest features with version detection and fallbacks
10. **CI/CD Integration** - Automation workflows and security scanning

> **Progressive Disclosure**: For deep dives, see [references/](.) directory.

## Essential Defensive Patterns

### 1. Strict Mode Template

```bash
#!/usr/bin/env bash
set -Eeuo pipefail  # Exit on error, undefined vars, pipe failures
shopt -s inherit_errexit  # Bash 4.4+ better error propagation
IFS=$'\n\t'  # Prevent unwanted word splitting on spaces

# Error trap with context
trap 'echo "Error at line $LINENO: exit $?" >&2' ERR

# Cleanup trap for temporary resources
cleanup() {
  [[ -n "${tmpdir:-}" ]] && rm -rf "$tmpdir"
}
trap cleanup EXIT
```

### 2. Safe Variable Handling

```bash
# Quote all variable expansions
cp "$source_file" "$dest_dir"

# Required variables with error messages
: "${REQUIRED_VAR:?not set or empty}"

# Safe iteration over files (NEVER use for f in $(ls))
find . -name "*.txt" -print0 | while IFS= read -r -d '' file; do
  echo "Processing: $file"
done

# Binary-safe array population
readarray -d '' files < <(find . -print0)
```

### 3. Robust Argument Parsing

```bash
usage() {
  cat <<EOF
Usage: ${0##*/} [OPTIONS] <required-arg>

OPTIONS:
  -h, --help     Show this help message
  -v, --verbose  Enable verbose output
  -n, --dry-run  Dry run mode
EOF
}

# Parse arguments
while getopts "hvn-:" opt; do
  case "$opt" in
    h) usage; exit 0 ;;
    v) VERBOSE=1 ;;
    n) DRY_RUN=1 ;;
    -) # Long options
      case "$OPTARG" in
        help) usage; exit 0 ;;
        verbose) VERBOSE=1 ;;
        dry-run) DRY_RUN=1 ;;
        *) echo "Unknown option: --$OPTARG" >&2; exit 1 ;;
      esac
      ;;
    *) usage >&2; exit 1 ;;
  esac
done
shift $((OPTIND - 1))
```

### 4. Safe Temporary Resources

```bash
# Create temp directory with cleanup
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

# Safe temp file creation
tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT
```

### 5. Structured Logging

```bash
readonly SCRIPT_NAME="${0##*/}"
readonly LOG_LEVELS=(DEBUG INFO WARN ERROR)

log() {
  local level="$1"; shift
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$timestamp] [$level] $SCRIPT_NAME: $*" >&2
}

log_info() { log INFO "$@"; }
log_error() { log ERROR "$@"; }
log_debug() { [[ ${VERBOSE:-0} -eq 1 ]] && log DEBUG "$@" || true; }
```

### 6. Version Detection & Modern Features

```bash
# Check Bash version before using modern features
if (( BASH_VERSINFO[0] >= 5 )); then
  # Bash 5.x features available
  declare -A config=([host]="localhost" [port]="8080")
  echo "${config[@]@K}"  # Assignment format (Bash 5.x)
else
  echo "Warning: Bash 5.x features not available" >&2
fi

# Check for required commands
for cmd in jq curl; do
  command -v "$cmd" &>/dev/null || {
    echo "Error: Required command '$cmd' not found" >&2
    exit 1
  }
done
```

### 7. Safe Command Execution

```bash
# Separate options from arguments with --
rm -rf -- "$user_input"

# Timeout for external commands
timeout 30s curl -fsSL "$url" || {
  echo "Error: curl timed out" >&2
  exit 1
}

# Capture both stdout and stderr
output=$(command 2>&1) || {
  echo "Error: command failed with output: $output" >&2
  exit 1
}
```

### 8. Platform Portability

```bash
# Detect platform
case "$(uname -s)" in
  Linux*)   PLATFORM="linux" ;;
  Darwin*)  PLATFORM="macos" ;;
  *)        PLATFORM="unknown" ;;
esac

# Handle GNU vs BSD tool differences
if [[ $PLATFORM == "macos" ]]; then
  sed -i '' 's/old/new/' file  # BSD sed
else
  sed -i 's/old/new/' file     # GNU sed
fi
```

### 9. Script Directory Detection

```bash
# Robust script directory detection (handles symlinks)
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly SCRIPT_DIR
```

### 10. Best Practices Quick Reference

- **Quote everything**: `"$var"` not `$var`
- **Use `[[ ]]`**: Bash conditionals, fall back to `[ ]` for POSIX
- **Prefer arrays**: Over unsafe patterns like `for f in $(ls)`
- **Use `printf`**: Not `echo` for predictable output
- **Command substitution**: `$()` not backticks
- **Arithmetic**: `$(( ))` not `expr`
- **Built-ins**: Use Bash built-ins over external commands
- **End options**: Use `--` before arguments
- **Validate input**: Check existence, permissions, format
- **Cleanup traps**: Always cleanup temporary resources

## Output Deliverables

When creating Bash scripts, provide:

1. **Production-ready script** with:
   - Strict mode enabled (`set -Eeuo pipefail`)
   - Comprehensive error handling and cleanup traps
   - Clear usage message (`--help`)
   - Proper argument parsing with `getopts`
   - Structured logging with log levels

2. **Test suite** (bats-core or shellspec):
   - Edge cases and error conditions
   - Mock external dependencies
   - TAP output format

3. **CI/CD configuration**:
   - ShellCheck static analysis
   - shfmt formatting validation
   - Automated testing with Bats

4. **Documentation**:
   - Usage examples in `--help`
   - Required dependencies and versions
   - Exit codes and error messages

5. **Static analysis config**:
   - `.shellcheckrc` with appropriate suppressions
   - `.editorconfig` for consistent formatting

## Tools & Commands

### Essential Tools
- **ShellCheck**: `shellcheck --enable=all script.sh`
- **shfmt**: `shfmt -i 2 -ci -bn -sr -kp script.sh`
- **bats-core**: `bats test/script.bats`

### Quick Validation
```bash
# Run full validation
shellcheck *.sh && shfmt -d *.sh && bats test/
```

## Reference Documentation

For detailed guidance on specific topics:

- **[Modern Bash 5.x Features](references/MODERN_BASH.md)** - Version-specific features, transformations, and compatibility
- **[Testing Frameworks](references/TESTING.md)** - bats-core, shellspec, test patterns, mocking
- **[CI/CD Integration](references/CICD.md)** - GitHub Actions, pre-commit hooks, matrix testing
- **[Security & Hardening](references/SECURITY.md)** - SAST, secrets detection, input sanitization, audit logging

## Common Pitfalls to Avoid

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

Quick list:
- ❌ `for f in $(ls ...)` → ✅ `find -print0 | while IFS= read -r -d '' f`
- ❌ Unquoted variables → ✅ Always quote: `"$var"`
- ❌ Missing cleanup traps → ✅ `trap cleanup EXIT`
- ❌ Using `echo` for data → ✅ Use `printf` instead
- ❌ Ignoring exit codes → ✅ Check all critical operations
- ❌ Unsafe array population → ✅ Use `readarray`/`mapfile`

## Examples

See [EXAMPLES.md](EXAMPLES.md) for complete script templates and usage patterns.
