---
name: qa
description: QA workflow for software projects. Use for tasks like writing test plans, deriving test cases from PRDs, risk-based testing, API testing, UI testing, test data design, defect reporting, release checklists, and setting up automation strategy (unit/integration/e2e) with clear entry/exit criteria.
---

# qa

Use this skill to drive Quality Assurance work end-to-end: test planning, test case design, execution strategy, and release readiness.

## Core outputs (pick what the task needs)

- Test plan (scope, approach, environments, entry/exit criteria)
- Risk matrix (severity × probability × detectability)
- Test cases (functional, negative, boundary, compatibility)
- API test checklist (contracts, auth, idempotency, error codes)
- Regression suite definition and release checklist
- Automation strategy (what to automate, where to stop)

## Workflow

1) Understand the product and changes
- Identify user journeys, critical flows, and non-functional requirements.
- List assumptions and external dependencies (3rd party APIs, DB migrations).

2) Risk-based test design
- Classify features by business criticality and change frequency.
- Prioritize tests for high-risk areas: auth, payments, data integrity, permissions, migrations.

3) Derive test cases
- Happy path + negative path + boundary conditions.
- State transitions, concurrency, retries, and idempotency for APIs.
- Localization/timezone, accessibility, performance where relevant.

4) Test data and environment
- Define test accounts/roles.
- Seed data strategy; ensure repeatability and cleanup.
- Identify environment parity gaps (staging vs prod).

5) Execution and reporting
- Run smoke → functional → regression.
- Record evidence, steps to reproduce, expected vs actual, logs/screenshots.
- Triage and retest; track flaky issues explicitly.

6) Release readiness
- Define entry/exit criteria.
- Prepare rollback plan and monitoring checks (error rate, latency, core KPIs).

## Defect report template (use verbatim)

- Title:
- Environment:
- Version/commit:
- Severity / Priority:
- Preconditions:
- Steps to reproduce:
- Expected:
- Actual:
- Attachments (logs/screenshots/video):
- Notes (suspected area, frequency, impact):

## Automation guidance (practical)

- Automate high-value stable paths first (smoke + core regression).
- Prefer unit/integration tests before E2E.
- Keep E2E small, deterministic, and focused on journeys.
- Add contract tests for APIs; pin schemas and error codes.

