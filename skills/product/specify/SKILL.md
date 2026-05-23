---
name: specify
description: "Create feature specification from natural language description. Use when starting a new feature or creating a spec. Triggers on: create spec, specify feature, new feature spec."
---

# Feature Specification Generator

Create structured feature specifications from natural language descriptions.

---

## SpecKit Workflow

This skill is **Step 1 of 6** in the Relentless workflow:

**specify** → plan → tasks → analyze → implement (task by task) or relentless run --feature [FEATURE NAME] --tui

What flows to next step:
- User requirements → plan will create technical approach
- Routing preference → carried through all artifacts
- Acceptance criteria → basis for TDD in implementation

---

## TDD is MANDATORY

The specification MUST include testable acceptance criteria:
- Every user requirement should be verifiable with tests
- Test scenarios should be part of each story
- Edge cases should be documented for test coverage

**All acceptance criteria must be written in Given/When/Then format** to enable direct test implementation.

---

## The Job

1. Receive feature description from user
2. **Confirm routing preference (Step 0)**
3. Generate short name and feature number
4. Create branch and feature directory in `relentless/features/NNN-feature-name/`
5. Generate specification using template
6. Validate specification quality (including TDD readiness)
7. Save to `spec.md`

---

## Step 0: Confirm Routing Preference (BEFORE generating spec)

Ask the user these specific questions:

1. **"Which routing mode?"** (free/cheap/good/genius) - Default: `good`
2. **"Allow free models in fallback?"** - Default: `yes`
3. **"Specific harness/model preference?"** - Default: `auto`

Record the answer in spec.md metadata:
```
**Routing Preference**: auto: good | allow free: yes
<!-- Options: auto: free|cheap|good|genius | allow free: yes|no | OR specific: harness/model -->
```

---

## Step 1: Create Feature Structure

Run the create-new-feature script to set up the branch and directory:

```bash
.claude/skills/specify/scripts/bash/create-new-feature.sh --json "FEATURE_DESCRIPTION"
```

This will output JSON with:
- `BRANCH_NAME`: e.g., "003-user-auth"
- `SPEC_FILE`: Full path to spec.md
- `FEATURE_DIR`: Full path to feature directory
- `FEATURE_NUM`: e.g., "003"

**Important:** Parse this JSON and use these paths for all subsequent operations.

---

## Step 2: Load Constitution & Context

1. Read `relentless/constitution.md` for project governance
2. Note any MUST/SHOULD rules that apply to specifications
3. Keep these principles in mind while generating the spec
4. **Pay special attention to TDD requirements** - all features must be testable

---

## Step 3: Generate Specification

Using the template at `templates/spec.md`, create a specification with:

### Required Sections:

**1. Feature Overview**
- One-paragraph summary
- User value proposition
- Problem being solved

**2. User Scenarios & Testing**
- Concrete user stories with priorities (P1, P2, P3...)
- Step-by-step flows
- Expected outcomes
- **Given/When/Then acceptance scenarios (MANDATORY)**
- **Independent testability explanation for each story**

**3. Functional Requirements**
- What the system must do
- Testable requirements (no implementation details)
- Clear success criteria

**4. Test Strategy (MANDATORY)**
- Unit test approach
- Integration test scenarios
- Edge case tests
- Test data requirements

**5. Success Criteria**
- Measurable, technology-agnostic outcomes
- Quantitative metrics (time, performance, volume)
- Qualitative measures (user satisfaction, task completion)

**6. Key Entities (if applicable)**
- Data models and relationships
- Fields and types (logical, not implementation)

**7. Dependencies & Assumptions**
- External systems required
- Prerequisites
- Assumptions made

**8. Out of Scope**
- What this feature explicitly does NOT include
- Future considerations

---

## Step 4: Handle Ambiguities

If aspects are unclear:
- Interview the user first with questions to clarify any doubts, concerns or about his opinion on eventual ideas to improve the feature.
- Only mark `[NEEDS CLARIFICATION: specific question]` if:
  - Choice significantly impacts scope or UX
  - Multiple reasonable interpretations exist
  - No reasonable default exists
  - Question not already solved by interview
- **LIMIT: Maximum 3 clarifications**

If clarifications needed, present to user:

```markdown
## Clarification Needed

**Q1: [Topic]**
Context: [Quote spec section]
Question: [Specific question]

Options:
A. [Option 1] - [Implications]
B. [Option 2] - [Implications]
C. Custom - [Your answer]

Your choice: _
```

---

## Step 5: Validate Quality

Check the specification against:

### General Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] All requirements are testable
- [ ] Success criteria are measurable
- [ ] User scenarios cover primary flows
- [ ] Dependencies identified
- [ ] Scope clearly bounded
- [ ] No more than 3 `[NEEDS CLARIFICATION]` markers

### TDD Readiness (MANDATORY)
- [ ] Every user story has Given/When/Then acceptance criteria
- [ ] Acceptance criteria are specific enough to write tests against
- [ ] Edge cases are documented for test coverage
- [ ] Test strategy section is complete

### Routing Compliance
- [ ] Routing preference is recorded in metadata
- [ ] Routing choice is reasonable for feature complexity

If validation fails, revise and re-check (max 3 iterations).

---

## Step 6: Save & Report

1. Write complete specification to `SPEC_FILE` from JSON output
2. Create progress.txt if it doesn't exist:
   ```markdown
   ---
   feature: FEATURE_NAME
   started: DATE
   last_updated: DATE
   stories_completed: 0
   routing_preference: [auto: mode | allow free: yes/no]
   ---

   # Progress Log: FEATURE_NAME
   ```

3. Report to user:
   - Branch created: `BRANCH_NAME`
   - Spec saved: `SPEC_FILE`
   - Quality validation: PASSED/FAILED
   - TDD readiness: PASSED/FAILED
   - Routing preference: [recorded value]
   - Next step: `/relentless.plan` or `/relentless.clarify`

---

## Example Output

```markdown
# Feature: User Authentication

**Routing Preference**: auto: good | allow free: yes

## Overview
Enable users to create accounts and log in securely using email/password.

## User Scenarios

### User Story 1: New User Registration (Priority: P1)

User visits signup page, enters email and password, and creates an account.

**Why this priority**: Core functionality, blocks all other auth features.

**Independent Test**: Can be fully tested by registering a new account and verifying the account exists.

**Acceptance Scenarios**:

1. **Given** a visitor on the signup page, **When** they submit valid email and password, **Then** the account is created and confirmation email sent
2. **Given** an email already in use, **When** visitor tries to register, **Then** error message shown without revealing account exists

## Functional Requirements

**REQ-1:** System must validate email format
**REQ-2:** System must require passwords ≥ 8 characters
**REQ-3:** System must send confirmation email within 1 minute
**REQ-4:** System must hash passwords before storage

## Test Strategy (MANDATORY)

### Unit Test Approach
- Email validation logic
- Password strength validation
- Password hashing utility

### Integration Test Scenarios
- Full registration flow (submit form → create account → send email)
- Duplicate email rejection

### Edge Case Tests
- Invalid email formats (missing @, invalid domain)
- Password too short
- Unicode in email/password

### Test Data Requirements
- Valid test email addresses
- Various invalid email formats
- Password examples at boundary conditions

## Success Criteria

1. 95% of signups complete within 60 seconds
2. Zero plaintext passwords in database
3. Email confirmation rate > 80%

## Key Entities

**User**
- email: string (unique)
- password_hash: string
- confirmed: boolean
- created_at: timestamp

## Dependencies

- Email service provider (e.g., SendGrid, Mailgun)
- Session management system

## Out of Scope

- Social login (OAuth)
- Two-factor authentication
- Password reset (separate feature)
```

---

## Notes

- Always run the script first to get proper paths
- Use absolute paths from JSON output
- Validate before marking complete
- Keep specification technology-agnostic
- Focus on WHAT, not HOW
- **TDD readiness is non-negotiable** - all acceptance criteria must be testable
