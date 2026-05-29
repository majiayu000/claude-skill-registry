# 💡 Smart Suggestions Skill

---
name: smart-suggestions
description: Provide intelligent suggestions for code improvements, next steps, and optimizations
---

## 🎯 Purpose

Proactively suggest improvements, optimizations, and next steps based on context analysis.

## 📋 When to Use

- After completing a task
- During code review
- When user seems stuck
- Before major changes

## 🔧 Suggestion Categories

### 1. Code Improvements
| Category | Example Suggestions |
|----------|---------------------|
| Performance | "Consider memoizing this component" |
| Readability | "This function could be split into smaller parts" |
| Security | "Add input validation here" |
| Accessibility | "Add aria-label to this button" |

### 2. Next Steps
```markdown
Based on your current work, consider:
1. Adding tests for the new function
2. Updating documentation
3. Running security audit
4. Testing on mobile
```

### 3. Architecture
```markdown
As your app grows, you might want to:
- Extract shared logic into hooks
- Create a design system
- Add error boundaries
- Implement proper logging
```

## 💡 Suggestion Templates

### After Feature Complete
```markdown
## 💡 Suggestions

### Immediate
- [ ] Add unit tests for [component]
- [ ] Update README with new feature

### Soon
- [ ] Add error handling for edge cases
- [ ] Consider adding loading states

### Later
- [ ] Extract reusable logic to hooks
- [ ] Add analytics tracking
```

### During Code Review
```markdown
## 💡 Improvement Suggestions

### Performance
- Line 45: Consider using `useMemo` for expensive calculation
- Line 78: This API call could be cached

### Readability
- Function `handleClick` is 50 lines, consider splitting
- Variable names could be more descriptive

### Security
- User input at line 23 should be sanitized
```

### When Stuck
```markdown
## 💡 Possible Approaches

### Option 1: [Approach A]
- Pros: [benefits]
- Cons: [drawbacks]
- Effort: Low/Medium/High

### Option 2: [Approach B]
- Pros: [benefits]
- Cons: [drawbacks]
- Effort: Low/Medium/High

### Recommendation
I suggest Option [X] because [reasoning].
```

## 🔍 Context Analysis

### What to Analyze
| Context | Look For |
|---------|----------|
| Code | Patterns, anti-patterns, complexity |
| Project | Tech stack, conventions, size |
| User | Skill level, preferences, history |
| Task | Goals, constraints, requirements |

### Suggestion Priority
| Priority | When to Suggest |
|----------|-----------------|
| 🔴 Critical | Security issues, bugs |
| 🟠 Important | Performance, accessibility |
| 🟡 Helpful | Readability, best practices |
| 🟢 Optional | Nice-to-haves, future ideas |

## 📊 Smart Patterns

### Pattern: Suggest Tests
```javascript
// After writing a function
if (functionCreated && !hasTests) {
  suggest("Add tests for " + functionName);
}
```

### Pattern: Suggest Docs
```javascript
// After API changes
if (apiChanged && !docsUpdated) {
  suggest("Update API documentation");
}
```

### Pattern: Suggest Refactor
```javascript
// If file is too long
if (fileLines > 300) {
  suggest("Consider splitting this file");
}
```

## 🎯 When NOT to Suggest

- User is in a hurry (quick fixes)
- Suggestion already discussed
- Out of scope for current task
- Would cause scope creep

## 🔗 Related Skills

- `code-review` - Review and suggest
- `refactoring` - Implement suggestions
- `testing` - Suggest test coverage
- `documentation` - Suggest doc updates
