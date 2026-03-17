---
name: prd-v07-test-planning
description: Define test cases BEFORE implementation, ensuring every API, business rule, and user journey has verifiable acceptance criteria during PRD v0.7 Build Execution. Triggers on requests to define tests, plan test coverage, create test cases, or when user asks "define tests", "test planning", "what to test?", "test cases", "test coverage", "TEST-", "test-first". Consumes EPIC- (scope), API-, DBT-, BR-, UJ-. Outputs TEST- entries with Given-When-Then format. Feeds v0.7 Implementation Loop.
---

# Test Planning

Position in workflow: v0.7 Epic Scoping → **v0.7 Test Planning** → v0.7 Implementation Loop

## Core Principle: Test-First

> Tests are not an afterthought. They are the **contract** that defines what "done" means.
> If you can't write the test, you don't understand the requirement.

Write TEST- entries **before** writing code. This forces clarity about what you're building.

## Test Types

| Type | What It Tests | When to Use | Scope |
|------|---------------|-------------|-------|
| **Unit** | Single function/method | Business logic, calculations | Smallest unit |
| **Integration** | Component boundaries | API ↔ Database | Module level |
| **E2E** | Full user flow | Critical journeys | System level |
| **Contract** | API shape/types | External integrations | Interface level |
| **Performance** | Speed/load | Critical paths | Benchmark |

## Coverage Requirements

| ID Type | Minimum Coverage | Rationale |
|---------|------------------|-----------|
| **API-** | 1 happy path + 1 error case per endpoint | Endpoints are integration points |
| **BR-** | 1 test per rule, including boundary cases | Rules are product logic |
| **UJ-** | 1 E2E test per core journey | Journeys are user value |
| **DBT-** | Constraint tests for critical fields | Data integrity is foundational |

## Test Planning Process

1. **Pull EPIC- scope**
   - Which APIs, DBTs, BRs are included?

2. **For each API-**: Define request/response tests
   - Happy path: Valid input → expected output
   - Error cases: Invalid input, auth failures, not found

3. **For each BR-**: Define rule validation tests
   - Positive: Rule allows expected behavior
   - Negative: Rule blocks invalid behavior
   - Boundary: Edge cases at limits

4. **For each UJ-**: Define end-to-end flow tests
   - Complete journey from trigger to value moment

5. **For each DBT-**: Define data integrity tests
   - Constraints enforced (unique, not null)
   - Relationships maintained (FK integrity)

6. **Create TEST- entries** linked to implementation IDs

7. **Add TEST- references** back to EPIC-

## TEST- Output Template

```
TEST-XXX: [Test Name]
Type: [Unit | Integration | E2E | Contract | Performance]
Tests: [API-XXX | BR-XXX | UJ-XXX | DBT-XXX]
EPIC: [EPIC-XXX]

Given: [Preconditions — initial state]
When: [Action/trigger — what happens]
Then: [Expected outcome — what should result]

Validation Method: [Automated | Manual | Both]
Automation: [Test file path when implemented]
Priority: [Critical | High | Medium | Low]
```

**Example TEST- entries:**
```
TEST-001: User creation succeeds with valid data
Type: Integration
Tests: API-001 (POST /users), BR-001 (email uniqueness)
EPIC: EPIC-01

Given: No user with email "test@example.com" exists
When: POST /api/users with { email: "test@example.com", password: "Valid123!" }
Then:
  - Response status: 201 Created
  - Response body contains user id and email
  - User record exists in DBT-010 (users)
  - Password is hashed (not plaintext)

Validation Method: Automated
Automation: tests/api/users.test.ts
Priority: Critical
```

```
TEST-002: User creation fails with duplicate email
Type: Integration
Tests: API-001, BR-001 (email uniqueness)
EPIC: EPIC-01

Given: User with email "existing@example.com" already exists
When: POST /api/users with { email: "existing@example.com", password: "Valid123!" }
Then:
  - Response status: 409 Conflict
  - Response body: { error: { code: "EMAIL_EXISTS", message: "..." } }
  - No new user record created

Validation Method: Automated
Automation: tests/api/users.test.ts
Priority: Critical
```

```
TEST-003: User creation fails with weak password
Type: Unit
Tests: BR-002 (password requirements)
EPIC: EPIC-01

Given: Password validation function
When: Validate password "weak"
Then:
  - Returns false
  - Error message indicates minimum length requirement

Validation Method: Automated
Automation: tests/unit/validation.test.ts
Priority: High
```

```
TEST-010: Onboarding journey completes successfully
Type: E2E
Tests: UJ-000 (onboarding)
EPIC: EPIC-01

Given: New user on signup page
When: User completes signup → email verification → profile setup
Then:
  - User arrives at dashboard (SCR-001)
  - Welcome message displayed
  - User session is active
  - KPI-001 (activation) event tracked

Validation Method: Both (Automated + Manual verification)
Automation: tests/e2e/onboarding.spec.ts
Priority: Critical
```

## Test Priority Framework

| Priority | Criteria | Example |
|----------|----------|---------|
| **Critical** | Breaks core value, data loss possible | Auth, payments, data creation |
| **High** | Blocks key journey, user-facing error | Onboarding, main features |
| **Medium** | Degrades experience, workaround exists | Settings, secondary features |
| **Low** | Edge case, admin-only, cosmetic | Rare scenarios, admin tools |

## Writing Good Given-When-Then

### Good Examples

```
Given: User is logged in and has 3 existing reports
When: User clicks "Create Report" and fills required fields
Then: 4 reports now exist, new report appears at top of list
```

```
Given: User has reached the free tier limit of 5 reports
When: User attempts to create a 6th report
Then: Error message shows "Upgrade to create more reports"
      Create button is disabled
      Upgrade CTA is displayed
```

### Bad Examples

```
Given: The system is working
When: User does something
Then: It works correctly
```
(Too vague — what does "working" mean?)

```
Given: User
When: API
Then: Success
```
(No specifics — useless as a test spec)

## Test Categories by EPIC Phase

### For Database Schema (Window 1)
```
TEST-XXX: [Table] enforces [constraint]
TEST-XXX: [Table] allows valid data
TEST-XXX: RLS policy restricts access correctly
```

### For API Endpoints (Window 2)
```
TEST-XXX: [Method] [Path] returns [status] for [scenario]
TEST-XXX: [Method] [Path] enforces [BR-XXX]
TEST-XXX: [Method] [Path] handles [error case]
```

### For UI Integration (Window 3)
```
TEST-XXX: [Screen] loads data from [API-XXX]
TEST-XXX: [Form] validates input per [BR-XXX]
TEST-XXX: [UJ-XXX] completes end-to-end
```

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **Tests after code** | "We'll add tests later" | Define TEST- before writing code |
| **Only happy path** | No error case tests | Every API needs at least 1 error test |
| **Orphaned tests** | TEST- not linked to API-/BR-/UJ- | Every test must trace to a spec ID |
| **Test explosion** | 200+ tests for MVP | Focus on critical paths; 30-50 typical |
| **Vague assertions** | "System works correctly" | Specific, measurable outcomes |
| **No automation path** | Manual-only critical tests | Critical tests must be automatable |
| **Testing implementation** | Test verifies internal details | Test behavior, not implementation |

## Quality Gates

Before proceeding to Implementation Loop:

- [ ] Every API- endpoint has at least 2 TEST- entries (happy + error)
- [ ] Every BR- rule has at least 1 TEST- entry
- [ ] Every core UJ- journey has an E2E TEST-
- [ ] Critical tests are marked for automation
- [ ] TEST- entries added to EPIC- Section 2
- [ ] Total test count is reasonable (30-50 for MVP)

## Downstream Connections

TEST- entries feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **Implementation Loop** | TEST- defines acceptance criteria | EPIC done when TEST-001–010 pass |
| **EPIC Validation (Phase D)** | TEST- list for validation checklist | Run all TEST- for EPIC |
| **CI/CD** | TEST- becomes automated suite | TEST- entries → test files |
| **Code Review** | TEST- as review checklist | "Does PR pass TEST-005?" |

## Detailed References

- **Test planning examples**: See `references/examples.md`
- **TEST- entry template**: See `assets/test.md`
- **Test type decision guide**: See `references/test-types.md`
