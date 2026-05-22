---
name: control-structure-optimization
description: Provides a systematic checklist for optimizing control structures (loops, conditionals, control flow) to create self-documenting, maintainable code. Use this skill when writing new control logic, refactoring existing code, or conducting code reviews to minimize complexity and improve readability.
---

# Control Structure Optimization

Use this checklist to evaluate and improve control structures in your code. Apply these principles when writing or reviewing any control flow logic including loops, conditional statements, and branching logic.

## Optimization Checklist

### 1. Nominal Path Clarity
- Identify the nominal (normal execution) path through the code
- Ensure this path is immediately obvious to readers
- Place the most common case first in conditional structures
- Avoid burying the happy path inside nested conditions

### 2. Statement Grouping
- Group related statements together logically
- Use blank lines or comments to visually separate logical groups
- Ensure statements that work together are adjacent
- Maintain consistent ordering of related operations

### 3. Routine Encapsulation
- Identify independent statement groups that perform a cohesive function
- Extract these groups into their own routines/functions
- Give each routine a descriptive name that explains its purpose
- Keep routines focused on a single responsibility

### 4. Normal Case Priority
- Structure conditionals to handle the normal case in the `if` branch
- Reserve `else` branches for exceptional or error cases
- This makes the code read like a description of normal behavior
- Avoid double negatives in conditions

### 5. Structural Simplicity
- Choose the simplest control structure that accomplishes the goal
- Avoid unnecessary branching or complex conditionals
- Prefer linear flow over deeply nested structures
- Eliminate redundant checks

### 6. Single-Function Loops
- Ensure each loop performs only one well-defined function
- If a loop does multiple things, consider splitting it
- Give loops a clear, single purpose that can be easily described
- Avoid loops that mix iteration with unrelated operations

### 7. Nesting Minimization
- Reduce nesting depth wherever possible
- Use guard clauses (early returns) to eliminate nesting
- Consider extracting nested blocks into separate functions
- Aim for maximum nesting depth of 3-4 levels

### 8. Boolean Expression Simplification
- Introduce boolean variables to clarify complex conditions
- Create boolean functions for repeated or complex checks
- Use decision tables for complex multi-condition logic
- Replace nested conditionals with boolean algebra when appropriate

## Application Process

1. **Review the control structure** - Identify all loops, conditionals, and branching logic
2. **Apply each checklist item** - Systematically evaluate the code against all 8 points
3. **Refactor as needed** - Make improvements to address any issues found
4. **Verify the changes** - Ensure the refactored code maintains the same behavior
5. **Document rationale** - Add comments if the optimization isn't immediately obvious