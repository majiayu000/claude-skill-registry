---
id: SKL-docker-DOCKERPATTERNS
name: Docker Patterns
description: Docker containerization provides consistent environments across development,
  testing, and production. This skill covers Dockerfile best practices, multi-stage
  builds, layer caching optimization, .dock
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

# Docker Patterns

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Docker containerization provides consistent environments across development, testing, and production. This skill covers Dockerfile best practices, multi-stage builds, layer caching optimization, .dockerignore, environment variables, health checks, security scanning, image optimization, common patterns (Node.js, Python, Go, React, Next.js), production Dockerfile examples, and best practices.

## Why This Matters
- **Consistency**: Same environment across development, testing, and production
- **Portability**: Run anywhere Docker is installed
- **Efficiency**: Multi-stage builds and layer caching reduce image size and build time
- **Security**: Scan images for vulnerabilities and use official base images

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
  - Application source code
  - Dockerfile for image definition
  - .dockerignore for build context optimization
  - Build dependencies (package.json, requirements.txt, go.mod)
  - Configuration files (nginx.conf, environment files)

* **Entry Conditions**:
  - Docker installed and running
  - Application code available
  - Dockerfile created
  - Build dependencies defined

* **Outputs**:
  - Optimized Docker image
  - Containerized application
  - Security scan reports
  - Health check status
  - Image pushed to registry

* **Artifacts Required (Deliverables)**:
  - Dockerfile with multi-stage build
  - .dockerignore file
  - Security scan configuration
  - Build scripts and Makefile
  - Documentation for image usage

* **Acceptance Evidence**:
  - Screenshot of `docker images` showing built image
  - Screenshot of `docker run` showing running container
  - Screenshot of security scan results
  - Screenshot of health check status

* **Success Criteria**:
  - Image builds successfully
  - Image size is optimized (Alpine base, multi-stage)
  - Security scan passes (no critical vulnerabilities)
  - Health check passes
  - Container starts and application is accessible

## Skill Composition
* **Depends on**: [docker-compose](./docker-compose/SKILL.md), [kubernetes-deployment](./kubernetes-deployment/SKILL.md)
* **Compatible with**: [ci-cd-github-actions](./ci-cd-github-actions/SKILL.md), [terraform-infrastructure](./terraform-infrastructure/SKILL.md)
* **Conflicts with**: None - Docker can coexist with other containerization tools
* **Related Skills**: [deployment-patterns](../../69-platform-engineering-lite/deployment-patterns/SKILL.md), [service-orchestration](./service-orchestration/SKILL.md)

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

