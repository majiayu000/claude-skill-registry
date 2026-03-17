---
name: prd
description: |
    Use when writing Product Requirements Documents that define what to build and why. Covers problem statements, goals/non-goals, user stories, success metrics, functional and non-functional requirements, milestones, prioritization frameworks, and the relationship to BRD and TRD.
    USE FOR: product requirements, feature specifications, user stories, success metrics, MoSCoW prioritization, RICE scoring, product roadmap items, feature acceptance criteria, stakeholder alignment documents
    DO NOT USE FOR: technical implementation details (use trd), business justification (use brd), architecture decisions (use adr), executable acceptance criteria (use gherkin)
license: MIT
metadata:
  displayName: "PRD (Product Requirements Document)"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Product Requirements Document — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Product_requirements_document"
---

# Product Requirements Document (PRD)

## Overview
A Product Requirements Document (PRD) defines *what* a product or feature should do and *why* it matters, without prescribing *how* to build it. It aligns product, engineering, design, and business stakeholders around a shared understanding of the problem, the proposed solution, success criteria, and scope boundaries.

The PRD sits between the BRD (business justification) and the TRD (technical design):
```
BRD ("Should we build this?") --> PRD ("What are we building?") --> TRD ("How do we build it?")
```

## Standard PRD Structure

### 1. Title and Metadata
```markdown
# PRD: [Feature/Product Name]

| Field          | Value                          |
|----------------|--------------------------------|
| Author         | [Name]                         |
| Status         | Draft / In Review / Approved   |
| Created        | YYYY-MM-DD                     |
| Last Updated   | YYYY-MM-DD                     |
| Reviewers      | [Names]                        |
| Approvers      | [Names]                        |
| Target Release | [Version / Quarter]            |
```

### 2. Problem Statement
Clearly articulate the problem from the user's perspective. Avoid solution language.

### 3. Goals and Non-Goals
Define what success looks like and explicitly state what is out of scope.

### 4. User Stories
Structured descriptions of desired functionality from the user's perspective.

### 5. Success Metrics
Quantifiable criteria that determine whether the feature achieved its goals.

### 6. Requirements
Functional requirements (what the system must do) and non-functional requirements (quality attributes).

### 7. Milestones and Timeline
Key deliverables and their target dates.

### 8. Open Questions
Unresolved decisions or unknowns that need answers before or during implementation.

## Complete PRD Template

```markdown
# PRD: [Feature/Product Name]

| Field          | Value                          |
|----------------|--------------------------------|
| Author         | [Name]                         |
| Status         | Draft / In Review / Approved   |
| Created        | YYYY-MM-DD                     |
| Last Updated   | YYYY-MM-DD                     |
| Reviewers      | [Names]                        |
| Approvers      | [Names]                        |
| Target Release | [Version / Quarter]            |

## Problem Statement

[Describe the problem from the user's perspective. What pain point exists?
What opportunity are we addressing? Include data or user research that
substantiates the problem. Avoid mentioning solutions here.]

## Goals

- [Goal 1: measurable outcome]
- [Goal 2: measurable outcome]
- [Goal 3: measurable outcome]

## Non-Goals

- [Explicitly state what is OUT of scope for this effort]
- [Things that might seem related but will not be addressed]
- [Features deferred to future iterations]

## User Stories

### Persona: [Persona Name]

As a [type of user],
I want [action/capability],
So that [benefit/value].

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Persona: [Persona Name]

As a [type of user],
I want [action/capability],
So that [benefit/value].

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Success Metrics

| Metric                | Current Baseline | Target       | Measurement Method       |
|-----------------------|------------------|--------------|--------------------------|
| [Metric 1]           | [Current value]  | [Target]     | [How you will measure]   |
| [Metric 2]           | [Current value]  | [Target]     | [How you will measure]   |
| [Metric 3]           | [Current value]  | [Target]     | [How you will measure]   |

## Functional Requirements

### FR-1: [Requirement Name]
**Priority:** Must Have / Should Have / Could Have / Won't Have
**Description:** [Detailed description of the requirement]

### FR-2: [Requirement Name]
**Priority:** Must Have / Should Have / Could Have / Won't Have
**Description:** [Detailed description of the requirement]

## Non-Functional Requirements

### NFR-1: Performance
[Response time, throughput, latency targets]

### NFR-2: Security
[Authentication, authorization, data protection requirements]

### NFR-3: Scalability
[Expected load, growth projections, scaling requirements]

### NFR-4: Accessibility
[WCAG compliance level, assistive technology support]

### NFR-5: Compatibility
[Browser, device, OS, API version requirements]

## Design and UX

[Link to design mockups, wireframes, or prototypes.
Describe key user flows and interaction patterns.]

## Milestones

| Milestone          | Target Date | Description                              |
|--------------------|-------------|------------------------------------------|
| Design Complete    | YYYY-MM-DD  | UX mockups approved                      |
| Alpha              | YYYY-MM-DD  | Core functionality implemented           |
| Beta               | YYYY-MM-DD  | Feature complete, internal testing        |
| GA                 | YYYY-MM-DD  | General availability                     |

## Dependencies

- [Dependency 1: external service, team, or infrastructure]
- [Dependency 2: other feature or project that must complete first]

## Risks and Mitigations

| Risk                          | Likelihood | Impact | Mitigation                    |
|-------------------------------|------------|--------|-------------------------------|
| [Risk 1]                     | High/Med/Low | High/Med/Low | [Mitigation strategy]   |
| [Risk 2]                     | High/Med/Low | High/Med/Low | [Mitigation strategy]   |

## Open Questions

- [ ] [Question 1 -- who owns answering this?]
- [ ] [Question 2 -- target date for resolution?]
- [ ] [Question 3]
```

## Writing Good User Stories

### The Standard Format
```
As a [persona/role],
I want [action or capability],
So that [business value or benefit].
```

### INVEST Criteria for User Stories
| Criterion | Meaning |
|-----------|---------|
| **I**ndependent | Can be developed and delivered independently of other stories |
| **N**egotiable | Details can be discussed and refined collaboratively |
| **V**aluable | Delivers clear value to the user or business |
| **E**stimable | Team can estimate the effort required |
| **S**mall | Can be completed within a single sprint |
| **T**estable | Has clear acceptance criteria that can be verified |

### Good vs Poor User Stories

**Poor (too vague):**
```
As a user, I want a better search so that I can find things.
```

**Good (specific and valuable):**
```
As a product catalog browser,
I want to filter search results by price range, category, and rating,
So that I can quickly find products that match my budget and preferences.

Acceptance Criteria:
- [ ] Filter panel displays on the search results page
- [ ] Price range filter supports min/max with a slider
- [ ] Category filter shows top-level categories with item counts
- [ ] Rating filter allows selecting minimum star rating (1-5)
- [ ] Filters can be combined (AND logic)
- [ ] Clearing all filters restores the full result set
- [ ] Filter selections persist across pagination
```

### Acceptance Criteria Formats

**Checklist format:**
```
Acceptance Criteria:
- [ ] User can upload files up to 50MB
- [ ] Supported formats: PDF, DOCX, XLSX, PNG, JPG
- [ ] Upload progress bar is displayed during upload
- [ ] Error message shown for unsupported file types
```

**Given/When/Then format (for complex scenarios):**
```
Acceptance Criteria:
- Given I am on the search results page
  When I set the price filter to $10-$50
  Then only products priced between $10 and $50 are displayed
```

## Prioritization Frameworks

### MoSCoW Method

| Priority | Meaning | Guideline |
|----------|---------|-----------|
| **Must Have** | Non-negotiable for launch | ~60% of effort |
| **Should Have** | Important but not critical | ~20% of effort |
| **Could Have** | Nice to have, low impact if omitted | ~20% of effort |
| **Won't Have** | Explicitly out of scope for this release | Documented for future |

Example:
```markdown
## Requirements by Priority

### Must Have
- FR-1: User registration and login
- FR-2: Product search with basic filters
- FR-3: Shopping cart and checkout
- NFR-1: Page load time < 3 seconds

### Should Have
- FR-4: Wishlist functionality
- FR-5: Order tracking dashboard
- NFR-2: Support for 3 languages

### Could Have
- FR-6: Product recommendation engine
- FR-7: Social sharing buttons

### Won't Have (this release)
- FR-8: Marketplace for third-party sellers
- FR-9: Mobile native app
```

### RICE Scoring

| Factor | Description | Scale |
|--------|-------------|-------|
| **R**each | How many users will this impact per quarter? | Number of users |
| **I**mpact | How much will this impact each user? | 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal |
| **C**onfidence | How confident are we in estimates? | 100% = high, 80% = medium, 50% = low |
| **E**ffort | How many person-months to complete? | Person-months |

**Formula:** `RICE Score = (Reach x Impact x Confidence) / Effort`

| Feature | Reach | Impact | Confidence | Effort | Score |
|---------|-------|--------|------------|--------|-------|
| Search filters | 5000 | 2 | 80% | 2 | 4000 |
| Wishlist | 2000 | 1 | 80% | 1 | 1600 |
| Recommendations | 5000 | 2 | 50% | 4 | 1250 |
| Social sharing | 1000 | 0.5 | 80% | 0.5 | 800 |

Higher RICE score = higher priority.

## Relationship to Other Documents

```
BRD (Business Requirements)
 |  Answers: "Should we build this? What is the business case?"
 |  Audience: Leadership, business stakeholders
 |
 v
PRD (Product Requirements)  <-- YOU ARE HERE
 |  Answers: "What are we building? For whom? What does success look like?"
 |  Audience: Product, engineering, design
 |
 +---> ADR (Architecture Decision Records)
 |     Records: "Why did we choose X over Y?"
 |
 v
TRD (Technical Requirements)
 |  Answers: "How do we build it? What are the technical constraints?"
 |  Audience: Engineering
 |
 v
Gherkin / Gauge (Executable Specs)
    Answers: "How do we verify it works?"
    Audience: QA, engineering, product
```

## Best Practices

- **Start with the problem, not the solution** -- clearly articulate the user pain point before proposing any feature.
- **Be specific about non-goals** -- explicitly stating what you will *not* build prevents scope creep and misaligned expectations.
- **Make success metrics measurable** -- "improve user experience" is not a metric. "Reduce checkout abandonment rate from 68% to 45%" is.
- **Write user stories from the user's perspective** -- avoid implementation language like "the system shall" in favor of "as a user, I want."
- **Include acceptance criteria for every user story** -- without testable criteria, it is impossible to know when a story is done.
- **Prioritize ruthlessly** -- use MoSCoW or RICE to force trade-off decisions early. Not everything can be "Must Have."
- **Keep the PRD living** -- update the document as requirements evolve. A stale PRD is worse than no PRD because it actively misleads.
- **Separate functional from non-functional requirements** -- performance, security, and scalability constraints deserve explicit attention.
- **Link to related documents** -- reference the BRD for business context, ADRs for architectural decisions, and the TRD for technical design.
- **Resolve open questions before development starts** -- open questions that linger into implementation cause rework and delays.
- **Review with all stakeholders** -- engineering, design, QA, and product should all review and approve the PRD before implementation begins.
