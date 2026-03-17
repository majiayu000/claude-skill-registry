---
scope: uds-specific
description: |
  Testing pyramid and test writing standards for UT/IT/ST/E2E.
  Supports ISTQB and Industry Pyramid frameworks.
  Use when: writing tests, discussing test coverage, test strategy, or test naming.
  Keywords: test, unit, integration, e2e, coverage, mock, ISTQB, SIT, 測試, 單元, 整合, 端對端.
---

# Testing Guide

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/testing-guide/SKILL.md)

**Version**: 1.2.0
**Last Updated**: 2026-01-29
**Applicability**: Claude Code Skills

---

## Purpose

This skill provides testing pyramid standards and best practices for systematic testing, supporting both ISTQB and Industry Pyramid frameworks.

## Framework Selection

| Framework | Levels | Best For |
|-----------|--------|----------|
| **ISTQB** | UT → IT/SIT → ST → AT/UAT | Enterprise, compliance, formal QA |
| **Industry Pyramid** | UT (70%) → IT (20%) → E2E (10%) | Agile, DevOps, CI/CD |

**Note on Integration Testing abbreviation:**
- **IT** (Integration Testing): Agile/DevOps communities
- **SIT** (System Integration Testing): Enterprise/ISTQB contexts
- Both refer to the same testing level

## Quick Reference

### Testing Pyramid (Industry Standard)

```
              ┌─────────┐
              │   E2E   │  ← 10% (Fewer, slower)
             ─┴─────────┴─
            ┌─────────────┐
            │   IT/SIT    │  ← 20% (Integration)
           ─┴─────────────┴─
          ┌─────────────────┐
          │       UT        │  ← 70% (Unit)
          └─────────────────┘
```

### Test Levels Overview

| Level | Scope | Speed | Dependencies |
|-------|-------|-------|-------------|
| **UT** | Single function/class | < 100ms | Mocked |
| **IT/SIT** | Component interaction | 1-10s | Real DB (containerized) |
| **ST** | Full system (ISTQB) | Minutes | Production-like |
| **E2E** | User journeys | 30s+ | Everything real |
| **AT/UAT** | Business validation (ISTQB) | Varies | Everything real |

### Coverage Targets

| Metric | Minimum | Recommended |
|--------|---------|-------------|
| Line | 70% | 85% |
| Branch | 60% | 80% |
| Function | 80% | 90% |

## Detailed Guidelines

For complete standards, see:
- [Testing Standards](../../core/testing-standards.md) - Actionable rules
- [Testing Theory](./testing-theory.md) - Educational knowledge base
- [Testing Pyramid](./testing-pyramid.md) - Detailed pyramid ratios

### AI-Optimized Format (Token-Efficient)

For AI assistants, use the YAML format files for reduced token usage:
- Base standard: `ai/standards/testing.ai.yaml`
- Framework options:
  - ISTQB Framework: `ai/options/testing/istqb-framework.ai.yaml`
  - Industry Pyramid: `ai/options/testing/industry-pyramid.ai.yaml`
- Test level options:
  - Unit Testing: `ai/options/testing/unit-testing.ai.yaml`
  - Integration Testing: `ai/options/testing/integration-testing.ai.yaml`
  - System Testing: `ai/options/testing/system-testing.ai.yaml`
  - E2E Testing: `ai/options/testing/e2e-testing.ai.yaml`

## Naming Conventions

### File Naming

```
[ClassName]Tests.cs       # C#
[ClassName].test.ts       # TypeScript
[class_name]_test.py      # Python
[class_name]_test.go      # Go
```

### Method Naming

```
[MethodName]_[Scenario]_[ExpectedResult]()
should_[behavior]_when_[condition]()
test_[method]_[scenario]_[expected]()
```

## Test Doubles

| Type | Purpose | When to Use |
|------|---------|-------------|
| **Stub** | Returns predefined values | Fixed API responses |
| **Mock** | Verifies interactions | Check method called |
| **Fake** | Simplified implementation | In-memory database |
| **Spy** | Records calls, delegates | Partial mocking |

### When to Use What

- **UT**: Use mocks/stubs for all external deps
- **IT**: Use fakes for DB, stubs for external APIs
- **ST**: Real components, fake only external services
- **E2E**: Real everything

## AAA Pattern

```typescript
test('method_scenario_expected', () => {
    // Arrange - Setup test data
    const input = createTestInput();
    const sut = new SystemUnderTest();

    // Act - Execute behavior
    const result = sut.execute(input);

    // Assert - Verify result
    expect(result).toBe(expected);
});
```

## FIRST Principles

- **F**ast - Tests run quickly
- **I**ndependent - Tests don't affect each other
- **R**epeatable - Same result every time
- **S**elf-validating - Clear pass/fail
- **T**imely - Written with production code

## Anti-Patterns to Avoid

- ❌ Test Interdependence (tests must run in order)
- ❌ Flaky Tests (sometimes pass, sometimes fail)
- ❌ Testing Implementation Details
- ❌ Over-Mocking
- ❌ Missing Assertions
- ❌ Magic Numbers/Strings

---

## Testing Theory Essentials (YAML Compressed)

```yaml
# === ISTQB FUNDAMENTALS ===
terminology:
  error: "Human mistake in thinking"
  defect: "Bug in code (caused by error)"
  failure: "System behaves incorrectly (caused by defect)"
  chain: "Error → Defect → Failure"

oracle_problem:
  definition: "How do we know the expected result is correct?"
  approaches:
    - specification_oracle: "Compare against spec"
    - reference_oracle: "Compare against reference impl"
    - consistency_oracle: "Same input → same output"
    - heuristic_oracle: "Reasonable approximation"

# === STATIC vs DYNAMIC ===
static_testing:
  definition: "Examine without executing"
  techniques: [reviews, walkthroughs, inspections, static_analysis]
  finds: "Defects before runtime"
  examples: [ESLint, SonarQube, code_review]

dynamic_testing:
  definition: "Execute and observe behavior"
  techniques: [unit, integration, system, acceptance]
  finds: "Failures during execution"

# === TEST DESIGN TECHNIQUES ===
black_box:
  equivalence_partitioning:
    principle: "Divide inputs into equivalent classes"
    example: "Age: [<0 invalid], [0-17 minor], [18-64 adult], [65+ senior]"
  boundary_value:
    principle: "Test at boundaries of partitions"
    example: "Age: test -1, 0, 17, 18, 64, 65"
  decision_table:
    principle: "Combinations of conditions → actions"
    use: "Complex business rules"
  state_transition:
    principle: "Valid sequences of states"
    use: "Workflow, state machines"

white_box:
  statement_coverage: "Every statement executed once"
  branch_coverage: "Every decision branch taken"
  condition_coverage: "Every condition T/F"
  path_coverage: "Every possible path (often impractical)"

# === RISK-BASED TESTING ===
risk_assessment:
  likelihood: "How likely to fail?"
  impact: "How bad if fails?"
  priority: "likelihood × impact"

risk_matrix:
  high_high: "Test extensively, first priority"
  high_low: "Good coverage"
  low_high: "Good coverage"
  low_low: "Basic coverage"

# === DEFECT MANAGEMENT ===
defect_lifecycle:
  states: [new, assigned, in_progress, fixed, verified, closed]
  reopen_trigger: "Verification fails"

severity_vs_priority:
  severity: "Technical impact (critical/major/minor/trivial)"
  priority: "Business urgency (high/medium/low)"
  example: "Typo on login page: low severity, high priority (brand)"

# === TEST ENVIRONMENT ===
isolation_levels:
  unit: "In-memory, mocked deps"
  integration: "Containerized DB (Docker)"
  staging: "Production-like, isolated"
  production: "Real, feature flags for testing"

test_data_strategies:
  fixtures: "Static predefined data"
  factories: "Dynamic generation (faker)"
  snapshots: "Sanitized production copy"
  synthetic: "Algorithm-generated edge cases"
```

---

## Configuration Detection

This skill supports project-specific configuration.

### Detection Order

1. Check `CONTRIBUTING.md` for "Disabled Skills" section
   - If this skill is listed, it is disabled for this project
2. Check `CONTRIBUTING.md` for "Testing Standards" section
3. If not found, **default to standard coverage targets**

### First-Time Setup

If no configuration found and context is unclear:

1. Ask the user: "This project hasn't configured testing standards. Would you like to customize coverage targets?"
2. After user selection, suggest documenting in `CONTRIBUTING.md`:

```markdown
## Testing Standards

### Coverage Targets
| Metric | Target |
|--------|--------|
| Line | 80% |
| Branch | 70% |
| Function | 85% |
```

### Configuration Example

In project's `CONTRIBUTING.md`:

```markdown
## Testing Standards

### Coverage Targets
| Metric | Target |
|--------|--------|
| Line | 80% |
| Branch | 70% |
| Function | 85% |

### Testing Framework
- Unit Tests: Jest
- Integration Tests: Supertest
- E2E Tests: Playwright
```

---

## Related Standards

- [Testing Standards](../../core/testing-standards.md) - Actionable rules
- [Testing Theory](./testing-theory.md) - Educational knowledge base
- [Code Review Checklist](../../core/code-review-checklist.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.0 | 2026-01-29 | Added links to new testing-theory.md knowledge base |
| 1.1.0 | 2025-12-29 | Added Testing Theory Essentials YAML section |
| 1.0.0 | 2025-12-24 | Initial: Standard sections (Purpose, Related Standards, Version History, License) |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
