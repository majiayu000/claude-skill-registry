---
name: prp-generator
version: 1.0.0
description: Generate Product Requirements Planning (PRP) documents and comprehensive PRDs. Creates feature specifications, user stories, acceptance criteria, and technical requirements from natural language descriptions. Use when writing product requirements, creating feature specifications, or documenting product decisions.
---

# PRP Generator: Product Requirements Planning

Generate comprehensive Product Requirements Planning (PRP) documents, PRDs, and feature specifications from natural language descriptions.

## Triggers

Use this skill when:
- Writing product requirements documents (PRD)
- Creating feature specifications
- Documenting user stories and acceptance criteria
- Generating technical requirements
- Planning product features
- Keywords: PRP, PRD, product requirements, feature spec, user story, acceptance criteria, specification, requirements document

## Document Types

### PRP (Product Requirements Planning)

Full product planning document including:
- Vision and goals
- User personas
- Feature breakdown
- Success metrics
- Timeline estimates

### Feature Spec

Detailed specification for a single feature:
- User stories
- Acceptance criteria
- Technical requirements
- Edge cases
- Dependencies

### Issue Investigation (5 Whys)

Root cause analysis format:
- Problem statement
- 5 Whys analysis
- Root cause identification
- Solution proposals
- Fix validation plan

---

## PRP Document Template

```markdown
# PRP: [Feature/Product Name]

**Status:** Draft | In Review | Approved
**Author:** [Name]
**Created:** [Date]
**Last Updated:** [Date]

## Executive Summary

[2-3 sentences describing what this feature does and why it matters]

## Problem Statement

### Current State
[What is the current situation?]

### Pain Points
- [Pain point 1]
- [Pain point 2]

### Impact
[What happens if we don't solve this?]

## Goals & Success Metrics

### Primary Goal
[The main thing we're trying to achieve]

### Success Metrics
| Metric | Current | Target | Method |
|--------|---------|--------|--------|
| [Metric 1] | [Value] | [Value] | [How measured] |
| [Metric 2] | [Value] | [Value] | [How measured] |

## User Personas

### Primary: [Persona Name]
- **Role:** [Job title/role]
- **Goals:** [What they want to achieve]
- **Pain Points:** [Current frustrations]
- **Quote:** "[Representative quote]"

### Secondary: [Persona Name]
[Same format]

## User Stories

### Epic: [Epic Name]

#### Story 1: [Story Title]
**As a** [persona]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

**Priority:** P1 | P2 | P3
**Estimate:** S | M | L | XL

#### Story 2: [Story Title]
[Same format]

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-001 | System MUST [capability] | P1 | [Notes] |
| FR-002 | System MUST [capability] | P1 | [Notes] |
| FR-003 | System SHOULD [capability] | P2 | [Notes] |

## Non-Functional Requirements

| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-001 | Performance: [metric] | [target] | [Notes] |
| NFR-002 | Availability: [metric] | [target] | [Notes] |
| NFR-003 | Security: [requirement] | [standard] | [Notes] |

## Technical Considerations

### Architecture Impact
[How does this affect existing architecture?]

### Dependencies
- [Dependency 1]: [Status/Impact]
- [Dependency 2]: [Status/Impact]

### Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Strategy] |

## Out of Scope

- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

## Open Questions

- [ ] [Question 1]
- [ ] [Question 2]

## Timeline

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Design Complete | [Date] | Not Started |
| Development Complete | [Date] | Not Started |
| Testing Complete | [Date] | Not Started |
| Launch | [Date] | Not Started |

## Appendix

### Related Documents
- [Link to design doc]
- [Link to technical spec]

### Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial draft |
```

---

## Feature Spec Template

```markdown
# Feature Spec: [Feature Name]

**Parent PRP:** [Link if applicable]
**Status:** Draft | In Review | Approved
**Author:** [Name]
**Last Updated:** [Date]

## Overview

[1-2 paragraphs describing the feature]

## User Stories

### US-001: [Story Title]
**As a** [user type]
**I want to** [action]
**So that** [benefit]

#### Acceptance Criteria
- [ ] Given [precondition], when [action], then [outcome]
- [ ] Given [precondition], when [action], then [outcome]

#### Test Scenarios
1. **Happy Path:** [Description]
2. **Edge Case:** [Description]
3. **Error Case:** [Description]

### US-002: [Story Title]
[Same format]

## Requirements

### Functional
- **REQ-001:** [Requirement description]
- **REQ-002:** [Requirement description]

### Non-Functional
- **Performance:** [Requirement]
- **Security:** [Requirement]
- **Accessibility:** [Requirement]

## UI/UX Considerations

### User Flow
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Wireframes/Mockups
[Link or embed]

## Technical Design

### Components
- [Component 1]: [Purpose]
- [Component 2]: [Purpose]

### Data Model
[Entity descriptions or diagram link]

### API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/resource | Create resource |
| GET | /api/v1/resource/:id | Get resource |

## Edge Cases & Error Handling

| Scenario | Expected Behavior |
|----------|------------------|
| [Edge case 1] | [Behavior] |
| [Error case 1] | [Behavior] |

## Dependencies

- [Dependency 1]: [Impact/Status]
- [Dependency 2]: [Impact/Status]

## Out of Scope

- [Item 1]
- [Item 2]

## Implementation Tasks

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3
```

---

## Issue Investigation Template (5 Whys)

```markdown
# Issue Investigation: [Issue Title]

**Issue ID:** [GitHub/JIRA ID]
**Severity:** Critical | High | Medium | Low
**Status:** Investigating | Root Cause Found | Fix In Progress | Resolved
**Investigator:** [Name]
**Date:** [Date]

## Problem Statement

**What:** [Clear description of the problem]
**When:** [When did it start/when observed]
**Where:** [Where in the system]
**Impact:** [Who/what is affected]

## 5 Whys Analysis

### Why 1: Why did [problem] occur?
**Answer:** [First-level cause]
**Evidence:** [How we know this]

### Why 2: Why did [first cause] happen?
**Answer:** [Second-level cause]
**Evidence:** [How we know this]

### Why 3: Why did [second cause] happen?
**Answer:** [Third-level cause]
**Evidence:** [How we know this]

### Why 4: Why did [third cause] happen?
**Answer:** [Fourth-level cause]
**Evidence:** [How we know this]

### Why 5: Why did [fourth cause] happen?
**Answer:** [Root cause]
**Evidence:** [How we know this]

## Root Cause

[Summary of the true root cause]

## Contributing Factors

- [Factor 1]
- [Factor 2]

## Solution Proposals

### Option A: [Solution Name]
**Description:** [What this solution does]
**Pros:** [Benefits]
**Cons:** [Drawbacks]
**Effort:** S | M | L | XL
**Recommendation:** Recommended | Acceptable | Not Recommended

### Option B: [Solution Name]
[Same format]

## Recommended Solution

[Which option and why]

## Fix Validation Plan

### Pre-Fix State
- [Observable symptom 1]
- [Observable symptom 2]

### Validation Steps
1. [Step to verify fix]
2. [Step to verify fix]

### Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Rollback Plan
[How to revert if fix causes issues]

## Timeline

| Phase | Target | Status |
|-------|--------|--------|
| Investigation | [Date] | Complete |
| Fix Development | [Date] | In Progress |
| Testing | [Date] | Not Started |
| Deployment | [Date] | Not Started |

## Learnings & Prevention

### What We Learned
- [Learning 1]
- [Learning 2]

### Prevention Measures
- [ ] [Action to prevent recurrence]
- [ ] [Action to prevent recurrence]
```

---

## Generation Workflow

### From Natural Language

```
User: "I need a PRP for adding user authentication to our app"

1. Extract key concepts:
   - Feature: User authentication
   - Scope: Application-wide

2. Generate questions for clarification:
   - Auth methods? (email/password, OAuth, etc.)
   - User types?
   - Security requirements?

3. Generate document:
   - Fill template sections
   - Mark [NEEDS CLARIFICATION] for unknowns
   - Include reasonable defaults

4. Present for review
```

### From GitHub Issue

```python
# Read issue details
issue = gh_api_get_issue(owner, repo, issue_number)

# Parse into investigation template
investigation = {
    "problem_statement": issue.body,
    "issue_id": f"{owner}/{repo}#{issue_number}",
    "labels": issue.labels,
    "comments": issue.comments
}

# Generate 5 Whys starter
# User fills in during investigation
```

---

## Archon Integration

### Store PRP in Archon

```python
# Create as document
manage_document("create",
    project_id=PROJECT_ID,
    title="PRP: User Authentication",
    document_type="prp",
    content={
        "version": "1.0",
        "status": "draft",
        "sections": {
            "executive_summary": "...",
            "user_stories": [...],
            "requirements": [...]
        }
    },
    tags=["authentication", "security"]
)
```

### Generate Tasks from PRP

```python
# For each user story in PRP
for story in prp.user_stories:
    manage_task("create",
        project_id=PROJECT_ID,
        title=f"Implement: {story.title}",
        description=story.full_description,
        feature=story.epic,
        status="todo",
        task_order=story.priority_score
    )
```

---

## Command Reference

| Command | Description |
|---------|-------------|
| `/prp-generate <description>` | Generate PRP from description |
| `/prp-feature <description>` | Generate feature spec |
| `/prp-investigate <issue>` | Start 5 Whys investigation |
| `/prp-review` | Review current PRP for completeness |
| `/prp-to-tasks` | Convert PRP to Archon tasks |

---

## Best Practices

1. **Start with Problem**: Always define the problem clearly first
2. **User-Centric**: Write from user perspective, not technical
3. **Measurable Success**: Every goal needs a metric
4. **Reasonable Scope**: Define out-of-scope as clearly as in-scope
5. **Living Documents**: PRPs evolve - version and track changes
6. **Testable Criteria**: Acceptance criteria must be verifiable
7. **Cross-Reference**: Link related documents and issues

---

## Notes

- PRPs are planning documents, not technical specs
- Keep language accessible to non-technical stakeholders
- Use 5 Whys for bugs, PRPs for features
- Integration with Archon enables task generation
- Templates are starting points - adapt to your needs
