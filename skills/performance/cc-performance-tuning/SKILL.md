---
name: cc-performance-tuning
description: "Enforce measure-first discipline for code optimization using a 7-step gated decision tree and 40-item checklist. Use when code is too slow, has performance issues, timeouts, OOM errors, high CPU/memory, or doesn't scale. Triggers on: profiler hot spots, latency complaints, unresponsive UI, memory allocation slow, needs optimization. Produce violation/warning/pass table with evidence."
---

# Skill: cc-performance-tuning

## STOP - Measure First

- **Don't optimize based on intuition—profile first**
- **Correctness before speed** - Make it work, then make it fast
- **<4% of code causes >50% of runtime** - Find the hot spot before touching anything

---

## CRITICAL: Even In Emergencies

Production down? Losing money? User panicking? **Especially then:**
- Guessing wrong costs MORE time than 60-second profiling
- Multiple shotgun changes make rollback impossible
- Wrong "fix" can mask the real problem for days

**Minimum crisis protocol (non-negotiable):**
1. 60-second profiler check OR recent deployment/config check
2. ONE change at a time
3. Revert immediately if no improvement within 5 minutes

## Scope & Limitations

**This skill covers:** Single-threaded, single-process code tuning for general-purpose computing.

**NOT covered (need specialized guidance):**
- **Concurrency:** Lock contention often dominates; profile thread states, not just CPU
- **Distributed systems:** Network latency ~10,000x memory; optimize RPC/serialization first
- **Real-time systems:** Need worst-case latency, not average; caching adds variance
- **Embedded/constrained:** Memory/power budgets require different tradeoffs

## Quick Reference

| Threshold/Rule | Value | Source |
|----------------|-------|--------|
| Hot spot concentration | <4% causes >50% runtime | Knuth 1971 |
| Failed optimization rate | >50% produce negligible or negative results | p.607 |
| Compiler optimization gains | 40-59% improvement possible | p.596 |
| Interpreted vs compiled | PHP/Python >100x slower than C++ | Table 25-1 |
| I/O vs memory | ~1000x difference | p.591 |

**Key Principles:**
- Make it correct first, then make it fast
- Measure before AND after every optimization
- Profile to find hot spots; never guess
- Compiler optimization often beats manual tuning
- Code tuning is the LAST resort, not first

## Core Patterns

**PREREQUISITE:** Only apply these patterns AFTER profiling confirms the specific code is in the <4% hot path. Applying without measurement is a skill violation.

### Page Fault Loop Ordering
```java
// BEFORE: Causes page fault on every access [ANTI-PATTERN]
for (column = 0; column < MAX_COLUMNS; column++) {
    for (row = 0; row < MAX_ROWS; row++) {
        table[row][column] = BlankTableElement();
    }
}

// AFTER: Page fault only when switching rows (up to 1000x faster)
for (row = 0; row < MAX_ROWS; row++) {
    for (column = 0; column < MAX_COLUMNS; column++) {
        table[row][column] = BlankTableElement();
    }
}
```

### Sentinel Value in Search Loop
```java
// BEFORE: Compound test every iteration [ANTI-PATTERN]
found = false;
i = 0;
while (!found && i < count) {
    if (item[i] == target) found = true;
    i++;
}

// AFTER: Single test per iteration (23-65% faster)
// Place sentinel past end of search range
item[count] = target;  // sentinel
i = 0;
while (item[i] != target) {
    i++;
}
if (i < count) {
    // found at position i
}
```

### Loop Unswitching
```java
// BEFORE: Testing invariant condition every iteration [ANTI-PATTERN]
for (i = 0; i < count; i++) {
    if (type == TYPE_A) {
        processTypeA(item[i]);
    } else {
        processTypeB(item[i]);
    }
}

// AFTER: Test once outside loop (19-28% faster)
if (type == TYPE_A) {
    for (i = 0; i < count; i++) {
        processTypeA(item[i]);
    }
} else {
    for (i = 0; i < count; i++) {
        processTypeB(item[i]);
    }
}
```

### Strength Reduction in Expression
```java
// BEFORE: Expensive operation [ANTI-PATTERN]
if (Math.sqrt(x) < Math.sqrt(y)) {
    // ...
}

// AFTER: Algebraically equivalent, 90-99.9% faster
if (x < y) {  // when x,y >= 0
    // ...
}
```

## APPLIER: When to Optimize

**Decision Tree (STRICT ORDER - Do NOT skip steps):**

Each step is a gate. Skipping steps = wasted effort or masked problems.

```
1. Is the program correct and complete?
   NO  -> Make it correct first. STOP optimization.
   YES -> Continue

2. Have you measured to find the actual bottleneck?
   NO  -> Profile/measure first. Do NOT guess.
   YES -> Continue

3. Can requirements be relaxed?
   YES -> Relax requirements. Done.
   NO  -> Continue

4. Can design/architecture solve it?
   YES -> Fix design. Done.
   NO  -> Continue

5. Can algorithm/data structure solve it?
   YES -> Change algorithm. Done.
   NO  -> Continue

6. Can compiler flags help?
   YES -> Enable optimizations. Measure.
   NO  -> Continue

7. Is it in the <4% that causes >50% of runtime?
   NO  -> Do NOT optimize this code. Find actual hot spot.
   YES -> PROCEED with code tuning
```

#### Code Tuning Procedure (STRICT ORDER)
```
1. Save working version (cannot revert without backup)
2. Make ONE change (multiple changes = unmeasurable)
3. Measure improvement (same workload, before/after)
4. Keep if faster, revert if not (no "close enough")
5. Repeat
```

#### Technique Priority (by category)

**Logic:**
1. Stop testing when answer known (use break, short-circuit)
2. Order tests by frequency (most common first)
3. Substitute table lookups for complex logic
4. Use lazy evaluation

**Loops:**
1. Unswitch (move invariant tests outside)
2. Jam/fuse loops operating on same range
3. Put busiest loop on inside
4. Minimize work inside loops
5. Use sentinel values for search loops
6. Unroll ONLY if measured (can be -27% in Python!)

**Data:**
1. Use integers instead of floating-point when possible
2. Use fewest array dimensions
3. Cache frequently computed values
4. Precompute results where practical

**Expressions:**
1. Initialize at compile time
2. Exploit algebraic identities
3. Use strength reduction (multiplication -> addition)
4. Eliminate common subexpressions

## CHECKER: Review for Anti-Patterns

Checklist: **[checklists.md](./checklists.md)**
Output Format:
  | Item | Status | Evidence | Location |
  |------|--------|----------|----------|
  | Measured before tuning? | VIOLATION | No profiler/measurement found | N/A |
  | Loop unswitching opportunity | WARNING | Invariant `if (debug)` inside loop | app.py:142 |
Severity:
  - VIOLATION: Clear anti-pattern present
  - WARNING: Potential issue (needs measurement)
  - PASS: No obvious performance issues

## Rationalization Counters

| Excuse | Reality |
|--------|---------|
| "Fewer lines of code is faster" | No predictable relationship; unrolled loops often 60-74% faster [p.603] |
| "I know this operation is slow" | You must measure; rules change with every environment change |
| "I'll optimize as I go" | You'll spend 96% of time on code that doesn't matter [Pareto] |
| "Experience tells me where bottlenecks are" | No programmer has ever predicted bottlenecks without data [Newcomer] |
| "This clever trick will be faster" | Compilers optimize straightforward code better than tricky code [p.596] |
| "We need to rewrite in assembler now" | Usually <4% of code causes >50% of runtime; find it first [Knuth 1971] |
| "Fast code is as important as correct code" | Correct first, fast second. Always. |
| "I already optimized this; it will stay optimized" | Re-profile after any compiler/library/environment change |
| "This optimization always works" | Results vary wildly by language; Python -27% for loop unrolling [p.623] |
| "The theory says this should be faster" | Theory doesn't always hold; Visual Basic -94% on polynomial strength reduction [p.636] |
| "I don't need to profile small changes" | If not worth profiling, not worth degrading readability for [p.609] |
| **Crisis:** "We're losing $X/minute!" | Guessing wrong = paying that $X until you find real cause. 60-sec profile saves hours. |
| **Crisis:** "No time to profile!" | Wrong guess costs more time than profiling. Panic causes cascading errors. |
| **Sunk cost:** "I already spent 4 hours optimizing" | Time invested doesn't validate method. Revert all, apply with measurement. |
| **Sunk cost:** "It seems faster now" | "Seems faster" is not data. You may have made some faster, others slower. |
| **Success streak:** "I've been right 5 times" | Past success doesn't change physics. Calibration illusion: 5 wins don't predict win 6. |


---

## Chain

| After | Next |
|-------|------|
| Optimization complete | Verify design not degraded |
| Structure degraded | cc-refactoring-guidance |
