---
id: SKL-env-ENVDIAGNOSIS
name: Env Diagnosis
description: Environment diagnosis is systematic process of identifying and resolving
  issues in development environments before they block productivity. This skill provides
  checklists, automated scripts, and repai
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

# Env Diagnosis

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Environment diagnosis is systematic process of identifying and resolving issues in development environments before they block productivity. This skill provides checklists, automated scripts, and repair protocols for common environment problems including version mismatches, permission issues, port conflicts, and dependency conflicts.

**When to use this skill:** When experiencing environment issues, when setting up a new development environment, or when encountering "it works on my machine" problems.

---

## Why This Matters
- **<Benefit>**: <short explanation>
- **<Benefit>**: <short explanation>
- **<Benefit>**: <short explanation>

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

## Assumptions
- Developer has access to terminal
- Version managers (nvm, pyenv) are available
- Sufficient permissions to make changes

## Compatibility
- Works on Linux, macOS, Windows (with WSL)
- Language-agnostic diagnosis principles
- Can be adapted to different environments

---

## Test Scenario Matrix
| Scenario | Diagnosis | Fix | Notes |
|----------|-----------|-----|-------|
| Node version mismatch | Check `node --version` vs `.nvmrc` | Use `nvm install` | Requires nvm |
| Port in use | Check `lsof -i :<port>` | Kill process | Verify correct process |
| Permission denied | Check `ls -la` | Use `chown` | May need sudo |
| Dependency conflict | Check `npm ls` | Clean install | May need to clear cache |

---

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


## Definition of Done
- [ ] Diagnosis protocol documented
- [ ] Version checking procedures
- [ ] Permission diagnosis and fixes
- [ ] Port conflict resolution
- [ ] Dependency issue resolution
- [ ] Automated repair scripts
- [ ] Quick reference guide
- [ ] Common pitfalls documented
- [ ] Additional resources linked

---

## Anti-patterns / Pitfalls

* ⛔ **Don't**: Log PII, catch-all exception, N+1 queries
* ⚠️ **Watch out for**: Common symptoms and quick fixes
* 💡 **Instead**: Use proper error handling, pagination, and logging


## Reference Links
- [Node Version Manager (nvm)](https://github.com/nvm-sh/nvm)
- [Python Version Manager (pyenv)](https://github.com/pyenv/pyenv)
- [Docker Troubleshooting](https://docs.docker.com/engine/troubleshooting/)
- [Linux Permissions Guide](https://linuxjourney.com/lesson/file-permissions)

## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

