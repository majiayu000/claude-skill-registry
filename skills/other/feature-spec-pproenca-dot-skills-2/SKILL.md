---
name: feature-spec
description: Feature specification and planning guidelines for software engineers. This skill should be used when writing PRDs, defining requirements, managing scope, prioritizing features, or handling change requests. Triggers on tasks involving feature planning, specification writing, stakeholder alignment, or scope management.
---

# Software Engineering Feature Specification and Planning Best Practices

Comprehensive feature specification and planning guide for software engineers, product managers, and technical leads. Contains 42 rules across 8 categories, prioritized by impact to prevent scope creep and ensure project success.

## When to Apply

Reference these guidelines when:
- Writing PRDs or feature specifications
- Defining requirements or user stories
- Managing scope and preventing scope creep
- Prioritizing features and backlog items
- Handling change requests
- Aligning stakeholders on project goals

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Scope Definition | CRITICAL | `scope-` |
| 2 | Requirements Clarity | CRITICAL | `req-` |
| 3 | Prioritization Frameworks | HIGH | `prio-` |
| 4 | Acceptance Criteria | HIGH | `accept-` |
| 5 | Stakeholder Alignment | MEDIUM-HIGH | `stake-` |
| 6 | Technical Specification | MEDIUM | `tech-` |
| 7 | Change Management | MEDIUM | `change-` |
| 8 | Documentation Standards | LOW | `doc-` |

## Quick Reference

### 1. Scope Definition (CRITICAL)

- `scope-define-boundaries` - Define explicit scope boundaries
- `scope-document-assumptions` - Document all assumptions explicitly
- `scope-work-breakdown` - Break scope into measurable work items
- `scope-define-mvp` - Define MVP before full feature set
- `scope-stakeholder-signoff` - Get stakeholder signoff on scope

### 2. Requirements Clarity (CRITICAL)

- `req-specific-measurable` - Write specific, measurable requirements
- `req-user-stories` - Structure requirements as user stories
- `req-avoid-solution-language` - Avoid solution-specific language
- `req-functional-nonfunctional` - Separate functional and non-functional
- `req-consistent-terminology` - Use consistent terminology
- `req-traceability` - Maintain requirements traceability

### 3. Prioritization Frameworks (HIGH)

- `prio-moscow-method` - Use MoSCoW prioritization method
- `prio-rice-scoring` - Apply RICE scoring for objectivity
- `prio-value-vs-effort` - Map value vs effort explicitly
- `prio-dependencies-first` - Identify and order dependencies
- `prio-kano-model` - Apply Kano model for feature classification

### 4. Acceptance Criteria (HIGH)

- `accept-given-when-then` - Use Given-When-Then format
- `accept-testable-criteria` - Write testable acceptance criteria
- `accept-edge-cases` - Include edge cases in acceptance
- `accept-definition-of-done` - Define clear definition of done
- `accept-avoid-over-specification` - Avoid over-specification

### 5. Stakeholder Alignment (MEDIUM-HIGH)

- `stake-identify-stakeholders` - Identify all stakeholders early
- `stake-early-feedback` - Gather feedback early and often
- `stake-conflict-resolution` - Resolve conflicts explicitly
- `stake-communication-plan` - Establish communication cadence
- `stake-success-metrics` - Align on success metrics

### 6. Technical Specification (MEDIUM)

- `tech-system-context` - Document system context and dependencies
- `tech-api-contracts` - Define API contracts before implementation
- `tech-data-model` - Specify data models and schema changes
- `tech-error-handling` - Plan error handling and recovery
- `tech-performance-requirements` - Specify performance requirements
- `tech-security-considerations` - Document security considerations

### 7. Change Management (MEDIUM)

- `change-formal-process` - Use formal change request process
- `change-impact-assessment` - Assess full impact before approval
- `change-version-tracking` - Version all specification documents
- `change-scope-freeze` - Implement scope freeze periods
- `change-defer-log` - Maintain deferred items log

### 8. Documentation Standards (LOW)

- `doc-single-source` - Maintain single source of truth
- `doc-consistent-templates` - Use consistent document templates
- `doc-decision-records` - Document key decisions with context
- `doc-accessible-format` - Keep documentation accessible
- `doc-glossary-terms` - Define project terminology
