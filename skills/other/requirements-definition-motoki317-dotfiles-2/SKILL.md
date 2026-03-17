---
name: Requirements Definition
description: This skill should be used when the user asks to "define requirements", "create specification", "clarify requirements", "write requirements document", or mentions requirement analysis. Provides comprehensive requirements definition methodology.
---

# Requirements Definition

Methodology for requirements definition ensuring comprehensive specification before implementation.

## Investigation Workflow

1. **Directory structure** - Glob
2. **Symbol analysis** - get_symbols_overview
3. **Keyword search** - Grep or find_symbol
4. **Dependency mapping** - find_referencing_symbols
5. **Specific content** - Read
6. **Latest API docs** - Context7

## Question Scoring

Score each unclear requirement (1-5 each):

| Criterion | Description |
|-----------|-------------|
| Design Branching | How much does answer affect design? |
| Irreversibility | How difficult to change after implementation? |
| Investigation Impossibility | Cannot determine through code alone? |
| Effort Impact | How much affects implementation effort? |

**Critical questions (score >= 15)**: Must answer before proceeding.

**Example:**
```
Question: "Should we use TypeScript's strict mode?"
- Design Branching: 5
- Irreversibility: 4
- Investigation Impossibility: 3
- Effort Impact: 4
Total: 16 (critical)
```

## Question Types

- **Spec confirmation**: "Does API return null or empty array?"
- **Design choice**: "REST or GraphQL?"
- **Constraint**: "Must support IE11?"
- **Scope**: "Include admin features in v1?"
- **Priority**: "Which feature first?"

## Functional Requirements Format

```
FR-001: User Authentication
Priority: mandatory
- Users can log in with email/password
- Session expires after 24h inactivity
- Failed logins rate-limited (max 5/hour)
```

## Non-Functional Requirements

```
Performance:
- API response < 200ms (95th percentile)
- Support 1000 concurrent users

Security:
- AES-256 encryption at rest
- JWT authentication

Maintainability:
- Test coverage >= 80%
- Documentation for public APIs
```

## Technical Specifications

```
Design Decision: Use React Query for data fetching
Rationale:
- Built-in caching
- Auto background refetching
- TypeScript support
- Widely adopted in codebase

Impact: All API-calling components, test utilities
```

## Quality Metrics

| Metric | 90-100 | 70-89 | 50-69 | <50 |
|--------|--------|-------|-------|-----|
| Feasibility | Straightforward | Some research | Challenges | Architecture changes |
| Objectivity | All verified | Most verified | Mixed | Mostly assumptions |

## Output Structure

1. **Summary**: Request, background, expected outcomes
2. **Current State**: System, stack, patterns
3. **Functional Requirements**: FR-XXX with priority and acceptance criteria
4. **Non-Functional**: Performance, security, maintainability
5. **Technical Specs**: Design decisions with rationale
6. **Metrics**: Feasibility and objectivity scores
7. **Constraints**: Technical and operational
8. **Test Requirements**: Coverage, scenarios, acceptance
9. **Task Breakdown**: Dependencies, phases, handoff

## Best Practices

**Critical:**
- Investigate current state before defining requirements
- Score questions and prioritize high-score (>= 15)
- Distinguish mandatory from optional with rationale

**High:**
- Document all assumptions when unclear
- Map requirements to test scenarios
- Include rationale for design decisions

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Vague requirements | Specific, testable with acceptance criteria |
| Implementation details | Describe what, not how |
| Skipping investigation | Always investigate first |
| Missing constraints | Document all constraints |
| Undefined priorities | Mark mandatory/optional |

## Constraints

**Must:**
- Investigate before concluding
- Ask questions before assuming
- Include (Recommended) option in AskUserQuestion

**Avoid:**
- Proceeding without answering critical questions
- Justifying user preferences over technical validity
