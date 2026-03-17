---
name: failure-criteria
description: Immediate failure conditions that stop work
---

# Immediate Failure Conditions

Task FAILS immediately if any of these conditions are met:

## Critical Violations

### 1. Operation Naming
**Condition:** Operation name contains 'describe'
**Action:** STOP immediately, use 'get' instead
**Why:** 'describe' is reserved for AWS-style APIs. Use standard HTTP verbs.

### 2. Error Responses in API Spec
**Condition:** API spec contains 4xx or 5xx responses
**Action:** DELETE all error responses
**Why:** Framework handles errors automatically through core error types

### 3. Skipped Generation
**Condition:** Did not run `npm run clean && npm run generate` after API changes
**Result:** TASK FAILED
**Fix:** Must run generation before implementation

### 4. No Tests Written
**Condition:** Operation implemented without tests
**Result:** TASK FAILED
**Fix:** Tests are mandatory, not optional

### 5. Tests Not Executed
**Condition:** Tests written but not run
**Result:** TASK FAILED
**Fix:** Must execute `npm test` and verify pass

### 6. Build Not Verified
**Condition:** Did not run `npm run build`
**Result:** TASK FAILED
**Fix:** Must verify build succeeds before completion

### 7. Dependencies Not Locked
**Condition:** Did not run `npm run shrinkwrap`
**Result:** TASK FAILED
**Fix:** Must lock dependencies for npm package

### 8. Using Any Types
**Condition:** Used `Promise<any>` in method signatures
**Result:** TASK FAILED
**Fix:** Use generated types from generated/api/

### 9. Incomplete Execution
**Condition:** Stopped before Gate 6
**Result:** TASK INCOMPLETE
**Fix:** Continue working through all gates

### 10. Schema Context Violation
**Condition:** Schema used in BOTH nested and direct contexts without separation
**Criteria:** Schema has 10+ properties AND is referenced by other schemas AND has its own endpoint
**Action:** CREATE separate `{Schema}Summary` for nested usage
**Reference:** See api-specification.md Rule #19

### 11. Hardcoded Test Values
**Condition:** Integration tests contain hardcoded IDs or test data
**Examples:**
- ❌ `const userId = '12345'`
- ❌ `const email = 'test@example.com'`
**Action:** Move ALL test values to .env
**Process:**
1. Add to .env file
2. Export from test/integration/Common.ts
3. Import in integration tests
**Correct:**
- ✅ `const userId = TEST_USER_ID` (from .env via Common.ts)
**Reference:** See testing.md Rule #7

## Red Flags (Signs of Incomplete Work)

Watch for these indicators that work is not complete:

1. **No mention of tests** - MAJOR red flag
2. **"I've added the operation"** without test confirmation
3. **No `npm test` output shown**
4. **No build validation**
5. **Jumping to "done" after implementation**

## What User Should NEVER Have To Say

If user has to say any of these, **TASK HAS FAILED**:

- "Now write tests"
- "Did you test it?"
- "Run the tests"
- "Does it build?"
- "You forgot the tests"
- "Did you run shrinkwrap?"

## Enforcement Summary

| Rule | Violation = Task Failure |
|------|--------------------------|
| NEVER use 'describe' prefix | ✅ Yes |
| ONLY 200/201 responses | ✅ Yes |
| ALWAYS run generate after API changes | ✅ Yes |
| ALWAYS write tests | ✅ Yes |
| ALWAYS run tests | ✅ Yes |
| ALWAYS build and verify | ✅ Yes |
| ALWAYS run shrinkwrap | ✅ Yes |
| NO `Promise<any>` types | ✅ Yes |
| NO hardcoded test values in integration tests | ✅ Yes |

## Validation Priority

Gates must be passed in order:
1. Gate 1: API Specification
2. Gate 2: Type Generation
3. Gate 3: Implementation
4. Gate 4: Test Creation
5. Gate 5: Test Execution
6. Gate 6: Build

**GATES ARE NOT OPTIONAL**

Every operation MUST pass through ALL gates sequentially.
No shortcuts. No exceptions. Complete or fail.
