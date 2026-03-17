---
name: check-memory-safety
description: "Check Mojo code for memory safety issues (ownership violations, use-after-free, etc.). Use to catch memory bugs."
category: mojo
mcp_fallback: none
agent: test-engineer
user-invocable: false
---

# Check Memory Safety

Validate Mojo code for memory safety violations and ownership issues.

## When to Use

- Code review focused on memory safety
- Testing for use-after-free issues
- Verifying ownership transfer correctness
- Catching double-free or segmentation fault sources
- Validating SIMD memory access patterns

## Quick Reference

```bash
# Find potential use-after-free patterns
grep -n "var .* = .*\^" *.mojo | head -20

# Check for uninitialized access
grep -n "List\[.*\]()" *.mojo | grep -A 2 "\..*\["

# Verify ownership transfer
grep -n "owned\|var.*=" *.mojo | sort

# Check pointer operations
grep -n "DTypePointer\|alloc\|free\|__del__" *.mojo

# Find scope issues
grep -n "{" *.mojo | wc -l  # Check nesting depth
```

## Memory Safety Patterns

**Safe Ownership Transfer**:

- ✅ `fn take(var data: List[Int])` - Caller loses access
- ✅ `return self.data^` - Transfer from struct field
- ✅ `var copy = data^` - Move to new variable
- ❌ `fn take(data: List[Int])` - Ambiguous, use var
- ❌ `return self.data` - Missing transfer operator

**Safe Initialization**:

- ✅ `var shape = List[Int]()` then `shape.append(dim)`
- ✅ `var data = DTypePointer[DType.float32].alloc(size)`
- ✅ Check `size > 0` before allocation
- ❌ `var list = List[Int]()` then `list[0] = value` (uninitialized)
- ❌ `alloc(0)` or `alloc(negative)` (invalid size)

**Safe Pointer Usage**:

- ✅ Allocate before use: `alloc(size)`
- ✅ Store size separately for bounds checking
- ✅ Verify pointer validity before dereference
- ❌ Use after free (manually deleted pointer)
- ❌ Out-of-bounds access
- ❌ Null pointer dereference

**Safe Scope Management**:

- ✅ Owned values dropped at scope end
- ✅ RAII pattern with proper cleanup
- ✅ Lifetime boundaries clear
- ❌ Variable used after scope exit
- ❌ Reference to stack variable returned
- ❌ Missing ownership transfer between scopes

## Safety Validation Workflow

1. **Identify pointers**: Find all pointer operations
2. **Check allocation**: Verify all pointers allocated before use
3. **Trace ownership**: Follow ownership transfers
4. **Verify lifetimes**: Check value scopes
5. **Find violations**: Identify safety issues
6. **Suggest fixes**: Provide safety corrections
7. **Verify fixes**: Compile to confirm safety

## Output Format

Report memory safety issues with:

1. **Issue Type** - Use-after-free, double-free, uninitialized, bounds, etc.
2. **Location** - File and line number
3. **Code Snippet** - The problematic code
4. **Root Cause** - Why it's unsafe
5. **Risk Level** - Segfault, undefined behavior, or warning
6. **Fix** - How to correct it safely

## Common Safety Issues & Fixes

**Uninitialized List Access**:

- Problem: `var list = List[Int](); list[0] = 5`
- Risk: Out-of-bounds write, segmentation fault
- Fix: Use `list.append(5)` instead

**Use After Move**:

- Problem: `var a = list^; print(list)` (list moved, now invalid)
- Risk: Use-after-free
- Fix: Don't use list after transfer, or create copy

**Missing Bounds Check**:

- Problem: Access `tensor._data[index]` without size check
- Risk: Out-of-bounds access, segfault
- Fix: Add `assert index < size` or check in loop

**Pointer Without Size**:

- Problem: `var ptr = alloc(size)` but size not tracked
- Risk: Invalid access, use-after-free
- Fix: Store size, verify before access

**Double-Free**:

- Problem: Manual `free()` called twice on same pointer
- Risk: Heap corruption, segfault
- Fix: Use RAII, don't call free manually

## Error Handling

| Problem | Solution |
|---------|----------|
| Compiler not available | Build with `mojo build` to get errors |
| Complex ownership | Trace step-by-step through ownership chain |
| Generic code | Check all type instantiations |
| External code | Verify contract assumptions |
| False positives | Verify with test execution |

## Safety Checklist

Before committing Mojo code:

- [ ] All pointers have size tracked
- [ ] All List/Dict allocations use append/insert
- [ ] All ownership transfers use `^`
- [ ] No variables used after move
- [ ] All pointer access has bounds check
- [ ] Scope lifetimes match usage
- [ ] Compiler produces no errors or warnings

## References

- See CLAUDE.md for ownership patterns
- See validate-mojo-patterns for pattern checking
- See mojo-lint-syntax for syntax issues
