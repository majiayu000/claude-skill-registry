---
name: ln-628-concurrency-auditor
description: Concurrency audit worker (L3). Checks race conditions, missing async/await, resource contention, thread safety, deadlock potential. Returns findings with severity, location, effort, recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

# Concurrency Auditor (L3 Worker)

Specialized worker auditing concurrency and async patterns.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline**
- Audit **concurrency** (Category 11: High Priority)
- Check race conditions, async/await, thread safety
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with tech stack, language, codebase root.

## Workflow

1) Parse context
2) Check concurrency patterns
3) Collect findings
4) Calculate score
5) Return JSON

## Audit Rules

### 1. Race Conditions
**Detection:**
- Shared state modified without synchronization
- Global variables accessed by multiple async functions
- Check for locks/mutexes usage

**Severity:**
- **CRITICAL:** Race condition in payment/auth
- **HIGH:** Race in user-facing feature
- **MEDIUM:** Race in background job

**Recommendation:** Use locks, atomic operations, message queues

**Effort:** M-L (redesign with synchronization)

### 2. Missing Async/Await
**Detection:**
- Callback hell: nested callbacks >3 levels
- Grep for `.then().then().then()`
- Find promises without await

**Severity:**
- **MEDIUM:** Callback hell (hard to maintain)
- **LOW:** Mixed Promise styles (then + await)

**Recommendation:** Convert to async/await

**Effort:** M (refactor control flow)

### 3. Resource Contention
**Detection:**
- Multiple file handles to same file
- Database connection pool exhausted
- Concurrent writes without locking

**Severity:**
- **HIGH:** File corruption risk
- **MEDIUM:** Performance degradation

**Recommendation:** Use connection pooling, file locking

**Effort:** M (add resource management)

### 4. Thread Safety Violations
**Detection (Go, Rust, Java):**
- Shared mutable state
- Missing `sync.Mutex` (Go)
- Missing `Arc<Mutex<T>>` (Rust)
- Missing `synchronized` (Java)

**Severity:**
- **HIGH:** Data corruption possible

**Recommendation:** Use thread-safe primitives

**Effort:** M (add synchronization)

### 5. Deadlock Potential
**Detection:**
- Multiple locks acquired in different order
- Lock held while calling external API

**Severity:**
- **HIGH:** Deadlock freezes application

**Recommendation:** Consistent lock ordering, timeout locks

**Effort:** L (redesign locking strategy)

## Scoring Algorithm

```
penalty = (critical * 2.0) + (high * 1.0) + (medium * 0.5) + (low * 0.2)
score = max(0, 10 - penalty)
```

## Output Format

```json
{
  "category": "Concurrency",
  "score": 7,
  "total_issues": 4,
  "critical": 0,
  "high": 2,
  "medium": 2,
  "low": 0,
  "findings": [
    {
      "severity": "HIGH",
      "location": "src/services/payment.ts:45",
      "issue": "Shared state 'balanceCache' modified without synchronization",
      "principle": "Thread Safety / Concurrency Control",
      "recommendation": "Use mutex or atomic operations for balanceCache updates",
      "effort": "M"
    }
  ]
}
```

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
