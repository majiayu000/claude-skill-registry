---
name: claude-hook-writer
description: Expert guidance for writing secure, reliable, and performant Claude Code hooks - validates design decisions, enforces best practices, and prevents common pitfalls. Use when creating, reviewing, or debugging Claude Code hooks.
metadata:
  version: 2.0.0
  author: Claude Skills Maintainers
  last_verified: 2025-12-17
  optimization_date: 2025-12-17
  token_savings: ~55%
  errors_prevented: 5
---

# Claude Hook Writer

**Status**: Production Ready
**Version**: 2.0.0 (Optimized with progressive disclosure)
**Last Updated**: 2025-12-17

---

## Overview

Expert guidance for writing secure, reliable, and performant Claude Code hooks. This skill validates design decisions, enforces best practices, and prevents common pitfalls.

---

## When to Use This Skill

- Designing a new Claude Code hook
- Reviewing existing hook code
- Debugging hook failures
- Optimizing slow hooks
- Securing hooks that handle sensitive data
- Publishing hooks as PRPM packages

---

## Core Principles

### 1. Security is Non-Negotiable

Hooks execute automatically with user permissions and can read, modify, or delete any file the user can access.

**ALWAYS validate and sanitize all input.** Hooks receive JSON via stdin—never trust it blindly.

**For complete security patterns**: Load `references/security-requirements.md` when implementing validation or securing hooks.

### 2. Reliability Over Features

A hook that works 99% of the time is a broken hook. Edge cases (Unicode filenames, spaces in paths, missing tools) will happen.

**Test with edge cases before deploying.**

**For reliability patterns**: Load `references/reliability-performance.md` when handling errors or edge cases.

### 3. Performance Matters

Hooks block operations. A 5-second hook means Claude waits 5 seconds before continuing.

**Keep hooks fast. Run heavy operations in background.**

**For performance optimization**: Load `references/reliability-performance.md` when optimizing hook speed.

### 4. Fail Gracefully

Missing dependencies, malformed input, and disk errors will occur.

**Handle errors explicitly. Log failures. Return meaningful exit codes.**

---

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

---

## Top 5 Pitfalls (Must Know)

### Pitfall #1: Not Quoting Variables

**Error**: Hooks break on filenames with spaces or special characters

**Why**: Unquoted variables split on whitespace

**Example**:
```bash
# ❌ WRONG - breaks on "my file.txt"
cat $FILE
prettier --write $FILE
rm $FILE

# ✅ RIGHT - handles spaces and special chars
cat "$FILE"
prettier --write "$FILE"
rm "$FILE"
```

**Why this matters**: Files with spaces (`"my file.txt"`), Unicode (`"文件.txt"`), or special chars (`"file (1).txt"`) are common.

**For quoting best practices**: Load `references/security-requirements.md` for comprehensive input handling patterns.

---

### Pitfall #2: Trusting Input Without Validation

**Error**: Hook executes on malicious or malformed input

**Why**: Not validating JSON fields before using them

**Example**:
```bash
# ❌ DANGEROUS - no validation
FILE=$(jq -r '.input.file_path')
rm "$FILE"  # Could delete ../../../etc/passwd

# ✅ SAFE - validate first
FILE=$(jq -r '.input.file_path // empty')
[[ -n "$FILE" ]] || exit 1
[[ "$FILE" == "$CLAUDE_PROJECT_DIR"* ]] || exit 2
[[ "$FILE" != *".."* ]] || exit 2
rm "$FILE"
```

**Why this matters**: Prevents path traversal attacks, protects files outside project, prevents malformed input crashes.

**For complete security patterns**: Load `references/security-requirements.md`.

---

### Pitfall #3: Blocking Operations Too Long

**Error**: Hook takes 30+ seconds, blocking Claude

**Why**: Running expensive operations (tests, builds) synchronously in hook

**Example**:
```bash
# ❌ BLOCKS Claude for 30 seconds
npm test
npm run build

# ✅ RUN IN BACKGROUND - returns immediately
(npm test > /tmp/test-results.log 2>&1 &)
(npm run build > /tmp/build.log 2>&1 &)
exit 0
```

**Why this matters**: Slow hooks create bad user experience. Target < 100ms for PreToolUse, < 500ms for PostToolUse.

**For performance optimization**: Load `references/reliability-performance.md`.

---

### Pitfall #4: Wrong Exit Code for Blocking

**Error**: PreToolUse hook doesn't actually block the operation

**Why**: Using exit 1 instead of exit 2

**Example**:
```bash
# ❌ WRONG - logs error but doesn't block
if [[ $FILE == ".env" ]]; then
  echo "Don't edit .env" >&2
  exit 1  # Tool still runs!
fi

# ✅ RIGHT - actually blocks
if [[ $FILE == ".env" ]]; then
  echo "Blocked: .env is protected" >&2
  exit 2  # Tool is blocked
fi
```

**Why this matters**: Exit 1 only logs errors. Exit 2 is required to block in PreToolUse hooks.

**For exit code patterns**: Load `references/hook-templates.md` for complete hook response patterns.

---

### Pitfall #5: Assuming Tools Exist

**Error**: Hook crashes when dependency is missing

**Why**: Not checking if tool is installed before using

**Example**:
```bash
# ❌ BREAKS if prettier not installed
prettier --write "$FILE"

# ✅ SAFE - check first
if command -v prettier &>/dev/null; then
  prettier --write "$FILE"
else
  echo "prettier not installed, skipping" >&2
  exit 0  # Success exit, just skip
fi
```

**Why this matters**: Users may not have all tools installed. Hooks should degrade gracefully.

**For reliability patterns**: Load `references/reliability-performance.md`.

---

## Critical Rules

### Always Do

✅ Validate all JSON input before using (`jq -r '... // empty'`)
✅ Quote all variables containing paths or user input
✅ Use absolute paths for scripts (`${CLAUDE_PLUGIN_ROOT}/...`)
✅ Block sensitive files (`.env`, `*.key`, credentials)
✅ Check if required tools exist (`command -v toolname`)
✅ Set reasonable timeouts (< 5s for PreToolUse)
✅ Run heavy operations in background
✅ Test with edge cases (spaces, Unicode, special chars)
✅ Use exit 2 to block in PreToolUse hooks
✅ Log errors to stderr or file, not stdout

### Never Do

❌ Trust JSON input without validation
❌ Use unquoted variables ($FILE instead of "$FILE")
❌ Use relative paths for scripts
❌ Skip path sanitization (check for `..`, validate in project)
❌ Assume tools are installed
❌ Block for > 1 second in PreToolUse hooks
❌ Use exit 1 when you mean to block (use exit 2)
❌ Log sensitive data to stdout or files
❌ Use `matcher: "*"` unless truly necessary

---

## When to Load References

Load reference files when working on specific hook aspects:

### Security Requirements (`references/security-requirements.md`)
Load when:
- Implementing input validation and sanitization
- Securing hooks that handle sensitive data
- Blocking sensitive files (`.env`, keys, credentials)
- Preventing path traversal attacks
- Understanding security vulnerabilities and best practices
- Testing security with malicious input

### Reliability & Performance (`references/reliability-performance.md`)
Load when:
- Handling missing dependencies or tools
- Setting timeouts and handling slow operations
- Optimizing hook performance (< 100ms target)
- Running heavy operations in background
- Caching expensive results
- Testing with edge cases (Unicode, spaces, deep paths)
- Deduplicating expensive operations

### Code Templates (`references/code-templates.md`)
Load when:
- Starting a new hook and need working examples
- Implementing format-on-save functionality
- Blocking sensitive files from modification
- Logging commands or operations
- Using prompt-based security analysis
- Customizing templates for specific use cases

### Testing & Debugging (`references/testing-debugging.md`)
Load when:
- Writing test cases for hooks
- Debugging hook failures or unexpected behavior
- Testing with edge cases (malformed JSON, missing fields)
- Checking hook execution in transcript (Ctrl-R)
- Profiling hook performance
- Creating automated test suites

### Publishing Guide (`references/publishing-guide.md`)
Load when:
- Publishing hooks to PRPM registry
- Creating package manifest (prpm.json)
- Configuring hook.json with advanced options
- Using `continue`, `stopReason`, `suppressOutput`, `systemMessage`
- Writing README.md for users
- Understanding versioning and publishing commands

### Quick Reference (`references/quick-reference.md`)
Load when:
- Need quick syntax lookup (exit codes, jq patterns)
- Looking up environment variables
- Finding common bash patterns (file validation, background execution)
- Checking hook events and matchers
- Need performance tips summary
- Looking up JSON input structure

---

## Final Checklist

Before publishing a hook:

- [ ] Validates all stdin input with jq
- [ ] Quotes all variables
- [ ] Uses absolute paths for scripts
- [ ] Blocks sensitive files (`.env`, `*.key`, etc.)
- [ ] Handles missing tools gracefully
- [ ] Sets reasonable timeout (< 5s for PreToolUse)
- [ ] Logs errors to stderr or file, not stdout
- [ ] Tests with edge cases (spaces, Unicode, malformed JSON)
- [ ] Tests in real Claude Code session
- [ ] Documents dependencies in README
- [ ] Uses semantic versioning
- [ ] Clear description and tags

---

## Using Bundled Resources

This skill includes 6 reference files for on-demand loading:

**Security & Reliability** (2 files):
- `security-requirements.md` - Input validation, path sanitization, blocking sensitive files
- `reliability-performance.md` - Error handling, timeouts, performance optimization

**Implementation** (2 files):
- `code-templates.md` - Working hook examples (format-on-save, block-sensitive, logger, etc.)
- `quick-reference.md` - Fast syntax lookup (exit codes, jq patterns, environment vars)

**Testing & Publishing** (2 files):
- `testing-debugging.md` - Test patterns, edge cases, debugging techniques
- `publishing-guide.md` - PRPM packaging, advanced configuration, README template

Load references on-demand when specific knowledge is needed. See "When to Load References" section for triggers.

---

## Resources

- [Claude Code Hooks Docs](https://docs.claude.com/en/docs/claude-code/hooks)
- [PRPM Hook Packages](https://prpm.dev/packages?format=claude&subtype=hook)

---

**Last verified**: 2025-12-17 | **Version**: 2.0.0
