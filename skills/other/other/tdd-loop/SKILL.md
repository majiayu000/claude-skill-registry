---
name: tdd-loop
description: Test-Driven Development loop for audit refactor tasks. Automatically picks next task, enforces test-first, runs validation. Based on Ralph Wiggum AI Loop Technique.
---

# TDD Loop Skill

Automated Test-Driven Development workflow for completing audit refactor tasks.

## When to Use

- Running `/tdd-loop` to start automated task completion
- Working through `skill_audit_refactor.json` tasks systematically
- Enforcing test-first development with automated validation

## Commands

| Command | Description |
|---------|-------------|
| `/tdd-loop` | Start TDD loop for next priority task |
| `/tdd-next` | Show next task without starting loop |
| `/tdd-summary` | Show audit refactor progress summary |
| `/tdd-loop --skill <name>` | Loop on specific skill tasks |
| `/tdd-loop --priority P0` | Loop on specific priority level |

## How It Works

Based on [Ralph Wiggum AI Loop Technique](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum):

```
┌─────────────────────────────────────────────────────────────┐
│                      TDD LOOP WORKFLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. PICK TASK                                                │
│     └─ Read skill_audit_refactor.json                       │
│     └─ Select highest priority task with test_exists: false │
│                                                              │
│  2. RED PHASE (Create Failing Test)                         │
│     └─ Create test file at specified path                   │
│     └─ Write test cases for expected behavior               │
│     └─ Run test (should FAIL)                               │
│     └─ Update test_exists: true                             │
│                                                              │
│  3. GREEN PHASE (Implement Fix)                             │
│     └─ Implement the fix in source file                     │
│     └─ Run test (should PASS)                               │
│     └─ Update implemented: true                             │
│                                                              │
│  4. VISUAL PHASE (If Needed)                                │
│     └─ Take screenshot with Chrome DevTools MCP             │
│     └─ Compare with baseline                                │
│     └─ Verify UI renders correctly                          │
│                                                              │
│  5. VALIDATE & LOOP                                          │
│     └─ Update tested: true in audit file                    │
│     └─ Commit changes                                       │
│     └─ Continue to next task                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## TDD Guard Hooks

The TDD Loop uses hooks to enforce test-first:

### PreToolUse Hook (tdd-guard.js)
- Intercepts Edit/Write operations
- Checks if target file has test_exists: false
- BLOCKS implementation if test doesn't exist
- Provides guidance on creating tests first

### PostToolUse Hook (test-validator.js)
- Runs after file modifications
- Executes related tests automatically
- Updates task status on success
- Recommends visual testing for UI components

## Usage Example

```bash
# Start TDD loop for highest priority task
/tdd-loop

# Work on specific skill
/tdd-loop --skill nuxt

# Work on critical issues only
/tdd-loop --priority P0-critical

# Check progress
/tdd-summary
```

## Task File Structure

Tasks are defined in `skill_audit_refactor.json`:

```json
{
  "id": "sec-1",
  "description": "Fix non-timing-safe CSRF comparison",
  "file": "server/utils/cartSecurity.ts",
  "test_file": "tests/server/utils/__tests__/cartSecurity.test.ts",
  "test_exists": false,
  "implemented": false,
  "tested": false,
  "tasks": [
    { "id": "sec-1-a", "task": "Create unit test for timing-safe comparison", "type": "test-first" },
    { "id": "sec-1-b", "task": "Replace string comparison with crypto.timingSafeEqual()", "type": "implementation" },
    { "id": "sec-1-c", "task": "Run unit test to validate fix", "type": "validation" },
    { "id": "sec-1-d", "task": "Visual test: verify cart operations work", "type": "visual-test" }
  ]
}
```

## Loop Control

The loop continues until:
- All tasks in filter are completed
- Maximum iterations reached (default: 50)
- User cancels with `/cancel-tdd`
- An error requires manual intervention

## Best Practices

1. **Always check progress first**: Run `/tdd-summary` before starting
2. **Start with P0-critical**: Focus on security and critical fixes first
3. **Commit frequently**: After each task completion
4. **Review visual tests**: Don't skip UI verification for components
5. **Update audit file**: Mark tasks complete as you go

## References

- [Ralph Wiggum Plugin](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum)
- [TDD Guard for Claude Code](https://nizar.se/tdd-guard-for-claude-code/)
- [Claude Code Hooks Documentation](https://www.letanure.dev/blog/2025-08-06--claude-code-part-8-hooks-automated-quality-checks)
