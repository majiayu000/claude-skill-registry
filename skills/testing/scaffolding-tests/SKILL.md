---
name: scaffolding-tests
description: Generate characterization tests that capture current behavior for safe refactoring
---

# Scaffolding Tests Skill

Scaffolding tests (also called "characterization tests" or "golden master tests") capture the current behavior of code before refactoring. They verify that behavior is preserved without requiring understanding of why the code works.

**Purpose:** Enable safe refactoring by detecting any behavior change, intentional or not.

**When to use:** Before any refactoring that modifies code paths, especially when existing test coverage is insufficient.

---

## Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCAFFOLDING TEST FLOW                         │
│                                                                  │
│   1. CAPTURE                                                     │
│      Input A → Current Code → Output A₁  ← Record this          │
│      Input B → Current Code → Output B₁  ← Record this          │
│      Input C → Current Code → Output C₁  ← Record this          │
│                                                                  │
│   2. REFACTOR                                                    │
│      Modify code structure (not behavior)                        │
│                                                                  │
│   3. VERIFY                                                      │
│      Input A → Refactored Code → Output A₂                       │
│      Assert: A₂ == A₁  ← Behavior preserved!                    │
│                                                                  │
│   4. CLEANUP                                                     │
│      Replace scaffolding with proper unit tests                  │
│      Delete scaffolding tests                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Workflow

### Step 1: Understand What to Scaffold

You should receive a refactoring spec that identifies:
- Which components need scaffolding
- What input categories to test
- Expected risk level

If no spec exists, identify components using:

| Scaffold This | Find With |
|---------------|-----------|
| Public API surface | Exported functions, HTTP handlers |
| High fan-in functions | `Grep` for function name, count call sites |
| Data boundaries | Functions with DB/API/file operations |
| Complex conditionals | Functions with many `if`/`switch` statements |

### Step 2: Generate Representative Inputs

For each component, create inputs that cover:

| Category | Examples | Why |
|----------|----------|-----|
| **Happy path** | Valid complete input | Baseline behavior |
| **Boundary values** | 0, -1, max_int, empty string, max length | Edge behavior |
| **Error conditions** | nil, invalid format, missing required | Error handling |
| **Unicode/i18n** | "María García", "日本語", emojis | Encoding issues |
| **Realistic data** | Production-like payloads | Real-world behavior |

**Generate inputs programmatically when possible:**

```go
// Input generator for user creation
func generateUserInputs() []UserInput {
    return []UserInput{
        // Happy path
        {Name: "John Smith", Email: "john@example.com", Age: 30},

        // Boundary: empty/nil
        {Name: "", Email: "valid@example.com", Age: 0},
        {Name: "Valid", Email: "", Age: 25},

        // Boundary: max length
        {Name: strings.Repeat("a", 255), Email: "max@example.com", Age: 120},

        // Error: invalid format
        {Name: "Valid", Email: "not-an-email", Age: 25},
        {Name: "Valid", Email: "valid@example.com", Age: -1},

        // Unicode
        {Name: "María García-López", Email: "maría@ejemplo.com", Age: 28},
        {Name: "田中太郎", Email: "tanaka@example.jp", Age: 35},

        // Realistic
        {Name: "Robert O'Brien Jr.", Email: "rob.obrien+work@company.co.uk", Age: 42},
    }
}
```

### Step 3: Capture Current Outputs

Run inputs through the current code and record outputs exactly:

```go
func TestScaffold_CreateUser(t *testing.T) {
    // This test CAPTURES behavior, it does not ASSERT correctness

    svc := setupRealService(t)  // Use real dependencies if safe

    inputs := generateUserInputs()

    for _, input := range inputs {
        t.Run(describeInput(input), func(t *testing.T) {
            result, err := svc.CreateUser(context.Background(), input)

            // Record the golden output
            golden := GoldenOutput{
                Input:      input,
                Result:     result,
                Error:      errorToString(err),
                ErrorType:  errorType(err),
            }

            // Compare against stored golden (or store if first run)
            assertGolden(t, "create_user", input.Name, golden)
        })
    }
}

// Helper to serialize errors consistently
func errorToString(err error) string {
    if err == nil {
        return ""
    }
    return err.Error()
}

func errorType(err error) string {
    if err == nil {
        return ""
    }
    // Capture error type for errors.Is() compatibility
    return fmt.Sprintf("%T", err)
}
```

### Step 4: Store Golden Outputs

Store captured outputs in a structured format:

```
testdata/
└── golden/
    └── create_user/
        ├── happy_path_john_smith.golden.json
        ├── boundary_empty_name.golden.json
        ├── boundary_max_length.golden.json
        ├── error_invalid_email.golden.json
        └── unicode_japanese.golden.json
```

**Golden file format:**

```json
{
  "input": {
    "name": "John Smith",
    "email": "john@example.com",
    "age": 30
  },
  "output": {
    "result": {
      "id": "GENERATED_ID",
      "name": "John Smith",
      "email": "john@example.com",
      "created_at": "TIMESTAMP"
    },
    "error": "",
    "error_type": ""
  },
  "captured_at": "2026-01-31T10:00:00Z",
  "code_version": "abc123"
}
```

**Handle non-deterministic values:**

```go
// Normalize outputs before comparison
func normalizeOutput(output *CreateUserResult) {
    // Replace generated IDs with placeholder
    if output.ID != "" {
        output.ID = "GENERATED_ID"
    }

    // Replace timestamps with placeholder
    if !output.CreatedAt.IsZero() {
        output.CreatedAt = time.Time{}  // or a fixed time
    }
}
```

### Step 5: Create Scaffolding Test File

```go
// user_scaffold_test.go
//
// SCAFFOLDING TESTS - DELETE AFTER REFACTORING
//
// These tests capture current behavior for the user service refactoring.
// They should be replaced with proper unit tests after refactoring is complete.
//
// Refactoring ticket: RF-2026-001
// Created: 2026-01-31
// Expected removal: After RF-2026-001 Phase 4 (cleanup)

package handlers

import (
    "context"
    "encoding/json"
    "os"
    "path/filepath"
    "testing"
)

// TestScaffold_ prefix indicates these are temporary scaffolding tests
func TestScaffold_CreateUser(t *testing.T) {
    if os.Getenv("SKIP_SCAFFOLD") != "" {
        t.Skip("Scaffolding tests skipped")
    }

    svc := setupService(t)

    tests := []struct {
        name  string
        input UserInput
    }{
        {"happy_path", UserInput{Name: "John", Email: "john@example.com"}},
        {"empty_name", UserInput{Name: "", Email: "valid@example.com"}},
        {"invalid_email", UserInput{Name: "John", Email: "not-an-email"}},
        // ... more cases
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := svc.CreateUser(context.Background(), tt.input)

            actual := normalize(result, err)
            expected := loadGolden(t, "create_user", tt.name)

            if !equalGolden(actual, expected) {
                // On first run or with -update flag, save the golden
                if os.Getenv("UPDATE_GOLDEN") != "" {
                    saveGolden(t, "create_user", tt.name, actual)
                    return
                }

                t.Errorf("Behavior changed!\nExpected: %s\nActual: %s",
                    formatGolden(expected), formatGolden(actual))
            }
        })
    }
}

func TestScaffold_GetUser(t *testing.T) {
    // Similar structure...
}

// Golden file helpers

func loadGolden(t *testing.T, component, testCase string) Golden {
    t.Helper()
    path := filepath.Join("testdata", "golden", component, testCase+".golden.json")

    data, err := os.ReadFile(path)
    if err != nil {
        if os.IsNotExist(err) {
            return Golden{}  // First run, no golden yet
        }
        t.Fatalf("Failed to load golden: %v", err)
    }

    var golden Golden
    if err := json.Unmarshal(data, &golden); err != nil {
        t.Fatalf("Failed to parse golden: %v", err)
    }
    return golden
}

func saveGolden(t *testing.T, component, testCase string, golden Golden) {
    t.Helper()
    dir := filepath.Join("testdata", "golden", component)
    if err := os.MkdirAll(dir, 0755); err != nil {
        t.Fatalf("Failed to create golden dir: %v", err)
    }

    path := filepath.Join(dir, testCase+".golden.json")
    data, err := json.MarshalIndent(golden, "", "  ")
    if err != nil {
        t.Fatalf("Failed to marshal golden: %v", err)
    }

    if err := os.WriteFile(path, data, 0644); err != nil {
        t.Fatalf("Failed to write golden: %v", err)
    }

    t.Logf("Updated golden: %s", path)
}
```

### Step 6: Verify Scaffolding Before Refactoring

Before starting refactoring:

```bash
# Generate/update golden files
UPDATE_GOLDEN=1 go test -v -run TestScaffold_ ./...

# Verify scaffolding captures current behavior
go test -v -run TestScaffold_ ./...

# All scaffolding tests should pass
```

### Step 7: Use During Refactoring

After each refactoring change:

```bash
# Quick check - scaffolding tests only
go test -v -run TestScaffold_ ./...

# Any failure means behavior changed
# Either: fix the refactoring, or update the golden (if change is intentional)
```

### Step 8: Cleanup After Refactoring

Once refactoring is complete:

1. Write proper unit tests for the refactored code
2. Verify proper tests cover the same behaviors
3. Delete scaffolding tests and golden files
4. Remove `testdata/golden/` directory

```bash
# Remove scaffolding artifacts
rm -rf testdata/golden/
rm *_scaffold_test.go
```

---

## HTTP Handler Scaffolding

For HTTP handlers, capture the full response:

```go
func TestScaffold_UserHandler_Create(t *testing.T) {
    handler := setupHandler(t)

    tests := []struct {
        name   string
        method string
        path   string
        body   string
    }{
        {"valid_user", "POST", "/users", `{"name":"John","email":"john@example.com"}`},
        {"invalid_json", "POST", "/users", `{invalid`},
        {"missing_email", "POST", "/users", `{"name":"John"}`},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest(tt.method, tt.path, strings.NewReader(tt.body))
            req.Header.Set("Content-Type", "application/json")

            rec := httptest.NewRecorder()
            handler.ServeHTTP(rec, req)

            actual := HTTPGolden{
                StatusCode: rec.Code,
                Headers:    normalizeHeaders(rec.Header()),
                Body:       normalizeBody(rec.Body.String()),
            }

            expected := loadHTTPGolden(t, "user_handler", tt.name)

            if !equalHTTPGolden(actual, expected) {
                if os.Getenv("UPDATE_GOLDEN") != "" {
                    saveHTTPGolden(t, "user_handler", tt.name, actual)
                    return
                }
                t.Errorf("Response changed!\nExpected: %+v\nActual: %+v", expected, actual)
            }
        })
    }
}
```

---

## Database-Dependent Scaffolding

For code that modifies database state:

```go
func TestScaffold_CreateUser_DBState(t *testing.T) {
    db := setupTestDB(t)  // Fresh DB for each test
    svc := NewService(db)

    input := UserInput{Name: "John", Email: "john@example.com"}

    // Capture before state
    beforeCount := countUsers(t, db)

    // Execute
    result, err := svc.CreateUser(context.Background(), input)

    // Capture after state
    afterCount := countUsers(t, db)
    createdUser := getUserByEmail(t, db, "john@example.com")

    actual := DBGolden{
        Result:       normalize(result),
        Error:        errorToString(err),
        UsersBefore:  beforeCount,
        UsersAfter:   afterCount,
        CreatedUser:  normalizeUser(createdUser),
    }

    // Compare with golden...
}
```

---

## Naming Conventions

| Element | Convention |
|---------|------------|
| Test file | `{component}_scaffold_test.go` |
| Test function | `TestScaffold_{Component}_{Operation}` |
| Golden directory | `testdata/golden/{component}/` |
| Golden file | `{test_case}.golden.json` |

---

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Scaffold everything | Wastes time, brittle tests | Scaffold only high-risk components |
| Keep scaffolding tests forever | Become maintenance burden | Delete after refactoring complete |
| Test implementation details | Breaks on any internal change | Test observable behavior only |
| Skip normalization | Non-deterministic failures | Normalize IDs, timestamps, etc. |
| Assert "correctness" | Wrong mindset for scaffolding | Assert "sameness" only |
| One golden per component | Misses edge cases | Cover all input categories |

---

## Checklist

Before starting scaffolding:
```markdown
- [ ] Components to scaffold identified (from refactoring spec or self-analysis)
- [ ] Input categories defined for each component
- [ ] Golden file storage structure decided
```

During scaffolding:
```markdown
- [ ] Inputs cover: happy path, boundaries, errors, unicode, realistic data
- [ ] Non-deterministic values normalized (IDs, timestamps)
- [ ] Golden files generated with UPDATE_GOLDEN=1
- [ ] All scaffolding tests pass before refactoring starts
```

After refactoring:
```markdown
- [ ] All scaffolding tests pass (behavior preserved)
- [ ] Proper unit tests written for refactored code
- [ ] Scaffolding tests deleted
- [ ] Golden files deleted
```

---

## Integration with Testing Skill

Scaffolding tests are **temporary** and have different rules than regular tests:

| Regular Tests | Scaffolding Tests |
|---------------|-------------------|
| Assert correctness | Assert sameness |
| Test contracts | Capture behavior |
| Keep forever | Delete after refactoring |
| Part of CI | Optional in CI (can slow builds) |
| Cover new code | Cover code being changed |

After refactoring, replace scaffolding with regular tests following the [Testing Skill](../testing/SKILL.md).
