---
name: writing-prds
description: Create Product Requirements Documents. Use when defining new features, projects, or initiatives. Covers user stories, acceptance criteria, and scope definition.
allowed-tools: Read, Write, Glob, Grep
---

# Writing PRDs

## Workflows

- [ ] **Define Goals**: Articulate business goals and success metrics
- [ ] **Identify Stakeholders**: List all relevant stakeholders
- [ ] **Draft User Stories**: Capture user needs
- [ ] **Detail Requirements**: List functional and non-functional requirements
- [ ] **Save Artifact**: Save to `./artifacts/prd_[feature].md`
- [ ] **Review**: Conduct stakeholder review

## PRD Structure

1. **Overview**: What and why
2. **Goals & Success Metrics**: How we measure success
3. **User Stories**: Who benefits and how
4. **Requirements**: What must be built
5. **Out of Scope**: What we're NOT building
6. **Timeline**: Key milestones

## User Story Format

```
As a [role],
I want [feature],
So that [benefit].
```

### Example
```
As a registered user,
I want to reset my password via email,
So that I can regain access to my account if I forget it.
```

## Acceptance Criteria

Use Given/When/Then format:

```
Given I am on the login page
When I click "Forgot Password"
Then I see a form to enter my email

Given I enter a valid registered email
When I submit the form
Then I receive a password reset email within 5 minutes
```

## INVEST Criteria

Good user stories are:
- **I**ndependent: Can be developed separately
- **N**egotiable: Details can be discussed
- **V**aluable: Delivers user value
- **E**stimable: Can be sized
- **S**mall: Fits in a sprint
- **T**estable: Has clear acceptance criteria

## Resources

- [PRD Template](./resources/prd.template.md)
