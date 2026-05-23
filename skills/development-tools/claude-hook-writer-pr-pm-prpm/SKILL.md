---
name: claude-hook-writer
description: Expert guidance for writing secure, reliable, and performant Claude Code hooks - validates design decisions, enforces best practices, and prevents common pitfalls
---

# Claude Hook Writer

Use this skill when creating or improving Claude Code hooks. This skill ensures hooks are secure, reliable, performant, and follow best practices.

## When to Use This Skill

- Designing a new Claude Code hook
- Reviewing existing hook code
- Debugging hook failures
- Optimizing slow hooks
- Securing hooks that handle sensitive data
- Publishing hooks as PRPM packages

## Core Principles

### 1. Security is Non-Negotiable

Hooks execute automatically with user permissions. They can read, modify, or delete any file the user can access.

**ALWAYS validate and sanitize all input.** Hooks receive JSON via stdin—never trust it blindly.

### 2. Reliability Over Features

A hook that works 99% of the time is a broken hook. Edge cases (Unicode filenames, spaces in paths, missing tools) will happen.

**Test with edge cases before deploying.**

### 3. Performance Matters

Hooks block operations. A 5-second hook means Claude waits 5 seconds before continuing.

**Keep hooks fast. Run heavy operations in background.**

### 4. Fail Gracefully

Missing dependencies, malformed input, and disk errors will occur.

**Handle errors explicitly. Log failures. Return meaningful exit codes.**

## Hook Design Checklist

Before writing code, answer these questions:

### What Event Does This Hook Target?

- `PreToolUse` - Before tool execution (modify input, validate, block)
- `PostToolUse` - After tool completes (format, log, cleanup)
- `UserPromptSubmit` - Before user input processes (validate, enhance)
- `SessionStart` - When Claude Code starts (setup, env check)
- `SessionEnd` - When Claude Code exits (cleanup, persist state)
- `Notification` - During alerts (desktop notifications, logging)
- `Stop` / `SubagentStop` - When responses finish (cleanup, summary)
- `PreCompact` - Before context compaction (save important context)

**Common mistake:** Using PostToolUse for validation (too late—tool already ran). Use PreToolUse to block operations.

### Which Tools Should Trigger This Hook?

Be specific. `matcher: "*"` runs on every tool call.

**Good matchers:**
- `"Write"` - Only file writes
- `"Edit|Write"` - File modifications
- `"Bash"` - Shell commands
- `"mcp__github__*"` - All GitHub MCP tools

**Bad matchers:**
- `"*"` - Everything (use only for logging/metrics)

### What Input Does This Hook Need?

Different tools provide different input. Check what's available:

```bash
# PreToolUse / PostToolUse
{
  "input": {
    "file_path": "/path/to/file.ts",     // Read, Write, Edit
    "command": "npm test",                // Bash
    "old_string": "...",                  // Edit
    "new_string": "..."                   // Edit
  }
}
```

**Validate fields exist before using them:**
```bash
FILE=$(echo "$INPUT" | jq -r '.input.file_path // empty')
if [[ -z "$FILE" ]]; then
  echo "No file path provided" >&2
  exit 1
fi
```

### Should This Be a Command Hook or Prompt Hook?

**Command hooks** (`type: "command"`):
- Fast (milliseconds)
- Deterministic
- Good for: formatting, logging, file checks

**Prompt hooks** (`type: "prompt"`):
- Slow (2-10 seconds)
- Context-aware (uses LLM)
- Good for: complex validation, security analysis, intent detection

**Rule of thumb:** Use command hooks unless you need LLM reasoning.

### What Exit Code Communicates Success/Failure?

- `exit 0` - Success (continue operation)
- `exit 2` - Block operation (show error to Claude)
- `exit 1` or other - Non-blocking error (log but continue)

**For PreToolUse hooks:**
- Exit 2 blocks the tool from running
- Exit 0 allows it (optionally with modified input)

**For PostToolUse hooks:**
- Exit codes don't block (tool already ran)
- Use exit 0 for success, 1 for logging errors

## Security Requirements

### MUST-HAVE Security Checks

Every hook must implement these:

#### 1. Input Validation

```bash
#!/bin/bash
set -euo pipefail  # Exit on errors, undefined vars

INPUT=$(cat)

# Validate JSON parse
if ! FILE=$(echo "$INPUT" | jq -r '.input.file_path // empty' 2>&1); then
  echo "JSON parse failed: $FILE" >&2
  exit 1
fi

# Validate field exists
if [[ -z "$FILE" ]]; then
  echo "No file path in input" >&2
  exit 1
fi
```

#### 2. Path Sanitization

```bash
# Validate file is in project
if [[ "$FILE" != "$CLAUDE_PROJECT_DIR"* ]]; then
  echo "File outside project: $FILE" >&2
  exit 2  # Block operation
fi

# Validate no directory traversal
if [[ "$FILE" == *".."* ]]; then
  echo "Path traversal detected: $FILE" >&2
  exit 2
fi
```

#### 3. Sensitive File Protection

```bash
# Block list (extend as needed)
BLOCKED_PATTERNS=(
  ".env"
  ".env.*"
  "*.pem"
  "*.key"
  "*credentials*"
  ".git/*"
  ".ssh/*"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if [[ "$FILE" == $pattern ]]; then
    echo "Blocked: $FILE matches sensitive pattern $pattern" >&2
    exit 2
  fi
done
```

#### 4. Quote All Variables

Spaces and special characters in paths break unquoted variables:

```bash
# WRONG
cat $FILE              # Breaks on "my file.txt"
prettier --write $FILE # Fails with spaces

# RIGHT
cat "$FILE"              # Handles spaces
prettier --write "$FILE" # Safe
```

#### 5. Use Absolute Paths for Scripts

```bash
# WRONG - relative path might not resolve
./my-script.sh

# RIGHT - explicit path
"${CLAUDE_PLUGIN_ROOT}/scripts/my-script.sh"

# ALSO RIGHT - use full path
/Users/username/.claude/scripts/my-script.sh
```

## Reliability Requirements

### Handle Missing Dependencies

```bash
# Check tool exists
if ! command -v prettier &> /dev/null; then
  echo "prettier not installed, skipping" >&2
  exit 0  # Success exit (just skip)
fi

# Check file exists
if [[ ! -f "$FILE" ]]; then
  echo "File not found: $FILE" >&2
  exit 1
fi
```

### Set Timeouts

Default is 60 seconds. For slow operations, set explicit timeout:

```json
{
  "hooks": [{
    "type": "command",
    "command": "./slow-operation.sh",
    "timeout": 10000  // 10 seconds
  }]
}
```

Or run in background:

```bash
# Don't block Claude
(heavy_operation "$FILE" &)
exit 0
```

### Log Errors Properly

```bash
LOG_FILE=~/.claude-hooks/my-hook.log

# Log to stderr (shown in transcript)
echo "Hook failed: some reason" >&2

# Or log to file (for debugging)
echo "[$(date)] Error: some reason" >> "$LOG_FILE"
```

**Don't log to stdout** unless you want output in Claude's transcript.

### Test With Edge Cases

Test files:
- `"file with spaces.txt"`
- `"文件.txt"` (Unicode)
- `"src/deep/nested/path/file.tsx"` (deep paths)
- `"/absolute/path.txt"` (absolute paths)
- `"../../../etc/passwd"` (traversal attempts)

Test input:
- Malformed JSON
- Missing fields
- Empty strings
- `null` values

## Performance Requirements

### Keep Hooks Fast

Target < 100ms for PreToolUse hooks. Longer hooks block Claude visibly.

**Slow operations:**
- Running tests: Run in background or use PostToolUse
- Type checking: Cache results by file hash
- Network calls: Avoid in hooks (use subagents instead)
- Heavy linting: Only lint changed file, not entire project

### Use Specific Matchers

```json
// BAD - runs on everything
{"matcher": "*", ...}

// GOOD - only file writes
{"matcher": "Write", ...}

// BETTER - only TypeScript writes
// (check file extension in hook)
{"matcher": "Write", ...}
```

### Dedupe Expensive Operations

If multiple hooks match, they run in parallel. Dedupe with locks:

```bash
LOCK_FILE="/tmp/claude-hook-${SESSION_ID}-${HOOK_NAME}.lock"

if [[ -f "$LOCK_FILE" ]]; then
  exit 0  # Already running
fi

touch "$LOCK_FILE"
trap "rm -f '$LOCK_FILE'" EXIT  # Clean up on exit

# Do work here
expensive_operation
```

## Code Templates

### Template: Format On Save Hook

```bash
#!/bin/bash
set -euo pipefail

# Parse input
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.input.file_path // empty')

# Validate
[[ -n "$FILE" ]] || exit 0
[[ -f "$FILE" ]] || exit 0
[[ "$FILE" == "$CLAUDE_PROJECT_DIR"* ]] || exit 0

# Check formatter installed
if ! command -v prettier &> /dev/null; then
  exit 0
fi

# Format by extension
case "$FILE" in
  *.ts|*.tsx|*.js|*.jsx)
    prettier --write "$FILE" 2>/dev/null || exit 0
    ;;
  *.py)
    black "$FILE" 2>/dev/null || exit 0
    ;;
  *.go)
    gofmt -w "$FILE" 2>/dev/null || exit 0
    ;;
esac
```

**JSON config:**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "/path/to/format-on-save.sh",
        "timeout": 5000
      }]
    }]
  }
}
```

### Template: Block Sensitive Files Hook

```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.input.file_path // empty')

[[ -n "$FILE" ]] || exit 0

# Sensitive patterns
BLOCKED=(
  ".env"
  ".env.*"
  "*.pem"
  "*.key"
  "*secret*"
  "*credential*"
  ".git/*"
)

for pattern in "${BLOCKED[@]}"; do
  # Use case for glob matching
  case "$FILE" in
    $pattern)
      echo "🚫 Blocked: $FILE is a sensitive file" >&2
      echo "   Pattern: $pattern" >&2
      exit 2  # Block operation
      ;;
  esac
done

exit 0  # Allow
```

**JSON config:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "/path/to/block-sensitive.sh"
      }]
    }]
  }
}
```

### Template: Command Logger Hook

```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.input.command // empty')

[[ -n "$COMMAND" ]] || exit 0

LOG_FILE=~/claude-commands.log
mkdir -p "$(dirname "$LOG_FILE")"

# Log with timestamp and context
{
  echo "---"
  echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "Directory: $CLAUDE_CURRENT_DIR"
  echo "Command: $COMMAND"
} >> "$LOG_FILE"

exit 0
```

**JSON config:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "/path/to/command-logger.sh"
      }]
    }]
  }
}
```

### Template: Prompt-Based Security Hook

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "prompt",
        "prompt": "Analyze the file content being written to ${input.file_path}. Check if it contains: hardcoded API keys, AWS credentials, private keys, passwords, or secrets. Return {\"decision\": \"block\", \"reason\": \"<specific issue>\"} if found, otherwise {\"decision\": \"allow\"}.",
        "schema": {
          "type": "object",
          "properties": {
            "decision": {"enum": ["allow", "block"]},
            "reason": {"type": "string"}
          },
          "required": ["decision"]
        }
      }]
    }]
  }
}
```

**Use sparingly:** Prompt hooks take 2-10 seconds. Only use for critical security checks.

## Testing Hooks

### Manual Testing

Create test input:

```bash
# Test with sample JSON
echo '{
  "session_id": "test",
  "input": {
    "file_path": "/tmp/test.ts"
  }
}' | ./my-hook.sh

# Check exit code
echo $?  # 0 = success, 2 = blocked, 1 = error
```

### Edge Case Testing

```bash
#!/bin/bash
# test-hook.sh

HOOK=./my-hook.sh

test_case() {
  local description="$1"
  local input="$2"
  local expected_exit="$3"

  echo "Testing: $description"

  echo "$input" | $HOOK
  actual_exit=$?

  if [[ $actual_exit -eq $expected_exit ]]; then
    echo "  ✓ PASS"
  else
    echo "  ✗ FAIL (expected exit $expected_exit, got $actual_exit)"
    return 1
  fi
}

# Test cases
test_case "Normal file" \
  '{"input":{"file_path":"/tmp/test.ts"}}' \
  0

test_case "Sensitive .env file" \
  '{"input":{"file_path":".env"}}' \
  2

test_case "File with spaces" \
  '{"input":{"file_path":"/tmp/my file.ts"}}' \
  0

test_case "Missing file_path" \
  '{"input":{}}' \
  1

test_case "Malformed JSON" \
  'not json' \
  1

echo "All tests passed"
```

### Integration Testing

1. Register hook in Claude Code
2. Trigger the event (write file, run command)
3. Check transcript (Ctrl-R) for hook output
4. Verify expected behavior

## Publishing Hooks as PRPM Packages

### Package Structure

```
my-hook/
├── prpm.json          # Package manifest
├── hook.json          # Hook configuration
├── scripts/
│   └── my-hook.sh     # Hook script
└── README.md          # Documentation
```

### prpm.json

```json
{
  "name": "@yourname/my-hook",
  "version": "1.0.0",
  "description": "Brief description of what hook does (shown in search)",
  "author": "Your Name",
  "format": "claude",
  "subtype": "hook",
  "tags": [
    "formatting",
    "security",
    "automation"
  ],
  "main": "hook.json",
  "scripts": {
    "test": "./test-hook.sh"
  }
}
```

### hook.json

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/my-hook.sh",
        "timeout": 5000
      }]
    }]
  }
}
```

**Use `${CLAUDE_PLUGIN_ROOT}`** to reference scripts—expands to hook installation directory.

### Advanced Hook Configuration

All hook types support optional fields for controlling execution behavior:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "./my-hook.sh",
        "timeout": 5000,
        "continue": true,              // Whether Claude continues after hook (default: true)
        "stopReason": "string",        // Message shown when continue is false
        "suppressOutput": false,       // Hide stdout from transcript (default: false)
        "systemMessage": "string"      // Warning message shown to user
      }]
    }]
  }
}
```

#### `continue` (boolean, default: true)

Controls whether Claude continues after hook execution.

**When to use `false`:**
- Security hooks that must block operations
- Validation hooks that found critical errors
- Hooks that require user intervention

```json
{
  "type": "command",
  "command": "./validate-security.sh",
  "continue": false,
  "stopReason": "Security validation failed. Please review the detected issues before proceeding."
}
```

**Exit code interaction:**
- If hook exits with code 2 (block): `continue` is ignored, operation is blocked
- If hook exits with code 0 or 1: `continue` field determines behavior

#### `stopReason` (string)

Message displayed to user when `continue: false`. Should explain why execution stopped and what action is needed.

```json
{
  "continue": false,
  "stopReason": "Pre-commit checks failed. Fix linting errors and try again."
}
```

#### `suppressOutput` (boolean, default: false)

Hides hook stdout from transcript mode (Ctrl-R). Stderr is always shown.

**When to use `true`:**
- Hooks that produce verbose output
- Debugging logs not useful to users
- Noisy background operations

```json
{
  "type": "command",
  "command": "./sync-to-cloud.sh",
  "suppressOutput": true  // Don't show sync progress in transcript
}
```

**Note:** Always show critical errors via stderr, as stderr is never suppressed.

#### `systemMessage` (string)

Warning or info message shown to user when hook executes. Useful for non-blocking warnings.

```json
{
  "type": "command",
  "command": "./check-dependencies.sh",
  "systemMessage": "⚠️  Some dependencies are outdated. Consider running 'npm update'."
}
```

**Difference from `stopReason`:**
- `systemMessage`: Informational, Claude continues
- `stopReason`: Critical, requires `continue: false`

### README.md

```markdown
# My Hook

Brief description.

## What It Does

- Clear, specific bullet points
- Mention which events it triggers on
- Mention which tools it matches

## Installation

```bash
prpm install @yourname/my-hook
```

## Requirements

- prettier (install: `npm install -g prettier`)
- jq (install: `brew install jq`)

## Configuration

Optional: How to customize behavior.

## Examples

Show example output or behavior.

## Troubleshooting

Common issues and fixes.
```

### Publishing

```bash
# Test locally first
prpm test

# Publish
prpm publish

# Version bumps
prpm publish patch  # 1.0.0 -> 1.0.1
prpm publish minor  # 1.0.0 -> 1.1.0
prpm publish major  # 1.0.0 -> 2.0.0
```

## Common Pitfalls

### ❌ Pitfall 1: Not Quoting Variables

```bash
# BREAKS on spaces
prettier --write $FILE

# SAFE
prettier --write "$FILE"
```

### ❌ Pitfall 2: Trusting Input

```bash
# DANGEROUS - no validation
FILE=$(jq -r '.input.file_path')
rm "$FILE"

# SAFE - validate first
FILE=$(jq -r '.input.file_path // empty')
[[ "$FILE" == "$CLAUDE_PROJECT_DIR"* ]] || exit 2
[[ "$FILE" != *".env"* ]] || exit 2
rm "$FILE"
```

### ❌ Pitfall 3: Blocking Operations Too Long

```bash
# BLOCKS Claude for 30 seconds
npm test

# RUN IN BACKGROUND
(npm test &)
exit 0
```

### ❌ Pitfall 4: Wrong Exit Code

```bash
# PreToolUse hook that should block

if [[ $FILE == ".env" ]]; then
  echo "Don't edit .env" >&2
  exit 1  # WRONG - doesn't block, just logs error
fi

# RIGHT
if [[ $FILE == ".env" ]]; then
  echo "Blocked: .env is protected" >&2
  exit 2  # Blocks operation
fi
```

### ❌ Pitfall 5: Logging to stdout

```bash
# WRONG - appears in transcript
echo "Hook running..."

# RIGHT - stderr or file
echo "Hook running..." >&2
# or
echo "Hook running..." >> ~/.claude-hooks/debug.log
```

### ❌ Pitfall 6: Assuming Tools Exist

```bash
# BREAKS if prettier not installed
prettier --write "$FILE"

# SAFE
if command -v prettier &>/dev/null; then
  prettier --write "$FILE"
fi
```

## Debugging Hooks

### Enable Verbose Logging

```bash
#!/bin/bash
set -x  # Print commands as they execute
```

### Check Transcript

Run Claude Code with Ctrl-R (transcript mode) to see hook execution:

```
PreToolUse hook: ./my-hook.sh
  stdout: Formatted file.ts
  stderr:
  exit: 0
  duration: 47ms
```

### Test JSON Parsing

```bash
# Debug what jq extracts
INPUT=$(cat)
echo "$INPUT" | jq '.' >&2  # Show full JSON
echo "$INPUT" | jq -r '.input.file_path' >&2  # Show field
```

### Check Environment Variables

```bash
echo "PROJECT_DIR: $CLAUDE_PROJECT_DIR" >&2
echo "CURRENT_DIR: $CLAUDE_CURRENT_DIR" >&2
echo "SESSION_ID: $SESSION_ID" >&2
echo "PLUGIN_ROOT: $CLAUDE_PLUGIN_ROOT" >&2
```

## Quick Reference

### Exit Codes
- `0` = Success (continue)
- `2` = Block operation (PreToolUse only)
- `1` or other = Non-blocking error

### Hook Configuration Fields
**Required:**
- `type` - "command" or "prompt"
- `command` or `prompt` - Script path or prompt text

**Optional:**
- `timeout` - Max execution time in ms (default: 60000)
- `continue` - Continue after hook? (default: true)
- `stopReason` - Message when continue=false
- `suppressOutput` - Hide stdout from transcript (default: false)
- `systemMessage` - Warning message to user

### Environment Variables
- `$CLAUDE_PROJECT_DIR` - Project root
- `$CLAUDE_CURRENT_DIR` - Current directory
- `$SESSION_ID` - Session identifier
- `$CLAUDE_PLUGIN_ROOT` - Hook installation directory
- `$CLAUDE_ENV_FILE` - File for persisting vars

### JSON Input Structure
```json
{
  "session_id": "...",
  "transcript_path": "...",
  "current_dir": "...",
  "input": {
    // Tool-specific fields
  }
}
```

### Common jq Patterns
```bash
# Extract with default
$(jq -r '.input.file_path // empty')

# Extract array
$(jq -r '.input.files[]')

# Check field exists
if jq -e '.input.file_path' >/dev/null; then

# Parse entire object
INPUT_OBJ=$(jq '.input')
```

## Final Checklist

Before publishing:

- [ ] Validates all stdin input
- [ ] Quotes all variables
- [ ] Uses absolute paths for scripts
- [ ] Blocks sensitive files
- [ ] Handles missing tools gracefully
- [ ] Sets reasonable timeout
- [ ] Logs errors to stderr or file
- [ ] Tests with edge cases
- [ ] Tests in real Claude session
- [ ] Documents dependencies
- [ ] README includes examples
- [ ] Semantic version number
- [ ] Clear description and tags

## Resources

- [Claude Code Hooks Docs](https://code.claude.com/docs/en/hooks)
- [Claude Hooks Best Practices Blog](/blog/claude-hooks-best-practices)
- [PRPM Hook Packages](https://prpm.dev/packages?format=claude&subtype=hook)
- [Hook Examples Repo](https://github.com/pr-pm/claude-hooks-examples)
