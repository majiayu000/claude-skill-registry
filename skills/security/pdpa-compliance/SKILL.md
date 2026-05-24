---
id: SKL-pdpa-PDPACOMPLIANCE
name: Pdpa Compliance
description: PDPA (Personal Data Protection Act) is Thailand's comprehensive data
  protection law that regulates how organizations collect, use, and store personal
  data. This skill provides patterns for implementin
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

# Pdpa Compliance

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
PDPA (Personal Data Protection Act) is Thailand's comprehensive data protection law that regulates how organizations collect, use, and store personal data. This skill provides patterns for implementing PDPA compliance across all aspects of data processing.

## Why This Matters
PDPA compliance is essential for:
- **Legal Requirements**: Mandatory for organizations processing personal data in Thailand
- **Risk Mitigation**: Avoiding fines up to 5 million THB
- **User Trust**: Demonstrating commitment to data protection
- **Market Access**: Enabling business in Thailand market
- **Brand Reputation**: Maintaining a positive public image

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


## Assumptions
- Organization processes personal data of Thai residents
- Consent can be obtained and tracked
- Data subject requests can be processed within time limits
- Data breach can be reported within required timeframe

## Compatibility
- PDPA B.E. 2562 compliant (Data Collection)
- PDPA B.E. 2563 compliant (Data Use)
- PDPA B.E. 2564 compliant (Data Security)
- PDPA B.E. 2565 compliant (Data Subject Rights)

---

## Test Scenario Matrix
| Scenario | Input | Expected Output | Priority |
|----------|-------|-----------------|----------|
| Check data classification | Data type | Classification details | P0 |
| Record consent | User ID, data type, purpose | Consent record created | P0 |
| Withdraw consent | User ID, data type | Consent marked as withdrawn | P0 |
| Submit access request | User ID | Request created and processed | P0 |
| Submit erasure request | User ID, reason | Request created and processed | P0 |
| Report breach | Breach details | Breach reported to PDPC | P0 |
| Check DPO requirement | Data type | Boolean result | P0 |

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


## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns
- **Pre-checked Consent**: Consent must be affirmative, not pre-checked
- **Bundled Consent**: Consent must be granular, not bundled
- **Hard to Withdraw**: Withdrawal must be as easy as giving consent
- **No Legal Basis**: Processing without documented legal basis
- **Ignoring DPO Requirements**: Not appointing DPO when required

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

