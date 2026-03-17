---
name: release-validation
description: The final "Green Light". Checks all test suites (Unit, Int, E2E) and third-party reports.
role: ops-release
triggers:
  - release check
  - go no go
  - release readiness
  - acceptance
  - smoke test
---

# release-validation Skill

This skill is the "Gatekeeper" of Production.

## 1. The 7-Gate Quality System (Review)
1.  **Spec**: PRD Approved?
2.  **Arch**: ADRs + Threat Model?
3.  **Code**: Lint + Clean Code?
4.  **Test**: Unit + Int Pass?
5.  **Security**: SAST + Dep Scan?
6.  **Performance**: Load Test Pass?
7.  **E2E**: Critical Journeys Pass?

## 2. Validation Workflow
1.  **Freeze**: No new code commits.
2.  **Audit**: Run `traceability-audit.skill.md`. (Did we build what we promised?).
3.  **Test**: Trigger full regression suite on Staging.
4.  **Sign-off**: Collect approvals from Lead, Product, Security.

## 3. Decision Matrix
- **Critical Bug**: NO GO.
- **Major Bug (Workaround available)**: GO (with Hotfix scheduled).
- **Minor UI Glitch**: GO.
- **Security High**: NO GO.

## 4. Output
Use `templates/ops/RELEASE_READINESS_REPORT.md` to document the decision.
