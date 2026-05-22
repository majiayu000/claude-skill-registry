---
name: verification-before-completion
description: This skill should be used when about to claim work is complete, fixed, or passing. It requires running verification commands and confirming output before making any success claims. Evidence before assertions, always.
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Type:** RIGID - Follow exactly. Do not adapt away from this discipline.

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
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags - STOP

If you catch yourself:

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence does not equal evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter does not equal compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion is not an excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
Correct: [Run test command] [See: 34/34 pass] "All tests pass"
Wrong:   "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
Correct: Write -> Run (pass) -> Revert fix -> Run (MUST FAIL) -> Restore -> Run (pass)
Wrong:   "I've written a regression test" (without red-green verification)
```

**Build:**
```
Correct: [Run build] [See: exit 0] "Build passes"
Wrong:   "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
Correct: Re-read plan -> Create checklist -> Verify each -> Report gaps or completion
Wrong:   "Tests pass, phase complete"
```

**Agent delegation:**
```
Correct: Agent reports success -> Check VCS diff -> Verify changes -> Report actual state
Wrong:   Trust agent report
```

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## Integration with Other Skills

This skill pairs with:
- **systematic-debugging** - Verify fix worked before claiming bug resolved
- **brainstorming** - Verify design meets requirements before implementation

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
