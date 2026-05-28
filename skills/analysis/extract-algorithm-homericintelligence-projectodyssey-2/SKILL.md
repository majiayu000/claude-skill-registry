---
name: extract-algorithm
description: "Parse and document algorithm pseudocode from research papers. Use when preparing for implementation."
mcp_fallback: none
category: analysis
tier: 2
user-invocable: false
---

# Extract Algorithm

Identify, document, and translate algorithms from research papers into structured pseudocode for implementation planning.

## When to Use

- Converting paper algorithms to code
- Understanding computational complexity
- Planning implementation steps
- Documenting algorithm variations

## Quick Reference

```bash
# Extract text from PDF focusing on algorithms
pdftotext paper.pdf - | grep -A 20 -i "algorithm\|pseudocode" | head -50

# Convert pseudo-code to structured documentation
# Use cleaner formatting with numbered steps
```

## Workflow

1. **Locate algorithm**: Find algorithm description, pseudocode, or flowchart in paper
2. **Document steps**: Extract numbered steps or pseudocode from paper
3. **Identify inputs/outputs**: List parameters, preconditions, postconditions
4. **Note special cases**: Document edge cases and conditional logic
5. **Translate to implementation plan**: Convert to implementation checklist

## Output Format

Algorithm documentation:

- Algorithm name and source reference
- Inputs (parameters, data types, constraints)
- Outputs (return values, side effects)
- Pseudocode or step-by-step description
- Complexity analysis (time and space)
- Special cases and error handling
- Implementation notes and tips

## References

- See `analyze-equations` skill for mathematical formula extraction
- See `identify-architecture` skill for understanding algorithm structure
- See CLAUDE.md > Key Development Principles for implementation guidance
