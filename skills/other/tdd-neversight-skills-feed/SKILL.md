---
name: tdd
description: PROACTIVELY enforce Test-Driven Development when implementing features or fixing bugs. Ensures tests are written BEFORE code. Use for new methods, services, repositories, or bug fixes. Guides RED-GREEN-REFACTOR cycle.
---

# TDD (Test-Driven Development) Skill

Guide Claude to follow strict Test-Driven Development practices when implementing new features or fixing bugs. Ensures tests are written BEFORE implementation code.

## When to Use

- Implementing new features
- Adding new methods to existing services/repositories
- Fixing bugs (write failing test first)
- Refactoring existing code

## Core TDD Cycle

```
RED → GREEN → REFACTOR
 ↓      ↓         ↓
Fail   Pass    Improve
```

### 1. RED - Write Failing Test
- Write test that describes desired behavior
- Test MUST fail (compilation error or assertion failure)
- Verify test fails for the right reason

### 2. GREEN - Make Test Pass
- Write minimal code to make test pass
- Don't worry about perfect code yet
- Just make it work

### 3. REFACTOR - Improve Code
- Clean up implementation
- Remove duplication
- Improve naming
- Tests still pass

## Critical Rules

### Rule 1: ALWAYS Identify Entity Under Test

Before writing any test, Claude MUST:

1. **Ask the user** if entity under test is ambiguous
2. **State explicitly** which entity is being tested
3. **Use correct naming** in test file and test functions

See `examples/dialogue-examples.md` for examples of clear vs ambiguous entity identification.

### Rule 2: Test File Location

Place test files next to the code being tested:

```
internal/service/
├── transaction_service.go
└── transaction_service_test.go  ← Test file here

pkg/ofx/
├── parser.go
└── parser_test.go  ← Test file here
```

### Rule 3: Test Naming Convention

**Pattern:** `Test<EntityName>_<MethodName>_<Scenario>`

See `data/naming-conventions.md` for detailed naming guidelines and examples.

```go
// ✅ GOOD - Clear entity, method, and scenario
func TestTransactionService_ImportFromOFX_WithDuplicateFITID(t *testing.T)
func TestOFXParser_Parse_WithInvalidXML(t *testing.T)
func TestBudgetRepository_Create_WithNullAmount(t *testing.T)

// ❌ BAD - Missing entity or scenario
func TestImport(t *testing.T)
func TestValidData(t *testing.T)
```

### Rule 4: Test Main Cases (Not Everything)

Focus on:
- **Happy path** (1 test)
- **Common errors** (2-3 tests)
- **Edge cases** (1-2 tests)
- **Business rules** (as many as needed)

**Don't test:**
- Language features (e.g., "does append work?")
- Third-party library internals
- Trivial getters/setters
- Every possible combination

See `data/coverage-guidelines.md` for what to test and what to skip.

## Test Structure (AAA Pattern)

Use templates from `templates/test-structure.md`:

```go
func TestTransactionService_ImportFromOFX_Success(t *testing.T) {
    // ARRANGE - Setup test data and dependencies
    mockRepo := &mockTransactionRepository{}
    parser := ofx.NewParser()
    service := NewTransactionService(mockRepo, parser)

    ofxData := []byte(`<OFX>...</OFX>`)
    accountID := uuid.New()

    // ACT - Execute the method being tested
    result, err := service.ImportFromOFX(context.Background(), ofxData, accountID)

    // ASSERT - Verify expectations
    require.NoError(t, err)
    assert.Equal(t, 5, result.Inserted)
    assert.Equal(t, 0, result.Skipped)
}
```

## TDD Workflow Examples

See `examples/feature-implementation.md` for complete examples:

### Example 1: New Feature
1. **RED** - Write failing test for `BudgetService.CalculateEffectiveAmount()`
2. **GREEN** - Implement minimal code to pass
3. **REFACTOR** - Add more test cases and improve

### Example 2: Bug Fix
1. **RED** - Reproduce bug with failing test
2. **GREEN** - Fix the bug to make test pass
3. **REFACTOR** - Verify no other bugs introduced

### Example 3: Multiple Scenarios
Test 4 main cases for each method:
- Happy path
- Error handling
- Boundary conditions
- Business rules

## Test Coverage Guidelines

From `data/coverage-guidelines.md`:

### What to Test ✅
- **Repository**: CRUD, constraints, complex queries
- **Service**: Business logic, validation, error handling
- **Handler**: Request/response, status codes, auth

### What NOT to Test ❌
- Language features
- Framework internals
- Database engine behavior
- Third-party libraries
- Trivial code

## Mocking Guidelines

### When to Mock
- External dependencies (HTTP clients, databases)
- Other services in service layer
- Slow operations
- Non-deterministic behavior (time, random)

### How to Mock

See `templates/test-structure.md` for mock templates:

```go
// Define interface in domain
type TransactionRepository interface {
    BulkInsert(ctx context.Context, txs []*Transaction) error
}

// Create mock in test file
type mockTransactionRepository struct {
    mock.Mock
}

func (m *mockTransactionRepository) BulkInsert(ctx context.Context, txs []*Transaction) error {
    args := m.Called(ctx, txs)
    return args.Error(0)
}
```

## Claude's TDD Checklist

Before writing implementation code, Claude MUST:

- [ ] Identify entity under test explicitly
- [ ] Create/open correct test file (`*_test.go`)
- [ ] Write test with clear AAA structure
- [ ] Run test and verify it FAILS
- [ ] State why test fails (compilation or assertion)
- [ ] Ask user if entity or scenario is ambiguous

After test fails, Claude can:

- [ ] Implement minimal code to pass test
- [ ] Run test and verify it PASSES
- [ ] Refactor if needed
- [ ] Add more test cases for edge cases

## Common Mistakes to Avoid

### ❌ Writing Implementation First
```
WRONG: "I'll implement ImportFromOFX, then test it"
RIGHT: "I'll write a test for ImportFromOFX first, then implement"
```

### ❌ Testing Multiple Things in One Test
One scenario per test function.

### ❌ Unclear Entity Under Test
Always specify which entity (Service, Repository, Handler) is being tested.

### ❌ Testing Implementation Details
Test public behavior, not internal variables or private methods.

## TDD Dialog Examples

See `examples/dialogue-examples.md` for:
- How to handle clear entity requests
- How to ask for clarification when ambiguous
- How to propose multiple test scenarios
- How to stop before writing implementation without tests

## Summary

**TDD in 3 Steps:**
1. 🔴 **RED** - Write failing test (describe what you want)
2. 🟢 **GREEN** - Make test pass (implement minimal code)
3. 🔵 **REFACTOR** - Improve code (keep tests passing)

**Always remember:**
- Identify entity under test explicitly
- Write test BEFORE implementation
- Test main cases (not every possibility)
- Use clear naming conventions
- Ask when unsure

**Golden Rule:** If you're writing implementation code without a failing test, STOP and write the test first.

## Reference Files

- **Examples**: See `examples/feature-implementation.md` and `examples/dialogue-examples.md`
- **Templates**: See `templates/test-structure.md` for test patterns and mocks
- **Naming**: See `data/naming-conventions.md` for naming guidelines
- **Coverage**: See `data/coverage-guidelines.md` for what to test
