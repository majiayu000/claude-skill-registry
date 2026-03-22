---
name: feature-plan
description: Plan feature implementation across services and workstreams by reading ARCHITECTURE.md and AGENTS.md, identifying affected areas, and producing an actionable Windsurf-friendly implementation plan.
---

# Feature Plan

Create an implementation plan before code changes begin.

## 1. Parse Requirements

Extract:

- Goal
- Requirements
- Acceptance criteria
- Constraints
- Out-of-scope items

## 2. Read Project Context

Read:

1. `ARCHITECTURE.md`
2. Root `AGENTS.md`
3. Relevant scoped `AGENTS.md`
4. Service configs and entry points if docs are incomplete

## 3. Build a Service Map

For each affected area, capture:

- Service or module
- Stack
- Responsibility
- Expected impact

Include infrastructure, schema, and documentation work if required.

## 4. Decompose Into Work Packages

Create self-contained work packages with:

- Title
- Scope
- Files likely to change
- Dependencies
- Acceptance criteria
- Complexity

Make cross-service dependencies explicit.

## 5. Assess Risk

Call out:

- API compatibility risk
- Migration risk
- Deployment-order risk
- Security risk
- Test coverage gaps

## 6. Present the Plan

Output:

- Goal
- Architecture impact
- Work packages
- Critical path
- Parallelizable work
- Risks

## 7. Handoff

The result should be directly executable by `feature-dev`.

If `FEATURES.md` exists, note whether it should be updated to reflect the planned work.

## Integration

- Input: PRD, design doc, ARD, ticket, or direct request
- Followed by: `feature-dev`
- Companion skills: `architecture`, `testing-procedures`, `context-engineering`