---
description: Write a comprehensive Product Requirements Document for a feature or initiative
disable-model-invocation: false
---

# Write PRD

Create a structured Product Requirements Document that aligns stakeholders and guides implementation.

## When to Use

- Starting a new feature or project
- Documenting requirements before development
- Creating alignment between product, design, and engineering
- Formalizing user feedback into actionable requirements

## Used By

- Product Manager (primary owner)
- Full-Stack Engineer (technical input)
- UI/UX Designer (design requirements)

---

## PRD Template

```markdown
# PRD: [Feature/Project Name]

**Author**: [Name]
**Status**: Draft | In Review | Approved
**Last Updated**: [Date]
**Version**: 1.0

---

## Executive Summary

[2-3 sentence summary of what we're building and why it matters]

---

## Problem Statement

### The Problem
[Clear description of the user/business problem]

### Who Has This Problem
- **Primary Users**: [User segment]
- **Secondary Users**: [Other affected users]
- **Frequency**: [How often does this problem occur]

### Impact
- **User Impact**: [How it affects users]
- **Business Impact**: [How it affects the business]

### Evidence
- [User research finding]
- [Support ticket data]
- [Analytics insight]

---

## Goals & Success Metrics

### Objective
[One clear objective this feature achieves]

### Key Results
1. **KR1**: [Measurable outcome] - Target: [X]
2. **KR2**: [Measurable outcome] - Target: [X]
3. **KR3**: [Measurable outcome] - Target: [X]

### Non-Goals
- [What we are explicitly NOT trying to do]
- [Scope boundaries]

---

## User Stories

### Primary Flow

**As a** [user type]
**I want to** [action/goal]
**So that** [benefit/outcome]

**Acceptance Criteria:**
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]

### Secondary Flows

[Additional user stories for edge cases, admin flows, etc.]

---

## Scope

### In Scope (MVP)
- [ ] [Feature/capability 1]
- [ ] [Feature/capability 2]
- [ ] [Feature/capability 3]

### Out of Scope (Future)
- [ ] [Explicitly excluded 1]
- [ ] [Explicitly excluded 2]

### Dependencies
- [External system/team dependency]
- [Technical prerequisite]

---

## Design & UX

### User Flow
[Description or link to user flow diagram]

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Wireframes/Mockups
[Links to design files or embedded images]

### Key Design Decisions
- **Decision 1**: [Choice made] - Rationale: [Why]
- **Decision 2**: [Choice made] - Rationale: [Why]

### Accessibility Requirements
- [ ] [WCAG requirement]
- [ ] [Keyboard navigation]
- [ ] [Screen reader support]

---

## Technical Requirements

### Architecture Overview
[High-level technical approach]

### Data Model Changes
[New entities, fields, relationships]

### API Design
[New endpoints or changes needed]

### Performance Requirements
- Load time: [Target]
- Throughput: [Target]
- Scalability: [Considerations]

### Security Considerations
- [Authentication requirements]
- [Data protection needs]
- [Compliance requirements]

---

## Analytics & Tracking

### Events to Track
| Event Name | Trigger | Properties |
|------------|---------|------------|
| [event] | [when] | [what data] |

### Success Dashboard
[Metrics to display and how to measure]

### Experiment Plan
[A/B tests or phased rollout approach]

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | H/M/L | H/M/L | [Strategy] |
| [Risk 2] | H/M/L | H/M/L | [Strategy] |

---

## Timeline & Milestones

### Phase 1: [Name]
- [Deliverable 1]
- [Deliverable 2]

### Phase 2: [Name]
- [Deliverable 1]
- [Deliverable 2]

### Key Dates
- Design Complete: [Date]
- Development Start: [Date]
- Beta Release: [Date]
- GA Release: [Date]

---

## Open Questions

- [ ] [Question 1] - Owner: [Name]
- [ ] [Question 2] - Owner: [Name]

---

## Appendix

### Related Documents
- [Link to design specs]
- [Link to technical specs]
- [Link to research]

### Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial draft |
```

---

## PRD Best Practices

### Writing Guidelines

1. **Lead with the problem, not the solution**
   - Start by deeply understanding and articulating the problem
   - Resist jumping to solutions until the problem is clear

2. **Be specific and measurable**
   - Avoid vague language like "improve" or "better"
   - Define concrete metrics and targets

3. **Keep it concise**
   - PRDs that are too long don't get read
   - Focus on what's essential for decision-making

4. **Show your work**
   - Include evidence for assertions
   - Link to research, data, or feedback

5. **Define what's NOT included**
   - Out of scope is as important as in scope
   - Prevents scope creep

### Common Mistakes to Avoid

- **Solutioning too early**: Define the problem first
- **Vague acceptance criteria**: Make them testable
- **Missing success metrics**: How will you know it worked?
- **Skipping edge cases**: Think about error states and failures
- **Ignoring accessibility**: Include from the start, not as afterthought

### Review Checklist

Before sharing the PRD:

- [ ] Problem statement is clear and evidence-backed
- [ ] User stories have testable acceptance criteria
- [ ] Scope is explicitly defined (in and out)
- [ ] Success metrics are measurable
- [ ] Technical approach has been validated with engineering
- [ ] Design requirements are specified
- [ ] Open questions are documented with owners
- [ ] Risks are identified with mitigations

---

## Quick Reference

### User Story Format
```
As a [user type]
I want to [action/goal]
So that [benefit/outcome]
```

### Acceptance Criteria Format
```
Given [context/precondition]
When [action/trigger]
Then [expected outcome]
```

### INVEST Criteria for Stories
- **I**ndependent: Can be developed separately
- **N**egotiable: Details can be discussed
- **V**aluable: Provides value to users
- **E**stimable: Can estimate effort
- **S**mall: Can complete in a sprint
- **T**estable: Can verify completion
