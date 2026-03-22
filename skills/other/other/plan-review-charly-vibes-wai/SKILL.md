---
name: plan-review
description: Perform iterative implementation plan review using Rule of 5 methodology. Reviews feasibility, completeness, TDD alignment, ordering, and executability.
---

# Iterative Plan Review (Rule of 5)

Perform thorough implementation plan review using the Rule of 5 - iterative refinement until convergence.

## Setup

**If plan path provided:** Read the plan completely

**If no plan path:** Ask for the plan path or list available plans from `plans/`

## Process

Perform 5 passes, each focusing on different aspects. After each pass (starting with pass 2), check for convergence.

### PASS 1 - Feasibility & Risk

**Focus on:**
- Technical feasibility of proposed changes
- Identified risks and their mitigations
- Dependencies on external factors (APIs, services, libraries)
- Assumptions that need validation
- Potential blockers not addressed
- Resource requirements (time, expertise, infrastructure)

**Output format:**
```
PASS 1: Feasibility & Risk

Issues Found:

[FEAS-001] [CRITICAL|HIGH|MEDIUM|LOW] - Phase/Section
Description: [What's wrong]
Evidence: [Why this is a problem]
Recommendation: [How to fix with specific guidance]

[FEAS-002] ...
```

**What to look for:**
- "We'll just..." statements hiding complexity
- External dependencies assumed to be available
- Time estimates that seem unrealistic
- Required expertise not accounted for
- Breaking changes not acknowledged
- Rollback strategy missing or inadequate

### PASS 2 - Completeness & Scope

**Focus on:**
- Missing phases or steps
- Undefined or vague success criteria
- Gaps between current and desired state
- "Out of Scope" clearly defined
- All affected files/components identified
- Testing strategy covers all scenarios
- Edge cases considered

**Prefix:** COMP-001, COMP-002, etc.

**What to look for:**
- "And then..." without the "then" being in the plan
- Success criteria that can't be verified
- Missing integration points
- Unclear handoff points between phases
- Scope creep hiding in vague language

### PASS 3 - Spec & TDD Alignment

**Focus on:**
- Links to spec files (if applicable)
- Tests planned before implementation (TDD)
- Success criteria are testable
- Test-first approach clear in each phase
- All requirements from specs covered
- Verification steps defined

**Prefix:** TDD-001, TDD-002, etc.

**What to look for:**
- "We'll test it" without specific test descriptions
- Implementation before tests in phase sequence
- Untestable success criteria ("works well", "is fast")
- Missing test coverage for error cases
- No mention of what tests to write

### PASS 4 - Ordering & Dependencies

**Focus on:**
- Phases in correct order (can't do B before A)
- Dependencies between phases clearly stated
- Parallelizable work identified
- Critical path identified
- Each phase can be independently verified
- Rollback/reversal possible at phase boundaries

**Prefix:** ORD-001, ORD-002, etc.

**What to look for:**
- Phase 2 requires Phase 3 to be done first
- Circular dependencies between phases
- "Big bang" integration at the end
- No incremental verification
- All-or-nothing approach

### PASS 5 - Clarity & Executability

**Focus on:**
- Specific enough for someone else to implement
- File paths and changes are concrete
- No ambiguous instructions
- Clear what "done" means for each phase
- Technical terms defined or understood
- Handoff points between phases clear

**Prefix:** EXEC-001, EXEC-002, etc.

**What to look for:**
- "Update the authentication" - update how? where?
- "Make it work with..." - what does "work" mean?
- "Refactor as needed" - refactor what? when?
- File paths missing or vague
- Assumptions about shared knowledge

## Convergence Check

After each pass (starting with pass 2), report:

```
Convergence Check After Pass [N]:

1. New CRITICAL issues: [count]
2. Total new issues this pass: [count]
3. Total new issues previous pass: [count]
4. Estimated false positive rate: [percentage]

Status: [CONVERGED | ITERATE | NEEDS_HUMAN]
```

**Convergence criteria:**
- **CONVERGED**: No new CRITICAL, <10% new issues vs previous pass, <20% false positives
- **ITERATE**: Continue to next pass
- **NEEDS_HUMAN**: Found blocking issues requiring human judgment

**If CONVERGED before Pass 5:** Stop and report final findings.

## Final Report

After convergence or completing all passes:

```
## Plan Review Final Report

**Plan:** plans/[filename].md

### Summary

Total Issues by Severity:
- CRITICAL: [count] - Must fix before implementation
- HIGH: [count] - Should fix before implementation
- MEDIUM: [count] - Consider addressing
- LOW: [count] - Nice to have

Convergence: Pass [N]

### Top 3 Most Critical Findings

1. [FEAS-001] [Description] - Phase [N]
   Impact: [Why this matters]
   Fix: [What to do]

2. [COMP-003] [Description] - Phase [N]
   Impact: [Why this matters]
   Fix: [What to do]

3. [TDD-002] [Description] - Phase [N]
   Impact: [Why this matters]
   Fix: [What to do]

### Recommended Next Actions

1. [Action 1 - specific and actionable]
2. [Action 2 - specific and actionable]
3. [Action 3 - specific and actionable]

### Verdict

[READY_TO_IMPLEMENT | NEEDS_REVISION | NEEDS_MORE_RESEARCH]

**Rationale:** [1-2 sentences explaining the verdict]
```

## Rules

1. **Be specific** - Reference plan sections/phases, provide file:line if relevant
2. **Provide actionable fixes** - Don't just say "add more detail", say what detail
3. **Validate claims** - Don't flag potential issues, confirm they exist
4. **Prioritize correctly**:
   - CRITICAL: Blocks implementation or will cause failure
   - HIGH: Significantly impacts quality or feasibility
   - MEDIUM: Worth addressing but not blocking
   - LOW: Minor improvements
5. **If converged before pass 5** - Stop and report, don't continue needlessly
