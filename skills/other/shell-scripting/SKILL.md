---
name: shell-scripting
description: Write robust, portable shell scripts with proper error handling, argument parsing, and testing. Use when automating system tasks, building CI/CD scripts, or creating container entrypoints.
---

# Shell Scripting

## Purpose

Provides patterns and best practices for writing maintainable shell scripts with error handling, argument parsing, and portability considerations. Covers POSIX sh vs Bash decision-making, parameter expansion, integration with common utilities (jq, yq, awk), and testing with ShellCheck and Bats.

## When to Use This Skill

Use shell scripting when:
- Orchestrating existing command-line tools and system utilities
- Writing CI/CD pipeline scripts (GitHub Actions, GitLab CI)
- Creating container entrypoints and initialization scripts
- Automating system administration tasks (backups, log rotation)
- Building development tooling (build scripts, test runners)

Consider Python/Go instead when:
- Complex business logic or data structures required
- Cross-platform GUI needed
- Heavy API integration (REST, gRPC)
- Script exceeds 200 lines with significant logic complexity

## POSIX sh vs Bash

**Use POSIX sh (#!/bin/sh) when:**
- Maximum portability required (Linux, macOS, BSD, Alpine)
- Minimal container images needed
- Embedded systems or unknown target environments

**Use Bash (#!/bin/bash) when:**
- Controlled environment (specific OS, container)
- Arrays or associative arrays needed
- Advanced parameter expansion beneficial
- Process substitution `<(cmd)` useful

For detailed comparison and testing strategies, see `references/portability-guide.md`.

## Essential Error Handling

### Fail-Fast Pattern

```bash
#!/bin/bash
set -euo pipefail

# -e: Exit on error
# -u: Exit on undefined variable
# -o pipefail: Pipeline fails if any command fails
```

Use for production automation, CI/CD scripts, and critical operations.

### Explicit Exit Code Checking

```bash
#!/bin/bash

if ! command_that_might_fail; then
    echo "Error: Command failed" >&2
    exit 1
fi
```

Use for custom error messages and interactive scripts.

### Trap Handlers for Cleanup

```bash
#!/bin/bash
set -euo pipefail

TEMP_FILE=$(mktemp)

cleanup() {
    rm -f "$TEMP_FILE"
}

trap cleanup EXIT
```

Use for guaranteed cleanup of temporary files, locks, and resources.

For comprehensive error patterns, see `references/error-handling.md`.

## Argument Parsing

### Short Options with getopts (POSIX)

```bash
#!/bin/bash

while getopts "hvf:o:" opt; do
    case "$opt" in
        h) usage ;;
        v) VERBOSE=true ;;
        f) INPUT_FILE="$OPTARG" ;;
        o) OUTPUT_FILE="$OPTARG" ;;
        *) usage ;;
    esac
done

shift $((OPTIND - 1))
```

### Long Options (Manual Parsing)

```bash
#!/bin/bash

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help) usage ;;
        --verbose) VERBOSE=true; shift ;;
        --file) INPUT_FILE="$2"; shift 2 ;;
        --file=*) INPUT_FILE="${1#*=}"; shift ;;
        *) break ;;
    esac
done
```

For hybrid approaches and validation patterns, see `references/argument-parsing.md`.

## Parameter Expansion Quick Reference

```bash
# Default values
${var:-default}              # Use default if unset
${var:=default}              # Assign default if unset
: "${API_KEY:?Error: required}"  # Error if unset

# String manipulation
${#var}                      # String length
${var:offset:length}         # Substring
${var%.txt}                  # Remove suffix
${var##*/}                   # Basename
${var/old/new}               # Replace first
${var//old/new}              # Replace all

# Case conversion (Bash 4+)
${var^^}                     # Uppercase
${var,,}                     # Lowercase
```

For complete expansion patterns and array handling, see `references/parameter-expansion.md`.

## Common Utilities Integration

### JSON with jq

```bash
# Extract field
name=$(curl -sSL https://api.example.com/user | jq -r '.name')

# Filter array
active=$(jq '.users[] | select(.active) | .name' data.json)

# Check existence
if ! echo "$json" | jq -e '.field' >/dev/null; then
    echo "Error: Field missing" >&2
fi
```

### YAML with yq

```bash
# Read value (yq v4)
host=$(yq eval '.database.host' config.yaml)

# Update in-place
yq eval '.port = 5432' -i config.yaml

# Convert to JSON
yq eval -o=json config.yaml
```

### Text Processing

```bash
# awk: Extract columns
awk -F',' '{print $1, $3}' data.csv

# sed: Replace text
sed 's/old/new/g' file.txt

# grep: Pattern match
grep -E "ERROR|WARN" logfile.txt
```

For detailed examples and best practices, see `references/common-utilities.md`.

## Testing and Validation

### ShellCheck: Static Analysis

```bash
# Check script
shellcheck script.sh

# POSIX compliance
shellcheck --shell=sh script.sh

# Exclude warnings
shellcheck --exclude=SC2086 script.sh
```

### Bats: Automated Testing

```bash
#!/usr/bin/env bats

@test "script runs successfully" {
    run ./script.sh --help
    [ "$status" -eq 0 ]
    [ "${lines[0]}" = "Usage: script.sh [OPTIONS]" ]
}

@test "handles missing argument" {
    run ./script.sh
    [ "$status" -eq 1 ]
    [[ "$output" =~ "Error" ]]
}
```

Run tests:
```bash
bats test/
```

For CI/CD integration and debugging techniques, see `references/testing-guide.md`.

## Defensive Programming Checklist

```bash
#!/bin/bash
set -euo pipefail

# Check required commands
command -v jq >/dev/null 2>&1 || {
    echo "Error: jq required" >&2
    exit 1
}

# Check environment variables
: "${API_KEY:?Error: API_KEY required}"

# Check files
[ -f "$CONFIG_FILE" ] || {
    echo "Error: Config not found: $CONFIG_FILE" >&2
    exit 1
}

# Quote all variables
echo "Processing: $file"        # ❌ Unquoted
echo "Processing: \"$file\""    # ✅ Quoted
```

## Platform Considerations

### macOS vs Linux Differences

```bash
# sed in-place
sed -i '' 's/old/new/g' file.txt    # macOS
sed -i 's/old/new/g' file.txt       # Linux

# Portable: Use temp file
sed 's/old/new/g' file.txt > file.txt.tmp
mv file.txt.tmp file.txt

# readlink
readlink -f /path                    # Linux only
cd "$(dirname "$0")" && pwd         # Portable
```

For complete platform differences, see `references/portability-guide.md`.

## Script Categories

**System Administration:** Cron jobs, log rotation, backup automation
**Build/Deployment:** CI/CD pipelines, Docker builds, deployments
**Development Tooling:** Project setup, test runners, code generators
**Container Entrypoints:** Initialization, signal handling, configuration

## Production Script Template

```bash
#!/bin/bash
set -euo pipefail

readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

TEMP_DIR=""

cleanup() {
    local exit_code=$?
    rm -rf "$TEMP_DIR"
    exit "$exit_code"
}

trap cleanup EXIT

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >&2
}

main() {
    # Check dependencies
    command -v jq >/dev/null 2>&1 || exit 1

    # Parse arguments
    # Validate input
    # Process
    # Report results

    log "Completed successfully"
}

main "$@"
```

For complete production template, see `examples/production-template.sh`.

## Tool Recommendations

**Core Tools:**
- **jq**: JSON parsing and transformation
- **yq**: YAML parsing (v4 recommended)
- **ShellCheck**: Static analysis and linting
- **Bats**: Automated testing framework

**Installation:**
```bash
# macOS
brew install jq yq shellcheck bats-core

# Ubuntu/Debian
apt-get install jq shellcheck
```

## Related Skills

- **linux-administration**: System commands and administration
- **building-ci-pipelines**: Using scripts in CI/CD
- **infrastructure-as-code**: Terraform/Pulumi wrappers
- **kubernetes-operations**: kubectl scripts, Helm hooks
- **writing-dockerfiles**: Container entrypoints

## Additional Resources

**Reference Files:**
- `references/error-handling.md` - Comprehensive error patterns
- `references/argument-parsing.md` - Advanced parsing techniques
- `references/parameter-expansion.md` - Complete expansion reference
- `references/portability-guide.md` - POSIX vs Bash differences
- `references/testing-guide.md` - ShellCheck and Bats guide
- `references/common-utilities.md` - jq, yq, awk, sed usage

**Example Scripts:**
- `examples/production-template.sh` - Production-ready template
- `examples/getopts-basic.sh` - Simple getopts usage
- `examples/getopts-advanced.sh` - Complex option handling
- `examples/long-options.sh` - Manual long option parsing
- `examples/error-handling.sh` - Error handling patterns
- `examples/json-yaml-processing.sh` - jq/yq examples

**Utility Scripts:**
- `scripts/lint-script.sh` - ShellCheck wrapper for CI
- `scripts/test-script.sh` - Bats wrapper for CI
