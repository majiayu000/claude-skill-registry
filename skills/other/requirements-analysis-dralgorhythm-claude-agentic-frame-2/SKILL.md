---
name: requirements-analysis
description: Analyze and refine product requirements. Use when clarifying scope, identifying gaps, or validating requirements. Covers requirement types and analysis techniques.
allowed-tools: Read, Write, Glob, Grep
---

# Requirements Analysis

## Requirement Types

### Functional Requirements
What the system should DO.
- "Users can log in with email and password"
- "System sends order confirmation email"

### Non-Functional Requirements
How the system should BEHAVE.
- Performance: "Page loads in < 2 seconds"
- Security: "Passwords stored with bcrypt"
- Scalability: "Supports 10,000 concurrent users"

### Constraints
Limitations on the solution.
- "Must use existing authentication system"
- "Must run on AWS"

## Analysis Techniques

### Ask "Why?" Five Times
Uncover the real requirement.

```
Requirement: "Add export to Excel button"
Why? → "Users need to share reports"
Why? → "Finance reviews monthly sales"
Why? → "They compare against targets"
Why? → "To identify underperforming regions"
Real Need: Regional performance dashboard
```

### SMART Criteria
Requirements should be:
- **S**pecific: Clear and unambiguous
- **M**easurable: Can verify completion
- **A**chievable: Technically feasible
- **R**elevant: Aligned with goals
- **T**ime-bound: Has deadline

### Edge Case Analysis
- What happens with no data?
- What happens with too much data?
- What if the user is offline?
- What if permissions are denied?

## Requirement Validation

- [ ] Is it testable?
- [ ] Is it achievable?
- [ ] Is it necessary?
- [ ] Is it consistent with other requirements?
- [ ] Is it complete?
- [ ] Is the priority clear?

## Documenting Requirements

```markdown
**REQ-001**: User Authentication

**Description**: Users must authenticate to access the system.

**Acceptance Criteria**:
1. Given valid credentials, user gains access
2. Given invalid credentials, user sees error
3. After 5 failed attempts, account is locked

**Priority**: Must Have
**Dependencies**: REQ-002 (User Management)
```
