---
name: file-organization-and-structure
description: Organize routines within files using blank line separation, consider alphabetical ordering when appropriate, and follow C++ standard file structure. Use when organizing source files, when language doesn't support class-based organization, or when editor navigation is limited.
---

# File Organization and Structure

Apply these principles to create well-organized source files.

## Routine Separation Within Files

**When to apply:** When a file contains multiple routines

1. Use at least two blank lines to separate each routine from others
2. **Visual distinction:**
   - Use two to three blank lines to create visual difference from internal routine spacing
   - Blank lines are as effective as asterisk or dash lines, and easier to input and maintain

## Routine Ordering Strategy

**When to apply:** When organizing routines within a file and no stronger principle applies

1. **Alternative approach:** Arrange related routines alphabetically
2. **Applicable scenarios:**
   - Programs cannot be decomposed into classes
   - Editor doesn't allow easy function lookup
3. **Advantage:** Saves search time

## C++ Source File Content Order

**When to apply:** When organizing C++ source files

Follow this typical order for C++ source file contents:

1. File description comment
2. `#include` files
3. Constant definitions applicable to multiple classes (if file contains multiple classes)
4. Enums applicable to multiple classes (if file contains multiple classes)
5. Macro function definitions
6. Type definitions applicable to multiple classes (if file contains multiple classes)
7. Imported global variables and functions
8. Exported global variables and functions
9. File-private variables and functions
10. Classes, including constant definitions, enums, and type definitions within each class

## Result
- Routine boundaries are clearly visible
- File structure follows consistent conventions
- Code is easier to navigate and maintain