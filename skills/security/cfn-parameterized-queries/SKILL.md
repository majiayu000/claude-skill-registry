---
name: cfn-parameterized-queries
description: "Secure SQL query execution with parameterized queries to prevent SQL injection attacks. Use when executing database queries, inserting/updating records, or performing any SQL operations that require security hardening."
version: 1.0.0
tags: [security, sql, database, parameterized-queries, injection-prevention]
status: production
---

#!/bin/bash

# CFN Parameterized Queries - Secure SQL Query Execution
# Security Level: CRITICAL - Prevents SQL injection attacks
# Status: Production Ready

set -euo pipefail

# Security Functions
validate_sql_identifier() {
    local identifier="$1"
    local identifier_type="${2:-identifier}"
    
    # Remove control characters and null bytes
    identifier=$(sanitize_value "$identifier")
    
    # Strict validation: alphanumeric + underscore, optional dot notation
    if [[ ! "$identifier" =~ ^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*$ ]]; then
        echo "ERROR: Invalid $identifier_type '$identifier' - must match ^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*$" >&2
        return 1
    fi
    
    # Reasonable length limit (128 chars per part)
    for part in ${identifier//./ }; do
        if [[ ${#part} -gt 128 ]]; then
            echo "ERROR: $identifier_type part too long (max 128 chars): '$part'" >&2
            return 1
        fi
    done
    
    return 0
}

validate_table_name() {
    validate_sql_identifier "$1" "table name"
}

validate_column_name() {
    validate_sql_identifier "$1" "column name"
}

sanitize_value() {
    local value="$1"
    # Remove null bytes and control characters except newline and tab
    echo "$value" | tr -d '\000' | tr -cd '\011\012\015\040-\176'
}

# Core Query Functions
execute_select_one() {
    local db_path="$1"
    local query="$2"
    shift 2
    local params=("$@")
    
    [[ -f "$db_path" ]] || {
        echo "ERROR: Database not found: $db_path" >&2
        return 1
    }
    
    # Build parameter file for secure binding
    local param_file
    param_file=$(mktemp)
    trap "rm -f '$param_file'" RETURN
    
    {
        echo ".param init"
        for i in "${!params[@]}"; do
            local param_index=$((i + 1))
            echo ".param set @p$param_index '${params[$i]}'"
        done
        echo "$query"
    } > "$param_file"
    
    sqlite3 "$db_path" < "$param_file"
}

execute_select_many() {
    local db_path="$1"
    local query="$2"
    shift 2
    local params=("$@")
    
    [[ -f "$db_path" ]] || {
        echo "ERROR: Database not found: $db_path" >&2
        return 1
    }
    
    # Build parameter file for secure binding
    local param_file
    param_file=$(mktemp)
    trap "rm -f '$param_file'" RETURN
    
    {
        echo ".param init"
        for i in "${!params[@]}"; do
            local param_index=$((i + 1))
            echo ".param set @p$param_index '${params[$i]}'"
        done
        echo "$query"
    } > "$param_file"
    
    sqlite3 -line "$db_path" < "$param_file"
}

execute_insert() {
    local db_path="$1"
    local table="$2"
    shift 2
    
    validate_table_name "$table" || return 1
    
    local columns=""
    local values=()
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --columns)
                shift
                columns="$1"
                # Validate each column name
                for col in $(echo "$columns" | tr ',' ' '); do
                    validate_column_name "$col" || return 1
                done
                ;;
            --values)
                shift
                while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
                    values+=("$(sanitize_value "$1")")
                    shift
                done
                ;;
            *)
                echo "ERROR: Unknown option: $1" >&2
                return 1
                ;;
        esac
        shift
    done
    
    [[ -n "$columns" ]] || {
        echo "ERROR: --columns required" >&2
        return 1
    }
    
    [[ ${#values[@]} -gt 0 ]] || {
        echo "ERROR: --values required" >&2
        return 1
    }
    
    # Build placeholders
    local placeholders
    placeholders=$(printf "?,%.0s" "${values[@]}" | sed 's/,$//')
    
    # Execute parameterized insert
    local param_file
    param_file=$(mktemp)
    trap "rm -f '$param_file'" RETURN
    
    {
        echo ".param init"
        for i in "${!values[@]}"; do
            local param_index=$((i + 1))
            echo ".param set @p$param_index '${values[$i]}'"
        done
        echo "INSERT INTO $table ($columns) VALUES ($placeholders);"
    } > "$param_file"
    
    sqlite3 "$db_path" < "$param_file"
}

execute_update() {
    local db_path="$1"
    local table="$2"
    local set_column="$3"
    local set_value="$4"
    local where_column="$5"
    local where_value="$6"
    
    validate_table_name "$table" || return 1
    validate_column_name "$set_column" || return 1
    validate_column_name "$where_column" || return 1
    
    set_value=$(sanitize_value "$set_value")
    where_value=$(sanitize_value "$where_value")
    
    sqlite3 "$db_path" <<EOF
.param init
.param set @set_value '$set_value'
.param set @where_value '$where_value'
UPDATE $table SET $set_column = @set_value WHERE $where_column = @where_value;
EOF
}

execute_delete() {
    local db_path="$1"
    local table="$2"
    local where_column="$3"
    local where_value="$4"
    
    validate_table_name "$table" || return 1
    validate_column_name "$where_column" || return 1
    
    where_value=$(sanitize_value "$where_value")
    
    sqlite3 "$db_path" <<EOF
.param init
.param set @where_value '$where_value'
DELETE FROM $table WHERE $where_column = @where_value;
EOF
}

# Utility Functions
execute_exists() {
    local db_path="$1"
    local table="$2"
    local column="$3"
    local value="$4"
    
    validate_table_name "$table" || return 1
    validate_column_name "$column" || return 1
    value=$(sanitize_value "$value")
    
    local count
    count=$(sqlite3 "$db_path" <<EOF
.param init
.param set @value '$value'
SELECT COUNT(*) FROM $table WHERE $column = @value;
EOF
)
    
    [[ "$count" -gt 0 ]]
}

get_by_id() {
    local db_path="$1"
    local table="$2"
    local id="$3"
    
    validate_table_name "$table" || return 1
    id=$(sanitize_value "$id")
    
    sqlite3 "$db_path" <<EOF
.param init
.param set @id '$id'
SELECT * FROM $table WHERE id = @id LIMIT 1;
EOF
}

count_records() {
    local db_path="$1"
    local table="$2"
    local where_clause="${3:-}"
    
    validate_table_name "$table" || return 1
    
    local query="SELECT COUNT(*) FROM $table"
    [[ -n "$where_clause" ]] && query+=" WHERE $where_clause"
    query+=";"
    
    sqlite3 "$db_path" "$query"
}

# Transaction Support
begin_transaction() {
    local db_path="$1"
    [[ -f "$db_path" ]] || {
        echo "ERROR: Database not found: $db_path" >&2
        return 1
    }
    sqlite3 "$db_path" "BEGIN TRANSACTION;"
}

commit_transaction() {
    local db_path="$1"
    sqlite3 "$db_path" "COMMIT;"
}

rollback_transaction() {
    local db_path="$1"
    sqlite3 "$db_path" "ROLLBACK;"
}

# Legacy compatibility functions
select_single_value() {
    execute_select_one "$@"
}

multiple_row_select() {
    execute_select_many "$@"
}

insert_record() {
    local db_path="$1"
    local table="$2"
    local columns="$3"
    shift 3
    local values=("$@")
    
    execute_insert "$db_path" "$table" --columns "$columns" --values "${values[@]}"
}

update_record() {
    local db_path="$1"
    local table="$2"
    local set_clause="$3"
    local where_clause="$4"
    shift 4
    local params=("$@")
    
    echo "WARNING: update_record is deprecated. Use execute_update instead." >&2
    
    # Parse set and where clauses for simple cases
    if [[ "$set_clause" =~ ^([a-zA-Z_][a-zA-Z0-9_]*)=\?$ ]]; then
        local set_col="${BASH_REMATCH[1]}"
    else
        echo "ERROR: Complex SET clause not supported in legacy function" >&2
        return 1
    fi
    
    if [[ "$where_clause" =~ ^([a-zA-Z_][a-zA-Z0-9_]*)=\?$ ]]; then
        local where_col="${BASH_REMATCH[1]}"
    else
        echo "ERROR: Complex WHERE clause not supported in legacy function" >&2
        return 1
    fi
    
    execute_update "$db_path" "$table" "$set_col" "${params[0]}" "$where_col" "${params[1]}"
}

delete_record() {
    execute_delete "$@"
}

execute_parameterized() {
    execute_select_many "$@"
}

load_skill_secure() {
    local db_path="$1"
    local skill_name="$2"
    local cache_dir="${3:-./.skill-cache}"
    
    [[ -f "$db_path" ]] || {
        echo "ERROR: Database not found: $db_path" >&2
        return 1
    }
    
    skill_name=$(sanitize_value "$skill_name")
    mkdir -p "$cache_dir"
    local cache_file="${cache_dir}/${skill_name}.md"
    
    local skill_content
    skill_content=$(sqlite3 "$db_path" <<EOF
.param init
.param set @skill_name '$skill_name'
SELECT content FROM skills WHERE name = @skill_name;
EOF
)
    
    [[ -n "$skill_content" ]] || {
        echo "ERROR: Skill not found: $skill_name" >&2
        return 1
    }
    
    echo "$skill_content" > "$cache_file"
    echo "$cache_file"
}