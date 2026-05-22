---
name: mojo-type-safety
description: "Validate type safety in Mojo code including parametric types and trait constraints. Use during code review or when type errors occur."
mcp_fallback: none
category: mojo
agent: test-engineer
user-invocable: false
---

# Type Safety Validation Skill

Ensure Mojo code follows type safety principles.

## When to Use

- Type errors during compilation
- Code review for type safety
- Designing generic functions
- Working with trait constraints

## Quick Reference

```mojo
# Generic function with type parameter
fn add[dtype: DType](a: Scalar[dtype], b: Scalar[dtype]) -> Scalar[dtype]:
    return a + b

# Trait constraint
fn process[T: Copyable](data: T):
    let copy = data  # T is Copyable

# Compile-time check
@parameter
fn validate[size: Int]():
    constrained[size > 0, "Size must be positive"]()
```

## Workflow

1. **Add type annotations** - All parameters and returns
2. **Use type parameters** - For generic code
3. **Add trait constraints** - When required
4. **Run compiler** - Verify type checking passes
5. **Test generic code** - With multiple types

## Mojo-Specific Notes

- Prefer `fn` over `def` for type safety
- Generic type parameters use `[T]` syntax
- Traits constrain what operations are allowed
- Compile-time checks prevent runtime errors

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Missing type annotation` | Untyped parameter | Add `: Type` to parameter |
| `Type mismatch` | Incompatible types | Add explicit conversion |
| `Unsupported operation` | Trait not constrained | Add trait constraint |
| `Constraint failed` | Compile-time check failed | Verify constraint conditions |

## References

- `.claude/shared/mojo-guidelines.md` - Current syntax and patterns
- `.claude/shared/mojo-anti-patterns.md` - Common constructor mistakes
