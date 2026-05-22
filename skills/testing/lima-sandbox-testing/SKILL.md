---
name: lima-sandbox-testing
description: Run Claude Code integration tests in isolated Lima VM sandboxes. Use for E2E testing, hook validation, session survival tests, and any scenario requiring isolated Claude execution.
version: 1.0.0
triggers:
  - "integration test"
  - "sandbox test"
  - "lima vm"
  - "isolated testing"
  - "e2e test claude"
tools:
  - Bash
  - Read
  - Write
---

# Lima VM Sandbox Testing

Run Claude Code in isolated VMs for reliable integration testing.

## Quick Install (Other Projects)

Run this in any project to set up Lima VM sandbox testing:

```bash
# Install Lima (macOS)
brew install lima

# Clone the integration test framework
mkdir -p .claude && cd .claude
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/hgeldenhuys/claude-code-sdk.git claude-code-sdk
cd claude-code-sdk
git sparse-checkout set integration-tests
cd ../..

# Or copy just the integration-tests folder
curl -fsSL https://raw.githubusercontent.com/hgeldenhuys/claude-code-sdk/main/integration-tests/setup-lima.sh -o .claude/setup-lima.sh
curl -fsSL https://raw.githubusercontent.com/hgeldenhuys/claude-code-sdk/main/integration-tests/run-tests.sh -o .claude/run-tests.sh
curl -fsSL https://raw.githubusercontent.com/hgeldenhuys/claude-code-sdk/main/integration-tests/lib/test-utils.sh -o .claude/lib/test-utils.sh
chmod +x .claude/*.sh
```

## One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/hgeldenhuys/claude-code-sdk/main/scripts/install-lima-tests.sh | bash
```

## VM Setup (One-Time)

```bash
cd integration-tests  # or .claude if installed there

# Create VM (~5 min, downloads Ubuntu)
./setup-lima.sh create

# Install Claude Code and dependencies in VM
./setup-lima.sh install

# Authenticate Claude (interactive)
limactl shell claude-sdk-test
claude login
exit

# Snapshot authenticated state (for fast restore)
./setup-lima.sh snapshot
```

## Running Tests

```bash
# Run all tests
./run-tests.sh

# Run specific test
./run-tests.sh session-survival

# Restore to clean state first
./run-tests.sh --restore session-survival
```

## Writing Tests

Create test files in `tests/` directory:

```bash
#!/bin/bash
# tests/my-feature.sh
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/test-utils.sh"

test_my_feature() {
    test_start "Feature works correctly"

    # Run Claude headless in VM
    claude_headless "Your prompt here" "/tmp/workspace"

    # Assert results
    assert_exit_code 0 "Should succeed"
    assert_contains "$CLAUDE_OUTPUT" "expected" "Should contain expected"

    test_pass
}

main() {
    test_my_feature
    print_summary
}

main "$@"
```

## Test Utilities Reference

### Claude Execution

```bash
# Run Claude with prompt
claude_headless "prompt" "/workspace"
# Results in: $CLAUDE_OUTPUT, $CLAUDE_EXIT_CODE

# Resume session by name
claude_resume "session-name" "prompt" "/workspace"

# Run slash command
claude_slash "/compact" "/workspace"
```

### Session Management

```bash
# Get session ID from name
sesh_get_id "brave-elephant"

# Get name from session ID
sesh_get_name "abc-123-def"

# Check if session exists
sesh_exists "session-name"

# List sessions as JSON
sesh_list "--json"
```

### Assertions

```bash
assert_eq "$actual" "$expected" "Values should match"
assert_ne "$actual" "$unexpected" "Values should differ"
assert_not_empty "$value" "Should have value"
assert_contains "$string" "substring" "Should contain"
assert_exit_code 0 "Should succeed"
```

### VM Commands

```bash
# Run command in VM
vm_exec "ls -la /home"

# Run and capture output
vm_exec_capture "cat /etc/os-release"
# Results in: $VM_STDOUT, $VM_STDERR, $VM_EXIT_CODE
```

## VM Management

```bash
./setup-lima.sh status   # Check VM state
./setup-lima.sh shell    # Open interactive shell
./setup-lima.sh restore  # Reset to authenticated snapshot
./setup-lima.sh destroy  # Delete VM completely
```

## Use Cases

1. **Session Survival**: Test that session names persist across `/compact`
2. **Hook Validation**: Verify hooks execute correctly in real Claude
3. **SDK Integration**: Test SDK features with actual Claude execution
4. **Regression Testing**: Catch breaking changes before release

## Troubleshooting

### VM won't start
```bash
limactl list
limactl stop claude-sdk-test
limactl start claude-sdk-test
```

### Authentication expired
```bash
limactl shell claude-sdk-test -- claude login
./setup-lima.sh snapshot  # Update snapshot
```

### Test pollution
```bash
./setup-lima.sh restore  # Reset to clean state
```

## Architecture

```
integration-tests/
├── setup-lima.sh       # VM lifecycle management
├── run-tests.sh        # Test orchestrator
├── lib/
│   └── test-utils.sh   # Shared utilities
├── tests/
│   └── *.sh            # Test scripts
├── fixtures/           # Test data
└── results/            # JSON test results
```

The VM provides complete isolation - each test run can restore to a known-good authenticated state, ensuring reproducible results.
