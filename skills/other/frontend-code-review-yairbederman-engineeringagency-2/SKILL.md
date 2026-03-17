---
name: frontend-code-review
description: Trigger when the user requests a review of frontend files (e.g., `.tsx`, `.ts`, `.js`). Support both pending-change reviews and focused file reviews.
---

# Frontend Code Review

## Intent

Use this skill whenever the user asks to review frontend code (especially `.tsx`, `.ts`, or `.js` files). Support two review modes:

1. **Pending-change review** – inspect staged/working-tree files slated for commit and flag checklist violations before submission.
2. **File-targeted review** – review the specific file(s) the user names and report the relevant checklist findings.

## Checklist Categories

### Code Quality
- [ ] Component follows single responsibility principle
- [ ] Props have proper TypeScript typing
- [ ] No unused imports or variables
- [ ] Consistent naming conventions
- [ ] Error boundaries in place where needed
- [ ] Proper use of React hooks (dependencies, cleanup)
- [ ] No direct DOM manipulation
- [ ] Accessibility attributes present (aria-*, role)

### Performance
- [ ] Expensive computations memoized (useMemo, useCallback)
- [ ] Large lists use virtualization
- [ ] Images optimized and lazy-loaded
- [ ] No unnecessary re-renders (React.memo where appropriate)
- [ ] Bundle size considered (dynamic imports for large deps)
- [ ] No N+1 query patterns in data fetching

### Business Logic
- [ ] Edge cases handled (empty states, loading, errors)
- [ ] User input validated
- [ ] Security considerations addressed (XSS, injection)
- [ ] Proper error messages displayed to user
- [ ] Business rules correctly implemented

## Review Process

1. Open the relevant component/module
2. Gather lines that relate to:
   - Class names and styling
   - React hooks and state
   - Prop memoization
   - Event handlers
3. For each checklist item, note where the code deviates
4. Capture representative code snippets
5. Compose the review per the template below

## Required Output

### Template A (any findings)

```
# Code Review

Found <N> urgent issues need to be fixed:

## 1. <brief description of bug>
**FilePath:** `<path>` line `<line>`
```<language>
<relevant code snippet>
```

### Suggested Fix
<brief description of suggested fix>

---

... (repeat for each urgent issue) ...

Found <M> suggestions for improvement:

## 1. <brief description of suggestion>
**FilePath:** `<path>` line `<line>`
```<language>
<relevant code snippet>
```

### Suggested Fix
<brief description of suggested fix>

---

... (repeat for each suggestion) ...
```

If there are no urgent issues, omit that section.
If there are no suggestions, omit that section.

If issue count exceeds 10, summarize as "10+ urgent issues" and output only the first 10.

**Follow-up:** If at least one issue requires code changes, ask:
> "Would you like me to apply the suggested fixes?"

### Template B (no issues)

```
## Code Review
No issues found.
```

## Severity Guidelines

| Severity | Description | Example |
|----------|-------------|---------|
| 🔴 Urgent | Blocks release, security/data issue | XSS vulnerability, data leak |
| 🟠 Important | Should fix before merge | Missing error handling |
| 🟡 Suggestion | Code quality improvement | Naming convention, memoization |
