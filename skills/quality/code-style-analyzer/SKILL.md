---
name: code-style-analyzer
description: Analyzes code for style and formatting issues including inconsistent formatting, naming conventions, code organization, comment quality, unused code, and magic numbers. Returns structured style issue reports with suggestions for improvement.
---

# Code Style Analyzer Skill

## Instructions

1. Analyze code for style and formatting issues
2. Check for inconsistent formatting (indentation, spacing, brackets)
3. Verify naming conventions are followed
4. Check code organization and structure
5. Review comment quality and presence
6. Identify unused code (variables, functions, imports)
7. Look for magic numbers and strings
8. Return structured style reports with:
   - File path and line numbers
   - Style issue type
   - Current code
   - Suggested improvement
   - Reason
   - Priority (usually Should-Fix or Nice-to-Have)

## Examples

**Input:** Inconsistent indentation
**Output:**
```markdown
### STYLE-001
- **File**: `index.html`
- **Lines**: 15-20
- **Priority**: Should-Fix
- **Issue**: Inconsistent indentation (mixing tabs and spaces)
- **Current Code**:
  ```html
  <div>
    <p>Text</p>
      <span>More text</span>
  </div>
  ```
- **Suggested Fix**:
  ```html
  <div>
      <p>Text</p>
      <span>More text</span>
  </div>
  ```
- **Reason**: Consistent indentation improves readability and maintainability
```

## Style Issues to Detect

- **Formatting**: Inconsistent indentation, spacing, bracket placement
- **Naming**: Inconsistent naming conventions (camelCase vs snake_case)
- **Code Organization**: Poor file structure, functions in wrong places
- **Comments**: Missing comments, poor comment quality, outdated comments
- **Unused Code**: Unused variables, functions, imports, dead code
- **Magic Numbers/Strings**: Hardcoded values that should be constants
- **Line Length**: Lines that are too long
- **File Length**: Files that are too long
- **Code Duplication**: Repeated code that could be extracted
- **Import Organization**: Unorganized imports

## Priority Guidelines

- **Must-Fix**: Style issues that cause bugs or significant readability problems
- **Should-Fix**: Style issues that affect readability and maintainability
- **Nice-to-Have**: Cosmetic style improvements
