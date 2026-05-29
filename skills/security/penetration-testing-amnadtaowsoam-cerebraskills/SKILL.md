---
id: SKL-penetration-PENETRATIONTESTING
name: Penetration Testing
description: Penetration testing (pen testing) is a simulated cyber attack on your
  systems to identify vulnerabilities before malicious attackers do. It's ethical
  hacking with explicit permission. Effective penetr
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

# Penetration Testing

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Penetration testing (pen testing) is a simulated cyber attack on your systems to identify vulnerabilities before malicious attackers do. It's ethical hacking with explicit permission. Effective penetration testing includes planning, reconnaissance, exploitation, reporting, and remediation verification. This skill covers black box, white box, and gray box testing methodologies, common attack vectors, tools, and reporting standards.

## Why This Matters
- **Find vulnerabilities first**: Before attackers do
- **Test real-world scenarios**: Simulate actual attack techniques
- **Validate security investments**: Confirm controls work as expected
- **Meet compliance**: PCI DSS, SOC 2, HIPAA require regular testing
- **Reduce breach risk**: Proactive identification reduces exposure

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
  - Written authorization from system owner
  - Target systems and applications
  - Testing scope and rules of engagement
  - Threat model and risk assessment
  - Security requirements and compliance standards
* **Entry Conditions**:
  - Written authorization obtained
  - Testing scope clearly defined
  - Rules of engagement agreed upon
  - Testing tools and environment prepared
  - Incident response plan in place
* **Outputs**:
  - Penetration test report with findings
  - Vulnerability details and evidence
  - Risk ratings and impact assessment
  - Remediation recommendations
  - Proof of concept (PoC) exploits
  - Verification results after remediation
* **Artifacts Required (Deliverables)**:
  - Executive summary of findings
  - Technical vulnerability details
  - Evidence screenshots and logs
  - Risk assessment and ratings
  - Remediation recommendations
  - Proof of concept code or demonstrations
  - Testing methodology and timeline
* **Acceptance Evidence**:
  - All findings documented with severity ratings
  - Evidence preserved for verification
  - Vulnerabilities validated and reproducible
  - Remediation recommendations actionable
  - Report delivered to stakeholders
  - Scope respected throughout testing
* **Success Criteria**:
  - All high/critical vulnerabilities identified
  - Risk assessment completed with ratings
  - Remediation verified effective
  - Report comprehensive and actionable
  - Testing completed within agreed timeline
  - No systems taken offline during testing

## Skill Composition
* **Depends on**: [owasp-top-10](file://24-security-practices/owasp-top-10/), [vulnerability-management](file://24-security-practices/vulnerability-management/), [security-audit](file://24-security-practices/security-audit/)
* **Compatible with**: [incident-response](file://24-security-practices/incident-response/), [secrets-management](file://24-security-practices/secrets-management/), [secure-coding](file://24-security-practices/secure-coding/)
* **Conflicts with**: None
* **Related Skills**: [web-application-security](file://03-backend-api/web-application-security/), [api-security](file://03-backend-api/api-security/)

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
