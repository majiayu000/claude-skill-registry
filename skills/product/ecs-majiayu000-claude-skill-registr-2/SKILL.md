---
name: specs-creator
description: Creates detailed specifications from client needs including product specs, technical specs, design specs, and API specs. Use when the user requests help with requirement gathering, creating specifications, documenting client requirements, converting feature requests into structured specs, or needs to formalize project requirements for development handoff.
---

# Specification Creator

Systematically gather client requirements and transform them into comprehensive, development-ready specifications.

## Core Specification Types

### Product Specifications (PRD)
User-facing features, business goals, and product requirements

### Technical Specifications
Architecture, implementation details, technology stack, and system design

### Design Specifications
UI/UX requirements, visual design guidelines, interaction patterns, and accessibility

### API Specifications
Endpoint definitions, request/response schemas, authentication, and integration details

## Specification Creation Workflow

Follow this systematic process for gathering requirements and creating specs:

```
Specification Progress:
- [ ] Step 1: Identify specification type and scope
- [ ] Step 2: Gather requirements through structured questions
- [ ] Step 3: Organize and structure collected information
- [ ] Step 4: Create specification document
- [ ] Step 5: Validate for completeness and clarity
- [ ] Step 6: Review and finalize
```

### Step 1: Identify Specification Type and Scope

Determine what type of specification is needed:

**Questions to ask:**
- What is the primary purpose of this specification?
- Who is the intended audience (developers, designers, stakeholders)?
- What is the project scope (new feature, entire system, integration)?
- What are the deliverables and success criteria?

### Step 2: Gather Requirements Through Structured Questions

Use targeted questions based on specification type:

#### For Product Specifications:
- What problem does this solve for users?
- Who are the target users and what are their needs?
- What are the core features and functionality?
- What are the business goals and success metrics?
- What are the constraints (timeline, budget, resources)?
- What are the dependencies on other systems or features?

#### For Technical Specifications:
- What is the current system architecture?
- What are the technical requirements and constraints?
- What technologies and frameworks will be used?
- What are the performance requirements?
- What are the security and compliance needs?
- How will the system scale?
- What are the data storage and processing requirements?

#### For Design Specifications:
- What is the desired user experience?
- What are the visual design requirements (branding, style guide)?
- What are the interaction patterns and user flows?
- What are the accessibility requirements (WCAG compliance)?
- What are the responsive design requirements?
- What components and design patterns should be used?

#### For API Specifications:
- What are the API endpoints and their purposes?
- What are the request and response formats?
- What authentication and authorization are required?
- What are the rate limits and quotas?
- What error handling is needed?
- What are the versioning requirements?
- What documentation format should be used (OpenAPI, etc.)?

### Step 3: Organize and Structure Information

**Group related requirements:**
- Categorize by feature, component, or functional area
- Identify dependencies between requirements
- Prioritize requirements (must-have, should-have, nice-to-have)
- Note any conflicts or ambiguities that need resolution

**Create initial outline:**
- Executive summary or overview
- Core requirements sections
- Technical details
- Success criteria and acceptance criteria
- Timeline and milestones (if applicable)

### Step 4: Create Specification Document

Use the appropriate template based on specification type. See reference files for detailed templates:

**Product Specs:** See [PRODUCT-TEMPLATE.md](PRODUCT-TEMPLATE.md)
**Technical Specs:** See [TECHNICAL-TEMPLATE.md](TECHNICAL-TEMPLATE.md)
**Design Specs:** See [DESIGN-TEMPLATE.md](DESIGN-TEMPLATE.md)
**API Specs:** See [API-TEMPLATE.md](API-TEMPLATE.md)

### Step 5: Validate for Completeness

Run through the validation checklist:

```typescript
// Validation Checklist
const validation = {
  clarity: [
    'Are all technical terms defined?',
    'Are requirements specific and measurable?',
    'Is the language clear and unambiguous?',
  ],
  completeness: [
    'Are all sections filled out?',
    'Are dependencies identified?',
    'Are edge cases addressed?',
    'Are acceptance criteria defined?',
  ],
  consistency: [
    'Do different sections align with each other?',
    'Are naming conventions consistent?',
    'Are similar requirements handled similarly?',
  ],
  feasibility: [
    'Are requirements technically achievable?',
    'Are timelines realistic?',
    'Are resources adequate?',
  ],
};
```

**If validation fails:**
- Note specific gaps or issues
- Gather additional information
- Revise the specification
- Run validation again

**Only proceed when validation passes**

### Step 6: Review and Finalize

Final review process:

1. Read through entire specification end-to-end
2. Verify all cross-references are correct
3. Ensure consistent formatting and structure
4. Add table of contents if document is long
5. Include version number and last updated date
6. List all stakeholders and reviewers
7. Save in appropriate format (Markdown, PDF, etc.)

## Question Patterns for Requirement Gathering

### Discovery Questions
Uncover hidden requirements and constraints:

- "What happens when [edge case]?"
- "How should the system handle [error condition]?"
- "What are the performance expectations for [scenario]?"
- "Who needs to be notified when [event occurs]?"
- "What data needs to be tracked for [feature]?"

### Clarification Questions
Eliminate ambiguity:

- "When you say [term], do you mean [interpretation A] or [interpretation B]?"
- "Can you provide an example of [requirement]?"
- "What does success look like for [feature]?"
- "What are the specific metrics for [goal]?"

### Constraint Questions
Identify limitations:

- "What are the technical constraints?"
- "What is the timeline for delivery?"
- "What is the budget?"
- "What compliance requirements must be met?"
- "What are the integration requirements?"

### Prioritization Questions
Determine what matters most:

- "If you could only have three features, which would they be?"
- "What is absolutely required for launch vs. what can wait?"
- "What would cause the most user pain if missing?"

## Specification Quality Guidelines

### Good Specifications

**Characteristics:**
- Specific and measurable acceptance criteria
- Clear user stories or use cases
- Concrete examples with input/output
- Well-defined edge cases and error handling
- Explicit dependencies and assumptions
- Quantified performance requirements
- Structured and easy to navigate

**Example - Good Requirement:**
```
Requirement: User Authentication
The system shall implement JWT-based authentication with the following requirements:

1. Login endpoint: POST /api/auth/login
   - Input: { email: string, password: string }
   - Output: { token: string, expiresIn: number, user: UserObject }
   - Response time: < 200ms (p95)

2. Token expiration: 24 hours
3. Password requirements:
   - Minimum 8 characters
   - Must contain: uppercase, lowercase, number, special character

4. Rate limiting: 5 failed attempts per email per 15 minutes
5. Security: Passwords hashed with bcrypt (cost factor: 12)

Acceptance Criteria:
- User can log in with valid credentials
- Invalid credentials return 401 with error message
- Expired tokens are rejected with 401
- Rate limit blocks after 5 failed attempts
```

### Bad Specifications

**Avoid:**
- Vague requirements ("fast", "user-friendly", "secure")
- Missing acceptance criteria
- Implementation details in product specs
- Conflicting requirements
- Undefined technical terms without context
- No prioritization
- Missing error handling

**Example - Bad Requirement:**
```
Requirement: User Login
Users should be able to log in to the system. The login should be secure
and fast. Use industry best practices.

// Problems:
// - "secure" is vague
// - "fast" is not quantified
// - "best practices" is undefined
// - No acceptance criteria
// - No error handling specified
// - No technical details
```

## Common Patterns by Specification Type

### Product Specification Pattern

```markdown
# [Feature Name] - Product Specification

## Overview
[One-paragraph summary of what this feature does and why it matters]

## Problem Statement
[What user problem does this solve?]

## User Stories
As a [user type], I want to [action] so that [benefit]

## Requirements
### Must Have (P0)
- [Critical requirement 1]
- [Critical requirement 2]

### Should Have (P1)
- [Important requirement 1]

### Nice to Have (P2)
- [Optional enhancement 1]

## User Flows
[Step-by-step user interactions]

## Success Metrics
[How will we measure success?]

## Out of Scope
[What this does NOT include]
```

### Technical Specification Pattern

```markdown
# [System/Feature Name] - Technical Specification

## Architecture Overview
[High-level system design]

## Components
### Component A
- Responsibility: [What it does]
- Technology: [Stack used]
- Dependencies: [What it depends on]
- API: [Interfaces it exposes]

## Data Models
[Database schemas, entities]

## API Endpoints
[If applicable]

## Security Considerations
[Authentication, authorization, data protection]

## Performance Requirements
[Latency, throughput, scalability targets]

## Error Handling
[How errors are handled and reported]

## Testing Strategy
[Unit, integration, e2e testing approach]

## Deployment
[How it will be deployed and configured]
```

### Design Specification Pattern

```markdown
# [Feature Name] - Design Specification

## Design Goals
[What experience are we creating?]

## User Personas
[Who are we designing for?]

## User Flows
[Visual or text-based flow diagrams]

## Component Library
[What UI components are used?]

## Visual Design
- Colors: [Palette]
- Typography: [Font families, sizes]
- Spacing: [Grid system]
- Icons: [Icon set]

## Interaction Patterns
[How users interact with elements]

## Responsive Behavior
[Mobile, tablet, desktop breakpoints]

## Accessibility
- WCAG Level: [A, AA, AAA]
- Keyboard navigation: [Requirements]
- Screen reader support: [Requirements]
- Color contrast: [Ratios]

## States
[Default, hover, active, disabled, error states]
```

### API Specification Pattern

```markdown
# [API Name] - API Specification

## Base URL
https://api.example.com/v1

## Authentication
[OAuth 2.0, API Key, JWT, etc.]

## Endpoints

### GET /resource
**Description:** [What this endpoint does]

**Request:**
- Headers: [Required headers]
- Query params: [Parameters]
- Example:
  ```
  GET /resource?filter=value
  Authorization: Bearer {token}
  ```

**Response:**
- Status codes: [200, 400, 401, 404, 500]
- Body schema:
  ```json
  {
    "id": "string",
    "name": "string",
    "created_at": "ISO8601 timestamp"
  }
  ```

**Rate Limiting:** [Limits]

**Errors:**
- 400: [What causes this]
- 401: [What causes this]
```

## Gap Identification

When reviewing requirements, actively look for:

**Missing Information:**
- Undefined error scenarios
- Unspecified performance requirements
- Missing user flows or interaction details
- Unclear data ownership
- Undefined integration points

**Ambiguities:**
- Subjective terms without definitions ("fast", "easy", "secure")
- Conflicting requirements
- Unclear priorities
- Vague success criteria

**Inconsistencies:**
- Different terminology for same concept
- Conflicting timelines
- Contradictory requirements

**When gaps are found:**
1. Document the gap clearly
2. Formulate specific questions to fill the gap
3. Get answers from stakeholders
4. Update specification
5. Re-validate

## Specification Formats

### Markdown Format
Best for: Internal documentation, version control, developer-focused specs

**Advantages:**
- Easy to read and write
- Version control friendly
- Supports code blocks and tables
- Can be rendered as HTML

### PDF Format
Best for: Client deliverables, formal sign-off, presentations

**Advantages:**
- Professional appearance
- Consistent rendering across platforms
- Can include rich graphics

### OpenAPI/Swagger Format
Best for: API specifications

**Advantages:**
- Machine-readable
- Auto-generates documentation
- Supports testing tools
- Industry standard

### Confluence/Notion Format
Best for: Team collaboration, living documents

**Advantages:**
- Real-time collaboration
- Rich media support
- Comments and discussions
- Easy to organize

## Tips for Effective Specification Creation

1. **Start with the problem, not the solution**
   - Understand the "why" before the "what"
   - Validate the problem exists

2. **Use concrete examples**
   - Include actual data samples
   - Show input/output examples
   - Demonstrate edge cases

3. **Define acceptance criteria upfront**
   - Make success measurable
   - Use specific, testable criteria

4. **Iterate early and often**
   - Share drafts for feedback
   - Validate assumptions
   - Refine based on questions

5. **Keep stakeholders aligned**
   - Regular check-ins during creation
   - Document decisions and rationale
   - Get sign-off on major decisions

6. **Version your specifications**
   - Track changes over time
   - Document what changed and why
   - Maintain history

7. **Link related specifications**
   - Reference dependencies
   - Cross-link related features
   - Maintain traceability

## When to Use This Skill

Use specification creation when:
- Starting a new project or feature
- Converting client conversations into formal requirements
- Documenting an existing system
- Preparing for development handoff
- Resolving ambiguous or conflicting requirements
- Creating API or integration documentation
- Defining design systems or component libraries

Specifications are especially valuable for:
- Complex features with multiple stakeholders
- Projects requiring formal approval or sign-off
- Systems with compliance requirements
- Features requiring cross-team coordination
- Long-term projects needing documentation
