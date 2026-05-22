---
name: bash-script-framework
description: Create organized bash script structure with color output, menu systems, error handling, and cross-platform support. Standardizes CLI tooling.
version: 1.0.0
category: workspace-hub
type: skill
trigger: manual
auto_execute: false
capabilities:
  - script_organization
  - menu_systems
  - color_output
  - error_handling
  - cross_platform
tools:
  - Write
  - Bash
  - Read
related_skills:
  - python-project-template
  - yaml-workflow-executor
---

# Bash Script Framework

> Create standardized bash scripts with menus, colors, and error handling.

## Quick Start

```bash
# Create script directory structure
/bash-script-framework init

# Create new script with menu
/bash-script-framework new my-script --menu

# Add to existing scripts directory
/bash-script-framework add utility-script
```

## When to Use

**USE when:**
- Creating CLI tools for repository
- Building menu-driven automation
- Standardizing script organization
- Cross-platform script development

**DON'T USE when:**
- Python script is more appropriate
- Simple one-liner needed
- Windows-only environment

## Prerequisites

- Bash 4.0+
- Unix-like environment (Linux, macOS, WSL)

## Overview

Creates organized bash scripts following workspace-hub patterns:

1. **Color utilities** - Consistent terminal output
2. **Menu systems** - Multi-level navigation
3. **Error handling** - Proper exit codes
4. **Logging** - Timestamped output
5. **Cross-platform** - Linux/macOS/WSL support

## Directory Structure

```
scripts/
├── workspace                  # Main entry point
├── lib/
│   ├── colors.sh             # Color definitions
│   ├── logging.sh            # Logging utilities
│   ├── menu.sh               # Menu system
│   └── utils.sh              # General utilities
├── bash/
│   ├── git/                  # Git operations
│   └── dev/                  # Development tools
├── python/                   # Python utilities
└── powershell/               # Windows scripts
```

## Core Templates

### 1. Color Library (lib/colors.sh)

```bash
#!/bin/bash
# lib/colors.sh - Color definitions for terminal output
# Source this file: source lib/colors.sh

# Reset
NC='\033[0m'              # No Color / Reset

# Regular Colors
BLACK='\033[0;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'

# Bold Colors
BOLD_BLACK='\033[1;30m'
BOLD_RED='\033[1;31m'
BOLD_GREEN='\033[1;32m'
BOLD_YELLOW='\033[1;33m'
BOLD_BLUE='\033[1;34m'
BOLD_MAGENTA='\033[1;35m'
BOLD_CYAN='\033[1;36m'
BOLD_WHITE='\033[1;37m'

# Background Colors
BG_BLACK='\033[40m'
BG_RED='\033[41m'
BG_GREEN='\033[42m'
BG_YELLOW='\033[43m'
BG_BLUE='\033[44m'
BG_MAGENTA='\033[45m'
BG_CYAN='\033[46m'
BG_WHITE='\033[47m'

# Formatting
BOLD='\033[1m'
DIM='\033[2m'
UNDERLINE='\033[4m'
BLINK='\033[5m'
REVERSE='\033[7m'

# Status indicators
SUCCESS="${GREEN}✓${NC}"
FAIL="${RED}✗${NC}"
WARN="${YELLOW}⚠${NC}"
INFO="${BLUE}ℹ${NC}"
ARROW="${CYAN}→${NC}"

# Print colored text
print_color() {
    local color="$1"
    local message="$2"
    echo -e "${color}${message}${NC}"
}

# Status messages
print_success() { echo -e "${SUCCESS} ${GREEN}$1${NC}"; }
print_error() { echo -e "${FAIL} ${RED}$1${NC}" >&2; }
print_warning() { echo -e "${WARN} ${YELLOW}$1${NC}"; }
print_info() { echo -e "${INFO} ${BLUE}$1${NC}"; }

# Headers and separators
print_header() {
    local title="$1"
    local width=${2:-60}
    local line=$(printf '═%.0s' $(seq 1 $width))
    echo -e "\n${BOLD_CYAN}╔${line}╗${NC}"
    printf "${BOLD_CYAN}║${NC} ${BOLD_WHITE}%-$((width-2))s${NC} ${BOLD_CYAN}║${NC}\n" "$title"
    echo -e "${BOLD_CYAN}╚${line}╝${NC}\n"
}

print_separator() {
    local width=${1:-60}
    local char=${2:-─}
    printf "${DIM}%${width}s${NC}\n" | tr ' ' "$char"
}

# Check if colors are supported
supports_colors() {
    if [[ -t 1 ]] && [[ -n "$TERM" ]] && [[ "$TERM" != "dumb" ]]; then
        return 0
    fi
    return 1
}

# Disable colors if not supported
if ! supports_colors; then
    NC='' RED='' GREEN='' YELLOW='' BLUE='' MAGENTA='' CYAN='' WHITE=''
    BOLD='' DIM='' SUCCESS='[OK]' FAIL='[FAIL]' WARN='[WARN]' INFO='[INFO]'
fi
```

### 2. Logging Library (lib/logging.sh)

```bash
#!/bin/bash
# lib/logging.sh - Logging utilities
# Source this file after colors.sh

# Log levels
LOG_LEVEL_DEBUG=0
LOG_LEVEL_INFO=1
LOG_LEVEL_WARN=2
LOG_LEVEL_ERROR=3

# Current log level (default: INFO)
CURRENT_LOG_LEVEL=${CURRENT_LOG_LEVEL:-$LOG_LEVEL_INFO}

# Log file (optional)
LOG_FILE="${LOG_FILE:-}"

# Timestamp format
timestamp() {
    date "+%Y-%m-%d %H:%M:%S"
}

# Internal log function
_log() {
    local level="$1"
    local level_name="$2"
    local color="$3"
    local message="$4"

    if [[ $level -ge $CURRENT_LOG_LEVEL ]]; then
        local ts=$(timestamp)
        local formatted="[${ts}] [${level_name}] ${message}"

        # Output to console
        echo -e "${color}${formatted}${NC}"

        # Output to log file if configured
        if [[ -n "$LOG_FILE" ]]; then
            echo "${formatted}" >> "$LOG_FILE"
        fi
    fi
}

# Log functions
log_debug() { _log $LOG_LEVEL_DEBUG "DEBUG" "$DIM" "$1"; }
log_info() { _log $LOG_LEVEL_INFO "INFO " "$BLUE" "$1"; }
log_warn() { _log $LOG_LEVEL_WARN "WARN " "$YELLOW" "$1"; }
log_error() { _log $LOG_LEVEL_ERROR "ERROR" "$RED" "$1"; }

# Log with custom prefix
log_step() {
    local step="$1"
    local message="$2"
    echo -e "${CYAN}[Step ${step}]${NC} ${message}"
}

log_progress() {
    local current="$1"
    local total="$2"
    local message="${3:-Processing}"
    local percent=$((current * 100 / total))
    printf "\r${CYAN}%s${NC}: [%3d%%] %d/%d" "$message" "$percent" "$current" "$total"
}

log_progress_done() {
    echo ""  # New line after progress
}

# Set log level
set_log_level() {
    case "$1" in
        debug|DEBUG) CURRENT_LOG_LEVEL=$LOG_LEVEL_DEBUG ;;
        info|INFO)   CURRENT_LOG_LEVEL=$LOG_LEVEL_INFO ;;
        warn|WARN)   CURRENT_LOG_LEVEL=$LOG_LEVEL_WARN ;;
        error|ERROR) CURRENT_LOG_LEVEL=$LOG_LEVEL_ERROR ;;
        *) log_error "Unknown log level: $1" ;;
    esac
}

# Enable file logging
enable_file_logging() {
    LOG_FILE="${1:-logs/script.log}"
    mkdir -p "$(dirname "$LOG_FILE")"
    log_info "Logging to file: $LOG_FILE"
}
```

### 3. Menu System (lib/menu.sh)

```bash
#!/bin/bash
# lib/menu.sh - Menu system utilities
# Source after colors.sh

# Display menu and get selection
show_menu() {
    local title="$1"
    shift
    local options=("$@")

    print_header "$title"

    local i=1
    for option in "${options[@]}"; do
        if [[ "$option" == "---" ]]; then
            print_separator 40
        else
            printf "  ${CYAN}%2d)${NC} %s\n" "$i" "$option"
            ((i++))
        fi
    done

    echo ""
    printf "  ${CYAN} 0)${NC} ${DIM}Exit / Back${NC}\n"
    echo ""

    read -p "$(echo -e ${BOLD}Select option: ${NC})" choice
    echo "$choice"
}

# Confirm action
confirm() {
    local message="${1:-Are you sure?}"
    local default="${2:-n}"

    if [[ "$default" == "y" ]]; then
        read -p "$(echo -e ${YELLOW}$message [Y/n]: ${NC})" response
        response=${response:-y}
    else
        read -p "$(echo -e ${YELLOW}$message [y/N]: ${NC})" response
        response=${response:-n}
    fi

    [[ "$response" =~ ^[Yy]$ ]]
}

# Prompt for input
prompt_input() {
    local message="$1"
    local default="${2:-}"
    local result

    if [[ -n "$default" ]]; then
        read -p "$(echo -e ${CYAN}$message [$default]: ${NC})" result
        result=${result:-$default}
    else
        read -p "$(echo -e ${CYAN}$message: ${NC})" result
    fi

    echo "$result"
}

# Select from list
select_from_list() {
    local title="$1"
    shift
    local items=("$@")

    echo -e "\n${BOLD}$title${NC}\n"

    local i=1
    for item in "${items[@]}"; do
        printf "  ${CYAN}%2d)${NC} %s\n" "$i" "$item"
        ((i++))
    done

    echo ""
    read -p "$(echo -e ${BOLD}Select [1-${#items[@]}]: ${NC})" choice

    if [[ "$choice" =~ ^[0-9]+$ ]] && [[ "$choice" -ge 1 ]] && [[ "$choice" -le ${#items[@]} ]]; then
        echo "${items[$((choice-1))]}"
    else
        echo ""
    fi
}

# Multi-select from list
multi_select() {
    local title="$1"
    shift
    local items=("$@")
    local selected=()

    echo -e "\n${BOLD}$title${NC}"
    echo -e "${DIM}(Enter numbers separated by spaces, or 'all')${NC}\n"

    local i=1
    for item in "${items[@]}"; do
        printf "  ${CYAN}%2d)${NC} %s\n" "$i" "$item"
        ((i++))
    done

    echo ""
    read -p "$(echo -e ${BOLD}Select: ${NC})" choices

    if [[ "$choices" == "all" ]]; then
        selected=("${items[@]}")
    else
        for choice in $choices; do
            if [[ "$choice" =~ ^[0-9]+$ ]] && [[ "$choice" -ge 1 ]] && [[ "$choice" -le ${#items[@]} ]]; then
                selected+=("${items[$((choice-1))]}")
            fi
        done
    fi

    printf '%s\n' "${selected[@]}"
}

# Wait for keypress
wait_for_key() {
    local message="${1:-Press any key to continue...}"
    echo -e "\n${DIM}$message${NC}"
    read -n 1 -s
}

# Clear screen with header
clear_with_header() {
    local title="${1:-Menu}"
    clear
    print_header "$title" 60
}
```

### 4. Utilities (lib/utils.sh)

```bash
#!/bin/bash
# lib/utils.sh - General utilities

# Check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check required commands
require_commands() {
    local missing=()
    for cmd in "$@"; do
        if ! command_exists "$cmd"; then
            missing+=("$cmd")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing required commands: ${missing[*]}"
        return 1
    fi
    return 0
}

# Get script directory
get_script_dir() {
    echo "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
}

# Get project root
get_project_root() {
    local dir="$(get_script_dir)"
    while [[ "$dir" != "/" ]]; do
        if [[ -f "$dir/pyproject.toml" ]] || [[ -f "$dir/CLAUDE.md" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    echo "$(pwd)"
}

# Run command with error handling
run_cmd() {
    local cmd="$*"
    log_debug "Running: $cmd"

    if eval "$cmd"; then
        return 0
    else
        local exit_code=$?
        log_error "Command failed (exit code $exit_code): $cmd"
        return $exit_code
    fi
}

# Retry command
retry() {
    local max_attempts="${1:-3}"
    local delay="${2:-5}"
    shift 2
    local cmd="$*"

    local attempt=1
    while [[ $attempt -le $max_attempts ]]; do
        log_info "Attempt $attempt/$max_attempts: $cmd"

        if eval "$cmd"; then
            return 0
        fi

        if [[ $attempt -lt $max_attempts ]]; then
            log_warn "Retrying in ${delay}s..."
            sleep "$delay"
        fi

        ((attempt++))
    done

    log_error "All $max_attempts attempts failed"
    return 1
}

# Check if running as root
is_root() {
    [[ $EUID -eq 0 ]]
}

# Check OS type
get_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux" ;;
        Darwin*)    echo "macos" ;;
        CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
        *)          echo "unknown" ;;
    esac
}

# Check if in git repository
is_git_repo() {
    git rev-parse --is-inside-work-tree &> /dev/null
}

# Get current git branch
get_git_branch() {
    git rev-parse --abbrev-ref HEAD 2>/dev/null
}

# Cleanup handler
cleanup() {
    local exit_code=$?
    # Add cleanup tasks here
    exit $exit_code
}

# Setup signal handlers
setup_cleanup() {
    trap cleanup EXIT INT TERM
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -v|--verbose) VERBOSE=true ;;
            -q|--quiet) QUIET=true ;;
            -h|--help) show_help; exit 0 ;;
            --) shift; break ;;
            -*) log_error "Unknown option: $1"; exit 1 ;;
            *) ARGS+=("$1") ;;
        esac
        shift
    done
}

# File operations
backup_file() {
    local file="$1"
    if [[ -f "$file" ]]; then
        local backup="${file}.bak.$(date +%Y%m%d%H%M%S)"
        cp "$file" "$backup"
        log_info "Backed up: $file -> $backup"
    fi
}

# Ensure directory exists
ensure_dir() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        log_debug "Created directory: $dir"
    fi
}
```

### 5. Main Script Template

```bash
#!/bin/bash
# scripts/my-tool - Main entry point
# Description: Tool description here

set -e  # Exit on error

# Get script directory and load libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/colors.sh"
source "${SCRIPT_DIR}/lib/logging.sh"
source "${SCRIPT_DIR}/lib/menu.sh"
source "${SCRIPT_DIR}/lib/utils.sh"

# Configuration
VERSION="1.0.0"
TOOL_NAME="My Tool"

# Show help
show_help() {
    cat << EOF
${BOLD}${TOOL_NAME}${NC} v${VERSION}

${BOLD}Usage:${NC}
    $0 [options] [command]

${BOLD}Commands:${NC}
    menu        Show interactive menu (default)
    status      Show status
    run         Run operation
    help        Show this help

${BOLD}Options:${NC}
    -v, --verbose    Enable verbose output
    -q, --quiet      Suppress output
    -h, --help       Show this help

${BOLD}Examples:${NC}
    $0                  # Interactive menu
    $0 status           # Show status
    $0 run --verbose    # Run with verbose output
EOF
}

# Show version
show_version() {
    echo "${TOOL_NAME} v${VERSION}"
}

# Status command
cmd_status() {
    print_header "Status"
    print_info "Version: ${VERSION}"
    print_info "OS: $(get_os)"
    print_info "User: $(whoami)"

    if is_git_repo; then
        print_success "Git repository: $(get_git_branch)"
    else
        print_warning "Not a git repository"
    fi
}

# Run command
cmd_run() {
    print_header "Running Operation"
    log_info "Starting operation..."

    # Add operation logic here

    print_success "Operation completed"
}

# Main menu
main_menu() {
    while true; do
        clear_with_header "$TOOL_NAME"

        choice=$(show_menu "Main Menu" \
            "View Status" \
            "Run Operation" \
            "Settings" \
            "---" \
            "Help"
        )

        case "$choice" in
            1) cmd_status; wait_for_key ;;
            2) cmd_run; wait_for_key ;;
            3) settings_menu ;;
            4) show_help; wait_for_key ;;
            0|"") break ;;
            *) print_error "Invalid option"; sleep 1 ;;
        esac
    done
}

# Settings submenu
settings_menu() {
    while true; do
        choice=$(show_menu "Settings" \
            "Set Log Level" \
            "Enable File Logging" \
            "View Configuration"
        )

        case "$choice" in
            1)
                level=$(select_from_list "Log Level" "debug" "info" "warn" "error")
                [[ -n "$level" ]] && set_log_level "$level"
                ;;
            2) enable_file_logging "logs/tool.log" ;;
            3) print_info "Config: verbose=$VERBOSE" ;;
            0|"") break ;;
        esac
    done
}

# Main entry point
main() {
    # Parse global options
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -v|--verbose) set_log_level debug ;;
            -q|--quiet) set_log_level error ;;
            -h|--help) show_help; exit 0 ;;
            --version) show_version; exit 0 ;;
            -*) log_error "Unknown option: $1"; exit 1 ;;
            *) break ;;
        esac
        shift
    done

    # Handle commands
    local cmd="${1:-menu}"

    case "$cmd" in
        menu) main_menu ;;
        status) cmd_status ;;
        run) shift; cmd_run "$@" ;;
        help) show_help ;;
        *) log_error "Unknown command: $cmd"; show_help; exit 1 ;;
    esac
}

# Run main
main "$@"
```

## Usage Examples

### Example 1: Create New CLI Tool

```bash
# Initialize framework
/bash-script-framework init

# Create tool with menu
/bash-script-framework new repo-manager --menu

# Result: scripts/repo-manager with full menu system
```

### Example 2: Add Simple Script

```bash
# Add utility script
/bash-script-framework add backup-tool

# Creates scripts/backup-tool with basic template
```

## Best Practices

1. **Use set -e** - Exit on errors
2. **Source libraries** - Don't duplicate code
3. **Use functions** - Modular, testable code
4. **Handle signals** - Cleanup on exit
5. **Validate inputs** - Check before executing

## Related Skills

- [python-project-template](../python-project-template/SKILL.md) - Python CLI tools
- [yaml-workflow-executor](../yaml-workflow-executor/SKILL.md) - YAML-driven execution

## References

- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
- [workspace-hub CLI Standards](../../../docs/modules/cli/WORKSPACE_CLI.md)

---

## Version History

- **1.0.0** (2026-01-14): Initial release - bash script framework with colors, menus, logging, and utilities
