# Iterative Debugging Skill

> Version: 1.0.0
> Compiler: manual (bootstrap)
> Last Updated: 2026-01-22

Systematic fix-verify-iterate debugging cycles with tools, not humans.

## When to Activate

Use this skill when:
- Debugging an issue
- Fixing an error
- Investigating why something is broken
- Encountering an error during task execution

## Core Principles

### 1. Hypothesis-Driven Debugging
Form a specific hypothesis about the cause before making changes.

*Random changes waste time; targeted changes based on evidence converge faster.*

### 2. One Change At A Time
Make exactly one change, then verify; never batch unrelated fixes.

*Batched changes make it impossible to know what worked if it succeeds, or what failed if it doesn't.*

### 3. Verify Immediately
After every change, run the verification step immediately.

*Fast feedback loops prevent going down wrong paths.*

### 4. Preserve Evidence
Capture logs, errors, and state at each iteration.

*Evidence enables backtracking and pattern recognition across attempts.*

### 5. Escalate With Context
If stuck after 3-5 iterations, escalate with full evidence chain.

*Knowing what was tried prevents duplicate effort.*

---

## Workflow

### Phase 1: Reproduce

Confirm the bug exists and capture initial state.

1. Run the failing scenario to confirm the bug
2. Capture the exact error message, stack trace, or unexpected behavior
3. Note the environment details (versions, config, state)
4. Establish baseline - what exactly is broken

**Outputs:** Confirmed reproduction steps, Initial error evidence, Baseline state

### Phase 2: Hypothesize

Form a specific, testable hypothesis about the cause.

1. Read the error message carefully - what is it actually saying
2. Trace the call stack to identify the failure point
3. Consider recent changes that might have caused this
4. Form a specific hypothesis (not "something is wrong" but "X is null because Y")

**Outputs:** Specific hypothesis, Predicted fix

### Phase 3: Fix

Make exactly one targeted change based on the hypothesis.

1. Implement the minimal fix that addresses the hypothesis
2. Make ONLY this one change
3. Document what was changed and why

**Outputs:** Single, targeted code change, Change rationale

### Phase 4: Verify

Test whether the fix resolved the issue.

1. Run the exact same reproduction steps from Phase 1
2. Compare result to baseline
3. If fixed, run related tests to check for regressions
4. If not fixed, capture new evidence (different error? same error? partial improvement?)

**Outputs:** Pass/fail result, New evidence if failed, Regression check if passed

### Phase 5: Iterate or Complete

Based on verification, either continue debugging or declare victory.

1. If fixed - document the root cause and solution
2. If not fixed - update hypothesis based on new evidence
3. If stuck after 3-5 iterations - compile evidence chain and escalate
4. Return to Phase 2 with refined hypothesis

**Outputs:** Resolution documentation OR Updated hypothesis for next iteration OR Escalation package with evidence chain

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Binary Search Debugging** | Bug is somewhere in a large change or code path | Bisect the code or changes to narrow down the exact failure point | Logarithmic reduction beats linear scanning |
| **Print Statement Archaeology** | State is unclear at a failure point | Add targeted logging around the suspected area, run, examine output | Direct observation beats speculation |
| **Diff Against Working** | Something that used to work is now broken | Diff current state against last known working state | Changes are finite; one of them caused the bug |
| **Minimal Reproduction** | Bug is hard to reproduce or involves complex state | Strip away everything not essential to the bug | Isolation reveals the core issue |
| **Rubber Duck** | Stuck and hypotheses are exhausted | Explain the problem out loud, step by step, as if teaching someone | Articulation often reveals overlooked assumptions |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Shotgun Debugging** | If it works, you don't know why; if it fails, you don't know what to undo | One change at a time, verify after each |
| **Hypothesis-Free Changes** | Random walk through solution space is exponentially slow | Always articulate why you think this change will help |
| **Skipping Verification** | False confidence; bug may persist or new bugs introduced | Always verify immediately after every change |
| **Evidence Amnesia** | May retry same failed approaches; cannot escalate effectively | Keep a log of hypothesis, change, and result for each iteration |
| **Premature Escalation** | Wastes others' time; misses learning opportunity | Try 3-5 focused iterations with evidence before escalating |
| **Infinite Loop** | Sunk cost fallacy; diminishing returns | Escalate with evidence chain after 3-5 attempts |

---

## Quality Checklist

Before completing:

- [ ] Reproduced the bug and captured initial evidence
- [ ] Formed a specific, testable hypothesis
- [ ] Made exactly one change based on hypothesis
- [ ] Verified immediately after the change
- [ ] Captured evidence of result (pass or new failure state)
- [ ] Either resolved with documentation OR updated hypothesis for next iteration
- [ ] After 3-5 failed iterations, escalated with full evidence chain

---

## Examples

**API returns 500 error**

1. **Reproduce**: curl the endpoint, confirm 500, capture response body
2. **Hypothesize**: Stack trace shows null pointer in UserService.getUser() - hypothesis is user ID is not being passed
3. **Fix**: Add null check and logging for user ID parameter
4. **Verify**: curl again, now see "user_id is null" in logs - hypothesis confirmed but root cause is upstream
5. **Iterate**: New hypothesis - the auth middleware is not extracting user ID from token
6. **Fix**: Check auth middleware, find token parsing bug
7. **Verify**: curl again, now returns 200 with correct user data
8. **Complete**: Document root cause (token parsing) and fix

**UI element not rendering**

1. **Reproduce**: Load page in browser, confirm element missing, open dev tools
2. **Hypothesize**: Console shows "cannot read property X of undefined" - hypothesis is data not loaded
3. **Fix**: Add defensive check and loading state
4. **Verify**: Reload page, element still missing but no console error - partial progress
5. **Iterate**: New hypothesis - CSS is hiding the element
6. **Fix**: Inspect element, find display:none from parent component
7. **Verify**: Override CSS, element appears - root cause confirmed
8. **Complete**: Fix parent component conditional rendering logic

---

## References

- "The Art of Debugging with GDB, DDD, and Eclipse" - Norman Matloff
- "Debugging: The 9 Indispensable Rules" - David J. Agans
- Session insight - iterative fix cycles during Oracy web app debugging
