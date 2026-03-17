---
name: refactor-extract-and-isolate
description: "[Code Quality] Extracts methods, classes, or modules to reduce complexity and improve isolation. Use when functions are too long, classes have too many responsibilities, or concerns are mixed."
---

# Refactor: Extract and Isolate

Break down complex code into focused, reusable units.

## Extract Method

### When to Extract
- Function > 20 lines
- Code block has a distinct purpose
- Same logic repeated
- Deep nesting (> 3 levels)

## Extract Class

### When to Extract
- Class > 300 lines
- Multiple distinct responsibilities
- Group of related methods/properties
- Feature envy

## Extract Protocol/Interface

### When to Extract
- Multiple implementations possible
- Testing requires mocking
- Dependency inversion needed

## Checklist

1. Identify extraction boundary
2. Choose good name for new unit
3. Move code to new location
4. Update references
5. Add tests for new unit
6. Verify original tests pass