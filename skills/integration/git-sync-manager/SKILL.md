---
name: git-sync-manager
version: 1.0.0
description: Multi-repository git synchronization patterns for batch operations
author: workspace-hub
category: bash
tags: [bash, git, sync, multi-repo, batch, automation]
platforms: [linux, macos]
---

# Git Sync Manager

Patterns for synchronizing multiple Git repositories with phased operations, status tracking, and error handling. Extracted from workspace-hub's repository sync scripts.

## When to Use This Skill

✅ **Use when:**
- Managing multiple Git repositories from a central location
- Performing batch git operations (pull, commit, push)
- Need consistent sync workflows across many repos
- Automating daily/periodic repository synchronization
- Building repository management CLIs

❌ **Avoid when:**
- Single repository operations
- Complex merge/rebase workflows requiring manual intervention
- Repositories with conflicting changes that need resolution

## Core Capabilities

### 1. Repository Discovery from .gitignore

Automatically discover repositories listed in .gitignore:

```bash
#!/bin/bash
# ABOUTME: Discover repositories from .gitignore patterns
# ABOUTME: Parses directory entries and validates git repos

WORKSPACE_ROOT="${1:-.}"

# Discover repositories from .gitignore
discover_repos() {
    local repos=()

    while IFS= read -r line; do
        # Skip comments and empty lines
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "$line" ]] && continue

        # Extract repo name (before the /)
        local repo_name="${line%%/*}"
        [[ -z "$repo_name" ]] && continue

        # Check if directory exists and is a git repo
        if [[ -d "$WORKSPACE_ROOT/$repo_name/.git" ]]; then
            repos+=("$repo_name")
        fi
    done < <(grep -v "^[[:space:]]*#" "$WORKSPACE_ROOT/.gitignore" | grep "/" | head -100)

    printf '%s\n' "${repos[@]}"
}

# Usage
REPOS=($(discover_repos))
echo "Found ${#REPOS[@]} repositories"
```

### 2. Multi-Phase Sync Pattern

Execute git operations in ordered phases:

```bash
#!/bin/bash
# ABOUTME: Multi-phase git synchronization
# ABOUTME: Executes pull → commit → push in controlled phases

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Counters
SUCCESS=0
FAILED=0
SKIPPED=0

# ─────────────────────────────────────────────────────────────────
# Phase 1: Pull
# ─────────────────────────────────────────────────────────────────

phase_pull() {
    local repos=("$@")

    echo -e "${CYAN}PHASE 1: Pulling latest changes${NC}"
    echo -e "${CYAN}─────────────────────────────────${NC}"

    for repo in "${repos[@]}"; do
        if [[ -d "$repo/.git" ]]; then
            echo -n "→ Pulling $repo... "

            local branch
            branch=$(cd "$repo" && git rev-parse --abbrev-ref HEAD 2>/dev/null)

            if (cd "$repo" && git pull origin "$branch" 2>&1 | grep -qE "Already up.to" ); then
                echo -e "${GREEN}✓ (up to date)${NC}"
                ((SUCCESS++))
            elif (cd "$repo" && git pull origin "$branch" &>/dev/null); then
                echo -e "${GREEN}✓ (updated)${NC}"
                ((SUCCESS++))
            else
                echo -e "${YELLOW}⚠ (offline or error)${NC}"
                ((SKIPPED++))
            fi
        fi
    done
}

# ─────────────────────────────────────────────────────────────────
# Phase 2: Commit
# ─────────────────────────────────────────────────────────────────

phase_commit() {
    local repos=("$@")
    local message="${COMMIT_MESSAGE:-chore: Batch synchronization}"

    echo -e "\n${CYAN}PHASE 2: Staging and committing changes${NC}"
    echo -e "${CYAN}───────────────────────────────────────${NC}"

    for repo in "${repos[@]}"; do
        if [[ -d "$repo/.git" ]]; then
            # Check for changes (staged or unstaged)
            local has_changes=false

            if ! (cd "$repo" && git diff --quiet 2>/dev/null); then
                has_changes=true
            fi
            if ! (cd "$repo" && git diff --cached --quiet 2>/dev/null); then
                has_changes=true
            fi

            if [[ "$has_changes" == "true" ]]; then
                echo -n "→ Committing $repo... "

                if (cd "$repo" && git add -A && git commit -m "$message" --no-verify 2>/dev/null); then
                    echo -e "${GREEN}✓${NC}"
                    ((SUCCESS++))
                else
                    echo -e "${YELLOW}⊘ (commit failed)${NC}"
                    ((SKIPPED++))
                fi
            else
                echo -e "${YELLOW}⊘ $repo: no changes${NC}"
                ((SKIPPED++))
            fi
        fi
    done
}

# ─────────────────────────────────────────────────────────────────
# Phase 3: Push
# ─────────────────────────────────────────────────────────────────

phase_push() {
    local repos=("$@")

    echo -e "\n${CYAN}PHASE 3: Pushing to remote${NC}"
    echo -e "${CYAN}──────────────────────────${NC}"

    for repo in "${repos[@]}"; do
        if [[ -d "$repo/.git" ]]; then
            local branch
            branch=$(cd "$repo" && git rev-parse --abbrev-ref HEAD 2>/dev/null)

            echo -n "→ Pushing $repo ($branch)... "

            if (cd "$repo" && git push origin "$branch" 2>&1 | grep -qE "Everything up-to-date|up to date"); then
                echo -e "${GREEN}✓ (up to date)${NC}"
                ((SUCCESS++))
            elif (cd "$repo" && git push origin "$branch" &>/dev/null); then
                echo -e "${GREEN}✓ (pushed)${NC}"
                ((SUCCESS++))
            else
                echo -e "${RED}✗${NC}"
                ((FAILED++))
            fi
        fi
    done
}

# ─────────────────────────────────────────────────────────────────
# Full Sync
# ─────────────────────────────────────────────────────────────────

full_sync() {
    local repos=("$@")

    phase_pull "${repos[@]}"
    phase_commit "${repos[@]}"
    phase_push "${repos[@]}"

    # Summary
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}Summary${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "Total Repos:    ${#repos[@]}"
    echo -e "Successful:     ${GREEN}${SUCCESS}${NC}"
    echo -e "Skipped:        ${YELLOW}${SKIPPED}${NC}"
    echo -e "Failed:         ${RED}${FAILED}${NC}"
}
```

### 3. Repository Status Check

Get detailed status for multiple repositories:

```bash
#!/bin/bash
# ABOUTME: Check git status across multiple repositories
# ABOUTME: Reports uncommitted, unpushed, and behind-remote states

check_repo_status() {
    local repo="$1"

    if [[ ! -d "$repo/.git" ]]; then
        echo "not_git"
        return
    fi

    cd "$repo" || return

    # Check for uncommitted changes
    if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
        echo "uncommitted"
        return
    fi

    # Check for unpushed commits
    local branch
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    local ahead
    ahead=$(git rev-list --count "origin/$branch..HEAD" 2>/dev/null || echo "0")

    if [[ "$ahead" -gt 0 ]]; then
        echo "unpushed"
        return
    fi

    # Check if behind remote
    git fetch origin "$branch" --quiet 2>/dev/null
    local behind
    behind=$(git rev-list --count "HEAD..origin/$branch" 2>/dev/null || echo "0")

    if [[ "$behind" -gt 0 ]]; then
        echo "behind"
        return
    fi

    echo "clean"
}

# Batch status check
batch_status() {
    local repos=("$@")

    printf "%-30s %-15s %s\n" "Repository" "Status" "Branch"
    printf "%s\n" "────────────────────────────────────────────────────────"

    for repo in "${repos[@]}"; do
        local status
        status=$(check_repo_status "$repo")

        local branch="N/A"
        if [[ -d "$repo/.git" ]]; then
            branch=$(cd "$repo" && git rev-parse --abbrev-ref HEAD 2>/dev/null)
        fi

        local color=""
        case "$status" in
            clean)      color="${GREEN}" ;;
            uncommitted) color="${YELLOW}" ;;
            unpushed)   color="${CYAN}" ;;
            behind)     color="${RED}" ;;
            *)          color="${NC}" ;;
        esac

        printf "%-30s ${color}%-15s${NC} %s\n" "$repo" "$status" "$branch"
    done
}
```

### 4. Category-Based Operations

Filter repositories by category (Work/Personal):

```bash
#!/bin/bash
# ABOUTME: Category-based repository filtering
# ABOUTME: Parse categories from .gitignore comments

declare -A REPO_CATEGORIES

# Parse categories from .gitignore comments
# Format: repo_name/   # Category
parse_categories() {
    local gitignore="$1"

    while IFS= read -r line; do
        if [[ "$line" =~ ^([a-zA-Z0-9_-]+)/[[:space:]]*#[[:space:]]*(Personal|Work|Both)$ ]]; then
            local name="${BASH_REMATCH[1]}"
            local category="${BASH_REMATCH[2]}"
            REPO_CATEGORIES["$name"]="$category"
        fi
    done < "$gitignore"
}

# Get repos by category
get_repos_by_category() {
    local target_category="$1"
    local repos=()

    for repo in "${!REPO_CATEGORIES[@]}"; do
        local category="${REPO_CATEGORIES[$repo]}"

        if [[ "$category" == "$target_category" ]] || \
           [[ "$target_category" == "all" ]] || \
           [[ "$category" =~ $target_category ]]; then
            repos+=("$repo")
        fi
    done

    printf '%s\n' "${repos[@]}" | sort
}

# Usage
parse_categories ".gitignore"

echo "Work repositories:"
get_repos_by_category "Work"

echo "Personal repositories:"
get_repos_by_category "Personal"
```

### 5. Safe Branch Operations

Switch branches safely across repositories:

```bash
#!/bin/bash
# ABOUTME: Safe branch switching across repositories
# ABOUTME: Validates branch existence and checks for uncommitted changes

switch_branch() {
    local repo="$1"
    local target_branch="$2"

    if [[ ! -d "$repo/.git" ]]; then
        echo "skip: not a git repo"
        return 1
    fi

    cd "$repo" || return 1

    # Check for uncommitted changes
    if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
        echo "blocked: uncommitted changes"
        return 1
    fi

    # Check if branch exists locally
    if git show-ref --verify --quiet "refs/heads/$target_branch" 2>/dev/null; then
        git checkout "$target_branch" 2>/dev/null
        echo "switched: local branch"
        return 0
    fi

    # Check if branch exists remotely
    if git show-ref --verify --quiet "refs/remotes/origin/$target_branch" 2>/dev/null; then
        git checkout -b "$target_branch" "origin/$target_branch" 2>/dev/null
        echo "switched: created from remote"
        return 0
    fi

    echo "skip: branch not found"
    return 1
}

# Batch branch switch
batch_switch_branch() {
    local target_branch="$1"
    shift
    local repos=("$@")

    echo "Switching to branch: $target_branch"
    echo ""

    for repo in "${repos[@]}"; do
        echo -n "→ $repo: "
        switch_branch "$repo" "$target_branch"
    done
}
```

## Complete Example: Repository Sync CLI

Full implementation combining all patterns:

```bash
#!/bin/bash
# ABOUTME: Complete multi-repository sync manager
# ABOUTME: Provides pull, commit, push, sync, and status operations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-$(dirname "$SCRIPT_DIR")}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ─────────────────────────────────────────────────────────────────
# Repository Discovery
# ─────────────────────────────────────────────────────────────────

declare -a REPOS=()
declare -A CATEGORIES=()

discover_repos() {
    REPOS=()

    while IFS= read -r line; do
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "$line" ]] && continue

        local repo_name="${line%%/*}"
        [[ -z "$repo_name" ]] && continue

        if [[ -d "$WORKSPACE_ROOT/$repo_name/.git" ]]; then
            REPOS+=("$repo_name")

            # Extract category from comment
            if [[ "$line" =~ #[[:space:]]*(Personal|Work|Both) ]]; then
                CATEGORIES["$repo_name"]="${BASH_REMATCH[1]}"
            fi
        fi
    done < <(grep "/" "$WORKSPACE_ROOT/.gitignore" 2>/dev/null | head -100)
}

# ─────────────────────────────────────────────────────────────────
# Operations
# ─────────────────────────────────────────────────────────────────

do_pull() {
    local repos=("$@")
    local success=0 failed=0

    for repo in "${repos[@]}"; do
        echo -n "Pulling $repo... "
        if (cd "$WORKSPACE_ROOT/$repo" && git pull --quiet 2>/dev/null); then
            echo -e "${GREEN}✓${NC}"
            ((success++))
        else
            echo -e "${YELLOW}⚠${NC}"
            ((failed++))
        fi
    done

    echo "Pull complete: $success succeeded, $failed failed"
}

do_commit() {
    local message="$1"
    shift
    local repos=("$@")
    local committed=0 skipped=0

    for repo in "${repos[@]}"; do
        if (cd "$WORKSPACE_ROOT/$repo" && ! git diff --quiet) || \
           (cd "$WORKSPACE_ROOT/$repo" && ! git diff --cached --quiet); then
            echo -n "Committing $repo... "
            if (cd "$WORKSPACE_ROOT/$repo" && git add -A && git commit -m "$message" --no-verify &>/dev/null); then
                echo -e "${GREEN}✓${NC}"
                ((committed++))
            else
                echo -e "${RED}✗${NC}"
            fi
        else
            ((skipped++))
        fi
    done

    echo "Commit complete: $committed committed, $skipped skipped (no changes)"
}

do_push() {
    local repos=("$@")
    local success=0 failed=0

    for repo in "${repos[@]}"; do
        echo -n "Pushing $repo... "
        local branch
        branch=$(cd "$WORKSPACE_ROOT/$repo" && git rev-parse --abbrev-ref HEAD)

        if (cd "$WORKSPACE_ROOT/$repo" && git push origin "$branch" --quiet 2>/dev/null); then
            echo -e "${GREEN}✓${NC}"
            ((success++))
        else
            echo -e "${RED}✗${NC}"
            ((failed++))
        fi
    done

    echo "Push complete: $success succeeded, $failed failed"
}

do_sync() {
    local message="${1:-chore: Batch sync}"
    shift
    local repos=("$@")

    echo -e "${CYAN}=== Full Sync ===${NC}"
    do_pull "${repos[@]}"
    echo ""
    do_commit "$message" "${repos[@]}"
    echo ""
    do_push "${repos[@]}"
}

do_status() {
    local repos=("$@")

    printf "%-25s %-12s %-15s %s\n" "Repository" "Category" "Status" "Branch"
    printf "%s\n" "────────────────────────────────────────────────────────────────"

    for repo in "${repos[@]}"; do
        local category="${CATEGORIES[$repo]:-Unknown}"
        local branch status

        branch=$(cd "$WORKSPACE_ROOT/$repo" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "N/A")

        if ! (cd "$WORKSPACE_ROOT/$repo" && git diff --quiet 2>/dev/null); then
            status="uncommitted"
        elif [[ $(cd "$WORKSPACE_ROOT/$repo" && git rev-list --count "origin/$branch..HEAD" 2>/dev/null || echo 0) -gt 0 ]]; then
            status="unpushed"
        else
            status="clean"
        fi

        printf "%-25s %-12s %-15s %s\n" "$repo" "$category" "$status" "$branch"
    done
}

# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

show_usage() {
    cat << EOF
Usage: $(basename "$0") <command> [scope] [options]

Commands:
    list [scope]              List repositories
    pull [scope]              Pull all repositories
    commit [scope] -m "msg"   Commit changes
    push [scope]              Push to remote
    sync [scope] -m "msg"     Full sync (pull + commit + push)
    status [scope]            Show repository status

Scope:
    all       All repositories (default)
    work      Work repositories only
    personal  Personal repositories only

Examples:
    $(basename "$0") pull all
    $(basename "$0") sync work -m "End of day sync"
    $(basename "$0") status personal

EOF
}

main() {
    local command="${1:-help}"
    local scope="${2:-all}"
    local message="chore: Batch operation"

    # Parse -m flag
    shift 2 2>/dev/null || true
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -m|--message) message="$2"; shift 2 ;;
            *) shift ;;
        esac
    done

    # Discover repos
    discover_repos

    # Filter by scope
    local filtered_repos=()
    for repo in "${REPOS[@]}"; do
        local cat="${CATEGORIES[$repo]:-Unknown}"
        case "$scope" in
            all) filtered_repos+=("$repo") ;;
            work) [[ "$cat" == "Work" || "$cat" == "Both" ]] && filtered_repos+=("$repo") ;;
            personal) [[ "$cat" == "Personal" || "$cat" == "Both" ]] && filtered_repos+=("$repo") ;;
        esac
    done

    # Execute command
    case "$command" in
        list)   printf '%s\n' "${filtered_repos[@]}" ;;
        pull)   do_pull "${filtered_repos[@]}" ;;
        commit) do_commit "$message" "${filtered_repos[@]}" ;;
        push)   do_push "${filtered_repos[@]}" ;;
        sync)   do_sync "$message" "${filtered_repos[@]}" ;;
        status) do_status "${filtered_repos[@]}" ;;
        help|*) show_usage ;;
    esac
}

main "$@"
```

## Best Practices

### 1. Always Check Before Operating
```bash
# Check for uncommitted changes before destructive operations
if ! git diff --quiet; then
    echo "Error: uncommitted changes"
    exit 1
fi
```

### 2. Use --no-verify for Batch Commits
```bash
# Skip hooks in batch operations for speed
git commit -m "message" --no-verify
```

### 3. Handle Offline/Network Errors Gracefully
```bash
# Suppress errors and provide fallback
if ! git pull --quiet 2>/dev/null; then
    echo "Warning: could not pull (offline?)"
fi
```

### 4. Track Operation Statistics
```bash
# Always maintain counters for summary
SUCCESS=0; FAILED=0; SKIPPED=0
# Update appropriately in each operation
```

### 5. Validate Git Repositories
```bash
# Always check .git directory exists
[[ -d "$repo/.git" ]] || continue
```

## Resources

- [Git Reference](https://git-scm.com/docs)
- [Bash Arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)
- [Associative Arrays in Bash](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)

---

## Version History

- **1.0.0** (2026-01-14): Initial release - extracted from workspace-hub repository sync scripts
