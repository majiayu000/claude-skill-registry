---
name: code-simplifier
description: "This skill should be used when code has been written or modified and needs to be simplified for clarity, consistency, and maintainability while preserving all functionality. The skill should be triggered automatically after completing a coding task or writing a logical chunk of code. It focuses only on recently modified code unless instructed otherwise."
---

# Code Simplifier

## Overview

Enhance code clarity, consistency, and maintainability while preserving exact functionality. This skill applies project-specific best practices to simplify and improve code without altering its behavior, prioritizing readable, explicit code over overly compact solutions.

## When to Use

- After implementing a new feature
- After fixing a bug
- After refactoring or optimizing code
- When code has been modified and needs quality review

## The Simplification Process

### Step 1: Identify Recently Modified Code

Locate the code sections that have been recently modified or touched in the current session. Use git diff or conversation context to identify changes.

### Step 2: Analyze and Apply Refinements

Apply refinements that follow these principles:

**Preserve Functionality**
- Never change what the code does - only how it does it
- All original features, outputs, and behaviors must remain intact

**Apply Project Standards**
- Use ES modules with proper import sorting and extensions
- Prefer `function` keyword over arrow functions
- Use explicit return type annotations for top-level functions
- Follow proper React component patterns with explicit Props types
- Use proper error handling patterns (avoid try/catch when possible)
- Maintain consistent naming conventions
- Follow any CLAUDE.md standards in the project

**Enhance Clarity**
- Reduce unnecessary complexity and nesting
- Eliminate redundant code and abstractions
- Improve readability through clear variable and function names
- Consolidate related logic
- Remove unnecessary comments that describe obvious code
- IMPORTANT: Avoid nested ternary operators - prefer switch statements or if/else chains for multiple conditions
- Choose clarity over brevity - explicit code is often better than overly compact code

### Step 3: Validate Balance

Avoid over-simplification that could:
- Reduce code clarity or maintainability
- Create overly clever solutions that are hard to understand
- Combine too many concerns into single functions or components
- Remove helpful abstractions that improve code organization
- Prioritize "fewer lines" over readability (e.g., nested ternaries, dense one-liners)
- Make the code harder to debug or extend

### Step 4: Apply Changes

1. Make the refinements using the Edit tool
2. Ensure all functionality remains unchanged
3. Verify the refined code is simpler and more maintainable

### Step 5: Document Changes

Document only significant changes that affect understanding. No need to explain trivial formatting adjustments.

## Key Principles

- **Functionality First** - Never break existing behavior
- **Clarity Over Brevity** - Readable code trumps clever one-liners
- **Project Consistency** - Follow established patterns and standards
- **Focused Scope** - Only refine recently modified code unless asked otherwise
- **Balanced Simplification** - Avoid both over-engineering and over-simplification
