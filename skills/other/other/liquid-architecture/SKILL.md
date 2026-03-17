---
id: SKL-liquid-LIQUIDARCHITECTURE
name: Liquid Architecture
description: Liquid Architecture enables the AI system to modify and optimize its
  own codebase in real-time without human intervention. This God-Mode protocol allows
  the agent to analyze, refactor, and improve cod
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

# Liquid Architecture

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Liquid Architecture enables the AI system to modify and optimize its own codebase in real-time without human intervention. This God-Mode protocol allows the agent to analyze, refactor, and improve code dynamically, adapting to new requirements and fixing bugs autonomously. The system uses LLM-powered code analysis, AST manipulation, and runtime instrumentation to achieve continuous self-improvement.

## Why This Matters
- **Autonomous Evolution**: System can improve itself without human intervention
- **Rapid Adaptation**: Respond to new requirements in real-time
- **Continuous Improvement**: Always optimizing code for better performance
- **Self-Healing**: Automatically detect and fix bugs
- **Knowledge Accumulation**: Learn from past modifications to improve future decisions

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
  - Codebase to analyze and modify
  - Performance metrics and profiling data
  - Change requirements and objectives
  - Safety constraints and approval requirements
  - Runtime instrumentation and monitoring data
* **Entry Conditions**:
  - Codebase is accessible and analyzable
  - LLM with code analysis capabilities is available
  - Runtime instrumentation is deployed
  - Safety validation mechanisms are in place
* **Outputs**:
  - Modified code files with applied changes
  - Performance improvement metrics
  - Rollback plans if needed
  - Change logs and audit trails
* **Artifacts Required (Deliverables)**:
  - Modified source code
  - Diff files showing changes
  - Performance comparison reports
  - Validation and test results
* **Acceptance Evidence**:
  - Code modifications improve performance or fix bugs
  - Changes pass all validation checks
  - System remains stable during and after modifications
  - Rollback is available if needed
* **Success Criteria**:
  - Modification success rate: ≥95%
  - Performance improvement: ≥10% for targeted areas
  - System uptime: ≥99.9% during hot reload
  - Rollback success rate: 100%

## Skill Composition
* **Depends on**: [`algorithmic-self-discovery`](000-GOD-MODE-PROTOCOL/algorithmic-self-discovery/SKILL.md), [`cognitive-governance`](000-GOD-MODE-PROTOCOL/cognitive-governance/SKILL.md)
* **Compatible with**: [`self-validation-cicd`](00-meta-skills/self-validation-cicd/SKILL.md), [`skill-generator`](00-meta-skills/skill-generator/SKILL.md)
* **Conflicts with**: [`code-review`](01-foundations/code-review/SKILL.md) (manual review vs self-modification)
* **Related Skills**: [`system-thinking`](00-meta-skills/system-thinking/SKILL.md), [`refactoring-strategies`](01-foundations/refactoring-strategies/SKILL.md)

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

