---
name: code-refactoring-dry
description: Remove code duplication by extracting shared logic into reusable components. Use when the same logic appears in multiple places.
---

# Code Refactoring: Don't Repeat Yourself

Remove code duplication you just introduced by refactoring duplicated code to follow the DRY principle.

## When to Use This Skill

Use this skill when:
- You notice the same logic appearing in multiple places
- Code has been copied and pasted with minor variations
- A change needs to be made in multiple locations
- Following the "NO DUPLICATED CODE!" rule from code review

## Instructions

### Step 1: Identify the Duplication

Review your recent changes (committed or uncommitted) to find:
- Duplicated code patterns
- Duplicated logic or structures
- Copied and pasted blocks with minor variations

### Step 2: Clarify Scope (If Needed)

If the duplication is not obvious, ask the user to clarify which specific
duplication they want addressed before proceeding.

### Step 3: Refactor

Once the duplication is identified:
- Extract shared logic into reusable functions, classes, or modules
- Replace duplicated code with calls to the shared implementation
- Ensure the refactoring maintains the same functionality
- Update all call sites to use the new shared implementation

### Step 4: Verify

After refactoring:
- Run tests if available
- Verify the code still works as expected
- Check that the solution is cleaner and more maintainable

## Goal

Eliminate unnecessary duplication while maintaining code clarity and
functionality. The refactored code should be easier to maintain and modify
in the future.

## Benefits of DRY

- **Single source of truth**: Changes only need to be made in one place
- **Easier maintenance**: Bug fixes propagate automatically
- **Reduced risk**: Consistency is enforced
- **Better testing**: Test shared logic once
