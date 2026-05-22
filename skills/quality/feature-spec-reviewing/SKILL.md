---
name: feature-spec-reviewing
description: Reviews feature specifications for completeness, testability, and implementation readiness. Validates acceptance criteria, edge cases, and technical constraints. Use when reviewing feature specs before implementation or during sprint planning.
version: 1.0.0
---

# Feature Spec Reviewing

## Purpose

Systematically review feature specifications to ensure they are complete, testable, and ready for implementation. Catches gaps in edge cases and error handling before engineering work begins.

## When NOT to Use This Skill

- Creating feature specs (use `feature-spec-writing` instead)
- Reviewing PRDs (use `prd-reviewing` instead)
- Reviewing technical specs (use `technical-spec-reviewing` instead)
- Code review (different domain)
- No spec exists yet (nothing to review)

## Review Workflow

### Step 1: Document Analysis

Read the entire feature spec and assess structure:

```markdown
Initial Assessment:
- [ ] Feature definition is clear one-sentence
- [ ] Primary user story present
- [ ] Acceptance criteria exist
- [ ] Error states documented
- [ ] Definition of Done checklist exists
```

**Red Flags:**
- Feature definition is vague or multi-sentence
- Multiple unrelated user stories bundled
- Only happy path documented
- No error handling defined

### Step 2: Feature Definition Review

Evaluate the feature definition:

```markdown
Feature Definition Checklist:
1. Is it a single sentence?
2. Does it follow [Verb] [what] for [whom] to [outcome]?
3. Is the scope clear and bounded?
4. Is it too broad (actually multiple features)?
5. Does it align with parent PRD (if applicable)?
```

**Severity Guide:**
| Issue | Severity |
|-------|----------|
| No feature definition | BLOCKER |
| Multi-feature bundling | BLOCKER |
| Vague definition | CRITICAL |
| Misaligned with PRD | MAJOR |
| Minor clarity issues | MINOR |

### Step 3: User Story Quality

Evaluate user story against standard format:

```markdown
User Story Checklist:
- [ ] Follows "As a... I want... So that..." format
- [ ] User type is specific (not just "user")
- [ ] Goal is concrete and achievable
- [ ] Benefit explains real value
- [ ] Story is right-sized (not an epic)
- [ ] Variants cover key user paths (if applicable)
```

**Common Issues:**
| Issue | Example | Severity |
|-------|---------|----------|
| Missing format | "Add quick view feature" | CRITICAL |
| Generic user | "As a user" instead of "As a shopper" | MAJOR |
| No benefit | Missing "so that" clause | MAJOR |
| Epic-sized | Entire workflow in one story | CRITICAL |

### Step 4: Acceptance Criteria Review

Evaluate acceptance criteria for completeness and testability:

```markdown
Criteria Coverage Checklist:
- [ ] Happy path (primary success scenario)
- [ ] Input validation (valid and invalid)
- [ ] Edge cases (boundaries, empty, max)
- [ ] Error handling (network, server, timeout)
- [ ] Performance expectations
- [ ] Security requirements (if applicable)
- [ ] Accessibility (if UI feature)
```

**Testability Test:**
For each criterion, ask: "Can QA write a test case from this?"

```markdown
❌ Untestable: "Quick view should be fast"
✅ Testable: "Quick view modal appears within 300ms of hover"

❌ Untestable: "Handle errors gracefully"
✅ Testable: "On network failure, show 'Connection lost' and retry button"

❌ Untestable: "Work on mobile"
✅ Testable: "On screens < 768px, bottom sheet replaces modal"
```

### Step 5: Edge Case Coverage

Verify edge cases are comprehensive:

```markdown
Edge Case Categories:
□ Empty state (no data, first use)
□ Minimum values (0, 1, empty string)
□ Maximum values (limits, overflow)
□ Null/undefined handling
□ Concurrent access (race conditions)
□ Timeout scenarios
□ Partial failure (some items succeed, some fail)
□ Network conditions (slow, offline, reconnect)
```

**Coverage Scoring:**
| Coverage | Rating | Action |
|----------|--------|--------|
| 7-8 categories | Strong | Approve |
| 5-6 categories | Adequate | Minor improvements |
| 3-4 categories | Weak | Critical - add cases |
| < 3 categories | Missing | Blocker - major gaps |

### Step 6: Error States Review

Evaluate error states matrix:

```markdown
Error States Checklist:
- [ ] All API calls have failure handling
- [ ] User-facing messages are helpful
- [ ] System actions are appropriate
- [ ] Recovery paths are clear
- [ ] Logging/alerting defined
```

**Error Categories to Verify:**
| Category | Example Errors |
|----------|---------------|
| Input | Invalid format, missing required, too long |
| Network | Offline, timeout, partial response |
| Server | 500, 503, rate limit |
| Business Logic | Conflict, not found, unauthorized |
| External | Third-party API down, invalid response |

### Step 7: Technical Feasibility

Assess implementation readiness:

```markdown
Feasibility Assessment:
- [ ] Dependencies identified and available
- [ ] Non-functional requirements realistic
- [ ] Data requirements clear
- [ ] No obvious technical blockers
- [ ] Performance targets achievable
```

### Step 8: Parent PRD Alignment

If feature has parent PRD:

```markdown
Alignment Check:
- [ ] Feature implements specific PRD user story
- [ ] Acceptance criteria align with PRD scope
- [ ] Out-of-scope items match PRD exclusions
- [ ] Success metrics support PRD goals
```

### Step 9: Generate Review Report

Compile findings using the template below.

## Severity Levels

| Level | Definition | Action |
|-------|------------|--------|
| **BLOCKER** | Cannot implement | Must fix before approval |
| **CRITICAL** | Will cause major issues | Should fix before sprint |
| **MAJOR** | Will cause rework | Should fix soon |
| **MINOR** | Nice to have | Can address during implementation |

### Severity Examples

**BLOCKER:**
- No feature definition or user story
- Multiple features bundled as one
- No acceptance criteria
- Missing critical error handling

**CRITICAL:**
- Acceptance criteria not testable
- Missing edge case categories
- No performance requirements
- Conflicting requirements

**MAJOR:**
- Vague user story benefit
- Incomplete error states matrix
- Missing accessibility considerations
- Technical dependencies unclear

**MINOR:**
- Minor clarity improvements
- Additional edge cases nice to have
- Formatting inconsistencies
- Could add more detail

## Review Report Template

```markdown
# Feature Spec Review: [Feature Name]

**Reviewer:** [Name]
**Review Date:** [Date]
**Spec Version:** [Version]
**Spec Author:** [Name]

---

## Summary

**Status:** [APPROVE / APPROVE WITH CHANGES / NEEDS REVISION / MAJOR REVISION]

**Implementation Readiness:** [Ready / Ready After Fixes / Not Ready]

**Assessment:**
[2-3 sentences on overall quality and readiness]

---

## Findings by Severity

### Blockers
- [ ] [Finding with location and recommendation]

### Critical
- [ ] [Finding with location and recommendation]

### Major
- [ ] [Finding with location and recommendation]

### Minor
- [ ] [Finding with location and recommendation]

---

## Section Ratings

| Section | Rating | Notes |
|---------|--------|-------|
| Feature Definition | [Strong/Adequate/Weak/Missing] | |
| User Story | [Strong/Adequate/Weak/Missing] | |
| Acceptance Criteria | [Strong/Adequate/Weak/Missing] | |
| Edge Cases | [Strong/Adequate/Weak/Missing] | |
| Error States | [Strong/Adequate/Weak/Missing] | |
| Technical Constraints | [Strong/Adequate/Weak/Missing] | |

---

## Edge Case Coverage

□ Empty state - [Covered/Missing]
□ Minimum values - [Covered/Missing]
□ Maximum values - [Covered/Missing]
□ Null handling - [Covered/Missing]
□ Concurrent access - [Covered/Missing]
□ Timeout scenarios - [Covered/Missing]
□ Partial failure - [Covered/Missing]
□ Network conditions - [Covered/Missing]

**Coverage Score:** [X/8]

---

## Testability Assessment

**Can QA write tests?** [Yes / Partially / No]

**Problematic Criteria:**
- [Criterion that's not testable and why]

---

## Strengths
- [What the spec does well]
- [What the spec does well]

## Risks
1. [Risk and suggested mitigation]
2. [Risk and suggested mitigation]

---

## Questions for Author
1. [Clarifying question]
2. [Clarifying question]

---

## Recommendation

[Detailed recommendation with specific next steps]
```

## Examples

### Example 1: Strong Spec (Minor Feedback)

**Status:** APPROVE WITH CHANGES

**Assessment:**
Well-structured feature spec with clear definition and comprehensive acceptance criteria. Minor gaps in timeout handling edge cases.

**Findings:**
- MINOR: AC for network timeout missing retry limit
- MINOR: Consider adding concurrent edit scenario

**Edge Case Coverage:** 7/8 (Missing: Partial failure)

---

### Example 2: Needs Work (Critical Gaps)

**Status:** NEEDS REVISION

**Assessment:**
Good user story but acceptance criteria lack edge case coverage. Error states incomplete. Should add missing scenarios before sprint planning.

**Findings:**
- CRITICAL: Only happy path acceptance criteria defined
- CRITICAL: Error states matrix incomplete (missing network, timeout)
- MAJOR: Performance requirements not specified
- MAJOR: Mobile responsive behavior undefined

**Edge Case Coverage:** 2/8

---

### Example 3: Major Problems

**Status:** MAJOR REVISION REQUIRED

**Assessment:**
Feature definition describes multiple features bundled together. Recommend splitting into separate specs.

**Findings:**
- BLOCKER: "User authentication" bundles login, signup, password reset, MFA
- BLOCKER: No acceptance criteria for individual flows
- CRITICAL: User story is epic-sized
- MAJOR: No error handling defined

**Recommendation:** Split into 4 separate feature specs.

## Integration with Other Skills

**Reviews Output From:**
- `feature-spec-writing` - Validate completed feature specs

**Leads To:**
- `technical-spec-writing` - After spec approved
- `sparc-planning` - After spec approved

## Resources

- See CHECKLIST.md for comprehensive review checklist


---

## Related Agent

For comprehensive specification guidance that coordinates this and other spec skills, use the **`specification-architect`** agent.
