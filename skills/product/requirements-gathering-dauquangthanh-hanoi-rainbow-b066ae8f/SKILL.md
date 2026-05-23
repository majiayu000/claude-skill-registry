---
name: requirements-gathering
description: Guides comprehensive requirements gathering and analysis including stakeholder interviews, user story creation, use case documentation, acceptance criteria, requirements prioritization, and traceability. Produces requirements documents, user stories, use cases, and development roadmaps. Use when gathering requirements, writing user stories, creating acceptance criteria, analyzing stakeholder needs, prioritizing features, or when users mention requirements analysis, business analysis, user stories, use cases, or requirements documentation.
---

# Requirements Gathering

## Overview

This skill guides you through systematic requirements gathering and documentation for software projects, from initial stakeholder analysis to detailed specifications and acceptance criteria.

## Requirements Gathering Workflow

## 1. Planning & Stakeholder Analysis

**Identify Stakeholders:**

- Map stakeholder categories: executives, users, developers, operations
- Assess influence, interest, and availability
- Plan engagement strategy for each stakeholder group

**Select Elicitation Techniques:**

- **Interviews**: One-on-one discussions for deep insights (see [elicitation-techniques.md](references/elicitation-techniques.md))
- **Workshops**: Collaborative sessions for alignment
- **Document Analysis**: Review existing systems and documentation
- **Observation**: Job shadowing to understand workflows
- **Surveys**: Gather input from large user groups
- **Prototyping**: Validate requirements with mockups

### 2. Requirements Elicitation

**Conduct Stakeholder Sessions:**

- Prepare structured interview questions
- Focus on current pain points and desired outcomes
- Document business context, goals, and constraints
- Capture exact quotes for later reference
- Follow up with clarifications as needed

**Key Questions to Ask:**

- What problems are you trying to solve?
- What does success look like?
- Who will use this system and how?
- What are your constraints (budget, timeline, technical)?
- What are must-have vs nice-to-have features?

### 3. Requirements Analysis & Documentation

**Document Requirements:**

Choose format based on project methodology:

**For Agile Projects** - Use user stories (see [agile-requirements.md](references/agile-requirements.md)):

```
As a [role]
I want [capability]
So that [business value]

Acceptance Criteria:
- Given [context]
- When [action]
- Then [outcome]
```

**For Traditional Projects** - Use structured specifications:

- Business Requirements Document (BRD): High-level business needs
- Functional Requirements: What system must do
- Non-Functional Requirements: Performance, security, usability
- Use Cases: Detailed user-system interactions

**Classify Requirements:**

- Functional vs Non-Functional
- Business vs Technical vs User
- Must-Have vs Should-Have vs Could-Have vs Won't-Have (MoSCoW)

### 4. Requirements Prioritization

**Apply Prioritization Framework** (see [prioritization-frameworks.md](references/prioritization-frameworks.md)):

- **MoSCoW**: Must/Should/Could/Won't have (good for stakeholder alignment)
- **Value vs Effort**: Plot on 2×2 matrix (quick wins vs long-term investments)
- **RICE**: Reach × Impact × Confidence / Effort (data-driven scoring)
- **Kano Model**: Basic/Performance/Delight features (user satisfaction focus)

### 5. Validation & Refinement

**Review Requirements Quality:**

- [ ] **Clear**: Unambiguous, easy to understand
- [ ] **Complete**: All necessary information included
- [ ] **Consistent**: No contradictions
- [ ] **Testable**: Can verify when implemented
- [ ] **Feasible**: Technically and economically viable
- [ ] **Traceable**: Linked to business goals

**Get Stakeholder Sign-Off:**

- Review with each stakeholder group
- Address conflicts and gaps
- Document approvals and changes
- Maintain requirements traceability matrix

## Key Deliverables

**Depending on project needs, produce:**

- **Stakeholder Analysis**: Categories, needs, engagement plan
- **Interview Summaries**: Key findings and quotes
- **User Stories/Use Cases**: Detailed functionality descriptions
- **Requirements Document**: BRD, SRS, or PRD
- **Requirements Traceability Matrix**: Links requirements to business goals, design, tests
- **Product Roadmap**: Prioritized feature timeline

## Reference Files

Load these on demand based on specific needs:

### Process Guidance

- **[elicitation-techniques.md](references/elicitation-techniques.md)** - Detailed interview techniques, workshop facilitation, and observation methods
- **[agile-requirements.md](references/agile-requirements.md)** - User story writing, backlog management, sprint planning, and acceptance criteria
- **[prioritization-frameworks.md](references/prioritization-frameworks.md)** - MoSCoW, RICE, Kano, Value/Effort frameworks with examples
- **[requirements-gathering-process.md](references/requirements-gathering-process.md)** - End-to-end process from initiation to sign-off
- **[best-practices.md](references/best-practices.md)** - Quality standards, common pitfalls, and validation checklists

### Documentation Templates

- **[requirements-traceability-matrix.md](references/requirements-traceability-matrix.md)** - Template and examples for tracking requirements
- **[use-case-overview.md](references/use-case-overview.md)** - Use case structure and examples

## Best Practices Summary

**Avoid Common Pitfalls:**

- ❌ Solution-focused: "Use React framework" → ✅ "Provide responsive web interface"
- ❌ Vague language: "System should be fast" → ✅ "System responds within 2 seconds for 95% of requests"
- ❌ Gold plating: Focus on business value, not nice-to-haves
- ❌ Assuming knowledge: Document all assumptions and define terms
- ❌ Skipping validation: Always review and get stakeholder sign-off

**Requirements Quality:**
Every requirement must be clear, complete, consistent, testable, feasible, necessary, prioritized, and traceable.
