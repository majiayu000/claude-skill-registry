---
name: compact-reviewer:code-quality
description: Use when reviewing Compact code for readability issues, naming conventions, code organization, documentation quality, or consistent formatting and style.
---

# Code Quality Skill

Evaluate code readability, organization, and documentation.

## When to Use

This skill activates for queries about:
- Code readability
- Naming conventions
- Code organization
- Documentation quality
- Formatting and style

**Trigger words**: readability, naming, organization, documentation, clean code, style, format

## Quick Reference

### Quality Checklist

| Aspect | Good | Poor |
|--------|------|------|
| Naming | `get_user_balance` | `gub` |
| Structure | Logical grouping | Mixed concerns |
| Comments | Explain why | Explain what |
| Formatting | Consistent | Inconsistent |
| Length | <50 lines/circuit | >100 lines |

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Circuits | verb_noun | `transfer_tokens`, `get_balance` |
| Ledgers | noun | `balances`, `user_count` |
| Constants | UPPER_SNAKE | `MAX_SUPPLY`, `FEE_RATE` |
| Parameters | snake_case | `recipient_address`, `token_amount` |
| Witnesses | get_* prefix | `get_secret_key`, `get_proof` |

## Review Process

### 1. Naming Analysis

Check all names for:
- Clarity and descriptiveness
- Consistent conventions
- Meaningful distinctions
- No abbreviations (except common ones)

### 2. Structure Review

Evaluate organization:
- Logical grouping of related items
- Consistent ordering
- Appropriate separation
- Clear module boundaries

### 3. Documentation Check

Assess documentation:
- Public interfaces documented
- Complex logic explained
- Assumptions stated
- Examples where helpful

### 4. Formatting Assessment

Check consistency:
- Indentation
- Line length
- Blank lines
- Brace style

## References

- [Naming Conventions](./references/naming-conventions.md) - Detailed naming rules
- [Organization Guidelines](./references/organization-guidelines.md) - Code structure

## Related Skills

- [best-practices](../best-practices/SKILL.md) - Idiomatic patterns
- [maintainability](../maintainability/SKILL.md) - Long-term quality
