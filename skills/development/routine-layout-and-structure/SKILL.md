---
name: routine-layout-and-structure
description: Format routine parameters using standard indentation and organize routine internal structure with blank lines. Use when defining functions with multi-line parameters, writing routine implementations, or establishing coding standards for function formatting.
---

# Routine Layout and Structure

Apply these formatting rules to improve routine readability and maintainability.

## Routine Parameter Layout

**When to apply:** When routine parameters cannot fit on a single line

1. Use standard indentation for multi-line parameter lists
2. Place each parameter on a new line
3. Vertically align parameters using standard indentation

**Avoid "Endline Layout":** 
- Endline layout attempts to align parameters to the right edge
- High maintenance cost: changing function name length requires reformatting all parameter lines
- Can cause right-side space limitations

**Advantages of standard indentation:**
- Better accuracy, consistency, readability, and maintainability
- Function name changes don't affect parameter layout
- Adding or removing parameters requires modifying only one line

## Routine Internal Structure

**When to apply:** When writing routine implementations with declarations and executable code

Use blank lines to separate logical parts of the routine:

1. After the routine header
2. Around data declarations and named constant declarations (if present)
3. Before the routine body

**Purpose:** Clearly delineate the logical components (header, declarations, body) of the routine.

## Result
- Parameter lists are clear and easy to maintain
- Routine structure is visually organized with clear section boundaries
- Code modifications don't cascade formatting changes