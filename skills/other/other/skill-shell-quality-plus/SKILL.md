---
name: shell-quality-plus
description: Unified shell script quality: ShellCheck linting + BATS testing. Use for CLI scripts, headless agent commands (gemini, codex, droid, claude, kilo), or any bash script. IRON RULE: Lint first, test always. Triggers on "shell script", "bash test", "shellcheck", "CLI script", "agent command".
allowed-tools: [shellcheck, Write, Bash, Read, Glob]
---

# Shell Quality Plus - Unified Shell Script Quality

> "Talk is cheap. Show me the code." - Linus Torvalds

## IRON RULE: Lint First, Test Always

```
FOR shell scripts:
  1. Run ShellCheck BEFORE executing
  2. Write BATS tests AFTER creating the script
  3. Both are REQUIRED for production scripts
```

**NO EXCEPTIONS for CLI scripts, agent commands, or any production shell script.**

## When to Use This Skill

- Writing CLI scripts for headless agents (gemini, codex, droid, claude, kilo)
- Creating bash scripts with multiple options/flags
- Testing shell script behavior
- Validating scripts before execution
- Setting up shell script CI/CD pipelines
- Debugging shell script issues

## Two-Phase Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: LINTING (ShellCheck)                              │
│  → Verify code quality before execution                     │
│  → Catch common pitfalls                                    │
│  → Configure for target shell (bash/sh)                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: TESTING (BATS)                                    │
│  → Test functional behavior                                 │
│  → Mock external commands                                   │
│  → CI/CD integration                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: ShellCheck Linting

### Quick Reference: Common Error Codes

| Code | Issue | Fix |
|------|-------|-----|
| **SC2086** | Word splitting/globbing | Double quote variables: `"$var"` |
| **SC2154** | Referenced but not assigned | Check variable spelling |
| **SC2317** | Unreachable exit code | Remove unreachable code |
| **SC1091** | Not following sourced files | Use `source` or disable |
| **SC2164** | Use `cd ... &&` to avoid path change | Wrap `cd` in subshell |
| **SC2181** | Check exit code directly | Use `if cmd; then` not `$?` |

### Run ShellCheck

```bash
# Basic check
shellcheck script.sh

# Check all scripts in project
find . -name "*.sh" -exec shellcheck {} \;

# With specific shell target
shellcheck --shell=bash script.sh

# Exclude specific warnings
shellcheck --exclude=SC1091,SC2086 script.sh

# Strict mode (all warnings enabled)
shellcheck --enable=all script.sh
```

### ShellCheck Configuration (.shellcheckrc)

Create `.shellcheckrc` in project root:

```bash
# Target shell
shell=bash

# Enable optional checks
enable=avoid-nullary-conditions,require-variable-braces,check-unassigned-uppercase

# Disable common false positives
disable=SC1091  # Not following sourced files
disable=SC2086  # Double quote to prevent globbing (sometimes too noisy)
disable=SC2317  # Command unreachable exit code
```

### Suppress Inline Warnings

```bash
#!/bin/bash
# shellcheck disable=SC2086
for i in $list; do
    echo "$i"
done
```

---

## Phase 2: BATS Testing

### Install BATS

```bash
# macOS
brew install bats-core/bats/bats

# From source
git clone https://github.com/bats-core/bats-core.git
cd bats-core
./install.sh /usr/local
```

### Test Structure

```bash
#!/usr/bin/env bats

setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'
    export TEST_MODE=1
}

teardown() {
    rm -rf "$BATS_TEST_TMPDIR" 2>/dev/null || true
}

@test "script accepts --approval flag" {
    run ./script.sh --approval=auto
    assert_success
    assert_output --partial "approved"
}

@test "agent command executes correctly" {
    AGENT_TYPE=claude run ./script.sh --test
    assert_success
    assert_output --regexp "agent.*executed"
}
```

### Running Tests

```bash
# Basic execution
bats test/

# Parallel execution
bats --jobs 4 test/

# Filter by name
bats --filter "approval" test/

# JUnit output for CI
bats --formatter junit --output ./reports test/
```

---

## Template: CLI Script for Headless Agents

Use this template for scripts that call agents (gemini, codex, droid, claude, kilo):

```bash
#!/bin/bash
# =============================================================================
# agent-cli-template.sh - Template for headless agent CLI scripts
# =============================================================================

# shellcheck disable=SC2086  # Allow word splitting for arrays
# shellcheck disable=SC2154  # Variables set by CLI args

set -Eeuo pipefail  # ERR trap, exit on error, unset=error, pipefail

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
AGENT_TYPE="${AGENT_TYPE:-claude}"    # gemini/codex/droid/claude/kilo
APPROVAL_MODE="${APPROVAL_MODE:-auto}"  # auto/manual/confirm
OUTPUT_FORMAT="${OUTPUT_FORMAT:-json}"   # json/text/markdown
SCRIPT_PATH="${SCRIPT_PATH:-}"
VERBOSE="${VERBOSE:-false}"

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------

log() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    fi
}

error() {
    echo "ERROR: $*" >&2
    exit 1
}

# Execute command on target agent
execute_agent_command() {
    local agent="$1"
    local cmd="$2"
    
    case "$agent" in
        gemini)
            gemini-cli exec --script="$cmd" --approval="$APPROVAL_MODE" --format="$OUTPUT_FORMAT"
            ;;
        codex)
            codex run "$cmd" --no-confirm --output="$OUTPUT_FORMAT"
            ;;
        droid)
            droid-cli execute "$cmd" --headless --approval="$APPROVAL_MODE"
            ;;
        claude|kilo)
            claude-code "$cmd" --approval="$APPROVAL_MODE" --format="$OUTPUT_FORMAT"
            ;;
        *)
            error "Unknown agent: $agent"
            ;;
    esac
}

# Validate prerequisites
validate_prerequisites() {
    local agent="$1"
    command -v "$agent" >/dev/null 2>&1 || error "$agent not found in PATH"
}

# Show usage
usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Execute commands on headless agents.

OPTIONS:
    --agent AGENT      Agent type: gemini, codex, droid, claude, kilo (default: claude)
    --approval MODE    Approval mode: auto, manual, confirm (default: auto)
    --format FORMAT    Output format: json, text, markdown (default: json)
    --script FILE      Script file to execute
    --verbose          Enable verbose output
    --help             Show this help

EXAMPLES:
    $(basename "$0") --agent claude --script ./my-script.sh --approval auto
    $(basename "$0") --agent codex --script ./deploy.sh --format json
    $(basename "$0") --agent droid --verbose --script ./cleanup.sh
EOF
}

# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --agent)
                AGENT_TYPE="$2"
                shift 2
                ;;
            --approval)
                APPROVAL_MODE="$2"
                shift 2
                ;;
            --format)
                OUTPUT_FORMAT="$2"
                shift 2
                ;;
            --script)
                SCRIPT_PATH="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help)
                usage
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done
    
    # Validate
    [[ -n "$SCRIPT_PATH" ]] || error "Script path is required (--script)"
    [[ -f "$SCRIPT_PATH" ]] || error "Script not found: $SCRIPT_PATH"
    
    log "Agent: $AGENT_TYPE"
    log "Approval: $APPROVAL_MODE"
    log "Format: $OUTPUT_FORMAT"
    log "Script: $SCRIPT_PATH"
    
    # Validate prerequisites
    validate_prerequisites "$AGENT_TYPE"
    
    # Execute
    log "Executing agent command..."
    execute_agent_command "$AGENT_TYPE" "$SCRIPT_PATH"
    
    log "Done!"
}

# Run in test mode if TEST_MODE is set (for BATS)
if [[ -n "${TEST_MODE:-}" ]]; then
    main "$@" > /dev/null 2>&1 || exit 1
else
    main "$@"
fi
```

---

## Common ShellCheck Violations & Fixes

### SC2086: Double Quote to Prevent Globbing

```bash
# BAD
for i in $list; do
    echo $i
done

# GOOD
for i in "$list"; do
    echo "$i"
done

# GOOD (if list is array)
for i in "${list[@]}"; do
    echo "$i"
done
```

### SC2181: Check Exit Code Directly

```bash
# BAD
some_command
if [ $? -eq 0 ]; then
    echo "success"
fi

# GOOD
if some_command; then
    echo "success"
fi
```

### SC2154: Referenced but Not Assigned

```bash
# BAD - $AGENT_TYPO is not set
echo "$AGENT_TYPO"

# GOOD - Check if set first
echo "${AGENT_TYPE:-default}"
```

### SC2317: Command Unreachable Exit Code

```bash
# BAD - return after exit
exit 1
echo "unreachable"

# GOOD - remove unreachable code
exit 1
```

---

## BATS Test Examples for CLI Scripts

```bash
#!/usr/bin/env bats

setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'
    export TEST_MODE=1
}

@test "script fails without --script argument" {
    run ./agent-cli-template.sh
    assert_failure
    assert_output --partial "Script path is required"
}

@test "script fails with unknown agent" {
    run ./agent-cli-template.sh --agent unknown --script test.sh
    assert_failure
    assert_output --partial "Unknown agent"
}

@test "script shows help with --help" {
    run ./agent-cli-template.sh --help
    assert_success
    assert_output --partial "Usage:"
    assert_output --partial "--agent"
    assert_output --partial "--approval"
}

@test "script accepts all valid agents" {
    for agent in claude kilo; do
        run ./agent-cli-template.sh --agent "$agent" --script test.sh
        assert_failure  # Fails because test.sh doesn't exist, but agent is valid
        refute_output --partial "Unknown agent"
    done
}

@test "script respects --verbose flag" {
    VERBOSE=true run ./agent-cli-template.sh --agent claude --script test.sh 2>&1
    assert_output --partial "Agent:"
    assert_output --partial "Approval:"
}
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Shell Quality

on: [push, pull_request]

jobs:
  shell-quality:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install ShellCheck
        run: sudo apt-get install -y shellcheck
      
      - name: Install BATS
        run: |
          git clone https://github.com/bats-core/bats-core.git
          ./bats-core/install.sh /usr/local
      
      - name: Run ShellCheck
        run: |
          find . -name "*.sh" -exec shellcheck --exclude=SC1091 {} \;
      
      - name: Run BATS tests
        run: |
          bats --formatter junit --output ./reports test/
      
      - name: Publish test results
        uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          files: reports/report.xml
```

---

## Quick Reference

### ShellCheck Commands

```bash
# Basic
shellcheck script.sh

# All scripts
find . -name "*.sh" -exec shellcheck {} \;

# With exclusions
shellcheck --exclude=SC1091,SC2086 script.sh

# JSON output (for CI parsing)
shellcheck --format=json script.sh
```

### BATS Commands

```bash
# Run tests
bats test/

# Parallel
bats --jobs 4 test/

# Filter
bats --filter "approval" test/

# JUnit output
bats --formatter junit --output ./reports test/
```

---

## After Creating a Shell Script

1. **Run ShellCheck** - Fix all warnings (or document why not)
2. **Write BATS tests** - Test main functionality
3. **Run BATS** - Verify tests pass
4. **Integrate in CI/CD** - Automatic quality checks

---

**Remember: Lint First, Test Always. No exceptions for production scripts.**