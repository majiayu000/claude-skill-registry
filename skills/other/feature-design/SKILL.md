---
name: feature-design
description: Guide users through feature specification development using EARS patterns and INCOSE quality rules. Creates requirements documents and technical design specifications with iterative user feedback.
arguments:
  - name: feature_idea
    description: Brief description of the feature idea to develop
    required: false
  - name: workspace
    description: Absolute path to the workspace directory
    required: false
---

# Feature Design

Transform rough feature ideas into detailed requirements and technical design documents through an iterative, user-collaborative process.

## Overview

This skill implements a Spec-Driven Development (SDD) workflow that systematically:
1. Captures and refines feature requirements using EARS (Easy Approach to Requirements Syntax)
2. Validates requirements against INCOSE semantic quality rules
3. Creates technical design documents with architecture, components, and implementation plans

## Glossaries

### EARS (Easy Approach to Requirements Syntax)

EARS provides standardized templates for writing clear, unambiguous requirements:

| Pattern | Template | Example |
|---------|----------|---------|
| Ubiquitous | The `<system>` SHALL `<function>` | The system SHALL provide user login functionality |
| Event-Driven | WHEN `<trigger>`, the `<system>` SHALL `<function>` | WHEN user clicks "Login", the system SHALL validate credentials |
| State-Driven | WHILE `<state>`, the `<system>` SHALL `<function>` | WHILE user is logged in, the system SHALL display dashboard |
| Unwanted-Behavior | IF `<condition>`, the `<system>` SHALL `<function>` | IF password fails 3 times, the system SHALL lock account for 30 minutes |
| Complex | [WHERE] [WHILE] [WHEN/IF] THE `<system>` SHALL `<function>` | Clause order: WHERE → WHILE → WHEN/IF → THE → SHALL |

### INCOSE Semantic Quality Rules

Requirements must comply with these quality rules:

- **Active voice** - Clearly state who does what
- **No vague terms** - Avoid "quickly", "adequate", "user-friendly"
- **No escape clauses** - Avoid "where possible", "if feasible"
- **No negative statements** - Avoid "SHALL NOT" (rephrase positively)
- **One thought per requirement** - Single, testable concept
- **Explicit conditions** - Measurable criteria and thresholds
- **Consistent terminology** - Use defined terms from glossary
- **No pronouns** - Avoid "it", "them", "this"
- **No absolutes** - Avoid "never", "always", "100%"
- **Solution-free** - Focus on what, not how

## Document Templates

### Requirements Document (`requirements.md`)

```markdown
# Requirements Document

## Introduction

[Summary of the feature/system]

## Glossary

- **System/Term**: [Definition]

## Requirements

### Requirement 1

**User Story:** AS [role], I want [feature], so that [benefit]

#### Acceptance Criteria

1. WHEN [event], [system] SHALL [response]
2. WHILE [state], [system] SHALL [response]
3. IF [unwanted event], [system] SHALL [response]
... (2-5 EARS definitions per requirement)

[Repeat for other requirements]
```

### Design Document (`design.md`)

```markdown
# [Feature Title]

Feature Name: feature-name
Updated: yyyy-mm-dd

## Description

[Feature description]

## Architecture

[Mermaid diagrams as needed]
[Architecture explanation]

## Components and Interfaces

[Component and interface descriptions]

## Data Models

[Data structure descriptions]

## Correctness Properties

[Invariants and constraints]

## Error Handling

[Error scenarios and handling strategies]

## Test Strategy

[Testing approach and coverage]

## References

[^1]: (Website) - [Page description](URL)
[^2]: (Filename#Lnnn) - [File link](relative/path)
```

## Workflow

### Phase 1: Requirements Generation

1. **Initialize Feature**
   - Generate a short feature name in `kebab-case` format (e.g., `user-authentication`)
   - Create directory `.monkeycode/specs/{FEATURE_NAME}/`

2. **Gather Context**
   - Read project documentation from `.monkeycode/docs/` if available:
     - `INDEX.md` - Project overview
     - `ARCHITECTURE.md` - System architecture
   - Scan `.monkeycode/specs/*/` for related historical requirements
   - Understand existing code structure

3. **Generate Initial Requirements**
   - Decompose the feature idea into user stories
   - Apply EARS patterns to each acceptance criterion
   - Validate against INCOSE quality rules
   - Write to `.monkeycode/specs/{FEATURE_NAME}/requirements.md`

4. **Iterate with User**
   - Present requirements document to user
   - Ask clarifying questions (maximum 3 questions per round)
   - Provide options with reasonable defaults
   - Update document based on feedback

5. **Special Handling for Parsers/Serializers**
   - Explicitly list all parsers and serializers as requirements
   - Add pretty-printer requirements for each parser
   - Include round-trip validation in acceptance criteria

### Phase 2: Technical Design

1. **Initialize Design Document**
   - Get current date via `date '+%Y-%m-%d'`
   - Create feature name with date prefix (e.g., `2025-01-15-user-authentication`)
   - Create initial design outline in `.monkeycode/specs/{FEATURE_NAME}/design.md`

2. **Gather Technical Context**
   - Read `.monkeycode/docs/INDEX.md` and `.monkeycode/docs/ARCHITECTURE.md`
   - Analyze project structure and existing patterns
   - Review related specifications in `.monkeycode/specs/`

3. **Generate Design Document**
   - Include all required sections:
     - Description
     - Architecture (with Mermaid diagrams)
     - Components and Interfaces
     - Data Models
     - Correctness Properties
     - Error Handling
     - Test Strategy
   - Ensure design addresses all requirements from Phase 1
   - Highlight design decisions and rationale

4. **Iterate with User**
   - Present design document to user
   - Ask technical questions (maximum 3 per round)
   - Update based on feedback

5. **Finalize**
   - Commit changes with `git commit`
   - Push to remote with `git push`
   - Summarize deliverables to user

## Decision Points

During the workflow, ask the user about:

| Topic | Example Questions |
|-------|-------------------|
| Scope | Which user roles need this feature? |
| Integration | Should this integrate with existing systems? |
| Performance | What are the expected load requirements? |
| Security | What authentication/authorization is needed? |
| Data | What data needs to be persisted? |
| Error Handling | How should failures be communicated to users? |

## Output Files

```
.monkeycode/specs/{FEATURE_NAME}/
├── requirements.md    # EARS-compliant requirements
└── design.md          # Technical design specification
```

## Notes

- All communication with users must use the project's configured language
- Maximum 3 clarifying questions per iteration round
- Always validate requirements against both EARS and INCOSE rules
- Correct non-compliant user inputs and explain corrections
- Design documents should be solution-agnostic where possible
- Include Mermaid diagrams for complex architectures
- Reference specific files with line numbers when applicable
