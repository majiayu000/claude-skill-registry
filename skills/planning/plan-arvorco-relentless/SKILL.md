---
name: plan
description: "Generate technical implementation plan from feature specification. Use after creating spec. Triggers on: create plan, technical plan, implementation design."
---

# Technical Implementation Plan Generator

Create detailed technical plans that translate feature specifications into implementation designs.

---

## SpecKit Workflow

This skill is **Step 2 of 6** in the Relentless workflow:

specify → **plan** → tasks → analyze → implement

What flows from spec:
- User requirements → technical approach
- Routing preference → carried forward
- Acceptance criteria → test specifications

What flows to tasks:
- Technical approach → implementation breakdown
- Test specifications → TDD acceptance criteria

---

## TDD is MANDATORY

The technical plan MUST include concrete test specifications:
- **Test file locations** (where tests will live)
- **Test class/function names** (what to create)
- **Mock/fixture requirements** (what test data needed)
- **Coverage targets** per component

**The agent MUST write tests BEFORE implementation code.**

This is non-negotiable. Plans without test specifications are incomplete.

---

## The Job

1. Read the feature specification (`spec.md`)
2. **Extract and validate routing preference (Step 2)**
3. Read project constitution for technical constraints
4. Generate technical architecture and implementation plan
5. **Include complete test specifications**
6. **Validate against quality gates**
7. Save to `plan.md` in the feature directory

---

## Step 1: Locate Feature Files

Find the current feature directory:
- Look in `relentless/features/` for the most recent feature
- Or ask user which feature to plan
- Verify `spec.md` exists

---

## Step 2: Extract Routing Preference

1. Read `spec.md` and extract routing preference
2. If missing, DEFAULT to: `auto: good | allow free: yes`
3. Validate format is correct
4. Carry forward to plan.md metadata
5. Update progress.txt with routing decision

Example:
```
Spec says: **Routing Preference**: auto: genius | allow free: no
Plan carries: **Routing Preference**: auto: genius | allow free: no
```

---

## Step 3: Load Context

Read these files:
1. **relentless/constitution.md** - Project governance and technical standards
2. **relentless/features/NNN-feature/spec.md** - Feature requirements
3. Project README or docs for tech stack information

Note all MUST and SHOULD rules from constitution - these are quality gates.

---

## Step 4: Generate Technical Plan

Using the template at `templates/plan.md`, create a plan with:

### Required Sections:

**1. Technical Overview**
- Architecture approach
- Key technologies to use (from constitution/existing stack)
- Integration points
- Routing preference carried from spec (auto mode or harness/model)

**2. Data Models**
- Database schemas
- Entity relationships
- Field definitions with types
- Indexes and constraints

**3. API Contracts**
- Endpoints and methods
- Request/response formats
- Authentication requirements
- Error responses

**4. Implementation Strategy**
- Phase breakdown
- Dependencies between components
- Integration approach

**5. Test Specifications (MANDATORY)**
- Test file structure
- Unit test table (component → test file → functions)
- Integration test table (flow → test file → scenarios)
- Mock requirements
- Coverage targets (minimum 80%)

**6. Security Considerations**
- Authentication/authorization
- Data validation
- Security best practices
- Compliance requirements

**7. Rollout Plan**
- Deployment strategy
- Migration requirements (if any)
- Monitoring and observability
- Rollback plan

---

## Step 5: Ensure Constitution Compliance

Validate the plan against constitution:

### Quality Gates Check

Before completing the plan, validate:
- [ ] **TDD approach defined** - test specs with file locations
- [ ] **Quality commands identified** - typecheck, lint, test
- [ ] **Routing preference carried** from spec
- [ ] **All MUST rules** from constitution addressed
- [ ] **No `any` types** planned in TypeScript
- [ ] **Error handling strategy** defined

**MUST** rules: Required, plan must follow these
**SHOULD** rules: Best practices, document any deviations

If plan violates MUST rules, revise until compliant.

If plan generates any doubts, interview the user about them with insightful questions to improve the plan.

---

## Step 6: Save & Validate

1. Save plan to `relentless/features/NNN-feature/plan.md`
2. **Run the validator to ensure plan.md is correctly formatted:**
   ```bash
   .claude/skills/validators/scripts/validate-plan.sh "relentless/features/NNN-feature/plan.md"
   ```
   - If validation fails, fix the errors and re-run
   - Warnings are acceptable but should be reviewed
3. Update progress.txt with plan creation timestamp and routing info
4. Report:
   - Plan location
   - Key technical decisions
   - Test specifications summary
   - Constitution compliance: PASS/FAIL
   - Validation: PASS/FAIL
   - Routing preference: [carried value]
   - Next step: `/relentless.tasks`

---

## Example Sections

```markdown
# Technical Implementation Plan: User Authentication

**Routing Preference**: auto: good | allow free: yes

## Technical Overview

**Architecture:** Three-tier (API, Service, Data)
**Stack:** Node.js, TypeScript, PostgreSQL
**Authentication:** JWT tokens with refresh mechanism

## Data Models

### User Table
\`\`\`sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  confirmed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
\`\`\`

## API Contracts

### POST /api/auth/register
**Request:**
\`\`\`json
{
  "email": "user@example.com",
  "password": "password123"
}
\`\`\`

**Response (201):**
\`\`\`json
{
  "id": "uuid",
  "email": "user@example.com",
  "message": "Confirmation email sent"
}
\`\`\`

## Test Specifications (MANDATORY)

### Test File Structure
\`\`\`
tests/
├── unit/
│   ├── auth/
│   │   ├── password.test.ts
│   │   └── email-validation.test.ts
│   └── token/
│       └── jwt.test.ts
├── integration/
│   └── auth/
│       ├── register.test.ts
│       └── login.test.ts
└── e2e/
    └── auth-flow.test.ts
\`\`\`

### Unit Tests
| Component | Test File | Functions to Test |
|-----------|-----------|-------------------|
| Password | `tests/unit/auth/password.test.ts` | hashPassword, verifyPassword |
| Email | `tests/unit/auth/email-validation.test.ts` | validateEmail |
| JWT | `tests/unit/token/jwt.test.ts` | generateToken, verifyToken |

### Integration Tests
| Flow | Test File | Scenarios |
|------|-----------|-----------|
| Register | `tests/integration/auth/register.test.ts` | success, duplicate email, invalid input |
| Login | `tests/integration/auth/login.test.ts` | success, wrong password, unconfirmed |

### Mock Requirements
- Database mock (in-memory or test container)
- Email service mock (no actual sends)
- Time mock for token expiration tests

### Coverage Targets
- Unit: 90% minimum (critical auth code)
- Integration: All happy paths + error paths
- E2E: Complete registration and login flow

## Constitution Compliance

**MUST Rules Checked:**
- [x] TDD is mandatory - test specs defined above
- [x] Quality gates defined - typecheck, lint, test commands
- [x] Routing preference carried from spec
- [x] No `any` types planned
- [x] Error handling strategy defined

**If any MUST rule cannot be satisfied, document the exception and remediation plan.**
```

---

## Notes

- Plan bridges WHAT (spec) to HOW (implementation)
- Include specific technologies and patterns
- Must comply with constitution
- Detailed enough for task generation
- Interview user if you have any doubts or suggestions
- **Test specifications are mandatory** - no tests = incomplete plan
- **Routing preference must be carried forward** from spec
