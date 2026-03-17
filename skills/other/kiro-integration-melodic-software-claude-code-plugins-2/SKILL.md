---
name: kiro-integration
description: AWS Kiro specification patterns and synchronization. Use when working with Kiro IDE, syncing requirements.md/design.md/tasks.md files, or configuring steering files for AI agent context.
allowed-tools: Read, Glob, Grep, Write, Edit, Task
---

# Kiro Integration

AWS Kiro specification patterns, file structure, and synchronization with canonical model.

## When to Use This Skill

**Keywords:** Kiro, AWS Kiro, requirements.md, design.md, tasks.md, steering files, Kiro IDE, Kiro agent, Kiro sync, spec generation, agentic development, Kiro hooks

**Use this skill when:**

- Working with AWS Kiro IDE or Kiro-compatible tools
- Syncing between Kiro format and canonical specifications
- Creating or updating Kiro specification files
- Configuring steering files for agent context
- Integrating Kiro with existing spec-driven workflows
- Converting between Kiro and other specification formats

## Kiro Overview

Kiro is an agentic IDE developed by AWS that uses specification-driven development. It generates three interconnected files:

```text
.kiro/
├── specs/
│   ├── requirements.md    # EARS-formatted requirements
│   ├── design.md          # Technical implementation design
│   └── tasks.md           # Executable task breakdown
└── steering/
    └── context.md         # Agent steering context
```

## Key Concepts

### Specification Files

| File | Purpose | Format |
| --- | --- | --- |
| `requirements.md` | Requirements using EARS patterns | EARS syntax in markdown |
| `design.md` | Technical design and architecture | Markdown with diagrams |
| `tasks.md` | Executable task checklist | Markdown checkboxes |

### EARS Integration

Kiro uses EARS (Easy Approach to Requirements Syntax) for requirements. All six patterns are supported:

- **Ubiquitous:** `The system SHALL...`
- **State-Driven:** `WHILE <condition>, the system SHALL...`
- **Event-Driven:** `WHEN <trigger>, the system SHALL...`
- **Unwanted:** `IF <condition>, THEN the system SHALL...`
- **Optional:** `WHERE <feature>, the system SHALL...`
- **Complex:** Combinations of the above

### Steering Files

Steering files provide context to the Kiro agent:

- Project-specific knowledge
- Codebase conventions
- Domain terminology
- Architectural constraints

## Kiro File Structure

### requirements.md

```markdown
# Requirements: <Feature Name>

## Context

<Problem statement and background>

## Functional Requirements

### FR-1: <Requirement Title>

**Pattern:** Event-Driven
**Priority:** Must

WHEN the user submits a form, the system SHALL validate all required fields.

#### Acceptance Criteria

- [ ] AC-1.1: Given valid input, when submitted, then success message shown
- [ ] AC-1.2: Given invalid input, when submitted, then errors highlighted

### FR-2: ...

## Non-Functional Requirements

### NFR-1: Performance

The system SHALL respond within 200ms for all API requests.
```

### design.md

```markdown
# Design: <Feature Name>

## Overview

<High-level design approach>

## Architecture

### Component Diagram

<Mermaid or text diagram>

### Components

| Component | Responsibility |
| --- | --- |
| FormValidator | Input validation logic |
| FormHandler | Form submission handling |

## Data Model

### Entities

- **FormSubmission**: Captures form data
  - id: UUID
  - data: JSON
  - status: enum

## API Design

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| POST | /api/forms | Submit form |

## Technical Decisions

### Approach Selected

<Chosen approach with rationale>

### Alternatives Considered

| Alternative | Pros | Cons | Why Not |
| --- | --- | --- | --- |
| ... | ... | ... | ... |
```

### tasks.md

````markdown
# Tasks: <Feature Name>

## Task List

### Phase 1: Setup

- [ ] **TSK-001**: Create FormValidator component
  - Requirement: FR-1
  - Deliverables: `src/validators/FormValidator.ts`
  - Acceptance: Unit tests pass

- [ ] **TSK-002**: Create FormHandler service
  - Requirement: FR-1, FR-2
  - Deliverables: `src/services/FormHandler.ts`
  - Acceptance: Integration tests pass

### Phase 2: Integration

- [ ] **TSK-003**: Wire up API endpoint
  - Requirement: FR-1
  - Deliverables: `src/routes/forms.ts`
  - Acceptance: E2E tests pass

## Dependency Graph

```text
TSK-001 ─┬─> TSK-003
TSK-002 ─┘
```

## Progress

| Status | Count |
| --- | --- |
| Pending | 3 |
| In Progress | 0 |
| Complete | 0 |
````

## Sync with Canonical Model

### Kiro to Canonical

| Kiro Field | Canonical Field |
| --- | --- |
| requirements.md FR-x | `requirements[].id` |
| EARS text | `requirements[].text` |
| Priority | `requirements[].priority` |
| AC-x.y | `requirements[].acceptance_criteria[]` |
| design.md | `implementation_notes` |
| tasks.md TSK-x | maps to task schema |

### Canonical to Kiro

When converting from canonical format to Kiro:

1. Split canonical spec into three files
2. Format requirements using EARS syntax
3. Generate design.md from implementation notes
4. Create tasks.md from task breakdown

## Steering File Configuration

### context.md Structure

```markdown
# Project Context

## Overview

<Project description and purpose>

## Technology Stack

- Language: TypeScript
- Framework: Next.js
- Database: PostgreSQL

## Conventions

### Naming

- Use camelCase for variables
- Use PascalCase for components
- Use kebab-case for files

### Architecture

- Follow vertical slice architecture
- Use feature-based folder structure
- Apply CQRS for complex operations

## Domain Glossary

| Term | Definition |
| --- | --- |
| Form | User input collection |
| Submission | Completed form data |

## Constraints

- All APIs must be RESTful
- Response time < 200ms
- Test coverage > 80%
```

## Workflows

### Generate Kiro Specs from Feature Request

1. Analyze feature request
2. Generate `requirements.md` with EARS patterns
3. Generate `design.md` with architecture
4. Generate `tasks.md` with breakdown
5. Create steering context if needed

### Sync Kiro to Canonical

1. Read Kiro spec files
2. Parse EARS requirements
3. Extract acceptance criteria
4. Map to canonical schema
5. Output canonical YAML/JSON

### Sync Canonical to Kiro

1. Read canonical specification
2. Split into three Kiro files
3. Format requirements as EARS
4. Structure design document
5. Create task checklist

## Quick Commands

| Action | Command |
| --- | --- |
| Generate from feature | `/spec:kiro:sync --from feature` |
| Sync to canonical | `/spec:kiro:sync --to canonical` |
| Update from canonical | `/spec:kiro:sync --from canonical` |
| Validate Kiro files | `/spec:validate .kiro/specs/` |

## Integration with Spec Kit

Kiro files map to Spec Kit phases:

| Kiro File | Spec Kit Phase |
| --- | --- |
| requirements.md | Phase 1: Specify |
| design.md | Phase 2: Plan |
| tasks.md | Phase 3: Tasks |

## References

**Detailed Documentation:**

- [Kiro Structure Reference](references/kiro-structure.md) - File organization patterns
- [Steering Files Guide](references/steering-files.md) - Context configuration
- [Hooks Integration](references/hooks-integration.md) - Kiro hooks patterns

**Related Skills:**

- `ears-authoring` - EARS requirement patterns
- `speckit-workflow` - GitHub Spec Kit 5-phase workflow
- `canonical-spec-format` - Canonical specification structure

---

**Last Updated:** 2025-12-24

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
