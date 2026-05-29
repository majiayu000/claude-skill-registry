---
name: headless-terminal
description: This skill provides guidance for implementing headless terminal interfaces that programmatically control interactive shell sessions. Use this skill when tasks involve creating terminal emulators, implementing pseudo-terminal (PTY) wrappers, building programmatic shell interfaces, or any scenario requiring automated interaction with command-line programs.
---

# Headless Terminal

## Overview

This skill guides the implementation of headless terminal interfaces—programmatic abstractions that spawn and control interactive shell sessions without a visible terminal window. These implementations enable automated interaction with command-line programs, handling of interactive prompts, and capture of terminal output.

## When to Apply This Skill

Apply this skill when:
- Implementing a class or module that wraps shell/terminal functionality
- Building programmatic interfaces to interactive CLI programs
- Creating test harnesses for terminal-based applications
- Automating interactions with programs that expect TTY input
- Implementing BaseTerminal or similar abstract interfaces

## Implementation Approach

### Step 1: Interface Discovery

Before implementing, locate and understand any base interface or abstract class that defines the contract:

1. Search for abstract base classes or interface definitions (e.g., `BaseTerminal`, `TerminalInterface`)
2. Identify all required methods and their signatures
3. Note any expected behaviors documented in docstrings or comments
4. Check for existing implementations that can serve as reference

### Step 2: Library Selection

Choose an appropriate library for PTY interaction. Common options include:

| Library | Pros | Cons | Best For |
|---------|------|------|----------|
| `pexpect` | Simple API, handles expect patterns, cross-platform | Higher-level abstraction | Most use cases |
| `pty` + `subprocess` | Standard library, fine-grained control | More complex setup | Custom requirements |
| `tmux`/`screen` | Session persistence, multiplexing | External dependency | Long-running sessions |

Document the reasoning for the chosen library explicitly.

### Step 3: Core Implementation

Implement these essential components:

1. **Shell Spawning**: Start an interactive shell with appropriate flags
   - Consider using `-i` flag for bash to source startup files
   - Set appropriate terminal dimensions (rows, columns)
   - Configure echo behavior explicitly

2. **Input Methods**: Implement keystroke and command sending
   - Handle special characters (Ctrl+C as `\x03`, Ctrl+D as `\x04`, Ctrl+Z as `\x1a`)
   - Consider line endings (`\n` vs `\r\n`)
   - Implement both raw keystroke and full command methods

3. **Output Reading**: Capture terminal output reliably
   - Handle non-blocking reads
   - Manage output buffering
   - Consider timeout behavior

4. **Resource Management**: Ensure proper cleanup
   - Implement context manager protocol (`__enter__`, `__exit__`)
   - Close file descriptors and terminate processes
   - Prevent zombie processes

### Step 4: Verification Strategy

**Critical**: Always verify implementations are complete and correct.

1. **Post-Write Verification**: After writing any file, read it back to confirm:
   - All methods are complete (not truncated mid-definition)
   - All imports are present
   - Syntax is valid

2. **Incremental Testing**: Test each component before integration:
   - Shell spawning works
   - Commands execute and return output
   - Special keystrokes are handled
   - Cleanup occurs properly

3. **Assertion Quality**: Avoid weak assertions that always pass:
   ```python
   # BAD - always passes
   assert "expected" in output or True

   # GOOD - actually verifies behavior
   assert "expected" in output, f"Expected 'expected' in output, got: {output}"
   ```

4. **Edge Case Testing**: Explicitly test:
   - Empty output handling
   - Long-running commands
   - Commands that produce no output
   - Error conditions (invalid commands)
   - Resource cleanup after errors

## Common Pitfalls

### Truncated Implementations

**Problem**: Code gets cut off mid-method, especially in longer files.

**Prevention**:
- After writing, use Read tool to verify the complete file
- Check that all method definitions have complete bodies
- Verify closing brackets/parentheses match opening ones

### Weak Test Assertions

**Problem**: Tests that cannot fail provide false confidence.

**Prevention**:
- Every assertion should be capable of failing
- Include the actual value in assertion messages
- Test both positive and negative cases

### Missing Error Handling

**Problem**: Implementations fail silently on edge cases.

**Prevention**:
- Test what happens when shell dies unexpectedly
- Handle timeout scenarios explicitly
- Verify behavior after close() is called

### Resource Leaks

**Problem**: Zombie processes or unclosed file descriptors.

**Prevention**:
- Always implement context manager protocol
- Test that cleanup occurs even after exceptions
- Verify no processes remain after test completion:
  ```python
  import subprocess
  # After cleanup, verify no orphaned processes
  result = subprocess.run(['pgrep', '-f', 'pattern'], capture_output=True)
  assert result.returncode != 0, "Found orphaned processes"
  ```

### Race Conditions

**Problem**: Timing-dependent behavior causes flaky tests.

**Prevention**:
- Avoid arbitrary `time.sleep()` calls; use expect patterns when possible
- Document why specific delays are necessary
- Use output patterns rather than fixed waits:
  ```python
  # BAD - arbitrary delay
  time.sleep(0.1)

  # GOOD - wait for specific pattern
  terminal.expect(r'\$\s*$', timeout=5)  # Wait for prompt
  ```

### Incomplete Signal Support

**Problem**: Only testing Ctrl+C while ignoring other signals.

**Prevention**:
- Test Ctrl+C (`\x03`) for interrupt
- Test Ctrl+D (`\x04`) for EOF
- Test Ctrl+Z (`\x1a`) for suspend
- Document which signals are supported

## Verification Checklist

Before declaring implementation complete:

- [ ] All interface methods are implemented with complete bodies
- [ ] File has been read back to verify no truncation
- [ ] Tests use meaningful assertions that can fail
- [ ] Context manager properly cleans up resources
- [ ] Error conditions are tested
- [ ] Special keystrokes (Ctrl+C, Ctrl+D, Ctrl+Z) are verified
- [ ] No zombie processes remain after cleanup
- [ ] Timeout behavior is documented and tested
- [ ] Encoding handling is explicit

## References

For detailed technical documentation on PTY handling and common implementation patterns, see `references/pty_implementation.md`.
