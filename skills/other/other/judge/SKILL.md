---
name: judge
description: Scoring framework for test-kitchen cookoff and omakase-off. Invoked at Phase 4 to evaluate implementations using 5-criteria scoring. Do not invoke directly - called by cookoff/omakase-off.
---

# Test Kitchen Judge

Score implementations using the 5-criteria framework. Fill out ALL sections exactly as shown.

**Terminology:** This skill uses "impl" but works for both:
- Cookoff: impl-1, impl-2, impl-3 (same design, different implementations)
- Omakase: variant-a, variant-b (different approaches/designs)

## REQUIRED OUTPUT FORMAT

You MUST produce this exact structure. Do not summarize or abbreviate.

```markdown
## Gate Check
| Impl | Tests Pass | Design Adherence |
|------|------------|------------------|
| impl-1 | X/X ✓ or ✗ | Yes/No |
| impl-2 | X/X ✓ or ✗ | Yes/No |

## Feasibility Check
| Impl | Status | Notes |
|------|--------|-------|
| impl-1 | ✓ OK / ⚠️ Flag | Details |
| impl-2 | ✓ OK / ⚠️ Flag | Details |

## Scoring Worksheet

### impl-1
**Fitness for Purpose** (Does it solve the actual problem?)

*Functional requirements:*
- [ ] Primary use case works end-to-end?
- [ ] All explicitly stated requirements implemented?
- [ ] Handles realistic scenarios, not just happy path?

*User needs (beyond literal requirements):*
- [ ] Would the user actually use this, or just demo it?
- [ ] Does it solve the real problem, not just the literal request?
- [ ] Does deployment/distribution match stated needs?

*Future considerations (if relevant):*
- [ ] If growth/scaling mentioned, does architecture support it?
- [ ] If team/collaboration mentioned, is it maintainable by others?

Checklist: _/8 YES → **Score: _/5** (7-8=5, 5-6=4, 4=3, 2-3=2, 0-1=1)
*Note: Not all items apply to every project. Score based on relevant items.*

**Justified Complexity** (Every line earning its keep?)
- Unnecessary abstractions: ___
- Dead code: ___
- Bloat estimate: ___%

*Line count comparison (if multiple impls):*
- This impl: ___ lines
- Smallest impl: ___ lines
- Extra lines justified by: ___

→ **Score: _/5** (5=minimal, 4=slight bloat <10%, 3=10-25% bloat, 2=25-50%, 1=>50%)

**Readability** (Understand core flow in 5 min?)
Violations:
- [ ] Single-letter vars (not loop index): +1 each = __
- [ ] Functions >50 lines: +1 each = __
- [ ] Nesting >3 levels: +1 each = __
- [ ] Magic numbers: +1 each = __
- [ ] Bad function names: +1 each = __
Total violations: __ → **Score: _/5** (0=5, 1-2=4, 3-4=3, 5-7=2, 8+=1)

**Robustness & Scale** (Handles unexpected + growth?)
- [ ] Input validation?
- [ ] External call error handling?
- [ ] Useful error messages?
- [ ] Null/empty handling?
- [ ] Async timeouts?
- [ ] No unbounded loops?
- [ ] O(n log n) or better?
- [ ] Bounded memory?
- [ ] Queries paginated?
- [ ] No blocking I/O in hot path?
- [ ] Backoff/retry logic?
- [ ] Handles 10x load?
Checklist: _/12 YES + feasibility flags → **Score: _/5**
(11-12 + no flags=5, 9-10 or minor flag=4, 7-8=3, 5-6 or major flag=2, <5 or critical flag=1)

**Maintainability** (Pain of next change?)
- [ ] Single responsibility per function?
- [ ] Explicit dependencies (no globals)?
- [ ] Business logic separated from infra?
- [ ] New feature = ≤3 files changed?
- [ ] Config externalized?
- [ ] Tests catch regressions?
Checklist: _/6 YES → **Score: _/5** (6=5, 5=4, 4=3, 2-3=2, 0-1=1)

### impl-2
[REPEAT SAME FORMAT]

### impl-3 (if applicable)
[REPEAT SAME FORMAT]

## Judge Scorecard
| Criterion | impl-1 | impl-2 | impl-3 | Best |
|-----------|--------|--------|--------|------|
| Fitness for Purpose | | | | |
| Justified Complexity | | | | |
| Readability | | | | |
| Robustness & Scale | | | | |
| Maintainability | | | | |
| **TOTAL** | /25 | /25 | /25 | |

## Hard Gates
| Gate | Result |
|------|--------|
| Fitness Gate (Δ ≥ 2) | Triggered/Not triggered |
| Critical Flaw (any = 1) | Triggered/Not triggered |

## Winner Selection
**Winner: impl-X** (Score: __/25)

**Selection rationale:**
[2-3 sentences explaining WHY this implementation won]

**Trade-offs acknowledged:**
[What the other implementations did better]
```

## Scoring Reference

### Scores Meaning
| Score | Meaning |
|-------|---------|
| 5 | Excellent - exceeds expectations |
| 4 | Good - fully meets requirements |
| 3 | Adequate - core works, some gaps |
| 2 | Poor - significant issues |
| 1 | Critical flaw - disqualifying |

### Hard Gates (Automatic)

1. **Fitness Gate:** If Fitness Δ ≥ 2 between impls → Higher fitness WINS immediately
2. **Critical Flaw:** If ANY criterion = 1 → That impl is ELIMINATED

#### Fitness Gate Interpretation

The Fitness Gate triggers the same way in both contexts, but means different things:

| Context | What Fitness Δ ≥ 2 Means |
|---------|--------------------------|
| **Cookoff** | One implementation *deviated from or misunderstood the design*. All impls should have similar Fitness since they're implementing the same spec. A large gap is a red flag. |
| **Omakase** | One approach *genuinely solves the problem better*. Different approaches can legitimately have different Fitness. A large gap means one approach is clearly superior. |

In both cases, higher Fitness wins. The interpretation just explains *why* the gap exists.

### Feasibility Red Flags

Check before scoring:
- O(n²) or worse on unbounded data
- Unbounded memory growth
- Self-DDoS patterns (polling, no backoff)
- Missing pagination
- Blocking I/O in hot path
- No error recovery

## Process

1. **Read** all implementation code (should already be in context)
2. **Fill out** the worksheet for EACH implementation - do not skip sections
3. **Check** hard gates
4. **Announce** winner with rationale

**CRITICAL:** Use integer scores only (1-5). Do not use half points like 4.5.

**CRITICAL:** Fill out every checkbox. Do not summarize or abbreviate the worksheet.
