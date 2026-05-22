---
name: checklist-generation
description: "Expertise in generating domain-specific quality checklists for specifications. Activates when user discusses quality validation or requirement testing. Trigger keywords: checklist, quality gate, requirement testing, validation, completeness check, review checklist"
allowed-tools: Read, Write, Edit, Glob
user-invocable: false
---

# Checklist Generation Skill

## Purpose

This skill provides expertise in generating domain-specific quality checklists for specifications. Unlike static templates, it dynamically produces questions and validation items based on the actual content of the specification. The output is a tailored checklist that tests whether the specification adequately addresses the relevant quality domains.

## When It Activates

The skill is triggered when the conversation involves:

- Generating quality validation checklists for a specification
- Running completeness checks against requirements
- Preparing review checklists before implementation
- Discussing quality gates or readiness criteria
- Validating specification coverage across specific domains

## Dynamic Question Generation Methodology

The skill does NOT use static, one-size-fits-all checklists. Instead, it follows a dynamic generation pipeline:

1. **Parse Specification**: Extract all requirements (FR/NFR), user stories, data model entities, API endpoints, and success criteria from the specification.
2. **Detect Relevant Domains**: Determine which quality domains are applicable based on the specification content. Skip domains that have no relevance to the project.
3. **Generate Domain Questions**: For each relevant domain, produce specific questions derived from the actual requirements and entities in the specification.
4. **Add Traceability References**: Each question includes a `[Spec §X.Y]` reference linking it back to the specific section or requirement it validates.
5. **Filter and Prioritize**: Remove redundant questions and order by importance within each domain.

## Available Domains

The skill supports five quality domains:

### 1. UX Domain

Questions about user experience, interface design, and interaction patterns.

- Accessibility requirements for each user-facing feature
- Error state handling and user feedback mechanisms
- Navigation flows and information architecture
- Responsive design and device support considerations

### 2. API Domain

Questions about API design, contracts, and integration points.

- Endpoint completeness (CRUD coverage for each entity)
- Request/response schema validation and error codes
- Authentication and authorization per endpoint
- Pagination, filtering, and sorting support

### 3. Security Domain

Questions about security posture, threat mitigation, and data protection.

- Authentication mechanism specification (method, token lifecycle)
- Authorization model and role-based access definitions
- Input validation and sanitization requirements
- Data encryption requirements (at rest, in transit)

### 4. Performance Domain

Questions about performance targets, scalability, and resource management.

- Response time targets for critical operations
- Concurrency and throughput requirements
- Caching strategy and invalidation rules
- Database query performance constraints

### 5. Data Domain

Questions about data modeling, integrity, and lifecycle management.

- Entity relationship completeness and constraint definitions
- Data validation rules for each field
- Migration strategy and backward compatibility
- Retention policies and archival requirements

## Question Pattern Types

Questions are generated using five pattern types:

| Pattern | Source | Example |
|---------|--------|---------|
| **Requirement-based** | FR/NFR items | "Does FR-003 specify the retry count and backoff strategy?" |
| **User story** | US definitions | "Does US2 define the error state when payment fails?" |
| **Entity-based** | Data model | "Are all fields of the `Order` entity typed and constrained?" |
| **Endpoint** | API contracts | "Does `POST /orders` specify the 409 conflict response?" |
| **Success criteria** | Metrics | "Is the 99th percentile response time target quantified?" |

## Output Format

The checklist is output as markdown with checkboxes, grouped by domain:

```markdown
## UX Checklist

- [ ] Accessibility: Does FR-005 specify keyboard navigation for the dashboard? [Spec §3.5]
- [ ] Error states: Does US3 define the empty state when no results are found? [Spec §4.3]

## API Checklist

- [ ] Does `GET /users` specify pagination parameters and defaults? [Spec §5.1]
- [ ] Does `POST /orders` define validation error response schema? [Spec §5.3]
```

Each item includes a `[Spec §X.Y]` reference for traceability.

## Relevance Filtering

Not all domains apply to every specification. The skill applies relevance filtering:

- **UX**: Skipped if the specification has no user-facing interface (e.g., pure backend service)
- **API**: Skipped if no API contracts or endpoints are defined
- **Security**: Always included (security is universally relevant)
- **Performance**: Skipped if no NFRs mention performance, latency, or throughput
- **Data**: Skipped if no data model or entities are defined

When a domain is skipped, the report notes the reason for exclusion.

## References

For domain definitions, question patterns, and configuration options, consult:

- `references/checklist-domains.md` -- Full domain definitions and applicability rules
- `references/question-patterns.md` -- Question pattern templates and generation logic
