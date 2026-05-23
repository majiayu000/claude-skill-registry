---
name: code-review-auto
description: |
  Automatic code review and fixes before showing to user.
  Use when: code generation is complete, before preview.
  Triggers: internal use only.
---

# Automatic Code Review

Review and fix issues before user sees code.

## Review Checklist

### Code Quality
- [ ] No unused imports
- [ ] No unused variables
- [ ] No console.log in production
- [ ] Consistent naming conventions
- [ ] No magic numbers (use constants)

### Structure
- [ ] Components properly extracted
- [ ] No code duplication
- [ ] Reasonable file sizes (<300 lines)
- [ ] Logical folder organization

### Performance
- [ ] No N+1 queries
- [ ] Images optimized
- [ ] Lazy loading where appropriate
- [ ] No blocking operations

### Accessibility
- [ ] Alt text on images
- [ ] Proper heading hierarchy
- [ ] Focusable interactive elements
- [ ] Color contrast sufficient

## Auto-Fix Rules

| Issue | Fix |
|-------|-----|
| Unused import | Remove |
| console.log | Remove |
| Missing alt text | Generate from context |
| Duplicate code | Extract function |
| Long function | Split into smaller |

## Process

1. **Scan generated code**
2. **Identify issues** (categorize by severity)
3. **Auto-fix** what's possible
4. **Re-run tests** to verify fixes don't break
5. **Continue to preview** if all good

## User Experience

User never sees:
- Linting errors
- Initial messy code
- Intermediate states

User always sees:
- Clean, reviewed code
- Working preview
- ✅ confirmation
