---
name: complex-conditional-refactoring
description: Refactor complex case statements and deeply nested code using appropriate strategies. Use this skill when you identify complex conditional logic, excessive nesting levels, or unwieldy case statements that need simplification.
---

# Complex Conditional Refactoring

## When to Use This Skill

- Code contains complex case statements that are hard to understand
- Nested conditionals exceed 3-4 levels of depth
- Conditional logic is difficult to test or maintain
- You need to simplify control flow without changing behavior

## Refactoring Strategies

### 1. Transformation Strategies

Change the control flow structure:

- **Convert to if-then-else statements** - Replace complex case logic with clearer conditional chains
- **Convert to Factory Method pattern** - Use object-oriented polymorphism instead of type-based switching
- **Convert to object-oriented approach** - Leverage polymorphism and inheritance to eliminate conditionals

### 2. Decomposition Strategies

Break large logic into smaller units:

- **Extract to subroutines** - Pull out conditional branches into separate functions
- **Functional decomposition** - Split complex logic into smaller, focused functions

### 3. Simplification Strategies

Optimize existing conditional structures:

- **Simplify by retesting conditions** - Restructure conditions to eliminate redundancy
- **Simplify using break blocks** - Use early exits to reduce nesting

### 4. Redesign Strategy

- **Redesign the logic** - When other strategies aren't sufficient, reconsider the underlying design

## Decision Guide

Choose a strategy based on your code's characteristics:

| Situation | Recommended Strategy |
|-----------|---------------------|
| Type-based behavior selection | Factory Method / OO approach |
| Long sequential conditions | Extract to subroutines |
| Deep nesting (4+ levels) | Break blocks / Early returns |
| Repeated similar conditions | Redesign with polymorphism |
| Complex case statement | Convert to if-then-else or OO |

## Execution Steps

1. **Identify the problem** - Locate complex conditionals or deep nesting
2. **Analyze the logic** - Understand what the code is trying to accomplish
3. **Select a strategy** - Choose the appropriate refactoring approach
4. **Apply the refactoring** - Implement the chosen strategy
5. **Verify behavior** - Ensure the refactored code produces identical results
6. **Test thoroughly** - Run all tests to confirm no regressions

## Constraints

- Not applicable to simple linear logic
- Detailed implementation techniques may require additional reference material
- Always maintain backward compatibility unless explicitly changing requirements