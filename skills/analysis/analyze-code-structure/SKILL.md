---
name: analyze-code-structure
description: "Examine code organization and identify structural patterns. Use when reviewing module design."
mcp_fallback: none
category: analysis
tier: 1
user-invocable: false
---

# Analyze Code Structure

Examine code organization, module hierarchy, and structural patterns to understand how components are organized.

## When to Use

- Initial codebase review and orientation
- Understanding existing module organization
- Identifying code structure for documentation
- Planning refactoring or reorganization

## Quick Reference

```bash
# Quick code structure analysis
find . -name "*.py" -o -name "*.mojo" | head -20
tree -L 2 --dirsfirst
grep -r "^class\|^def\|^fn\|^struct" --include="*.py" --include="*.mojo" | head -30
```

## Workflow

1. **Survey the codebase**: Identify top-level modules and packages
2. **Map module hierarchy**: Create visual tree of module organization
3. **List main components**: Classes, structs, major functions
4. **Trace imports**: Understand module dependencies
5. **Document findings**: Summarize structure for team

## Output Format

Structure analysis:

- Module/package hierarchy (tree view)
- Key components per module
- Import dependencies
- Layer organization (if applicable)
- Notable patterns (MVC, singleton, factory, etc.)

## References

- See `analyze-code-structure` tier-2 skill for deeper analysis
- See CLAUDE.md > Modularity for design principles
- See `identify-architecture` skill for ML-specific structure
