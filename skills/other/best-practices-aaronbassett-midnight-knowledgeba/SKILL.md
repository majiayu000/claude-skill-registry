---
name: compact-reviewer:best-practices
description: Use when reviewing Compact contracts for idiomatic patterns, learning recommended practices, or identifying common mistakes to avoid in Midnight smart contract development.
---

# Best Practices Skill

Guidance on idiomatic Compact patterns and common mistakes to avoid.

## When to Use

This skill activates for queries about:
- Idiomatic Compact code
- Best practices and conventions
- Common mistakes
- Recommended patterns
- Library usage

**Trigger words**: best practices, idiomatic, convention, pattern, recommended, should, ought

## Quick Reference

### Idiomatic Patterns

| Pattern | Good | Avoid |
|---------|------|-------|
| Authorization | `require_owner()` helper | Inline auth in every circuit |
| Constants | Named constants | Magic numbers |
| Error handling | Descriptive assertions | Silent failures |
| State access | Controlled via helpers | Direct ledger access everywhere |
| Naming | `verb_noun` for circuits | Cryptic abbreviations |

### Common Mistakes

```compact
// ❌ Missing language pragma
// Should be at the top of every file
export circuit example(): [] { }

// ✅ With pragma
pragma language_version >= 0.18.0;
export circuit example(): [] { }
```

```compact
// ❌ Not using Counter for counts
ledger count: Cell<Uint<64>>;
export circuit increment(): [] {
    count.write(count.read() + 1);
}

// ✅ Using Counter ADT
ledger count: Counter;
export circuit increment(): [] {
    count.increment(1);
}
```

## Review Process

### 1. Pragma and Imports

Check file structure:
- Pragma present and version specified
- Imports at top (when supported)
- Logical ordering of declarations

### 2. Type Choices

Verify appropriate types:
- Counter for counts
- Map for key-value pairs
- Set for membership
- Cell for single values
- Vector for fixed-size arrays

### 3. Pattern Compliance

Check against idioms:
- Authorization extracted to helpers
- Constants defined at top
- Consistent naming
- Documented public interfaces

## References

- [Idioms](./references/idioms.md) - Idiomatic patterns
- [Common Mistakes](./references/common-mistakes.md) - Mistakes to avoid

## Related Skills

- [code-quality](../code-quality/SKILL.md) - Code organization
- [compact-core/language-reference](../../../compact-core/skills/language-reference/SKILL.md) - Language features
