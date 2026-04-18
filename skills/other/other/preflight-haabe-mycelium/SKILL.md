---
name: preflight
description: "Use before starting delivery work. Pre-implementation validation checklist to ensure readiness."
---

# Preflight Skill

Pre-delivery validation checklist. Run before every implementation task.

## Checklist

### Context
- [ ] corrections.md reviewed for relevant past mistakes
- [ ] patterns.md reviewed for applicable patterns
- [ ] Current diamond phase is Develop or Deliver
- [ ] Acceptance criteria are clear and measurable
- [ ] Scenarios linked: `canvas/scenarios.yml` has scenarios for this solution, and acceptance criteria trace back to scenario success/failure states (Hoskins)

### Scope
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
