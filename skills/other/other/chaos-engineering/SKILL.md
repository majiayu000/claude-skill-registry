---
id: SKL-chaos-CHAOSENGINEERING
name: Chaos Engineering
description: 'Chaos Engineering is the discipline of experimenting on a system to
  build confidence in its capability to withstand turbulent conditions in production.
  By proactively injecting failures, you discover '
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

# Chaos Engineering

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Chaos Engineering is the discipline of experimenting on a system to build confidence in its capability to withstand turbulent conditions in production. By proactively injecting failures, you discover weaknesses before they cause outages.

**Core Principle**: "Break things on purpose to learn how to make them stronger."

## Why This Matters
- **Proactive Discovery**: Find weaknesses before customers do
- **Confidence Building**: Verify that resilience patterns actually work
- **Cultural Shift**: Normalizes failure as expected, not exceptional
- **Reduced MTTR**: Practice recovery procedures under controlled conditions
- **Better Architecture**: Forces design for failure from the start

---

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
  - System architecture and component mapping
  - Steady state metrics (baseline)
  - Hypothesis to test
  - Blast radius configuration
* **Entry Conditions**:
  - System is in production with real traffic
  - Monitoring and alerting are operational
  - Rollback mechanisms are documented and tested
* **Outputs**:
  - Experiment report with findings
  - Updated monitoring dashboards
  - Action items for system improvements
* **Artifacts Required (Deliverables)**:
  - Experiment documentation (hypothesis, results, findings)
  - Metrics before/during/after experiment
  - Screenshots/graphs of system behavior
* **Acceptance Evidence**:
  - Test Report (screenshot/log)
  - Benchmark Result (latency, error rate)
  - Security Scan Report (if applicable)
* **Success Criteria**:
  - Hypothesis validated or disproven with data
  - System recovered to steady state within defined timeframe
  - No customer impact exceeding blast radius

## Skill Composition
* **Depends on**: Failure Modes Analysis (40-system-resilience/failure-modes)
* **Compatible with**: Postmortem Analysis, Monitoring & Observability
* **Conflicts with**: Production systems without monitoring/rollback capabilities
* **Related Skills**: 
  - [40-system-resilience/failure-modes](40-system-resilience/failure-modes/SKILL.md) - Understanding what to test
  - [40-system-resilience/postmortem-analysis](40-system-resilience/postmortem-analysis/SKILL.md) - Learning from experiments
  - [40-system-resilience/retry-timeout-strategies](40-system-resilience/retry-timeout-strategies/SKILL.md) - Testing retry behavior
  - [14-monitoring-observability/metrics-collection](14-monitoring-observability/metrics-collection/SKILL.md) - Measuring steady state

---

## Quick Start / Implementation Example

1. Review requirements and constraints
2. Set up development environment
3. Implement core functionality following patterns
4. Write tests for critical paths
5. Run tests and fix issues
6. Document any deviations or decisions

```python
# Example implementation following best practices
def example_function():
    # Your implementation here
    pass
```


## Assumptions / Constraints / Non-goals

* **Assumptions**:
  - Development environment is properly configured
  - Required dependencies are available
  - Team has basic understanding of domain
* **Constraints**:
  - Must follow existing codebase conventions
  - Time and resource limitations
  - Compatibility requirements
* **Non-goals**:
  - This skill does not cover edge cases outside scope
  - Not a replacement for formal training


## Compatibility & Prerequisites

* **Supported Versions**:
  - Python 3.8+
  - Node.js 16+
  - Modern browsers (Chrome, Firefox, Safari, Edge)
* **Required AI Tools**:
  - Code editor (VS Code recommended)
  - Testing framework appropriate for language
  - Version control (Git)
* **Dependencies**:
  - Language-specific package manager
  - Build tools
  - Testing libraries
* **Environment Setup**:
  - `.env.example` keys: `API_KEY`, `DATABASE_URL` (no values)


## Test Scenario Matrix (QA Strategy)

| Type | Focus Area | Required Scenarios / Mocks |
| :--- | :--- | :--- |
| **Unit** | Core Logic | Must cover primary logic and at least 3 edge/error cases. Target minimum 80% coverage |
| **Integration** | DB / API | All external API calls or database connections must be mocked during unit tests |
| **E2E** | User Journey | Critical user flows to test |
| **Performance** | Latency / Load | Benchmark requirements |
| **Security** | Vuln / Auth | SAST/DAST or dependency audit |
| **Frontend** | UX / A11y | Accessibility checklist (WCAG), Performance Budget (Lighthouse score) |


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


## Agent Directives & Error Recovery
*(ข้อกำหนดสำหรับ AI Agent ในการคิดและแก้ปัญหาเมื่อเกิดข้อผิดพลาด)*

- **Thinking Process**: Analyze root cause before fixing. Do not brute-force.
- **Fallback Strategy**: Stop after 3 failed test attempts. Output root cause and ask for human intervention/clarification.
- **Self-Review**: Check against Guardrails & Anti-patterns before finalizing.
- **Output Constraints**: Output ONLY the modified code block. Do not explain unless asked.


## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns / Pitfalls

* ⛔ **Don't**: Log PII, catch-all exception, N+1 queries
* ⚠️ **Watch out for**: Common symptoms and quick fixes
* 💡 **Instead**: Use proper error handling, pagination, and logging


## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

