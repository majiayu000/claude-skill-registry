---
name: rule-of-5-universal
description: Apply Steve Yegge's Rule of 5 iterative review to any artifact - code, plans, research, issues, specs, or documents. Five stages from draft through excellence.
---

# Universal Rule of 5 Review

Review this [CODE/PLAN/RESEARCH/ISSUE/SPEC/DOCUMENT] using Steve Yegge's Rule of 5 - five stages of iterative editorial refinement until convergence.

## Work to Review

[PASTE YOUR WORK OR SPECIFY FILE PATH]

## Core Philosophy

"Breadth-first exploration, then editorial passes"

Don't aim for perfection in early stages. Each stage builds on insights from previous stages.

## Stage 1: DRAFT - Get the shape right

**Question:** Is the overall approach sound?

**Focus on:**
- Overall structure and organization
- Major architectural or conceptual issues
- Is this solving the right problem?
- Are the main components/sections present?
- Is the scope appropriate?
- Don't sweat the details yet - focus on the big picture

**For Code:** Architecture, design patterns, major functions/classes
**For Plans:** Phase structure, dependencies, overall approach
**For Research:** Sections, flow, research questions coverage
**For Issues:** Title appropriateness, basic description presence
**For Specs:** Requirements structure, completeness at high level

**Output:**
```
STAGE 1: DRAFT

Assessment: [1-2 sentences on overall shape]

Major Issues:
[DRAFT-001] [CRITICAL|HIGH|MEDIUM|LOW] - [Location]
Description: [What's wrong structurally]
Recommendation: [How to fix]

[DRAFT-002] ...

Shape Quality: [EXCELLENT|GOOD|FAIR|POOR]
```

---

## Stage 2: CORRECTNESS - Is the logic sound?

**Question:** Are there errors, bugs, or logical flaws?

**Focus on:**
- Building on Stage 1 assessment
- Factual accuracy and logical consistency
- Errors, bugs, or incorrect assumptions
- Internal contradictions
- Misinterpretation or misunderstanding
- Does it actually work/make sense?

**For Code:** Syntax errors, logic bugs, algorithm correctness, data structure usage
**For Plans:** Feasibility issues, impossible dependencies, resource misestimates
**For Research:** Factual errors, incorrect citations, wrong conclusions from data
**For Issues:** Impossible scope, contradictory requirements, technical impossibilities
**For Specs:** Contradictory requirements, infeasible features, wrong assumptions

**Output:**
```
STAGE 2: CORRECTNESS

Issues Found:
[CORR-001] [CRITICAL|HIGH|MEDIUM|LOW] - [Location]
Description: [What's incorrect]
Evidence: [Why this is wrong]
Recommendation: [How to fix with specifics]

[CORR-002] ...

Correctness Quality: [EXCELLENT|GOOD|FAIR|POOR]
```

**Convergence Check (after Stage 2):**
```
New CRITICAL issues: [count]
Total new issues: [count]
Status: [CONVERGED | CONTINUE]
```

---

## Stage 3: CLARITY - Can someone else understand this?

**Question:** Is this comprehensible to the intended audience?

**Focus on:**
- Building on corrected work from Stage 2
- Readability and comprehensibility
- Unclear or ambiguous language
- Jargon without explanation
- Poor naming or labeling
- Missing context or explanation
- Flow and organization

**For Code:** Variable/function names, comments, code organization, complexity
**For Plans:** Phase descriptions, success criteria clarity, instruction specificity
**For Research:** Term definitions, logical flow, transitions, accessibility
**For Issues:** Description clarity, actionability, context sufficiency
**For Specs:** Requirement clarity, unambiguous language, examples provided

**Output:**
```
STAGE 3: CLARITY

Issues Found:
[CLAR-001] [HIGH|MEDIUM|LOW] - [Location]
Description: [What's unclear]
Impact: [Why this matters]
Recommendation: [How to improve clarity]

[CLAR-002] ...

Clarity Quality: [EXCELLENT|GOOD|FAIR|POOR]
```

**Convergence Check (after Stage 3):**
```
New CRITICAL issues: [count]
Total new issues: [count]
New issues vs Stage 2: [percentage change]
Status: [CONVERGED | CONTINUE]
```

---

## Stage 4: EDGE CASES - What could go wrong?

**Question:** Are boundary conditions and unusual scenarios handled?

**Focus on:**
- Building on clarified work from Stage 3
- Edge cases and boundary conditions
- Error handling and failure modes
- Unusual inputs or scenarios
- Gaps in coverage
- "What if..." scenarios
- Assumptions that might not hold

**For Code:** Null checks, empty arrays, max values, error handling, race conditions
**For Plans:** Rollback strategies, blocked scenarios, resource unavailability, assumption failures
**For Research:** Alternative explanations, conflicting evidence, unanswered questions, limitations
**For Issues:** Acceptance criteria gaps, unclear done conditions, edge scenarios
**For Specs:** Corner cases, conflicting requirements, missing scenarios, error states

**Output:**
```
STAGE 4: EDGE CASES

Issues Found:
[EDGE-001] [CRITICAL|HIGH|MEDIUM|LOW] - [Location]
Description: [What edge case is unhandled]
Scenario: [When this could happen]
Impact: [What goes wrong]
Recommendation: [How to handle it]

[EDGE-002] ...

Edge Case Coverage: [EXCELLENT|GOOD|FAIR|POOR]
```

**Convergence Check (after Stage 4):**
```
New CRITICAL issues: [count]
Total new issues: [count]
New issues vs Stage 3: [percentage change]
Estimated false positive rate: [percentage]
Status: [CONVERGED | CONTINUE]
```

---

## Stage 5: EXCELLENCE - Ready to ship?

**Question:** Would you be proud to ship this?

**Focus on:**
- Final polish based on all previous stages
- Production quality assessment
- Best practices adherence
- Professional standards
- Performance and efficiency
- Completeness and thoroughness
- Overall quality for intended purpose

**For Code:** Performance, style, documentation, test coverage, maintainability
**For Plans:** Implementability, completeness, TDD approach, verification steps
**For Research:** Actionability, recommendations, references, presentation quality
**For Issues:** Executability, priority, labels, handoff readiness
**For Specs:** Testability, completeness, stakeholder readiness, sign-off criteria

**Output:**
```
STAGE 5: EXCELLENCE

Final Polish Issues:
[EXCL-001] [HIGH|MEDIUM|LOW] - [Location]
Description: [What could be better]
Recommendation: [How to achieve excellence]

[EXCL-002] ...

Excellence Assessment:
- Structure: [EXCELLENT|GOOD|FAIR|POOR]
- Correctness: [EXCELLENT|GOOD|FAIR|POOR]
- Clarity: [EXCELLENT|GOOD|FAIR|POOR]
- Edge Cases: [EXCELLENT|GOOD|FAIR|POOR]
- Overall: [EXCELLENT|GOOD|FAIR|POOR]

Production Ready: [YES|NO|WITH_NOTES]
```

**Convergence Check (after Stage 5):**
```
New CRITICAL issues: [count]
Total new issues: [count]
New issues vs Stage 4: [percentage change]
Estimated false positive rate: [percentage]
Status: [CONVERGED | NEEDS_ITERATION | ESCALATE_TO_HUMAN]
```

---

## Convergence Criteria

**CONVERGED** if:
- No new CRITICAL issues AND
- New issue rate < 10% vs previous stage AND
- False positive rate < 20%

**CONTINUE** if:
- New issues found that need addressing

**ESCALATE_TO_HUMAN** if:
- After 5 stages, still finding CRITICAL issues OR
- Uncertain about severity or correctness OR
- False positive rate > 30%

**If converged before Stage 5:** Stop and report. Don't continue unnecessarily.

---

## Final Report

After convergence or completing Stage 5:

```
# Rule of 5 Review - Final Report

**Work Reviewed:** [type] - [path/identifier]
**Convergence:** Stage [N]

## Summary

Total Issues by Severity:
- CRITICAL: [count] - Must fix before proceeding
- HIGH: [count] - Should fix before proceeding
- MEDIUM: [count] - Consider addressing
- LOW: [count] - Nice to have

## Top 3 Critical Findings

1. [ID] [Description] - [Location]
   Impact: [Why this matters]
   Fix: [What to do]

2. [ID] [Description] - [Location]
   Impact: [Why this matters]
   Fix: [What to do]

3. [ID] [Description] - [Location]
   Impact: [Why this matters]
   Fix: [What to do]

## Stage-by-Stage Quality

- Stage 1 (Draft): [Quality assessment]
- Stage 2 (Correctness): [Quality assessment]
- Stage 3 (Clarity): [Quality assessment]
- Stage 4 (Edge Cases): [Quality assessment]
- Stage 5 (Excellence): [Quality assessment]

## Recommended Actions

1. [Action 1 - specific and actionable]
2. [Action 2 - specific and actionable]
3. [Action 3 - specific and actionable]

## Verdict

[READY | NEEDS_REVISION | NEEDS_REWORK | NOT_READY]

**Rationale:** [1-2 sentences explaining the verdict]
```

---

## Rules for All Stages

1. **Build progressively** - Each stage builds on work from previous stages
2. **Be specific** - Reference exact locations (file:line, section, paragraph)
3. **Provide actionable fixes** - Don't just identify problems, suggest solutions
4. **Validate claims** - Don't flag potential issues, confirm they exist
5. **Prioritize correctly**:
   - CRITICAL: Blocks use/deployment, fundamentally broken
   - HIGH: Significantly impacts quality or usability
   - MEDIUM: Should be addressed but not blocking
   - LOW: Minor improvements
6. **Check convergence** - Stop when new issues drop below threshold
7. **Don't force 5 stages** - If converged earlier, report and stop
