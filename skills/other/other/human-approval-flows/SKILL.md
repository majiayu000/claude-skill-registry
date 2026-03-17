---
id: SKL-human-HUMANAPPROVALFLOWS
name: Human Approval Flows
description: Human-in-the-Loop (HITL) workflows integrate human judgment into AI systems,
  ensuring that critical decisions receive human oversight while allowing automation
  for routine cases. HITL is essential for
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

# Human Approval Flows

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Human-in-the-Loop (HITL) workflows integrate human judgment into AI systems, ensuring that critical decisions receive human oversight while allowing automation for routine cases. HITL is essential for high-stakes applications and regulatory compliance.

**Core Principle**: "Automate the routine, escalate the exceptional. Humans and AI working together outperform either alone."

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
- Human reviewers have domain expertise
- Review capacity is sufficient for the workload
- Confidence scores are well-calibrated
- Reviewers have access to necessary context

## Compatibility
- Works with any AI/ML model that provides confidence scores
- Language-agnostic workflow patterns
- Can be integrated with existing review systems

---

## Test Scenario Matrix
| Scenario | Confidence | Expected Action | Notes |
|----------|-----------|-----------------|-------|
| Safe content | >0.95 | Auto-approve | High confidence, low risk |
| Moderate confidence | 0.80-0.95 | Async review | Queue for later review |
| Low confidence | 0.60-0.80 | Sync review | Immediate review required |
| Very low confidence | <0.60 | Manual handling | AI should not act |
| Critical domain | Any | Human review | Regulatory requirement |

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
- [ ] Confidence thresholds defined and documented
- [ ] Review queue implemented with prioritization
- [ ] SLA tracking and alerting in place
- [ ] Reviewer interface provides sufficient context
- [ ] Feedback loop for model improvement
- [ ] Metrics dashboard configured
- [ ] Load balancing implemented
- [ ] Escalation procedures documented
- [ ] Integration tests passing
- [ ] Documentation complete

---

## Anti-patterns / Pitfalls

* ⛔ **Don't**: Log PII, catch-all exception, N+1 queries
* ⚠️ **Watch out for**: Common symptoms and quick fixes
* 💡 **Instead**: Use proper error handling, pagination, and logging


## Reference Links
- [EU AI Act - Human Oversight Requirements](https://artificialintelligenceact.eu/)
- [GDPR - Automated Decision Making](https://gdpr.eu/article-22-automated-decision-making/)
- [Google's People + AI Guidebook](https://pair.withgoogle.com/)
- [Microsoft's Human-AI Interaction Guidelines](https://www.microsoft.com/en-us/research/project/guidelines-for-human-ai-interaction/)

---

## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

