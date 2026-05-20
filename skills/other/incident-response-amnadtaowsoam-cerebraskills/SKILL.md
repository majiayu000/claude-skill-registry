---
id: SKL-incident-INCIDENTRESPONSE
name: Incident Response
description: Incident response is a systematic approach to handling security breaches
  and incidents to minimize damage, reduce recovery time, and prevent future occurrences.
  Effective incident response includes pr
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

# Incident Response

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Incident response is a systematic approach to handling security breaches and incidents to minimize damage, reduce recovery time, and prevent future occurrences. Effective incident response includes preparation, detection, containment, eradication, recovery, and lessons learned. This skill covers the complete incident response lifecycle, team roles, tools, communication strategies, and compliance requirements for organizations handling security incidents.

## Why This Matters
- **Faster Containment**: Reduce damage from hours to minutes with proper procedures
- **Evidence Preservation**: Enable root cause analysis and legal proceedings
- **Compliance**: Meet SOC2, ISO 27001, GDPR, PCI DSS requirements
- **Customer Trust**: Professional handling builds confidence during incidents
- **Cost Reduction**: Faster recovery equals less downtime cost and business impact

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
  - Security alerts and notifications
  - System logs and monitoring data
  - Threat intelligence feeds
  - Incident reports from users or systems
  - Legal and compliance requirements
* **Entry Conditions**:
  - Incident response plan documented
  - Incident response team identified and trained
  - Security monitoring tools deployed (SIEM, IDS/IPS, WAF)
  - Communication channels established
* **Outputs**:
  - Incident reports (executive summary, technical details, root cause analysis)
  - Timeline of incident and response actions
  - Lessons learned and improvement recommendations
  - Updated incident response procedures
  - Evidence collected and preserved
* **Artifacts Required (Deliverables)**:
  - Incident report with executive summary and technical details
  - Root cause analysis document
  - Timeline of events and actions
  - Evidence collection log
  - Lessons learned document with action items
  - Updated incident response plan
* **Acceptance Evidence**:
  - Incident contained within SLA (based on severity)
  - Services restored and verified
  - Evidence properly preserved and documented
  - Stakeholders notified appropriately
  - Root cause identified and documented
  - Lessons learned documented and action items assigned
* **Success Criteria**:
  - Incident response time meets SLA targets
  - Services restored with integrity verified
  - Evidence preserved for investigation
  - Stakeholders communicated transparently
  - Lessons learned documented and improvements implemented

## Skill Composition
* **Depends on**: [vulnerability-management](file://24-security-practices/vulnerability-management/), [security-audit](file://24-security-practices/security-audit/), [secrets-management](file://24-security-practices/secrets-management/)
* **Compatible with**: [secure-coding](file://24-security-practices/secure-coding/), [penetration-testing](file://24-security-practices/penetration-testing/), [monitoring-observability](file://14-monitoring-observability/)
* **Conflicts with**: None
* **Related Skills**: [owasp-top-10](file://24-security-practices/owasp-top-10/), [compliance-governance](file://12-compliance-governance/)

---

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

