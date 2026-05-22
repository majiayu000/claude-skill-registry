---
id: SKL-docker-DOCKERCOMPOSE
name: Docker Compose
description: Docker Compose is a tool for defining and running multi-container Docker
  applications. This skill covers Compose file structure, services definition, networks,
  volumes, environment variables, dependen
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

# Docker Compose

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Docker Compose is a tool for defining and running multi-container Docker applications. This skill covers Compose file structure, services definition, networks, volumes, environment variables, dependencies (depends_on), health checks, development setup, production considerations, common stacks (PERN, FastAPI, microservices), and best practices.

## Why This Matters
- **Simplified Orchestration**: Define multi-container applications in a single YAML file
- **Development Experience**: Quick startup, hot reload, and easy debugging
- **Consistency**: Same configuration works across development and production
- **Portability**: Run anywhere Docker is installed without complex setup

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
  - Docker Compose file (docker-compose.yml)
  - Dockerfile for custom builds
  - Application code and configuration
  - Environment variables and secrets
  - Volume definitions for persistent data

* **Entry Conditions**:
  - Docker and Docker Compose installed
  - Application has Dockerfile or uses existing images
  - Configuration files available
  - Sufficient disk space for volumes

* **Outputs**:
  - Running multi-container application
  - Exposed services on host ports
  - Persistent data in volumes
  - Networked services for communication
  - Health status of services

* **Artifacts Required (Deliverables)**:
  - docker-compose.yml file
  - Dockerfile for custom builds
  - Environment configuration files (.env)
  - Volume definitions
  - Documentation for service architecture

* **Acceptance Evidence**:
  - Screenshot of `docker-compose ps` showing running services
  - Screenshot of application accessible in browser
  - Screenshot of volume data persistence
  - Screenshot of health check status

* **Success Criteria**:
  - All services start successfully
  - Services communicate via networks
  - Data persists in volumes after restart
  - Health checks pass for all services
  - Application is accessible on configured ports

## Skill Composition
* **Depends on**: [docker-patterns](./docker-patterns/SKILL.md), [kubernetes-deployment](./kubernetes-deployment/SKILL.md)
* **Compatible with**: [ci-cd-github-actions](./ci-cd-github-actions/SKILL.md), [terraform-infrastructure](./terraform-infrastructure/SKILL.md)
* **Conflicts with**: None - Docker Compose can coexist with other orchestration tools
* **Related Skills**: [service-orchestration](./service-orchestration/SKILL.md), [deployment-patterns](../../69-platform-engineering-lite/deployment-patterns/SKILL.md)

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

