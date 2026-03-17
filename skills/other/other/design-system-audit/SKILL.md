---
name: design-system-audit
description: Review design system usage and gaps
role_groups: [design, product]
jtbd: |
  Design systems drift and gaps appear. This scans projects for design system 
  mentions, identifies inconsistencies or gaps, suggests components to build, and 
  tracks adoption so your design system stays healthy and useful.
time_investment: "20-30 minutes per audit"
---

## Purpose

Audit design system health, identify gaps, and track adoption.

## Usage

- `/design-system-audit` - Full design system review

---

## Steps

1. **Scan for design system usage:**
   - Search 04-Projects/ for component mentions
   - Identify which components are used frequently
   - Find custom implementations (should use system)

2. **Identify gaps:**
   - Patterns appearing in multiple places
   - Requested components
   - Missing design system coverage

3. **Check consistency:**
   - Are teams using system components?
   - Custom implementations vs. system
   - Deviation from standards

4. **Track adoption:**
   - % of projects using design system
   - Common reasons for not using
   - Barriers to adoption

5. **Recommend improvements:**
   - Components to add
   - Documentation needs
   - Adoption initiatives

---

## Output Format

```markdown
# Design System Audit

**Date:** [Today]
**Projects reviewed:** [Count]

## Adoption Metrics
- Design system usage: [X]%
- Most used components: [List]

## Gaps Identified
1. [Pattern/Component needed] - Appears in [X] projects
2. [Gap description]

## Consistency Issues
- [Issue]: [Projects affected]

## Recommendations
1. Build [Component] - Priority: [High/Medium/Low]
2. [Recommendation]

## Roadmap Suggestions
- [Component] - Justification: [Why needed]
```
