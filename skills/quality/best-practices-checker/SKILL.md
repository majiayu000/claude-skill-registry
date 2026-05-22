---
name: best-practices-checker
description: Checks code for best practice violations including DRY violations, SOLID principles, error handling patterns, testing practices, documentation standards, and version control practices. Returns structured best practice reports with improvement suggestions.
---

# Best Practices Checker Skill

## Instructions

1. Review code for best practice violations
2. Check for DRY (Don't Repeat Yourself) violations
3. Verify SOLID principles are followed
4. Review error handling patterns
5. Check testing practices and coverage
6. Review documentation standards
7. Check version control practices
8. Return structured best practice reports with:
   - File path and line numbers
   - Best practice violation type
   - Current code
   - Suggested improvement
   - Reason
   - Priority (usually Should-Fix or Nice-to-Have)

## Examples

**Input:** Code duplication
**Output:**
```markdown
### BEST-001
- **File**: `utils.js`, `helpers.js`
- **Lines**: 15-20 (utils.js), 30-35 (helpers.js)
- **Priority**: Should-Fix
- **Issue**: Duplicate code for calculating total price
- **Current Code**:
  ```javascript
  // In utils.js
  function calculateTotal(items) {
      let total = 0;
      for (let item of items) {
          total += item.price;
      }
      return total;
  }
  
  // In helpers.js (duplicate)
  function getTotal(items) {
      let total = 0;
      for (let item of items) {
          total += item.price;
      }
      return total;
  }
  ```
- **Suggested Fix**:
  ```javascript
  // In shared/utils.js
  export function calculateTotal(items) {
      return items.reduce((sum, item) => sum + item.price, 0);
  }
  
  // Import in both files
  import { calculateTotal } from './shared/utils';
  ```
- **Reason**: DRY principle - code duplication makes maintenance harder and increases bug risk
```

## Best Practice Areas to Check

- **DRY Violations**: Code duplication that should be extracted
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Error Handling**: Consistent error handling patterns, proper error propagation
- **Testing**: Test coverage, test quality, testing patterns
- **Documentation**: Code comments, API documentation, README quality
- **Version Control**: Commit message quality, branch naming, git practices
- **Code Organization**: Logical file structure, module organization
- **Naming Conventions**: Clear, descriptive names
- **Function Size**: Functions that are too long
- **Complexity**: Cyclomatic complexity, nested conditionals

## Priority Guidelines

- **Must-Fix**: Best practice violations that cause bugs or significant maintainability issues
- **Should-Fix**: Best practice improvements that enhance code quality
- **Nice-to-Have**: Minor best practice enhancements
