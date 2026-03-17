---
name: refactor-simplify-branching
description: "[Code Quality] Simplifies complex conditionals: deep nesting, long if-else chains, switch sprawl. Use when control flow is hard to follow or has high cyclomatic complexity."
---

# Refactor: Simplify Branching

Reduce conditional complexity for better readability.

## Techniques

### 1. Guard Clauses (Early Return)
Replace deep nesting with flat guards.

### 2. Replace Conditionals with Polymorphism
Use protocol dispatch instead of type checking.

### 3. Replace Nested Conditionals with Table
Use lookup tables for multi-dimensional conditions.

### 4. Decompose Compound Conditionals
Extract complex conditions to named variables or methods.

### 5. Replace Flag Arguments
Create separate methods instead of boolean flags.

## Warning Signs

- Nesting > 3 levels deep
- More than 3 else-if branches
- Switch with > 5 cases
- Condition spans multiple lines