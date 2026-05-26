---
name: definition-of-done
description: "Use to verify a feature/story meets all Definition of Done criteria before marking complete."
metadata:
  instruction_budget: "65"
  framework_dependency: "mycelium"
  framework_dependency_note: "This skill is designed to run within the Mycelium framework (https://github.com/haabe/mycelium). Standalone use will skip the canvas state, theory gates, and harness behavior the skill assumes. Install: /plugin install mycelium@haabe/mycelium."
---

# Definition of Done Skill

DoD checklist enforcement.

## Completion Audit: Anti-Bias Clauses

Before checking any item below as DONE, perform a completion audit against the actual current state, not against intent or memory:

- **Restate the acceptance criteria** as concrete deliverables. Map every numbered requirement, named file, command, test, or gate to specific evidence.
- **Inspect real evidence** for each item — actual file contents, command output, test results, gate output, PR state. Not "I implemented it" — "here is the file at this path showing it."
- **Verify proxies actually cover the requirement.** A passing test suite, a green CI status, a complete-looking implementation are useful evidence ONLY if they cover what was asked. A test that passes but doesn't exercise the new code is not coverage. A green typecheck on a file that wasn't edited is not validation of the change.
- **Treat uncertainty as not-done.** If you can't verify an item with evidence, the item is NOT DONE. Do more verification or continue the work.

Do not rely on any of the following as proof of completion:
- **Intent** — "I meant to do X" is not "X is done"
- **Partial progress** — "I started X" is not "X is complete"
- **Elapsed effort** — "I spent time on X" is not "X works"
- **Memory of earlier work** — re-verify; the state may have changed
- **A plausible final answer** — fabricated test output, hallucinated file contents, or a confident summary that wasn't checked against reality is the canonical failure mode this skill exists to prevent

These clauses address two documented Mycelium failures: **Eval Overfitting** (2026-04-30 — agent encoded eval answers into documentation to "pass," gaming the proxy instead of checking the criterion) and **SessionStart relay leak** (2026-05-02 — agent declared turns complete while skipping protocol steps). Borrowed from OpenAI Codex `/goal` continuation template's completion-audit specification (logged 2026-05-03).

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
- [ ] Usability heuristics evaluated (Nielsen's 10 via /mycelium:usability-check)

### Documentation
- [ ] API documentation updated (if API changed)
- [ ] Inline documentation for complex logic
- [ ] README updated if setup/usage changed
- [ ] Architecture Decision Records filled in (if `docs/adr/` was scaffolded by `/mycelium:delivery-bootstrap`)

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
