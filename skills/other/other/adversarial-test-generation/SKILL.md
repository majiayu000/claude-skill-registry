---
name: vibe-adversarial-test-generation
description: Generates edge case, failure mode, and spec-driven test cases. Covers boundary values, nil inputs, concurrency, resource exhaustion, malformed data, and requirement-linked traceability tests.
user-invocable: true
---

# vibe-adversarial-test-generation

Happy-path tests prove your code works. Adversarial tests prove it doesn't break. Spec-linked tests prove it does what it's supposed to.

## When to Use This Skill

- After writing happy-path tests for a feature
- Before claiming test coverage is complete
- When spec requirements lack corresponding tests
- When preparing for a security review
- When `vibe-spec-sync` or `vibe-coverage-enforcer` reports uncovered requirements

## When NOT to Use This Skill

- Before happy-path tests exist (write those first)
- For throwaway/prototype code
- When the function is trivially simple (e.g., getters/setters)

## Modes

### Mode 1: Adversarial (Edge Cases)

Generate tests that break assumptions across 6 categories.

#### 1. Boundary Values
- Zero, one, max, max+1 for all numeric inputs
- Empty string, single char, max-length string
- Empty array, single element, very large array
- Exactly at threshold values

#### 2. Nil/Null/Undefined
- nil pointer as receiver
- nil arguments to every parameter
- nil nested fields in structs
- Returning nil where non-nil expected

#### 3. Type Edge Cases
- Unicode: emoji, RTL text, zero-width chars, combining chars
- Strings: newlines, tabs, null bytes, control characters
- Numbers: NaN, Infinity, -0, very large, very small
- Dates: leap year, DST transitions, timezone boundaries, epoch

#### 4. Concurrency
- Two goroutines/threads calling the same function
- Read during write
- Close during use
- Cancel during operation

#### 5. Resource Exhaustion
- Very large inputs (10MB string, 1M element slice)
- Disk full simulation
- Network timeout simulation
- Memory pressure

#### 6. Malformed Input
- Invalid JSON/YAML/XML
- Truncated input (cut off mid-field)
- Wrong types (string where int expected)
- Extra fields, missing required fields
- SQL injection patterns, XSS payloads (for external inputs)

### Mode 2: Spec-Driven (Requirement Coverage)

Generate tests that trace back to specific spec requirements.

1. **Read the spec** — Find the specification document for the feature under test

2. **Extract requirements** — Parse each requirement into an atomic, testable statement:
   - "Users can reset passwords via email" → testable
   - "The system should be fast" → not testable (flag it)

3. **Map existing tests to requirements** — Scan test files for:
   - Comment markers: `# req:[REQ-ID]` or `// req:[REQ-ID]`
   - Function name patterns: `test_req_[REQ-ID]_*`
   - If no markers exist, use semantic matching (test name/body vs requirement text)

4. **Identify uncovered requirements** — Requirements with no mapped tests

5. **Generate tests for uncovered requirements**:
   - One test function per requirement minimum
   - Name format: `test_req_[REQ-ID]_[description]` (e.g., `test_req_AUTH003_password_reset_sends_email`)
   - First line of test body MUST include traceability marker:
     ```python
     # req:AUTH-003
     ```
     ```go
     // req:AUTH-003
     ```
     ```typescript
     // req:AUTH-003
     ```
   - Test must assert actual behavior against the requirement, not just call the function
   - No `skip()`, no `TODO`, no empty bodies

6. **Report coverage delta**:
   - Requirements covered before: X/N
   - Requirements covered after: Y/N
   - Remaining uncovered (with reasons — e.g., "requires external service mock")

## Steps (Adversarial Mode)

1. **Read the function under test** — understand inputs, outputs, side effects
2. **For each input parameter**, generate adversarial values from each category
3. **For each adversarial input**, determine expected behavior:
   - Should it return an error? (most common)
   - Should it handle gracefully? (fallback behavior)
   - Should it panic? (almost never the right answer)
4. **Write the tests** as table-driven test cases
5. **Run them** and fix any unexpected panics or wrong error handling

## Steps (Spec-Driven Mode)

1. **Read the spec** and extract atomic requirements with IDs
2. **Scan existing tests** for requirement markers and semantic matches
3. **Generate a coverage map**: requirement → test(s) or UNCOVERED
4. **Write tests** for uncovered requirements with traceability markers
5. **Run tests** and verify they pass against current implementation
6. **Report** the before/after coverage delta

## Output Format

### Adversarial Tests: [Function Name]

**Tests Generated**: X
**Categories Covered**: Y/6

| # | Category | Input | Expected | Actual |
|---|----------|-------|----------|--------|
| 1 | Nil input | nil | ErrNilInput | PASS |
| 2 | Empty string | "" | ErrEmpty | PANIC! |

### Issues Found
1. [Function] panics on nil input (should return error)

---

### Spec-Driven Tests: [Feature/Spec Name]

**Spec**: [path/to/spec.md]
**Requirements Found**: N
**Previously Covered**: X/N (Y%)
**Now Covered**: Z/N (W%)

| REQ ID | Requirement | Test Status | Test Function |
|--------|-------------|-------------|---------------|
| AUTH-001 | Login requires email + password | Covered | test_req_AUTH001_login_requires_credentials |
| AUTH-002 | Failed login locks after 5 attempts | NEW | test_req_AUTH002_lockout_after_five_failures |
| AUTH-003 | Password reset sends email | UNCOVERED | (requires email service mock) |

### Remaining Gaps
1. AUTH-003: Requires email service mock — suggest adding mock in conftest.py
