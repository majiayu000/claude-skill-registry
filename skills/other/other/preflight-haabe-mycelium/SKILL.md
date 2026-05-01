---
name: preflight
description: "Use before starting delivery work. Pre-implementation validation checklist to ensure readiness."
instruction_budget: 45
---

# Preflight Skill

Pre-delivery validation checklist. Run before every implementation task.

## Checklist

### Constraints (ALWAYS FIRST)

Before scoping any delivery work, establish constraints. Do not propose a plan before knowing the budget.

- [ ] **Time budget**: "How much time do you have for this?" (hours, days, sprint length)
- [ ] **Resource constraints**: Solo? Team? What skills are available?
- [ ] **Fidelity**: Demo/prototype vs. production? Who is the audience?
- [ ] **Dependencies**: Waiting on anything external?

If time budget < 8 hours, scope aggressively — one vertical slice, no polish. If the initial plan exceeds the time budget, cut scope before presenting it to the user.

*Source: Hoskins transcript (2026-04-25) — agent proposed 20-hour plan before learning user had 8 hours. Goldratt (Theory of Constraints — identify the constraint before optimizing). Corrections.md: "Over-scope before constraints."*

### Context
- [ ] corrections.md reviewed for relevant past mistakes
- [ ] patterns.md reviewed for applicable patterns
- [ ] Current diamond phase is Develop or Deliver
- [ ] Acceptance criteria are clear and measurable
- [ ] Scenarios linked: `canvas/scenarios.yml` has scenarios for this solution, and acceptance criteria trace back to scenario success/failure states (Hoskins)

### Scope
- [ ] Scope fits within the time budget declared above
- [ ] This is the smallest vertical slice that delivers value
- [ ] Scope is explicitly bounded (what is NOT included)
- [ ] No speculative features (YAGNI check)
- [ ] Dependencies identified and available

### Technical / Production Readiness
**Software/AI tool:**
- [ ] Tech stack detected and understood
- [ ] Build/test/lint commands confirmed working
- [ ] Development environment functional
- [ ] Existing code patterns reviewed

**Content:**
- [ ] Production tools ready (editor, recording, hosting)
- [ ] Style guide / editorial standards available
- [ ] Existing content patterns reviewed

**Service:**
- [ ] Delivery tools ready (templates, scheduling, communication)
- [ ] Existing service patterns reviewed

### Security (software, ai_tool, service with digital infra)
- [ ] Data classification understood for this feature
- [ ] Security requirements identified (auth, input validation, etc.)
- [ ] No secrets will be hardcoded
- [ ] Dependencies checked for known vulnerabilities

### Accessibility
**Software:**
- [ ] Accessibility requirements identified
- [ ] Semantic HTML approach planned
- [ ] Keyboard interaction model defined
- [ ] Color contrast requirements noted

**Content:**
- [ ] Captions/transcripts planned for audio/video
- [ ] Alt text planned for images
- [ ] Readable typography confirmed

### Validation Strategy
**Software:** Test approach defined (unit, integration, e2e), edge cases and error scenarios identified.
**Content:** Review process defined (SME, self-checklist, fact-check), learning objectives mapped.
**AI tool:** Eval test cases defined, red-team scenarios planned, bias testing approach chosen.
**Service:** Walkthrough planned, client feedback mechanism defined.

### Success Criteria (G-V11)
- [ ] Declare what will be true after this delivery increment (1-3 measurable statements)
- [ ] Declare how each criterion will be verified (test, manual check, metric)
- [ ] Record criteria in decision-log.md alongside the delivery decision

Example:
```
Success criteria:
1. "Users can complete onboarding in < 5 min" — verified by usability test
2. "API responds in < 200ms at p95" — verified by load test
3. "No new lint or type errors introduced" — verified by CI
```

### Definition of Done
- [ ] DoD criteria reviewed and understood
- [ ] All criteria are achievable within this task

## If Any Item Fails

Do not proceed to implementation. Instead:
1. Document what is missing.
2. Determine the fastest path to readiness.
3. Address the gap before starting delivery work.

## Theory Citations
- Smart: BVSSH (Sooner -- avoid rework by preparing)
- Forsgren: Accelerate (reduce lead time by removing blockers early)
