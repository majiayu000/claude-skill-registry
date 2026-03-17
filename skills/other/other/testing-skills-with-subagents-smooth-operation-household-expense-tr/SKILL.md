---
name: testing-skills-with-subagents
description: "Use to validate process documentation. Apply TDD to skill writing: RED (run without skill, document failures) → GREEN (write skill) → REFACTOR (close loopholes). Test under pressure: time constraints, sunk cost, exhaustion, authority."
---

# Testing Skills with Subagents

## Core Principle

Skills are process documentation. Like code, they need tests. Use TDD to validate skills actually work under pressure.

## When to Use This Skill

- Writing new skills
- Validating existing skills
- Skill seems incomplete
- Want to ensure skill works
- Before sharing skills upstream
- After receiving feedback on skills
- Refining skill effectiveness

## The Iron Law

**NO SKILL WITHOUT A FAILING TEST FIRST.**

If you can't demonstrate the skill solves a problem, you don't need the skill.

## Why Test Skills?

**Benefits:**
✅ Proves skill actually helps
✅ Finds gaps and loopholes
✅ Validates under pressure
✅ Creates realistic examples
✅ Builds confidence in skill

**Without testing:**
❌ Untested assumptions
❌ Skill might not work
❌ Loopholes undiscovered
❌ No proof of value
❌ False confidence

## TDD for Skills

### RED: Run Scenarios WITHOUT Skill

```
🔴 RED Phase: Establish baseline

Scenario: Debug intermittent test failure without root-cause-tracing skill

Setup:
- Fresh subagent
- Give debugging task
- Do NOT provide root-cause-tracing skill
- Observe behavior

Task given to subagent:
---
You are debugging a test that fails intermittently (1 in 20 runs).

Test:
```php
public function test_order_total()
{
    $order = Order::factory()->create();
    $order->addItem(['price' => 10, 'qty' => 2]);

    $this->assertEquals(20, $order->total());
    // Sometimes fails: Expected 20, got 0
}
```

Debug this issue and fix it.
---

Observed behavior (WITHOUT skill):
1. Subagent adds logging
2. Runs test multiple times
3. Finds timing issue
4. Fixes symptom (adds sleep)
5. ❌ Does NOT trace to root cause
6. ❌ Does NOT find async job issue
7. ❌ Quick fix instead of proper fix

FAILURES DOCUMENTED:
- Stopped at symptom, not root cause
- Added sleep() instead of fixing architecture
- Didn't trace backward through call chain
- Missed the async job that caused race condition

✅ Baseline failures documented
Ready for GREEN phase
```

### GREEN: Write Skill to Address Failures

```
🟢 GREEN Phase: Create skill

Based on RED phase failures, write skill that addresses:
1. Stopping at symptoms ← Need backward tracing process
2. Quick fixes ← Need emphasis on finding root cause
3. Missing call chain analysis ← Need tracing technique
4. Not finding async issues ← Need timing-related patterns

Write root-cause-tracing skill:
---
# Root Cause Tracing

## The Iron Law
NEVER STOP AT THE SYMPTOM. Trace backward until you find
the ORIGINAL TRIGGER.

## Process
1. Observe symptom
2. Find immediate cause
3. Trace backward through call chain
4. Keep asking "Why?"
5. Find original trigger

...detailed process...
---

Skill written ✅
Ready to test if it works
```

### REFACTOR: Test with Skill, Close Loopholes

```
🔵 REFACTOR Phase: Test skill and refine

Test 1: Same scenario WITH skill
---
Setup:
- Fresh subagent
- Same debugging task
- Include root-cause-tracing skill

Observed behavior (WITH skill):
1. Subagent follows tracing process
2. Observes symptom (0 value)
3. Finds immediate cause (timing)
4. Traces backward (async job)
5. Finds root cause (race condition)
6. ✅ Fixes architecture, not symptom

SUCCESS! Skill prevented failures observed in RED phase.
---

Test 2: Pressure scenario - Time constraint
---
Setup:
- Fresh subagent
- Same task + "You have 5 minutes"
- Include root-cause-tracing skill

Observed behavior:
1. Subagent starts tracing process
2. Time pressure mentioned
3. ❌ Skips tracing, adds quick fix
4. Rationalization: "No time for full trace"

FAILURE! Skill failed under time pressure.

LOOPHOLE FOUND: Skill doesn't address time pressure.

Fix: Add to skill:
"Time pressure is when you MOST need root cause tracing.
Quick fixes under pressure create technical debt that
takes 10x longer to fix later."

Skill updated ✅
---

Test 3: Pressure scenario - Sunk cost
---
Setup:
- Fresh subagent
- Task: "You've spent 2 hours debugging, just make it work"
- Include updated root-cause-tracing skill

Observed behavior:
1. Subagent mentions sunk cost
2. ⚠️ Considers quick fix
3. ✅ Skill reminds: trace to root cause
4. ✅ Completes proper tracing
5. ✅ Finds and fixes root cause

SUCCESS! Updated skill handles sunk cost pressure.
---

Test 4: Pressure scenario - Exhaustion
---
Setup:
- Fresh subagent
- Task: "You've been debugging for 6 hours, tired"
- Include updated skill

Observed behavior:
1. Subagent acknowledges exhaustion
2. ❌ Suggests taking shortcut
3. Rationalization: "I'm too tired to trace properly"

FAILURE! Skill failed under exhaustion.

LOOPHOLE FOUND: Skill doesn't address exhaustion.

Fix: Add to skill:
"When exhausted, your judgment is impaired. This is
when you MOST need to follow the process systematically.
The process protects you when judgment fails."

Skill updated ✅
---

Test 5: Pressure scenario - Authority
---
Setup:
- Fresh subagent
- Task: "Manager says just fix it fast"
- Include updated skill

Observed behavior:
1. Authority pressure mentioned
2. ⚠️ Considers compliance
3. ✅ Skill provides response template
4. ✅ Explains why proper fix is faster
5. ✅ Proceeds with tracing

SUCCESS! Skill handles authority pressure.
---

All pressure scenarios tested ✅
Loopholes found and fixed ✅
Skill ready for use ✅
```

## The Four Pressure Scenarios

### Pressure 1: Time Constraints

```
Scenario: "We need this fixed in 15 minutes"

Without skill:
- Quick fixes
- Symptom treatment
- Technical debt

Test approach:
1. Give subagent task + time limit
2. Observe if skill followed
3. Look for shortcuts
4. Check if skill addresses time pressure

Skill must include:
"Time pressure is when you MOST need systematic approach.
Quick fixes take 10x longer to fix later."
```

### Pressure 2: Sunk Cost

```
Scenario: "You've already spent 3 hours on this"

Without skill:
- Desperation fixes
- "Make it work" mentality
- Abandoning proper process

Test approach:
1. Give subagent task + sunk cost context
2. Observe if skill followed
3. Look for "just make it work"
4. Check if skill addresses sunk cost

Skill must include:
"Sunk cost is irrelevant. What matters: doing it right
vs. doing it twice. Follow the process."
```

### Pressure 3: Exhaustion

```
Scenario: "You've been working for 8 hours straight"

Without skill:
- Impaired judgment
- Taking shortcuts
- Missing obvious things

Test approach:
1. Give subagent task + exhaustion context
2. Observe if skill followed
3. Look for "too tired to do it right"
4. Check if skill addresses exhaustion

Skill must include:
"Exhaustion impairs judgment. Process protects you when
judgment fails. Follow it systematically."
```

### Pressure 4: Authority

```
Scenario: "Boss/client demands quick fix"

Without skill:
- Compliance over quality
- Shortcuts to please
- Technical debt

Test approach:
1. Give subagent task + authority pressure
2. Observe if skill followed
3. Look for inappropriate compliance
4. Check if skill provides response template

Skill must include:
"Authority pressure needs thoughtful response:
'Quick fix now = 10x work later. Let me do this right,
it'll take [time] and prevent future issues.'"
```

## Complete Testing Process

### Step 1: Identify Problem

```
Problem observed:
Subagents fixing symptoms instead of root causes

Evidence:
- Added sleep() for race conditions
- Try/catch to hide errors
- Quick workarounds instead of proper fixes

Need: Skill for root cause tracing
```

### Step 2: RED - Establish Baseline

```
Create 3-5 scenarios:
1. Intermittent test failure
2. Performance issue
3. Data corruption
4. Production bug
5. "Works on my machine"

For each scenario:
1. Fresh subagent
2. No skill provided
3. Observe behavior
4. Document failures

Common failures found:
- Stops at symptoms ✅
- Doesn't trace backward ✅
- Accepts first explanation ✅
- Skips verification ✅
- Makes quick fixes ✅

Baseline documented ✅
```

### Step 3: GREEN - Write Skill

```
Based on failures, write skill:

Must address:
- ✅ Stopping at symptoms → Process for tracing backward
- ✅ Not tracing back → Call chain analysis technique
- ✅ First explanation → "Keep asking why"
- ✅ Skipping verification → Verification step required
- ✅ Quick fixes → Emphasis on root cause

Skill structure:
1. Core Principle
2. When to Use
3. The Iron Law
4. Step-by-step process
5. Examples
6. Common mistakes
7. Authority
8. Commitment

Skill written ✅
```

### Step 4: REFACTOR - Test and Refine

```
Test with skill:
1. Same scenarios from RED phase
2. Fresh subagent each time
3. Include skill
4. Observe improvement

Expected improvement:
- ✅ Traces to root cause (not just symptoms)
- ✅ Follows backward tracing process
- ✅ Asks "Why?" multiple times
- ✅ Verifies root cause hypothesis
- ✅ Makes proper fix

Improvement verified ✅

Test pressure scenarios:
1. Time constraint → ❌ Failed
2. Sunk cost → ✅ Passed
3. Exhaustion → ❌ Failed
4. Authority → ⚠️ Partial

Loopholes found:
- Time pressure needs addressing
- Exhaustion needs addressing
- Authority needs response template

Update skill to close loopholes ✅

Re-test pressure scenarios:
1. Time constraint → ✅ Now passes
2. Sunk cost → ✅ Still passes
3. Exhaustion → ✅ Now passes
4. Authority → ✅ Now passes

All scenarios passing ✅
Skill validated ✅
```

### Step 5: Document Test Results

```
Test Report: root-cause-tracing skill

Scenarios tested: 9 total
- 5 baseline scenarios
- 4 pressure scenarios

RED phase results:
- Intermittent failure: Fixed symptom (sleep), not root cause
- Performance issue: Added cache, didn't find missing index
- Data corruption: Added validation, didn't find race condition
- Production bug: Rolled back, didn't identify cause
- Works locally: Changed config, didn't compare environments

GREEN phase results:
- All 5 scenarios: Root cause found and fixed properly

REFACTOR phase results:
Initial test: 4/4 passed
Pressure test (v1): 2/4 passed
Pressure test (v2): 4/4 passed

Loopholes found and fixed: 2
- Time pressure rationalization
- Exhaustion rationalization

Skill validated ✅
Ready for use ✅
```

## Real-World Example: Testing TDD Skill

```
🔴 RED Phase

Scenario: Add new feature without TDD skill

Task to subagent:
"Add user profile update endpoint"

Observed behavior:
1. ❌ Writes controller code first
2. ❌ Adds tests after code
3. ❌ Tests pass immediately (no RED phase)
4. ❌ Tests check implementation, not behavior

Failures documented:
- Test-after, not test-first
- No RED/GREEN/REFACTOR cycle
- Tests verify implementation

---

🟢 GREEN Phase

Write TDD skill addressing failures:
- Iron Law: TEST FIRST, CODE SECOND
- Process: RED → GREEN → REFACTOR
- Examples of proper TDD cycle
- Anti-patterns to avoid

Skill written ✅

---

🔵 REFACTOR Phase

Test with skill:
1. Same task, include TDD skill
2. Observe: ✅ Writes test first
3. Observe: ✅ Test fails (RED)
4. Observe: ✅ Minimal code to pass
5. Observe: ✅ Refactors with green tests

Improvement verified ✅

Pressure test - Time constraint:
"Add feature in 30 minutes"
Result: ❌ Skips tests, writes code first
Rationalization: "No time for TDD"

LOOPHOLE! Add to skill:
"TDD seems slower but is faster. Bugs caught
immediately, not after deployment. Follow process."

Update skill ✅

Re-test with time pressure:
Result: ✅ Follows TDD despite pressure
Explanation given: "TDD prevents bugs, saves time"

Skill validated ✅
```

## Skill Testing Checklist

For each skill:
- [ ] 3-5 baseline scenarios created
- [ ] RED: Tested without skill
- [ ] Failures documented
- [ ] GREEN: Skill written to address failures
- [ ] REFACTOR: Tested with skill
- [ ] Improvement verified
- [ ] Time pressure scenario tested
- [ ] Sunk cost scenario tested
- [ ] Exhaustion scenario tested
- [ ] Authority scenario tested
- [ ] Loopholes found and fixed
- [ ] Re-tested after updates
- [ ] All scenarios pass
- [ ] Test results documented

## Integration with Skills

**Required for:**
- `writing-skills` - Validate skills before documenting
- `sharing-skills` - Test before contributing upstream

**Use with:**
- `subagent-driven-development` - Each test is a subagent task

**Testing skills:**
- This skill validates other skills
- Ensures skills actually work
- Finds gaps before production use

## Common Mistakes

### Mistake 1: Testing Without Pressure Scenarios

```
❌ BAD:
Only test happy path scenarios
Skip pressure testing
Assume skill will hold up

Result: Skill fails when it matters most

✅ GOOD:
Test under all four pressures
Find loopholes
Strengthen skill
Ensure it works when needed
```

### Mistake 2: Not Establishing Baseline

```
❌ BAD:
Write skill without RED phase
No proof it solves problem
Assume problem exists

Result: Might not need the skill

✅ GOOD:
RED: Document failures without skill
Proves skill is needed
Identifies what to address
Creates realistic examples
```

### Mistake 3: Stopping at First Pass

```
❌ BAD:
Skill passes basic test
Don't test pressure scenarios
Ship it

Result: Loopholes discovered in production

✅ GOOD:
Test basic scenarios
Test pressure scenarios
Find loopholes
Fix loopholes
Re-test
Only then ship
```

## Authority

**This skill is based on:**
- Test-Driven Development applied to process documentation
- RED/GREEN/REFACTOR cycle (Kent Beck)
- Pressure testing from aviation and medical fields
- Quality assurance best practices

**Research**: Studies show tested process documentation is followed 3x more often than untested.

**Parallel**: Just as code needs tests, skills need tests. Same principles apply.

## Your Commitment

When writing skills:
- [ ] I will test skills before using them
- [ ] I will establish baseline (RED phase)
- [ ] I will write skill to address failures (GREEN)
- [ ] I will test under pressure (REFACTOR)
- [ ] I will find and close loopholes
- [ ] I will document test results
- [ ] I will only share tested skills

---

**Bottom Line**: Skills are process documentation. Test them like code. RED (document failures) → GREEN (write skill) → REFACTOR (test under pressure). Find loopholes before they find you.
