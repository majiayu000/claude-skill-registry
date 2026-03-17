---
id: SKL-runbooks-RUNBOOKSOPS
name: Runbooks Ops
description: Runbooks are documented procedures for operational tasks, incident response,
  and troubleshooting. Essential for maintaining reliable systems and enabling team
  members to handle issues independently.
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

# Runbooks Ops

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Runbooks are documented procedures for operational tasks, incident response, and troubleshooting. Essential for maintaining reliable systems and enabling team members to handle issues independently.

## Why This Matters
- **Faster resolution**: Step-by-step guides reduce MTTR
- **Consistency**: Same procedure every time
- **Knowledge sharing**: Reduce bus factor
- **Onboarding**: New team members can handle ops tasks

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
- Production environment with Kubernetes
- PostgreSQL database
- AWS cloud infrastructure
- PagerDuty for alerting
- Slack for team communication
- Git for version control

## Compatibility
- **Kubernetes**: 1.20+
- **PostgreSQL**: 12+
- **AWS CLI**: 2.0+
- **PagerDuty API**: Latest
- **Slack API**: Latest

## Test Scenario Matrix
| Scenario | Input | Expected Output | Verification |
|----------|-------|-----------------|--------------|
| Service down incident | Alert notification | Runbook executed, service restored | Incident report |
| Production deployment | New version | Deployment successful, no issues | Smoke tests pass |
| High database CPU | CPU alert | Query identified and resolved | CPU returns to normal |
| Database backup | Scheduled job | Backup created and uploaded | S3 verification |
| On-call handoff | Shift change | Handoff notes documented | Next engineer confirms |

## Technical Guardrails
#

## Agent Directives & Error Recovery
*(ข้อกำหนดสำหรับ AI Agent ในการคิดและแก้ปัญหาเมื่อเกิดข้อผิดพลาด)*

- **Thinking Process**: Analyze root cause before fixing. Do not brute-force.
- **Fallback Strategy**: Stop after 3 failed test attempts. Output root cause and ask for human intervention/clarification.
- **Self-Review**: Check against Guardrails & Anti-patterns before finalizing.
- **Output Constraints**: Output ONLY the modified code block. Do not explain unless asked.


## Definition of Done
A runbook is complete when:

- [ ] Follows standard template structure
- [ ] Has clear overview and when-to-use sections
- [ ] Lists all prerequisites and required access
- [ ] Provides step-by-step procedures
- [ ] Includes copy-paste ready commands
- [ ] Documents expected outputs
- [ ] Has verification steps
- [ ] Includes rollback procedures
- [ ] Specifies escalation paths
- [ ] Links to related runbooks
- [ ] Has owner and last updated date
- [ ] Has been tested in staging

## Anti-patterns
1. **Outdated runbooks**: Procedures that don't match current system
2. **Missing steps**: Skipping important verification or rollback steps
3. **Vague instructions**: Not specific enough to follow without guessing
4. **No owner**: Unclear who maintains the runbook
5. **Untested procedures**: Runbooks that haven't been validated
6. **Missing context**: Not explaining why steps matter
7. **No escalation**: Unclear when to escalate and to whom
8. **Copy-paste errors**: Commands that don't work as written

## Reference Links
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [PagerDuty Documentation](https://support.pagerduty.com/)
- [Incident Response Best Practices](https://sre.google/sre-book/postmortem-culture/)

## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

