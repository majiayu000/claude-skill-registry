---
name: ln-632-test-e2e-priority-auditor
description: E2E Critical Coverage audit worker (L3). Validates E2E coverage for critical paths (Money 20+, Security 20+, Data 15+). Pure risk-based - no pyramid percentages.
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

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

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md#audit-coordinator--worker-contract` for contextStore structure.

Receives `contextStore` with: `tech_stack`, `testFilesMetadata`, `codebase_root`, `output_dir`.

## Workflow

1) **Parse Context:** Extract tech stack, critical paths, user journeys, test file list, output_dir from contextStore
2) **Identify Critical Paths:** Scan codebase for critical paths (Money, Security, Data)
3) **Identify Core Journeys:** Identify core user journeys (multi-step flows)
4) **Check Critical Path Coverage:** Check E2E coverage for critical paths (Priority >=20)
5) **Check Journey Coverage:** Check E2E coverage for user journeys (Priority 15-19)
6) **Validate E2E Tests:** Validate existing E2E tests (Usefulness Score >=15)
7) **Collect Findings:** Record each violation with severity, location (file:line), effort estimate (S/M/L), recommendation
8) **Calculate Score:** Count violations by severity, calculate compliance score (X/10)
9) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/632-e2e-priority.md` in single Write call
10) **Return Summary:** Return minimal summary to coordinator (see Output Format)

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

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/632-e2e-priority.md` with `category: "E2E Critical Coverage"` and checks: critical_path_coverage, user_journey_coverage, e2e_usefulness_validation.

Return summary to coordinator:
```
Report written: docs/project/.audit/ln-630/{YYYY-MM-DD}/632-e2e-priority.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

- **Do not auto-fix:** Report only
- **Risk-based only:** Prioritize by business impact (Money > Security > Data), not by code coverage percentage
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Usefulness Score threshold:** Only flag E2E tests with Score <15 as wasteful
- **No pyramid enforcement:** Do not recommend E2E/Integration/Unit ratios — focus on critical path coverage

## Definition of Done

- contextStore parsed successfully (including output_dir)
- Critical paths identified (Money, Security, Data) with Priority scores
- All 3 checks completed (critical path coverage, user journey coverage, E2E usefulness validation)
- Findings collected with severity, location, effort, recommendation
- Score calculated using penalty algorithm
- Report written to `{output_dir}/632-e2e-priority.md` (atomic single Write call)
- Summary returned to coordinator

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
