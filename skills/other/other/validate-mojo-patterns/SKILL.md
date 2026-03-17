---
name: validate-mojo-patterns
description: "Validate Mojo code patterns (out self, mut, List, etc.) against best practices. Use to ensure code follows project standards."
category: mojo
mcp_fallback: none
agent: test-engineer
user-invocable: false
---

# Validate Mojo Patterns

Check Mojo code for correct usage of language patterns and conventions.

## When to Use

- Code review to catch pattern violations
- Pre-commit validation of Mojo standards
- Verifying constructor signatures are correct
- Checking memory safety patterns
- Validating trait conformances

## Quick Reference

```bash
# Find incorrect constructor patterns
grep -n "fn __init__.*mut self\|fn __init__.*var self" *.mojo

# Find non-copyable returns without transfer
grep -n "-> List\|-> Dict\|-> String" *.mojo | grep -v "^"

# Check for deprecated patterns
grep -n "inout\|@value\|DynamicVector" *.mojo

# Verify trait conformances
grep -n "struct.*:" *.mojo | grep -v "Copyable\|Movable"

# Check method signatures
grep -n "fn.*self" *.mojo | grep -v "read\|mut\|var"

# Build package (validates all library files together)
mojo package shared
```

## Pattern Validation Rules

**Constructor Patterns**:

- ✅ `fn __init__(out self, ...)` - Correct for constructors
- ✅ `fn __moveinit__(out self, deinit existing: Self)` - Move constructor
- ✅ `fn __copyinit__(out self, existing: Self)` - Copy constructor
- ❌ `fn __init__(mut self, ...)` - WRONG for constructors
- ❌ `fn __init__(var self, ...)` - WRONG for constructors

**Method Patterns**:

- ✅ `fn method(self) -> Value` - Read-only (implicit read)
- ✅ `fn modify(mut self)` - Mutable operations
- ✅ `fn get_data(self) -> List[Int]` - Return copyable
- ❌ `fn modify(self)` - Misleading (looks immutable)
- ❌ `fn method(read self)` - Unnecessary (implicit)

**Ownership Patterns**:

- ✅ `fn take(var data: List[Int])` - Takes ownership
- ✅ `return self.list^` - Transfer operator for non-copyable
- ✅ `fn use(data: ExTensor)` - Borrowed reference
- ❌ `return self.list` - Missing transfer for List
- ❌ `fn take(data: List[Int])` - Ambiguous (appears borrowed)

**Trait Conformances**:

- ✅ `struct Data(Copyable, Movable)` - Value type traits
- ✅ `struct Model(Copyable, Movable, Stringable)` - With extras
- ❌ `struct Data(Copyable)` - Missing Movable
- ❌ `struct Data(ImplicitlyCopyable)` - Only for simple types

## Validation Workflow

1. **Extract patterns**: Find all fn signatures and struct definitions
2. **Categorize**: Group by pattern type (constructors, methods, ownership)
3. **Validate**: Check each against rules
4. **Identify violations**: Mark incorrect patterns
5. **Suggest fixes**: Provide correction for each violation
6. **Summarize**: Report all pattern issues
7. **Verify**: Use `mojo package` to validate packages, not `mojo build` on individual library files

## v0.26.1 Validation Patterns

**Relative imports are valid in library files, invalid in executables**:

- Library files (in `shared/`): Can use `from ..module import X` - part of package structure
- Executable files (in `examples/`): Must use `from shared.module import X` with `-I .` flag

**Use `mojo package` to validate packages**:

- Build entire package: `mojo package shared`
- DO NOT validate individual library files: `mojo build shared/core/__init__.mojo` will fail with expected errors

## Output Format

Report validation results with:

1. **Total Checks** - Number of patterns validated
2. **Violations Found** - Count of pattern violations
3. **Issues by Type** - Grouped by pattern type
4. **Details** - File, line, pattern, violation, fix
5. **Severity** - Will break compilation or warning
6. **Summary** - Pass/fail overall validation

## Common Violations & Fixes

**Issue**: Constructor uses `mut self`

- Location: `fn __init__(mut self, ...)`
- Fix: Change to `fn __init__(out self, ...)`
- Impact: Critical - won't compile

**Issue**: Missing transfer operator

- Location: `return self.data` (where data is List/Dict)
- Fix: Change to `return self.data^`
- Impact: Critical - won't compile

**Issue**: Missing trait conformance

- Location: `struct Type(Copyable)` (missing Movable)
- Fix: Add `struct Type(Copyable, Movable)`
- Impact: High - can cause use-after-move

**Issue**: ImplicitlyCopyable on non-trivial type

- Location: `struct Layer(ImplicitlyCopyable)` with List fields
- Fix: Remove ImplicitlyCopyable, use default traits
- Impact: Critical - won't compile

## Error Handling

| Problem | Solution |
|---------|----------|
| Can't parse Mojo | Check for syntax errors first (use mojo-lint-syntax) |
| False positives | Verify context manually, may need refinement |
| Mixed patterns | Process each pattern type separately |
| Large codebase | Use grep filters to focus on specific patterns |
| Version issues | Verify code is v0.26.1+ compatible |

## References

- See CLAUDE.md for complete pattern guidelines
- See mojo-lint-syntax for syntax validation
- See check-memory-safety for memory safety issues
