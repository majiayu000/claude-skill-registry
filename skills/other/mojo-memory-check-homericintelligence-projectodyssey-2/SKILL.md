---
name: mojo-memory-check
description: "Verify memory safety in Mojo code including ownership, borrowing, and lifetime management. Use when reviewing code or debugging memory issues."
mcp_fallback: none
category: mojo
agent: test-engineer
user-invocable: false
---

# Memory Safety Check Skill

Validate Mojo ownership and borrowing rules.

## When to Use

- Reviewing code for memory safety
- Debugging memory or segfault issues
- Before merging code
- Performance testing reveals corruption

## Quick Reference

```mojo
# Owned parameter - takes ownership
fn consume(var data: Tensor):
    process(data)  # data moved here

# Borrowed parameter - read-only reference
fn read_only(data: Tensor):
    let value = data[0]  # OK: read-only

# Mutable reference - in-place modification
fn modify(mut data: Tensor):
    data[0] = 42  # Mutate in caller's variable
```

## Workflow

1. **Trace ownership** - Which function owns each value
2. **Check borrows** - Are references short-lived
3. **Verify moves** - Use `^` operator for ownership transfer
4. **Test lifetimes** - Compile and run with memory checks
5. **Debug issues** - Identify use-after-move or dangling refs

## Mojo-Specific Notes

- Use `^` operator ONLY when transferring ownership
- `mut self` for mutating methods (NOT `out self`)
- `out self` ONLY for constructors (`__init__`)
- List/Dict/String are non-copyable - must use `^` when returning

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Use after move` | Variable used after ownership transfer | Create copy or don't move |
| `Dangling reference` | Reference to local variable | Return owned value with `^` |
| `Mutable aliasing` | Multiple mutable refs to same data | Ensure single mutable reference |
| `Type not copyable` | Missing `^` on non-copyable return | Add transfer operator `^` |

## References

- `.claude/shared/mojo-anti-patterns.md` - Ownership violations section
- `.claude/shared/mojo-guidelines.md` - Parameter conventions table
