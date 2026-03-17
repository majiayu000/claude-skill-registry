---
name: tdd
description: Comprehensive test-driven development: TDD workflow, test suggestions from diff,
test generation, and property-based testing. Use when: (1) implementing new features,
(2) fixing bugs, (3) refactoring code, (4) reviewing test coverage.
Enforces RED → GREEN → REFACTOR cycle.

category: principles
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Test-Driven Development

Comprehensive testing workflow: TDD cycle, test suggestions, generation, and property-based testing.

---

## TDD Cycle (RED → GREEN → REFACTOR)

You are not allowed to implement code until the full TDD cycle is followed.

### Phase 1: RED (Write Failing Test)

**BLOCKED: Cannot proceed until test failure is proven**

1. Write a test that captures the expected behavior
2. Run the test - it MUST fail
3. Document the failure output as proof

**Phase 1 Checklist:**
- [ ] Test file created/modified
- [ ] Test run completed
- [ ] Failure output captured
- [ ] Failure is for the RIGHT reason (not syntax error)

**Example output:**
```
PHASE 1 - RED ✗
Test: should return user by email
Result: FAILED
Failure: expected undefined to equal { id: 1, email: 'test@example.com' }
Proceeding to Phase 2...
```

### Phase 2: GREEN (Make It Pass)

**BLOCKED: Cannot proceed until test passes**

1. Write the MINIMUM code to make the test pass
2. No refactoring, no extra features, no "while I'm here" changes
3. Run the test - it MUST pass
4. Document the pass output as proof

### Phase 3: REFACTOR (Clean Up)

**Only proceed after Phase 2 is complete**

1. Review code for improvements (naming, structure, duplication)
2. Make changes while keeping tests green
3. Run tests after each refactoring change

### Blocking Conditions

| Phase | Condition to Proceed |
|-------|---------------------|
| RED → GREEN | Test failure output must be shown |
| GREEN → REFACTOR | Test pass output must be shown |
| REFACTOR → Done | Tests must still pass |

**If Phase 1 is missing:** **"BLOCKED: PHASE 1 - RED REQUIRED"**

---

## Test Suggestions from Diff

Analyze code changes and recommend test additions.

### Procedure

1. Get all changes in this branch compared to default
2. Identify changed functions, methods, classes
3. Prioritize by risk level:

| Risk Level | Triggers |
|------------|----------|
| **HIGH** | New code, core logic, missing coverage |
| **MEDIUM** | Modified parameters, return types, conditionals |
| **LOW** | Trivial changes with existing coverage |

### Output Format

```markdown
## Risk Level High
**functionName**
- location: src/path/to/file.ts
- change type: modified
- reason: Why this needs tests
- suggested tests:
  - Test case 1
  - Test case 2
```

---

## Test Generation

Generate comprehensive tests for functions.

### Phases

1. **Detect**: Identify language and testing framework
2. **Locate**: Find existing tests, determine placement
3. **Analyze**: Parse signatures, inputs, outputs, edge cases
4. **Design**: Create minimal set for branch coverage
5. **Emit**: Write tests consistent with framework style
6. **Validate**: Self-check imports, assertions, compilation
7. **Run**: Execute tests, verify they pass

### Security-Focused Cases

Include tests for:
- Invalid/tainted inputs
- Injection payloads
- Path traversal
- Overflow/underflow
- Encoding pitfalls

---

## Property-Based Testing

Use for stronger coverage than example-based tests.

### When to Use

| Pattern | Property | Priority |
|---------|----------|----------|
| encode/decode pair | Roundtrip | HIGH |
| Pure function | Multiple | HIGH |
| Validator | Valid after normalize | MEDIUM |
| Sorting/ordering | Idempotence + ordering | MEDIUM |
| Normalization | Idempotence | MEDIUM |

### Property Catalog

| Property | Formula | When to Use |
|----------|---------|-------------|
| **Roundtrip** | `decode(encode(x)) == x` | Serialization pairs |
| **Idempotence** | `f(f(x)) == f(x)` | Normalization, formatting |
| **Invariant** | Property holds before/after | Any transformation |
| **Commutativity** | `f(a, b) == f(b, a)` | Binary/set operations |

### Detection Patterns

Invoke when you detect:
- **Serialization pairs**: encode/decode, serialize/deserialize, toJSON/fromJSON
- **Parsers**: URL parsing, config parsing, protocol parsing
- **Normalization**: normalize, sanitize, clean, canonicalize
- **Validators**: is_valid, validate, check_*

For detailed patterns, see `references/property-patterns.md`.

---

## Combined With no-workarounds

**When both tdd AND no-workarounds are activated:**
1. You are BLOCKED from implementing ANY fix until Phase 1 (RED) is complete
2. You are BLOCKED from working around the tool failure
3. The ONLY valid path: RED → GREEN → REFACTOR → Verify tool works

---

## Rationalizations (All Rejected)

| Excuse | Why It's Wrong | Required Action |
|--------|----------------|-----------------|
| "It's a simple change" | Simple changes still need tests | Write the test |
| "I'll add tests after" | Tests after = not TDD | BLOCKED |
| "Tests are slow" | Speed doesn't override process | Write the test |
| "I know this works" | Confidence ≠ proof | Write the test |
| "Just this once" | That's what you said last time | Write the test |

---

## Reference Files

- `references/property-patterns.md` - Property-based testing patterns
- `references/libraries.md` - PBT libraries by language