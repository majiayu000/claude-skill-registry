---
name: Automated Test-Fix Loop
description: Pattern for automated testing with GitHub issue creation and Claude Code auto-fixing. Creates Test → Fail → Issue → Fix → Repeat cycle until tests pass.
tags: [testing, automation, github, ci-cd]
version: 1.0
---

# Automated Test-Fix Loop Pattern

## Overview

This skill provides a generalized pattern for continuous automated testing and fixing using Claude Code. The system creates a feedback loop: **Test → Fail → Issue → Fix → Test** that runs until all tests pass.

Use this pattern when you want:
- Automated bug fixing during development
- Regression testing after major changes
- CI/CD integration with self-healing tests
- Overnight fuzzing with automatic fixes

## Architecture

```
Test Runner (run-tests.sh)
  ├─> Runs test suite with timeout
  ├─> Captures output and environment context
  └─> On failure: Creates GitHub issue
         ↓
    GitHub Issues (with full context)
         ↓
Issue Fixer (fix-issue.sh)
  ├─> Fetches issue from GitHub
  ├─> Invokes Claude Code with detailed prompt
  └─> Claude investigates, fixes, tests, closes issue
         ↓
Auto-Fix Loop (auto-fix-loop.sh)
  └─> Orchestrates: Test → Fix → Repeat until green
```

## Core Components

### 1. Test Runner Script Template

```bash
#!/bin/bash
set -euo pipefail

# Configuration
TIMEOUT_SECONDS=10
OUTPUT_FILE="/tmp/test-output.txt"
COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
DATE=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
OS_INFO=$(uname -a)

# Run tests with timeout
timeout $TIMEOUT_SECONDS <YOUR_TEST_COMMAND> 2>&1 | tee "$OUTPUT_FILE"
EXIT_CODE=${PIPESTATUS[0]}

# Annotate timeout
if [ $EXIT_CODE -eq 124 ]; then
    EXIT_CODE="124 (timeout after ${TIMEOUT_SECONDS}s)"
fi

# On failure: Create GitHub issue
if [ $EXIT_CODE -ne 0 ]; then
    # Strip ANSI color codes
    CLEAN_OUTPUT=$(sed 's/\x1b\[[0-9;]*m//g' "$OUTPUT_FILE")

    # Create issue
    gh issue create \
        --title "Test Failure: <TEST_NAME>" \
        --body "$(cat <<EOF
## Test Failure Report

**Exit Code:** $EXIT_CODE
**Date:** $DATE
**Commit:** $COMMIT
**Branch:** $BRANCH
**OS:** $OS_INFO

### Test Output
\`\`\`
$CLEAN_OUTPUT
\`\`\`

### Diagnostic Information
<Add service status, connectivity checks, etc.>

### Files Involved
- Test: <path/to/test>
- Implementation: <path/to/impl>

### Expected Behavior
<What should happen>

### Actual Behavior
<What actually happened>
EOF
)"

    exit 1
fi

echo "All tests passed!"
exit 0
```

**Key Customization Points:**
- `<YOUR_TEST_COMMAND>`: Language-specific test runner
  - Python: `pytest tests/`
  - Node.js: `npm test`
  - Rust: `cargo test`
  - Go: `go test ./...`
- `TIMEOUT_SECONDS`: Appropriate for your test suite
- Diagnostic checks: Database connections, API availability, etc.

### 2. Issue Fixer Script Template

```bash
#!/bin/bash
set -euo pipefail

# Parse arguments
ISSUE_NUM="$1"
MODEL="${2:-haiku}"
PERMISSION_MODE="interactive"

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        --model)
            MODEL="$2"
            shift 2
            ;;
        --auto-edit)
            PERMISSION_MODE="acceptEdits"
            shift
            ;;
        --no-prompts)
            PERMISSION_MODE="dangerouslySkip"
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Fetch issue
ISSUE_TITLE=$(gh issue view "$ISSUE_NUM" --json title --jq '.title')
ISSUE_BODY=$(gh issue view "$ISSUE_NUM" --json body --jq '.body')

# Create prompt with guidance
PROMPT=$(cat <<EOF
GitHub Issue #$ISSUE_NUM: $ISSUE_TITLE

$ISSUE_BODY

IMPORTANT: Project-Specific Guidance
- <What code to modify vs what code to leave alone>
- <Where to look for the bug>
- <Common pitfalls to avoid>

Steps:
1. Read the test output carefully
2. Examine the source code
3. Identify the root cause
4. Implement a fix
5. Test with: ./run-tests.sh
6. If tests pass, close the issue with: gh issue close $ISSUE_NUM

You MUST verify the fix by running tests before closing the issue.
EOF
)

# Build Claude Code command
CLAUDE_OPTS=(--model "$MODEL")

if [ "$PERMISSION_MODE" = "dangerouslySkip" ]; then
    CLAUDE_OPTS+=(--dangerously-skip-permissions)
elif [ "$PERMISSION_MODE" != "interactive" ]; then
    CLAUDE_OPTS+=(--permission-mode "$PERMISSION_MODE")
fi

# Invoke Claude Code
claude "${CLAUDE_OPTS[@]}" "$PROMPT"
```

**Model Selection:**
- `haiku`: Simple bugs, syntax errors (fast, cheap)
- `sonnet`: Most issues (balanced)
- `opus`: Complex architectural problems (slow, expensive)

**Permission Modes:**
- `interactive` (default): User approves each action
- `acceptEdits`: Auto-accept file edits, prompt for bash
- `dangerouslySkip`: No prompts (sandboxed environments only!)

### 3. Auto-Fix Loop Script Template

```bash
#!/bin/bash
set -euo pipefail

MAX_ITERATIONS=${1:-10}
MODEL=${2:-haiku}
TEST_MODE=${3:-}

echo "Starting auto-fix loop (max $MAX_ITERATIONS iterations, model: $MODEL)"

iteration=0
while [ $iteration -lt $MAX_ITERATIONS ]; do
    echo "========================================="
    echo "Iteration $((iteration + 1))/$MAX_ITERATIONS"
    echo "========================================="

    # Run tests
    if ./run-tests.sh $TEST_MODE; then
        echo "SUCCESS! All tests passed!"
        exit 0
    fi

    # Wait for GitHub API
    sleep 2

    # Find open issues
    OPEN_ISSUES=$(gh issue list --state open --search "Test Failure" --json number --jq '.[].number')

    if [ -z "$OPEN_ISSUES" ]; then
        echo "No open test failure issues found"
        sleep 2
        continue
    fi

    # Fix the first issue
    ISSUE_NUM=$(echo "$OPEN_ISSUES" | head -1)
    echo "Fixing issue #$ISSUE_NUM..."

    ./fix-issue.sh --model "$MODEL" --no-prompts "$ISSUE_NUM"

    iteration=$((iteration + 1))
done

echo "Max iterations reached without success"
exit 1
```

## Sandboxing Strategies

### Why Sandbox?

Using `--dangerously-skip-permissions` requires sandboxing because Claude Code can:
- Execute arbitrary bash commands
- Modify any files
- Make network requests

**Only use `--dangerously-skip-permissions` in isolated environments!**

### Option 1: Local QEMU VM

```bash
# Start VM
qemu-system-x86_64 \
    -m 2048 \
    -hda debian-vm.qcow2 \
    -netdev user,id=net0,hostfwd=tcp::2224-:22 \
    -enable-kvm -cpu host \
    -display none -daemonize

# Copy project
rsync -avz --exclude='target/' --exclude='.git/' \
    ./ user@localhost:~/project/ -e "ssh -p 2224"

# Run in VM
ssh -p 2224 user@localhost 'cd ~/project && ./auto-fix-loop.sh'
```

**Pros:** Full isolation, easy reset, works offline
**Cons:** Requires local resources, disk space limits

### Option 2: Remote Server VM

```bash
# Copy to remote with lots of space
rsync -avz ./ user@remote:/path/to/testing/

# Start VM on remote
ssh user@remote 'qemu-system-x86_64 ... -daemonize'

# Forward VM SSH port
ssh -L 2230:localhost:3260 user@remote

# Access remote VM as if local
ssh -p 2230 user@localhost 'cd ~/project && ./auto-fix-loop.sh'
```

**Pros:** Unlimited disk space, doesn't consume local resources, can run overnight
**Cons:** Requires network, more complex setup

### Option 3: Docker Container

```dockerfile
FROM <base-image>
RUN apt-get update && apt-get install -y gh <build-tools>
COPY . /project
WORKDIR /project
CMD ["./auto-fix-loop.sh"]
```

```bash
docker build -t auto-tester .
docker run --rm auto-tester
```

**Pros:** Lightweight, fast startup
**Cons:** Less isolation than VM

## Usage Examples

### Initial Development

```bash
# 1. Write tests for new feature (they fail)
./run-tests.sh

# 2. Run auto-fix loop (interactive)
./auto-fix-loop.sh 20 sonnet

# 3. Review changes
git diff

# 4. Commit if satisfied
git commit -am "Implement feature X"
```

### Regression Testing

```bash
# After making changes
./run-tests.sh

# If issues created
./fix-issue.sh --auto-edit 15

# Verify
./run-tests.sh
```

### Overnight Fuzzing (in VM)

```bash
# In sandboxed VM
nohup ./auto-fix-loop.sh 100 haiku > overnight.log 2>&1 &

# Next morning
tail overnight.log
gh issue list --state closed
```

## Best Practices

### 1. Issue Quality

**Include in issues:**
- Test command that failed
- Exit code (with timeout annotation)
- Full test output (cleaned of ANSI codes)
- Environment: commit, branch, OS, date
- Diagnostic info: service status, connectivity
- Files involved: test code, implementation code
- Expected vs actual behavior

**Bad issue:** "Tests failed. Output: Error"

### 2. Test Timeouts

- Unit tests: 10-30 seconds
- Integration tests: 1-5 minutes
- E2E tests: 5-15 minutes

Too short = false positives. Too long = wasted time on hangs.

### 3. Preventing Test Modifications

**Critical:** Add to fix-issue.sh prompt:

```
IMPORTANT: The tests in tests/ are CORRECT and must NOT be modified.
Fix the implementation code in src/, not the test code.
```

Claude Code may try to "fix" tests to make them pass. Explicitly forbid this.

### 4. Iteration Limits

Set based on:
- Test suite size
- Time budget (overnight = 50+, quick check = 5-10)
- Cost concerns

Typical: 10-20 iterations

## Language-Specific Adaptations

### Python

```bash
# run-tests.sh
pytest tests/ --junit-xml=results.xml || EXIT_CODE=$?
```

### Node.js

```bash
# run-tests.sh
npm test 2>&1 | tee test-output.txt || EXIT_CODE=$?
```

### Rust

```bash
# run-tests.sh
cargo test --all 2>&1 | tee test-output.txt || EXIT_CODE=$?
```

### Go

```bash
# run-tests.sh
go test ./... -v -timeout 30s || EXIT_CODE=$?
```

## Troubleshooting

### Claude Fixes Tests Instead of Code

**Problem:** Modifies test files to make tests pass

**Solution:** Add explicit guidance in fix-issue.sh:
```
IMPORTANT: Tests are CORRECT. Fix implementation code only.
```

### Infinite Loop (Same Issue Reopens)

**Problem:** Fix doesn't solve the problem

**Solution:**
- Add more context to issues (logs, diagnostics)
- Escalate to stronger model (haiku → sonnet → opus)
- Add project-specific debugging hints

### Tests Pass Locally, Fail in VM

**Problem:** Different environment

**Solution:**
- Ensure VM has all dependencies
- Check environment variables
- Verify file permissions
- Compare tool versions

## Security Considerations

### Safe to Auto-Fix
- ✅ Unit tests
- ✅ Integration tests (internal)
- ✅ Linting/formatting
- ✅ Type errors

### Review Before Accepting
- ⚠️ Security-sensitive code (auth, crypto)
- ⚠️ Database migrations
- ⚠️ API contract changes
- ⚠️ Dependency updates

### Never Auto-Fix
- ❌ Production deployments
- ❌ Credentials/secrets
- ❌ Access control
- ❌ Billing/payment code

## Quick Start Checklist

- [ ] Install `gh` CLI: `sudo apt-get install gh`
- [ ] Authenticate: `gh auth login`
- [ ] Create `run-tests.sh` with your test command
- [ ] Create `fix-issue.sh` with project guidance
- [ ] Create `auto-fix-loop.sh` for orchestration
- [ ] Test manually: `./run-tests.sh` (should create issue)
- [ ] Fix manually: `./fix-issue.sh 1` (check it works)
- [ ] Run loop: `./auto-fix-loop.sh 5 haiku`
- [ ] For full automation: Set up sandboxed VM
- [ ] In VM: Use `--no-prompts` mode

## References

- GitHub CLI: https://cli.github.com/
- Claude Code: https://claude.ai/claude-code
- Full pattern documentation: See AUTOMATED_TESTING_PATTERN.md in reference projects
