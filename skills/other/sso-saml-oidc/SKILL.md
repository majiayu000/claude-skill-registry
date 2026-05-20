---
id: SKL-sso-SSOSAMLOIDC
name: Sso Saml Oidc
description: 'Single Sign-On (SSO) enables users to authenticate once and access multiple
  applications. This skill covers implementing SSO with SAML 2.0 (enterprise standard)
  and OpenID Connect (OIDC, modern OAuth '
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

# Sso Saml Oidc

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Single Sign-On (SSO) enables users to authenticate once and access multiple applications. This skill covers implementing SSO with SAML 2.0 (enterprise standard) and OpenID Connect (OIDC, modern OAuth 2.0-based) for enterprise authentication, including JIT provisioning, group/role mapping, and multi-tenancy support.

## Why This Matters
- **Enterprise Requirement**: SSO is mandatory for most enterprise deals
- **Security**: Centralized authentication with MFA enforcement
- **User Experience**: No password fatigue, seamless access to all apps
- **Operational Efficiency**: Automated onboarding/offboarding through IdP

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
  - SAML assertion (signed XML)
  - OIDC ID token (JWT)
  - IdP metadata (SAML) or discovery endpoint (OIDC)
  - Client credentials (client_id, client_secret)
* **Entry Conditions**:
  - Database initialized with users table
  - SSO/OIDC library installed
  - IdP configuration available
* **Outputs**:
  - Authenticated user session
  - User attributes (email, name, groups)
  - User roles mapped from groups
  - JWT session token (optional)
* **Artifacts Required (Deliverables)**:
  - SAML/OIDC authentication endpoints
  - Metadata exchange implementation
  - JIT provisioning logic
  - Group/role mapping configuration
  - Session management (secure cookies)
* **Acceptance Evidence**:
  - Successful SSO login with test accounts
  - User attributes correctly mapped
  - Group/role mapping working
  - Session properly secured (httpOnly, secure)
* **Success Criteria**:
  - SSO login works with at least 3 IdPs (Okta, Azure AD, Google)
  - OIDC login works with Google, Auth0
  - JIT provisioning creates/updates users
  - Group/role mapping assigns correct roles
  - Session is secure (httpOnly, SameSite)

## Skill Composition
* **Depends on**: Database Design, Session Management
* **Compatible with**: SCIM Provisioning, Enterprise RBAC Models, Security Questionnaires
* **Conflicts with**: None
* **Related Skills**: [SCIM Provisioning](file://50-enterprise-integrations/scim-provisioning/SKILL.md), [Enterprise RBAC Models](file://50-enterprise-integrations/enterprise-rbac-models/SKILL.md)

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

