---
name: test-orchestrator
description: |
  Unified orchestration layer that coordinates all test skills into cohesive validation pipelines.
  Provides a single entry point for comprehensive project validation with intelligent skill selection,
  quality gates, and consolidated reporting. Supports quick PR checks through full release validation.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
  - Task
compatibility:
  claude-code: ">=1.0.0"
metadata:
  version: "1.0.0"
  author: "QuantQuiver AI R&D"
  category: "testing"
  tags:
    - orchestration
    - validation-pipeline
    - ci-cd
    - quality-gates
---

# Test Orchestrator

## Purpose

Unified orchestration layer that coordinates all test skills into cohesive validation pipelines. Provides a single entry point for comprehensive project validation with intelligent skill selection, quality gates, and consolidated reporting.

## Triggers

Use this skill when:
- "run full test suite"
- "validate this project"
- "comprehensive testing"
- "pre-deployment validation"
- "test everything"
- "quality gate check"
- "CI/CD validation pipeline"

## When to Use

- New project setup requiring test infrastructure
- Pre-release validation checkpoints
- Continuous integration pipeline design
- Quality assurance automation
- Multi-dimensional validation needs

## When NOT to Use

- Running individual test types (use specific skill)
- Simple single-skill validation
- Quick exploratory testing

---

## Core Instructions

### Skill Coordination Matrix

| Skill | When Triggered | Output |
|-------|---------------|--------|
| `unit-test-generator` | Code files present | Generated tests, coverage |
| `api-contract-validator` | OpenAPI spec found | Contract report |
| `security-test-suite` | Always (security critical) | Security report |
| `performance-benchmark` | Endpoints defined | Performance report |
| `data-validation` | Data files/schemas present | Quality report |
| `test-health-monitor` | Existing tests found | Health report |

### Predefined Pipelines

| Pipeline | Duration | Use Case |
|----------|----------|----------|
| `quick_validation` | < 5 min | PR checks |
| `standard_validation` | < 15 min | CI/CD |
| `comprehensive_validation` | < 60 min | Releases |
| `pre_production` | < 120 min | Production readiness |

### Pipeline Configurations

```yaml
quick_validation:
  skills:
    - unit-test-generator: { mode: "check-existing" }
    - security-test-suite: { scan_types: ["sast", "secrets"] }
  parallel: true

comprehensive_validation:
  skills:
    - unit-test-generator: { coverage_target: 85 }
    - api-contract-validator: { breaking_changes: true }
    - security-test-suite: { scan_types: "all" }
    - performance-benchmark: { scenarios: ["baseline", "load", "stress"] }
    - data-validation: { all_dimensions: true }
    - test-health-monitor: { flaky_detection: true }
  gates:
    - security_critical: 0
    - coverage: ">= 80"
    - performance_p99: "< 500ms"
```

### Quality Gates

| Gate | Target | Blocking |
|------|--------|----------|
| Security Critical | 0 | Yes |
| Security High | 0 | Yes |
| Coverage | >= 80% | No |
| p99 Latency | < 500ms | Yes |
| Error Rate | < 0.1% | Yes |
| Data Quality | >= 80 | No |

---

## Templates

### Unified Validation Report

```markdown
# Project Validation Report

**Project:** {project_name}
**Pipeline:** {pipeline_name}
**Generated:** {timestamp}
**Duration:** {duration} seconds

## Executive Summary

### Overall Status: {status}

| Gate | Target | Actual | Status |
|------|--------|--------|--------|
| Security Critical | 0 | {actual} | {status_icon} |
| Security High | 0 | {actual} | {status_icon} |
| Coverage | >= 80% | {actual}% | {status_icon} |
| p99 Latency | < 500ms | {actual}ms | {status_icon} |

### Risk Assessment

**Deployment Risk:** {risk_level}

**Blocking Issues:**
- {blocking_issue}

## Skill Results Summary

| Skill | Status | Score | Issues | Duration |
|-------|--------|-------|--------|----------|
| Unit Tests | {status} | {score} | {issues} | {duration} |
| Security | {status} | {score} | {issues} | {duration} |
| Performance | {status} | {score} | {issues} | {duration} |

## Recommended Actions

### Immediate (Block Deployment)
1. {action}

### Before Next Release
2. {action}
```

---

## Example

**Input**: Pre-release validation

**Output**:
```markdown
## Executive Summary

### Overall Status: CONDITIONAL PASS

| Gate | Target | Actual | Status |
|------|--------|--------|--------|
| Security Critical | 0 | 0 | Pass |
| Security High | 0 | 2 | Fail |
| Coverage | >= 80% | 82.3% | Pass |
| p99 Latency | < 500ms | 234ms | Pass |

### Risk Assessment

**Deployment Risk:** MEDIUM

**Blocking Issues:**
- 2 HIGH severity security vulnerabilities require remediation
- Estimated fix time: 4-8 hours

## Skill Results Summary

| Skill | Status | Score | Issues |
|-------|--------|-------|--------|
| Unit Tests | Pass | 82.3% | 3 flaky |
| API Contract | Pass | 100% | 0 |
| Security | Fail | 2 HIGH | 8 total |
| Performance | Pass | 234ms p99 | 0 |
```

---

## Validation Checklist

- [ ] All enabled skills executed successfully
- [ ] Quality gates evaluated against targets
- [ ] Blocking issues clearly identified
- [ ] Risk assessment reflects findings
- [ ] Recommendations are prioritized
- [ ] Individual skill reports generated
- [ ] Unified report is comprehensive

---

## Related Skills

- `unit-test-generator` - Generate unit tests
- `api-contract-validator` - Validate API contracts
- `security-test-suite` - Security scanning
- `performance-benchmark` - Performance testing
- `data-validation` - Data quality validation
- `test-health-monitor` - Test suite health
