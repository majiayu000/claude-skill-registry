---
name: verification-before-completion
description: |
  Use when about to claim work is complete, fixed, or passing.
  REQUIRES running verification commands and confirming output before making any success claims.
  Evidence before assertions, always.
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| TDD followed | Show failing then passing output | "I followed TDD" |
| Spec compliant | Show test for each Scenario | "Tests exist" |
| Task complete | All verification commands run | "Implementation done" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags - STOP

If you catch yourself:
- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting subagent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

**ALL of these mean: STOP. Run verification first.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ tests ≠ build |
| "Subagent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |
| "I already tested manually" | Manual ≠ automated verification |
| "The code looks correct" | Looking ≠ running |
| "It worked before" | Before ≠ now |
| "Small change, can't break anything" | Small changes break things. Verify. |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**TDD Evidence:**
```
✅ Show failing test output → Show passing test output → "TDD followed"
❌ "I followed TDD" (without evidence)
```

**Spec Compliance:**
```
✅ Show test for Scenario X → Show test for Scenario Y → "Spec compliant"
❌ "All Scenarios have tests" (without showing them)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Subagent delegation:**
```
✅ Subagent reports success → Check actual output → Verify changes → Report actual state
❌ Trust subagent report
```

## SuperSpec Integration

### Before Claiming Task Complete

```
1. Run tests: npm test (or project test command)
2. Show output: "X/Y tests pass"
3. Check Spec coverage: Does test exist for each Scenario?
4. Show evidence: "Test for Scenario X: [test name]"
5. THEN claim: "Task complete"
```

### Before Claiming TDD Followed

```
1. Show: Failing test output (RED phase)
2. Show: Passing test output (GREEN phase)
3. Verify: Failure came BEFORE implementation
4. THEN claim: "TDD followed"
```

### Before Claiming Phase Complete

```
1. List all tasks in phase
2. For each task: show completion evidence
3. Run full test suite
4. Show output
5. THEN claim: "Phase complete"
```

## Why This Matters

**Trust is earned through evidence:**
- Unverified claims break trust
- "I don't believe you" = trust broken
- Undefined functions shipped = would crash
- Missing requirements shipped = incomplete features
- Time wasted on false completion → redirect → rework

**Verification is faster than rework:**
- 30 seconds to verify
- Hours to debug shipped bugs
- Days to rebuild trust

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Reporting to user

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## Integration

**Called by:**
- `superspec:execute` - Before marking task complete
- `superspec:finish-branch` - Before presenting options
- `superspec:verify` - Core verification skill

**Pairs with:**
- `tdd` - TDD evidence verification
- All skills that claim completion

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
