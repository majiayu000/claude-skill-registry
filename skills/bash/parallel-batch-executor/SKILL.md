---
name: parallel-batch-executor
version: 1.0.0
description: Parallel task execution patterns for 300% performance gains
author: workspace-hub
category: bash
tags: [bash, parallel, xargs, performance, batch, optimization]
platforms: [linux, macos]
---

# Parallel Batch Executor

Patterns for executing tasks in parallel using bash, delivering up to 300% performance improvements. Extracted from workspace-hub's batchtools and orchestration scripts.

## When to Use This Skill

✅ **Use when:**
- Processing multiple independent files or items
- Running the same operation across multiple repositories
- Batch operations that don't depend on each other
- Need significant performance improvements
- Operations are I/O bound rather than CPU bound

❌ **Avoid when:**
- Tasks have dependencies on each other
- Order of execution matters
- Shared resources require synchronization
- Single task that can't be parallelized

## Core Capabilities

### 1. Basic Parallel Execution with xargs

The fundamental pattern for parallel execution:

```bash
#!/bin/bash
# ABOUTME: Basic parallel execution using xargs
# ABOUTME: Process multiple items concurrently with controlled parallelism

PARALLEL="${PARALLEL:-5}"  # Default to 5 parallel workers

# Process items from stdin in parallel
cat items.txt | xargs -I {} -P "$PARALLEL" bash -c 'echo "Processing: {}"'

# Process with error handling
cat items.txt | xargs -I {} -P "$PARALLEL" bash -c '
    item="{}"
    if process_item "$item"; then
        echo "✓ $item"
    else
        echo "✗ $item" >&2
    fi
'
```

### 2. JSON Array Processing

Process JSON arrays in parallel (from batch_runner.sh):

```bash
#!/bin/bash
# ABOUTME: Process JSON array items in parallel
# ABOUTME: Uses jq for parsing and xargs for parallel execution

set -e

PARALLEL="${1:-5}"
ORCHESTRATOR="./scripts/routing/orchestrate.sh"

# Check dependencies
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed."
    exit 1
fi

echo "Starting batch execution with $PARALLEL parallel workers..."

# Read JSON array from stdin, extract items, process in parallel
jq -r '.[]' | xargs -I {} -P "$PARALLEL" bash -c "$ORCHESTRATOR \"{}\" > /dev/null"

echo "Batch execution complete."
```

### 3. Repository Batch Operations

Execute commands across multiple repositories:

```bash
#!/bin/bash
# ABOUTME: Execute operations across multiple repositories in parallel
# ABOUTME: Pattern from workspace-hub repository_sync

PARALLEL="${PARALLEL:-5}"
REPOS_DIR="/mnt/github"

# Get list of repositories
get_repos() {
    find "$REPOS_DIR" -maxdepth 1 -type d -name "[!.]*" | sort
}

# Execute command in each repository in parallel
batch_repo_command() {
    local command="$1"
    local repos
    repos=$(get_repos)

    echo "$repos" | xargs -I {} -P "$PARALLEL" bash -c "
        repo=\"{}\"
        repo_name=\$(basename \"\$repo\")

        if cd \"\$repo\" 2>/dev/null; then
            result=\$($command 2>&1)
            exit_code=\$?

            if [[ \$exit_code -eq 0 ]]; then
                echo \"✓ \$repo_name: \$result\"
            else
                echo \"✗ \$repo_name: \$result\" >&2
            fi
        else
            echo \"⊘ \$repo_name: Directory not accessible\" >&2
        fi
    "
}

# Usage examples
batch_repo_command "git status --porcelain | head -1"
batch_repo_command "git pull --rebase"
batch_repo_command "git push"
```

### 4. Progress Tracking

Track progress during parallel execution:

```bash
#!/bin/bash
# ABOUTME: Parallel execution with progress tracking
# ABOUTME: Shows real-time progress and summary statistics

PARALLEL="${PARALLEL:-5}"
PROGRESS_FILE=$(mktemp)
TOTAL=0
SUCCESS=0
FAILED=0

# Initialize progress file
echo "0" > "$PROGRESS_FILE"

# Track progress atomically
track_progress() {
    local status="$1"
    local item="$2"

    # Use flock for atomic updates
    (
        flock -x 200
        local current=$(cat "$PROGRESS_FILE")
        echo $((current + 1)) > "$PROGRESS_FILE"

        if [[ "$status" == "success" ]]; then
            echo "S" >> "${PROGRESS_FILE}.status"
        else
            echo "F" >> "${PROGRESS_FILE}.status"
        fi
    ) 200>"${PROGRESS_FILE}.lock"
}

process_with_tracking() {
    local items=("$@")
    local total=${#items[@]}

    echo "Processing $total items with $PARALLEL workers..."
    echo ""

    printf '%s\n' "${items[@]}" | xargs -I {} -P "$PARALLEL" bash -c "
        item=\"{}\"

        # Process item
        if process_item \"\$item\" 2>/dev/null; then
            echo \"success \$item\"
        else
            echo \"failed \$item\"
        fi
    " | while read status item; do
        track_progress "$status" "$item"

        local current=$(cat "$PROGRESS_FILE")
        local pct=$((current * 100 / total))

        # Update progress line
        printf \"\\r[%3d%%] Processed %d/%d items\" \$pct \$current \$total
    done

    echo ""
    echo "Complete!"

    # Show summary
    local success=$(grep -c "S" "${PROGRESS_FILE}.status" 2>/dev/null || echo 0)
    local failed=$(grep -c "F" "${PROGRESS_FILE}.status" 2>/dev/null || echo 0)
    echo "Success: $success, Failed: $failed"

    # Cleanup
    rm -f "$PROGRESS_FILE" "${PROGRESS_FILE}.lock" "${PROGRESS_FILE}.status"
}
```

### 5. Error Collection

Collect and report errors from parallel execution:

```bash
#!/bin/bash
# ABOUTME: Parallel execution with centralized error collection
# ABOUTME: Aggregates errors for reporting after batch completion

ERROR_LOG=$(mktemp)
SUCCESS_LOG=$(mktemp)

cleanup() {
    rm -f "$ERROR_LOG" "$SUCCESS_LOG"
}
trap cleanup EXIT

parallel_with_errors() {
    local command="$1"
    shift
    local items=("$@")

    printf '%s\n' "${items[@]}" | xargs -I {} -P "$PARALLEL" bash -c "
        item=\"{}\"
        output=\$($command \"\$item\" 2>&1)
        exit_code=\$?

        if [[ \$exit_code -eq 0 ]]; then
            echo \"\$item\" >> \"$SUCCESS_LOG\"
        else
            echo \"\$item: \$output\" >> \"$ERROR_LOG\"
        fi
    "

    # Report results
    local success_count=$(wc -l < "$SUCCESS_LOG" 2>/dev/null || echo 0)
    local error_count=$(wc -l < "$ERROR_LOG" 2>/dev/null || echo 0)

    echo ""
    echo "Results: $success_count succeeded, $error_count failed"

    if [[ $error_count -gt 0 ]]; then
        echo ""
        echo "Errors:"
        cat "$ERROR_LOG" | while read line; do
            echo "  ✗ $line"
        done
        return 1
    fi

    return 0
}
```

### 6. GNU Parallel Alternative

For more advanced parallelism:

```bash
#!/bin/bash
# ABOUTME: Advanced parallel execution using GNU Parallel
# ABOUTME: Provides job control, logging, and resume capabilities

# Check for GNU Parallel
if command -v parallel &> /dev/null; then
    USE_GNU_PARALLEL=true
else
    USE_GNU_PARALLEL=false
fi

parallel_execute() {
    local command="$1"
    local jobs="${2:-5}"

    if [[ "$USE_GNU_PARALLEL" == true ]]; then
        # GNU Parallel with job log
        parallel --jobs "$jobs" \
                 --joblog /tmp/parallel_joblog.txt \
                 --bar \
                 "$command" {}
    else
        # Fallback to xargs
        xargs -I {} -P "$jobs" bash -c "$command \"{}\""
    fi
}

# Usage
cat files.txt | parallel_execute "process_file" 10
```

## Complete Example: Batch Task Runner

Full implementation from workspace-hub:

```bash
#!/bin/bash
# ABOUTME: Batch Task Executor
# ABOUTME: Executes tasks in parallel using the Multi-Provider Orchestrator

set -e

# ─────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORCHESTRATOR="$SCRIPT_DIR/../routing/orchestrate.sh"
PARALLEL=1
LOG_DIR="$SCRIPT_DIR/logs"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ─────────────────────────────────────────────────────────────────
# Functions
# ─────────────────────────────────────────────────────────────────

log_info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }
die()       { log_error "$1"; exit 1; }

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS] < tasks.json

Executes tasks in parallel using the Multi-Provider Orchestrator.

Options:
    --parallel N    Number of parallel workers (default: 1)
    --log-dir DIR   Directory for logs (default: ./logs)
    -h, --help      Show this help

Input Format:
    JSON array of task descriptions from stdin.
    Example: ["task 1", "task 2", "task 3"]

Examples:
    echo '["Build project", "Run tests"]' | $0 --parallel 2
    cat tasks.json | $0 --parallel 5

EOF
}

# ─────────────────────────────────────────────────────────────────
# Argument Parsing
# ─────────────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
    case $1 in
        --parallel)
            PARALLEL="$2"
            shift 2
            ;;
        --log-dir)
            LOG_DIR="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            die "Unknown option: $1"
            ;;
    esac
done

# ─────────────────────────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────────────────────────

[[ -f "$ORCHESTRATOR" ]] || die "Orchestrator not found: $ORCHESTRATOR"
command -v jq &> /dev/null || die "jq is required but not installed"

mkdir -p "$LOG_DIR"

# ─────────────────────────────────────────────────────────────────
# Main Execution
# ─────────────────────────────────────────────────────────────────

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}  Batch Task Executor${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""

log_info "Starting batch execution with $PARALLEL parallel workers..."
log_info "Logs directory: $LOG_DIR"
echo ""

# Statistics
START_TIME=$(date +%s)
TASK_COUNT=0
SUCCESS_COUNT=0
FAIL_COUNT=0

# Create temporary files for tracking
SUCCESS_FILE=$(mktemp)
FAIL_FILE=$(mktemp)

cleanup() {
    rm -f "$SUCCESS_FILE" "$FAIL_FILE"
}
trap cleanup EXIT

# Read JSON and process in parallel
jq -r '.[]' | while read -r task; do
    TASK_COUNT=$((TASK_COUNT + 1))
done

# Reset and process
jq -r '.[]' | xargs -I {} -P "$PARALLEL" bash -c "
    task=\"{}\"
    task_hash=\$(echo \"\$task\" | md5sum | cut -c1-8)
    log_file=\"$LOG_DIR/task_\${task_hash}.log\"

    echo \"[START] \$task\" > \"\$log_file\"

    if \"$ORCHESTRATOR\" \"\$task\" >> \"\$log_file\" 2>&1; then
        echo \"SUCCESS\" >> \"$SUCCESS_FILE\"
        echo -e \"${GREEN}✓${NC} \$task\"
    else
        echo \"FAIL\" >> \"$FAIL_FILE\"
        echo -e \"${RED}✗${NC} \$task\"
    fi
"

# Calculate statistics
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
SUCCESS_COUNT=$(wc -l < "$SUCCESS_FILE" 2>/dev/null || echo 0)
FAIL_COUNT=$(wc -l < "$FAIL_FILE" 2>/dev/null || echo 0)
TOTAL=$((SUCCESS_COUNT + FAIL_COUNT))

# Summary
echo ""
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}  Execution Summary${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""
echo "Total tasks:    $TOTAL"
echo "Successful:     $SUCCESS_COUNT"
echo "Failed:         $FAIL_COUNT"
echo "Duration:       ${DURATION}s"
echo "Logs:           $LOG_DIR"
echo ""

[[ $FAIL_COUNT -eq 0 ]] && log_info "All tasks completed successfully!" || log_error "$FAIL_COUNT tasks failed"

exit $([[ $FAIL_COUNT -eq 0 ]] && echo 0 || echo 1)
```

## Performance Tuning

### Optimal Parallelism

```bash
# CPU-bound tasks: match CPU cores
PARALLEL=$(nproc)

# I/O-bound tasks: 2-4x CPU cores
PARALLEL=$(($(nproc) * 2))

# Network-bound tasks: higher parallelism
PARALLEL=20

# Memory-constrained: limit based on available RAM
AVAILABLE_MB=$(free -m | awk '/^Mem:/{print $7}')
TASK_MB=100  # Estimate per task
PARALLEL=$((AVAILABLE_MB / TASK_MB))
```

### Throttling

```bash
# Add delay between task starts
printf '%s\n' "${items[@]}" | xargs -I {} -P "$PARALLEL" bash -c "
    sleep 0.1  # 100ms delay
    process_item \"{}\"
"
```

## Best Practices

### 1. Always Set a Default
```bash
PARALLEL="${PARALLEL:-5}"
```

### 2. Validate Input
```bash
[[ $PARALLEL -gt 0 ]] || die "Parallelism must be positive"
[[ $PARALLEL -le 50 ]] || log_warning "High parallelism may overwhelm system"
```

### 3. Handle Failures Gracefully
```bash
# Don't use set -e with xargs - it will mask failures
# Instead, track failures explicitly
```

### 4. Log Everything
```bash
# Create per-task logs for debugging
log_file="$LOG_DIR/task_$(date +%s)_$$.log"
```

### 5. Clean Up Resources
```bash
trap cleanup EXIT INT TERM
```

## Resources

- [GNU xargs Manual](https://www.gnu.org/software/findutils/manual/html_node/find_html/xargs-options.html)
- [GNU Parallel Tutorial](https://www.gnu.org/software/parallel/parallel_tutorial.html)
- [Bash Process Substitution](https://mywiki.wooledge.org/ProcessSubstitution)

---

## Version History

- **1.0.0** (2026-01-14): Initial release - extracted from workspace-hub batchtools
