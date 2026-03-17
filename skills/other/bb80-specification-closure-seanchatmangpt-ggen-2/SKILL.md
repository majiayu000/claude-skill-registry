# Big Bang 80/20: Specification Closure Skill

**Auto-trigger**: Whenever you see "specification", "incomplete", "closure", "TBD", "undefined"

## Core Concept

Specification closure is the **gate before EPIC 9 fan-out**.

No implementation begins without closure verification. Iteration is a defect signal of incomplete specification.

## Closure Checklist

A specification is **closed** when:

### 1. Input Characterization
- [ ] All possible inputs are described
- [ ] Input constraints are explicit
- [ ] Edge cases are enumerated
- [ ] Invalid inputs are rejected clearly

**Example**:
```
CLOSED: "File input: 1MB-100MB, UTF-8 text, non-empty"
OPEN: "File input: any file the user provides"
```

### 2. Output Specification
- [ ] Observable behavior is specified (not just internal)
- [ ] Success criteria are measurable
- [ ] Invariants are documented
- [ ] Error outputs are defined

**Example**:
```
CLOSED: "Output: sorted array of tuples (name, score), score ∈ [0,100], alphabetical by name"
OPEN: "Output: processed data"
```

### 3. Acceptance Criteria
- [ ] At least 1 scenario per requirement
- [ ] Scenarios are testable (not vague)
- [ ] Happy path covered
- [ ] Edge cases covered
- [ ] Error paths covered

**Example**:
```
CLOSED:
  - Scenario 1: Normal case with 5 items → returns sorted list
  - Scenario 2: Empty list → returns empty
  - Scenario 3: File >100MB → returns error "File exceeds maximum size"

OPEN:
  - "Handle various inputs"
```

### 4. Non-Functional Requirements
- [ ] Performance targets (SLOs) specified
- [ ] Memory constraints stated
- [ ] Concurrency model described
- [ ] Security requirements listed

**Example**:
```
CLOSED:
  - Performance: Parse 1000 files in <5s (p99)
  - Memory: <100MB resident
  - Concurrency: Thread-safe, allow 10 concurrent operations
  - Security: Validate all file paths, reject directory traversal

OPEN:
  - "Should be fast"
  - "Keep memory low"
```

### 5. Ambiguity Resolution
- [ ] No undefined terms (define glossary if needed)
- [ ] No "TBD", "TODO", "maybe", "probably"
- [ ] No contradictions between requirements
- [ ] Scope explicitly bounded

**Example**:
```
CLOSED: "Cache strategy: LRU with 10,000 entry limit, 30min TTL"
OPEN: "Cache entries appropriately"

CLOSED: "Error handling: All Result<T, E> with custom Error enum. Never panic."
OPEN: "Handle errors gracefully"
```

## Red Flags (Incomplete Specification)

If you see ANY of these, specification is **NOT closed**:

| Red Flag | Signal |
|----------|--------|
| "TBD", "TODO", "TK" | Unresolved |
| "TBD after first pass", "iterate later" | Deferred decision |
| "probably", "maybe", "roughly" | Vague |
| "nice to have", "could also" | Unscoped |
| "similar to X but different" | Undefined difference |
| "users will decide" | Unspecified |
| "depends on the input" | Unconstrained |
| "we'll see how it performs" | Unmeasured |

## Closure Process

When you encounter open specification:

1. **Identify incomplete areas** (use checklist above)
2. **List what's unclear** (specific, not vague)
3. **Propose clarifications** (what needs deciding)
4. **Request approval** (don't proceed without closure)

**Example closure conversation:**

```
User: "Add validation to the API"

YOU: Specification is incomplete. Before implementation:
  - Which fields require validation? (email only? username? all?)
  - What validation rules? (format, length, character set?)
  - What happens on validation failure? (error response format?)
  - Performance target? (validate <10ms per request?)

Please clarify these, then we proceed to implementation.
```

## Why Closure Matters

**Closed specification → Single-pass implementation → No iteration**

**Open specification → Iteration → Rework → Defects**

EPIC 9 atomic cycle assumes specification closure. Without it:
- Agents cannot work independently (unsure what "correct" means)
- Collision detection cannot evaluate alternatives (no reference point)
- Convergence cannot apply selection pressure (unknown criteria)

## Integration with EPIC 9

```
1. User: [Task description]
2. You: [Run specification validator agent]
3. Agent: [Report closure status]
4. If OPEN: [Request clarifications]
5. If CLOSED: [Proceed to EPIC 9 fan-out]
```

## Examples: Open vs. Closed Specifications

### Example 1: File Processing

**OPEN**:
```
"Process CSV files and output results"
```

**CLOSED**:
```
Input: CSV files (max 10MB, UTF-8, comma-delimited)
  - Fields: name (string, 1-100 chars), age (int, 0-150), email (string, valid email)
  - Invalid rows: Reject with detailed error message

Output: Processed data
  - Format: JSON array of objects with same fields
  - Ordering: By name, alphabetically ascending
  - Success: File fully parsed or error reported for first invalid row

Performance: Parse 10 files of 1MB each in <5s (p99)
Concurrency: Thread-safe, allow 5 parallel files
Errors:
  - Invalid CSV format → error with line number
  - Missing required field → error with row number
  - File >10MB → error "File exceeds 10MB limit"

Acceptance Scenarios:
  1. Normal: 100-row CSV → output 100 objects, sorted
  2. Edge case: Single row → output 1 object
  3. Edge case: Empty file → output empty array
  4. Error: Missing email field → error message "Row 5: missing email field"
  5. Error: File 15MB → error "File exceeds maximum size"
```

### Example 2: Authentication

**OPEN**:
```
"Add user authentication"
```

**CLOSED**:
```
Input: Username (string), password (string, ≥8 chars, ≥1 uppercase, ≥1 digit)
Behavior:
  1. Correct credentials → session token valid for 24h
  2. Incorrect credentials → reject after 3 attempts, lock for 15min
  3. Invalid format → reject immediately
Output: Session token (JWT, signed with RS256, include exp claim)
Storage: Passwords hashed with Argon2, never stored plaintext
Invariant: All inputs sanitized (reject SQL special chars, XSS payloads)
Acceptance Scenarios:
  - Scenario 1: Valid credentials → token issued, valid 24h
  - Scenario 2: Invalid password (1st attempt) → reject, allow retry
  - Scenario 3: Invalid password (3rd attempt) → lock account
  - Scenario 4: Locked account login attempt → reject "Account locked"
  - Scenario 5: SQL injection in username → reject "Invalid characters"
```

## When to Use This Skill

- **Before EPIC 9 fan-out**: Verify specification closure
- **During clarification**: Use checklist to structure discussion
- **Before implementation**: Gate work until closed
- **During code review**: Ensure spec matches implementation

## Notes

- Closed ≠ Perfect (but complete enough to implement single-pass)
- Can iterate specification itself (with user), but NOT implementation
- Specification closure is one-time cost upfront
- Single-pass implementation is the payoff
