---
name: prd-reviewing
description: Reviews and validates Product Requirements Documents for completeness, clarity, and feasibility. Identifies gaps, ambiguities, and risks using systematic checklist. Use when reviewing PRDs before approval, during stakeholder reviews, or validating requirements quality.
version: 1.0.0
---

# PRD Reviewing

## Purpose

Systematically review Product Requirements Documents to ensure they are complete, clear, actionable, and ready for implementation planning. Identifies issues before they become costly engineering problems.

## When NOT to Use This Skill

- Creating PRDs (use `prd-writing` instead)
- Reviewing technical implementation plans (use `sparc-planning` or `technical-spec-reviewing`)
- Code review (different domain entirely)
- No PRD exists yet (nothing to review)
- Reviewing feature specs (use `feature-spec-reviewing` instead)

## Review Workflow

### Step 1: Document Analysis

Read the entire PRD and assess structural completeness:

```markdown
Initial Assessment Checklist:

- [ ] Document has clear title and metadata
- [ ] Problem statement section exists
- [ ] User stories are present
- [ ] Acceptance criteria defined
- [ ] Scope section (in/out) exists
- [ ] Success metrics defined
- [ ] Stakeholders identified
```

**Red Flags:**

- Document is mostly implementation details
- No user-focused problem statement
- Missing "out of scope" section
- No measurable success criteria

### Step 2: Problem Validation

Evaluate the problem statement:

```markdown
Problem Validation Questions:

1. Is this a real user problem (not a solution in disguise)?
2. Who experiences this problem? (Specific personas)
3. Is the impact quantified or explained?
4. What's the evidence? (Research, data, feedback)
5. Is the problem scoped appropriately?
```

**Severity Guide:**
| Issue | Severity |
|-------|----------|
| No problem statement | BLOCKER |
| Solution masquerading as problem | BLOCKER |
| Problem exists but unquantified | MAJOR |
| Vague target users | MAJOR |
| Missing evidence/research links | MINOR |

### Step 3: User Story Quality

Evaluate each user story against INVEST criteria:

```markdown
User Story Checklist:

- [ ] Follows "As a... I want... So that..." format
- [ ] User type is specific (not just "user")
- [ ] Goal is achievable and clear
- [ ] Benefit explains the "why"
- [ ] Story is independent (no hidden dependencies)
- [ ] Story is small enough for one sprint
- [ ] Story delivers user value
```

**Common Issues:**
| Issue | Example | Severity |
|-------|---------|----------|
| Missing format | "Add shipping calculator" | CRITICAL |
| Epic-sized story | "Complete checkout redesign" | CRITICAL |
| No clear benefit | "...so that it works better" | MAJOR |
| Vague user type | "As a user" (which user?) | MAJOR |
| Implementation detail | "As a dev, I want API..." | MAJOR |

### Step 4: Acceptance Criteria Review

Evaluate acceptance criteria for testability:

```markdown
Criteria Quality Checklist:

- [ ] Uses Given/When/Then or clear checklist format
- [ ] Covers happy path scenario
- [ ] Covers error/edge cases
- [ ] Contains specific, measurable values
- [ ] Can be verified by QA without ambiguity
- [ ] Includes performance expectations where relevant
```

**Testability Test:**

Ask: "Could I write an automated test from this criterion?"

```markdown
❌ Untestable: "Page should load quickly"
✅ Testable: "Page loads within 2 seconds (p95)"

❌ Untestable: "User has good experience"
✅ Testable: "User can complete flow in ≤ 3 clicks"

❌ Untestable: "Handles errors gracefully"
✅ Testable: "On API failure, shows message 'Unable to calculate shipping. Try again.'"
```

### Step 5: Scope Analysis

Evaluate scope boundaries:

```markdown
Scope Validation:

- [ ] In-scope items are clearly listed
- [ ] Out-of-scope items are explicitly stated
- [ ] Each exclusion has a reason
- [ ] Dependencies are identified with owners
- [ ] Assumptions are documented
- [ ] Open questions are listed with owners
```

**Scope Smell Test:**

- If in-scope list seems endless → Scope creep risk
- If out-of-scope is empty → Boundaries not thought through
- If dependencies have no status → Delivery risk
- If assumptions aren't validated → Risk of rework

### Step 6: Feasibility Assessment

Evaluate implementation feasibility:

```markdown
Feasibility Questions:

1. Are the technical dependencies realistic?
2. Is the timeline achievable given scope?
3. Are there obvious technical blockers?
4. Does engineering have the required skills?
5. Are third-party integrations planned for?
6. Are there regulatory/compliance concerns?
```

**Red Flags:**

- No engineering input on timeline
- Dependencies on unavailable APIs
- Compliance requirements not addressed
- Resource assumptions not validated

### Step 7: Metrics Validation

Evaluate success metrics:

```markdown
Metrics Checklist:

- [ ] Metrics are measurable (not subjective)
- [ ] Current baseline is provided
- [ ] Target is specific and timebound
- [ ] Measurement method is defined
- [ ] Metrics align with problem statement
- [ ] Guardrails protect existing metrics
```

**Metrics Smell Test:**
| Issue | Example | Severity |
|-------|---------|----------|
| Vanity metric | "Increase page views" | MAJOR |
| No baseline | "Target: 20%" (from what?) | MAJOR |
| Unmeasurable | "Users are happier" | CRITICAL |
| Misaligned | Problem: speed, Metric: engagement | MAJOR |
| No guardrails | Missing "don't break X" | MAJOR |

### Step 8: Risk Identification

Identify what could go wrong:

```markdown
Risk Categories to Consider:

1. Technical: Can we build it?
2. Timeline: Can we build it in time?
3. Resource: Do we have the people?
4. Dependency: What if X isn't ready?
5. Market: Will users actually want this?
6. Compliance: Are there legal/regulatory issues?
7. Operational: Can we support/maintain it?
```

### Step 9: Generate Review Report

Compile findings into structured report (see template below).

### Step 10: Implementation Plan Review (Optional)

If PRD includes an Implementation Plan section (added by `prd-implementation-planning` skill):

```markdown
Implementation Plan Validation:

- [ ] Skill Requirements table covers all technical domains
- [ ] Tasks map to user stories (US-1, US-2, etc.)
- [ ] Each task has assigned skill
- [ ] Dependencies form valid DAG (no cycles)
- [ ] Estimates are reasonable (no XL tasks - should be split)
- [ ] P0 tasks form minimal critical path
- [ ] Progress tracker initialized with all tasks
```

**Note:** This step is only applicable for PRDs that have gone through the `prd-implementation-planning` skill. Skip if no Implementation Plan section exists.

## Severity Levels

| Level        | Definition         | Action                           |
| ------------ | ------------------ | -------------------------------- |
| **BLOCKER**  | Cannot approve PRD | Must fix before any approval     |
| **CRITICAL** | Significant gaps   | Should fix before implementation |
| **MAJOR**    | Notable issues     | Should fix soon, can start work  |
| **MINOR**    | Small improvements | Nice to have, low priority       |

### Severity Examples

**BLOCKER:**

- No problem statement (or it's actually a solution)
- No user stories
- Contradictory requirements
- Missing critical stakeholder sign-off

**CRITICAL:**

- Ambiguous acceptance criteria
- Missing key user stories for core flow
- No success metrics
- Unrealistic timeline without rationale

**MAJOR:**

- Vague problem statement (exists but unclear)
- Missing edge case handling
- Incomplete out-of-scope section
- Dependencies without owners

**MINOR:**

- Formatting inconsistencies
- Could add more detail to some areas
- Missing mockups (when not blocking)
- Minor clarity improvements

## Review Report Template

```markdown
# PRD Review: [Document Name]

**Reviewer:** [Your Name]
**Review Date:** [Date]
**PRD Version:** [Version being reviewed]
**PRD Author:** [Author Name]

---

## Summary

**Status:** [APPROVE / APPROVE WITH CHANGES / NEEDS REVISION / MAJOR REVISION REQUIRED]

**Overall Assessment:**
[2-3 sentences summarizing PRD quality and readiness for next phase]

---

## Findings by Severity

### Blockers (Must Fix Before Approval)

- [ ] [Location] [Issue description] → [Recommendation]

### Critical (Should Fix Before Implementation)

- [ ] [Location] [Issue description] → [Recommendation]

### Major (Fix Soon)

- [ ] [Location] [Issue description] → [Recommendation]

### Minor (Nice to Have)

- [ ] [Location] [Issue description] → [Recommendation]

---

## Section Ratings

| Section             | Rating                         | Notes        |
| ------------------- | ------------------------------ | ------------ |
| Problem Statement   | [Strong/Adequate/Weak/Missing] | [Brief note] |
| User Stories        | [Strong/Adequate/Weak/Missing] | [Brief note] |
| Acceptance Criteria | [Strong/Adequate/Weak/Missing] | [Brief note] |
| Scope               | [Strong/Adequate/Weak/Missing] | [Brief note] |
| Success Metrics     | [Strong/Adequate/Weak/Missing] | [Brief note] |

---

## Strengths

- [What the PRD does well]
- [What the PRD does well]

## Risks Identified

1. [Risk description] - Mitigation: [Suggestion]
2. [Risk description] - Mitigation: [Suggestion]

---

## Questions for Author

1. [Clarifying question]
2. [Clarifying question]

---

## Recommendation

[Detailed recommendation with specific next steps for the PRD author]
```

## Examples

### Example 1: Strong PRD (Minor Feedback)

**Status:** APPROVE WITH CHANGES

**Assessment:**
Well-structured PRD with clear problem statement and comprehensive user stories. Minor gaps in edge case coverage for acceptance criteria. Ready for engineering review after addressing minor items.

**Findings:**

- MINOR: US-3 acceptance criteria could specify timeout behavior
- MINOR: Consider adding "forgot password" to explicit out-of-scope

**Strengths:**

- Clear, quantified problem statement
- User stories follow INVEST criteria
- Good scope boundaries

---

### Example 2: Needs Work (Critical Issues)

**Status:** NEEDS REVISION

**Assessment:**
PRD has good structure but several critical gaps that would cause implementation ambiguity. Recommend revision and re-review before approval.

**Findings:**

- BLOCKER: No acceptance criteria for any user stories
- CRITICAL: "Make search faster" is not testable - needs specific targets
- CRITICAL: No success metrics defined
- MAJOR: Target users not clearly identified
- MAJOR: Dependencies on infrastructure team not noted

**Recommendation:** Return to author for acceptance criteria definition and success metrics. Re-review after updates.

---

### Example 3: Major Problems (Fundamental Issues)

**Status:** MAJOR REVISION REQUIRED

**Assessment:**
Document describes a solution rather than a user problem. Recommending restart from problem discovery phase.

**Findings:**

- BLOCKER: "We need a new dashboard" is a solution, not a problem
- BLOCKER: No user stories - only implementation requirements
- CRITICAL: Success metrics are vanity metrics (page views)
- MAJOR: Scope is trying to do too much for one release

**Recommendation:** Conduct user research to identify actual problem. Start fresh with problem-first approach.

## Integration with Other Skills

**Works With:**

- `prd-writing` - Review output from PRD creation
- `check-history` - Gather context before reviewing

**Leads To:**

- `prd-implementation-planning` - Map PRD to skills and create task list
- `sparc-planning` - After PRD approved (for complex tasks)
- `feature-spec-writing` - Break approved PRD into features

## Resources

- See CHECKLIST.md for comprehensive review checklist
- See EXAMPLES.md for detailed review examples

---

## Related Agent

For comprehensive specification guidance that coordinates this and other spec skills, use the **`specification-architect`** agent.
