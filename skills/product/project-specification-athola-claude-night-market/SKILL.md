---
name: project-specification
description: Transform project brief into detailed, testable specifications using spec-driven development methodology

Triggers: specification, testable, development, spec-driven, project
model_preference: claude-sonnet-4
---
## Table of Contents

- [When to Use](#when-to-use)
- [Integration](#integration)
- [Specification Structure](#specification-structure)
- [1. Overview Section](#1-overview-section)
- [2. Functional Requirements (FR-XXX)](#2-functional-requirements-(fr-xxx))
- [FR-001: [Requirement Name]](#fr-001:-[requirement-name])
- [3. Non-Functional Requirements (NFR-XXX)](#3-non-functional-requirements-(nfr-xxx))
- [NFR-001: [Category] - [Requirement]](#nfr-001:-[category]---[requirement])
- [4. Technical Constraints](#4-technical-constraints)
- [5. Out of Scope](#5-out-of-scope)
- [Out of Scope (v1.0)](#out-of-scope-(v10))
- [Clarification Workflow](#clarification-workflow)
- [Ambiguity Detection](#ambiguity-detection)
- [Question Generation](#question-generation)
- [Clarification Session](#clarification-session)
- [Quality Checks](#quality-checks)
- [Output Format](#output-format)
- [Change History](#change-history)
- [Overview](#overview)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [Technical Constraints](#technical-constraints)
- [Out of Scope](#out-of-scope)
- [Dependencies](#dependencies)
- [Acceptance Testing Strategy](#acceptance-testing-strategy)
- [Success Criteria](#success-criteria)
- [Glossary](#glossary)
- [References](#references)
- [Acceptance Criteria Patterns](#acceptance-criteria-patterns)
- [Given-When-Then](#given-when-then)
- [Error Cases](#error-cases)
- [Performance Criteria](#performance-criteria)
- [Security Criteria](#security-criteria)
- [Related Skills](#related-skills)
- [Related Commands](#related-commands)
- [Examples](#examples)


# Project Specification Skill

Transform project briefs into structured, testable specifications with acceptance criteria.

## When to Use

- After brainstorming phase completes
- Have project brief but need detailed requirements
- Need testable acceptance criteria for implementation
- Planning validation and testing strategy

## Integration

**With spec-kit**:
- Delegates to `Skill(spec-kit:spec-writing)` for methodology
- Uses spec-kit templates and validation
- Enables clarification workflow

**Without spec-kit**:
- Standalone specification framework
- Requirement templates
- Acceptance criteria patterns

## Specification Structure

### 1. Overview Section

- **Purpose**: What the project achieves (1-2 sentences)
- **Scope**: IN/OUT boundaries
- **Stakeholders**: Who cares and why

### 2. Functional Requirements (FR-XXX)

**Format per requirement**:
```markdown
### FR-001: [Requirement Name]

**Description**: Clear, unambiguous description

**Acceptance Criteria**:
- [ ] Given [context], when [action], then [expected result]
- [ ] Given [context], when [action], then [expected result]

**Priority**: High | Medium | Low
**Dependencies**: FR-002, FR-005
**Estimated Effort**: S | M | L | XL
```
**Verification:** Run the command with `--help` flag to verify availability.

**Validation Rules**:
- Description has no ambiguous words (might, could, maybe, probably)
- At least 2 acceptance criteria (happy path + error case)
- Criteria use Given-When-Then format
- Criteria are testable (observable outcomes)
- Dependencies are explicit

### 3. Non-Functional Requirements (NFR-XXX)

**Categories**:
- **Performance**: Response times, throughput, resource limits
- **Security**: Authentication, authorization, data protection, compliance
- **Reliability**: Uptime, error handling, recovery, fault tolerance
- **Usability**: UX requirements, accessibility, documentation
- **Maintainability**: Code quality, testing, observability

**Format**:
```markdown
### NFR-001: [Category] - [Requirement]

**Requirement**: [Specific, measurable requirement]

**Measurement**: [How to verify]
- Metric: [What to measure]
- Target: [Specific threshold]
- Tool: [How to measure]

**Priority**: Critical | High | Medium | Low
```
**Verification:** Run the command with `--help` flag to verify availability.

### 4. Technical Constraints

- Technology stack selections with rationale
- Integration requirements
- Data requirements (schema, migrations)
- Deployment constraints
- Regulatory/compliance requirements

### 5. Out of Scope

**Explicit exclusions** to prevent scope creep:
```markdown
## Out of Scope (v1.0)

- [Feature explicitly NOT included]
- [Capability deferred to later version]
- [Integration not planned]

**Rationale**: [Why these are excluded]
```
**Verification:** Run the command with `--help` flag to verify availability.

## Clarification Workflow

### Ambiguity Detection

Scan specification for:
- Vague quantifiers (many, few, several, most)
- Ambiguous terms (user-friendly, fast, scalable)
- Missing dependencies
- Untestable criteria
- Conflicting requirements

### Question Generation

For each ambiguity:
```markdown
**Question [N]**: [Reference to FR/NFR]

**Ambiguity**: [What is unclear]

**Impact**: [Why this matters]

**Options**:
- Option A: [Interpretation 1]
- Option B: [Interpretation 2]

**Recommendation**: [Preferred option with rationale]
```
**Verification:** Run the command with `--help` flag to verify availability.

### Clarification Session

Run interactive Q&A:
1. Present all questions
2. Gather stakeholder responses
3. Update specification
4. Re-validate for new ambiguities
5. Iterate until clear

## Quality Checks

Before completing specification:

- ✅ All requirements have unique IDs (FR-XXX, NFR-XXX)
- ✅ All functional requirements have ≥2 acceptance criteria
- ✅ All criteria use Given-When-Then format
- ✅ No ambiguous language detected
- ✅ Dependencies documented
- ✅ Effort estimates provided
- ✅ Out of scope explicitly stated
- ✅ Success criteria defined

## Output Format

Save to `docs/specification.md`:

```markdown
# [Project Name] - Specification v[version]

**Author**: [Name]
**Date**: [YYYY-MM-DD]
**Status**: Draft | Review | Approved | Implemented

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-01-02 | Alex | Initial draft |

## Overview

**Purpose**: [1-2 sentence purpose]

**Scope**:
- **IN**: [What's included]
- **OUT**: [What's excluded]

**Stakeholders**:
- [Stakeholder 1]: [Their interest]
- [Stakeholder 2]: [Their interest]

## Functional Requirements

[FR-XXX sections]

## Non-Functional Requirements

[NFR-XXX sections]

## Technical Constraints

[Technology, integration, data, deployment]

## Out of Scope

[Explicit exclusions with rationale]

## Dependencies

[External dependencies, third-party services]

## Acceptance Testing Strategy

[How requirements will be validated]

## Success Criteria

- [ ] [Measurable success indicator 1]
- [ ] [Measurable success indicator 2]

## Glossary

[Domain terms and definitions]

## References

[Related documents, research, prior art]
```
**Verification:** Run `pytest -v` to verify tests pass.

## Acceptance Criteria Patterns

### Given-When-Then

```markdown
Given [initial context/state]
When [action occurs]
Then [expected outcome]
```
**Verification:** Run the command with `--help` flag to verify availability.

**Examples**:
- Given unauthenticated user, when accessing dashboard, then redirect to login
- Given valid credentials, when logging in, then create session and redirect to dashboard
- Given expired session, when making API request, then return 401 Unauthorized

### Error Cases

Always include error scenarios:
- Invalid input handling
- Authentication/authorization failures
- Network/service failures
- Resource exhaustion
- Edge cases and boundaries

### Performance Criteria

Make performance requirements testable:
- "Dashboard loads in < 2 seconds" (measurable)
- NOT "Dashboard is fast" (vague)

### Security Criteria

Make security requirements verifiable:
- "All API endpoints require authentication" (testable)
- NOT "System is secure" (vague)

## Related Skills

- `Skill(spec-kit:spec-writing)` - Spec-kit methodology (if available)
- `Skill(attune:project-brainstorming)` - Previous phase
- `Skill(attune:project-planning)` - Next phase

## Related Commands

- `/attune:specify` - Invoke this skill
- `/attune:specify --clarify` - Run clarification workflow
- `/attune:plan` - Next step in workflow

## Examples

See `/attune:specify` command documentation for complete examples.
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
