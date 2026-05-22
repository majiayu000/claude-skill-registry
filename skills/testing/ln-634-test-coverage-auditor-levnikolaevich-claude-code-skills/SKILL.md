---
name: ln-634-test-coverage-auditor
description: Coverage Gaps audit worker (L3). Identifies missing tests for critical paths (Money 20+, Security 20+, Data Integrity 15+, Core Flows 15+). Returns list of untested critical business logic with priority justification.
allowed-tools: Read, Grep, Glob, Bash
---

# Coverage Gaps Auditor (L3 Worker)

Specialized worker identifying missing tests for critical business logic.

## Purpose & Scope

- **Worker in ln-630 coordinator pipeline**
- Audit **Coverage Gaps** (Category 4: High Priority)
- Identify untested critical paths
- Classify by category (Money, Security, Data, Core Flows)
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with critical paths classification, codebase structure, test file list.

**Domain-aware fields (NEW):**
- `domain_mode`: `"domain-aware"` | `"global"` (optional, defaults to "global")
- `current_domain`: `{name, path}` when domain_mode="domain-aware"

**Example contextStore (domain-aware):**
```json
{
  "tech_stack": {...},
  "best_practices": {...},
  "testFilesMetadata": [...],
  "codebase_root": "/project",
  "domain_mode": "domain-aware",
  "current_domain": {
    "name": "orders",
    "path": "src/orders"
  }
}
```

## Workflow

1) **Parse context from contextStore**
   - Extract tech_stack, best_practices, testFilesMetadata
   - **Determine scan_path (NEW):**
     ```
     IF domain_mode == "domain-aware":
       scan_path = codebase_root + "/" + current_domain.path
       domain_name = current_domain.name
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

5) **Calculate score**

6) **Return JSON with domain metadata**
   - Include `domain` and `scan_path` fields (if domain-aware)

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

```
critical_paths = count of critical paths
tested_paths = count of critical paths with tests
coverage_percentage = (tested_paths / critical_paths) * 100
score = coverage_percentage / 10  // 100% coverage = 10 score
score = max(0, min(10, score))
```

## Output Format

**Global mode output:**
```json
{
  "category": "Coverage Gaps",
  "score": 6,
  "critical_paths_total": 25,
  "tested_paths": 15,
  "untested_paths": 10,
  "coverage_percentage": 60,
  "findings": [
    {
      "severity": "CRITICAL",
      "category": "Money",
      "missing_test": "E2E: Payment with discount code",
      "location": "services/payment.ts:processPayment()",
      "priority": 25,
      "justification": "Money calculation with discount logic — high risk of incorrect total",
      "test_type": "E2E",
      "effort": "M"
    }
  ]
}
```

**Domain-aware mode output (NEW):**
```json
{
  "category": "Coverage Gaps",
  "score": 7,
  "domain": "orders",
  "scan_path": "src/orders",
  "critical_paths_total": 12,
  "tested_paths": 8,
  "untested_paths": 4,
  "coverage_percentage": 67,
  "findings": [
    {
      "severity": "CRITICAL",
      "category": "Money",
      "missing_test": "E2E: applyDiscount() with edge cases",
      "location": "src/orders/services/order.ts:45",
      "priority": 25,
      "justification": "Discount calculation in orders domain — high risk of incorrect total",
      "test_type": "E2E",
      "effort": "M",
      "domain": "orders"
    },
    {
      "severity": "HIGH",
      "category": "Data Integrity",
      "missing_test": "Integration: orderTransaction() rollback",
      "location": "src/orders/repositories/order.ts:78",
      "priority": 18,
      "justification": "Data corruption risk in orders domain",
      "test_type": "Integration",
      "effort": "M",
      "domain": "orders"
    }
  ]
}
```

## Critical Rules

- **Domain-aware scanning:** If `domain_mode="domain-aware"`, scan ONLY `scan_path` production code (not entire codebase)
- **Tag findings:** Include `domain` field in each finding when domain-aware
- **Test search scope:** Search ALL test files for coverage (tests may be in different location than production code)
- **Match by name:** Use function name, module name, or test description to match tests to production code

## Definition of Done

- contextStore parsed (including domain_mode and current_domain)
- scan_path determined (domain path or codebase root)
- Critical paths identified in scan_path (Money, Security, Data, Core Flows)
- Test coverage checked for each critical path
- Missing tests collected with severity, priority, justification, domain
- Score calculated
- JSON returned to coordinator with domain metadata

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
