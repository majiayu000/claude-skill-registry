---
name: "session-cleanup"
description: "Verify debug/dev artifacts are removed before commit. Use at session end to apply 'good boy scout' rule - leave code cleaner than you found it."
version: "1.0.0"
allowed-tools: "Bash, Read, Grep, Glob"
license: "AGPL-3.0"
---

# Session Cleanup Skill

## What This Skill Does

This skill verifies that debug and development artifacts are cleaned up before committing code. It embodies the "good boy scout" principle: leave the code cleaner than you found it.

**Key Responsibilities:**
- Find debug print statements (eprintln!, dbg!, println! for debug)
- Find commented-out debug code
- Find leftover test files or temporary code
- Report any cleanup needed before commit

## When to Use This Skill

Use this skill:
- At the end of a debug/investigation session
- Before creating a commit
- After fixing a bug to ensure debug code is removed
- When you've been adding/removing diagnostic code

**Automatic Reminder:** Consider adding to your session-end routine.

**Manual Triggers:**
- `/session-cleanup`
- "Check for debug artifacts"
- "Clean up session"

## Artifacts to Find

### Rust Debug Artifacts

```rust
// These should be removed before commit:
eprintln!("DEBUG: ...");           // Debug prints
println!("[DEBUG] ...");           // Debug prints
dbg!(variable);                    // Debug macro
#[allow(dead_code)]                // Only if for debug code
// TODO: REMOVE                    // Temporary markers
```

### Temporary Test Code

```rust
// Look for these patterns:
#[test]
fn temp_test() { ... }             // Temporary tests

#[ignore]                          // Tests that should be removed or fixed
fn test_disabled() { ... }
```

### Debug Logging Levels

```rust
// These are fine (production logging):
tracing::debug!(...);              // OK - controlled by log level
tracing::info!(...);               // OK - informational

// These may be debug artifacts:
tracing::warn!("DEBUG: ...");      // Suspicious - debug in warn?
```

## Cleanup Checklist

When running this skill:

1. **Scan for eprintln!/println! debug**
   ```bash
   grep -rn "eprintln!" src/ | grep -i debug
   grep -rn 'println!.*DEBUG' src/
   ```

2. **Scan for dbg! macros**
   ```bash
   grep -rn 'dbg!' src/
   ```

3. **Scan for TODO markers**
   ```bash
   grep -rn 'TODO.*REMOVE\|TEMPORARY\|DEBUG' src/
   ```

4. **Check for test artifacts**
   ```bash
   grep -rn 'temp_test\|test_debug' src/ tests/
   ```

5. **Review git diff for debug additions**
   ```bash
   git diff --cached | grep -E '^\+.*eprintln|^\+.*dbg!'
   ```

## Example Session Flow

```
[During Debug Session]
- Add eprintln! statements to trace execution
- Add temporary tests to verify fixes
- Use dbg! for quick value inspection

[At Session End]
- Invoke /session-cleanup
- Remove all debug artifacts found
- Verify changes still work
- Commit clean code
```

## Integration

This skill pairs well with:
- `/commit` - Run cleanup before committing
- `/validate-constitution` - Validate standards after cleanup
- Git pre-commit hooks - Automatic detection

## Remember

- Debug code is useful during development
- Debug code should NOT be committed
- The "good boy scout" rule: leave code cleaner than you found it
- A few minutes of cleanup saves reviewers time

---

*This skill ensures debug artifacts from investigation sessions don't pollute the codebase.*
