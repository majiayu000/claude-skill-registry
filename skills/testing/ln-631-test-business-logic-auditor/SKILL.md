---
name: ln-631-test-business-logic-auditor
description: Business Logic Focus audit worker (L3). Detects tests that validate framework/library behavior (Prisma, Express, bcrypt, JWT, axios, React hooks) instead of OUR code. Returns findings with REMOVE decisions.
allowed-tools: Read, Grep, Glob, Bash
---

# Business Logic Focus Auditor (L3 Worker)

Specialized worker auditing tests for Business Logic Focus (Category 1).

## Purpose & Scope

- **Worker in ln-630 coordinator pipeline**
- Audit **Business Logic Focus** (Category 1: High Priority)
- Detect tests validating framework/library behavior (NOT our code)
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with framework detection patterns, tech stack, test file list.

## Workflow

1) Parse context
2) Scan test files for framework/library tests
3) Collect findings
4) Calculate score
5) Return JSON

## Audit Rules

### 1. Framework Tests Detection

**What:** Tests validating framework behavior (Express, Fastify, Koa) instead of OUR business logic

**Detection Patterns:**
- `(express|fastify|koa).(use|get|post|put|delete|patch)`
- Test names: "middleware is called", "route handler works", "Express app listens"

**Severity:** **MEDIUM**

**Recommendation:** DELETE — framework already tested by maintainers

**Effort:** S (delete test file or test block)

### 2. ORM/Database Library Tests

**What:** Tests validating Prisma/Mongoose/Sequelize/TypeORM behavior

**Detection Patterns:**
- `(prisma|mongoose|sequelize|typeorm).(find|findMany|create|update|delete|upsert)`
- Test names: "Prisma findMany returns array", "Mongoose save works"

**Severity:** **MEDIUM**

**Recommendation:** DELETE — ORM already tested

**Effort:** S

### 3. Crypto/Hashing Library Tests

**What:** Tests validating bcrypt/argon2 hashing behavior

**Detection Patterns:**
- `(bcrypt|argon2).(hash|compare|verify|hashSync)`
- Test names: "bcrypt hashes password", "argon2 compares correctly"

**Severity:** **MEDIUM**

**Recommendation:** DELETE — crypto libraries already tested

**Effort:** S

### 4. JWT/Token Library Tests

**What:** Tests validating JWT signing/verification

**Detection Patterns:**
- `(jwt|jsonwebtoken).(sign|verify|decode)`
- Test names: "JWT signs token", "JWT verifies signature"

**Severity:** **MEDIUM**

**Recommendation:** DELETE — JWT library already tested

**Effort:** S

### 5. HTTP Client Library Tests

**What:** Tests validating axios/fetch/got behavior

**Detection Patterns:**
- `(axios|fetch|got|request).(get|post|put|delete|patch)`
- Test names: "axios makes GET request", "fetch returns data"

**Severity:** **MEDIUM**

**Recommendation:** DELETE — HTTP clients already tested

**Effort:** S

### 6. React Hooks/Framework Tests

**What:** Tests validating React hooks behavior (useState, useEffect, etc.)

**Detection Patterns:**
- `(useState|useEffect|useContext|useReducer|useMemo|useCallback)`
- Test names: "useState updates state", "useEffect runs on mount"

**Severity:** **LOW** (acceptable if testing OUR custom hook logic)

**Recommendation:** REVIEW — if testing framework behavior → DELETE; if testing custom hook → KEEP

**Effort:** S-M

## Scoring Algorithm

```
penalty = (medium * 0.5) + (low * 0.2)
score = max(0, 10 - penalty)
```

## Output Format

```json
{
  "category": "Business Logic Focus",
  "score": 7,
  "total_issues": 12,
  "medium": 10,
  "low": 2,
  "findings": [
    {
      "severity": "MEDIUM",
      "test_file": "auth.test.ts",
      "test_name": "bcrypt hashes password",
      "location": "auth.test.ts:45-52",
      "decision": "REMOVE",
      "usefulness_score": 3,
      "reason": "Tests bcrypt library behavior, not OUR code",
      "recommendation": "Delete test — bcrypt already tested by maintainers",
      "effort": "S"
    },
    {
      "severity": "MEDIUM",
      "test_file": "db.test.ts",
      "test_name": "Prisma findMany returns array",
      "location": "db.test.ts:78-85",
      "decision": "REMOVE",
      "usefulness_score": 4,
      "reason": "Tests Prisma ORM behavior, not OUR query logic",
      "recommendation": "Delete test — Prisma already tested",
      "effort": "S"
    }
  ]
}
```

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
