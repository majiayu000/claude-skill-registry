---
name: ln-634-test-coverage-auditor
description: Coverage Gaps audit worker (L3). Identifies missing tests for critical paths (Money 20+, Security 20+, Data Integrity 15+, Core Flows 15+). Returns list of untested critical business logic with priority justification.
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Coverage Gaps Auditor (L3 Worker)

Specialized worker identifying missing tests for critical business logic.

## Purpose & Scope

- **Worker in ln-630 coordinator pipeline**
- Audit **Coverage Gaps** (Category 4: High Priority)
- Identify untested critical paths
- Classify by category (Money, Security, Data, Core Flows)
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md#audit-coordinator--worker-contract` for contextStore structure.

Receives `contextStore` with: `tech_stack`, `testFilesMetadata`, `codebase_root`, `output_dir`.

**Domain-aware:** Supports `domain_mode` + `current_domain` (see `audit_output_schema.md#domain-aware-worker-output`).

## Workflow

1) **Parse context** — extract fields, determine `scan_path` (domain-aware if specified)
     ELSE:
       scan_path = codebase_root
       domain_name = null
     ```

2) **Identify critical paths in scan_path** (not entire codebase)
   - Scan production code in `scan_path` for money/security/data keywords
   - All Grep/Glob patterns use `scan_path` (not codebase_root)
   - Example: `Grep(pattern="payment|refund|discount", path=scan_path)`

3) **Check test coverage for each critical path**
   - Search ALL test files for coverage (tests may be in different location than production code)
   - Match by function name, module name, or test description

4) **Collect missing tests**
   - Tag each finding with `domain: domain_name` (if domain-aware)

5) **Calculate Score:** Count violations by severity, calculate compliance score (X/10)

6) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/634-coverage-gaps.md` (or `{output_dir}/634-coverage-gaps-{domain}.md` if domain-aware) in single Write call

7) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Critical Paths Classification

### 1. Money Flows (Priority 20+)

**What:** Any code handling financial transactions

**Examples:**
- Payment processing (`/payment`, `processPayment()`)
- Discounts/promotions (`calculateDiscount()`, `applyPromoCode()`)
- Tax calculations (`calculateTax()`, `getTaxRate()`)
- Refunds (`processRefund()`, `/refund`)
- Invoices/billing (`generateInvoice()`, `createBill()`)
- Currency conversion (`convertCurrency()`)

**Min Priority:** 20

**Why Critical:** Money loss, fraud, legal compliance

### 2. Security Flows (Priority 20+)

**What:** Authentication, authorization, encryption

**Examples:**
- Login/logout (`/login`, `authenticate()`)
- Token refresh (`/refresh-token`, `refreshAccessToken()`)
- Password reset (`/forgot-password`, `resetPassword()`)
- Permissions/RBAC (`checkPermission()`, `hasRole()`)
- Encryption/hashing (custom crypto logic, NOT bcrypt/argon2)
- API key validation (`validateApiKey()`)

**Min Priority:** 20

**Why Critical:** Security breach, data leak, unauthorized access

### 3. Data Integrity (Priority 15+)

**What:** CRUD operations, transactions, validation

**Examples:**
- Critical CRUD (`createUser()`, `deleteOrder()`, `updateProduct()`)
- Database transactions (`withTransaction()`)
- Data validation (custom validators, NOT framework defaults)
- Data migrations (`runMigration()`)
- Unique constraints (`checkDuplicateEmail()`)

**Min Priority:** 15

**Why Critical:** Data corruption, lost data, inconsistent state

### 4. Core User Journeys (Priority 15+)

**What:** Multi-step flows critical to business

**Examples:**
- Registration → Email verification → Onboarding
- Search → Product details → Add to cart → Checkout
- Upload file → Process → Download result
- Submit form → Approval workflow → Notification

**Min Priority:** 15

**Why Critical:** Broken user flow = lost customers

## Audit Rules

### 1. Identify Critical Paths

**Process:**
- Scan codebase for money-related keywords: `payment`, `refund`, `discount`, `tax`, `price`, `currency`
- Scan for security keywords: `auth`, `login`, `password`, `token`, `permission`, `encrypt`
- Scan for data keywords: `transaction`, `validation`, `migration`, `constraint`
- Scan for user journeys: multi-step flows in routes/controllers

### 2. Check Test Coverage

**For each critical path:**
- Search test files for matching test name/description
- If NO test found → add to missing tests list
- If test found but inadequate (only positive, no edge cases) → add to gaps list

### 3. Categorize Gaps

**Severity by Priority:**
- **CRITICAL:** Priority 20+ (Money, Security)
- **HIGH:** Priority 15-19 (Data, Core Flows)
- **MEDIUM:** Priority 10-14 (Important but not critical)

### 4. Provide Justification

**For each missing test:**
- Explain WHY it's critical (money loss, security breach, etc.)
- Suggest test type (E2E, Integration, Unit)
- Estimate effort (S/M/L)

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

**Severity mapping by Priority:**
- Priority 20+ (Money, Security) missing test → CRITICAL
- Priority 15-19 (Data Integrity, Core Flows) missing test → HIGH
- Priority 10-14 (Important) missing test → MEDIUM
- Priority <10 (Nice-to-have) → LOW

## Output Format

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/634-coverage-gaps.md` (global) or `{output_dir}/634-coverage-gaps-{domain}.md` (domain-aware) with `category: "Coverage Gaps"` and checks: money_flow_coverage, security_flow_coverage, data_integrity_coverage, core_journey_coverage.

Return summary to coordinator:
```
Report written: docs/project/.audit/ln-630/{YYYY-MM-DD}/634-coverage-gaps.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

- **Domain-aware scanning:** If `domain_mode="domain-aware"`, scan ONLY `scan_path` production code (not entire codebase)
- **Tag findings:** Include `domain` field in each finding when domain-aware
- **Test search scope:** Search ALL test files for coverage (tests may be in different location than production code)
- **Match by name:** Use function name, module name, or test description to match tests to production code

## Definition of Done

- contextStore parsed successfully (including output_dir, domain_mode, current_domain)
- scan_path determined (domain path or codebase root)
- Critical paths identified in scan_path (Money, Security, Data, Core Flows)
- Test coverage checked for each critical path
- Missing tests collected with severity, priority, justification, domain
- Score calculated using penalty algorithm
- Report written to `{output_dir}/634-coverage-gaps.md` or `634-coverage-gaps-{domain}.md` (atomic single Write call)
- Summary returned to coordinator

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
