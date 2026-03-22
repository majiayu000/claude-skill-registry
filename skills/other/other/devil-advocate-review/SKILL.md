---
name: vibe-devil-advocate-review
description: Challenges recommendations, designs, or synthesis by adversarial review across 5 dimensions. Use before shipping any significant recommendation or design document.
user-invocable: true
---

# vibe-devil-advocate-review

Before shipping a recommendation, challenge it. The goal is to find weaknesses BEFORE they become production incidents.

## When to Use This Skill

- Before sending a design document for approval
- Before shipping a recommendation that combines multiple inputs
- Before merging a large feature branch
- When you feel "too confident" about a solution
- User asks for a review or second opinion

## When NOT to Use This Skill

- Trivial changes (typo fixes, formatting)
- When the user explicitly says "just ship it"
- During brainstorming (don't kill ideas before they form)
- For code review of small PRs (use `vibe-quality-loop` instead)

## The 5 Dimensions

Challenge the work across:

1. **Consistency** — Do all parts agree with each other? Are there contradictions?
2. **Completeness** — What's missing? What edge cases are unaddressed? What blind spots exist?
3. **Actionability** — Is every recommendation concrete and measurable? Can someone actually do this?
4. **Alignment** — Does this match the stated goals, constraints, and user needs?
5. **Risk** — What could go wrong? What are the second-order effects? What's the blast radius of failure?

## Steps

1. **Read the artifact** thoroughly — don't skim
2. **For each dimension**, actively try to find problems. Assume there ARE problems.
3. **Score each dimension** 1-5 (1=critical issues, 5=solid)
4. **List specific issues** with evidence
5. **Deliver verdict**: APPROVE / REVISE (with required changes) / REJECT (with blocking issues)

## Output Format

### Devil's Advocate Review

| Dimension | Score | Issues Found |
|-----------|-------|-------------|
| Consistency | X/5 | [count] |
| Completeness | X/5 | [count] |
| Actionability | X/5 | [count] |
| Alignment | X/5 | [count] |
| Risk | X/5 | [count] |

### Critical Issues
1. [Issue with evidence]

### Warnings
1. [Non-blocking concern]

### Verdict: APPROVE / REVISE / REJECT
[Rationale]
