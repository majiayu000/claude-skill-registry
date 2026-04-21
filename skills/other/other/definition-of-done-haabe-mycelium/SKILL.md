---
name: definition-of-done
description: "Use to verify a feature/story meets all Definition of Done criteria before marking complete."
instruction_budget: 53
---

# Definition of Done Skill

DoD checklist enforcement.

## Checklist

### Functionality
- [ ] All acceptance criteria met and demonstrable
- [ ] Happy path works end-to-end
- [ ] Edge cases handled (empty, null, max, concurrent)
- [ ] Error states handled with user-friendly messages

### Code Quality
- [ ] Code reviewed (self-review minimum, peer review preferred)
- [ ] No linting errors or warnings
- [ ] No type errors
- [ ] Engineering principles followed (DRY, KISS, YAGNI, SoC, SOLID)
- [ ] No TODO/FIXME/HACK comments left without linked issue
- [ ] No commented-out code

### Testing
- [ ] Unit tests written and passing (target 70-80% coverage for new code)
- [ ] Integration tests written where applicable
- [ ] E2E tests for critical user journeys
- [ ] Edge case tests included
- [ ] No test pollution (tests independent, no shared mutable state)

### Security
- [ ] Input validation on all entry points
- [ ] Output encoding appropriate to context
- [ ] No hardcoded secrets
- [ ] Authentication/authorization verified
- [ ] Dependency scan clean (no high/critical vulnerabilities)
- [ ] OWASP Top 10:2025 addressed for this feature

### Accessibility
- [ ] Semantic HTML used correctly
- [ ] Keyboard navigation works
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 normal, 3:1 large)
- [ ] Screen reader announces content correctly
- [ ] Focus management correct for dynamic content
- [ ] Usability heuristics evaluated (Nielsen's 10 via /usability-check)

### Documentation
- [ ] API documentation updated (if API changed)
- [ ] Inline documentation for complex logic
- [ ] README updated if setup/usage changed

### Observability
- [ ] Structured logging for key operations
- [ ] Error tracking configured
- [ ] Metrics emitted for measurable behaviors
- [ ] Health check endpoint works (if service)

### Deployment
- [ ] Feature flag configured (if progressive rollout)
- [ ] Deployed to staging
- [ ] Smoke test passing in staging
- [ ] Rollback plan identified
- [ ] Monitoring/alerting configured

### Process
- [ ] corrections.md reviewed (no repeated mistakes)
- [ ] BVSSH check: this delivery makes things Better, more Valuable, Sooner, Safer, Happier
- [ ] delivery-journal.md updated

### MoSCoW Scope Compliance (DSDM)
- [ ] All **Must-have** items pass ALL REVIEW checks above
- [ ] All **Should-have** items pass ALL REVIEW checks above
- [ ] **Could-have** items pass NUDGE-only checks (acceptable to ship without full REVIEW compliance)
- [ ] **Won't-have** items documented for future reference (not silently dropped)

## Outcome
- **DONE**: All required items checked. Proceed.
- **NOT DONE**: List failing items. Address before marking complete.

## Theory Citations
- Forsgren: Accelerate (deployment practices)
- Smart: Sooner Safer Happier (BVSSH)
- Downe: Good Services (quality)
- OWASP: Security
- WCAG: Accessibility
