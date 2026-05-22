---
name: compact-reviewer:maintainability
description: Use when reviewing Compact contracts for long-term maintainability, identifying technical debt, planning upgrade strategies, or assessing modularity and refactoring needs.
---

# Maintainability Skill

Evaluate long-term maintainability and identify technical debt.

## When to Use

This skill activates for queries about:
- Long-term maintenance
- Technical debt
- Upgrade strategies
- Modularity
- Future changes

**Trigger words**: maintainability, technical debt, upgrade, modular, refactor, future-proof

## Quick Reference

### Maintainability Factors

| Factor | Good | Poor |
|--------|------|------|
| Modularity | Separated concerns | Monolithic |
| Coupling | Loose | Tight |
| Documentation | Current | Missing/stale |
| Dependencies | Minimal | Excessive |
| Complexity | Low | High |

### Technical Debt Indicators

- Large circuits (>50 lines)
- Duplicated code
- Magic numbers
- Missing documentation
- Complex nesting
- Unclear names

## Review Process

### 1. Modularity Assessment

Evaluate code separation:
- Single responsibility per circuit
- Clear module boundaries
- Minimal cross-dependencies

### 2. Change Impact Analysis

Consider future changes:
- How hard to add features?
- How hard to modify behavior?
- What breaks if X changes?

### 3. Debt Identification

Look for:
- TODOs and FIXMEs
- Commented-out code
- Workarounds
- Deprecated patterns

### 4. Upgrade Readiness

Check for:
- Version handling
- Migration paths
- Backward compatibility

## References

- [Modularity Guidelines](./references/modularity-guidelines.md) - Module design
- [Upgrade Patterns](./references/upgrade-patterns.md) - Safe upgrades

## Related Skills

- [design-architecture](../design-architecture/SKILL.md) - Structural design
- [code-quality](../code-quality/SKILL.md) - Code organization
