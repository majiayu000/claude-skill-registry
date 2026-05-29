---
id: SKL-owasp-OWASPTOP10
name: Owasp Top 10
description: The OWASP (Open Web Application Security Project) Top 10 is a standard
  awareness document representing a broad consensus about the most critical security
  risks to web applications. Updated every 3-4 y
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

# Owasp Top 10

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
The OWASP (Open Web Application Security Project) Top 10 is a standard awareness document representing a broad consensus about the most critical security risks to web applications. Updated every 3-4 years (2021 is the latest version), it provides a prioritized list of security risks and mitigation strategies. This skill covers all 10 vulnerability categories, their examples, prevention techniques, and testing methods.

## Why This Matters
- **Industry Standard**: Widely recognized security framework
- **Prioritization**: Focus on most critical risks
- **Compliance**: Required by many security standards (PCI DSS, SOC 2)
- **Education**: Learn common vulnerabilities and how to prevent them
- **Testing**: Guide for security testing and code reviews

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
  - Application code to review
  - Security requirements and threat model
  - OWASP Top 10 documentation
  - Security testing results (SAST, DAST, penetration testing)
  - Vulnerability database (CVE, NVD)
* **Entry Conditions**:
  - Understanding of web application architecture
  - Access to source code
  - Security testing tools available
  - Threat model for the application
* **Outputs**:
  - Security review findings
  - Vulnerability reports with severity ratings
  - Remediation recommendations
  - Code examples of secure implementations
  - Testing procedures and checklists
* **Artifacts Required (Deliverables)**:
  - Security review report with findings and recommendations
  - Code patches for identified vulnerabilities
  - Updated security coding guidelines
  - Test cases for security testing
  - OWASP Top 10 compliance checklist
* **Acceptance Evidence**:
  - All OWASP Top 10 categories reviewed
  - Vulnerabilities identified and classified by severity
  - Remediation code implemented
  - Security testing completed
  - Code reviewed for secure patterns
* **Success Criteria**:
  - No critical vulnerabilities (A01-A10) remain unaddressed
  - All user input validated
  - Authentication and authorization properly implemented
  - Cryptographic functions use strong algorithms
  - Security headers configured
  - Dependencies scanned and updated

## Skill Composition
* **Depends on**: [secure-coding](file://24-security-practices/secure-coding/), [penetration-testing](file://24-security-practices/penetration-testing/), [security-audit](file://24-security-practices/security-audit/)
* **Compatible with**: [secrets-management](file://24-security-practices/secrets-management/), [vulnerability-management](file://24-security-practices/vulnerability-management/), [incident-response](file://24-security-practices/incident-response/)
* **Conflicts with**: None
* **Related Skills**: [authentication-authorization](file://10-authentication-authorization/), [api-security](file://03-backend-api/api-security/)

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
