---
name: review-outside-box-open
description: Open zoom out and find whole classes of performance, bug, or anti-pattern issues hiding in plain sight
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Think outside the box. Use maximum parallelism and processing — don't worry about tokens.

## What This Is

We've done performance checks before and managed to overlook huge issues like our massive misuse of regex vs json parsing, which in retrospect are obvious. i
think its because weve been looking at functions and smaller level stuff. Can you think outside the box, zoom out, or back to fundamentals, to think is there
anything else like that we could be overlooking that is a whole class of performance improvements / bug surfaces / anti patterns? This is a big ask. Don't worry
about tokens, use maximum processing time / tool use that you want.


## Validation

After explore agents report back, **validate every finding yourself**. Systemic findings need extra scrutiny because they often suggest large refactors — make sure the payoff justifies the cost.

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" — quote the actual pattern across multiple files to show it's systemic, not isolated.
2. **Quantify the impact**: How many files/functions exhibit this pattern? What's the estimated cost (CPU time, memory, latency, code complexity)?
3. **Counter-argument**: "What would make this change counterproductive?" — Would the fix add complexity that outweighs the gain? Is the current approach "good enough" given actual usage patterns? Would the migration risk outweigh the benefit?
4. **Observed vs inferred**: Did you measure or count the pattern directly, or infer it from a few examples?
5. **Scope the fix**: Is this a "change 3 lines in 20 files" fix or a "redesign the subsystem" fix? Both can be valuable, but the plan should be honest about scope.

## Plan Format

Group by class of issue, not by file:

### Issue Class: [descriptive name]

**Pattern**: What's happening systemically (1–2 sentences)

**Evidence**: Files and line ranges showing the pattern across the codebase

**Impact**: Estimated performance/reliability/maintainability cost

**Fix approach**: High-level — not line-by-line, but "change X to Y across the codebase"

**Scope**: How many files, estimated effort

**Counter-argument**: Why this might not be worth doing

---

Order by estimated impact (largest systemic wins first). A single architectural insight that affects 20 files is more valuable than 10 isolated micro-optimizations.

Ignore any existing plans — create a fresh one.
