---
id: SKL-utm-UTMTRACKING
name: Utm Tracking
description: 'UTM (Urchin Tracking Module) parameters are tags added to URLs to track
  the effectiveness of marketing campaigns across various channels. They help identify
  where traffic is coming from and how users '
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

# Utm Tracking

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
UTM (Urchin Tracking Module) parameters are tags added to URLs to track the effectiveness of marketing campaigns across various channels. They help identify where traffic is coming from and how users interact with your content.

---

## Why This Matters
- **<Benefit>**: <short explanation>
- **<Benefit>**: <short explanation>
- **<Benefit>**: <short explanation>

## Core Concepts
#

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


## Anti-patterns
#

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure
