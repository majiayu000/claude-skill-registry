---
name: go-testing
description: Write and run Go tests using the built-in testing package with table-driven tests, subtests, and mocking via interfaces. Use when writing Go tests or setting up test infrastructure.
---

# Go Testing Skill

## When to Activate

Activate this skill when:
- Writing Go unit tests
- Creating table-driven tests
- Working with test helpers and fixtures
- Mocking dependencies via interfaces
- Running benchmarks or fuzz tests

## Quick Commands

```bash
# Run all tests
go test ./...

# Verbose output
go test -v ./...

# Run specific test
go test -run TestUserCreate

# With coverage
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Run benchmarks
go test -bench=. ./...

# Race detector
go test -race ./...
```

## Basic Test Structure

```go
// math_test.go
package math

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    expected := 5

    if result != expected {
        t.Errorf("Add(2, 3) = %d; want %d", result, expected)
    }
}
```

## Table-Driven Tests (Idiomatic Go)

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -1, -1, -2},
        {"mixed signs", -1, 5, 4},
        {"zeros", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

## Subtests and Parallel Execution

```go
func TestAPIEndpoints(t *testing.T) {
    tests := []struct {
        name     string
        endpoint string
        status   int
    }{
        {"health", "/health", 200},
        {"users", "/api/users", 200},
    }

    for _, tt := range tests {
        tt := tt // capture range variable
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // run in parallel
            // test logic
        })
    }
}
```

## Test Helpers

```go
func assertEqual(t *testing.T, got, want int) {
    t.Helper() // marks as helper for line numbers
    if got != want {
        t.Errorf("got %d; want %d", got, want)
    }
}

func assertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}
```

## Setup and Teardown

```go
func TestDatabase(t *testing.T) {
    // Setup
    db := setupTestDB(t)

    // Teardown (runs after test)
    t.Cleanup(func() {
        db.Close()
    })

    // Test code
    user, err := db.CreateUser("test@example.com")
    assertNoError(t, err)
}
```

## Mocking with Interfaces

```go
// Define interface for dependencies
type UserRepository interface {
    FindByID(id string) (*User, error)
    Save(user *User) error
}

// Mock implementation
type MockUserRepo struct {
    FindByIDFunc func(id string) (*User, error)
}

func (m *MockUserRepo) FindByID(id string) (*User, error) {
    return m.FindByIDFunc(id)
}

// Test with mock
func TestUserService_GetUser(t *testing.T) {
    mock := &MockUserRepo{
        FindByIDFunc: func(id string) (*User, error) {
            return &User{ID: "123", Email: "test@example.com"}, nil
        },
    }

    service := &UserService{repo: mock}
    user, err := service.GetUser("123")

    assertNoError(t, err)
    assertEqual(t, user.ID, "123")
}
```

## HTTP Handler Testing

```go
import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHealthHandler(t *testing.T) {
    req := httptest.NewRequest("GET", "/health", nil)
    rr := httptest.NewRecorder()

    handler := http.HandlerFunc(HealthHandler)
    handler.ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Errorf("status = %d; want %d", rr.Code, http.StatusOK)
    }
}
```

## Benchmarks

```go
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(2, 3)
    }
}

// Run: go test -bench=. -benchmem
```

## Directory Structure

```
project/
├── internal/
│   ├── user/
│   │   ├── user.go
│   │   └── user_test.go
│   └── api/
│       ├── handler.go
│       └── handler_test.go
└── test/
    └── integration/
        └── api_test.go
```

## Test Function Signatures

```go
func TestXxx(t *testing.T)      // Regular test
func BenchmarkXxx(b *testing.B) // Benchmark
func ExampleXxx()               // Example (docs)
func FuzzXxx(f *testing.F)      // Fuzz test
```

## Related Resources

See `AgentUsage/testing_go.md` for complete documentation including:
- Fuzz testing patterns
- Build tags for test types
- TestMain for package-level setup
- Coverage in CI
