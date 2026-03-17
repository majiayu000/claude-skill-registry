---
name: cfn-utilities
description: "Reusable bash utility functions for CFN Loop - logging, error handling, retry, file operations. Use when you need structured logging, atomic file operations, retry logic with exponential backoff, or standardized error handling in bash scripts."
version: 1.0.0
tags: [bash, logging, error-handling, retry, file-operations, utilities]
status: production
category: utilities
---

# CFN Utilities Skill

## Description

Reusable bash utility functions for the CFN Loop system. Provides standardized logging, error handling, retry logic, and atomic file operations with zero external dependencies.

## Purpose

- **Structured Logging**: JSON-formatted logs compatible with TypeScript logging system
- **Error Handling**: Consistent error management across bash scripts
- **Retry Logic**: Exponential backoff for transient failures
- **File Operations**: Atomic writes and file locking primitives

## Dependencies

- POSIX-compliant bash (4.0+)
- Coreutils (standard Linux/macOS utilities)
- No external dependencies required

## Usage

### Direct Function Invocation

```bash
# Source all utilities
source ./.claude/skills/cfn-utilities/execute.sh

# Use individual functions
log_info "Task started" '{"task_id":"abc123"}'
retry_with_backoff 3 2 curl https://api.example.com
atomic_write "/path/to/file.txt" "content here"
```

### Via Execute Script

```bash
# Execute specific function
./.claude/skills/cfn-utilities/execute.sh log_json "info" "Message" '{"key":"value"}'

# Source and call
source ./.claude/skills/cfn-utilities/execute.sh
log_error "Operation failed" '{"error_code":"E001"}'
```

## Available Functions

### Logging (lib/logging.sh)

**log_json(level, message, context)**
```bash
log_json "info" "Task started" '{"task_id":"abc123","agent":"backend-dev"}'
# Output: {"timestamp":"2025-11-15T20:00:00Z","level":"info","message":"Task started","context":{"task_id":"abc123","agent":"backend-dev"}}
```

**log_info(message, context)**
```bash
log_info "Processing file" '{"file":"data.txt"}'
```

**log_warn(message, context)**
```bash
log_warn "Deprecated function used" '{"function":"old_func"}'
```

**log_error(message, context)**
```bash
log_error "Failed to connect" '{"host":"api.example.com","code":500}'
```

**log_debug(message, context)**
```bash
export LOG_LEVEL=debug
log_debug "Variable state" '{"var":"value"}'
```

### Error Handling (lib/errors.sh)

**error_exit(message, exit_code, context)**
```bash
error_exit "Database connection failed" 1 '{"db":"postgres"}'
```

**error_handle(message, context)**
```bash
if ! validate_input "$data"; then
    error_handle "Invalid input" '{"input":"'$data'"}'
    return 1
fi
```

**is_error_code(expected_code)**
```bash
curl https://api.example.com
if is_error_code 7; then
    echo "Connection failed"
fi
```

### Retry Logic (lib/retry.sh)

**retry_with_backoff(max_attempts, base_delay_sec, command, args...)**
```bash
# Retry curl with exponential backoff (2s, 4s, 8s)
retry_with_backoff 3 2 curl -f https://api.example.com/data

# Retry custom command
retry_with_backoff 5 1 cfn-spawn agent "backend-developer" --task "task"
```

### File Operations (lib/file-ops.sh)

**atomic_write(filepath, content)**
```bash
atomic_write "/tmp/data.json" '{"status":"complete"}'
```

**acquire_lock(lockfile, timeout_sec)**
```bash
if acquire_lock "/tmp/resource.lock" 30; then
    # Critical section
    release_lock "/tmp/resource.lock"
fi
```

**release_lock(lockfile)**
```bash
release_lock "/tmp/resource.lock"
```

**with_lock(lockfile, timeout_sec, command, args...)**
```bash
with_lock "/tmp/database.lock" 60 ./scripts/migrate-db.sh
```

## Integration Points

### TypeScript Compatibility

**Logging Format**:
- JSON output compatible with `src/utils/logging.ts`
- Correlation ID format matches TypeScript UUID generation
- Timestamp format: ISO 8601 (UTC)

**Error Codes**:
- Error codes align with `src/utils/errors.ts`
- Exit codes: 0=success, 1=general error, 2=usage error, 130=timeout

**File Locking**:
- Lock files use `.lock` extension (same as `src/utils/file-operations.ts`)
- Timeout behavior matches TypeScript implementation

### CFN System Integration

**Used By**:
- `.claude/hooks/cfn-invoke-pre-edit.sh` - atomic backup creation
- `.claude/skills/cfn-coordination/` - structured logging
- `.claude/skills/cfn-loop-orchestration/orchestrate.sh` - retry logic
- All CFN agents - standardized error handling

**Correlation IDs**:
```bash
# Generate correlation ID (compatible with TypeScript)
CORRELATION_ID=$(uuidgen 2>/dev/null || echo "$(date +%s)-$$-$RANDOM")
log_info "Request started" '{"correlation_id":"'$CORRELATION_ID'"}'
```

## Testing

```bash
# Run all tests
./.claude/skills/cfn-utilities/test.sh

# Expected output:
# PASS: log_json outputs valid JSON
# PASS: retry_with_backoff succeeds after failures
# PASS: atomic_write creates file atomically
# PASS: with_lock prevents concurrent execution
# All tests passed (15/15)
```

## Implementation Patterns

### Safe Script Template

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.claude/skills/cfn-utilities/execute.sh"

main() {
    log_info "Script started" '{"script":"'$(basename "$0")'"}'

    retry_with_backoff 3 2 risky_operation || {
        error_exit "Operation failed after retries" 1
    }

    atomic_write "/tmp/result.txt" "Success"
    log_info "Script completed" '{"status":"success"}'
}

main "$@"
```

### Critical Section Pattern

```bash
#!/usr/bin/env bash
source ./.claude/skills/cfn-utilities/execute.sh

# Ensure only one instance modifies shared resource
with_lock "/tmp/shared-resource.lock" 30 bash -c '
    log_info "Updating shared resource"
    echo "new data" >> /tmp/shared-resource.txt
    log_info "Update complete"
'
```

## Best Practices

1. **Always use structured logging** - Include context objects for debugging
2. **Set strict mode** - Use `set -euo pipefail` in all scripts
3. **Use atomic operations** - Prevent partial writes with atomic_write()
4. **Implement retries** - Handle transient failures gracefully
5. **Lock shared resources** - Prevent race conditions with file locks

## Version History

- **1.0.0** (2025-11-15): Initial release with logging, errors, retry, and file ops
