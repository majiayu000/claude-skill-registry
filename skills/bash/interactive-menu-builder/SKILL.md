---
name: interactive-menu-builder
version: 1.0.0
description: Build multi-level interactive CLI menus for bash scripts
author: workspace-hub
category: bash
tags: [bash, menu, cli, interactive, tui, navigation]
platforms: [linux, macos]
---

# Interactive Menu Builder

Patterns for building professional multi-level interactive menus in bash scripts. Extracted from workspace-hub's workspace CLI and repository_sync tools.

## When to Use This Skill

✅ **Use when:**
- Building user-friendly CLI tools
- Need navigation through multiple options
- Complex tools with many sub-commands
- Tools used by humans (not just automation)
- Consolidating multiple scripts into one interface

❌ **Avoid when:**
- Scripts meant for automation/CI
- Simple single-purpose scripts
- When a plain command-line interface is sufficient

## Core Capabilities

### 1. Basic Menu Structure

Single-level menu with numbered options:

```bash
#!/bin/bash
# ABOUTME: Basic interactive menu pattern
# ABOUTME: Simple numbered option selection

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

show_menu() {
    clear
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}          Main Menu${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo ""
    echo "  1) Option One"
    echo "  2) Option Two"
    echo "  3) Option Three"
    echo ""
    echo "  0) Exit"
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo ""
}

handle_choice() {
    local choice="$1"

    case "$choice" in
        1)
            echo "Running Option One..."
            # Implementation
            ;;
        2)
            echo "Running Option Two..."
            # Implementation
            ;;
        3)
            echo "Running Option Three..."
            # Implementation
            ;;
        0)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            ;;
    esac
}

# Main loop
while true; do
    show_menu
    read -p "Select option: " choice
    handle_choice "$choice"
    echo ""
    read -p "Press Enter to continue..."
done
```

### 2. Multi-Level Menu System

Hierarchical menu with breadcrumb navigation:

```bash
#!/bin/bash
# ABOUTME: Multi-level menu system with navigation stack
# ABOUTME: Pattern from workspace-hub workspace CLI

# Navigation stack
declare -a MENU_STACK=("main")
CURRENT_MENU="main"

# Menu definitions
declare -A MENU_TITLES=(
    ["main"]="Main Menu"
    ["repo"]="Repository Management"
    ["repo_ops"]="Repository Operations"
    ["compliance"]="Compliance & Standards"
    ["tools"]="Development Tools"
)

# Go to submenu
push_menu() {
    local menu="$1"
    MENU_STACK+=("$menu")
    CURRENT_MENU="$menu"
}

# Go back
pop_menu() {
    if [[ ${#MENU_STACK[@]} -gt 1 ]]; then
        unset 'MENU_STACK[-1]'
        CURRENT_MENU="${MENU_STACK[-1]}"
    fi
}

# Display breadcrumb
show_breadcrumb() {
    local crumb=""
    for menu in "${MENU_STACK[@]}"; do
        [[ -n "$crumb" ]] && crumb+=" > "
        crumb+="${MENU_TITLES[$menu]}"
    done
    echo -e "${CYAN}$crumb${NC}"
}

# Main menu
show_main_menu() {
    clear
    echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}              Workspace Hub - Management Console${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
    echo ""
    show_breadcrumb
    echo ""
    echo "  1) Repository Management"
    echo "  2) Compliance & Standards"
    echo "  3) Development Tools"
    echo "  4) System Configuration"
    echo "  5) Help & Documentation"
    echo ""
    echo "  0) Exit"
    echo ""
}

# Repository submenu
show_repo_menu() {
    clear
    echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
    show_breadcrumb
    echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo "  1) Repository Sync Manager"
    echo "  2) Configure Repository URLs"
    echo "  3) Check All Repository Status"
    echo "  4) Clone Repositories"
    echo ""
    echo "  0) Back"
    echo ""
}

# Handle navigation
handle_menu() {
    local choice="$1"

    case "$CURRENT_MENU" in
        main)
            case "$choice" in
                1) push_menu "repo" ;;
                2) push_menu "compliance" ;;
                3) push_menu "tools" ;;
                4) run_system_config ;;
                5) run_help ;;
                0) exit 0 ;;
            esac
            ;;
        repo)
            case "$choice" in
                1) run_repo_sync ;;
                2) run_configure_urls ;;
                3) run_check_status ;;
                4) push_menu "repo_ops" ;;
                0) pop_menu ;;
            esac
            ;;
        # Add more menus...
    esac
}

# Display current menu
show_current_menu() {
    case "$CURRENT_MENU" in
        main) show_main_menu ;;
        repo) show_repo_menu ;;
        # Add more...
    esac
}

# Main loop
while true; do
    show_current_menu
    read -p "Select option: " choice
    handle_menu "$choice"
done
```

### 3. Table Display

Display data in formatted tables:

```bash
#!/bin/bash
# ABOUTME: Table display functions for CLI menus
# ABOUTME: Format data in aligned columns with headers

# Print table header
print_table_header() {
    local -a headers=("$@")
    local format=""

    # Build format string
    for header in "${headers[@]}"; do
        format+="%-20s "
    done

    echo ""
    printf "${CYAN}${format}${NC}\n" "${headers[@]}"
    printf "${CYAN}%s${NC}\n" "$(printf '─%.0s' {1..80})"
}

# Print table row
print_table_row() {
    local format=""
    local -a values=("$@")

    for _ in "${values[@]}"; do
        format+="%-20s "
    done

    printf "${format}\n" "${values[@]}"
}

# Display repository table
show_repo_table() {
    print_table_header "Repository" "Category" "Status" "Branch"

    for repo in "${REPOS[@]}"; do
        local category=$(get_category "$repo")
        local status=$(get_status "$repo")
        local branch=$(get_branch "$repo")

        # Color-code status
        case "$status" in
            "Clean")      status="${GREEN}Clean${NC}" ;;
            "Modified")   status="${YELLOW}Modified${NC}" ;;
            "Untracked")  status="${RED}Untracked${NC}" ;;
        esac

        print_table_row "$repo" "$category" "$status" "$branch"
    done
}
```

### 4. Selection Lists

Let users select from a list:

```bash
#!/bin/bash
# ABOUTME: Selection list patterns
# ABOUTME: Single and multi-select from numbered lists

# Single selection
select_single() {
    local prompt="$1"
    shift
    local -a options=("$@")

    echo ""
    for i in "${!options[@]}"; do
        echo "  $((i+1))) ${options[$i]}"
    done
    echo ""
    echo "  0) Cancel"
    echo ""

    read -p "$prompt: " choice

    if [[ "$choice" == "0" ]]; then
        return 1
    elif [[ "$choice" -ge 1 && "$choice" -le ${#options[@]} ]]; then
        SELECTED="${options[$((choice-1))]}"
        return 0
    else
        echo -e "${RED}Invalid selection${NC}"
        return 1
    fi
}

# Multi-selection
select_multiple() {
    local prompt="$1"
    shift
    local -a options=("$@")
    local -a selected=()

    echo ""
    echo "Enter numbers separated by spaces (or 'all' for all):"
    echo ""

    for i in "${!options[@]}"; do
        echo "  $((i+1))) ${options[$i]}"
    done
    echo ""

    read -p "$prompt: " input

    if [[ "$input" == "all" ]]; then
        SELECTED=("${options[@]}")
        return 0
    fi

    for num in $input; do
        if [[ "$num" -ge 1 && "$num" -le ${#options[@]} ]]; then
            selected+=("${options[$((num-1))]}")
        fi
    done

    SELECTED=("${selected[@]}")
    [[ ${#SELECTED[@]} -gt 0 ]]
}

# Usage
repos=("repo1" "repo2" "repo3" "repo4")

if select_single "Select repository" "${repos[@]}"; then
    echo "You selected: $SELECTED"
fi

if select_multiple "Select repositories" "${repos[@]}"; then
    echo "You selected: ${SELECTED[*]}"
fi
```

### 5. Confirmation Dialogs

Request user confirmation:

```bash
#!/bin/bash
# ABOUTME: Confirmation dialog patterns
# ABOUTME: Yes/No prompts with defaults

# Simple yes/no
confirm() {
    local prompt="${1:-Are you sure?}"
    local default="${2:-n}"  # Default to no

    if [[ "$default" == "y" ]]; then
        prompt+=" [Y/n]: "
    else
        prompt+=" [y/N]: "
    fi

    read -p "$prompt" response
    response="${response:-$default}"

    [[ "${response,,}" == "y" || "${response,,}" == "yes" ]]
}

# Confirmation with explanation
confirm_action() {
    local action="$1"
    local details="$2"

    echo ""
    echo -e "${YELLOW}⚠ Confirmation Required${NC}"
    echo ""
    echo "Action: $action"
    [[ -n "$details" ]] && echo "Details: $details"
    echo ""

    confirm "Proceed?" "n"
}

# Dangerous action confirmation
confirm_dangerous() {
    local action="$1"
    local confirm_word="${2:-DELETE}"

    echo ""
    echo -e "${RED}⚠ DANGEROUS OPERATION${NC}"
    echo ""
    echo "This action cannot be undone!"
    echo "Action: $action"
    echo ""
    echo -e "Type '${YELLOW}${confirm_word}${NC}' to confirm:"

    read -p "> " response
    [[ "$response" == "$confirm_word" ]]
}

# Usage
if confirm "Delete all logs?"; then
    rm -rf logs/*
fi

if confirm_dangerous "Delete all repositories" "DELETE"; then
    # Perform dangerous action
    echo "Proceeding..."
fi
```

### 6. Progress Indicators

Show progress during operations:

```bash
#!/bin/bash
# ABOUTME: Progress indicator patterns
# ABOUTME: Spinners, bars, and status updates

# Spinner
spinner() {
    local pid=$1
    local message="${2:-Processing}"
    local spin='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    local i=0

    while kill -0 "$pid" 2>/dev/null; do
        i=$(( (i+1) % ${#spin} ))
        printf "\r${CYAN}%s${NC} %s" "${spin:$i:1}" "$message"
        sleep 0.1
    done

    printf "\r${GREEN}✓${NC} %s\n" "$message"
}

# Usage
long_running_task &
spinner $! "Running long task..."

# Progress bar
progress_bar() {
    local current=$1
    local total=$2
    local width=40
    local percent=$((current * 100 / total))
    local filled=$((current * width / total))
    local empty=$((width - filled))

    printf "\r["
    printf "%${filled}s" | tr ' ' '█'
    printf "%${empty}s" | tr ' ' '░'
    printf "] %3d%% (%d/%d)" "$percent" "$current" "$total"
}

# Usage
total=100
for i in $(seq 1 $total); do
    progress_bar $i $total
    sleep 0.05
done
echo ""

# Status updates
status_line() {
    local message="$1"
    printf "\r\033[K%s" "$message"  # Clear line and print
}

# Completion markers
mark_done() {
    local message="$1"
    echo -e "${GREEN}✓${NC} $message"
}

mark_fail() {
    local message="$1"
    echo -e "${RED}✗${NC} $message"
}

mark_skip() {
    local message="$1"
    echo -e "${YELLOW}⊘${NC} $message"
}
```

## Complete Example: Multi-Level Menu System

Full implementation from workspace CLI:

```bash
#!/bin/bash
# ABOUTME: Complete multi-level menu system
# ABOUTME: Template for workspace-hub style CLI tools

set -e

# ─────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────

SCRIPT_NAME="$(basename "$0")"
VERSION="1.0.0"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# Menu state
CURRENT_MENU="main"
declare -a MENU_HISTORY=()

# ─────────────────────────────────────────────────────────────────
# Utility Functions
# ─────────────────────────────────────────────────────────────────

clear_screen() {
    printf "\033c"
}

print_header() {
    local title="$1"
    local width=60

    echo ""
    echo -e "${CYAN}$(printf '═%.0s' $(seq 1 $width))${NC}"
    printf "${CYAN}%*s${NC}\n" $(((${#title}+width)/2)) "$title"
    echo -e "${CYAN}$(printf '═%.0s' $(seq 1 $width))${NC}"
    echo ""
}

print_breadcrumb() {
    if [[ ${#MENU_HISTORY[@]} -gt 0 ]]; then
        local path=""
        for menu in "${MENU_HISTORY[@]}"; do
            [[ -n "$path" ]] && path+=" > "
            path+="$menu"
        done
        path+=" > $CURRENT_MENU"
        echo -e "${BLUE}$path${NC}"
        echo ""
    fi
}

print_option() {
    local num="$1"
    local text="$2"
    local desc="${3:-}"

    printf "  ${BOLD}%2s)${NC} %-25s" "$num" "$text"
    [[ -n "$desc" ]] && printf "${CYAN}%s${NC}" "$desc"
    echo ""
}

wait_key() {
    echo ""
    read -p "Press Enter to continue..."
}

navigate_to() {
    MENU_HISTORY+=("$CURRENT_MENU")
    CURRENT_MENU="$1"
}

navigate_back() {
    if [[ ${#MENU_HISTORY[@]} -gt 0 ]]; then
        CURRENT_MENU="${MENU_HISTORY[-1]}"
        unset 'MENU_HISTORY[-1]'
    fi
}

# ─────────────────────────────────────────────────────────────────
# Menu Displays
# ─────────────────────────────────────────────────────────────────

show_main_menu() {
    clear_screen
    print_header "Workspace Hub Management Console"

    echo "  ${BOLD}Workspace Management:${NC}"
    echo ""
    print_option 1 "Repository Management" "Git operations"
    print_option 2 "Compliance & Standards" "Code standards"
    print_option 3 "Development Tools" "Dev utilities"
    print_option 4 "System Configuration" "Setup"
    echo ""
    echo "  ${BOLD}Information:${NC}"
    echo ""
    print_option 5 "Help & Documentation"
    print_option 6 "About"
    echo ""
    print_option 0 "Exit"
    echo ""
}

show_repo_menu() {
    clear_screen
    print_header "Repository Management"
    print_breadcrumb

    print_option 1 "Sync All Repositories" "Pull/push all"
    print_option 2 "Clone Missing Repos" "Download new"
    print_option 3 "Check Status" "Git status"
    print_option 4 "Branch Operations" "Branch management"
    echo ""
    print_option 0 "Back"
    echo ""
}

show_compliance_menu() {
    clear_screen
    print_header "Compliance & Standards"
    print_breadcrumb

    print_option 1 "Propagate Configuration" "Sync settings"
    print_option 2 "Verify Compliance" "Check standards"
    print_option 3 "Install Hooks" "Git hooks"
    echo ""
    print_option 0 "Back"
    echo ""
}

# ─────────────────────────────────────────────────────────────────
# Action Handlers
# ─────────────────────────────────────────────────────────────────

run_sync_repos() {
    echo ""
    echo -e "${CYAN}Syncing all repositories...${NC}"
    # Implementation
    echo -e "${GREEN}✓ Sync complete${NC}"
    wait_key
}

run_check_status() {
    echo ""
    echo -e "${CYAN}Checking repository status...${NC}"
    # Implementation
    wait_key
}

# ─────────────────────────────────────────────────────────────────
# Menu Handlers
# ─────────────────────────────────────────────────────────────────

handle_main_menu() {
    local choice="$1"
    case "$choice" in
        1) navigate_to "repo" ;;
        2) navigate_to "compliance" ;;
        3) navigate_to "tools" ;;
        4) run_system_config ;;
        5) run_help ;;
        6) run_about ;;
        0) echo "Goodbye!"; exit 0 ;;
        *) echo -e "${RED}Invalid option${NC}"; sleep 1 ;;
    esac
}

handle_repo_menu() {
    local choice="$1"
    case "$choice" in
        1) run_sync_repos ;;
        2) run_clone_repos ;;
        3) run_check_status ;;
        4) navigate_to "branches" ;;
        0) navigate_back ;;
        *) echo -e "${RED}Invalid option${NC}"; sleep 1 ;;
    esac
}

handle_compliance_menu() {
    local choice="$1"
    case "$choice" in
        1) run_propagate_config ;;
        2) run_verify_compliance ;;
        3) run_install_hooks ;;
        0) navigate_back ;;
        *) echo -e "${RED}Invalid option${NC}"; sleep 1 ;;
    esac
}

# ─────────────────────────────────────────────────────────────────
# Main Loop
# ─────────────────────────────────────────────────────────────────

main() {
    while true; do
        case "$CURRENT_MENU" in
            main)
                show_main_menu
                read -p "Select option: " choice
                handle_main_menu "$choice"
                ;;
            repo)
                show_repo_menu
                read -p "Select option: " choice
                handle_repo_menu "$choice"
                ;;
            compliance)
                show_compliance_menu
                read -p "Select option: " choice
                handle_compliance_menu "$choice"
                ;;
            *)
                echo "Unknown menu: $CURRENT_MENU"
                CURRENT_MENU="main"
                ;;
        esac
    done
}

main "$@"
```

## Best Practices

### 1. Consistent Navigation
- `0` always goes back/exits
- Numbers 1-9 for options
- Use `q` as alternative to `0` for exit

### 2. Clear Visual Hierarchy
- Headers separate sections
- Indentation shows grouping
- Colors indicate meaning

### 3. Feedback on Actions
- Show progress during operations
- Confirm completion
- Display errors clearly

### 4. Graceful Error Handling
- Invalid input shouldn't crash
- Show helpful error messages
- Allow retry

## Resources

- [Dialog Tool](https://invisible-island.net/dialog/) - TUI dialogs
- [Whiptail](https://en.wikibooks.org/wiki/Bash_Shell_Scripting/Whiptail) - Alternative TUI
- [Gum](https://github.com/charmbracelet/gum) - Modern CLI toolkit

---

## Version History

- **1.0.0** (2026-01-14): Initial release - extracted from workspace-hub CLI tools
