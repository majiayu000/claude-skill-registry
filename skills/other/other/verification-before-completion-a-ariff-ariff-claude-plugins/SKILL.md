---
name: verification-before-completion
description: Never claim completion without fresh verification evidence
version: 1.0.0
author: Ariff
when_to_use: Before claiming ANYTHING is done, fixed, or passing
---

# Verification Before Completion

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the command in THIS message, you cannot claim it passes.

## The Gate

Before claiming ANY success:

```
1. IDENTIFY → What command proves this claim?
2. RUN → Execute the FULL command
3. READ → Full output, check exit code
4. VERIFY → Does output confirm the claim?
5. CLAIM → Only now, with evidence
```

Skip ANY step = lying, not verifying.

## What Requires Verification

| Claim | Requires | NOT Sufficient |
|-------|----------|----------------|
| "Tests pass" | Test output: 0 failures | "Should pass", previous run |
| "Build works" | Build output: exit 0 | Linter passing |
| "Bug fixed" | Test of original symptom | "Code changed" |
| "Linter clean" | Linter output: 0 errors | "Looks right" |
| "Feature complete" | All requirements checked | "Tests pass" |

## Red Flags - STOP

If you catch yourself:
- Using "should", "probably", "seems to"
- Saying "Great!", "Perfect!", "Done!" before running verification
- About to commit without fresh test run
- Thinking "just this once"
- Feeling tired and wanting to be done

**STOP. Run the verification.**

## Rationalization Prevention

| You Think | Reality |
|-----------|---------|
| "Should work now" | RUN IT |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ tests |
| "I'm tired" | Exhaustion ≠ excuse |

## Correct Patterns

**Tests:**
```
✅ [run test] → See "34/34 pass" → "All tests pass"
❌ "Tests should pass now"
```

**Build:**
```
✅ [run build] → See "exit 0" → "Build passes"
❌ "Build looks good"
```

**Requirements:**
```
✅ Re-read requirements → Check each → Report gaps
❌ "Tests pass so it's complete"
```

## Why This Matters

From actual failures:
- User said "I don't believe you" - trust broken
- Undefined functions shipped - would crash at runtime
- Missing requirements - incomplete features
- Time wasted on false completion → redirect → rework

## Bottom Line

**Run the command. Read the output. THEN claim the result.**

This is non-negotiable.
