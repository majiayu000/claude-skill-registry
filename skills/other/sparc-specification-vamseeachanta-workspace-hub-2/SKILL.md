---
name: sparc-specification
description: SPARC Specification phase specialist for requirements analysis, constraint identification, use case definition, and acceptance criteria creation
version: 1.0.0
category: development
type: hybrid
capabilities:
  - requirements_gathering
  - constraint_analysis
  - acceptance_criteria
  - scope_definition
  - stakeholder_analysis
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
related_skills:
  - sparc-pseudocode
  - sparc-architecture
  - sparc-refinement
hooks:
  pre: |
    echo "SPARC Specification phase initiated"
    memory_store "sparc_phase" "specification"
    memory_store "spec_start_$(date +%s)" "Task: $TASK"
  post: |
    echo "Specification phase complete"
    memory_store "spec_complete_$(date +%s)" "Specification documented"
---

# SPARC Specification Agent

> Requirements analysis specialist focused on creating comprehensive, clear, and testable specifications for the SPARC methodology.

## Quick Start

```bash
# Invoke SPARC Specification phase

# Or directly in Claude Code
# "Use SPARC specification to define requirements for user authentication"
```

## When to Use

- Starting a new feature or project that needs clear requirements
- Translating stakeholder needs into technical specifications
- Creating acceptance criteria for user stories
- Documenting constraints (technical, business, regulatory)
- Defining use cases with preconditions and postconditions

## Prerequisites

- Clear understanding of project goals
- Access to stakeholders for requirements validation
- Knowledge of existing system constraints
- Understanding of compliance requirements (if applicable)

## Core Concepts

### SPARC Specification Phase

The Specification phase is the foundation of SPARC methodology:

1. **Define clear, measurable requirements** - Avoid ambiguity
2. **Identify constraints and boundaries** - Technical, business, regulatory
3. **Create acceptance criteria** - Testable pass/fail conditions
4. **Document edge cases and scenarios** - What happens when things go wrong
5. **Establish success metrics** - How to measure completion

### Requirement Types

| Type | Purpose | Example |
|------|---------|---------|
| Functional (FR) | What the system does | "System shall authenticate users via OAuth2" |
| Non-Functional (NFR) | Quality attributes | "API response time <200ms for 95% of requests" |
| Constraint | Limitations | "Must use existing PostgreSQL database" |

## Implementation Pattern

### Requirements Document Structure

```yaml
specification:
  functional_requirements:
    - id: "FR-001"
      description: "System shall authenticate users via OAuth2"
      priority: "high"
      acceptance_criteria:
        - "Users can login with Google/GitHub"
        - "Session persists for 24 hours"
        - "Refresh tokens auto-renew"

  non_functional_requirements:
    - id: "NFR-001"
      category: "performance"
      description: "API response time <200ms for 95% of requests"
      measurement: "p95 latency metric"

    - id: "NFR-002"
      category: "security"
      description: "All data encrypted in transit and at rest"
      validation: "Security audit checklist"
```

### Constraint Analysis

```yaml
constraints:
  technical:
    - "Must use existing PostgreSQL database"
    - "Compatible with Node.js 18+"
    - "Deploy to AWS infrastructure"

  business:
    - "Launch by Q2 2024"
    - "Budget: $50,000"
    - "Team size: 3 developers"

  regulatory:
    - "GDPR compliance required"
    - "SOC2 Type II certification"
    - "WCAG 2.1 AA accessibility"
```

### Use Case Definition

```yaml
use_cases:
  - id: "UC-001"
    title: "User Registration"
    actor: "New User"
    preconditions:
      - "User has valid email"
      - "User accepts terms"
    flow:
      1. "User clicks 'Sign Up'"
      2. "System displays registration form"
      3. "User enters email and password"
      4. "System validates inputs"
      5. "System creates account"
      6. "System sends confirmation email"
    postconditions:
      - "User account created"
      - "Confirmation email sent"
    exceptions:
      - "Invalid email: Show error"
      - "Weak password: Show requirements"
      - "Duplicate email: Suggest login"
```

### Acceptance Criteria (Gherkin)

```gherkin
Feature: User Authentication

  Scenario: Successful login
    Given I am on the login page
    And I have a valid account
    When I enter correct credentials
    And I click "Login"
    Then I should be redirected to dashboard
    And I should see my username
    And my session should be active

  Scenario: Failed login - wrong password
    Given I am on the login page
    When I enter valid email
    And I enter wrong password
    And I click "Login"
    Then I should see error "Invalid credentials"
    And I should remain on login page
    And login attempts should be logged
```

## Configuration

```yaml
# sparc-specification-config.yaml
specification_settings:
  output_format: "markdown"
  id_prefix: "FR-"
  priority_levels: ["critical", "high", "medium", "low"]

templates:
  requirements_doc: ".agent-os/specs/{spec-name}/spec.md"
  use_cases: ".agent-os/specs/{spec-name}/sub-specs/use-cases.md"

validation:
  require_acceptance_criteria: true
  require_priority: true
  require_testability: true
```

## Usage Examples

### Example 1: API Requirements

```markdown
# System Requirements Specification

## 1. Introduction
### 1.1 Purpose
This system provides user authentication and authorization...

### 1.2 Scope
- User registration and login
- Role-based access control
- Session management
- Security audit logging

### 1.3 Definitions
- **User**: Any person with system access
- **Role**: Set of permissions assigned to users
- **Session**: Active authentication state

## 2. Functional Requirements

### 2.1 Authentication
- FR-2.1.1: Support email/password login
- FR-2.1.2: Implement OAuth2 providers
- FR-2.1.3: Two-factor authentication

### 2.2 Authorization
- FR-2.2.1: Role-based permissions
- FR-2.2.2: Resource-level access control
- FR-2.2.3: API key management

## 3. Non-Functional Requirements

### 3.1 Performance
- NFR-3.1.1: 99.9% uptime SLA
- NFR-3.1.2: <200ms response time
- NFR-3.1.3: Support 10,000 concurrent users

### 3.2 Security
- NFR-3.2.1: OWASP Top 10 compliance
- NFR-3.2.2: Data encryption (AES-256)
- NFR-3.2.3: Security audit logging
```

### Example 2: Data Model Specification

```yaml
entities:
  User:
    attributes:
      - id: uuid (primary key)
      - email: string (unique, required)
      - passwordHash: string (required)
      - createdAt: timestamp
      - updatedAt: timestamp
    relationships:
      - has_many: Sessions
      - has_many: UserRoles

  Role:
    attributes:
      - id: uuid (primary key)
      - name: string (unique, required)
      - permissions: json
    relationships:
      - has_many: UserRoles

  Session:
    attributes:
      - id: uuid (primary key)
      - userId: uuid (foreign key)
      - token: string (unique)
      - expiresAt: timestamp
    relationships:
      - belongs_to: User
```

## Execution Checklist

- [ ] Gather requirements from stakeholders
- [ ] Define functional requirements with IDs
- [ ] Define non-functional requirements (performance, security)
- [ ] Document technical, business, regulatory constraints
- [ ] Create use cases with flows and exceptions
- [ ] Write acceptance criteria in Gherkin format
- [ ] Define data model entities and relationships
- [ ] Validate all requirements are testable
- [ ] Get stakeholder approval

## Best Practices

1. **Be Specific**: Avoid ambiguous terms like "fast" or "user-friendly"
2. **Make it Testable**: Each requirement should have clear pass/fail criteria
3. **Consider Edge Cases**: What happens when things go wrong?
4. **Think End-to-End**: Consider the full user journey
5. **Version Control**: Track specification changes
6. **Get Feedback**: Validate with stakeholders early

## Error Handling

| Issue | Resolution |
|-------|------------|
| Ambiguous requirements | Ask clarifying questions, use specific metrics |
| Missing acceptance criteria | Add testable pass/fail conditions |
| Conflicting requirements | Document and escalate to stakeholders |
| Scope creep | Reference original scope, create change request |

## Metrics & Success Criteria

- All requirements have unique IDs
- 100% of requirements have acceptance criteria
- All NFRs have measurable targets
- Stakeholder sign-off obtained
- Zero ambiguous requirements

## Integration Points

### MCP Tools

```javascript
// Store specification phase start
  action: "store",
  key: "sparc/specification/status",
  namespace: "coordination",
  value: JSON.stringify({
    phase: "specification",
    status: "in_progress",
    timestamp: Date.now()
  })
}
```

### Hooks

```bash
# Pre-specification hook

# Post-specification hook
```

### Related Skills

- [sparc-pseudocode](../sparc-pseudocode/SKILL.md) - Next phase: algorithm design
- [sparc-architecture](../sparc-architecture/SKILL.md) - System design phase
- [sparc-refinement](../sparc-refinement/SKILL.md) - TDD implementation phase

## References

- [Gherkin Syntax](https://cucumber.io/docs/gherkin/)
- [IEEE 830 SRS Standard](https://standards.ieee.org/)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from agent to skill format
