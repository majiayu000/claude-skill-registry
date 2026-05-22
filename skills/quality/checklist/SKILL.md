---
name: checklist
description: "Generate quality validation checklist from spec, plan, and tasks. Use after creating tasks. Triggers on: create checklist, quality checklist, validation checklist."
---

# Quality Validation Checklist Generator

Generate domain-specific quality checklists to validate implementation completeness.

---

## SpecKit Workflow

This skill runs **after tasks, before analyze**:

specify → plan → tasks → **checklist** → analyze → implement

Purpose:
- Generate validation checklist from spec/plan/tasks
- **Ensure quality gates are defined**
- **Ensure TDD requirements are included**
- **Ensure routing compliance is checked**
- Provide implement phase with verification criteria

---

## TDD is MANDATORY

Every generated checklist MUST include these testing items:

### Testing & TDD (Required for ALL stories)
- [ ] Unit tests written BEFORE implementation
- [ ] Unit tests verified to FAIL before coding
- [ ] Integration tests for API/data flows
- [ ] E2E tests for user-facing flows
- [ ] Test coverage meets 80% target
- [ ] All tests pass

**These items are non-negotiable and must appear in every checklist.**

---

## Mandatory Quality Gates

Every story in the checklist MUST include:

### Quality Gates (Non-Negotiable)
- [ ] `bun run typecheck` passes with 0 errors
- [ ] `bun run lint` passes with 0 errors AND 0 warnings
- [ ] `bun test` passes
- [ ] No debug code (console.log, debugger)
- [ ] No unused imports or variables

**All three commands must pass - no exceptions.**

---

## Routing Validation Items

Every checklist MUST include:

### Routing Compliance
- [ ] Routing preference documented in spec.md
- [ ] prd.json has routing metadata for all stories
- [ ] Complexity classifications match story scope
- [ ] Estimated costs are reasonable
- [ ] Mode selection (free/cheap/good/genius) is appropriate

---

## The Job

1. Read spec.md, plan.md, and tasks.md
2. Extract quality requirements from constitution
3. **Include mandatory TDD items**
4. **Include mandatory quality gate items**
5. **Include routing compliance items**
6. Generate comprehensive checklist
7. Save to `checklist.md`

**Important:** Checklist items get merged into prd.json acceptance criteria!

---

## Step 1: Locate Feature Files

Verify these files exist:
- `relentless/features/NNN-feature/spec.md`
- `relentless/features/NNN-feature/plan.md`
- `relentless/features/NNN-feature/tasks.md`

---

## Step 2: Load Context

Read:
1. `relentless/constitution.md` - Quality standards and requirements
2. Feature files (spec, plan, tasks)
3. Identify the feature domain (auth, payments, dashboard, etc.)

---

## Step 3: Generate Checklist Categories

Create 7-10 categories based on feature domain:

**Mandatory Categories (always include):**
- **0. Quality Gates** - typecheck, lint, test
- **1. TDD Compliance** - tests before code
- **2. Routing Compliance** - metadata validation

**Common Categories (include as needed):**
- Schema & Database
- Backend Logic
- Frontend Components (if applicable)
- API Integration
- Security & Permissions
- Performance & UX
- Documentation

If you have any doubts or suggestions about the checklist, please, interview the user.
---

## Step 4: Generate Checklist Items

For each category, create 5-10 specific validation items:

**Format:**
```markdown
- [ ] CHK-001 [US-001] Specific, testable requirement
- [ ] CHK-002 [Gap] Missing specification identified
- [ ] CHK-003 [Ambiguity] Unclear requirement needs clarification
- [ ] CHK-004 [Edge Case] Potential edge case to handle
```

**Guidelines:**
- 80% of items should reference specific user stories `[US-XXX]`
- 20% should identify gaps, ambiguities, or edge cases
- Each item must be specific and testable
- Total: 30-50 items across all categories

---

## Step 5: Reference Constitution

Ensure checklist includes items for constitution MUST rules:
- Type safety requirements (no `any` types)
- Testing coverage (80% minimum)
- Security standards
- Performance expectations
- Code quality standards (0 lint warnings)

---

## Step 6: Save & Report

1. Save to `relentless/features/NNN-feature/checklist.md`
2. Report:
   - Total checklist items: N
   - Items per category
   - Mandatory items included: TDD ✓, Quality Gates ✓, Routing ✓
   - Constitution compliance items: N
   - Gaps identified: N
   - Next step: `/relentless.convert` (if not done) or `/relentless.analyze`

---

## Example Checklist

```markdown
# Quality Checklist: User Authentication

**Purpose:** Validate completeness of user authentication implementation
**Created:** 2026-01-11
**Feature:** [spec.md](./spec.md)

## 0. Quality Gates (MANDATORY - Every Story)

- [ ] CHK-001 `bun run typecheck` passes with 0 errors
- [ ] CHK-002 `bun run lint` passes with 0 errors AND 0 warnings
- [ ] CHK-003 `bun test` passes
- [ ] CHK-004 No debug code (console.log, debugger statements)
- [ ] CHK-005 No unused imports or variables

## 1. TDD Compliance (MANDATORY)

- [ ] CHK-006 Tests written BEFORE implementation code
- [ ] CHK-007 Tests verified to FAIL before writing implementation
- [ ] CHK-008 Unit test coverage ≥80%
- [ ] CHK-009 Integration tests for all API endpoints
- [ ] CHK-010 E2E tests for complete user flows

## 2. Routing Compliance (MANDATORY)

- [ ] CHK-011 Routing preference documented in spec.md
- [ ] CHK-012 prd.json has routing metadata for all stories
- [ ] CHK-013 Complexity classifications correct for story scope
- [ ] CHK-014 Estimated costs are reasonable
- [ ] CHK-015 Mode selection appropriate for complexity

## 3. Schema & Database

- [ ] CHK-016 [US-001] User table has all required fields (id, email, password_hash, confirmed, timestamps)
- [ ] CHK-017 [US-001] Email field has UNIQUE constraint
- [ ] CHK-018 [US-001] Indexes created on frequently queried fields (email)
- [ ] CHK-019 [Gap] Consider adding last_login_at timestamp for analytics
- [ ] CHK-020 [US-001] Migration script tested on clean database

## 4. Backend Logic

- [ ] CHK-021 [US-001] Password hashing uses bcrypt with appropriate cost factor
- [ ] CHK-022 [US-001] Email validation prevents common typos and invalid formats
- [ ] CHK-023 [US-002] JWT tokens include user ID and expiration
- [ ] CHK-024 [US-002] Token verification handles expired tokens gracefully
- [ ] CHK-025 [Ambiguity] Password reset flow not specified - out of scope?

## 5. API Integration

- [ ] CHK-026 [US-001] POST /api/auth/register returns 201 on success
- [ ] CHK-027 [US-001] Register endpoint returns 400 for invalid email
- [ ] CHK-028 [US-001] Register endpoint returns 409 for duplicate email
- [ ] CHK-029 [US-002] POST /api/auth/login returns 401 for wrong password
- [ ] CHK-030 [US-002] Login endpoint returns 403 for unconfirmed account
- [ ] CHK-031 [Edge Case] Rate limiting on auth endpoints to prevent brute force

## 6. Testing & Validation

- [ ] CHK-032 [US-001] Unit tests for password hashing utility
- [ ] CHK-033 [US-001] Unit tests for email validation
- [ ] CHK-034 [US-002] Integration test for full registration flow
- [ ] CHK-035 [US-002] Integration test for login flow
- [ ] CHK-036 [US-003] E2E test for email confirmation
- [ ] CHK-037 [Constitution] Test coverage meets minimum 80% requirement

## 7. Security & Permissions

- [ ] CHK-038 [US-001] Passwords never logged or exposed in errors
- [ ] CHK-039 [US-001] Password requirements enforced (min length, complexity)
- [ ] CHK-040 [US-002] JWT secret stored in environment variable, not code
- [ ] CHK-041 [US-002] Token expiration validated on every request
- [ ] CHK-042 [Gap] Consider adding account lockout after N failed attempts

## 8. Performance & UX

- [ ] CHK-043 [US-001] Registration completes within 2 seconds
- [ ] CHK-044 [US-002] Login completes within 1 second
- [ ] CHK-045 [US-003] Confirmation email sent within 30 seconds
- [ ] CHK-046 [Edge Case] Graceful handling when email service is down

## 9. Documentation

- [ ] CHK-047 API endpoints documented with examples
- [ ] CHK-048 Environment variables documented in README
- [ ] CHK-049 Database schema documented
```

---

## Notes

- Checklist items will be merged into acceptance criteria during convert
- Reference user stories with `[US-XXX]` tags
- Identify gaps and ambiguities with `[Gap]` and `[Ambiguity]` tags
- Each item must be independently verifiable
- Balance between comprehensiveness and practicality
- **Mandatory sections (Quality Gates, TDD, Routing) must always be included**
