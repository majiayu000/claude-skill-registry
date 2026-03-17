---
name: defensive-bash
description: Production-grade defensive Bash scripting for server automation, monitoring, and DevOps tasks. Emphasizes safety, error handling, idempotency, and logging.
---

# Defensive Bash Scripting for Server Automation

This skill provides expertise in writing safe, reliable, and maintainable Bash scripts for server administration, Docker automation, and Moodle operations.

## Core Principles

### 1. Script Safety Headers
**ALWAYS** start scripts with:
```bash
#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
```

Explanation:
- `set -e`: Exit on any error
- `set -u`: Exit on undefined variable
- `set -o pipefail`: Fail if any command in a pipeline fails
- `IFS`: Prevent word splitting issues

### 2. Error Handling
**ALWAYS** implement proper error handling:

```bash
# Error handler function
error_exit() {
    echo "ERROR: $1" >&2
    echo "Line: ${BASH_LINENO[0]}, Function: ${FUNCNAME[1]}" >&2
    exit "${2:-1}"
}

# Trap errors
trap 'error_exit "Script failed at line $LINENO"' ERR

# Usage
some_command || error_exit "Command failed" 1
```

### 3. Input Validation
**ALWAYS** validate inputs:

```bash
# Check arguments
if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <argument>" >&2
    exit 1
fi

# Validate argument types
if ! [[ "$1" =~ ^[0-9]+$ ]]; then
    error_exit "Argument must be a number"
fi

# Check file/directory existence
if [[ ! -f "$CONFIG_FILE" ]]; then
    error_exit "Config file not found: $CONFIG_FILE"
fi
```

### 4. Safe File Operations
**ALWAYS** use safe file handling:

```bash
# Create temporary files safely
readonly TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

# Backup before modifying
backup_file() {
    local file="$1"
    local backup="${file}.backup.$(date +%Y%m%d_%H%M%S)"
    cp -a "$file" "$backup" || error_exit "Backup failed for $file"
    echo "$backup"
}

# Atomic writes
atomic_write() {
    local content="$1"
    local target="$2"
    local tmpfile="${target}.tmp.$$"

    echo "$content" > "$tmpfile" || error_exit "Write failed"
    mv "$tmpfile" "$target" || error_exit "Atomic move failed"
}
```

### 5. Logging
**ALWAYS** implement comprehensive logging:

```bash
# Logging setup
readonly LOG_FILE="/var/log/$(basename "$0" .sh).log"
readonly LOG_LEVEL="${LOG_LEVEL:-INFO}"

log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"

    echo "[${timestamp}] [${level}] ${message}" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }
log_debug() { [[ "$LOG_LEVEL" == "DEBUG" ]] && log "DEBUG" "$@"; }
```

### 6. Idempotency
**ALWAYS** make operations idempotent:

```bash
# Check before creating
if [[ ! -d "$TARGET_DIR" ]]; then
    mkdir -p "$TARGET_DIR"
    log_info "Created directory: $TARGET_DIR"
else
    log_debug "Directory already exists: $TARGET_DIR"
fi

# Safe service restart
restart_service() {
    local service="$1"

    if systemctl is-active --quiet "$service"; then
        systemctl restart "$service"
        log_info "Restarted service: $service"
    else
        systemctl start "$service"
        log_info "Started service: $service"
    fi
}
```

### 7. Signal Handling
**ALWAYS** handle signals gracefully:

```bash
# Cleanup function
cleanup() {
    local exit_code=$?
    log_info "Cleaning up (exit code: $exit_code)..."

    # Cleanup operations
    [[ -d "$TMPDIR" ]] && rm -rf "$TMPDIR"
    [[ -n "$LOCKFILE" ]] && rm -f "$LOCKFILE"

    log_info "Cleanup complete"
    exit "$exit_code"
}

# Trap signals
trap cleanup EXIT
trap 'log_warn "Received SIGINT, exiting..."; exit 130' INT
trap 'log_warn "Received SIGTERM, exiting..."; exit 143' TERM
```

### 8. Locking Mechanism
**ALWAYS** prevent concurrent execution:

```bash
# Lock file management
readonly LOCKFILE="/var/run/$(basename "$0" .sh).lock"

acquire_lock() {
    if [[ -f "$LOCKFILE" ]]; then
        local pid
        pid=$(<"$LOCKFILE")
        if kill -0 "$pid" 2>/dev/null; then
            error_exit "Script already running (PID: $pid)"
        else
            log_warn "Removing stale lock file"
            rm -f "$LOCKFILE"
        fi
    fi

    echo $$ > "$LOCKFILE"
}

release_lock() {
    rm -f "$LOCKFILE"
}

trap release_lock EXIT
acquire_lock
```

## Docker-Specific Patterns

### Safe Container Execution
```bash
# Execute command in container with error handling
docker_exec() {
    local container="$1"
    shift
    local cmd="$*"

    if ! docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        error_exit "Container not running: $container"
    fi

    log_debug "Executing in $container: $cmd"
    docker exec "$container" bash -c "$cmd" || {
        error_exit "Command failed in container $container: $cmd"
    }
}

# Wait for container to be healthy
wait_for_container() {
    local container="$1"
    local timeout="${2:-60}"
    local elapsed=0

    log_info "Waiting for container: $container"

    while [[ $elapsed -lt $timeout ]]; do
        if docker ps --filter "name=${container}" --filter "status=running" | grep -q "$container"; then
            log_info "Container ready: $container"
            return 0
        fi
        sleep 2
        ((elapsed += 2))
    done

    error_exit "Container failed to start: $container"
}
```

### Service Health Checks
```bash
# Check service availability
check_service() {
    local service="$1"
    local container="${2:-moodle-dev}"

    log_debug "Checking service: $service in $container"

    if docker_exec "$container" "systemctl is-active --quiet $service"; then
        log_info "Service running: $service"
        return 0
    else
        log_error "Service not running: $service"
        return 1
    fi
}

# HTTP endpoint check
check_http() {
    local url="$1"
    local expected_code="${2:-200}"

    log_debug "Checking HTTP: $url"

    local response_code
    response_code=$(curl -s -o /dev/null -w '%{http_code}' "$url" || echo "000")

    if [[ "$response_code" == "$expected_code" ]]; then
        log_info "HTTP check passed: $url ($response_code)"
        return 0
    else
        log_error "HTTP check failed: $url (got $response_code, expected $expected_code)"
        return 1
    fi
}
```

## Moodle-Specific Patterns

### Multi-Version Moodle Operations
```bash
# Execute Moodle CLI across versions
moodle_cli() {
    local version="$1"
    local script="$2"
    shift 2
    local args="$*"

    local php_cmd moodle_dir

    case "$version" in
        "4.1")
            php_cmd="php8.1"
            moodle_dir="/opt/moodle-MOODLE_401_STABLE"
            ;;
        "4.5")
            php_cmd="php8.2"
            moodle_dir="/opt/moodle-MOODLE_405_STABLE"
            ;;
        "5.1")
            php_cmd="php8.3"
            moodle_dir="/opt/moodle-MOODLE_501_STABLE"
            ;;
        "dh-prod")
            php_cmd="php8.1"
            moodle_dir="/workspace/moodle-dh-prod"
            ;;
        *)
            error_exit "Invalid Moodle version: $version"
            ;;
    esac

    local full_script="${moodle_dir}/admin/cli/${script}"

    if [[ ! -f "$full_script" ]]; then
        error_exit "Script not found: $full_script"
    fi

    log_info "Running Moodle $version: $script $args"
    docker_exec moodle-dev "$php_cmd $full_script $args"
}

# Purge all caches
purge_all_caches() {
    local versions=("4.1" "4.5" "5.1" "dh-prod")

    for version in "${versions[@]}"; do
        log_info "Purging cache for Moodle $version"
        moodle_cli "$version" "purge_caches.php" || log_error "Cache purge failed for $version"
    done
}
```

## Best Practices Summary

1. **Always use `set -euo pipefail`** at script start
2. **Validate all inputs** before using them
3. **Log all significant actions** with timestamps
4. **Handle errors explicitly** with meaningful messages
5. **Make operations idempotent** when possible
6. **Clean up resources** in trap handlers
7. **Use locks** for critical sections
8. **Test before production** use
9. **Document assumptions** and requirements
10. **Version control** all scripts

## Common Anti-Patterns to Avoid

❌ **Don't:**
```bash
# No error checking
docker exec moodle-dev php script.php

# Unquoted variables
file=$1
cat $file

# Ignoring errors
command || true

# No validation
rm -rf $DIR/*
```

✅ **Do:**
```bash
# Proper error checking
docker_exec moodle-dev "php script.php" || error_exit "PHP script failed"

# Quoted variables
file="$1"
cat "$file"

# Explicit error handling
command || {
    log_error "Command failed"
    return 1
}

# Validation before destructive operations
if [[ -z "$DIR" ]] || [[ ! -d "$DIR" ]]; then
    error_exit "Invalid directory: $DIR"
fi
rm -rf "${DIR:?}/"*
```

## Testing Scripts

Always test with:
```bash
# ShellCheck static analysis
shellcheck script.sh

# Bash strict mode
bash -n script.sh  # Syntax check

# Debug mode
bash -x script.sh  # Trace execution

# Test with invalid inputs
./script.sh ""
./script.sh "../../etc/passwd"
./script.sh "$(printf '\0')"
```

Apply these patterns consistently for reliable, maintainable server automation scripts.
