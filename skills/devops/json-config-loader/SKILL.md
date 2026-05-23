---
name: json-config-loader
version: 1.0.0
description: Configuration file parsing patterns for bash scripts (INI, key=value, JSON)
author: workspace-hub
category: bash
tags: [bash, config, json, yaml, parsing, jq, configuration]
platforms: [linux, macos]
---

# JSON & Config Loader

Patterns for loading, parsing, and generating configuration files in bash scripts. Supports key=value files, JSON with jq, and associative array management. Extracted from workspace-hub's configuration scripts.

## When to Use This Skill

✅ **Use when:**
- Loading configuration from files into bash scripts
- Parsing key=value or INI-style configuration files
- Working with JSON data using jq
- Generating JSON reports from bash
- Managing configuration with associative arrays

❌ **Avoid when:**
- Complex nested configuration (consider Python instead)
- Real-time configuration changes (use a daemon)
- Configuration with complex validation rules

## Core Capabilities

### 1. Key=Value Configuration Parsing

Parse simple key=value configuration files:

```bash
#!/bin/bash
# ABOUTME: Parse key=value configuration files
# ABOUTME: Supports comments, empty lines, and quoted values

CONFIG_FILE="${1:-config.conf}"

# Declare associative array for config
declare -A CONFIG

# Parse configuration file
parse_config() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        echo "Error: Config file not found: $file" >&2
        return 1
    fi

    while IFS= read -r line || [[ -n "$line" ]]; do
        # Skip comments and empty lines
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "${line// /}" ]] && continue

        # Parse key=value pairs
        if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
            local key="${BASH_REMATCH[1]}"
            local value="${BASH_REMATCH[2]}"

            # Trim whitespace
            key="${key#"${key%%[![:space:]]*}"}"
            key="${key%"${key##*[![:space:]]}"}"
            value="${value#"${value%%[![:space:]]*}"}"
            value="${value%"${value##*[![:space:]]}"}"

            # Remove surrounding quotes if present
            if [[ "$value" =~ ^\"(.*)\"$ ]] || [[ "$value" =~ ^\'(.*)\'$ ]]; then
                value="${BASH_REMATCH[1]}"
            fi

            CONFIG["$key"]="$value"
        fi
    done < "$file"
}

# Get config value with default
get_config() {
    local key="$1"
    local default="${2:-}"

    echo "${CONFIG[$key]:-$default}"
}

# Check if key exists
has_config() {
    local key="$1"
    [[ -v CONFIG[$key] ]]
}

# Usage
parse_config "$CONFIG_FILE"

# Access values
echo "Database: $(get_config 'database' 'default.db')"
echo "Port: $(get_config 'port' '8080')"

if has_config 'debug'; then
    echo "Debug mode enabled"
fi
```

### 2. JSON Configuration with jq

Load and manipulate JSON configuration:

```bash
#!/bin/bash
# ABOUTME: JSON configuration loading with jq
# ABOUTME: Provides safe defaults and nested value access

# Check jq dependency
check_jq() {
    if ! command -v jq &> /dev/null; then
        echo "Error: jq is required but not installed" >&2
        echo "Install with: apt install jq (Ubuntu) or brew install jq (Mac)" >&2
        exit 1
    fi
}

# Load JSON config file
load_json_config() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        echo "{}"
        return 1
    fi

    # Validate JSON
    if ! jq empty "$file" 2>/dev/null; then
        echo "Error: Invalid JSON in $file" >&2
        echo "{}"
        return 1
    fi

    cat "$file"
}

# Get value from JSON with default
json_get() {
    local json="$1"
    local path="$2"
    local default="${3:-}"

    local value
    value=$(echo "$json" | jq -r "$path // empty" 2>/dev/null)

    if [[ -z "$value" || "$value" == "null" ]]; then
        echo "$default"
    else
        echo "$value"
    fi
}

# Get array from JSON
json_get_array() {
    local json="$1"
    local path="$2"

    echo "$json" | jq -r "$path[]? // empty" 2>/dev/null
}

# Check if path exists in JSON
json_has() {
    local json="$1"
    local path="$2"

    local result
    result=$(echo "$json" | jq -e "$path != null" 2>/dev/null)
    [[ "$result" == "true" ]]
}

# Usage example
check_jq

CONFIG_JSON=$(load_json_config "config.json")

# Access nested values
DB_HOST=$(json_get "$CONFIG_JSON" '.database.host' 'localhost')
DB_PORT=$(json_get "$CONFIG_JSON" '.database.port' '5432')
DEBUG=$(json_get "$CONFIG_JSON" '.settings.debug' 'false')

echo "Database: $DB_HOST:$DB_PORT"
echo "Debug: $DEBUG"

# Iterate array values
echo "Enabled features:"
while IFS= read -r feature; do
    echo "  - $feature"
done < <(json_get_array "$CONFIG_JSON" '.features')
```

### 3. JSON Report Generation

Generate structured JSON reports:

```bash
#!/bin/bash
# ABOUTME: Generate JSON reports from bash data
# ABOUTME: Uses jq for proper JSON encoding and structure

# Generate simple JSON object
generate_json_object() {
    local -n data=$1  # Nameref to associative array

    local json="{}"

    for key in "${!data[@]}"; do
        local value="${data[$key]}"
        json=$(echo "$json" | jq --arg k "$key" --arg v "$value" '. + {($k): $v}')
    done

    echo "$json"
}

# Generate JSON report with structure
generate_report() {
    local status="$1"
    local total="$2"
    local errors="$3"
    local warnings="$4"

    jq -n \
        --arg status "$status" \
        --arg timestamp "$(date -Iseconds)" \
        --arg run_id "$(date +%Y%m%d-%H%M%S)" \
        --argjson total "$total" \
        --argjson errors "$errors" \
        --argjson warnings "$warnings" \
        '{
            metadata: {
                status: $status,
                timestamp: $timestamp,
                run_id: $run_id
            },
            summary: {
                total_processed: $total,
                errors: $errors,
                warnings: $warnings,
                success_rate: (if $total > 0 then (($total - $errors) * 100 / $total) else 0 end)
            }
        }'
}

# Add items to JSON report
add_report_items() {
    local report="$1"
    shift
    local items=("$@")

    # Convert items array to JSON array
    local items_json="[]"
    for item in "${items[@]}"; do
        items_json=$(echo "$items_json" | jq --arg i "$item" '. + [$i]')
    done

    echo "$report" | jq --argjson items "$items_json" '. + {items: $items}'
}

# Save report to file
save_report() {
    local report="$1"
    local file="$2"

    mkdir -p "$(dirname "$file")"
    echo "$report" | jq '.' > "$file"

    echo "Report saved: $file"
}

# Usage
report=$(generate_report "success" 100 5 10)
report=$(add_report_items "$report" "item1" "item2" "item3")
save_report "$report" "reports/analysis-$(date +%Y%m%d).json"
```

### 4. Multi-Section INI Parsing

Parse INI-style files with sections:

```bash
#!/bin/bash
# ABOUTME: Parse INI-style configuration with sections
# ABOUTME: Supports [section] headers and section.key access

declare -A INI_CONFIG
declare -a INI_SECTIONS=()

parse_ini() {
    local file="$1"
    local current_section="default"

    if [[ ! -f "$file" ]]; then
        echo "Error: INI file not found: $file" >&2
        return 1
    fi

    INI_SECTIONS=("default")

    while IFS= read -r line || [[ -n "$line" ]]; do
        # Skip comments and empty lines
        [[ "$line" =~ ^[[:space:]]*[#\;] ]] && continue
        [[ -z "${line// /}" ]] && continue

        # Section header
        if [[ "$line" =~ ^\[([^\]]+)\] ]]; then
            current_section="${BASH_REMATCH[1]}"
            INI_SECTIONS+=("$current_section")
            continue
        fi

        # Key=value within section
        if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
            local key="${BASH_REMATCH[1]}"
            local value="${BASH_REMATCH[2]}"

            # Trim whitespace
            key="${key#"${key%%[![:space:]]*}"}"
            key="${key%"${key##*[![:space:]]}"}"
            value="${value#"${value%%[![:space:]]*}"}"
            value="${value%"${value##*[![:space:]]}"}"

            # Store as section.key
            INI_CONFIG["${current_section}.${key}"]="$value"
        fi
    done < "$file"
}

# Get INI value
ini_get() {
    local section="$1"
    local key="$2"
    local default="${3:-}"

    echo "${INI_CONFIG["${section}.${key}"]:-$default}"
}

# Get all keys in a section
ini_section_keys() {
    local section="$1"
    local prefix="${section}."

    for key in "${!INI_CONFIG[@]}"; do
        if [[ "$key" == "${prefix}"* ]]; then
            echo "${key#$prefix}"
        fi
    done
}

# List all sections
ini_sections() {
    printf '%s\n' "${INI_SECTIONS[@]}" | sort -u
}

# Usage
parse_ini "settings.ini"

# Access values
DB_HOST=$(ini_get "database" "host" "localhost")
DB_PORT=$(ini_get "database" "port" "5432")
LOG_LEVEL=$(ini_get "logging" "level" "INFO")

echo "Database: $DB_HOST:$DB_PORT"
echo "Log Level: $LOG_LEVEL"

# Iterate section keys
echo "Database settings:"
for key in $(ini_section_keys "database"); do
    echo "  $key = $(ini_get "database" "$key")"
done
```

### 5. Environment Variable Configuration

Load configuration with environment variable overrides:

```bash
#!/bin/bash
# ABOUTME: Configuration with environment variable overrides
# ABOUTME: File config < Environment variable precedence

declare -A APP_CONFIG

# Load config with env override support
load_config_with_env() {
    local file="$1"
    local prefix="${2:-APP_}"  # Environment variable prefix

    # First load from file
    if [[ -f "$file" ]]; then
        while IFS= read -r line || [[ -n "$line" ]]; do
            [[ "$line" =~ ^[[:space:]]*# ]] && continue
            [[ -z "${line// /}" ]] && continue

            if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
                local key="${BASH_REMATCH[1]}"
                local value="${BASH_REMATCH[2]}"

                key="${key#"${key%%[![:space:]]*}"}"
                key="${key%"${key##*[![:space:]]}"}"

                APP_CONFIG["$key"]="$value"
            fi
        done < "$file"
    fi

    # Override with environment variables
    for key in "${!APP_CONFIG[@]}"; do
        local env_key="${prefix}${key^^}"  # Convert to UPPER_CASE
        env_key="${env_key//-/_}"          # Replace - with _

        if [[ -v "$env_key" ]]; then
            APP_CONFIG["$key"]="${!env_key}"
        fi
    done
}

# Check required config keys
require_config() {
    local missing=()

    for key in "$@"; do
        if [[ -z "${APP_CONFIG[$key]:-}" ]]; then
            missing+=("$key")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "Error: Missing required configuration:" >&2
        printf "  - %s\n" "${missing[@]}" >&2
        return 1
    fi

    return 0
}

# Get config with type conversion
config_string() {
    local key="$1"
    local default="${2:-}"
    echo "${APP_CONFIG[$key]:-$default}"
}

config_int() {
    local key="$1"
    local default="${2:-0}"
    local value="${APP_CONFIG[$key]:-$default}"

    if [[ "$value" =~ ^-?[0-9]+$ ]]; then
        echo "$value"
    else
        echo "$default"
    fi
}

config_bool() {
    local key="$1"
    local default="${2:-false}"
    local value="${APP_CONFIG[$key]:-$default}"

    case "${value,,}" in
        true|yes|1|on) echo "true" ;;
        false|no|0|off) echo "false" ;;
        *) echo "$default" ;;
    esac
}

# Usage
load_config_with_env "app.conf" "MYAPP_"

# Check required keys
require_config "api_key" "database_url" || exit 1

# Access with type conversion
PORT=$(config_int "port" 8080)
DEBUG=$(config_bool "debug" false)
API_KEY=$(config_string "api_key")

echo "Starting on port $PORT (debug: $DEBUG)"
```

### 6. YAML Configuration (via yq)

Parse YAML files when yq is available:

```bash
#!/bin/bash
# ABOUTME: YAML configuration parsing with yq
# ABOUTME: Falls back to jq for JSON subset of YAML

# Check for yaml parser
get_yaml_parser() {
    if command -v yq &> /dev/null; then
        echo "yq"
    elif command -v jq &> /dev/null; then
        echo "jq"  # Can parse YAML's JSON subset
    else
        echo "none"
    fi
}

# Load YAML config
load_yaml_config() {
    local file="$1"
    local parser
    parser=$(get_yaml_parser)

    if [[ ! -f "$file" ]]; then
        echo "{}"
        return 1
    fi

    case "$parser" in
        yq)
            yq -o=json "$file" 2>/dev/null || echo "{}"
            ;;
        jq)
            # Try to parse as JSON (YAML subset)
            jq '.' "$file" 2>/dev/null || echo "{}"
            ;;
        *)
            echo "Error: No YAML parser available (install yq or jq)" >&2
            echo "{}"
            return 1
            ;;
    esac
}

# Get YAML value (returns as JSON for jq processing)
yaml_get() {
    local file="$1"
    local path="$2"
    local default="${3:-}"

    local parser
    parser=$(get_yaml_parser)

    local value
    case "$parser" in
        yq)
            value=$(yq -r "$path // \"$default\"" "$file" 2>/dev/null)
            ;;
        jq)
            value=$(jq -r "$path // \"$default\"" "$file" 2>/dev/null)
            ;;
        *)
            value="$default"
            ;;
    esac

    if [[ -z "$value" || "$value" == "null" ]]; then
        echo "$default"
    else
        echo "$value"
    fi
}

# Usage
CONFIG_FILE="config.yaml"

# Load entire config as JSON
CONFIG_JSON=$(load_yaml_config "$CONFIG_FILE")

# Or get specific values
DB_HOST=$(yaml_get "$CONFIG_FILE" '.database.host' 'localhost')
DB_PORT=$(yaml_get "$CONFIG_FILE" '.database.port' '5432')

echo "Database: $DB_HOST:$DB_PORT"
```

## Complete Example: Config Manager

Full configuration management with multiple formats:

```bash
#!/bin/bash
# ABOUTME: Universal configuration manager
# ABOUTME: Supports key=value, JSON, and environment overrides

set -e

# ─────────────────────────────────────────────────────────────────
# Configuration Storage
# ─────────────────────────────────────────────────────────────────

declare -A CONFIG
CONFIG_FILE=""
CONFIG_FORMAT=""

# ─────────────────────────────────────────────────────────────────
# Format Detection
# ─────────────────────────────────────────────────────────────────

detect_format() {
    local file="$1"

    case "${file##*.}" in
        json) echo "json" ;;
        yaml|yml) echo "yaml" ;;
        ini) echo "ini" ;;
        *) echo "keyvalue" ;;
    esac
}

# ─────────────────────────────────────────────────────────────────
# Loaders
# ─────────────────────────────────────────────────────────────────

load_keyvalue() {
    local file="$1"

    while IFS= read -r line || [[ -n "$line" ]]; do
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "${line// /}" ]] && continue

        if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
            local key="${BASH_REMATCH[1]// /}"
            local value="${BASH_REMATCH[2]}"
            value="${value#"${value%%[![:space:]]*}"}"
            CONFIG["$key"]="$value"
        fi
    done < "$file"
}

load_json() {
    local file="$1"

    if ! command -v jq &> /dev/null; then
        echo "Error: jq required for JSON config" >&2
        return 1
    fi

    # Flatten JSON to key=value pairs
    while IFS="=" read -r key value; do
        CONFIG["$key"]="$value"
    done < <(jq -r 'paths(scalars) as $p | "\($p | join("."))"+"="+"\(getpath($p))"' "$file" 2>/dev/null)
}

# ─────────────────────────────────────────────────────────────────
# Main API
# ─────────────────────────────────────────────────────────────────

config_load() {
    local file="$1"
    local env_prefix="${2:-}"

    if [[ ! -f "$file" ]]; then
        echo "Error: Config file not found: $file" >&2
        return 1
    fi

    CONFIG=()
    CONFIG_FILE="$file"
    CONFIG_FORMAT=$(detect_format "$file")

    case "$CONFIG_FORMAT" in
        json) load_json "$file" ;;
        *) load_keyvalue "$file" ;;
    esac

    # Apply environment overrides
    if [[ -n "$env_prefix" ]]; then
        for key in "${!CONFIG[@]}"; do
            local env_key="${env_prefix}${key^^}"
            env_key="${env_key//./_}"
            env_key="${env_key//-/_}"

            if [[ -v "$env_key" ]]; then
                CONFIG["$key"]="${!env_key}"
            fi
        done
    fi

    echo "Loaded ${#CONFIG[@]} config values from $file ($CONFIG_FORMAT)"
}

config_get() {
    local key="$1"
    local default="${2:-}"
    echo "${CONFIG[$key]:-$default}"
}

config_set() {
    local key="$1"
    local value="$2"
    CONFIG["$key"]="$value"
}

config_has() {
    [[ -v CONFIG[$1] ]]
}

config_keys() {
    printf '%s\n' "${!CONFIG[@]}" | sort
}

config_dump() {
    echo "# Configuration ($CONFIG_FORMAT from $CONFIG_FILE)"
    for key in $(config_keys); do
        echo "$key=${CONFIG[$key]}"
    done
}

config_to_json() {
    local json="{}"

    for key in "${!CONFIG[@]}"; do
        json=$(echo "$json" | jq --arg k "$key" --arg v "${CONFIG[$key]}" '. + {($k): $v}')
    done

    echo "$json" | jq '.'
}

# ─────────────────────────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────────────────────────

config_require() {
    local missing=()

    for key in "$@"; do
        if ! config_has "$key" || [[ -z "$(config_get "$key")" ]]; then
            missing+=("$key")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "Error: Missing required config keys:" >&2
        printf "  - %s\n" "${missing[@]}" >&2
        return 1
    fi
}

config_validate_int() {
    local key="$1"
    local value
    value=$(config_get "$key")

    if [[ -n "$value" && ! "$value" =~ ^-?[0-9]+$ ]]; then
        echo "Error: $key must be an integer (got: $value)" >&2
        return 1
    fi
}

config_validate_url() {
    local key="$1"
    local value
    value=$(config_get "$key")

    if [[ -n "$value" && ! "$value" =~ ^https?:// ]]; then
        echo "Error: $key must be a URL (got: $value)" >&2
        return 1
    fi
}

# ─────────────────────────────────────────────────────────────────
# Usage Example
# ─────────────────────────────────────────────────────────────────

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Load config with APP_ prefix for env overrides
    config_load "${1:-config.conf}" "APP_"

    # Validate required keys
    config_require "database_host" "api_key" || exit 1

    # Validate types
    config_validate_int "port" || exit 1
    config_validate_url "api_endpoint" || exit 1

    # Use config values
    echo "Host: $(config_get 'database_host' 'localhost')"
    echo "Port: $(config_get 'port' '5432')"

    # Dump all config
    echo ""
    config_dump
fi
```

## Best Practices

### 1. Always Provide Defaults
```bash
value=$(config_get "key" "default_value")
```

### 2. Validate Early
```bash
config_require "api_key" "database_url" || exit 1
```

### 3. Use Environment Overrides for Secrets
```bash
# Don't store secrets in files
API_KEY="${API_KEY:-$(config_get 'api_key')}"
```

### 4. Validate JSON with jq
```bash
if ! jq empty "$file" 2>/dev/null; then
    echo "Invalid JSON" >&2
    exit 1
fi
```

### 5. Handle Missing Files Gracefully
```bash
if [[ -f "$config_file" ]]; then
    load_config "$config_file"
else
    echo "Warning: Config not found, using defaults" >&2
fi
```

## Resources

- [jq Manual](https://stedolan.github.io/jq/manual/)
- [yq Documentation](https://mikefarah.gitbook.io/yq/)
- [Bash Associative Arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)

---

## Version History

- **1.0.0** (2026-01-14): Initial release - extracted from workspace-hub configuration scripts
