---
name: quality-gates
description: Implement quality gates, user approval, iteration loops, and test-driven development. Use when validating with users, implementing feedback loops, classifying issue severity, running test-driven loops, or building multi-iteration workflows. Trigger keywords - "approval", "user validation", "iteration", "feedback loop", "severity", "test-driven", "TDD", "quality gate", "consensus".
version: 0.1.0
tags: [orchestration, quality-gates, approval, iteration, feedback, severity, test-driven, TDD]
keywords: [approval, validation, iteration, feedback-loop, severity, test-driven, TDD, quality-gate, consensus, user-approval]
---

# Quality Gates

**Version:** 1.0.0
**Purpose:** Patterns for approval gates, iteration loops, and quality validation in multi-agent workflows
**Status:** Production Ready

## Overview

Quality gates are checkpoints in workflows where execution pauses for validation before proceeding. They prevent low-quality work from advancing through the pipeline and ensure user expectations are met.

This skill provides battle-tested patterns for:
- **User approval gates** (cost gates, quality gates, final acceptance)
- **Iteration loops** (automated refinement until quality threshold met)
- **Issue severity classification** (CRITICAL, HIGH, MEDIUM, LOW)
- **Multi-reviewer consensus** (unanimous vs majority agreement)
- **Feedback loops** (user reports issues → agent fixes → user validates)
- **Test-driven development loops** (write tests → run → analyze failures → fix → repeat)

Quality gates transform "fire and forget" workflows into **iterative refinement systems** that consistently produce high-quality results.

## Core Patterns

### Pattern 1: User Approval Gates

**When to Ask for Approval:**

Use approval gates for:
- **Cost gates:** Before expensive operations (multi-model review, large-scale refactoring)
- **Quality gates:** Before proceeding to next phase (design validation before implementation)
- **Final validation:** Before completing workflow (user acceptance testing)
- **Irreversible operations:** Before destructive actions (delete files, database migrations)

**How to Present Approval:**

```
Good Approval Prompt:

"You selected 5 AI models for code review:
 - Claude Sonnet (embedded, free)
 - Grok Code Fast (external, $0.002)
 - Gemini 2.5 Flash (external, $0.001)
 - GPT-5 Codex (external, $0.004)
 - DeepSeek Coder (external, $0.001)

 Estimated total cost: $0.008 ($0.005 - $0.010)
 Expected duration: ~5 minutes

 Proceed with multi-model review? (Yes/No/Cancel)"

Why it works:
✓ Clear context (what will happen)
✓ Cost transparency (range, not single number)
✓ Time expectation (5 minutes)
✓ Multiple options (Yes/No/Cancel)
```

**Anti-Pattern: Vague Approval**

```
❌ Wrong:

"This will cost money. Proceed? (Yes/No)"

Why it fails:
✗ No cost details (how much?)
✗ No context (what will happen?)
✗ No alternatives (what if user says no?)
```

**Handling User Responses:**

```
User says YES:
  → Proceed with workflow
  → Track approval in logs
  → Continue to next step

User says NO:
  → Offer alternatives:
    1. Use fewer models (reduce cost)
    2. Use only free embedded Claude
    3. Skip this step entirely
    4. Cancel workflow
  → Ask user to choose alternative
  → Proceed based on choice

User says CANCEL:
  → Gracefully exit workflow
  → Save partial results (if any)
  → Log cancellation reason
  → Clean up temporary files
  → Notify user: "Workflow cancelled. Partial results saved to..."
```

**Approval Bypasses (Advanced):**

For automated workflows, allow approval bypass:

```
Automated Workflow Mode:

If workflow is triggered by CI/CD or scheduled task:
  → Skip user approval gates
  → Use predefined defaults (e.g., max cost $0.10)
  → Log decisions for audit trail
  → Email report to stakeholders after completion

Example:
  if (isAutomatedMode) {
    if (estimatedCost <= maxAutomatedCost) {
      log("Auto-approved: $0.008 <= $0.10 threshold");
      proceed();
    } else {
      log("Auto-rejected: $0.008 > $0.10 threshold");
      notifyStakeholders("Cost exceeds automated threshold");
      abort();
    }
  }
```

---

### Pattern 2: Iteration Loop Patterns

**Max Iteration Limits:**

Always set a **max iteration limit** to prevent infinite loops:

```
Typical Iteration Limits:

Automated quality loops: 10 iterations
  - Designer validation → Developer fixes → Repeat
  - Test failures → Developer fixes → Repeat

User feedback loops: 5 rounds
  - User reports issues → Developer fixes → User validates → Repeat

Code review loops: 3 rounds
  - Reviewer finds issues → Developer fixes → Re-review → Repeat

Multi-model consensus: 1 iteration (no loop)
  - Parallel review → Consolidate → Present
```

**Exit Criteria:**

Define clear **exit criteria** for each loop type:

```
Loop Type: Design Validation

Exit Criteria (checked after each iteration):
  1. Designer assessment = PASS → Exit loop (success)
  2. Iteration count >= 10 → Exit loop (max iterations)
  3. User manually approves → Exit loop (user override)
  4. No changes made by developer → Exit loop (stuck, escalate)

Example:
  for (let i = 1; i <= 10; i++) {
    const review = await designer.validate();

    if (review.assessment === "PASS") {
      log("Design validation passed on iteration " + i);
      break;  // Success exit
    }

    if (i === 10) {
      log("Max iterations reached. Escalating to user validation.");
      break;  // Max iterations exit
    }

    await developer.fix(review.issues);
  }
```

**Progress Tracking:**

Show clear progress to user during iterations:

```
Iteration Loop Progress:

Iteration 1/10: Designer found 5 issues → Developer fixing...
Iteration 2/10: Designer found 3 issues → Developer fixing...
Iteration 3/10: Designer found 1 issue → Developer fixing...
Iteration 4/10: Designer assessment: PASS ✓

Loop completed in 4 iterations.
```

**Iteration History Documentation:**

Track what happened in each iteration:

```
Iteration History (ai-docs/iteration-history.md):

## Iteration 1
Designer Assessment: NEEDS IMPROVEMENT
Issues Found:
  - Button color doesn't match design (#3B82F6 vs #2563EB)
  - Spacing between elements too tight (8px vs 16px)
  - Font size incorrect (14px vs 16px)
Developer Actions:
  - Updated button color to #2563EB
  - Increased spacing to 16px
  - Changed font size to 16px

## Iteration 2
Designer Assessment: NEEDS IMPROVEMENT
Issues Found:
  - Border radius too large (8px vs 4px)
Developer Actions:
  - Reduced border radius to 4px

## Iteration 3
Designer Assessment: PASS ✓
Issues Found: None
Result: Design validation complete
```

---

### Pattern 3: Issue Severity Classification

**Severity Levels:**

Use 4-level severity classification:

```
CRITICAL - Must fix immediately
  - Blocks core functionality
  - Security vulnerabilities (SQL injection, XSS, auth bypass)
  - Data loss risk
  - System crashes
  - Build failures

  Action: STOP workflow, fix immediately, re-validate

HIGH - Should fix soon
  - Major bugs (incorrect behavior)
  - Performance issues (>3s page load, memory leaks)
  - Accessibility violations (keyboard navigation broken)
  - User experience blockers

  Action: Fix in current iteration, proceed after fix

MEDIUM - Should fix
  - Minor bugs (edge cases, visual glitches)
  - Code quality issues (duplication, complexity)
  - Non-blocking performance issues
  - Incomplete error handling

  Action: Fix if time permits, or schedule for next iteration

LOW - Nice to have
  - Code style inconsistencies
  - Minor refactoring opportunities
  - Documentation improvements
  - Polish and optimization

  Action: Log for future improvement, proceed without fixing
```

**Severity-Based Prioritization:**

```
Issue List (sorted by severity):

CRITICAL Issues (must fix all before proceeding):
  1. SQL injection in user search endpoint
  2. Missing authentication check on admin routes
  3. Password stored in plaintext

HIGH Issues (fix before code review):
  4. Memory leak in WebSocket connection
  5. Missing error handling in payment flow
  6. Accessibility: keyboard navigation broken

MEDIUM Issues (fix if time permits):
  7. Code duplication in auth controllers
  8. Inconsistent error messages
  9. Missing JSDoc comments

LOW Issues (defer to future):
  10. Variable naming inconsistency
  11. Redundant type annotations
  12. CSS could use more specificity

Action Plan:
  - Fix CRITICAL (1-3) immediately → Re-run tests
  - Fix HIGH (4-6) before code review
  - Log MEDIUM (7-9) for next iteration
  - Ignore LOW (10-12) for now
```

**Severity Escalation:**

Issues can escalate in severity based on context:

```
Context-Based Escalation:

Issue: "Missing error handling in payment flow"
  Base Severity: MEDIUM (code quality issue)

  Context 1: Development environment
    → Severity: MEDIUM (not user-facing yet)

  Context 2: Production environment
    → Severity: HIGH (affects real users, money involved)

  Context 3: Production + recent payment failures
    → Severity: CRITICAL (actively causing issues)

Rule: Escalate severity when:
  - Issue affects production users
  - Issue involves money/security/data
  - Issue is currently causing failures
```

---

### Pattern 4: Multi-Reviewer Consensus

**Consensus Levels:**

When multiple reviewers evaluate the same code/design:

```
UNANIMOUS (100% agreement):
  - ALL reviewers flagged this issue
  - VERY HIGH confidence
  - Highest priority (likely a real problem)

Example:
  3/3 reviewers: "SQL injection in search endpoint"
  → UNANIMOUS consensus
  → CRITICAL priority (all agree it's critical)

STRONG CONSENSUS (67-99% agreement):
  - MOST reviewers flagged this issue
  - HIGH confidence
  - High priority (probably a real problem)

Example:
  2/3 reviewers: "Missing input validation"
  → STRONG consensus (67%)
  → HIGH priority

MAJORITY (50-66% agreement):
  - HALF or more flagged this issue
  - MEDIUM confidence
  - Medium priority (worth investigating)

Example:
  2/3 reviewers: "Code duplication in controllers"
  → MAJORITY consensus (67%)
  → MEDIUM priority

DIVERGENT (< 50% agreement):
  - Only 1-2 reviewers flagged this issue
  - LOW confidence
  - Low priority (may be model-specific or false positive)

Example:
  1/3 reviewers: "Variable naming could be better"
  → DIVERGENT (33%)
  → LOW priority (one reviewer's opinion)
```

**Consensus-Based Prioritization:**

```
Prioritized Issue List (by consensus + severity):

1. [UNANIMOUS - CRITICAL] SQL injection in search
   ALL reviewers agree: Claude, Grok, Gemini (3/3)

2. [UNANIMOUS - HIGH] Missing input validation
   ALL reviewers agree: Claude, Grok, Gemini (3/3)

3. [STRONG - HIGH] Memory leak in WebSocket
   MOST reviewers agree: Claude, Grok (2/3)

4. [MAJORITY - MEDIUM] Code duplication
   HALF+ reviewers agree: Claude, Gemini (2/3)

5. [DIVERGENT - LOW] Variable naming
   SINGLE reviewer: Claude only (1/3)

Action:
  - Fix issues 1-2 immediately (unanimous + CRITICAL/HIGH)
  - Fix issue 3 before review (strong consensus)
  - Consider issue 4 (majority, but medium severity)
  - Ignore issue 5 (divergent, likely false positive)
```

---

### Pattern 5: Feedback Loop Implementation

**User Feedback Loop:**

```
Workflow: User Validation with Feedback

Step 1: Initial Implementation
  Developer implements feature
  Designer/Tester validates
  Present to user for manual validation

Step 2: User Validation Gate (MANDATORY)
  Present to user:
    "Implementation complete. Please manually verify:
     - Open app at http://localhost:3000
     - Test feature: [specific instructions]
     - Compare to design reference

     Does it meet expectations? (Yes/No)"

Step 3a: User says YES
  → ✅ Feature approved
  → Generate final report
  → Mark workflow complete

Step 3b: User says NO
  → Collect specific feedback

Step 4: Collect Specific Feedback
  Ask user: "Please describe the issues you found:"

  User response:
    "1. Button color is wrong (should be blue, not green)
     2. Spacing is too tight between elements
     3. Font size is too small"

Step 5: Extract Structured Feedback
  Parse user feedback into structured issues:

  Issue 1:
    Component: Button
    Problem: Color incorrect
    Expected: Blue (#2563EB)
    Actual: Green (#10B981)
    Severity: MEDIUM

  Issue 2:
    Component: Container
    Problem: Spacing too tight
    Expected: 16px
    Actual: 8px
    Severity: MEDIUM

  Issue 3:
    Component: Text
    Problem: Font size too small
    Expected: 16px
    Actual: 14px
    Severity: LOW

Step 6: Launch Fixing Agent
  Task: ui-developer
    Prompt: "Fix user-reported issues:

             1. Button color: Change from #10B981 to #2563EB
             2. Container spacing: Increase from 8px to 16px
             3. Text font size: Increase from 14px to 16px

             User feedback: [user's exact words]"

Step 7: Re-validate
  After fixes:
    - Re-run designer validation
    - Loop back to Step 2 (user validation)

Step 8: Max Feedback Rounds
  Limit: 5 feedback rounds (prevent infinite loop)

  If round > 5:
    Escalate to human review
    "Unable to meet user expectations after 5 rounds.
     Manual intervention required."
```

**Feedback Round Tracking:**

```
Feedback Round History:

Round 1:
  User Issues: Button color, spacing, font size
  Fixes Applied: Updated all 3 issues
  Result: Re-validate

Round 2:
  User Issues: Border radius too large
  Fixes Applied: Reduced border radius
  Result: Re-validate

Round 3:
  User Issues: None
  Result: ✅ APPROVED

Total Rounds: 3/5
```

---

### Pattern 6: Test-Driven Development Loop

**When to Use:**

Use TDD loop **after implementing code, before code review**:

```
Workflow Phases:

Phase 1: Architecture Planning
Phase 2: Implementation
Phase 2.5: Test-Driven Development Loop ← THIS PATTERN
Phase 3: Code Review
Phase 4: User Acceptance
```

**The TDD Loop Pattern:**

```
Step 1: Write Tests First
  Task: test-architect
    Prompt: "Write comprehensive tests for authentication feature.
             Requirements: [link to requirements]
             Implementation: [link to code]"
    Output: tests/auth.test.ts

Step 2: Run Tests
  Bash: bun test tests/auth.test.ts
  Capture output and exit code

Step 3: Check Test Results
  If all tests pass:
    → ✅ TDD loop complete
    → Proceed to code review (Phase 3)

  If tests fail:
    → Analyze failure (continue to Step 4)

Step 4: Analyze Test Failure
  Task: test-architect
    Prompt: "Analyze test failure output:

             [test failure logs]

             Determine root cause:
             - TEST_ISSUE: Test has bug (bad assertion, missing mock, wrong expectation)
             - IMPLEMENTATION_ISSUE: Code has bug (logic error, missing validation, incorrect behavior)

             Provide detailed analysis."

  test-architect returns:
    verdict: TEST_ISSUE | IMPLEMENTATION_ISSUE
    analysis: Detailed explanation
    recommendation: Specific fix needed

Step 5a: If TEST_ISSUE (test is wrong)
  Task: test-architect
    Prompt: "Fix test based on analysis:
             [analysis from Step 4]"

  After fix:
    → Re-run tests (back to Step 2)
    → Loop continues

Step 5b: If IMPLEMENTATION_ISSUE (code is wrong)
  Provide structured feedback to developer:

  Task: backend-developer
    Prompt: "Fix implementation based on test failure:

             Test Failure:
             [failure output]

             Root Cause:
             [analysis from test-architect]

             Recommended Fix:
             [specific fix needed]"

  After fix:
    → Re-run tests (back to Step 2)
    → Loop continues

Step 6: Max Iteration Limit
  Limit: 10 iterations

  Iteration tracking:
    Iteration 1/10: 5 tests failed → Fix implementation
    Iteration 2/10: 2 tests failed → Fix test (bad mock)
    Iteration 3/10: All tests pass ✅

  If iteration > 10:
    Escalate to human review
    "Unable to pass all tests after 10 iterations.
     Manual debugging required."
```

**Example TDD Loop:**

```
Phase 2.5: Test-Driven Development Loop

Iteration 1:
  Tests Run: 20 tests
  Results: 5 failed, 15 passed
  Failure: "JWT token validation fails with expired token"
  Analysis: IMPLEMENTATION_ISSUE - Missing expiration check
  Fix: Added expiration validation in TokenService
  Re-run: Continue to Iteration 2

Iteration 2:
  Tests Run: 20 tests
  Results: 2 failed, 18 passed
  Failure: "Mock database not reset between tests"
  Analysis: TEST_ISSUE - Missing beforeEach cleanup
  Fix: Added database reset in test setup
  Re-run: Continue to Iteration 3

Iteration 3:
  Tests Run: 20 tests
  Results: All passed ✅
  Result: TDD loop complete, proceed to code review

Total Iterations: 3/10
Duration: ~5 minutes
Benefits:
  - Caught 2 bugs before code review
  - Fixed 1 test quality issue
  - All tests passing gives confidence in implementation
```

**Benefits of TDD Loop:**

```
Benefits:

1. Catch bugs early (before code review, not after)
2. Ensure test quality (test-architect fixes bad tests)
3. Automated quality assurance (no manual testing needed)
4. Fast feedback loop (seconds to run tests, not minutes)
5. Confidence in implementation (all tests passing)

Performance:
  Traditional: Implement → Review → Find bugs → Fix → Re-review
  Time: 30+ minutes, multiple review rounds

  TDD Loop: Implement → Test → Fix → Test → Review (with confidence)
  Time: 15 minutes, single review round (fewer issues)
```

---

## Integration with Other Skills

**quality-gates + multi-model-validation:**

```
Use Case: Cost approval before multi-model review

Step 1: Estimate costs (multi-model-validation)
Step 2: User approval gate (quality-gates)
  If approved: Proceed with parallel execution
  If rejected: Offer alternatives
Step 3: Execute review (multi-model-validation)
```

**quality-gates + multi-agent-coordination:**

```
Use Case: Iteration loop with designer validation

Step 1: Agent selection (multi-agent-coordination)
  Select designer + ui-developer

Step 2: Iteration loop (quality-gates)
  For i = 1 to 10:
    - Run designer validation
    - If PASS: Exit loop
    - Else: Delegate to ui-developer for fixes

Step 3: User validation gate (quality-gates)
  Mandatory manual approval
```

**quality-gates + error-recovery:**

```
Use Case: Test-driven loop with error recovery

Step 1: Run tests (quality-gates TDD pattern)
Step 2: If test execution fails (error-recovery)
  - Syntax error → Fix and retry
  - Framework crash → Notify user, skip TDD
Step 3: If tests pass (quality-gates)
  - Proceed to code review
```

---

## Best Practices

**Do:**
- ✅ Set max iteration limits (prevent infinite loops)
- ✅ Define clear exit criteria (PASS, max iterations, user override)
- ✅ Track iteration history (document what happened)
- ✅ Show progress to user ("Iteration 3/10 complete")
- ✅ Classify issue severity (CRITICAL → HIGH → MEDIUM → LOW)
- ✅ Prioritize by consensus + severity
- ✅ Ask user approval for expensive operations
- ✅ Collect specific feedback (not vague complaints)
- ✅ Use TDD loop to catch bugs early

**Don't:**
- ❌ Create infinite loops (no exit criteria)
- ❌ Skip user validation gates (mandatory for UX)
- ❌ Ignore consensus (unanimous issues are real)
- ❌ Batch all severities together (prioritize CRITICAL)
- ❌ Proceed without approval for >$0.01 operations
- ❌ Collect vague feedback ("it's wrong" → what specifically?)
- ❌ Skip TDD loop (catches bugs before expensive review)

**Performance:**
- Iteration loops: 5-10 iterations typical, max 10-15 min
- TDD loop: 3-5 iterations typical, max 5-10 min
- User feedback: 1-3 rounds typical, max 5 rounds

---

## Examples

### Example 1: User Approval Gate for Multi-Model Review

**Scenario:** User requests multi-model review, costs $0.008

**Execution:**

```
Step 1: Estimate Costs
  Input: 450 lines × 1.5 = 675 tokens per model
  Output: 2000-4000 tokens per model
  Total: 3 models × 3000 avg = 9000 output tokens
  Cost: ~$0.008 ($0.005 - $0.010)

Step 2: Present Approval Gate
  "Multi-model review will analyze 450 lines with 3 AI models:
   - Claude Sonnet (embedded, free)
   - Grok Code Fast (external, $0.002)
   - Gemini 2.5 Flash (external, $0.001)

   Estimated cost: $0.008 ($0.005 - $0.010)
   Duration: ~5 minutes

   Proceed? (Yes/No/Cancel)"

Step 3a: User says YES
  → Proceed with parallel execution
  → Track approval: log("User approved $0.008 cost")

Step 3b: User says NO
  → Offer alternatives:
    1. Use only free Claude (no external models)
    2. Use only 1 external model (reduce cost to $0.002)
    3. Skip review entirely
  → Ask user to choose

Step 3c: User says CANCEL
  → Exit gracefully
  → Log: "User cancelled multi-model review"
  → Clean up temporary files
```

---

### Example 2: Designer Validation Iteration Loop

**Scenario:** UI implementation with automated iteration until PASS

**Execution:**

```
Iteration 1:
  Task: designer
    Prompt: "Validate navbar against Figma design"
    Output: ai-docs/design-review-1.md
    Assessment: NEEDS IMPROVEMENT
    Issues:
      - Button color: #3B82F6 (expected #2563EB)
      - Spacing: 8px (expected 16px)

  Task: ui-developer
    Prompt: "Fix issues from ai-docs/design-review-1.md"
    Changes: Updated button color, increased spacing

  Result: Continue to Iteration 2

Iteration 2:
  Task: designer
    Prompt: "Re-validate navbar"
    Output: ai-docs/design-review-2.md
    Assessment: NEEDS IMPROVEMENT
    Issues:
      - Border radius: 8px (expected 4px)

  Task: ui-developer
    Prompt: "Fix border radius issue"
    Changes: Reduced border radius to 4px

  Result: Continue to Iteration 3

Iteration 3:
  Task: designer
    Prompt: "Re-validate navbar"
    Output: ai-docs/design-review-3.md
    Assessment: PASS ✓
    Issues: None

  Result: Exit loop (success)

Summary:
  Total Iterations: 3/10
  Duration: ~8 minutes
  Automated Fixes: 3 issues resolved
  Result: PASS, proceed to user validation
```

---

### Example 3: Test-Driven Development Loop

**Scenario:** Authentication implementation with TDD

**Execution:**

```
Phase 2.5: Test-Driven Development Loop

Iteration 1:
  Task: test-architect
    Prompt: "Write tests for authentication feature"
    Output: tests/auth.test.ts (20 tests)

  Bash: bun test tests/auth.test.ts
    Result: 5 failed, 15 passed

  Task: test-architect
    Prompt: "Analyze test failures"
    Verdict: IMPLEMENTATION_ISSUE
    Analysis: "Missing JWT expiration validation"

  Task: backend-developer
    Prompt: "Add JWT expiration validation"
    Changes: Updated TokenService.verify()

  Bash: bun test tests/auth.test.ts
    Result: Continue to Iteration 2

Iteration 2:
  Bash: bun test tests/auth.test.ts
    Result: 2 failed, 18 passed

  Task: test-architect
    Prompt: "Analyze test failures"
    Verdict: TEST_ISSUE
    Analysis: "Mock database not reset between tests"

  Task: test-architect
    Prompt: "Fix test setup"
    Changes: Added beforeEach cleanup

  Bash: bun test tests/auth.test.ts
    Result: Continue to Iteration 3

Iteration 3:
  Bash: bun test tests/auth.test.ts
    Result: All 20 passed ✅

  Result: TDD loop complete, proceed to code review

Summary:
  Total Iterations: 3/10
  Duration: ~5 minutes
  Bugs Caught: 1 implementation bug, 1 test bug
  Result: All tests passing, high confidence in code
```

---

## Troubleshooting

**Problem: Infinite iteration loop**

Cause: No exit criteria or max iteration limit

Solution: Always set max iterations (10 for automated, 5 for user feedback)

```
❌ Wrong:
  while (true) {
    if (review.assessment === "PASS") break;
    fix();
  }

✅ Correct:
  for (let i = 1; i <= 10; i++) {
    if (review.assessment === "PASS") break;
    if (i === 10) escalateToUser();
    fix();
  }
```

---

**Problem: User approval skipped for expensive operation**

Cause: Missing approval gate

Solution: Always ask approval for costs >$0.01

```
❌ Wrong:
  if (userRequestedMultiModel) {
    executeReview();
  }

✅ Correct:
  if (userRequestedMultiModel) {
    const cost = estimateCost();
    if (cost > 0.01) {
      const approved = await askUserApproval(cost);
      if (!approved) return offerAlternatives();
    }
    executeReview();
  }
```

---

**Problem: All issues treated equally**

Cause: No severity classification

Solution: Classify by severity, prioritize CRITICAL

```
❌ Wrong:
  issues.forEach(issue => fix(issue));

✅ Correct:
  const critical = issues.filter(i => i.severity === "CRITICAL");
  const high = issues.filter(i => i.severity === "HIGH");

  critical.forEach(issue => fix(issue));  // Fix critical first
  high.forEach(issue => fix(issue));      // Then high
  // MEDIUM and LOW deferred or skipped
```

---

## Summary

Quality gates ensure high-quality results through:

- **User approval gates** (cost, quality, final validation)
- **Iteration loops** (automated refinement, max 10 iterations)
- **Severity classification** (CRITICAL → HIGH → MEDIUM → LOW)
- **Consensus prioritization** (unanimous → strong → majority → divergent)
- **Feedback loops** (collect specific issues, fix, re-validate)
- **Test-driven development** (write tests, run, fix, repeat until pass)

Master these patterns and your workflows will consistently produce high-quality, validated results.

---

**Extracted From:**
- `/review` command (user approval for costs, consensus analysis)
- `/validate-ui` command (iteration loops, user validation gates, feedback collection)
- `/implement` command (PHASE 2.5 test-driven development loop)
- Multi-model review patterns (consensus-based prioritization)
