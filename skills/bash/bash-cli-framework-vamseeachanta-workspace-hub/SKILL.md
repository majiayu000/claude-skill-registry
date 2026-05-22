---
name: bash-cli-framework
version: 1.0.0
description: Universal bash CLI patterns for colors, logging, headers, and error handling
author: workspace-hub
category: bash
tags: [bash, cli, colors, logging, framework, scripting]
platforms: [linux, macos]
---

# Bash CLI Framework

A comprehensive framework for building consistent, professional bash CLI tools with standardized colors, logging, headers, and error handling patterns extracted from workspace-hub scripts.

## When to Use This Skill

✅ **Use when:**
- Building new bash CLI tools or scripts
- Adding consistent output formatting to existing scripts
- Need standardized error handling and logging
- Creating user-friendly interactive scripts
- Building tools that will be used across multiple repositories

❌ **Avoid when:**
- Simple one-liner scripts
- Scripts that don't produce user-facing output
- When Python/Node CLI frameworks are more appropriate

## Core Capabilities

### 1. Color Definitions

Standard ANSI color codes for consistent terminal output:

```bash
#!/bin/bash
# ABOUTME: Standard color definitions for CLI output
# ABOUTME: Use these consistently across all workspace-hub scripts

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Bold variants
BOLD='\033[1m'
BOLD_RED='\033[1;31m'
BOLD_GREEN='\033[1;32m'
BOLD_YELLOW='\033[1;33m'
BOLD_BLUE='\033[1;34m'

# Usage examples
echo -e "${GREEN}✓ Success${NC}"
echo -e "${RED}✗ Error${NC}"
echo -e "${YELLOW}⚠ Warning${NC}"
echo -e "${CYAN}ℹ Info${NC}"
```

### 2. Script Header Template

Every script should start with proper identification:

```bash
#!/bin/bash
# ABOUTME: Brief one-line description of what this script does
# ABOUTME: Additional context about usage or dependencies

set -e  # Exit on error

# Script metadata
SCRIPT_NAME="$(basename "$0")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="1.0.0"
```

### 3. Logging Functions

Standardized logging with timestamps and levels:

```bash
#!/bin/bash
# ABOUTME: Logging framework for bash scripts
# ABOUTME: Supports DEBUG, INFO, WARNING, ERROR, CRITICAL levels

# Log file configuration
LOG_FILE="${LOG_FILE:-/tmp/${SCRIPT_NAME}.log}"
LOG_LEVEL="${LOG_LEVEL:-INFO}"

# Log level values
declare -A LOG_LEVELS=(
    ["DEBUG"]=0
    ["INFO"]=1
    ["WARNING"]=2
    ["ERROR"]=3
    ["CRITICAL"]=4
)

log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # Check if level meets threshold
    if [[ ${LOG_LEVELS[$level]} -ge ${LOG_LEVELS[$LOG_LEVEL]} ]]; then
        case "$level" in
            DEBUG)    echo -e "${CYAN}[${timestamp}] DEBUG${NC} - $message" ;;
            INFO)     echo -e "${GREEN}[${timestamp}] INFO${NC} - $message" ;;
            WARNING)  echo -e "${YELLOW}[${timestamp}] WARNING${NC} - $message" ;;
            ERROR)    echo -e "${RED}[${timestamp}] ERROR${NC} - $message" >&2 ;;
            CRITICAL) echo -e "${BOLD_RED}[${timestamp}] CRITICAL${NC} - $message" >&2 ;;
        esac

        # Also write to log file
        echo "[${timestamp}] ${level} - $message" >> "$LOG_FILE"
    fi
}

# Convenience functions
log_debug()    { log "DEBUG" "$@"; }
log_info()     { log "INFO" "$@"; }
log_warning()  { log "WARNING" "$@"; }
log_error()    { log "ERROR" "$@"; }
log_critical() { log "CRITICAL" "$@"; }
```

### 4. Display Headers

Professional header/banner display:

```bash
#!/bin/bash
# ABOUTME: Header and banner display functions
# ABOUTME: Creates consistent visual separation in CLI output

print_header() {
    local title="$1"
    local width="${2:-60}"
    local char="${3:-═}"

    local line=$(printf "%${width}s" | tr ' ' "$char")

    echo ""
    echo -e "${CYAN}${line}${NC}"
    echo -e "${CYAN}  ${title}${NC}"
    echo -e "${CYAN}${line}${NC}"
    echo ""
}

print_section() {
    local title="$1"
    echo ""
    echo -e "${BOLD}${title}${NC}"
    echo -e "${CYAN}$(printf '%.0s─' {1..40})${NC}"
}

print_status() {
    local status="$1"
    local message="$2"

    case "$status" in
        success) echo -e "  ${GREEN}✓${NC} $message" ;;
        error)   echo -e "  ${RED}✗${NC} $message" ;;
        warning) echo -e "  ${YELLOW}⚠${NC} $message" ;;
        info)    echo -e "  ${CYAN}ℹ${NC} $message" ;;
        pending) echo -e "  ${BLUE}○${NC} $message" ;;
        skip)    echo -e "  ${MAGENTA}⊘${NC} $message" ;;
    esac
}
```

### 5. Error Handling

Robust error handling with cleanup:

```bash
#!/bin/bash
# ABOUTME: Error handling and cleanup functions
# ABOUTME: Ensures graceful exit and resource cleanup

# Trap for cleanup on exit
cleanup() {
    local exit_code=$?

    # Remove temporary files
    [[ -n "$TEMP_DIR" && -d "$TEMP_DIR" ]] && rm -rf "$TEMP_DIR"

    # Log exit status
    if [[ $exit_code -eq 0 ]]; then
        log_info "Script completed successfully"
    else
        log_error "Script exited with code $exit_code"
    fi

    exit $exit_code
}

# Set trap
trap cleanup EXIT INT TERM

# Error handler
die() {
    local message="$1"
    local exit_code="${2:-1}"

    log_critical "$message"
    exit "$exit_code"
}

# Assert function
assert() {
    local condition="$1"
    local message="${2:-Assertion failed}"

    if ! eval "$condition"; then
        die "$message"
    fi
}
```

### 6. Argument Parsing

Standard argument parsing pattern:

```bash
#!/bin/bash
# ABOUTME: Argument parsing framework
# ABOUTME: Supports short/long options with values

# Default values
VERBOSE=false
DRY_RUN=false
CONFIG_FILE=""

show_usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS] <arguments>

Options:
    -h, --help          Show this help message
    -v, --verbose       Enable verbose output
    -n, --dry-run       Show what would be done without doing it
    -c, --config FILE   Use specified configuration file
    --version           Show version information

Examples:
    $SCRIPT_NAME --verbose process
    $SCRIPT_NAME -c config.yaml --dry-run

EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                show_usage
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                LOG_LEVEL="DEBUG"
                shift
                ;;
            -n|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -c|--config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            --version)
                echo "$SCRIPT_NAME version $VERSION"
                exit 0
                ;;
            --)
                shift
                break
                ;;
            -*)
                die "Unknown option: $1"
                ;;
            *)
                break
                ;;
        esac
    done

    # Remaining arguments
    ARGS=("$@")
}
```

## Complete Example

A complete script using all framework components:

```bash
#!/bin/bash
# ABOUTME: Example script demonstrating bash-cli-framework usage
# ABOUTME: Template for new CLI tools in workspace-hub

set -e

# ─────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────

SCRIPT_NAME="$(basename "$0")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="1.0.0"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Defaults
VERBOSE=false
DRY_RUN=false
LOG_LEVEL="INFO"

# ─────────────────────────────────────────────────────────────────
# Functions
# ─────────────────────────────────────────────────────────────────

log_info()    { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warning() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }

die() { log_error "$1"; exit "${2:-1}"; }

print_header() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo ""
}

show_usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS] <command>

Commands:
    run         Execute the main operation
    status      Show current status
    clean       Clean up temporary files

Options:
    -h, --help      Show this help
    -v, --verbose   Verbose output
    -n, --dry-run   Dry run mode
    --version       Show version

EOF
}

cleanup() {
    local exit_code=$?
    [[ $VERBOSE == true ]] && log_info "Cleanup complete"
    exit $exit_code
}

trap cleanup EXIT INT TERM

# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)    show_usage; exit 0 ;;
            -v|--verbose) VERBOSE=true; shift ;;
            -n|--dry-run) DRY_RUN=true; shift ;;
            --version)    echo "$VERSION"; exit 0 ;;
            -*)           die "Unknown option: $1" ;;
            *)            break ;;
        esac
    done

    local command="${1:-}"
    [[ -z "$command" ]] && { show_usage; die "No command specified"; }

    print_header "$SCRIPT_NAME v$VERSION"

    case "$command" in
        run)
            log_info "Running main operation..."
            [[ $DRY_RUN == true ]] && log_warning "Dry run mode - no changes made"
            # Implementation here
            ;;
        status)
            log_info "Checking status..."
            ;;
        clean)
            log_info "Cleaning up..."
            ;;
        *)
            die "Unknown command: $command"
            ;;
    esac

    log_info "Done!"
}

main "$@"
```

## Best Practices

### 1. Always Use `set -e`
Exit immediately if a command exits with non-zero status:
```bash
set -e
# Or for more control:
set -euo pipefail
```

### 2. Quote Variables
Always quote variables to prevent word splitting:
```bash
# Good
echo "$variable"
"$command" "$arg1" "$arg2"

# Bad
echo $variable
$command $arg1 $arg2
```

### 3. Use Meaningful Exit Codes
```bash
# Exit codes
EXIT_SUCCESS=0
EXIT_ERROR=1
EXIT_USAGE=2
EXIT_CONFIG=3
```

### 4. Provide Feedback
Always tell the user what's happening:
```bash
log_info "Starting process..."
# do work
log_info "Process complete (processed $count items)"
```

### 5. Support Dry Run
Let users preview changes:
```bash
if [[ $DRY_RUN == true ]]; then
    log_info "[DRY RUN] Would execute: $command"
else
    eval "$command"
fi
```

## Integration with workspace-hub

This framework is used across all workspace-hub scripts:
- `scripts/monitoring/suggest_model.sh`
- `scripts/monitoring/check_claude_usage.sh`
- `scripts/workspace`
- `scripts/repository_sync`

## Resources

- [Bash Best Practices](https://mywiki.wooledge.org/BashGuide/Practices)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [ShellCheck](https://www.shellcheck.net/) - Static analysis tool

---

## Version History

- **1.0.0** (2026-01-14): Initial release - extracted from workspace-hub scripts
