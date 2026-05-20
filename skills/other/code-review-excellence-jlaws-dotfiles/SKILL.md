---
name: code-review-excellence
description: Code review practices for giving and receiving feedback. Use when reviewing PRs, responding to review feedback, or establishing review standards.
---

# Code Review Excellence

## Review Mindset

**Goals:** Catch bugs/edge cases, ensure maintainability, share knowledge, enforce standards, improve design.

**Not goals:** Show off knowledge, nitpick formatting (use linters), block progress unnecessarily, rewrite to preference.

## Review Process

### Phase 1: Context (2-3 min)
1. Read PR description and linked issue
2. Check PR size (>400 lines? Ask to split)
3. CI/CD status passing?
4. Understand the business requirement

### Phase 2: High-Level (5-10 min)
- Does solution fit the problem? Simpler approaches?
- Consistent with existing patterns? Will it scale?
- Are there tests? Do they cover edge cases?

### Phase 3: Line-by-Line (10-20 min)
- **Logic**: Edge cases, off-by-one, null checks, race conditions
- **Security**: Input validation, SQL injection, XSS, data exposure
- **Performance**: N+1 queries, unnecessary loops, memory leaks, blocking ops
- **Maintainability**: Clear names, SRP functions, magic numbers extracted

### Phase 4: Summary (2-3 min)
1. Summarize key concerns
2. Highlight what worked well
3. Clear decision: Approve / Comment / Request Changes
4. Offer to pair if complex

## Feedback Severity Labels

```
[blocking]    - Must fix before merge
[important]   - Should fix, discuss if disagree
[nit]         - Nice to have, not blocking
[suggestion]  - Alternative approach to consider
[learning]    - Educational, no action needed
```

## Feedback Techniques

**Ask questions instead of stating problems:**
```
"What happens if `items` is an empty array?"
"How should this behave if the API call fails?"
```

**Suggest, don't command:**
```
"Would it make sense to extract this into a shared utility?
 It appears in 3 places."
```

**Be specific and actionable:**
```
"This could cause a race condition when multiple users access
simultaneously. Consider using a mutex here."
```

## Language-Specific Watch Items

### Python
- Mutable default arguments (`def fn(items=[])` -- use `None`)
- Bare `except:` catching everything
- Mutable class attributes shared across instances

### TypeScript
- `any` type defeating type safety
- Unhandled async errors (missing try/catch on await)
- Prop mutation in React components

## Review Checklists

### Security
- [ ] User input validated and sanitized
- [ ] SQL queries parameterized
- [ ] Auth/authz checked on endpoints
- [ ] Secrets not hardcoded
- [ ] Error messages don't leak internals

### Testing
- [ ] Happy path tested
- [ ] Edge cases covered
- [ ] Error cases tested
- [ ] Tests are behavior-based, not implementation-based
- [ ] Tests are deterministic

## Handling Disagreements

1. **Seek understanding**: "What led you to choose this pattern?"
2. **Acknowledge valid points**: "That's a fair consideration about X."
3. **Provide data**: "Can we add a benchmark to validate?"
4. **Escalate if needed**: Get architect/senior to weigh in
5. **Let go if non-critical**: Perfection is the enemy of progress

## Common Pitfalls

- **Perfectionism**: Blocking PRs for style preferences
- **Scope creep**: "While you're at it..."
- **Delayed reviews**: Let PRs sit for days
- **Rubber stamping**: Approving without reviewing
- **Bike shedding**: Debating trivial details extensively

## PR Review Comment Template

```markdown
## Summary
[Brief overview of what was reviewed]

## Required Changes
[blocking] Issue 1
[blocking] Issue 2

## Suggestions
[suggestion] Improvement 1
[nit] Minor item 1

## Questions
Clarification needed on X

## Verdict
Approve / Approve after fixes / Request changes
```

---

## Receiving & Responding to Reviews

### Response Pattern

```
1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

### Handling Unclear Feedback

If ANY item is unclear, stop. Do not implement partially.

```
Feedback: "Fix items 1-6"
Understand 1,2,3,6. Unclear on 4,5.

WRONG: Implement 1,2,3,6 now, ask about 4,5 later
RIGHT: "Understand 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

### From External Reviewers -- Verify Before Implementing

```
BEFORE implementing:
  1. Technically correct for THIS codebase?
  2. Breaks existing functionality?
  3. Reason for current implementation?
  4. Works on all platforms/versions?
  5. Does reviewer understand full context?

IF suggestion seems wrong:
  Push back with technical reasoning

IF conflicts with prior architectural decisions:
  Stop and discuss with project owner first
```

### YAGNI Check

```
IF reviewer suggests "implement properly":
  grep codebase for actual usage
  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implement properly
```

### When to Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with prior architectural decisions

**How:** Technical reasoning, specific questions, reference working tests/code.

### Acknowledging Correct Feedback

```
"Fixed. [Brief description of what changed]"
"Good catch - [specific issue]. Fixed in [location]."
[Just fix it and show in the code]
```

No performative agreement. Actions speak.

### Implementation Order for Multi-Item Feedback

1. Clarify anything unclear FIRST
2. Blocking issues (breaks, security)
3. Simple fixes (typos, imports)
4. Complex fixes (refactoring, logic)
5. Test each fix individually
6. Verify no regressions

### GitHub Thread Replies

Reply inline in comment threads (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as top-level PR comments.
