---
name: ic-optimize
description: Optimize IC10 code for efficiency and line count. Use when user wants to reduce line count, improve performance, or refactor existing Stationeers IC10 code.
---

# IC10 Code Optimization

Optimize IC10 code for better efficiency and lower line count.

## Workflow

1. **Analysis Phase**
   Use Task tool to spawn:
   - `code-analyzer` - Understand current code structure

2. **Optimization Phase**
   Use Task tool to spawn:
   - `code-optimizer` - Apply optimization techniques

## Instructions

When the user asks to optimize IC10 code:

1. Launch `code-analyzer` to understand the code structure

2. Launch `code-optimizer` with:
   - The original code
   - The analysis results
   - Any specific constraints (target line count, etc.)

3. Present the optimization report:
   - Before/after line counts
   - List of optimizations applied
   - Explanation of each change

4. Show the optimized code:
   - With preserved documentation
   - With clear structure
   - Verifiably equivalent behavior

5. Note any trade-offs:
   - Readability vs line count
   - Additional register usage
   - Potential edge cases

## Optimization Goals

1. **Line Count Reduction**
   - IC10 has 128 line limit
   - Critical when code is near limit
   - Use select, combine conditions, remove redundancy

2. **Efficiency Improvement**
   - Reduce instructions per tick
   - Cache device reads
   - Move static calculations outside loops

3. **Code Quality**
   - Maintain readability
   - Keep documentation
   - Preserve functionality

## Example Triggers

- "Optimize this code"
- "Reduce line count"
- "Make this more efficient"
- "Refactor this script"
- "I'm running out of lines"
- "Can this be shorter?"
