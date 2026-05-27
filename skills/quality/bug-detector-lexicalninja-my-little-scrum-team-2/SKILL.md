---
name: bug-detector
description: Detects bugs, logic errors, and edge case handling issues in code. Use when reviewing code for runtime errors, null/undefined handling, type errors, and edge cases. Returns structured bug reports with file paths, line numbers, and suggested fixes.
---

# Bug Detector Skill

## Instructions

1. Analyze code for potential bugs and logic errors
2. Check for null/undefined handling
3. Identify edge cases that aren't handled
4. Look for type errors and runtime exceptions
5. Check for off-by-one errors
6. Identify race conditions (if applicable)
7. Return structured bug reports with:
   - File path and line numbers
   - Description of the bug
   - Current problematic code
   - Suggested fix with code example
   - Reason why it's a bug
   - Priority (Must-Fix, Should-Fix, Nice-to-Have)

## Examples

**Input:** JavaScript function without null check
**Output:**
```markdown
### BUG-001
- **File**: `utils.js`
- **Lines**: 15-18
- **Priority**: Must-Fix
- **Issue**: Function will crash if items parameter is null or undefined
- **Current Code**:
  ```javascript
  function calculateTotal(items) {
      return items.reduce((sum, item) => sum + item.price, 0);
  }
  ```
- **Suggested Fix**:
  ```javascript
  function calculateTotal(items) {
      if (!items || !Array.isArray(items)) {
          return 0;
      }
      return items.reduce((sum, item) => sum + item.price, 0);
  }
  ```
- **Reason**: Calling reduce on null/undefined will throw TypeError
```

## Bug Types to Detect

- **Null/Undefined Errors**: Missing null checks before operations
- **Type Errors**: Wrong data types used in operations
- **Logic Errors**: Incorrect algorithm implementation
- **Edge Cases**: Unhandled boundary conditions
- **Off-by-One Errors**: Array/index boundary mistakes
- **Race Conditions**: Concurrent access issues (if applicable)
- **Division by Zero**: Missing zero checks
- **Array/Collection Errors**: Accessing invalid indices
- **Missing Return Values**: Functions that should return but don't
- **Incorrect Comparisons**: Wrong comparison operators

## Priority Guidelines

- **Must-Fix**: Bugs that cause crashes or incorrect behavior
- **Should-Fix**: Bugs that cause minor issues or unexpected behavior
- **Nice-to-Have**: Potential issues that might cause problems in edge cases
