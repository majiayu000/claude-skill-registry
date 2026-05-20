---
name: code-review
description: |
  Use after completing tasks to review code for quality and spec compliance.
  Two-stage review: Spec Compliance first, then Code Quality.
---

# Code Review

## Overview

Catch issues before they cascade. Review early, review often.

**Core principle:** Two-stage review ensures both correctness AND quality.

**Announce at start:** "I'm using the code-review skill to review this implementation."

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main
- Before running `/superspec:archive`

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## Two-Stage Review Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    Two-Stage Review                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   Stage 1: Spec Compliance Review                                │
│   └─→ Does implementation match Specs?                          │
│   └─→ Every Requirement implemented?                             │
│   └─→ Every Scenario has test?                                   │
│   └─→ No missing/extra features?                                 │
│                                                                   │
│        [Must pass before Stage 2]                                │
│                                                                   │
│   Stage 2: Code Quality Review                                    │
│   └─→ Error handling                                             │
│   └─→ Type safety                                                │
│   └─→ SOLID principles                                           │
│   └─→ Test quality                                               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Stage 1: Spec Compliance Review

### What to Check

1. **Requirement Coverage**
   - Does implementation match the Requirement description?
   - Are all SHALL/MUST statements implemented?

2. **Scenario Coverage**
   - Is there a test for each Scenario?
   - Does the test cover WHEN condition?
   - Does the test verify THEN result?
   - Does the test verify AND conditions (if any)?

3. **No Missing Features**
   - Are all aspects of the Scenario tested?
   - Any edge cases in the Scenario not covered?

4. **No Extra Features**
   - Is there any code NOT required by the Spec?
   - Any "nice to have" additions not in Spec?

### Review Checklist

```markdown
## Spec Compliance Review

### Requirement: [Name]
[✅ COMPLIANT / ❌ NOT COMPLIANT]

### Scenario: [Name]
- Test exists: [✅/❌]
- WHEN covered: [✅/❌]
- THEN verified: [✅/❌]
- AND verified: [✅/❌ or N/A]

### Issues Found
1. [Issue description] - [Missing/Extra/Incorrect]

### Verdict
[✅ SPEC COMPLIANT / ❌ NEEDS WORK]

If not compliant, list specific fixes needed.
```

### If Spec Review Fails

1. Fix issues found
2. Request re-review
3. Repeat until compliant
4. **Do NOT proceed to Quality Review until Spec Review passes**

## Stage 2: Code Quality Review

### What to Check

1. **Error Handling**
   - Are errors caught appropriately?
   - Are error messages helpful?
   - No swallowed errors?

2. **Type Safety**
   - Proper TypeScript types?
   - No `any` without justification?
   - Null/undefined handled?

3. **Code Quality**
   - SOLID principles followed?
   - No code duplication?
   - Clear naming?
   - Appropriate abstraction level?

4. **Test Quality**
   - Tests are focused (one thing)?
   - Tests are readable?
   - No testing implementation details?
   - Mocks used appropriately?

### Issue Classification

- **Critical**: Must fix before proceeding
- **Important**: Should fix, impacts maintainability
- **Suggestion**: Nice to have, optional

### Review Output

```markdown
## Code Quality Review

### Strengths
- [Good things about the code]

### Issues

#### Critical
1. [Issue] - [Why it's critical] - [Suggested fix]

#### Important
1. [Issue] - [Impact] - [Suggested fix]

#### Suggestions
1. [Suggestion] - [Benefit]

### Verdict
[✅ APPROVED / ❌ NEEDS WORK]

If needs work, list required fixes (Critical + Important).
```

### If Quality Review Fails

1. Fix Critical and Important issues
2. Request re-review
3. Repeat until approved
4. Suggestions are optional

## How to Request Review

### 1. Get Git Context

```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

### 2. Prepare Review Request

```markdown
## Review Request

**Change ID:** [change-id]
**Spec Files:**
- superspec/changes/[id]/specs/[cap]/spec.md

**Task Completed:**
- Requirement: [Name]
- Scenario: [Name]

**Code Changes:**
[Git diff or file paths]

**Base SHA:** [BASE_SHA]
**Head SHA:** [HEAD_SHA]
```

### 3. Act on Feedback

- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Suggestions for later
- Push back if reviewer is wrong (with reasoning)

## Quick Reference

| Stage | Focus | Must Pass |
|-------|-------|-----------|
| 1. Spec Compliance | Correctness | Yes |
| 2. Code Quality | Maintainability | Yes (Critical/Important) |

| Issue Type | Action |
|------------|--------|
| Critical | Fix immediately |
| Important | Fix before proceeding |
| Suggestion | Optional |

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Do Quality review before Spec review
- Accept "close enough" for Spec compliance

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

## Integration with Subagent Development

In subagent-driven development, reviews happen automatically:

1. **Implementer** completes task
2. **Spec Reviewer** checks compliance
3. **Quality Reviewer** checks code quality
4. Issues found → Implementer fixes → Re-review
5. Both pass → Mark task complete

See `subagent-development` skill for full workflow.

## Related References

**Prompt templates (for subagent dispatch):**
- `code-reviewer.md` - Full code reviewer subagent template with placeholders

**Handling review feedback:**
- `receiving-code-review` skill - How to respond to review feedback professionally

## Integration

**Called by:**
- `subagent-development` - Per-task reviews
- Before `verify` - Ensure quality before verification
- Before `finish-branch` - Final check before integration

**Pairs with:**
- `tdd` - Reviews should verify TDD was followed
- `verify` - Reviews complement verification
- `verification-before-completion` - Evidence before claims
