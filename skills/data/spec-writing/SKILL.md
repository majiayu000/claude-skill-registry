---
name: spec-writing
description: Skill for the Spec Writer agent to create and refine feature specifications. Provides templates for specs, clarification workflows, and quality checklists. Supports the SDD methodology by ensuring specs are complete, testable, and implementation-agnostic.
---

# Spec Writing Skill

> Equips the Spec Writer agent with templates, references, and workflows for creating high-quality feature specifications.

## Overview

This skill provides everything needed to:
- Create specifications from vague feature briefs
- Write clear, testable user stories
- Generate acceptance criteria
- Run clarification sessions
- Validate spec completeness

## Contents

### References

| File | Purpose |
|------|---------|
| `spec-taxonomy.md` | Categories for ambiguity scanning |
| `requirement-patterns.md` | Common requirement patterns and anti-patterns |
| `clarification-guide.md` | How to generate and prioritize questions |
| `quality-criteria.md` | Checklist criteria for spec validation |

### Assets (Templates)

| File | Purpose |
|------|---------|
| `.specify/templates/spec-template.md` | **CANONICAL** Main feature specification template |
| `user-story-template.md` | User story format with acceptance criteria |
| `clarification-question-template.md` | Question format for clarification sessions |
| `quality-checklist-template.md` | Spec quality validation checklist |

**NOTE:** The main spec template lives at `.specify/templates/spec-template.md` (project-wide canonical template). Always use this instead of creating duplicates.

## Usage

### Creating a New Specification

1. Parse the feature description for key concepts
2. **Load canonical template:** `.specify/templates/spec-template.md`
3. Fill in all mandatory sections
4. Reference `references/requirement-patterns.md` for good requirement examples
5. Validate against `references/quality-criteria.md`

### Writing User Stories

1. Load `assets/user-story-template.md`
2. Identify actors, goals, and benefits
3. Write acceptance criteria (Given/When/Then)
4. Assign priority (P1, P2, P3)
5. Ensure story is independently testable

### Running Clarification

1. Load current spec
2. Scan using `references/spec-taxonomy.md` categories
3. Generate questions using `references/clarification-guide.md`
4. Use `assets/clarification-question-template.md` for formatting
5. Update spec after each answer

### Validating Specification

1. Load `assets/quality-checklist-template.md`
2. Check each criterion against the spec
3. Document pass/fail for each item
4. Iterate until all critical items pass

## Spec Taxonomy Categories

Use these categories to scan for ambiguity:

### Functional Scope & Behavior
- Core user goals & success criteria
- Explicit out-of-scope declarations
- User roles / personas differentiation

### Domain & Data Model
- Entities, attributes, relationships
- Identity & uniqueness rules
- Lifecycle/state transitions
- Data volume / scale assumptions

### Interaction & UX Flow
- Critical user journeys / sequences
- Error/empty/loading states
- Accessibility or localization notes

### Non-Functional Quality Attributes
- Performance (latency, throughput targets)
- Scalability (horizontal/vertical, limits)
- Reliability & availability (uptime, recovery)
- Observability (logging, metrics, tracing)
- Security & privacy (authN/Z, data protection)
- Compliance / regulatory constraints

### Integration & External Dependencies
- External services/APIs and failure modes
- Data import/export formats
- Protocol/versioning assumptions

### Edge Cases & Failure Handling
- Negative scenarios
- Rate limiting / throttling
- Conflict resolution (e.g., concurrent edits)

### Constraints & Tradeoffs
- Technical constraints (language, storage, hosting)
- Explicit tradeoffs or rejected alternatives

### Terminology & Consistency
- Canonical glossary terms
- Avoided synonyms / deprecated terms

### Completion Signals
- Acceptance criteria testability
- Measurable Definition of Done indicators

## Key Rules

### Maximum Clarifications
- Max 3 [NEEDS CLARIFICATION] markers per spec
- Max 5 questions per clarification session
- Max 10 questions total across all sessions

### Prioritization Order
1. Scope (what's in/out)
2. Security/Privacy (compliance, data protection)
3. User Experience (flows, edge cases)
4. Technical Details (only if blocking functional clarity)

### Reasonable Defaults (Don't Ask)
- Data retention: Industry-standard for domain
- Performance: Standard web/mobile expectations
- Error handling: User-friendly messages with fallbacks
- Authentication: Session-based or OAuth2
- Integration: RESTful APIs

### Success Criteria Rules
- Must be measurable (include metrics)
- Must be technology-agnostic (no frameworks)
- Must be user-focused (outcomes, not internals)
- Must be verifiable (testable without implementation)

## Integration

This skill is automatically available to the Spec Writer agent via the `skills: spec-writing` frontmatter.

To use templates:
```
Read: .claude/skills/spec-writing/assets/[template]
```

To check references:
```
Read: .claude/skills/spec-writing/references/[reference]
```

## Related Commands

| Command | Description |
|---------|-------------|
| `/sp.specify` | Create specification from feature brief |
| `/sp.clarify` | Run clarification Q&A session |

## Quality Gate

A specification is ready for `/sp.plan` when:
- [ ] All mandatory sections completed
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] All requirements are testable
- [ ] Success criteria are measurable and technology-agnostic
- [ ] User stories have acceptance scenarios
- [ ] Edge cases are identified
- [ ] Assumptions are documented
