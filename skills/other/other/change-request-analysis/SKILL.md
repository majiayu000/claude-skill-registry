---
name: change-request-analysis
description: Use when the Manager is creating, evaluating, or scoping change requests. Activates when writing CRs, assessing feature requests, estimating effort, analyzing impact, or deciding whether to approve a proposed change.
version: 1.0.0
---

# Change Request Analysis Expertise

## When This Applies

Apply this guidance when:
- Creating a new Change Request (CR)
- Evaluating the feasibility of a proposed change
- Estimating scope and effort
- Assessing risk and impact of changes

## CR Quality Checklist

Every Change Request should include:

1. **Clear Problem Statement** — What problem does this solve? Why now?
2. **Specific Requirements** — Measurable, testable acceptance criteria
3. **Scope Boundaries** — What is explicitly out of scope
4. **Impact Assessment** — Which components, APIs, or data are affected
5. **Priority Justification** — Why this priority level

## Scope Estimation

### Sizing Guide

| Scope | Description | Typical Tasks | Typical Duration |
|-------|-------------|---------------|------------------|
| **Small** | Single component change, no new APIs | 1-2 tasks | 1-2 sessions |
| **Medium** | Multiple components, possible new API | 3-5 tasks | 2-4 sessions |
| **Large** | System-wide change, new architecture | 6+ tasks | 5+ sessions |

### Scope Red Flags

Watch for CRs that should be broken down further:
- Touches more than 3 project directories
- Requires changes to both frontend and backend
- Needs database schema changes alongside feature work
- Has more than 5 distinct requirements
- Affects authentication or authorization flows

## Impact Analysis

Before finalizing a CR, assess:

1. **Breaking Changes** — Will this break existing functionality or APIs?
2. **Data Impact** — Are database migrations needed? Is data at risk?
3. **Dependency Impact** — Will other in-progress CRs be affected?
4. **Test Impact** — Do existing tests need updating?
5. **Infrastructure Impact** — Are deployment or config changes needed?

## CR Workflow

1. Draft the CR with all required fields
2. Set priority based on impact and urgency
3. Assign to Architect for technical design
4. Track through: `open` → `in_progress` → `completed` → `closed`
5. Don't create implementation tasks until Architect has designed the solution
