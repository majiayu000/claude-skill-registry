---
name: architecture
description: Architecture workflow for producing architecture documentation, design records, API contracts, and implementation-facing system guidance from a feature request or analysis task.
---

# Architecture

Produce architecture deliverables without implementing code.

## 1. Classify the Request

Determine whether the task is:

- Feature design
- System analysis
- Cloud architecture
- CI/CD architecture
- Architecture evolution

## 2. Read Current Context

Read:

1. `ARCHITECTURE.md`
2. Root `AGENTS.md`
3. Relevant scoped `AGENTS.md`
4. Existing ADRs or API contracts

If docs are incomplete, inspect only the affected services and configs.

## 3. Define Constraints and NFRs

Capture only the categories that matter:

- Availability
- Latency
- Scalability
- Cost
- Security
- Observability
- Data integrity and recovery

## 4. Produce the Deliverable

Choose the smallest useful output:

- `ARCHITECTURE.md` update
- ADR
- API contract
- Service interaction diagram
- Migration plan

## 5. Validate

Check:

- Facts match the current codebase
- Component boundaries are explicit
- Tradeoffs are named
- Open questions are called out

## 6. Handoff

If implementation should follow, make the result directly consumable by `feature-plan` and `feature-dev`.