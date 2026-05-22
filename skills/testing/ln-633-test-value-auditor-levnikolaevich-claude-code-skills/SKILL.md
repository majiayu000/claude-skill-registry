---
name: ln-633-test-value-auditor
description: Risk-Based Value audit worker (L3). Calculates Usefulness Score = Impact (1-5) × Probability (1-5) for each test. Returns KEEP/REVIEW/REMOVE decisions based on thresholds (≥15 KEEP, 10-14 REVIEW, <10 REMOVE).
allowed-tools: Read, Grep, Glob, Bash
---

# Risk-Based Value Auditor (L3 Worker)

Specialized worker calculating Usefulness Score for each test.

## Purpose & Scope

- **Worker in ln-630 coordinator pipeline**
- Audit **Risk-Based Value** (Category 3: Critical Priority)
- Calculate Usefulness Score = Impact × Probability
- Make KEEP/REVIEW/REMOVE decisions
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with Impact/Probability matrices, test file list.

## Workflow

1) Parse context
2) For each test: calculate Usefulness Score
3) Classify: KEEP (≥15), REVIEW (10-14), REMOVE (<10)
4) Collect findings
5) Calculate score
6) Return JSON

## Usefulness Score Calculation

### Formula

```
Usefulness Score = Business Impact (1-5) × Failure Probability (1-5)
```

### Impact Scoring (1-5)

| Score | Impact | Examples |
|-------|--------|----------|
| **5** | **Critical** | Money loss, security breach, data corruption |
| **4** | **High** | Core flow breaks (checkout, login, registration) |
| **3** | **Medium** | Feature partially broken, degraded UX |
| **2** | **Low** | Minor UX issue, cosmetic bug |
| **1** | **Trivial** | Cosmetic issue, no user impact |

### Probability Scoring (1-5)

| Score | Probability | Indicators |
|-------|-------------|------------|
| **5** | **Very High** | Complex algorithm, new technology, many dependencies |
| **4** | **High** | Multiple dependencies, concurrency, edge cases |
| **3** | **Medium** | Standard CRUD, framework defaults, established patterns |
| **2** | **Low** | Simple logic, well-established library, trivial operation |
| **1** | **Very Low** | Trivial assignment, framework-generated, impossible to break |

### Decision Thresholds

| Score Range | Decision | Action |
|-------------|----------|--------|
| **≥15** | **KEEP** | Test is valuable, maintain it |
| **10-14** | **REVIEW** | Consider if E2E already covers this |
| **<10** | **REMOVE** | Delete test, not worth maintenance cost |

## Scoring Examples

### Example 1: Payment Processing Test

```
Test: "processPayment calculates discount correctly"
Impact: 5 (Critical — money calculation)
Probability: 4 (High — complex algorithm, multiple payment gateways)
Usefulness Score = 5 × 4 = 20
Decision: KEEP
```

### Example 2: Email Validation Test

```
Test: "validateEmail returns true for valid email"
Impact: 2 (Low — minor UX issue if broken)
Probability: 2 (Low — simple regex, well-tested library)
Usefulness Score = 2 × 2 = 4
Decision: REMOVE (likely already covered by E2E registration test)
```

### Example 3: Login Flow Test

```
Test: "login with valid credentials returns JWT"
Impact: 4 (High — core flow)
Probability: 3 (Medium — standard auth flow)
Usefulness Score = 4 × 3 = 12
Decision: REVIEW (if E2E covers, remove; else keep)
```

## Audit Rules

### 1. Calculate Score for Each Test

**Process:**
- Read test file, extract test name/description
- Analyze code under test (CUT)
- Determine Impact (1-5)
- Determine Probability (1-5)
- Calculate Usefulness Score

### 2. Classify Decisions

**KEEP (≥15):**
- High-value tests (money, security, data integrity)
- Core flows (checkout, login)
- Complex algorithms

**REVIEW (10-14):**
- Medium-value tests
- Question: "Is this already covered by E2E?"
- If yes → REMOVE; if no → KEEP

**REMOVE (<10):**
- Low-value tests (cosmetic, trivial)
- Framework/library tests
- Duplicates of E2E tests

### 3. Identify Patterns

**Common low-value tests (<10):**
- Testing framework behavior
- Testing trivial getters/setters
- Testing constant values
- Testing type annotations

## Scoring Algorithm (for compliance)

```
total_tests = KEEP + REVIEW + REMOVE
remove_percentage = (REMOVE / total_tests) * 100
score = 10 - (remove_percentage / 10)  // penalize for wasteful tests
score = max(0, min(10, score))
```

## Output Format

```json
{
  "category": "Risk-Based Value",
  "score": 7,
  "total_tests": 65,
  "keep_count": 35,
  "review_count": 15,
  "remove_count": 15,
  "findings": [
    {
      "test_file": "payment.test.ts",
      "test_name": "processPayment calculates discount correctly",
      "location": "payment.test.ts:45-68",
      "impact": 5,
      "probability": 4,
      "usefulness_score": 20,
      "decision": "KEEP",
      "reason": "Critical money calculation, complex algorithm"
    },
    {
      "test_file": "utils.test.ts",
      "test_name": "validateEmail returns true for valid email",
      "location": "utils.test.ts:23-27",
      "impact": 2,
      "probability": 2,
      "usefulness_score": 4,
      "decision": "REMOVE",
      "reason": "Low value, likely covered by E2E registration test",
      "effort": "S"
    },
    {
      "test_file": "auth.test.ts",
      "test_name": "login with valid credentials returns JWT",
      "location": "auth.test.ts:12-25",
      "impact": 4,
      "probability": 3,
      "usefulness_score": 12,
      "decision": "REVIEW",
      "question": "Is this already covered by E2E login test?",
      "effort": "S"
    }
  ]
}
```

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
