---
name: compact-reviewer:design-architecture
description: Use when reviewing Compact contract architecture, evaluating design patterns, assessing modularity, or analyzing API design and code organization quality.
---

# Design & Architecture Skill

Evaluate contract structure, design patterns, and architectural quality.

## When to Use

This skill activates for queries about:
- Contract architecture and structure
- Design patterns in Compact
- Modularity and organization
- API design
- Code organization

**Trigger words**: architecture, design pattern, structure, modularity, organization, layout, API design

## Quick Reference

### Architecture Checklist

| Aspect | Check | Severity |
|--------|-------|----------|
| Separation of concerns | Each circuit has one responsibility | 🟡 Medium |
| State encapsulation | Ledger access is controlled | 🟠 High |
| Clear interfaces | Export circuits have clear purposes | 🟡 Medium |
| Naming conventions | Circuits/ledgers clearly named | 🟢 Low |
| Documentation | Public interfaces documented | 🟢 Low |

### Good Architecture Patterns

```compact
// ✅ Single responsibility circuits
export circuit deposit(amount: Uint<64>): [] { }
export circuit withdraw(amount: Uint<64>): [] { }
export circuit get_balance(): Uint<64> { }

// ✅ Helper circuits for reusable logic
circuit verify_owner(): [] {
    const caller = get_caller_secret();
    assert hash(caller) == owner_hash.read();
}

// ✅ Clear state organization
ledger balances: Map<Bytes<32>, Uint<64>>;
ledger config: Cell<Config>;
ledger admin: Cell<Bytes<32>>;
```

### Anti-Patterns

```compact
// ❌ God circuit - does too much
export circuit do_everything(
    action: Uint<8>,
    arg1: Field,
    arg2: Field,
    arg3: Field
): Field {
    if action == 0 { /* deposit */ }
    if action == 1 { /* withdraw */ }
    if action == 2 { /* transfer */ }
    // ...
}

// ❌ Unclear naming
export circuit proc(x: Field): Field { }
ledger d: Map<Bytes<32>, Uint<64>>;
```

## Review Process

### 1. Structure Analysis

Evaluate overall organization:

```
1. Count exported circuits - too many (>10) suggests splitting
2. Check circuit sizes - >50 lines may be too complex
3. Verify helper circuits are used appropriately
4. Confirm ledger declarations are grouped logically
```

### 2. Pattern Recognition

Identify common patterns:

| Pattern | Indicators | Quality |
|---------|------------|---------|
| Owner pattern | `owner_hash`, `verify_owner()` | ✅ Good |
| Access control | Role-based checks | ✅ Good |
| Upgrade pattern | `implementation` ledger | ⚠️ Complex |
| Multi-sig | Multiple signatures required | ✅ Good |
| State machine | Enum-based state | ✅ Good |

### 3. Interface Design

Check public API:

```
1. Are circuit names descriptive?
2. Are parameters minimal and clear?
3. Is return type appropriate?
4. Are related operations grouped?
```

### 4. Modularity Assessment

Evaluate separation:

```
1. Can logic be tested independently?
2. Are concerns separated?
3. Is state access controlled?
4. Are dependencies explicit?
```

## References

- [Architecture Patterns](./references/architecture-patterns.md) - Good patterns
- [Anti-Patterns](./references/anti-patterns.md) - Patterns to avoid

## Related Skills

- [code-quality](../code-quality/SKILL.md) - Code organization
- [maintainability](../maintainability/SKILL.md) - Long-term structure
