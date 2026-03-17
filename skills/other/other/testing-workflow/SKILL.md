---
name: testing-workflow
model: standard
category: testing
description: Meta-skill that orchestrates comprehensive testing across a project by coordinating testing-patterns, e2e-testing, and testing agents. Use when setting up testing for a new project, improving coverage for an existing project, establishing a testing strategy, or verifying quality before a release.
version: 1.0
---

# Testing Workflow

Orchestrate comprehensive testing across a project by coordinating the **testing-patterns** skill, **e2e-testing** skill, and testing agents. This meta-skill does not define test patterns itself — it routes to the right skill or agent at each stage and ensures nothing is missed.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install testing-workflow
```


---

## When to Use

- Setting up testing for a new project from scratch
- Improving coverage for an existing project with gaps
- Establishing or revising a testing strategy
- Before a major release to verify quality gates are met
- After a large refactor to confirm nothing broke
- During code review when test adequacy is in question
- Onboarding a team to a testing workflow

---

## Orchestration Flow

Follow these steps in order. Each step routes to a specific skill or agent — read and apply that resource before moving to the next step.

### Phase 1: Discovery and Baseline

Scan the project to understand existing test infrastructure, measure current coverage, and identify gaps before making changes. Without a baseline, you cannot demonstrate improvement.

1. **Identify test infrastructure** — Determine the test runner, assertion library, coverage tool, and CI configuration already in use. If none exist, flag that setup is needed.
2. **Measure current coverage** — Run the existing test suite and record statement, branch, and function coverage. This is the baseline.
3. **Map untested code** — Identify modules, functions, and code paths with no test coverage. Prioritize by risk: business-critical logic first, utilities last.
4. **Catalog existing tests** — Categorize existing tests as unit, integration, or E2E. Check for skipped tests, flaky tests, and tests that don't assert anything meaningful.

### Phase 2: Strategy Selection

Based on the discovery results, select the appropriate testing approach for this project.

1. **Determine project type** — Use the Coverage Targets table below to set appropriate thresholds for the project type.
2. **Select test patterns** — Read `ai/skills/testing/testing-patterns/SKILL.md` and choose the unit/integration test patterns that match the project's architecture, language, and framework.
3. **Identify critical user journeys** — List the 3-10 most important user workflows that require E2E coverage. These are flows where a failure would directly impact revenue, user trust, or safety.
4. **Document the strategy** — Fill in the Testing Strategy Template (below) and commit it to the repository.

### Phase 3: Implementation

Generate tests following the patterns selected in Phase 2.

1. **Unit tests first** — Write unit tests for uncovered business logic, starting with the highest-risk modules. Follow the testing pyramid: ~70% of your tests should be unit tests.
2. **Integration tests next** — Write integration tests for module boundaries, API endpoints, and database queries. Focus on the seams where components interact.
3. **E2E tests for critical journeys** — Read `ai/skills/testing/e2e-testing/SKILL.md` and write E2E tests for each critical user journey identified in Phase 2.
4. **Edge case coverage** — After the happy paths are covered, add tests for error conditions, boundary values, null/empty inputs, and concurrency scenarios.

### Phase 4: Validation

Verify that the new tests meet quality standards and coverage targets.

1. **Run the full test suite** — Every test must pass. Fix failures before proceeding.
2. **Measure coverage against targets** — Compare new coverage against the thresholds for the project type. If targets are not met, return to Phase 3.
3. **Check test quality** — Review tests for the anti-patterns listed in testing-patterns (assert-free tests, overmocking, flaky tests, test pollution). Fix any found.
4. **Verify CI integration** — Confirm that tests run automatically on every push/PR and that coverage thresholds are enforced in CI.

### Phase 5: Maintenance

Establish ongoing practices to keep the test suite healthy.

1. **Set up coverage ratcheting** — Configure CI to fail if coverage drops below the current level. Coverage should only go up.
2. **Establish flaky test policy** — Any test that fails intermittently must be fixed within one sprint or removed with a justification.
3. **Define test review standards** — Every PR that adds or changes logic must include corresponding test changes. Reviewers check for this.
4. **Schedule test health audits** — Quarterly, review test execution time, flaky test rate, skipped test count, and coverage trends.

---

## Skill Routing Table

Use this table to route specific needs to the correct resource:

| Need | Route To | Path |
|------|----------|------|
| Unit/integration test patterns | testing-patterns | `ai/skills/testing/testing-patterns/SKILL.md` |
| E2E test patterns | e2e-testing | `ai/skills/testing/e2e-testing/SKILL.md` |
| Code quality standards | clean-code | `ai/skills/testing/clean-code/SKILL.md` |
| Review checklist | code-review | `ai/skills/testing/code-review/SKILL.md` |
| CI/CD quality gates | quality-gates | `ai/skills/testing/quality-gates/SKILL.md` |
| Debugging test failures | debugging | `ai/skills/testing/debugging/SKILL.md` |

When a request falls clearly into one row, go directly to that resource. Use the full orchestration flow only when comprehensive coverage is the goal.

---

## Coverage Targets

Targets vary by project type. Use the appropriate row to set expectations:

| Project Type | Statement | Branch | Function | E2E Journeys | Notes |
|--------------|-----------|--------|----------|--------------|-------|
| Startup MVP | 60% | 50% | 60% | Top 3 flows | Focus on critical paths only |
| Production App | 80% | 70% | 80% | Top 10 flows | Balance speed with confidence |
| Library / Package | 90% | 85% | 95% | N/A | Public API must be fully covered |
| Critical Infrastructure | 95% | 90% | 95% | All flows | Zero tolerance for gaps |

These are minimums. Aim higher when time permits, but do not block releases on vanity metrics — prioritize meaningful coverage over percentage points.

---

## Testing Strategy Template

Use this template to document the testing strategy for a project. Fill it in during the orchestration flow and keep it in the repo.

```markdown
# Testing Strategy

## Project Overview
- **Project**: [name]
- **Type**: [startup MVP | production app | library | critical infrastructure]
- **Primary Language**: [language]
- **Framework**: [framework]
- **Test Runner**: [runner]
- **Coverage Tool**: [tool]

## Coverage Baseline
- **Statement**: [X%]
- **Branch**: [X%]
- **Function**: [X%]
- **E2E Journeys Covered**: [N of M]
- **Date Measured**: [YYYY-MM-DD]

## Coverage Targets
- **Statement**: [target%]
- **Branch**: [target%]
- **Function**: [target%]
- **E2E Journeys**: [target count]

## Test Patterns Selected
- [ ] [Pattern 1 — reason for selection]
- [ ] [Pattern 2 — reason for selection]
- [ ] [Pattern 3 — reason for selection]

## Critical User Journeys (E2E)
1. [Journey 1 — e.g., signup -> onboarding -> first action]
2. [Journey 2 — e.g., login -> dashboard -> export]
3. [Journey 3 — e.g., checkout -> payment -> confirmation]

## Gaps and Risks
- [Untested area 1 — risk level, mitigation plan]
- [Untested area 2 — risk level, mitigation plan]

## Quality Gate Status
- [ ] All tests pass
- [ ] Coverage targets met
- [ ] Critical journeys covered with E2E
- [ ] No skipped tests without justification
- [ ] Test execution time within budget
- [ ] CI enforces coverage thresholds
```

---

## Quality Gates for Testing Completion

All of the following must be satisfied before marking testing complete:

| Gate | Requirement | Why |
|------|------------|-----|
| **All tests pass** | Zero failures, zero errors | Flaky tests count as failures |
| **Coverage targets met** | Statement, branch, and function coverage meet project-type thresholds | Untested code is unverified code |
| **Critical journeys covered** | Every critical user journey has a passing E2E test | Revenue and trust depend on these flows |
| **No unjustified skips** | Every `skip`, `xit`, or `xdescribe` has a comment and linked issue | Skipped tests rot into permanent gaps |
| **Execution time budget** | Unit < 60s, E2E < 10min | Slow suites get skipped by developers |
| **No test pollution** | Running any test file alone produces same results as full suite | Shared state masks failures |
| **Mocks are justified** | Every mock has a comment explaining why the real impl cannot be used | Over-mocking hides real bugs |

---

## NEVER Do

1. **NEVER write tests that test implementation details instead of behavior** — tests must verify what the code does, not how it does it
2. **NEVER skip the discovery phase** — always measure the baseline before writing new tests, or you cannot demonstrate improvement
3. **NEVER merge tests that depend on execution order** — each test must be independent and idempotent
4. **NEVER mock what you do not own** — wrap third-party dependencies in your own adapters and mock the adapters instead
5. **NEVER treat coverage percentage as the sole quality metric** — 100% coverage with weak assertions is worse than 70% coverage with strong assertions
6. **NEVER leave the test suite in a failing state** — if a test fails, fix it or remove it with a justification before moving on
7. **NEVER skip E2E tests for critical user journeys** — unit tests alone cannot catch integration failures in flows that matter most
8. **NEVER deploy without running the full test suite** — partial test runs create false confidence
