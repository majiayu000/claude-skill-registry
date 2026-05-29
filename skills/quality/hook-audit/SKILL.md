---
name: hook-audit
description: Audits Claude Code hooks for correctness, safety, and performance. Use when reviewing, validating, or debugging hooks, checking exit codes, error handling, or learning hook best practices.
allowed-tools: [Read, Grep, Glob, Bash]
# model: haiku
---

## Reference Files

Advanced hook patterns and best practices:

- [exit-codes.md](exit-codes.md) - Exit code semantics (0=allow, 2=block) with examples
- [json-handling.md](json-handling.md) - Safe JSON stdin parsing patterns
- [error-patterns.md](error-patterns.md) - Error handling and graceful degradation
- [performance.md](performance.md) - Timeout guidelines and optimization
- [examples.md](examples.md) - Good vs bad hook patterns with before/after examples

---

# Hook Audit

Performs comprehensive security and quality audits of Claude Code hooks, ensuring correct JSON handling, exit code semantics, error handling, and performance.

## Quick Start

**Audit a single hook**:

```text
User: "Audit my validate-config.py hook"
Assistant: [Reads hook file, checks patterns, generates report]
```

**Audit all hooks**:

```text
User: "Check all my hooks for best practices"
Assistant: [Finds all hooks, analyzes each, generates consolidated report]
```

**Fix specific issues**:

```text
User: "My hook is blocking on errors"
Assistant: [Analyzes error handling, suggests fixes]
```

## Hook Audit Checklist

Use this checklist to audit any Claude Code hook:

### Critical Requirements

- [ ] **Shebang Line**: Correct interpreter for hook type (see Shebang Standards below)
  - Python hooks: `#!/usr/bin/env python3`
  - Bash hooks: `#!/bin/bash` (NOT `#!/usr/bin/env bash` or `#!/bin/sh`)
- [ ] **JSON stdin Handling**: Safe parsing with try/except and `.get()` methods
- [ ] **Exit Codes**: Correct semantics (0=allow, 2=block, never 1)
- [ ] **Error Handling**: Exit 0 on hook errors (never block on hook failures)
- [ ] **Settings.json Registration**: Hook is registered with correct matcher and timeout

### High Priority

- [ ] **Timeout**: Configured appropriately for hook type (PreToolUse <500ms, PostToolUse <2s)
- [ ] **File Type Validation**: Checks file type before processing
- [ ] **Error Messages**: Clear messages to stderr
- [ ] **Performance**: Executes within reasonable time

### Medium Priority

- [ ] **Naming Convention**: Uses kebab-case naming
- [ ] **Documentation**: Header comments explain purpose and usage
- [ ] **Pattern Consistency**: Follows existing hook patterns
- [ ] **Security**: No security vulnerabilities or unsafe operations

## Audit Workflow

### Step 1: Identify Hook Type

Determine the hook type from settings.json registration:

- **PreToolUse**: Runs before tool execution, can block operations
- **PostToolUse**: Runs after successful tool execution
- **Notification**: Runs on specific events (Idle, etc.)
- **SessionStart**: Runs once at session start

Hook type determines performance requirements and exit code handling.

### Step 2: Read Hook File and Check Syntax

Read the hook file and verify basic syntax:

```bash
# For Python hooks
python3 -m py_compile hook-file.py

# For Bash hooks
bash -n hook-file.sh
```

Check for:

- Correct shebang line
- Executable permissions
- Valid syntax

### Step 3: Verify JSON Handling Pattern

For hooks that receive JSON stdin (PreToolUse, PostToolUse), verify safe parsing:

**Python Pattern**:

```python
try:
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")
    content = data.get("tool_input", {}).get("content", "")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block on parsing errors
```

**Bash Pattern**:

```bash
# Read stdin to variable
stdin_data=$(cat)

# Parse specific fields with jq
file_path=$(echo "$stdin_data" | jq -r '.tool_input.file_path // empty')
```

**Critical**: Use `.get()` with defaults, never direct key access.

### Step 4: Check Exit Code Usage

Verify exit codes follow correct semantics:

- **Exit 0**: Allow operation (or hook encountered error)
- **Exit 2**: Block operation (validation failed)
- **Never Exit 1**: Reserved, don't use

**Pattern to Check**:

```python
# Good: Block on validation failure
if errors:
    print(f"Validation errors:", file=sys.stderr)
    sys.exit(2)

# Good: Allow on hook error
except Exception as e:
    print(f"Hook error: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block user

# Bad: Exit 1 or non-zero on errors
sys.exit(1)  # ✗ Wrong, use 0 or 2
```

For details on exit code patterns, see [exit-codes.md](exit-codes.md).

### Step 5: Review Error Handling

Check that hooks degrade gracefully:

1. **Dependency Check**: Missing dependencies exit 0 (don't block)
2. **Try/Except**: All operations wrapped in try/except
3. **Error Exit**: Exceptions exit 0, not 1 or other codes
4. **Clear Messages**: Errors printed to stderr with context

**Example Pattern**:

```python
try:
    import yaml
except ImportError:
    print("Warning: PyYAML not installed, skipping", file=sys.stderr)
    sys.exit(0)  # Don't block user

try:
    # Hook logic here
    ...
except Exception as e:
    print(f"Error in hook: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block user
```

For error handling patterns, see [error-patterns.md](error-patterns.md).

### Step 6: Validate settings.json Registration

Check that the hook is properly registered:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "command": "python3 ~/.claude/hooks/validate-config.py",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

Verify:

- Hook file exists at specified path
- Matcher pattern is correct for intended triggers
- Timeout is appropriate for hook type
- Hook type (PreToolUse/PostToolUse/etc.) matches purpose

### Step 7: Generate Report

Create a structured audit report following the output format below.

## Hook Type Reference

### PreToolUse Hooks

**Purpose**: Validate operations before execution
**Can Block**: Yes (exit 2 to block)
**Performance Target**: <500ms (blocks user interaction)
**JSON stdin**: Tool name and input parameters

**Example Matchers**:

- `Edit|Write` - Validate before file modifications
- `Bash` - Validate before bash commands
- `.*` - All tools (use cautiously)

**Common Uses**:

- File content validation (YAML, config files)
- Security checks (prevent writing secrets)
- Policy enforcement

### PostToolUse Hooks

**Purpose**: Process results after successful execution
**Can Block**: No (exit code ignored, operation already completed)
**Performance Target**: <2s (runs after operation)
**JSON stdin**: Tool name, input, and output

**Common Uses**:

- Auto-formatting (gofmt, prettier)
- Logging operations
- Side effects (notifications, metrics)

### Notification Hooks

**Purpose**: React to events
**Can Block**: No
**Performance Target**: <100ms (quick notifications)
**JSON stdin**: Event-specific data

**Common Uses**:

- Desktop notifications (Idle event)
- Metrics tracking
- Alert systems

### SessionStart Hooks

**Purpose**: Initialize session state
**Can Block**: No
**Performance Target**: <5s (one-time initialization)
**JSON stdin**: Session metadata

**Common Uses**:

- Load git repository context
- Set environment variables
- Initialize session state

## Common Issues

### Missing try/except

**Problem**: Hook crashes on errors, blocks user

```python
# ✗ Bad: No error handling
data = json.load(sys.stdin)
file_path = data["tool_input"]["file_path"]
```

**Fix**: Wrap in try/except, exit 0 on errors

```python
# ✓ Good: Safe error handling
try:
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(0)
```

### Wrong Exit Codes

**Problem**: Using exit 1 instead of 0 or 2

```python
# ✗ Bad: Exit 1
if error:
    sys.exit(1)
```

**Fix**: Use exit 2 to block, exit 0 to allow

```python
# ✓ Good: Correct exit codes
if validation_failed:
    sys.exit(2)  # Block operation

if hook_error:
    sys.exit(0)  # Don't block user
```

### Blocking on Hook Errors

**Problem**: Hook exits non-zero on internal errors, blocks user

```python
# ✗ Bad: Blocks user on missing dependency
import yaml  # Crashes if not installed
```

**Fix**: Check dependencies, exit 0 on errors

```python
# ✓ Good: Graceful degradation
try:
    import yaml
except ImportError:
    print("Warning: PyYAML not installed", file=sys.stderr)
    sys.exit(0)
```

### Slow Performance

**Problem**: PreToolUse hook takes >1s, blocks user

**Fix**: Optimize or move to PostToolUse

- Cache expensive operations
- Use faster parsing (regex instead of full AST)
- Move non-critical checks to PostToolUse

For performance optimization, see [performance.md](performance.md).

## Shebang Standards

All hooks MUST use the correct shebang line for their language. Different shebangs are required for different hook types.

### Bash Hooks: `#!/bin/bash`

**All bash hooks MUST use**:

`#!/bin/bash`

**NOT**:

```bash
#!/bin/sh              # Too restrictive - lacks bash features
#!/usr/bin/env bash    # Unnecessary indirection for hooks
```

**Why `#!/bin/bash` for hooks**:

1. **Bash Features**: Hooks may use bash-specific features:
   - Arrays for processing multiple items
   - `[[` conditional expressions for safer string comparisons
   - `jq` integration patterns with process substitution
   - Extended pattern matching

2. **Consistency**: All hooks should behave identically across environments

3. **Performance**: Direct path avoids `env` lookup overhead
   - Matters for PreToolUse hooks on critical path
   - Faster startup time (<1ms vs ~10ms)

4. **Reliability**: macOS and Linux both guarantee bash at `/bin/bash`
   - Universal location across platforms Claude Code supports
   - No PATH dependency issues

5. **POSIX sh Limitations**: `/bin/sh` might be dash, ash, or other minimal shells
   - Missing bash arrays, `[[` tests, process substitution
   - Different behavior across systems

**Current hooks using `#!/bin/bash`** (all correct):

- `auto-format.sh`
- `load-session-context.sh`
- `log-git-commands.sh`
- `notify-idle.sh`

### Python Hooks: `#!/usr/bin/env python3`

**All Python hooks MUST use**:

```python
#!/usr/bin/env python3
```

**Why `#!/usr/bin/env python3` for Python**:

1. **Python Location Varies**: Python may be in `/usr/bin/`, `/usr/local/bin/`, virtualenv, etc.
2. **Virtual Environments**: `env` respects activated virtualenvs
3. **Version Clarity**: `python3` is explicit (not `python` which might be Python 2)
4. **Cross-Platform**: Works on systems with non-standard Python installations

**Current hooks using `#!/usr/bin/env python3`** (all correct):

- `validate-config.py`
- `validate-markdown.py`

### Validation

To verify hooks comply with shebang standards:

**Check all bash hooks**:

```bash
for hook in ~/.claude/hooks/*.sh; do
  shebang=$(head -1 "$hook")
  if [[ "$shebang" != "#!/bin/bash" ]]; then
    echo "ERROR: $hook uses wrong shebang: $shebang"
    echo "  Expected: #!/bin/bash"
  fi
done
```

**Check all Python hooks**:

```bash
for hook in ~/.claude/hooks/*.py; do
  shebang=$(head -1 "$hook")
  if [[ "$shebang" != "#!/usr/bin/env python3" ]]; then
    echo "ERROR: $hook uses wrong shebang: $shebang"
    echo "  Expected: #!/usr/bin/env python3"
  fi
done
```

### Note on Example Scripts vs Hooks

**Example scripts** (in skills, not hooks) may use `#!/usr/bin/env bash` because:

- They're intended for distribution across different systems
- Users might install them in non-standard locations
- Portability is more important than microsecond performance

**Hooks are different** because:

- They live in `~/.claude/hooks/` (fixed location)
- They run on every tool invocation (performance matters)
- They need bash features (reliability matters)
- They don't need portability (only run locally)

## Report Format

Generate audit reports in this standardized structure:

```markdown
# Hook Audit Report: {hook-name}

**Hook**: {name}
**Type**: PreToolUse | PostToolUse | Notification | SessionStart
**File**: {path}
**Audited**: {YYYY-MM-DD HH:MM}

## Summary

{1-2 sentence overview of hook and audit results}

## Compliance Status

**Overall**: PASS | NEEDS WORK | FAIL

- **Shebang Line**: ✓/✗
- **JSON Handling**: ✓/✗
- **Exit Codes**: ✓/✗
- **Error Handling**: ✓/✗
- **Performance**: ✓/✗
- **Registration**: ✓/✗

## Critical Issues

{List of critical failures that must be fixed}

### {Issue Title}

- **Severity**: CRITICAL
- **Location**: {file}:{line}
- **Issue**: {description}
- **Fix**: {specific remediation}

## High Priority Issues

{List of important improvements}

### {Issue Title}

- **Severity**: HIGH
- **Location**: {file}:{line}
- **Issue**: {description}
- **Fix**: {specific remediation}

## Medium Priority Issues

{List of best practice violations}

### {Issue Title}

- **Severity**: MEDIUM
- **Location**: {file}:{line}
- **Issue**: {description}
- **Fix**: {specific remediation}

## Recommendations

1. **Critical**: {must-fix items for safety/correctness}
2. **Important**: {should-fix items for reliability}
3. **Nice-to-Have**: {polish items for maintainability}

## Next Steps

{Specific actions to improve hook quality and safety}
```

## Integration

### With Other Auditors

- **evaluator**: General correctness and clarity
- **test-runner**: Functional testing
- **audit-coordinator**: Orchestrates multiple auditors

### With Hook Validation

The `validate-config.py` hook validates YAML frontmatter in agents/skills. The audit-hook validates hooks themselves - a meta-validation.

## Examples

For detailed examples of good and bad hook patterns, including before/after refactoring, see [examples.md](examples.md).

**Quick Examples**:

**Good Hook** (validate-config.py):

- ✓ Safe JSON parsing with try/except
- ✓ Correct exit codes (0 on error, 2 to block)
- ✓ Dependency checking (PyYAML)
- ✓ Clear error messages
- ✓ File type validation

**Simple Hook** (log-git-commands.sh):

- ✓ Basic bash pattern
- ✓ Safe jq parsing
- ✓ Always exits 0 (informational)
- ✓ Clear purpose

For complete examples and anti-patterns, see the references above.
