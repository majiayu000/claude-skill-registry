---
name: spec-authoring
description: "Expertise in writing clear, testable specifications. Activates when user discusses requirements, features, user stories, or acceptance criteria. Trigger keywords: specification, requirements, user story, acceptance criteria, feature spec, functional requirement, non-functional requirement, spec.md"
allowed-tools: Read, Write, Edit, Glob
user-invocable: false
---

# Spec Authoring Skill

## Purpose

This skill provides expertise in writing clear, testable, and structured specifications. It activates automatically when the user discusses requirements gathering, feature definitions, user stories, or acceptance criteria. The goal is to produce specification documents that are unambiguous, complete, and directly translatable into implementation tasks.

## When It Activates

The skill is triggered when the conversation involves:

- Drafting or refining a new specification document (`spec.md`)
- Defining functional requirements (FR) or non-functional requirements (NFR)
- Writing user stories or acceptance criteria
- Discussing feature scope, constraints, or success metrics
- Reviewing specification quality or completeness

## Capabilities

### 1. Structured Specification Generation

Generate specifications following a consistent template structure:

- **Overview**: Project context, goals, and scope boundaries
- **Functional Requirements**: Numbered as `FR-001`, `FR-002`, etc.
- **Non-Functional Requirements**: Numbered as `NFR-001`, `NFR-002`, etc.
- **Data Model**: Entity definitions, relationships, and constraints
- **API Contracts**: Endpoint definitions with request/response schemas
- **Success Metrics**: Measurable criteria for feature validation

### 2. Requirement Numbering

All requirements follow a strict numbering convention:

- Functional requirements: `FR-001`, `FR-002`, `FR-003`, ...
- Non-functional requirements: `NFR-001`, `NFR-002`, `NFR-003`, ...
- Each requirement is atomic, testable, and traceable to user stories

### 3. User Story Decomposition

Break down features into user stories using the standard format:

```
As a [role],
I want to [action],
So that [benefit].
```

Each user story is labeled (e.g., `US1`, `US2`) and linked to one or more functional requirements.

### 4. Acceptance Criteria (Given/When/Then)

Every user story includes acceptance criteria in Gherkin-style syntax:

```
Given [precondition],
When [action is performed],
Then [expected outcome].
```

Acceptance criteria serve as the contract between specification and implementation.

### 5. Quality Validation

Before finalizing a specification, the skill validates against a quality checklist to ensure completeness and clarity.

## Methodology

The spec authoring process follows a four-step pipeline:

1. **Read Project Context**: Examine existing project files, README, constitution, and prior specs to understand the domain, conventions, and constraints.
2. **Detect Tech Stack**: Identify the technology stack (languages, frameworks, databases) to tailor requirement language and feasibility assessments.
3. **Apply Spec Template**: Generate the specification document using the standard template, populating each section with requirements derived from user input.
4. **Validate Quality Criteria**: Run the quality checklist to flag missing sections, ambiguous language, untestable requirements, or orphaned user stories.

## Quality Checklist

Before a specification is considered complete, verify the following:

- [ ] Every functional requirement has a unique ID (`FR-XXX`)
- [ ] Every non-functional requirement has a unique ID (`NFR-XXX`)
- [ ] All user stories follow the `As a / I want / So that` format
- [ ] Every user story has at least one acceptance criterion in `Given/When/Then` format
- [ ] Requirements use precise, measurable language (no "should be fast" or "easy to use")
- [ ] Scope boundaries are explicitly defined (what is in scope vs. out of scope)
- [ ] Data model entities are defined with fields, types, and constraints
- [ ] API contracts specify HTTP methods, paths, request/response schemas, and error codes
- [ ] Success metrics are quantifiable and time-bound where applicable
- [ ] No orphaned requirements (every FR/NFR links to at least one user story)

## References

For detailed templates, criteria, and examples, consult the following reference files:

- `references/spec-template.md` -- The canonical specification template structure
- `references/quality-criteria.md` -- Full quality validation criteria and scoring rubric
- `references/examples.md` -- Annotated examples of well-written specifications
