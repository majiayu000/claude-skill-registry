---
name: rule-code-preservation
description: 'Rule mapping for code-preservation'
---

# Rule code-preservation

Apply this rule whenever work touches:
- `*`

This rule exists to prevent accidental loss of functionality during development. Code that is already working, tested, and deployed represents invested effort and validated behavior.

### Do not delete without approval

Before removing any code, test, or feature, ask the user for explicit confirmation. This includes:

- Removing a function, class, or module that appears unused.
- Deleting a test case that seems redundant.
- Dropping an entire file during a restructuring.

Even if you are confident the code is dead, confirm first. There may be runtime references, dynamic imports, or downstream consumers you are not aware of.

### Refactoring discipline

When refactoring:

1. **Run tests before starting** to establish a green baseline.
2. **Make changes incrementally** so that if a test breaks, the cause is easy to identify.
3. **Run tests after each change** to confirm behavior is preserved.
4. **Do not change signatures** of exported functions unless that is the explicit goal of the task.

### Stay in scope

If you notice unrelated code that could be improved while working on a task, note it but do not modify it. Unrelated changes:

- Make pull requests harder to review.
- Increase the risk of regressions.
- Obscure the intent of the change.

### Error handling is sacred

Existing error handling, catch blocks, validation checks, and fallback logic should not be removed or simplified during unrelated work. These guards often exist because of production incidents or edge cases that are not obvious from reading the code alone.

### Moving code

When relocating code (e.g., extracting to a shared library), ensure:

- All original call sites are updated to use the new location.
- No functionality is silently dropped during the move.
- Tests are updated to reference the new module paths.
- The old location is cleaned up only after confirming all references are resolved.
