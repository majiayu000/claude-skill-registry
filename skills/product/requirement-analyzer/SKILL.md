---
name: requirement-analyzer
description: Analyzes ideas and extracts functional and non-functional requirements. Use when breaking down concepts into specific, measurable requirements. Identifies what needs to be built, constraints, and success criteria.
---

# Requirement Analyzer Skill

## Instructions

1. Analyze the provided idea or concept
2. Extract functional requirements (what the system should do)
3. Identify non-functional requirements (performance, security, scalability, etc.)
4. Determine constraints (technical, time, resource limitations)
5. Define acceptance criteria for each requirement
6. Prioritize requirements (must-have, should-have, nice-to-have)
7. Identify dependencies between requirements
8. Format requirements in a clear, structured format

## Examples

**Input:** "I want a user authentication system"
**Output:**
```markdown
## Functional Requirements

### Must-Have
- FR1: Users can register with email and password
  - Acceptance: User can create account, receives confirmation email
- FR2: Users can log in with email/password
  - Acceptance: Valid credentials grant access, invalid credentials show error
- FR3: Users can reset forgotten passwords
  - Acceptance: Password reset link sent via email, user can set new password

### Should-Have
- FR4: Users can log in with OAuth providers (Google, GitHub)
  - Acceptance: User can authenticate via OAuth, account linked to email

## Non-Functional Requirements

- NFR1: Authentication must complete in < 2 seconds
- NFR2: Passwords must be hashed using bcrypt (minimum 10 rounds)
- NFR3: System must support 10,000 concurrent users
- NFR4: All authentication endpoints must use HTTPS

## Constraints

- Must use existing database infrastructure
- Must comply with GDPR for user data
- Must integrate with existing email service

## Dependencies

- User database schema
- Email service API
- Session management system
```

**Input:** "Build a task management API"
**Output:**
```markdown
## Functional Requirements

### Must-Have
- FR1: Create, read, update, delete tasks
- FR2: Assign tasks to users
- FR3: Set task priorities and due dates
- FR4: Filter and search tasks

### Should-Have
- FR5: Task comments and attachments
- FR6: Task status workflow (todo, in-progress, done)

## Non-Functional Requirements

- NFR1: API response time < 200ms for 95% of requests
- NFR2: Support pagination for large result sets
- NFR3: RESTful API design following OpenAPI 3.0

## Constraints

- Must use PostgreSQL database
- Must support authentication via JWT tokens
```

## Format Guidelines

- Use clear requirement IDs (FR1, NFR1, etc.)
- Include acceptance criteria for each requirement
- Prioritize requirements clearly
- Identify technical and business constraints
- Note dependencies and integration points
