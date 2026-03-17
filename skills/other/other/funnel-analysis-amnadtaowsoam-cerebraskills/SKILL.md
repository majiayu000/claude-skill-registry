---
id: SKL-funnel-FUNNELANALYSIS
name: Funnel Analysis
description: Funnel analysis is the process of tracking user journeys through sequential
  steps to identify where users drop off and optimize conversion at each stage. Effective
  funnel analysis helps identify bottl
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

# Funnel Analysis

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Funnel analysis is the process of tracking user journeys through sequential steps to identify where users drop off and optimize conversion at each stage. Effective funnel analysis helps identify bottlenecks, optimize user flows, and improve overall conversion rates by measuring conversion rates, drop-off rates, and time-to-convert at each stage, enabling data-driven optimization of user experiences.

## Why This Matters
- **Identify Bottlenecks**: Find biggest drop-offs in user flows
- **Measure Conversion**: Track overall performance and stage-by-stage conversion
- **Optimize Stages**: Improve each step in the user journey
- **Compare Segments**: Find high-performing user groups
- **Measure Test Impact**: Quantify A/B test effectiveness on funnels
- **Reduce Friction**: Remove barriers that cause user abandonment

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
  - User journey events (page views, actions, conversions)
  - Funnel stage definitions
  - Time windows for analysis
  - Segmentation dimensions (device, channel, user type)
  - Baseline conversion rates
* **Entry Conditions**:
  - Event tracking implemented for all funnel stages
  - Funnel steps clearly defined
  - Sufficient data volume for meaningful analysis
  - Time periods specified
* **Outputs**:
  - Funnel analysis table with conversion/drop-off rates
  - Funnel visualization (chart, diagram)
  - Segmented funnel analysis
  - Bottleneck identification
  - Optimization recommendations
* **Artifacts Required (Deliverables)**:
  - Funnel SQL queries
  - Funnel visualization code
  - Funnel analysis report
  - Bottleneck documentation
  - Segmentation analysis
* **Acceptance Evidence**:
  - Funnel stages correctly defined
  - Conversion rates calculated accurately
  - Visualizations render correctly
  - Bottlenecks identified and prioritized
  - Segmentation analysis completed
* **Success Criteria**:
  - Funnel conversion rate > baseline (if applicable)
  - Biggest bottleneck identified with drop-off rate
  - Segmentation reveals high-performing groups
  - Visualization loads within performance budget
  - Insights lead to actionable optimization recommendations

## Skill Composition
* **Depends on**: [KPI Metrics](23-business-analytics/kpi-metrics/), [Conversion Optimization](23-business-analytics/conversion-optimization/)
* **Compatible with**: [Dashboard Design](23-business-analytics/dashboard-design/), [A/B Testing Analysis](23-business-analytics/ab-testing-analysis/)
* **Conflicts with**: None
* **Related Skills**: [kpi-metrics](23-business-analytics/kpi-metrics/), [conversion-optimization](23-business-analytics/conversion-optimization/), [dashboard-design](23-business-analytics/dashboard-design/)

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

