---
id: SKL-dashboard-DASHBOARDDESIGN
name: Dashboard Design
description: A dashboard is a visual display of key metrics and data points that provides
  at-a-glance insights for monitoring, analysis, and decision-making. Effective dashboards
  present the right information at t
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

# Dashboard Design

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
A dashboard is a visual display of key metrics and data points that provides at-a-glance insights for monitoring, analysis, and decision-making. Effective dashboards present the right information at the right time, using appropriate visualizations and clear hierarchy to help users understand and act on data, saving time, improving decisions through data-driven insights, and increasing alignment through shared understanding.

## Why This Matters
- **Save Time**: Quick access to key information without manual data gathering
- **Improve Decisions**: Data-driven insights reduce reliance on intuition
- **Increase Alignment**: Shared understanding through consistent metrics and visualizations
- **Enable Action**: Identify issues and opportunities quickly
- **Monitor Performance**: Track real-time operational metrics
- **Communicate Status**: Share progress and results with stakeholders effectively

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
  - Business questions and goals
  - Key metrics and KPIs to display
  - Data sources (databases, APIs, analytics)
  - User personas and use cases
  - Brand guidelines and color palettes
* **Entry Conditions**:
  - Data sources accessible and reliable
  - Metrics clearly defined and calculated
  - Dashboard purpose and audience identified
  - Brand guidelines available
* **Outputs**:
  - Dashboard wireframe/mockup
  - Implemented dashboard with visualizations
  - Interactive features (filters, drill-downs)
  - Data queries and transformations
  - Documentation (metric definitions, user guide)
* **Artifacts Required (Deliverables)**:
  - Dashboard wireframe/design
  - Component library (reusable chart components)
  - Data queries/transformations
  - Dashboard implementation code
  - User documentation
  - Metric definitions document
* **Acceptance Evidence**:
  - Wireframe reviewed and approved
  - Dashboard loads within performance budget
  - All charts render correctly with test data
  - Interactive features work as specified
  - User acceptance testing completed
* **Success Criteria**:
  - Dashboard load time < 3s
  - All key metrics visible without scrolling
  - Interactive features responsive (< 500ms)
  - Mobile responsive design
  - Accessibility compliance (WCAG AA)
  - User satisfaction score > 4/5

## Skill Composition
* **Depends on**: [KPI Metrics](23-business-analytics/kpi-metrics/), [Data Visualization](23-business-analytics/data-visualization/)
* **Compatible with**: [Business Intelligence](23-business-analytics/business-intelligence/), [SQL for Analytics](23-business-analytics/sql-for-analytics/)
* **Conflicts with**: None
* **Related Skills**: [kpi-metrics](23-business-analytics/kpi-metrics/), [data-visualization](23-business-analytics/data-visualization/), [sql-for-analytics](23-business-analytics/sql-for-analytics/)

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

