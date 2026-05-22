---
name: qa-bug-reporting
description: When reporting bugs found during manual testing or QA validation.
version: 1.1.0
tokens: ~400
confidence: high
sources:
  - https://istqb-glossary.page/bug-report/
  - https://www.theknowledgeacademy.com/blog/defect-report-istqb/
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [qa, bugs, testing, reporting]
---

## When to Use
When reporting bugs found during manual testing or QA validation.

## Patterns

### Bug Report Structure
```markdown
## Bug: [Short descriptive title]

**Severity:** Critical | High | Medium | Low
**Priority:** P0 | P1 | P2 | P3
**Environment:** [browser, OS, device]
**Version:** [app version, commit]

### Steps to Reproduce
1. [First step]
2. [Second step]
3. [Step where bug occurs]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Evidence
- Screenshot: [link]
- Video: [link]
- Console logs: [paste]

### Additional Context
[Any other relevant info]
```

### Severity Levels
```
CRITICAL: System crash, data loss, security breach
          → Blocks release, fix immediately

HIGH:     Major feature broken, no workaround
          → Must fix before release

MEDIUM:   Feature broken but workaround exists
          → Should fix, can defer if needed

LOW:      Minor issue, cosmetic, edge case
          → Fix when time permits
```

### Good vs Bad Bug Titles
```
❌ "Button doesn't work"
✅ "Submit button unresponsive after form validation error on Safari"

❌ "Crash"
✅ "App crashes when uploading file >10MB on mobile"

❌ "Slow"
✅ "Dashboard load time >5s when user has >100 items"
```

## Anti-Patterns
- Missing reproduction steps
- No expected vs actual
- Vague titles ("doesn't work")
- No environment info
- Screenshots without context

## Verification Checklist
- [ ] Title is specific and searchable
- [ ] Steps reproduce the bug reliably
- [ ] Expected vs actual clearly stated
- [ ] Severity/priority assigned
- [ ] Evidence attached
