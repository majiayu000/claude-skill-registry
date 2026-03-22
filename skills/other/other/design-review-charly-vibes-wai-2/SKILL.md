---
name: design-review
description: Review problem statements and decision matrices
disable-model-invocation: true
---

# Design Artifact Review

Review design artifacts for rigor, completeness, and adherence to Design in Practice principles.

## Setup

**If artifact path provided:** Read the artifact completely
**If no path:** Ask which artifact to review, or list available design documents

## Review Framework

Perform targeted review based on artifact type. Each review checks for common failure modes that lead to poor solutions.

---

## ARTIFACT TYPE: Problem Statement

### Check 1: Solution Contamination

**Question:** Does the problem statement contain or imply solutions?

**Red flags:**
- "We need to..." (solution language)
- Technology names (Redis, Kafka, etc.) unless they ARE the problem
- "Add", "implement", "create", "build" verbs
- Comparison to how other systems work

**Test:** Could multiple fundamentally different solutions address this statement?
- YES → Good problem statement (solution-agnostic)
- NO → Solution is embedded, rewrite needed

**Output:**
```
Solution Contamination: [CLEAN | CONTAMINATED]

Evidence:
- [Quote from statement showing contamination, or "None found"]

Recommendation:
- [How to remove solution language]
```

### Check 2: Root Cause vs. Symptom

**Question:** Does this describe the mechanism, or just the observable effect?

**Symptom language:**
- "Users experience..."
- "The system is slow/broken/failing..."
- "Errors occur when..."

**Mechanism language:**
- "Because X happens, Y results in Z"
- "The [component] does [action] which causes [effect]"
- Clear causal chain

**Test:** Ask "Why?" - if there's a deeper answer, this is a symptom.

**Output:**
```
Root Cause Analysis: [MECHANISM | SYMPTOM | UNCLEAR]

Depth check:
- Statement says: [quote]
- Ask "Why?": [deeper cause if exists]
- Assessment: [Is this the root or just a layer?]

Recommendation:
- [How to dig deeper, or "Root cause identified"]
```

### Check 3: Specificity

**Question:** Is the problem precise enough to guide solution selection?

**Vague indicators:**
- "Performance issues" (which metric? what threshold?)
- "Users are confused" (which users? confused about what?)
- "The code is messy" (what aspect? what's the impact?)

**Specific indicators:**
- Quantified thresholds ("response time > 2s")
- Named components ("SessionManager.close()")
- Reproducible conditions ("when concurrent users > 50")

**Output:**
```
Specificity: [PRECISE | VAGUE | MIXED]

Vague elements:
- [Element 1]: [How to make specific]
- [Element 2]: [How to make specific]

Missing specifics:
- [What metric/threshold/condition is unclear]
```

### Check 4: Evidence Quality

**Question:** Is the diagnosis based on verified facts or assumptions?

**Look for:**
- Evidence cited for each claim
- Ruled-out alternatives documented
- Hypothesis testing described
- Data sources referenced

**Output:**
```
Evidence Quality: [VERIFIED | ASSUMED | MIXED]

Claims without evidence:
- [Claim 1]: [What evidence is needed]
- [Claim 2]: [What evidence is needed]

Ruled-out alternatives:
- [Listed? How many? Are they reasonable alternatives?]
```

### Check 5: The Obvious Solution Test

**Question:** Does the solution feel obvious after reading this statement?

If the reader finishes the problem statement and doesn't immediately think "oh, we should do X", the diagnosis is incomplete.

**Output:**
```
Obvious Solution Test: [PASS | FAIL | PARTIAL]

After reading, the obvious action is: [What seems like the right solution]

If FAIL:
- What's unclear: [What question remains]
- What's missing: [What would make it obvious]
```

### Problem Statement Verdict

```
## Problem Statement Review Summary

| Check | Result | Action Needed |
|-------|--------|---------------|
| Solution Contamination | [CLEAN/CONTAMINATED] | [Action or "None"] |
| Root Cause | [MECHANISM/SYMPTOM] | [Action or "None"] |
| Specificity | [PRECISE/VAGUE] | [Action or "None"] |
| Evidence | [VERIFIED/ASSUMED] | [Action or "None"] |
| Obvious Solution | [PASS/FAIL] | [Action or "None"] |

**Verdict:** [READY_FOR_DIRECTION | NEEDS_REVISION | BACK_TO_DESCRIBE]

**Top Issue:** [Most critical thing to fix]

**Recommended Action:** [Specific next step]
```

---

## ARTIFACT TYPE: Decision Matrix

### Check 1: Status Quo Baseline

**Question:** Is "do nothing" the first column?

The Status Quo:
- Provides baseline for comparison
- Forces articulation of current state costs
- Prevents "solution in search of problem"

**Output:**
```
Status Quo Baseline: [PRESENT | MISSING]

If missing:
- Impact: Cannot compare alternatives to current state
- Fix: Add Status Quo column with honest assessment
```

### Check 2: Fact vs. Judgment Separation

**Question:** Is cell text factual and neutral, with judgment shown separately?

**Contaminated cells:**
- "Good performance" (judgment as text)
- "Easy to implement" (subjective)
- "Better than X" (comparative judgment)

**Clean cells:**
- "< 10ms p99 latency" (measurable fact)
- "Requires changes to 3 files" (countable)
- "Uses existing auth pattern" (verifiable)

**Output:**
```
Fact/Judgment Separation: [CLEAN | CONTAMINATED]

Contaminated cells:
| Row | Column | Current Text | Factual Rewrite |
|-----|--------|--------------|-----------------|
| [Row] | [Col] | "[Text]" | "[Suggestion]" |

Assessment indicators:
- Are judgments (good/bad) shown via color/symbol, not text? [YES/NO]
```

### Check 3: Criteria Completeness

**Question:** Are all relevant trade-off dimensions represented?

**Common missing criteria:**
- Maintenance burden (long-term cost)
- Rollback difficulty (reversibility)
- Team expertise (can we actually do this?)
- Integration complexity (how it affects other systems)
- Failure modes (what happens when it breaks?)

**Output:**
```
Criteria Completeness: [COMPLETE | GAPS]

Present criteria: [List]

Potentially missing:
- [Criterion]: [Why it matters for this decision]
- [Criterion]: [Why it matters for this decision]

Recommendation:
- [Which criteria to add]
```

### Check 4: Approach Diversity

**Question:** Are the approaches fundamentally different, or variations of the same idea?

**Insufficient diversity:**
- "Option A: Use Redis" / "Option B: Use Memcached" (same category)
- All options involve adding something (no "remove feature" option)
- All options are technical (no process/product options)

**Good diversity:**
- Different architectural approaches
- Build vs. Buy vs. Remove
- Technical vs. Process vs. Product solutions

**Output:**
```
Approach Diversity: [DIVERSE | SIMILAR]

Approaches listed:
- [Approach 1]: [Category]
- [Approach 2]: [Category]
- [Approach 3]: [Category]

Missing perspectives:
- [What category of solution wasn't considered]
```

### Check 5: Cell Verification

**Question:** Are the facts in the matrix verifiable and accurate?

Spot-check 2-3 claims:
- Can this be verified in the codebase?
- Is this number accurate?
- Is this comparison fair?

**Output:**
```
Cell Verification: [VERIFIED | UNVERIFIED | ERRORS]

Spot checks:
- [Cell Row/Col]: [Claim] → [Verification result]
- [Cell Row/Col]: [Claim] → [Verification result]

Errors found:
- [Cell]: [What's wrong and what's correct]
```

### Decision Matrix Verdict

```
## Decision Matrix Review Summary

| Check | Result | Action Needed |
|-------|--------|---------------|
| Status Quo Baseline | [PRESENT/MISSING] | [Action or "None"] |
| Fact/Judgment Separation | [CLEAN/CONTAMINATED] | [Action or "None"] |
| Criteria Completeness | [COMPLETE/GAPS] | [Action or "None"] |
| Approach Diversity | [DIVERSE/SIMILAR] | [Action or "None"] |
| Cell Verification | [VERIFIED/ERRORS] | [Action or "None"] |

**Verdict:** [READY_FOR_DECISION | NEEDS_REVISION | NEEDS_MORE_OPTIONS]

**Selected approach justified?** [YES/NO - Is the rationale sound?]

**Top Issue:** [Most critical thing to fix]

**Recommended Action:** [Specific next step]
```

---

## ARTIFACT TYPE: Scope Document (Delimit Phase)

### Check 1: Explicit Non-Goals

**Question:** Are out-of-scope items explicitly listed?

Scope creep happens when boundaries are implicit. Explicit non-goals:
- Prevent "while we're in there" additions
- Set expectations with stakeholders
- Provide reference when scope questions arise

**Output:**
```
Non-Goals: [EXPLICIT | IMPLICIT | MISSING]

Listed non-goals: [count]

Likely scope creep vectors not addressed:
- [Related item that might get added]
- [Adjacent problem that might expand scope]
```

### Check 2: Constraint Realism

**Question:** Are the constraints achievable and honest?

Look for:
- Conflicting constraints ("fast AND cheap AND complete")
- Unstated constraints (timeline, budget, expertise)
- Over-optimistic assumptions

**Output:**
```
Constraints: [REALISTIC | OPTIMISTIC | CONFLICTING]

Constraint conflicts:
- [Constraint A] vs [Constraint B]: [Why they conflict]

Missing constraints:
- [What's unstated but will affect the work]
```

---

## COMBINED REVIEW (Full Design Package)

When reviewing Problem Statement + Decision Matrix + Plan together:

### Alignment Check

1. **Problem → Direction alignment:**
   - Does the selected approach actually address the diagnosed problem?
   - Or does it solve a different/adjacent problem?

2. **Scope → Plan alignment:**
   - Does the plan stay within stated scope?
   - Are non-goals respected in the implementation?

3. **Decision rationale → Plan execution:**
   - Does the plan leverage the reasons the approach was chosen?
   - Are accepted trade-offs reflected in implementation?

**Output:**
```
## Alignment Review

Problem → Direction: [ALIGNED | DRIFT]
- [Evidence of alignment or drift]

Scope → Plan: [ALIGNED | CREEP]
- [Evidence of scope adherence or creep]

Decision → Plan: [ALIGNED | INCONSISTENT]
- [Does plan execute on decision rationale?]
```

---

## Final Report Template

```
## Design Artifact Review Report

**Artifact(s) Reviewed:** [List]
**Date:** [YYYY-MM-DD]

### Summary

| Artifact | Verdict | Key Issues |
|----------|---------|------------|
| Problem Statement | [READY/REVISION/BACK] | [Top issue] |
| Decision Matrix | [READY/REVISION/MORE] | [Top issue] |
| Scope Document | [READY/REVISION] | [Top issue] |
| Alignment | [ALIGNED/DRIFT] | [Top issue] |

### Critical Findings

1. **[ARTIFACT-CHECK]** [Severity]
   - Issue: [What's wrong]
   - Impact: [Why it matters]
   - Fix: [Specific action]

2. **[ARTIFACT-CHECK]** [Severity]
   - Issue: [What's wrong]
   - Impact: [Why it matters]
   - Fix: [Specific action]

### Recommended Actions

1. [Most important action]
2. [Second action]
3. [Third action]

### Overall Verdict

[PROCEED_TO_IMPLEMENTATION | REVISE_ARTIFACTS | RETURN_TO_EARLIER_PHASE]

**Rationale:** [1-2 sentences]
```
