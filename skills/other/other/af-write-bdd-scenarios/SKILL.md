---
name: af-write-bdd-scenarios
description: Write BDD scenario specifications from requirements or mini-PRDs. Use when creating Markdown scenarios, classifying test types (unit/integration/E2E), enforcing glossary compliance, or defining acceptance criteria.

# AgentFlow documentation fields
title: BDD Expertise
created: 2025-10-29
updated: 2026-01-02
last_checked: 2026-01-02
tags: [skill, expertise, bdd, scenarios, testing, requirements]
parent: ../README.md
related:
  - ../../docs/guides/testing-guide.md
---

# BDD Expertise

## When to Use This Skill

Load this skill when you need to:
- Transform requirements into Markdown scenario specifications
- Write BDD scenarios with complete coverage
- Enforce glossary compliance in scenarios
- Design test coverage strategy
- Review scenario quality and completeness
- Understand Preconditions/Steps/Expected patterns

**Common triggers**:
- Refinement phase creates scenario specifications
- BDD-agent invoked by orchestrator
- Reviewing scenario coverage
- Adding new test scenarios
- Validating glossary compliance

## Quick Reference

BDD (Behavior-Driven Development) transforms requirements into executable specifications using domain language, comprehensive scenario coverage, and strict glossary compliance.

**Key principles:**
- Write in domain language (from glossary), not UI language or implementation details
- **Classify scenarios by test type**: E2E, Integration, Component, or Unit
- Scenarios are Markdown specifications that AI converts to tests
- Scenario → Test is direct (no intermediate Gherkin layer)

**Coverage requirements:** Every feature needs happy path, error, boundary, and validation scenarios.

**Test type classification (MUST specify for each scenario):**

| Type | Implementation | Use For |
|------|----------------|---------|
| E2E | Playwright | Full user journeys through real UI + real backend |
| Integration | Jest + SDK | Backend logic, API calls, cross-service behavior |
| Component | RTL (React Testing Library) | Component behavior, user interactions, accessibility |
| Unit | Jest (isolated) | Validation rules, pure functions, calculations |

**Output location:**
```
docs/requirements/mini-prd/[feature-name].md
├── Section 4: Scenarios       ← Markdown scenario specs
└── Section 5: Visual Specs    ← Storybook + RTL tests + Selector contract
```

### Scenarios Feed Test Generation

Scenarios written here become executable tests in Delivery phase:

```
Refinement phase (YOU ARE HERE):
  Write Markdown scenarios ──────────────────┐
  Define selector contract ──────────────────┤
                                             │
Delivery Phase (RED):                        │
  AI generates test files FROM scenarios: ◄──┘
    - E2E scenarios → Playwright specs
    - Integration scenarios → Jest tests
    - Component scenarios → RTL tests (often created in Refinement by ux-design-agent)
    - Unit scenarios → Jest tests
```

**Your job:** Write clear, complete scenarios with test type tags. AI handles conversion to executable tests.

See [Testing Expertise](../af-configure-test-frameworks/SKILL.md) for test writing timeline details.

## Rules

### Critical BDD Rules

1. **Always check glossary BEFORE writing scenarios** - Use approved terms only
2. **Every scenario set MUST link to Linear issue** - Reference in mini-PRD header
3. **Every scenario MUST have test type** - E2E, Integration, Component, or Unit
4. **Every scenario MUST have coverage category** - Happy, Error, Boundary, or Validation
5. **Minimum scenario coverage** - At least 1 happy path, 1 error case per feature
6. **Use domain language, not UI language** - "apply promo_code" not "click Submit button"
7. **No implementation details** - Behaviors only, not database/API calls
8. **Explicit actors always** - "the customer" not passive voice
9. **Measurable outcomes only** - Specific values, not "works correctly"
10. **Replace synonyms with approved terms** - Check glossary for exact wording
11. **Reference selector contract** - E2E and Component scenarios reference selectors

### Scenario Structure Rules

12. **Use Preconditions/Steps/Expected format** - Not Given/When/Then
13. **Scenarios live in mini-PRD Section 4** - Not separate .feature files
14. **Scenarios reference selector contract** - For testable UI elements
15. **Scenario names use sentence case** - "User signs up with valid email"
16. **Group scenarios by test type** - E2E first, then Integration, Component, Unit

### Quality Rules

17. **Keep scenarios focused** - One behavior per scenario
18. **Keep scenarios concise** - Under 10 items in Steps section
19. **Specific error messages** - Include exact wording in Expected section
20. **Use tables for data-driven scenarios** - When testing same behavior with different data

## Workflows

### Workflow: Creating Scenarios from Refinement

**When:** Refinement phase, transforming Linear issue into executable specification

**Procedure:**
```
1. Read glossary file
   Location: /docs/glossary.yml or .claude/templates/glossary.yml
   Check all approved terms, synonyms, forbidden terms

2. Extract Linear issue details
   - Issue ID for reference in mini-PRD
   - Acceptance criteria as scenario seeds
   - User stories for actor identification

3. Identify scenarios from acceptance criteria
   For each acceptance criterion:
   - What's the happy path?
   - What errors could occur?
   - What edge cases exist?
   - What validation is needed?

4. Classify each scenario by test type
   Ask for each scenario:
   - Does it require real UI + real backend? → E2E
   - Does it test backend/API without UI? → Integration
   - Does it test component behavior? → Component
   - Does it test pure logic? → Unit

5. Write scenarios in Markdown format
   For each scenario:
   - Test Type label
   - Selector contract reference (if UI involved)
   - Preconditions (initial state)
   - Steps (user/system actions)
   - Expected (verifiable outcomes)

6. Review for glossary compliance
   - All terms match approved glossary
   - No synonyms used
   - No forbidden terms present

7. Verify coverage completeness
   - At least 1 happy path
   - Relevant error cases
   - Boundary conditions where applicable
   - Input validation where applicable
```

### Workflow: Enforcing Glossary Compliance

**When:** Writing or reviewing any BDD scenario

**Procedure:**
```
1. Load glossary file
   .claude/templates/glossary.yml or /docs/glossary.yml

2. Identify all domain terms in scenario
   - Nouns (customer, order, promo_code)
   - Verbs (apply, submit, cancel)
   - States (active, expired, pending)

3. Check each term against glossary
   For each term:
   - Is it an approved term? → Use exactly as defined
   - Is it a synonym? → Replace with approved term
   - Is it forbidden? → Must replace
   - Is it missing? → Request glossary update

4. Apply replacements
   Examples:
   - "shopper" → "customer" (synonym)
   - "voucher" → "promo_code" (forbidden)
   - "discount code" → "promo_code" (synonym)

5. Verify snake_case for compound terms
   - promo_code (not promoCode or promo-code)
   - order_total (not orderTotal)
   - Apply consistently across all scenarios
```

### Workflow: Classifying Scenarios by Test Type

**When:** Writing scenarios, deciding which test type each belongs to

**Procedure:**
```
1. Ask: Is this a complete user journey through real UI + real backend?
   - YES → E2E (Playwright)
   - NO → Continue to step 2

2. Ask: Does this test backend/API behavior without UI?
   - YES → Integration (Jest + SDK)
   - NO → Continue to step 3

3. Ask: Does this test component behavior and user interaction?
   - YES → Component (RTL)
   - NO → Continue to step 4

4. It's pure logic/validation
   → Unit (Jest isolated)

Decision matrix:
┌────────────────────────────────────┬─────────────────┐
│ Scenario Type                      │ Test Type       │
├────────────────────────────────────┼─────────────────┤
│ User completes multi-page journey  │ E2E             │
│ Full signup → verify → dashboard   │ E2E             │
│ Cross-page navigation flow         │ E2E             │
├────────────────────────────────────┼─────────────────┤
│ JWT contains correct claims        │ Integration     │
│ Lambda creates tenant record       │ Integration     │
│ API returns correct error code     │ Integration     │
│ Cross-tenant access blocked        │ Integration     │
├────────────────────────────────────┼─────────────────┤
│ Button disables during submission  │ Component       │
│ Form shows validation errors       │ Component       │
│ Loading state displays correctly   │ Component       │
│ Accessible roles are correct       │ Component       │
├────────────────────────────────────┼─────────────────┤
│ Email format validation logic      │ Unit            │
│ Password strength calculation      │ Unit            │
│ Price discount calculation         │ Unit            │
│ Date formatting function           │ Unit            │
└────────────────────────────────────┴─────────────────┘
```

### Workflow: Reviewing Scenario Coverage

**When:** Before approving Refinement phase, during quality checks

**Procedure:**
```
1. Check mini-PRD structure
   ✅ Section 4 contains scenarios
   ✅ Section 5 contains selector contract
   ✅ Links to Linear issue present

2. Check scenario coverage
   ✅ At least 1 happy path scenario
   ✅ At least 1 error scenario
   ✅ Relevant boundary scenarios (limits, edges)
   ✅ Relevant validation scenarios (input checking)

3. Check test type distribution
   Guideline (not strict enforcement):
   - Unit: ~50% of scenarios
   - Component: ~20% of scenarios
   - Integration: ~20% of scenarios
   - E2E: ~10% of scenarios

   Flag unusual distributions for discussion, but don't block.

4. Review scenario quality
   Each scenario:
   ✅ Uses domain language (not UI language)
   ✅ No implementation details leaked
   ✅ Clear actor identification
   ✅ Measurable, specific outcomes
   ✅ References selector contract (if UI involved)

5. Verify glossary compliance
   ✅ All domain terms match glossary
   ✅ No synonyms used
   ✅ No forbidden terms present
   ✅ Consistent snake_case for compound terms

6. Check acceptance criteria coverage
   For each Linear acceptance criterion:
   ✅ Mapped to at least one scenario
   ✅ Happy path tested
   ✅ Error cases considered
```

## Scenario Format

### Markdown Scenario Structure

```markdown
## Scenarios

### E2E: User signs up with valid email
**Test Type:** E2E (complete user journey)
**Selectors:** AUTH.signup.*

**Preconditions:**
- User is not logged in
- Email address not already registered

**Steps:**
1. User navigates to /signup
2. User enters valid email and strong password
3. User submits form

**Expected:**
- Verification email sent
- User sees "Check your email" message
- User record created in Cognito (unverified)

---

### Component: Signup form disables submit when password weak
**Test Type:** Component (RTL)
**Selectors:** AUTH.signup.*

**Preconditions:**
- SignupForm component rendered
- Email field has valid email

**Steps:**
1. User types weak password (e.g., "weak")

**Expected:**
- Submit button is disabled
- Password error message visible: "Password is too short"
- Error has accessible role

---

### Unit: Password validation rules
**Test Type:** Unit (pure logic)

**Test cases:**
| Input | Expected Result |
|-------|-----------------|
| "weak" | { valid: false, errors: ["Too short", "No uppercase", "No number"] } |
| "WeakPass1" | { valid: true, errors: [] } |
| "nouppercaseornumber" | { valid: false, errors: ["No uppercase", "No number"] } |
```

### Selector Contract Reference

Scenarios that test UI elements must reference the selector contract:

```markdown
**Selectors:** AUTH.signup.*
```

The selector contract is defined in Section 5 of the mini-PRD and implemented in `/tests/selectors/[capability].ts`:

```typescript
// tests/selectors/auth.ts
export const AUTH = {
  signup: {
    form: 'signup-form',
    email: 'signup-email',
    password: 'signup-password',
    submit: 'signup-submit',
    successMessage: 'signup-success',
    passwordError: 'signup-password-error',
  },
};
```

## Examples

### Good: Domain Language (Not UI Language)

**✅ Correct - Domain-focused:**
```markdown
### E2E: Apply valid promo_code at checkout
**Test Type:** E2E
**Selectors:** CHECKOUT.promo.*

**Preconditions:**
- Customer is signed in
- Cart contains items totaling $100
- Active promo_code "SAVE10" exists with 10% discount

**Steps:**
1. Customer navigates to checkout
2. Customer applies promo_code "SAVE10"

**Expected:**
- order_total reduced to $90
- Success message: "Promo code applied successfully"
```

**❌ Wrong - UI-focused:**
```markdown
### Test: Click apply button with code

**Steps:**
1. I'm on the checkout page
2. I type "SAVE10" in the promo code text box
3. I click the green "Apply" button

**Expected:**
- The total field shows $90
- A green success banner appears
```

**Why wrong:** Describes UI interactions instead of business behavior.

### Good: No Implementation Details

**✅ Correct - Behavior-focused:**
```markdown
### Integration: Customer receives order confirmation
**Test Type:** Integration

**Preconditions:**
- Customer has completed checkout
- Payment processed successfully

**Steps:**
1. System processes payment completion

**Expected:**
- Confirmation email sent within 30 seconds
- Order status is "confirmed"
- Order appears in customer's order history
```

**❌ Wrong - Implementation leaked:**
```markdown
### Test: Send email after payment

**Steps:**
1. Row exists in orders table with status='pending'
2. POST /api/payments returns 200 OK

**Expected:**
- INSERT into email_queue with template_id=5
- UPDATE orders SET status='confirmed' WHERE id=123
```

**Why wrong:** Exposes database, API, and technical implementation.

### Good: Glossary Compliance

**✅ Correct - Approved terms:**
```markdown
**Preconditions:**
- The customer has an active promo_code

**Steps:**
1. Customer applies the promo_code at checkout

**Expected:**
- order_total reflects the discount
```

**❌ Wrong - Synonyms and forbidden terms:**
```markdown
**Preconditions:**
- The shopper has a valid voucher

**Steps:**
1. User enters the coupon code

**Expected:**
- Cart total is updated
```

**Why wrong:** Uses "shopper" (synonym), "voucher" (forbidden), "user" (synonym), "coupon" (forbidden), "cart" (should be "order" at checkout).

### Good: Complete Coverage Set

**✅ Correct - Comprehensive:**
```markdown
### E2E: Successfully apply valid promo_code
**Test Type:** E2E
...happy path...

### E2E: Reject expired promo_code
**Test Type:** E2E
...expiration error...

### Integration: Reject already-used single-use promo_code
**Test Type:** Integration
...usage limit error...

### Integration: Promo_code with minimum order - just under
**Test Type:** Integration
...boundary case below minimum...

### Component: Promo input shows format error
**Test Type:** Component
...format validation...

### Unit: Promo_code format validation
**Test Type:** Unit
| Input | Expected |
|-------|----------|
| "SAVE10" | valid |
| "save-10" | invalid (lowercase, hyphen) |
| "" | invalid (empty) |
```

**❌ Wrong - Only happy path:**
```markdown
### E2E: Apply promo code
...only tests success case...

# Missing: error scenarios, boundaries, validation
```

**Why wrong:** Incomplete coverage leads to bugs in production.

### Good: Component Scenario with RTL Focus

**✅ Correct - Behavior and accessibility focused:**
```markdown
### Component: Password field shows strength indicator
**Test Type:** Component (RTL)
**Selectors:** AUTH.signup.*

**Preconditions:**
- SignupForm component rendered
- Password field is empty

**Steps:**
1. User types "weak" in password field
2. User continues typing to "WeakPass1"

**Expected (after step 1):**
- Strength indicator shows "Weak"
- Indicator has aria-label "Password strength: weak"
- Submit button is disabled

**Expected (after step 2):**
- Strength indicator shows "Strong"
- Indicator has aria-label "Password strength: strong"
- Submit button is enabled
```

## Common Pitfalls

### 1. Skipping Glossary Check
**Problem:** Writing scenarios without consulting glossary first

**Impact:** Inconsistent terminology, rework required

**Solution:** Always read glossary BEFORE writing scenarios

### 2. Using UI Language
**Problem:** Describing button clicks instead of business actions

**Impact:** Scenarios break when UI changes, not reusable for API tests

**Solution:** Focus on "what" not "how" - business behavior, not UI mechanics

### 3. Leaking Implementation
**Problem:** Mentioning database, APIs, technical details in scenarios

**Impact:** Scenarios become brittle, hard to understand for non-technical stakeholders

**Solution:** Write for business audience - they shouldn't need to understand your tech stack

### 4. Vague Outcomes
**Problem:** "Then it works" or "User is happy"

**Impact:** Not testable, not measurable, not clear

**Solution:** Be specific - exact values, error messages, visible outcomes

### 5. Missing Test Type Classification
**Problem:** Scenarios without E2E/Integration/Component/Unit classification

**Impact:** No clear implementation path, all become slow E2E tests

**Solution:** Classify each scenario during writing - ask "What's the minimum test scope?"

### 6. All Scenarios as E2E
**Problem:** Everything classified as E2E

**Impact:** Slow test suite, brittle tests, expensive to maintain

**Solution:** Push tests down the pyramid - Unit for logic, Component for UI behavior, Integration for APIs, E2E only for critical journeys

### 7. Missing Selector Contract Reference
**Problem:** UI scenarios don't reference selector contract

**Impact:** Tests use arbitrary selectors, components don't have test IDs

**Solution:** Always specify which selector namespace scenarios use

### 8. Scenarios Too Long
**Problem:** 15+ steps in a single scenario

**Impact:** Hard to read, debug failures, maintain

**Solution:** Split into multiple focused scenarios, one behavior each

## Test Type Distribution Guidelines

The test pyramid ratio is a **guideline, not enforcement**:

| Feature Type | Typical Distribution |
|--------------|---------------------|
| Pure business logic | 70% unit, 20% integration, 5% component, 5% E2E |
| API-heavy workflow | 30% unit, 50% integration, 10% component, 10% E2E |
| UI-driven journey | 20% unit, 15% integration, 40% component, 25% E2E |
| Form-heavy feature | 30% unit, 10% integration, 50% component, 10% E2E |

**Agent behavior:**
- Observe the distribution after scenarios are written
- Flag unusual distributions for discussion
- Ask questions if the ratio seems off
- **Do NOT block progress** based on ratio alone

## Essential Reading

**For testing implementation patterns:**
- [Testing Guide](../../docs/guides/testing-guide.md) - Complete testing strategy, RTL patterns, E2E patterns

**For glossary template and structure:**
- [Glossary Template](../../templates/glossary.yml) - YAML format for approved terms

**For selector contract patterns:**
- [Selector Contract Template](../../templates/selector-contract.ts) - TypeScript selector structure

---

**Remember:**
1. Glossary compliance is mandatory, not optional
2. Domain language keeps scenarios stable as UI changes
3. Complete coverage (happy/error/boundary/validation) prevents bugs
4. Specific, measurable outcomes make scenarios testable
5. Test type classification determines implementation approach
6. Selector contracts bridge design and testing
