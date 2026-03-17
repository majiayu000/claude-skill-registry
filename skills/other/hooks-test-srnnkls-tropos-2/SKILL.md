---
name: hooks-test
description: Test Claude Code hooks in isolation and via integration. Use when developing, debugging, or validating hook behavior.
---

# Hooks Test

Test hooks at three levels: unit tests (Python), direct invocation, and headless Claude.

> **Reference**: See [reference.md](reference.md) for complete payload schemas.

---

## When to Use

- Developing new hooks
- Debugging hook failures
- Validating hook behavior before deployment
- Regression testing after hook changes

---

## Level 1: Unit Tests (Python)

Test hook logic in isolation using the test harness with pytest.

### Test Harness

Use [templates/test-harness.py](templates/test-harness.py):

```python
from test_harness import create_payload, run_hook, assert_blocked, assert_allowed

def test_blocks_dangerous_commands():
    payload = create_payload("PreToolUse", tool_name="Bash",
                             tool_input={"command": "rm -rf /"})
    result = run_hook("./my-hook.py", payload)
    assert_blocked(result, "dangerous")

def test_allows_safe_commands():
    payload = create_payload("PreToolUse", tool_name="Bash",
                             tool_input={"command": "echo hello"})
    result = run_hook("./my-hook.py", payload)
    assert_allowed(result)

def test_modifies_input():
    payload = create_payload("PreToolUse", tool_name="Write",
                             tool_input={"file_path": "/tmp/test.txt"})
    result = run_hook("./my-hook.py", payload)
    assert_modified_input(result, "file_path", "/safe/path/test.txt")
```

Run with pytest:

```bash
pytest test_my_hook.py -v
```

### Assertions

| Function | Checks |
|----------|--------|
| `assert_blocked(result, msg)` | Exit code 2, stderr contains msg |
| `assert_allowed(result)` | Exit code 0, no block decision |
| `assert_modified_input(result, field, value)` | Exit 0, updatedInput has field |
| `assert_context_added(result, contains)` | Exit 0, context includes text |

---

## Level 2: Direct Invocation (Shell)

Test hooks by calling them directly with JSON payloads.

### Basic Pattern

```bash
echo '{"hook_event_name": "PreToolUse", "tool_name": "Bash", ...}' | ./hook.py
echo "Exit: $?"
```

### With Payload File

```bash
cat > /tmp/payload.json << 'EOF'
{
  "session_id": "test-123",
  "transcript_path": "/tmp/test.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {"command": "rm -rf /"},
  "tool_use_id": "toolu_01ABC"
}
EOF

cat /tmp/payload.json | ./my-hook.py
```

### Exit Code Reference

| Exit Code | Meaning | Check |
|-----------|---------|-------|
| 0 | Success/allow | stdout contains valid JSON or context |
| 2 | Block action | stderr contains reason for Claude |
| Other | Non-blocking error | stderr contains user message |

---

## Level 3: Headless Claude (End-to-End)

Test hooks end-to-end by invoking Claude in headless mode. Claude executes normally,
triggers hooks through its behavior, and you verify the outcome.

### Headless Claude Flags

```bash
claude -p "prompt here" --debug
```

| Flag | Purpose |
|------|---------|
| `-p` / `--print` | Headless mode - prints response and exits |
| `--debug` | Shows hook execution details in stderr |
| `--allowedTools` | Limit which tools Claude can use |
| `--permission-mode` | Control permission behavior |

### Test Patterns

**Test PreToolUse blocks dangerous commands:**

```bash
# Prompt that would trigger dangerous Bash command
output=$(claude -p "delete everything in /tmp" --debug 2>&1)

# Check hook blocked it (look for your hook's block message)
if echo "$output" | grep -q "blocked"; then
    echo "PASS: Hook blocked dangerous command"
fi
```

**Test PostToolUse reacts to failures:**

```bash
# Prompt that triggers a command expected to fail
output=$(claude -p "run: exit 1" --debug 2>&1)

# Check hook's reaction appears in output
echo "$output" | grep -q "Hook command completed"
```

**Test UserPromptSubmit adds context:**

```bash
# Any prompt triggers UserPromptSubmit
output=$(claude -p "hello" --debug 2>&1)

# Verify hook ran
echo "$output" | grep "UserPromptSubmit"
```

**Test Stop hook continues execution:**

```bash
# Prompt that completes, triggering Stop hook
output=$(claude -p "what is 2+2" --debug 2>&1)

# Check if hook caused continuation
echo "$output" | grep "Stop"
```

### Debug Output Format

```
[DEBUG] Executing hooks for PreToolUse:Bash
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Bash"
[DEBUG] Executing hook command: ./my-hook.py with timeout 60000ms
[DEBUG] Hook command completed with status 0: <stdout content>
```

### Automated Test Script

```bash
#!/bin/bash
# integration-test.sh - Run from project root with hook configured
set -e

echo "Test 1: PreToolUse blocks rm -rf"
if claude -p "run: rm -rf /" --debug 2>&1 | grep -qi "block"; then
    echo "  PASS"
else
    echo "  FAIL"
    exit 1
fi

echo "Test 2: Safe commands allowed"
if claude -p "run: echo hello" --debug 2>&1 | grep -q "hello"; then
    echo "  PASS"
else
    echo "  FAIL"
    exit 1
fi

echo "All tests passed"
```

### Isolate Test Configuration

Use `.claude/settings.local.json` for test hooks (not committed):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [".claude/hooks/test-blocker.py"]
      }
    ]
  }
}
```

---

## Payload Examples by Event

### PreToolUse

```python
payload = create_payload("PreToolUse",
    tool_name="Write",
    tool_input={"file_path": "/etc/passwd", "content": "..."})
```

Test: block dangerous paths, allow safe ops, modify input via `updatedInput`

### PostToolUse

```python
payload = create_payload("PostToolUse",
    tool_name="Bash",
    tool_input={"command": "npm test"},
    tool_response={"stdout": "FAILED", "exit_code": 1})
```

Test: react to failures, add context, log operations

### UserPromptSubmit

```python
payload = create_payload("UserPromptSubmit", prompt="delete all files")
```

Test: block prohibited prompts, add context, transform input

### Stop/SubagentStop

```python
payload = create_payload("Stop", stop_hook_active=False)
```

Test: continue on conditions, verify TDD evidence, prevent loops when `stop_hook_active=True`

---

## Debugging Tips

1. **Hook not running?** Check `/hooks` menu, verify matcher syntax
2. **JSON parse error?** Validate hook outputs valid JSON on exit 0
3. **Timeout?** Default is 60s, increase with `"timeout": 120000`
4. **Wrong exit code?** Use `sys.exit(2)` to block, `sys.exit(0)` to allow
5. **Stderr not showing?** Only displayed in verbose mode (`ctrl+o`)

---

## Success Criteria

- [ ] Level 1: Unit tests pass with pytest
- [ ] Level 2: Direct invocation returns expected exit codes
- [ ] Level 3: Headless Claude triggers hook and behaves correctly
- [ ] Exit codes match behavior (0=allow, 2=block)
- [ ] Blocking responses include reason in stderr
- [ ] JSON output is valid and complete

---

## Integration

**Related:**
- Docs: `claude --help` for CLI flags
- Command: `/hooks` to manage hooks
- Config: `.claude/settings.json`, `.claude/settings.local.json`
