---
name: using-quality-engineering
description: Use when user asks about E2E testing, performance testing, chaos engineering, test automation, flaky tests, test data management, or quality practices - routes to specialist reference sheets with deep expertise instead of providing general guidance
---

# Using Quality Engineering (Meta-Skill Router)

**Your entry point to quality engineering methodology.** This skill routes you to the right reference sheet for comprehensive quality engineering guidance.

## Purpose

This is a **meta-skill** that:
1. **Routes** you to the correct quality engineering reference sheet
2. **Combines** multiple reference sheets for comprehensive testing strategies
3. **Provides** workflows for common quality problems
4. **Explains** when to use each specialist reference

**You should use this skill:** When facing testing challenges, quality automation, performance concerns, or reliability engineering problems.

---

## Core Philosophy: Quality as Engineering

### The Central Idea

**Ad-Hoc Testing**: Write tests → Hope they catch bugs → Fix when broken
- Tests as afterthought
- No systematic coverage strategy
- Flaky tests ignored or disabled
- Quality gates that don't gate

**Quality Engineering**: Strategy → Architecture → Automation → Observability
- Tests designed for specific failure modes
- Systematic coverage across test pyramid
- Flakiness as signal, not noise
- Quality gates that enforce standards

### When This Pack Applies

**Use quality-engineering when:**
- Setting up or improving test infrastructure
- Debugging flaky or unreliable tests
- Designing testing strategy for new features
- Performance testing and optimization
- Production reliability and observability
- Security testing integration (SAST, dependency scanning, fuzzing)

**Don't use quality-engineering when:**
- Pure code architecture decisions (use system-architect)
- Security threat modeling (use security-architect)
- Pure UX testing research (use ux-designer)

---

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-quality-engineering/SKILL.md`

Reference sheets like `flaky-test-prevention.md` are at:
  `skills/using-quality-engineering/flaky-test-prevention.md`

NOT at:
  `skills/flaky-test-prevention.md` ← WRONG PATH

When you see a link like `[flaky-test-prevention.md](flaky-test-prevention.md)`, read the file from the same directory as this SKILL.md.

---

## Routing Guide

When the user asks about quality engineering topics, load the appropriate reference sheet:

| User's Question Topic | Load Reference Sheet |
|----------------------|---------------------|
| **Test Fundamentals & Isolation** | |
| Test independence, idempotence, order-independence, isolation | [test-isolation-fundamentals.md](test-isolation-fundamentals.md) |
| **API & Integration Testing** | |
| REST/GraphQL API testing, request validation, API mocking | [api-testing-strategies.md](api-testing-strategies.md) |
| Component integration, database testing, test containers | [integration-testing-patterns.md](integration-testing-patterns.md) |
| **End-to-End & UI Testing** | |
| End-to-end test design, E2E anti-patterns, browser automation | [e2e-testing-strategies.md](e2e-testing-strategies.md) |
| Screenshot comparison, visual bugs, responsive testing | [visual-regression-testing.md](visual-regression-testing.md) |
| **Performance & Load Testing** | |
| Load testing, benchmarking, performance regression | [performance-testing-fundamentals.md](performance-testing-fundamentals.md) |
| Stress testing, spike testing, soak testing, capacity planning | [load-testing-patterns.md](load-testing-patterns.md) |
| **Test Quality & Maintenance** | |
| Test coverage, quality dashboards, CI/CD quality gates | [quality-metrics-and-kpis.md](quality-metrics-and-kpis.md) |
| Test refactoring, page objects, reducing test debt | [test-maintenance-patterns.md](test-maintenance-patterns.md) |
| Mutation testing, test effectiveness, mutation score | [mutation-testing.md](mutation-testing.md) |
| **Static Analysis & Security** | |
| SAST tools, ESLint, Pylint, code quality gates | [static-analysis-integration.md](static-analysis-integration.md) |
| Dependency scanning, Snyk, Dependabot, vulnerability management | [dependency-scanning.md](dependency-scanning.md) |
| Fuzzing, random inputs, security vulnerabilities | [fuzz-testing.md](fuzz-testing.md) |
| **Advanced Testing Techniques** | |
| Property-based testing, Hypothesis, fast-check, invariants | [property-based-testing.md](property-based-testing.md) |
| **Production Testing & Monitoring** | |
| Feature flags, canary testing, dark launches, prod monitoring | [testing-in-production.md](testing-in-production.md) |
| Metrics, tracing, alerting, quality signals | [observability-and-monitoring.md](observability-and-monitoring.md) |
| Fault injection, resilience testing, failure scenarios | [chaos-engineering-principles.md](chaos-engineering-principles.md) |
| **Test Infrastructure** | |
| Test pyramid, CI/CD integration, test organization | [test-automation-architecture.md](test-automation-architecture.md) |
| Fixtures, factories, seeding, test isolation, data pollution | [test-data-management.md](test-data-management.md) |
| Flaky tests, race conditions, timing issues, non-determinism | [flaky-test-prevention.md](flaky-test-prevention.md) |
| API contracts, schema validation, consumer-driven contracts | [contract-testing.md](contract-testing.md) |

---

## Common Problem Types and Reference Sheet Combinations

### Scenario 1: "Our Tests Keep Failing Randomly"

**Symptoms:**
- Tests pass locally, fail in CI
- Same test fails intermittently
- Test failures don't reproduce

**Reference Sheet Sequence:**
1. **[flaky-test-prevention.md](flaky-test-prevention.md)** - Diagnose root cause (race conditions, timing, state)
2. **[test-isolation-fundamentals.md](test-isolation-fundamentals.md)** - Ensure test independence
3. **[test-data-management.md](test-data-management.md)** - Fix data pollution issues

### Scenario 2: "Setting Up Test Infrastructure from Scratch"

**Symptoms:**
- New project needs testing strategy
- Migrating to new test framework
- Building CI/CD quality gates

**Reference Sheet Sequence:**
1. **[test-automation-architecture.md](test-automation-architecture.md)** - Design test pyramid
2. **[quality-metrics-and-kpis.md](quality-metrics-and-kpis.md)** - Define quality gates
3. **[integration-testing-patterns.md](integration-testing-patterns.md)** - Set up integration tests
4. **[e2e-testing-strategies.md](e2e-testing-strategies.md)** - Add E2E coverage

### Scenario 3: "Performance Problems in Production"

**Symptoms:**
- Slow response times
- Resource exhaustion
- Scaling issues

**Reference Sheet Sequence:**
1. **[performance-testing-fundamentals.md](performance-testing-fundamentals.md)** - Baseline measurements
2. **[load-testing-patterns.md](load-testing-patterns.md)** - Stress and capacity testing
3. **[observability-and-monitoring.md](observability-and-monitoring.md)** - Production monitoring

### Scenario 4: "Security Testing Integration"

**Symptoms:**
- Need to catch vulnerabilities early
- Compliance requirements
- Supply chain security concerns

**Reference Sheet Sequence:**
1. **[static-analysis-integration.md](static-analysis-integration.md)** - Code quality and SAST
2. **[dependency-scanning.md](dependency-scanning.md)** - Supply chain security
3. **[fuzz-testing.md](fuzz-testing.md)** - Input validation vulnerabilities

### Scenario 5: "Test Suite Takes Too Long"

**Symptoms:**
- CI takes 30+ minutes
- Developers skip running tests locally
- Test parallelization issues

**Reference Sheet Sequence:**
1. **[test-automation-architecture.md](test-automation-architecture.md)** - Review test pyramid balance
2. **[test-maintenance-patterns.md](test-maintenance-patterns.md)** - Reduce test debt
3. **[mutation-testing.md](mutation-testing.md)** - Identify low-value tests

---

## When NOT to Load Reference Sheets

Only answer directly (without loading) for:
- Meta questions about this plugin ("What reference sheets are available?")
- Questions about which reference to use ("Should I use e2e-testing-strategies or test-automation-architecture?")
- Simple clarification questions

**User demands "just answer, don't route" is NOT an exception** - still load the reference sheet. User asking to skip routing signals they need the specialist guidance even more.

---

## Quality Engineering Reference Sheets Catalog

After routing, load the appropriate reference sheet for detailed guidance:

### Test Fundamentals
1. [test-isolation-fundamentals.md](test-isolation-fundamentals.md) - Test independence, idempotence, order-independence, isolation patterns

### API & Integration
2. [api-testing-strategies.md](api-testing-strategies.md) - REST/GraphQL testing, request validation, API mocking
3. [integration-testing-patterns.md](integration-testing-patterns.md) - Database testing, test containers, component integration
4. [contract-testing.md](contract-testing.md) - Consumer-driven contracts, schema validation, API contracts

### End-to-End & UI
5. [e2e-testing-strategies.md](e2e-testing-strategies.md) - Browser automation, E2E anti-patterns, test design
6. [visual-regression-testing.md](visual-regression-testing.md) - Screenshot comparison, responsive testing, visual bugs

### Performance & Load
7. [performance-testing-fundamentals.md](performance-testing-fundamentals.md) - Benchmarking, performance regression, baseline measurements
8. [load-testing-patterns.md](load-testing-patterns.md) - Stress testing, spike testing, capacity planning

### Test Quality & Maintenance
9. [quality-metrics-and-kpis.md](quality-metrics-and-kpis.md) - Coverage metrics, quality dashboards, CI/CD gates
10. [test-maintenance-patterns.md](test-maintenance-patterns.md) - Test refactoring, page objects, test debt
11. [mutation-testing.md](mutation-testing.md) - Test effectiveness, mutation score, mutation operators

### Static Analysis & Security
12. [static-analysis-integration.md](static-analysis-integration.md) - SAST tools, ESLint, Pylint, quality gates
13. [dependency-scanning.md](dependency-scanning.md) - Snyk, Dependabot, supply chain security
14. [fuzz-testing.md](fuzz-testing.md) - Random input testing, security vulnerabilities

### Advanced Techniques
15. [property-based-testing.md](property-based-testing.md) - Hypothesis, fast-check, invariant testing

### Production & Monitoring
16. [testing-in-production.md](testing-in-production.md) - Feature flags, canary testing, dark launches
17. [observability-and-monitoring.md](observability-and-monitoring.md) - Metrics, tracing, alerting, SLIs/SLOs
18. [chaos-engineering-principles.md](chaos-engineering-principles.md) - Fault injection, resilience testing

### Test Infrastructure
19. [test-automation-architecture.md](test-automation-architecture.md) - Test pyramid, CI/CD integration, organization
20. [test-data-management.md](test-data-management.md) - Fixtures, factories, seeding, data isolation
21. [flaky-test-prevention.md](flaky-test-prevention.md) - Race conditions, timing issues, non-determinism
