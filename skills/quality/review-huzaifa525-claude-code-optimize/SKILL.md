---
name: review
description: Use when the user wants a code review, quality check, or asks to review their changes.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Explore
---

Review all current code changes using two-stage review.

## Iron Law

> **Two stages. In order. No shortcuts.**
> Stage 1 (Spec Compliance) MUST pass before Stage 2 (Code Quality) begins.
> These are different questions: "Did you build the right thing?" vs "Did you build it well?"

## Stage 1: Spec Compliance

**Question: Does the code do what was intended?**

1. **Get the diff**
   ```
   git diff
   git diff --cached
   ```

2. **Identify the intent** — What was the goal of these changes? Check:
   - Commit messages
   - Related issue/PR descriptions
   - task_plan.md if it exists
   - Ask the user if intent is unclear

3. **Verify spec compliance:**
   - Does the implementation match the stated goal?
   - Are all requirements addressed?
   - Are edge cases from the spec handled?
   - Were the correct files modified (not random unrelated changes)?
   - Do new features have corresponding tests?

4. **Stage 1 Verdict:**
   - **PASS** — Implementation matches intent. Proceed to Stage 2.
   - **FAIL** — Implementation misses requirements. List what's missing. STOP HERE.

## Stage 2: Code Quality

**Question: Is the code well-written?** (Only after Stage 1 PASSES)

Read each changed file in full to understand context, then check:

### Security
- Hardcoded secrets, API keys, passwords
- SQL injection, XSS, command injection
- Unsanitized user input
- Missing authentication/authorization checks
- Sensitive data in logs or error messages

### Performance
- N+1 query patterns
- Missing database indexes on new columns
- Unnecessary re-renders (React)
- Large synchronous operations blocking event loop
- Missing pagination on list endpoints
- Memory leaks (unclosed resources, event listeners)

### Code Quality
- Dead code or unused imports
- Duplicated logic (DRY violations)
- Functions too long (> 50 lines)
- Deeply nested conditionals (> 3 levels)
- Magic numbers or hardcoded strings
- Inconsistent naming with rest of codebase
- Missing error handling on external calls

### Convention Compliance
- Does it follow existing codebase patterns?
- Consistent with CLAUDE.md rules?
- Test coverage for new code?
- Consistent file/function naming?

## Output Format

```
## Code Review — Two-Stage

### Stage 1: Spec Compliance — PASS/FAIL
- Intent: [what the changes aim to do]
- Verdict: [pass/fail with reasoning]
- [If FAIL: what's missing or wrong]

### Stage 2: Code Quality — PASS/FAIL

#### Critical (must fix before merge)
- [file:line] [issue] — [why it matters]

#### Warning (should fix)
- [file:line] [issue] — [why it matters]

#### Suggestion (nice to have)
- [file:line] [suggestion]

#### Good Practices Observed
- [what was done well — reinforce good patterns]
```

## Pre-Delivery Checklist

Before presenting the review, verify:

- [ ] All changed files were read in full (not just the diff)
- [ ] Stage 1 verdict is explicitly stated (PASS/FAIL)
- [ ] Every critical issue has a file:line reference
- [ ] Security section checked for OWASP top 5 at minimum
- [ ] No "looks fine" without specific evidence
- [ ] Existing test coverage verified for new code
- [ ] Convention compliance checked against CLAUDE.md
- [ ] Good practices section is not empty — always acknowledge what was done well

## Anti-Rationalization

| Excuse | Rebuttal |
|--------|----------|
| "The spec is unclear so I'll skip Stage 1" | Then ASK for clarification. Unclear spec = ask, not skip. |
| "This is just a small change, doesn't need full review" | Small changes cause big bugs. Review everything. |
| "The code works, so the quality doesn't matter" | Working code that's unreadable is a liability. Quality always matters. |
| "I wrote this code so I know it's correct" | You have blind spots on your own code. Review it as if someone else wrote it. |
| "The security check is overkill for internal code" | Internal code gets exposed. Check it anyway. |
| "Tests are passing so it must be fine" | Tests check behavior. Review checks maintainability, security, and conventions. |

## Pre-Delivery Checklist

Before presenting the review, verify:

- [ ] `git diff` and `git diff --cached` were both read
- [ ] Every changed file was read in full (not just the diff)
- [ ] Stage 1 (spec compliance) was completed before Stage 2
- [ ] All security checks were performed (secrets, injection, auth)
- [ ] Convention compliance was checked against CLAUDE.md
- [ ] Each issue has file:line, description, and severity
- [ ] Good practices were acknowledged (not just negatives)
- [ ] No "probably fine" — every concern is flagged or verified

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
