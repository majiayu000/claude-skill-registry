---
id: SKL-advanced-ADVANCEDIACIOT
name: Advanced Iac Iot
description: Advanced Infrastructure as Code (IaC) for IoT enables automated, reproducible,
  and scalable infrastructure management across distributed IoT environments. This
  skill encompasses Terraform for infrastr
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

# Advanced Iac Iot

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Advanced Infrastructure as Code (IaC) for IoT enables automated, reproducible, and scalable infrastructure management across distributed IoT environments. This skill encompasses Terraform for infrastructure provisioning, Ansible for configuration management, and GitOps for continuous deployment, ensuring consistent infrastructure across thousands of edge devices and cloud resources.

## Why This Matters
- **Scalability**: Manage thousands of IoT devices programmatically
- **Consistency**: Ensure identical infrastructure across environments
- **Reproducibility**: Recreate infrastructure from version-controlled code
- **Speed**: Deploy infrastructure in minutes instead of days
- **Reliability**: Reduce human error through automation

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
  - Infrastructure specifications (VPC, subnets, gateways)
  - Configuration parameters (firmware, locations, deployment ID)
  - Git repository URLs and credentials
* **Entry Conditions**:
  - Cloud account configured with appropriate permissions
  - Git repository initialized
  - CI/CD pipeline configured
* **Outputs**:
  - Provisioned infrastructure resources
  - Configured IoT devices
  - Deployed applications
  - State files and outputs
* **Artifacts Required (Deliverables)**:
  - Terraform modules and configurations
  - Ansible playbooks and inventories
  - ArgoCD application manifests
  - Helm charts
* **Acceptance Evidence**:
  - Terraform plan shows no changes
  - Ansible playbook completes successfully
  - ArgoCD applications synced
  - Infrastructure resources provisioned
* **Success Criteria**:
  - Deployment time < 10 minutes
  - Configuration drift 0%
  - Success rate > 99%
  - Rollback time < 5 minutes
  - Compliance 100%

## Skill Composition
* **Depends on**: [Hardware Rooted Identity](../74-iot-zero-trust-security/hardware-rooted-identity/SKILL.md)
* **Compatible with**: [Chaos Engineering for IoT](../76-iot-infrastructure/chaos-engineering-iot/SKILL.md), [GitOps for IoT Infrastructure](../76-iot-infrastructure/gitops-iot-infrastructure/SKILL.md)
* **Conflicts with**: Manual infrastructure management
* **Related Skills**: [Chaos Engineering for IoT](../76-iot-infrastructure/chaos-engineering-iot/SKILL.md), [GitOps for IoT Infrastructure](../76-iot-infrastructure/gitops-iot-infrastructure/SKILL.md), [Multi-Cloud IoT Strategy](../76-iot-infrastructure/multi-cloud-iot/SKILL.md)

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

