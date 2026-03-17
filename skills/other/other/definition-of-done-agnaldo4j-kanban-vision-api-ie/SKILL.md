---
name: definition-of-done
description: >
  Read this skill before declaring any task, feature, bug fix, or tech debt item
  as complete. Applies to all downstream platform work. Every checkbox must be
  confirmed or explicitly justified as not applicable. If any box is unchecked
  without justification, the item is NOT done — do not mark it as such.
---

# Definition of Done — Platform Downstream

> **Golden Rule**: If any checkbox below is not checked, it is not done.
> Quality, security, and predictability for B2B/B2C come from fully meeting this DoD.
> If something prevented compliance, identify it and fix it so the next delivery is compliant.

---

## How to use this skill

When asked to finish, close, or mark a task as done:

1. Go through each section below.
2. For each item, confirm it was done or explicitly state why it is N/A.
3. If any item is missing, implement it or flag it before closing.
4. Never silently skip a section.

---

## 1. Contract, Traceability and Origin

- [ ] Item entered through official channels with origin and service class defined:
  `Feature/Outcome` | `Bug/Incident` | `Risk/Compliance` | `Tech Debt` | `Discovery/Experiment`
- [ ] Problem or hypothesis is clear, with target metric/SLO and success criteria defined.
- [ ] End-to-end traceability confirmed: `ticket ↔ branch/commits/PR ↔ build ↔ deploy ↔ business event/feature flag`

---

## 2. Technical Quality and Tests

- [ ] **Unit tests** written: fast, deterministic, given–when–then, covering success and error paths.
- [ ] **Integration/contract tests** written for every boundary (DB, APIs, queues) — OpenAPI/AsyncAPI/CDC updated.
- [ ] **Regression test** added if this is a bug fix (test that would have caught the bug).
- [ ] Code is simple, readable, and reviewed. Complexity and hotspots are under control.

---

## 3. Versioning and Backward Compatibility

- [ ] Additive changes kept in the same version. Breaking changes only in a major version with migration path.
- [ ] OpenAPI/AsyncAPI and changelog updated. Deprecated fields marked with a defined sunset window.
- [ ] Gateway/routing by version and flags ready for safe transition.

---

## 4. Security and Compliance

- [ ] Security scans completed (SCA / SAST / Secrets) — manually or via CI. Secrets rotated, minimum access principle applied.
- [ ] Test data is reproducible and free of sensitive PII.
- [ ] Incident response runbook updated if applicable.

---

## 5. Enablement and CI/CD

- [ ] Local environment runs with a single command and is in parity with CI/staging.
- [ ] CI pipeline green: build, tests, contracts, security. **No flaky tests allowed.**
- [ ] Feature flags / Dark Launch / Branch by Abstraction applied when the delivery is phased or incomplete.

---

## 6. Observability and Alerts

- [ ] Metrics, logs, and traces instrumented (golden signals: latency, traffic, errors, saturation).
- [ ] Dashboards published per domain/version/feature.
- [ ] Alerts configured: high signal, low noise — triggered by user impact or SLO breach.
- [ ] Each alert points to a runbook with clear actions and rollback steps.

---

## 7. Performance, Reliability and Risk

- [ ] Functional and performance limits defined. Circuit breakers, rate limiting, and timeouts in place.
- [ ] Risks mapped and mitigated (Plan A/B, canary/blue-green when applicable).
- [ ] High-risk items do not go to production without proportional mitigation.

---

## 8. Safe Deploy and Rollback

- [ ] Release strategy defined (canary / blue-green / gradual) — separate from deployment.
- [ ] Rollback plan tested and reversible. Health checks are reliable.

---

## 9. Documentation and Communication

- [ ] README / operational how-to updated. Decisions recorded (RFC when needed).
- [ ] Final communication posted in the official channel with summary, links (PR, docs, dashboards) and next steps.

---

## 10. Bug-Specific Criteria (OPON — escalated bugs)

*Apply only to items flagged as OPON (bugs escalated from Online Operations).*

- [ ] Classified and prioritized by impact (SLO / revenue / risk).
- [ ] Fix deployed to production within **15 calendar days** from triage acceptance.
- [ ] Post-deploy observability of the case confirmed and lightweight root-cause analysis completed.
- [ ] SLA violation metric updated.

---

## 11. Post-Deploy and Closure

- [ ] Production verification done: dashboards and alerts show no anomalies.
- [ ] Telemetry confirms expected outcome (business event fired, metric moved as expected).
- [ ] Flow is stable: item is not aging in any stage, no avoidable debt left for the next person.
- [ ] **All criteria above met → Done.**

---

## Quick reference — common failure modes

| Skipped item | Risk |
|---|---|
| No unit tests | Regression in next change, harder to refactor |
| No integration test for DB/API boundary | Silent contract break in production |
| No feature flag for incomplete feature | Unfinished work exposed to users |
| No observability | Blind in production, high MTTR |
| No rollback plan | Cannot recover fast from bad deploy |
| Breaking change without versioning | Downstream services break silently |
| Bug closed without regression test | Same bug ships again |
| OPON bug over 15 days | SLA violation, escalation required |