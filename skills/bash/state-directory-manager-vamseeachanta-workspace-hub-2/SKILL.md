---
name: state-directory-manager
version: 1.0.0
description: Manage persistent state directories for bash scripts
author: workspace-hub
category: bash
tags: [bash, state, persistence, config, directory, xdg]
platforms: [linux, macos]
---

# State Directory Manager

Patterns for managing persistent state, configuration, and cache directories in bash scripts following XDG Base Directory specification.

## When to Use This Skill

✅ **Use when:**
- Scripts need to persist data between runs
- Storing user preferences or configuration
- Caching results for performance
- Managing log files with rotation
- Creating portable CLI tools

❌ **Avoid when:**
- One-time scripts that don't need state
- Scripts that should be purely stateless
- When environment variables are sufficient

## Core Capabilities

### 1. XDG Base Directory Standard

Follow the XDG specification for directory locations:

```bash
#!/bin/bash
# ABOUTME: XDG Base Directory compliant state management
# ABOUTME: Cross-platform directory locations

# XDG Base Directories with fallbacks
XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"

# Application-specific directories
APP_NAME="my-tool"
CONFIG_DIR="$XDG_CONFIG_HOME/$APP_NAME"
DATA_DIR="$XDG_DATA_HOME/$APP_NAME"
STATE_DIR="$XDG_STATE_HOME/$APP_NAME"
CACHE_DIR="$XDG_CACHE_HOME/$APP_NAME"
LOG_DIR="$STATE_DIR/logs"

# Initialize directories
init_directories() {
    mkdir -p "$CONFIG_DIR"
    mkdir -p "$DATA_DIR"
    mkdir -p "$STATE_DIR"
    mkdir -p "$CACHE_DIR"
    mkdir -p "$LOG_DIR"
}
```

### 2. Workspace-Hub Pattern

Alternative using home directory (from workspace-hub scripts):

```bash
#!/bin/bash
# ABOUTME: Workspace-hub style state directory management
# ABOUTME: Simple $HOME/.app-name pattern

APP_NAME="workspace-hub"
APP_DIR="${HOME}/.${APP_NAME}"

# Directory structure
CONFIG_DIR="$APP_DIR/config"
DATA_DIR="$APP_DIR/data"
LOGS_DIR="$APP_DIR/logs"
CACHE_DIR="$APP_DIR/cache"
TEMP_DIR="$APP_DIR/tmp"

# Initialize with proper permissions
init_app_dirs() {
    local dirs=("$CONFIG_DIR" "$DATA_DIR" "$LOGS_DIR" "$CACHE_DIR" "$TEMP_DIR")

    for dir in "${dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            mkdir -p "$dir"
            chmod 700 "$dir"  # Private by default
        fi
    done
}

# Clean old temp files
clean_temp() {
    find "$TEMP_DIR" -type f -mtime +1 -delete 2>/dev/null || true
}
```

### 3. Configuration File Management

Read and write configuration files:

```bash
#!/bin/bash
# ABOUTME: Configuration file management
# ABOUTME: Key-value pairs with defaults

CONFIG_FILE="$CONFIG_DIR/config"

# Default configuration
declare -A DEFAULT_CONFIG=(
    ["parallel_workers"]="5"
    ["log_level"]="INFO"
    ["auto_sync"]="true"
    ["timeout"]="30"
)

# Initialize config with defaults
init_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        {
            echo "# Configuration for $APP_NAME"
            echo "# Generated: $(date)"
            echo ""
            for key in "${!DEFAULT_CONFIG[@]}"; do
                echo "${key}=${DEFAULT_CONFIG[$key]}"
            done
        } > "$CONFIG_FILE"
    fi
}

# Read config value
get_config() {
    local key="$1"
    local default="${2:-${DEFAULT_CONFIG[$key]:-}}"

    if [[ -f "$CONFIG_FILE" ]]; then
        local value
        value=$(grep "^${key}=" "$CONFIG_FILE" 2>/dev/null | cut -d'=' -f2-)
        echo "${value:-$default}"
    else
        echo "$default"
    fi
}

# Write config value
set_config() {
    local key="$1"
    local value="$2"

    init_config

    if grep -q "^${key}=" "$CONFIG_FILE" 2>/dev/null; then
        # Update existing
        sed -i "s|^${key}=.*|${key}=${value}|" "$CONFIG_FILE"
    else
        # Add new
        echo "${key}=${value}" >> "$CONFIG_FILE"
    fi
}

# Load all config into associative array
load_config() {
    declare -gA CONFIG

    # Start with defaults
    for key in "${!DEFAULT_CONFIG[@]}"; do
        CONFIG[$key]="${DEFAULT_CONFIG[$key]}"
    done

    # Override with file values
    if [[ -f "$CONFIG_FILE" ]]; then
        while IFS='=' read -r key value; do
            [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
            CONFIG[$key]="$value"
        done < "$CONFIG_FILE"
    fi
}

# Usage
init_config
load_config
echo "Parallel workers: ${CONFIG[parallel_workers]}"
set_config "parallel_workers" "10"
```

### 4. State File Operations

Track persistent state between runs:

```bash
#!/bin/bash
# ABOUTME: State file operations
# ABOUTME: Track last run, progress, etc.

STATE_FILE="$STATE_DIR/state.json"

# Initialize state
init_state() {
    if [[ ! -f "$STATE_FILE" ]]; then
        cat > "$STATE_FILE" << EOF
{
    "version": "1.0.0",
    "created": "$(date -Iseconds)",
    "last_run": null,
    "run_count": 0,
    "last_status": null
}
EOF
    fi
}

# Get state value (requires jq)
get_state() {
    local key="$1"
    local default="${2:-null}"

    if [[ -f "$STATE_FILE" ]] && command -v jq &>/dev/null; then
        jq -r ".$key // $default" "$STATE_FILE"
    else
        echo "$default"
    fi
}

# Update state value (requires jq)
set_state() {
    local key="$1"
    local value="$2"

    init_state

    if command -v jq &>/dev/null; then
        local temp=$(mktemp)
        jq ".$key = $value" "$STATE_FILE" > "$temp" && mv "$temp" "$STATE_FILE"
    fi
}

# Record run
record_run() {
    local status="$1"

    set_state "last_run" "\"$(date -Iseconds)\""
    set_state "last_status" "\"$status\""
    set_state "run_count" "$(($(get_state run_count 0) + 1))"
}

# Simple key-value state (no jq required)
STATE_KV_FILE="$STATE_DIR/state.kv"

get_state_kv() {
    local key="$1"
    local default="$2"

    if [[ -f "$STATE_KV_FILE" ]]; then
        grep "^${key}=" "$STATE_KV_FILE" 2>/dev/null | cut -d'=' -f2- || echo "$default"
    else
        echo "$default"
    fi
}

set_state_kv() {
    local key="$1"
    local value="$2"

    mkdir -p "$(dirname "$STATE_KV_FILE")"

    if [[ -f "$STATE_KV_FILE" ]] && grep -q "^${key}=" "$STATE_KV_FILE"; then
        sed -i "s|^${key}=.*|${key}=${value}|" "$STATE_KV_FILE"
    else
        echo "${key}=${value}" >> "$STATE_KV_FILE"
    fi
}
```

### 5. Cache Management

Implement caching with expiration:

```bash
#!/bin/bash
# ABOUTME: Cache management with TTL
# ABOUTME: Store and retrieve cached data

CACHE_TTL="${CACHE_TTL:-3600}"  # 1 hour default

# Get cache file path
cache_path() {
    local key="$1"
    local hash=$(echo -n "$key" | md5sum | cut -c1-16)
    echo "$CACHE_DIR/${hash}"
}

# Check if cache is valid
cache_valid() {
    local key="$1"
    local ttl="${2:-$CACHE_TTL}"
    local path=$(cache_path "$key")

    if [[ -f "$path" ]]; then
        local age=$(($(date +%s) - $(stat -c %Y "$path" 2>/dev/null || stat -f %m "$path")))
        [[ $age -lt $ttl ]]
    else
        return 1
    fi
}

# Get from cache
cache_get() {
    local key="$1"
    local ttl="${2:-$CACHE_TTL}"
    local path=$(cache_path "$key")

    if cache_valid "$key" "$ttl"; then
        cat "$path"
        return 0
    fi
    return 1
}

# Set cache
cache_set() {
    local key="$1"
    local value="$2"
    local path=$(cache_path "$key")

    mkdir -p "$CACHE_DIR"
    echo "$value" > "$path"
}

# Delete cache
cache_delete() {
    local key="$1"
    local path=$(cache_path "$key")
    rm -f "$path"
}

# Clear all cache
cache_clear() {
    rm -rf "$CACHE_DIR"/*
}

# Clean expired cache entries
cache_clean() {
    local ttl="${1:-$CACHE_TTL}"
    find "$CACHE_DIR" -type f -mmin "+$((ttl / 60))" -delete 2>/dev/null || true
}

# Usage with automatic caching
get_with_cache() {
    local key="$1"
    local command="$2"
    local ttl="${3:-$CACHE_TTL}"

    if cache_valid "$key" "$ttl"; then
        cache_get "$key"
    else
        local result
        result=$(eval "$command")
        cache_set "$key" "$result"
        echo "$result"
    fi
}

# Example
result=$(get_with_cache "api_response" "curl -s https://api.example.com/data" 300)
```

### 6. Log File Management

Manage logs with rotation:

```bash
#!/bin/bash
# ABOUTME: Log file management with rotation
# ABOUTME: Automatic cleanup of old logs

LOG_FILE="$LOG_DIR/app.log"
LOG_MAX_SIZE=$((10 * 1024 * 1024))  # 10MB
LOG_MAX_FILES=5

# Initialize logging
init_logging() {
    mkdir -p "$LOG_DIR"
    touch "$LOG_FILE"
}

# Write to log
log_to_file() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo "[$timestamp] $level: $message" >> "$LOG_FILE"

    # Check if rotation needed
    maybe_rotate_logs
}

# Rotate logs if needed
maybe_rotate_logs() {
    if [[ -f "$LOG_FILE" ]]; then
        local size=$(stat -c %s "$LOG_FILE" 2>/dev/null || stat -f %z "$LOG_FILE")

        if [[ $size -gt $LOG_MAX_SIZE ]]; then
            rotate_logs
        fi
    fi
}

# Perform log rotation
rotate_logs() {
    # Remove oldest
    rm -f "${LOG_FILE}.${LOG_MAX_FILES}"

    # Shift existing
    for ((i=LOG_MAX_FILES-1; i>=1; i--)); do
        if [[ -f "${LOG_FILE}.$i" ]]; then
            mv "${LOG_FILE}.$i" "${LOG_FILE}.$((i+1))"
        fi
    done

    # Rotate current
    if [[ -f "$LOG_FILE" ]]; then
        mv "$LOG_FILE" "${LOG_FILE}.1"
        touch "$LOG_FILE"
    fi
}

# Clean old logs
clean_old_logs() {
    local days="${1:-30}"
    find "$LOG_DIR" -name "*.log*" -mtime "+$days" -delete 2>/dev/null || true
}

# View recent logs
tail_logs() {
    local lines="${1:-50}"
    tail -n "$lines" "$LOG_FILE"
}

# Search logs
search_logs() {
    local pattern="$1"
    grep -h "$pattern" "$LOG_DIR"/*.log* 2>/dev/null | tail -100
}
```

## Complete Example: State Manager Module

```bash
#!/bin/bash
# ABOUTME: Complete state directory manager
# ABOUTME: Reusable module for bash scripts

# ─────────────────────────────────────────────────────────────────
# State Directory Manager v1.0.0
# ─────────────────────────────────────────────────────────────────

# Application identity (override in your script)
: "${STATE_APP_NAME:=my-app}"

# Directory setup
STATE_BASE_DIR="${HOME}/.${STATE_APP_NAME}"
STATE_CONFIG_DIR="$STATE_BASE_DIR/config"
STATE_DATA_DIR="$STATE_BASE_DIR/data"
STATE_CACHE_DIR="$STATE_BASE_DIR/cache"
STATE_LOG_DIR="$STATE_BASE_DIR/logs"
STATE_TMP_DIR="$STATE_BASE_DIR/tmp"

# File paths
STATE_CONFIG_FILE="$STATE_CONFIG_DIR/config"
STATE_STATE_FILE="$STATE_DATA_DIR/state"
STATE_LOG_FILE="$STATE_LOG_DIR/app.log"

# Settings
STATE_CACHE_TTL="${STATE_CACHE_TTL:-3600}"
STATE_LOG_MAX_SIZE="${STATE_LOG_MAX_SIZE:-10485760}"
STATE_LOG_MAX_FILES="${STATE_LOG_MAX_FILES:-5}"

# ─────────────────────────────────────────────────────────────────
# Initialization
# ─────────────────────────────────────────────────────────────────

state_init() {
    local dirs=(
        "$STATE_CONFIG_DIR"
        "$STATE_DATA_DIR"
        "$STATE_CACHE_DIR"
        "$STATE_LOG_DIR"
        "$STATE_TMP_DIR"
    )

    for dir in "${dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            mkdir -p "$dir"
            chmod 700 "$dir"
        fi
    done

    # Initialize files
    [[ -f "$STATE_CONFIG_FILE" ]] || touch "$STATE_CONFIG_FILE"
    [[ -f "$STATE_STATE_FILE" ]] || touch "$STATE_STATE_FILE"
    [[ -f "$STATE_LOG_FILE" ]] || touch "$STATE_LOG_FILE"
}

# ─────────────────────────────────────────────────────────────────
# Config Functions
# ─────────────────────────────────────────────────────────────────

state_config_get() {
    local key="$1"
    local default="$2"
    grep "^${key}=" "$STATE_CONFIG_FILE" 2>/dev/null | cut -d'=' -f2- || echo "$default"
}

state_config_set() {
    local key="$1"
    local value="$2"

    if grep -q "^${key}=" "$STATE_CONFIG_FILE" 2>/dev/null; then
        sed -i "s|^${key}=.*|${key}=${value}|" "$STATE_CONFIG_FILE"
    else
        echo "${key}=${value}" >> "$STATE_CONFIG_FILE"
    fi
}

state_config_list() {
    cat "$STATE_CONFIG_FILE" 2>/dev/null | grep -v '^#' | grep -v '^$'
}

# ─────────────────────────────────────────────────────────────────
# State Functions
# ─────────────────────────────────────────────────────────────────

state_get() {
    local key="$1"
    local default="$2"
    grep "^${key}=" "$STATE_STATE_FILE" 2>/dev/null | cut -d'=' -f2- || echo "$default"
}

state_set() {
    local key="$1"
    local value="$2"

    if grep -q "^${key}=" "$STATE_STATE_FILE" 2>/dev/null; then
        sed -i "s|^${key}=.*|${key}=${value}|" "$STATE_STATE_FILE"
    else
        echo "${key}=${value}" >> "$STATE_STATE_FILE"
    fi
}

# ─────────────────────────────────────────────────────────────────
# Cache Functions
# ─────────────────────────────────────────────────────────────────

state_cache_key() {
    echo -n "$1" | md5sum | cut -c1-16
}

state_cache_get() {
    local key="$1"
    local ttl="${2:-$STATE_CACHE_TTL}"
    local path="$STATE_CACHE_DIR/$(state_cache_key "$key")"

    if [[ -f "$path" ]]; then
        local age=$(($(date +%s) - $(stat -c %Y "$path" 2>/dev/null || stat -f %m "$path")))
        if [[ $age -lt $ttl ]]; then
            cat "$path"
            return 0
        fi
    fi
    return 1
}

state_cache_set() {
    local key="$1"
    local value="$2"
    local path="$STATE_CACHE_DIR/$(state_cache_key "$key")"
    echo "$value" > "$path"
}

state_cache_clear() {
    rm -rf "$STATE_CACHE_DIR"/*
}

# ─────────────────────────────────────────────────────────────────
# Log Functions
# ─────────────────────────────────────────────────────────────────

state_log() {
    local level="$1"
    shift
    local message="$*"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $level: $message" >> "$STATE_LOG_FILE"

    # Auto-rotate
    local size=$(stat -c %s "$STATE_LOG_FILE" 2>/dev/null || echo 0)
    if [[ $size -gt $STATE_LOG_MAX_SIZE ]]; then
        state_log_rotate
    fi
}

state_log_rotate() {
    rm -f "${STATE_LOG_FILE}.${STATE_LOG_MAX_FILES}"
    for ((i=STATE_LOG_MAX_FILES-1; i>=1; i--)); do
        [[ -f "${STATE_LOG_FILE}.$i" ]] && mv "${STATE_LOG_FILE}.$i" "${STATE_LOG_FILE}.$((i+1))"
    done
    mv "$STATE_LOG_FILE" "${STATE_LOG_FILE}.1"
    touch "$STATE_LOG_FILE"
}

state_log_tail() {
    tail -n "${1:-50}" "$STATE_LOG_FILE"
}

# ─────────────────────────────────────────────────────────────────
# Cleanup Functions
# ─────────────────────────────────────────────────────────────────

state_cleanup() {
    # Clean temp files older than 1 day
    find "$STATE_TMP_DIR" -type f -mtime +1 -delete 2>/dev/null || true

    # Clean expired cache
    find "$STATE_CACHE_DIR" -type f -mmin "+$((STATE_CACHE_TTL / 60))" -delete 2>/dev/null || true

    # Clean old logs
    find "$STATE_LOG_DIR" -name "*.log.*" -mtime +30 -delete 2>/dev/null || true
}

state_reset() {
    rm -rf "$STATE_BASE_DIR"
    state_init
}

# ─────────────────────────────────────────────────────────────────
# Auto-initialize
# ─────────────────────────────────────────────────────────────────

state_init
```

## Usage in Scripts

```bash
#!/bin/bash
# Your script that uses the state manager

# Set app name before sourcing
STATE_APP_NAME="my-tool"

# Source the state manager
source /path/to/state-manager.sh

# Now use it
state_config_set "api_key" "abc123"
api_key=$(state_config_get "api_key")

state_set "last_run" "$(date -Iseconds)"
state_log "INFO" "Script started"

# Use cache
if ! result=$(state_cache_get "api_response"); then
    result=$(curl -s https://api.example.com/data)
    state_cache_set "api_response" "$result"
fi
```

## Best Practices

1. **Use Standard Locations** - Follow XDG or `$HOME/.app-name`
2. **Initialize Early** - Call init before any operations
3. **Handle Permissions** - Use 700 for private data
4. **Clean Up Regularly** - Remove old temp/cache files
5. **Rotate Logs** - Prevent unbounded growth

## Resources

- [XDG Base Directory Spec](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
- [File Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)

---

## Version History

- **1.0.0** (2026-01-14): Initial release - extracted from workspace-hub patterns
