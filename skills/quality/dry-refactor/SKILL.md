---
name: dry-refactor
description: Use when user asks to "remove duplicates", "DRY up code", "extract common logic", "consolidate repeated code", or when /dry scan finds duplicates. Provides language-specific refactoring guidance.
user-invocable: false
---

# DRY Refactoring Guide

Help users eliminate code duplication by extracting shared logic into reusable modules.

## When This Applies

- User mentions "duplicates", "DRY", "repeated code", "copy-paste"
- `/bluera-base:dry scan` found duplicates that need refactoring
- Code review identified similar patterns across files

## When Duplication is Acceptable

Not all duplication is bad. Keep duplicates when:

1. **Test code**: Explicit test cases can repeat for clarity
2. **Generated code**: Don't DRY generated files
3. **Incidental similarity**: Coincidentally similar code that may diverge
4. **Coupling cost**: Extraction would create tight coupling between unrelated modules

## Refactoring Workflow

### 1. Analyze the Duplicates

```bash
# Run scan if not already done
/bluera-base:dry scan

# Review the report
/bluera-base:dry report
```

### 2. Categorize Each Duplicate

| Category | Action |
|----------|--------|
| **Exact copy** | Extract immediately |
| **Near-duplicate** | Parameterize differences, then extract |
| **Structural** | Consider codegen/templates |
| **Coincidental** | Leave as-is, document why |

### 3. Choose Extraction Target

| Scope | Target |
|-------|--------|
| Same file | Local function/method |
| Same module/package | Shared utility file |
| Across modules | New shared module |
| Across repos | Shared library/package |

### 4. Execute Extraction

1. Create the shared abstraction
2. Move one instance, verify tests pass
3. Replace remaining instances
4. Update imports/exports
5. Run tests after each replacement

### 5. Validate

- [ ] All tests pass
- [ ] No circular dependencies introduced
- [ ] Public API unchanged (if applicable)
- [ ] Code is actually simpler (not over-abstracted)

## Anti-patterns to Avoid

1. **Wrong abstraction**: Forcing unrelated code together
2. **Over-parameterization**: Too many config options
3. **Premature extraction**: Extracting before patterns stabilize
4. **Leaky abstraction**: Exposing implementation details

## Language-Specific Patterns

See `@dry-refactor/references/patterns.md` for detailed examples:

| Language | Primary Pattern |
|----------|-----------------|
| JS/TS | Module export, barrel index |
| Python | Module with **init**.py |
| Rust | Submodule with pub use |
| Go | Same-package separate file |

## Report Integration

When `/bluera-base:dry scan` identifies duplicates:

1. Review the report at `.bluera/bluera-base/state/dry-report.md`
2. Start with highest-impact duplicates (most tokens/instances)
3. Use suggested extraction targets from the report
4. Re-run `/bluera-base:dry scan` after refactoring to verify reduction
