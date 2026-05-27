---
name: component-library-creator
category: codegen-scaffolding
description: Create design system with Storybook and theming.
---

# Component Library Creator

## Purpose
- Create design system with Storybook and theming.

## Preconditions
- Access to system context (repos, infra, environments)
- Confirmed requirements and constraints
- Required approvals for security, compliance, or governance

## Inputs
- Problem statement and scope
- Current architecture or system constraints
- Non-functional requirements (performance, security, compliance)
- Target stack and environment

## Outputs
- Design or implementation plan
- Required artifacts (diagrams, configs, specs, checklists)
- Validation steps and acceptance criteria

## Detailed Step-by-Step Procedures
1. Clarify scope, constraints, and success metrics.
2. Review current system state, dependencies, and integration points.
3. Select patterns, tools, and architecture options that match constraints.
4. Produce primary artifacts (docs/specs/configs/code stubs).
5. Validate against requirements and known risks.
6. Provide rollout and rollback guidance.

## Decision Trees and Conditional Logic
- If compliance or regulatory scope applies -> add required controls and audit steps.
- If latency budget is strict -> choose low-latency storage and caching.
- Else -> prefer cost-optimized storage and tiering.
- If data consistency is critical -> prefer transactional boundaries and strong consistency.
- Else -> evaluate eventual consistency or async processing.

## Error Handling and Edge Cases
- Partial failures across dependencies -> isolate blast radius and retry with backoff.
- Data corruption or loss risk -> enable backups and verify restore path.
- Limited access to systems -> document gaps and request access early.
- Legacy dependencies with limited change tolerance -> use adapters and phased rollout.

## Tool Requirements and Dependencies
- CLI and SDK tooling for the target stack
- Credentials or access tokens for required environments
- Diagramming or spec tooling when producing docs

## Stack Profiles
- Use Profile A, B, or C from `skills/STACK_PROFILES.md`.
- Note selected profile in outputs for traceability.

## Validation
- Requirements coverage check
- Security and compliance review
- Performance and reliability review
- Peer or stakeholder sign-off

## Rollback Procedures
- Revert config or deployment to last known good state.
- Roll back database migrations if applicable.
- Verify service health, data integrity, and error rates after rollback.

## Success Metrics
- Measurable outcomes (latency, error rate, uptime, cost)
- Acceptance thresholds defined with stakeholders

## Example Workflows and Use Cases
- Minimal: apply the skill to a small service or single module.
- Production: apply the skill to a multi-service or multi-tenant system.
