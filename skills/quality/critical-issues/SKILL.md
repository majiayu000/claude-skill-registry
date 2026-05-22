---
name: compact-reviewer:critical-issues
description: Use when reviewing Compact contracts for bugs, logic errors, assertion issues, type mismatches, dead code, unreachable paths, or control flow problems.
---

# Critical Issues Skill

Detection of bugs, logic errors, and correctness issues in Compact smart contracts.

## When to Use

This skill activates for queries about:
- Bug detection and logic errors
- Assertion problems
- Type mismatches
- Dead code and unreachable paths
- Control flow issues
- State management bugs

**Trigger words**: bug, logic error, assertion, unreachable, dead code, type mismatch, correctness

## Quick Reference

### Common Bug Categories

| Category | Severity | Example |
|----------|----------|---------|
| Assertion always fails | 🔴 Critical | `assert x < y` where x ≥ y always |
| Assertion always passes | 🟠 High | Redundant check that's always true |
| Unreachable code | 🟡 Medium | Code after unconditional return |
| Type mismatch | 🔴 Critical | Wrong type in comparison |
| Integer overflow | 🟠 High | Unbounded arithmetic |
| Off-by-one | 🟠 High | Loop bounds errors |

### Bug Detection Patterns

```compact
// ❌ Assertion that always fails
export circuit verify(x: Uint<64>, y: Uint<64>): [] {
    assert x > y;     // Called with x = 0
    assert x <= y;    // Contradictory assertions
}

// ❌ Dead code after return
export circuit process(): Uint<64> {
    return 42;
    const x = 1;  // Never executes
}

// ❌ Off-by-one error
export circuit fill_array(): [] {
    for i in 0..100 {
        items[i + 1].write(0);  // Skips index 0, overflows at 100
    }
}
```

## Review Process

### 1. Assertion Analysis

For each assertion:
1. Determine if condition can ever be true/false
2. Check for contradictory assertions
3. Verify assertion is meaningful

**Patterns to flag**:
- `assert true` - Useless
- `assert false` - Circuit always fails
- `assert x && !x` - Contradiction
- Assertion after assignment that makes it always pass

### 2. Control Flow Analysis

Trace all execution paths:
1. Identify unreachable code
2. Check all branches return appropriate values
3. Verify loop bounds

**Patterns to flag**:
- Code after `return`
- `if` with identical branches
- Loops that never execute (`for i in 0..0`)
- Infinite loops (if possible)

### 3. Type Correctness

Verify type usage:
1. Comparisons between compatible types
2. Arithmetic within bounds
3. Array/map access with correct index types

### 4. State Consistency

Check ledger operations:
1. Read-before-write patterns
2. Inconsistent state updates
3. Missing initialization

## References

- [Common Bugs](./references/common-bugs.md) - Catalog of Compact-specific bugs
- [Logic Error Patterns](./references/logic-error-patterns.md) - Detection patterns

## Related Skills

- [security-review](../security-review/SKILL.md) - Security vulnerabilities
- [compact-core/language-reference](../../../compact-core/skills/language-reference/SKILL.md) - Type system
