---
name: prd-structure
description: When creating or reviewing Product Requirements Documents. Used by PM-AGENT.
version: 1.0.0
tokens: ~400
confidence: high
sources:
  - https://www.productplan.com/glossary/product-requirements-document/
  - https://www.atlassian.com/agile/product-management/requirements
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [product, prd, requirements, planning]
---

## When to Use
When creating or reviewing Product Requirements Documents. Used by PM-AGENT.

## Patterns

### PRD Essential Sections

**1. Problem Statement**
```markdown
## Problem
- Current state: {how it works today}
- Pain points: {specific issues}
- Impact: {quantified cost/time/frustration}
```

**2. Goals & Metrics**
```markdown
| Goal | Metric | Target |
|------|--------|--------|
| Reduce support tickets | Tickets/week | -30% |
| Improve conversion | Signup rate | +15% |
```

**3. Scope (MoSCoW)**
```markdown
## MVP (Must Have)
- Feature A
- Feature B

## Should Have (P1)
- Feature C

## Could Have (P2)
- Feature D

## Won't Have (Out of Scope)
- Feature X (reason)
```

**4. Requirements**
```markdown
## Functional Requirements
| ID | Requirement | Priority | AC |
|----|-------------|----------|-----|
| FR-01 | User can login | Must | Given/When/Then |

## Non-Functional Requirements
| ID | Category | Requirement | Target |
|----|----------|-------------|--------|
| NFR-01 | Performance | Response time | <200ms p95 |
```

## Anti-Patterns
- No measurable success criteria
- Scope without prioritization
- Requirements without acceptance criteria
- Missing constraints/assumptions
- No "out of scope" section

## Verification Checklist
- [ ] Problem quantified (not just described)
- [ ] Success metrics are measurable
- [ ] MoSCoW prioritization complete
- [ ] All requirements have AC
- [ ] Out of scope explicitly listed
- [ ] Assumptions documented
