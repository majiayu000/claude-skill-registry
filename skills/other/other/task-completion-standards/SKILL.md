---
name: task-completion-standards
description: "Use when completing ESLint rule tasks to verify all required files exist and quality standards are met."
user-invocable: false
---

# Task Completion Standards for ESLint Rules

## Definition of Done

### For New Rule Implementations

#### Files Checklist
- [ ] Rule file exists: `src/rules/<rule-name>.ts`
- [ ] Test file exists: `src/tests/<rule-name>.test.ts`
- [ ] Documentation exists: `docs/rules/<rule-name>.md`
- [ ] `src/index.ts` updated in THREE places:
  - [ ] Import statement at top
  - [ ] Entry in `configs.recommended.rules`
  - [ ] Entry in `rules` object
- [ ] `README.md` updated with rule listing

#### Quality Checklist
- [ ] All tests pass: `npm test`
- [ ] Linting passes: `npm run lint:fix && npm run lint:js`
- [ ] Build succeeds: `npm run build`
- [ ] **Minimum 20 tests** covering:
  - [ ] 10+ valid cases (code that should NOT trigger)
  - [ ] 10+ invalid cases (code that SHOULD trigger)
  - [ ] Edge cases mentioned in issue specification
  - [ ] Unusual patterns and nested structures
- [ ] Auto-fix works correctly (if rule has `fixable: 'code'`)
- [ ] Documentation includes examples of correct and incorrect code

### For Bug Fixes

- [ ] Bug is reproducible via test case
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Regression test(s) added
- [ ] All existing tests still pass
- [ ] Linting passes: `npm run lint:fix && npm run lint:js`
- [ ] Build succeeds: `npm run build`
- [ ] No new bugs introduced

### Common Reasons for Rejection

1. **Missing files** - All 5 file locations must be created/updated
2. **Insufficient tests** - Less than 20 tests is not comprehensive
3. **src/index.ts not updated in all 3 places** - Very common mistake
4. **Tests don't cover edge cases** - Must include unusual patterns
5. **Build fails** - TypeScript errors must be resolved
