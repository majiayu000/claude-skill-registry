---
description: PRD generation knowledge, templates, and compilation guidance for creating AI-optimized Product Requirements Documents
triggers:
  - compile PRD
  - generate PRD
  - create product requirements document
  - PRD template
  - finalize requirements
  - write PRD
---

# PRD Generation Skill

This skill provides structured knowledge for creating comprehensive, AI-optimized Product Requirements Documents.

## Core Principles

### 1. Phase-Based Milestones (Not Timelines)

PRDs should define clear phases with completion criteria rather than time estimates:

- **Phase 1: Foundation** - Core infrastructure and data models
- **Phase 2: Core Features** - Primary user-facing functionality
- **Phase 3: Enhancement** - Secondary features and optimizations
- **Phase 4: Polish** - UX refinement, edge cases, documentation

### 2. Testable Requirements

Every requirement should include:
- **Clear acceptance criteria** - Specific, measurable conditions for completion
- **Test scenarios** - How to verify the requirement is met
- **Edge cases** - Known boundary conditions to handle

### 3. Human Checkpoint Gates

Define explicit points where human review is required:
- Architecture decisions before implementation begins
- API contract review before integration work
- Security review before authentication/authorization features
- UX review before user-facing changes ship

### 4. Context for AI Consumption

Structure PRDs for optimal AI assistant consumption:
- Use consistent heading hierarchy
- Include code examples where applicable
- Reference existing patterns in the codebase
- Provide clear file location guidance

## Template Selection

Choose the appropriate template based on depth level:

| Depth Level | Template | Use Case |
|-------------|----------|----------|
| High-level overview | `template-high-level.md` | Executive summaries, stakeholder alignment, initial scoping |
| Detailed specifications | `template-detailed.md` | Standard development PRDs with clear requirements |
| Full technical documentation | `template-full-tech.md` | Complex features requiring API specs, data models, architecture |

## PRD Compilation Process

When compiling a PRD from gathered requirements:

1. **Select template** based on requested depth level
2. **Organize information** into template sections
3. **Fill gaps** by inferring logical requirements (flag assumptions clearly)
4. **Add acceptance criteria** for each functional requirement
5. **Define phases** with clear completion criteria
6. **Insert checkpoint gates** at critical decision points
7. **Review for completeness** before presenting to user

## Writing Guidelines

### Requirement Formatting

```markdown
### REQ-001: [Requirement Name]

**Priority**: P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low)

**Description**: Clear, concise statement of what is needed.

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

**Notes**: Any additional context or constraints.
```

### User Story Format

```markdown
**As a** [user type]
**I want** [capability]
**So that** [benefit/value]
```

### API Specification Format (Full Tech Only)

```markdown
#### Endpoint: `METHOD /path`

**Purpose**: Brief description

**Request**:
- Headers: `Content-Type: application/json`
- Body:
  ```json
  {
    "field": "type - description"
  }
  ```

**Response**:
- `200 OK`: Success response schema
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Authentication required
```

## Reference Files

- `references/template-high-level.md` - Streamlined executive overview template
- `references/template-detailed.md` - Standard PRD template with all sections
- `references/template-full-tech.md` - Extended template with technical specifications
- `references/interview-questions.md` - Question bank for requirement gathering
