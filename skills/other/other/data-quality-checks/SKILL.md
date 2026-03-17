---
id: SKL-data-DATAQUALITYCHECKS
name: Data Quality Checks
description: Data Quality Checks are automated tests that validate data against predefined
  rules and expectations. They act as the "unit tests" for data, catching issues before
  they propagate downstream to analyti
version: 1.0.0
status: active
owner: '@cerebra-team'
last_updated: '2026-02-22'
category: Backend
tags:
- api
- backend
- server
- database
stack:
- Python
- Node.js
- REST API
- GraphQL
difficulty: Intermediate
---

# Data Quality Checks

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Data Quality Checks are automated tests that validate data against predefined rules and expectations. They act as the "unit tests" for data, catching issues before they propagate downstream to analytics, ML models, or business decisions.

**Core Principle**: "Trust but verify. Every data pipeline should have quality gates."

This skill provides comprehensive guidance on implementing data quality checks across the data pipeline, from database constraints to ML-based anomaly detection.

## Why This Matters
- **<Benefit>**: <short explanation>
- **<Benefit>**: <short explanation>
- **<Benefit>**: <short explanation>

## Core Concepts & Rules

### 1. Core Principles
- Follow established patterns and conventions
- Maintain consistency across codebase
- Document decisions and trade-offs

### 2. Implementation Guidelines
- Start with the simplest viable solution
- Iterate based on feedback and requirements
- Test thoroughly before deployment


## Inputs / Outputs / Contracts
* **Inputs**:
  - <e.g., env vars, request payload, file paths, schema>
* **Entry Conditions**:
  - <Pre-requisites: e.g., Repo initialized, DB running, specific branch checked out>
* **Outputs**:
  - <e.g., artifacts (PR diff, docs, tests, dashboard JSON)>
* **Artifacts Required (Deliverables)**:
  - <e.g., Code Diff, Unit Tests, Migration Script, API Docs>
* **Acceptance Evidence**:
  - <e.g., Test Report (screenshot/log), Benchmark Result, Security Scan Report>
* **Success Criteria**:
  - <e.g., p95 < 300ms, coverage ≥ 80%>

## Skill Composition
* **Depends on**: None
* **Compatible with**: None
* **Conflicts with**: None
* **Related Skills**: None

## Quick Start
#

## Assumptions
- Data schemas are relatively stable
- Validation rules can be defined declaratively
- Team has capacity to maintain quality checks
- Historical data is available for anomaly detection

## Compatibility
- Works with any SQL database
- Compatible with Python, SQL, and other data processing languages
- Framework-agnostic approach
- Adaptable to different data platforms

## Test Scenario Matrix
| Scenario | Test Case | Expected Outcome |
|----------|-----------|------------------|
| Null values | Check for nulls in required fields | Fail if nulls found |
| Duplicate records | Check uniqueness of primary keys | Fail if duplicates found |
| Invalid formats | Validate email, phone, date formats | Fail if format invalid |
| Out of range | Check numeric values within bounds | Fail if out of range |
| Referential integrity | Check foreign keys exist | Fail if orphaned records |
| Freshness | Check data recency | Fail if data too old |

## Technical Guardrails & Security Threat Model

### 1. Security & Privacy (Threat Model)
* **Top Threats**: Injection attacks, authentication bypass, data exposure
- [ ] **Data Handling**: Sanitize all user inputs to prevent Injection attacks. Never log raw PII
- [ ] **Secrets Management**: No hardcoded API keys. Use Env Vars/Secrets Manager
- [ ] **Authorization**: Validate user permissions before state changes

### 2. Performance & Resources
- [ ] **Execution Efficiency**: Consider time complexity for algorithms
- [ ] **Memory Management**: Use streams/pagination for large data
- [ ] **Resource Cleanup**: Close DB connections/file handlers in finally blocks

### 3. Architecture & Scalability
- [ ] **Design Pattern**: Follow SOLID principles, use Dependency Injection
- [ ] **Modularity**: Decouple logic from UI/Frameworks

### 4. Observability & Reliability
- [ ] **Logging Standards**: Structured JSON, include trace IDs `request_id`
- [ ] **Metrics**: Track `error_rate`, `latency`, `queue_depth`
- [ ] **Error Handling**: Standardized error codes, no bare except
- [ ] **Observability Artifacts**:
    - **Log Fields**: timestamp, level, message, request_id
    - **Metrics**: request_count, error_count, response_time
    - **Dashboards/Alerts**: High Error Rate > 5%


## Agent Directives
1. **Always validate** - Never skip validation for production data
2. **Fail on critical issues** - Don't continue with bad data
3. **Quarantine for analysis** - Preserve bad data for investigation
4. **Track metrics** - Monitor quality over time
5. **Iterate on rules** - Update rules based on incidents

## Definition of Done
Data quality implementation is complete when:

- [ ] Validation rules defined for all critical tables
- [ ] Validation integrated at all pipeline stages
- [ ] Quarantine process implemented
- [ ] Quality metrics tracked and visualized
- [ ] Alerting configured for quality degradation
- [ ] Team trained on validation framework
- [ ] Documentation complete and up-to-date
- [ ] Regular review schedule established
- [ ] Integration with incident response
- [ ] Continuous improvement process in place

## Anti-patterns
1. **Validating only at load** - Check at every stage
2. **Silent failures** - Always alert on validation failures
3. **Over-validating** - Too many checks cause alert fatigue
4. **Ignoring quarantine** - Never analyze quarantined data
5. **Static rules** - Rules must evolve with data

## Reference Links
#

## Versioning
This skill follows semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes to procedures or standards
- **MINOR**: New validation methods or significant enhancements
- **PATCH**: Bug fixes or documentation updates
