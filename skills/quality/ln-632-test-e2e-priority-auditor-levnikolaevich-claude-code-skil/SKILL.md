---
name: ln-632-test-e2e-priority-auditor
description: E2E Critical Coverage audit worker (L3). Validates E2E coverage for critical paths (Money 20+, Security 20+, Data 15+). Pure risk-based - no pyramid percentages.
allowed-tools: Read, Grep, Glob, Bash
---

# E2E Critical Coverage Auditor (L3 Worker)

Specialized worker auditing E2E test coverage for critical paths (risk-based).

## Purpose & Scope

- **Worker in ln-630 coordinator pipeline**
- Audit **E2E Critical Coverage** (Category 2: High Priority)
- Validate E2E coverage for critical paths (Money/Security/Data Priority ≥20)
- Validate E2E coverage for core user journeys (Priority 15-19)
- Identify wasteful E2E tests (Usefulness Score <15)
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with risk-based testing philosophy, tech stack, codebase structure, test file list.

## Workflow

1) Parse context (critical paths, user journeys)
2) Identify critical paths in codebase (Money, Security, Data)
3) Identify core user journeys (multi-step flows)
4) Check E2E coverage for critical paths (Priority ≥20)
5) Check E2E coverage for user journeys (Priority 15-19)
6) Validate existing E2E tests (Usefulness Score ≥15)
7) Collect findings
8) Calculate score
9) Return JSON

## Audit Rules

### 1. Critical Path E2E Coverage

**Rule:** Every critical path MUST have E2E test

**Critical Paths (Priority ≥20):**
- **Money** (Priority 25): Payment processing, refunds, discounts, tax calculation
- **Security** (Priority 25): Login, auth, password reset, token refresh, permissions
- **Data Export** (Priority 20): Reports, CSV generation, data migration

**Detection:**
1. Scan codebase for critical keywords: `payment`, `refund`, `login`, `auth`, `export`
2. Extract critical functions/endpoints
3. Check if E2E test exists for each critical path
4. Missing E2E for Priority ≥20 → CRITICAL severity

**Severity:**
- **CRITICAL:** No E2E for Priority 25 (Money, Security)
- **HIGH:** No E2E for Priority 20 (Data Export)

**Recommendation:** Add E2E tests for critical paths immediately

**Effort:** M

### 2. Core User Journey E2E Coverage

**Rule:** Multi-step critical flows MUST have E2E test

**Core Journeys (Priority 15-19):**
- Registration → Email verification → First login (Priority 16)
- Product search → Add to cart → Checkout (Priority 18)
- File upload → Processing → Download result (Priority 15)

**Detection:**
1. Identify multi-step flows in routes/controllers
2. Check if end-to-end journey test exists
3. Missing E2E for Priority ≥15 → HIGH severity

**Severity:**
- **HIGH:** Missing E2E for core user journey (Priority ≥15)
- **MEDIUM:** Incomplete journey coverage (only partial steps tested)

**Recommendation:** Add end-to-end journey tests

**Effort:** M-L

### 3. E2E Test Usefulness Validation

**Rule:** Every E2E test MUST justify Priority ≥15

**Check:**
For each E2E test, calculate Usefulness Score = Impact × Probability
- If Score <15 → Flag as "Potentially wasteful E2E"
- Recommendation: Convert to Integration or Unit test (cheaper)

**Example:**
- E2E test for "API returns 200 OK" → Impact 2, Probability 1 → Score 2 → **WASTEFUL**
- E2E test for "Payment with discount calculates correctly" → Impact 5, Probability 5 → Score 25 → **VALUABLE**

**Severity:**
- **MEDIUM:** E2E test with Usefulness Score <15
- **LOW:** E2E test with Score 10-14 (review needed)

**Recommendation:** Convert low-value E2E to Integration/Unit or remove

**Effort:** S

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

**Severity mapping:**
- Missing E2E for Priority 25 (Money, Security) → CRITICAL
- Missing E2E for Priority 20 (Data Export) → HIGH
- Missing E2E for Priority 15-19 (Core Journeys) → HIGH
- Wasteful E2E (Score <15) → MEDIUM
- Incomplete journey coverage → LOW

## Output Format

**Return JSON to coordinator:**
```json
{
  "category": "E2E Critical Coverage",
  "score": 6,
  "total_issues": 8,
  "critical": 2,
  "high": 3,
  "medium": 2,
  "low": 1,
  "checks": [
    {"id": "critical_path_coverage", "name": "Critical Path Coverage", "status": "failed", "details": "Missing E2E for 2 Priority 25 paths (payment, auth)"},
    {"id": "user_journey_coverage", "name": "User Journey Coverage", "status": "warning", "details": "1 of 3 core journeys missing E2E"},
    {"id": "edge_case_coverage", "name": "Edge Case Coverage", "status": "passed", "details": "Error scenarios covered in existing E2E"}
  ],
  "findings": [
    {
      "severity": "CRITICAL",
      "location": "routes/payment.ts:45",
      "issue": "No E2E test for payment processing (POST /payment, Priority 25)",
      "principle": "E2E Critical Coverage / Money Flow",
      "recommendation": "Add E2E: successful payment + failed payment scenarios",
      "effort": "M"
    },
    {
      "severity": "HIGH",
      "location": "routes/auth.ts + routes/users.ts",
      "issue": "Missing E2E for user journey: Registration → Email verification → First login (Priority 16)",
      "principle": "E2E Critical Coverage / Core Journey",
      "recommendation": "Add E2E test covering full registration flow",
      "effort": "L"
    },
    {
      "severity": "MEDIUM",
      "location": "users.test.ts:23",
      "issue": "Low-value E2E test 'GET /users returns 200' (Usefulness Score 4 < 15)",
      "principle": "E2E Critical Coverage / Wasteful Test",
      "recommendation": "Convert to Integration test or remove",
      "effort": "S"
    }
  ]
}
```

## Reference Files

- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
