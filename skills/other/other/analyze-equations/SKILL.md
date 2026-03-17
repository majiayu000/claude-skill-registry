---
name: analyze-equations
description: "Parse and interpret mathematical equations from research papers. Use when extracting formulas for implementation."
mcp_fallback: none
category: analysis
tier: 2
user-invocable: false
---

# Analyze Equations

Extract and parse mathematical equations from research papers to understand computational requirements
and implementation details.

## When to Use

- Converting paper formulas to code implementations
- Understanding algorithm mathematical foundation
- Identifying performance-critical computations
- Planning SIMD optimization strategies

## Quick Reference

```bash
# Extract LaTeX equations from PDF
pdftotext -layout paper.pdf - | grep -E '\$\$|\\begin\{equation\}' | head -20
```

## Workflow

1. **Extract equations**: Identify and extract LaTeX/mathematical notation from source documents
2. **Parse components**: Break down complex equations into primitive operations
3. **Identify variables**: Document input parameters, intermediate values, output
4. **Determine data types**: Specify scalar vs vector operations, precision requirements
5. **Map to implementation**: Connect mathematical notation to code operations (matrix multiply, activation, etc.)

## Output Format

Mathematical analysis document:

- Extracted equations (with source references)
- Component breakdown (operands, operations)
- Variable definitions and constraints
- Data type requirements (float32, float64, int32)
- Mojo implementation mapping

## References

- See CLAUDE.md > Language Preference for Mojo ML implementations
- See `extract-algorithm` skill for algorithmic interpretation
- See `/notes/review/mojo-ml-patterns.md` for Mojo tensor operations
