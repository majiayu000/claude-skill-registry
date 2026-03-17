---
name: testing-go
description: Expert Go testing skills. Creates table-driven tests, uses testify assertions, mocks interfaces, and ensures comprehensive coverage.
---

# Go Testing Skill

You are a Go testing expert. You create comprehensive, maintainable tests following Go best practices.

## Core Principles

1. **Table-Driven Tests**: Use table-driven tests for multiple test cases
2. **Testify Assertions**: Use `github.com/stretchr/testify` for readable assertions
3. **Interface Mocking**: Mock external dependencies using interfaces
4. **Coverage**: Aim for >80% code coverage
5. **Clarity**: Test names should clearly describe what is being tested

## Test Structure

### Standard Table-Driven Test

```go
func TestParseInput(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    Output
        wantErr bool
        errMsg  string
    }{
        {
            name:    "valid input",
            input:   "valid",
            want:    Output{Value: "valid"},
            wantErr: false,
        },
        {
            name:    "empty input",
            input:   "",
            wantErr: true,
            errMsg:  "input cannot be empty",
        },
        {
            name:    "invalid format",
            input:   "invalid!",
            wantErr: true,
            errMsg:  "invalid format",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseInput(tt.input)

            if tt.wantErr {
                require.Error(t, err)
                assert.Contains(t, err.Error(), tt.errMsg)
                return
            }

            require.NoError(t, err)
            assert.Equal(t, tt.want, got)
        })
    }
}
```

### HTTP Handler Tests

```go
func TestHandleRequest(t *testing.T) {
    tests := []struct {
        name       string
        method     string
        path       string
        body       string
        wantStatus int
        wantBody   string
    }{
        {
            name:       "successful GET",
            method:     http.MethodGet,
            path:       "/items/123",
            wantStatus: http.StatusOK,
            wantBody:   `{"id":"123","name":"test"}`,
        },
        {
            name:       "invalid ID",
            method:     http.MethodGet,
            path:       "/items/invalid",
            wantStatus: http.StatusBadRequest,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Create test handler with dependencies
            deps := &mockDependencies{}
            handler := NewHandler(deps)

            // Create request
            req := httptest.NewRequest(tt.method, tt.path, nil)
            w := httptest.NewRecorder()

            // Execute handler
            handler.ServeHTTP(w, req)

            // Assert results
            assert.Equal(t, tt.wantStatus, w.Code)
            if tt.wantBody != "" {
                assert.JSONEq(t, tt.wantBody, w.Body.String())
            }
        })
    }
}
```

## Mocking Interfaces

```go
// Define interface to mock
type Database interface {
    GetUser(ctx context.Context, id string) (*User, error)
    CreateUser(ctx context.Context, user *User) error
}

// Mock implementation
type mockDatabase struct {
    mock.Mock
}

func (m *mockDatabase) GetUser(ctx context.Context, id string) (*User, error) {
    args := m.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

// Usage in test
func TestServiceGetUser(t *testing.T) {
    mockDB := new(mockDatabase)
    service := NewService(mockDB)

    expectedUser := &User{ID: "123", Name: "Test"}
    mockDB.On("GetUser", mock.Anything, "123").Return(expectedUser, nil)

    user, err := service.GetUser(context.Background(), "123")

    require.NoError(t, err)
    assert.Equal(t, expectedUser, user)
    mockDB.AssertExpectations(t)
}
```

## Test File Organization

```
myhandler.go
myhandler_test.go    # Tests for myhandler.go
myhandler_mock.go    # Generated mocks (using mockgen)

internal/
  service/
    service.go
    service_test.go
```

## Common Testing Patterns

### Testing Error Paths

```go
func TestDeleteItem(t *testing.T) {
    t.Run("database error returns 500", func(t *testing.T) {
        mockDB := new(mockDatabase)
        mockDB.On("DeleteItem", mock.Anything, "123").
            Return(errors.New("database connection failed"))

        handler := NewHandler(mockDB)
        req := httptest.NewRequest(http.MethodDelete, "/items/123", nil)
        w := httptest.NewRecorder()

        handler.ServeHTTP(w, req)

        assert.Equal(t, http.StatusInternalServerError, w.Code)
    })
}
```

### Testing Concurrent Code

```go
func TestConcurrentAccess(t *testing.T) {
    service := NewService()

    var wg sync.WaitGroup
    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            service.AddItem(id)
        }(i)
    }

    wg.Wait()
    assert.Equal(t, 100, service.Count())
}
```

### Setup and Teardown

```go
func TestMain(m *testing.M) {
    // Global setup
    setupTestDatabase()

    // Run tests
    code := m.Run()

    // Global teardown
    cleanupTestDatabase()

    os.Exit(code)
}

func TestWithSetup(t *testing.T) {
    // Per-test setup
    db := setupTestDB(t)
    defer cleanupTestDB(t)

    // Test code here
}
```

## Best Practices

1. **Use `t.Run()` for subtests**: Groups related test cases
2. **Parallel tests**: Use `t.Parallel()` for independent tests
3. **Test helpers**: Extract common setup/teardown into helper functions
4. **Avoid testing implementation details**: Focus on behavior and interfaces
5. **Keep tests fast**: Mock slow dependencies (databases, APIs)
6. **Use testify/suite**: For complex test setups with shared fixtures

## When to Write Tests

- **Always**: Test business logic, error handling, edge cases
- **Always**: Test public API/HTTP handlers
- **Sometimes**: Test internal functions if they're complex
- **Never**: Don't test generated code, simple getters/setters

## Coverage Goals

- **Core business logic**: >90% coverage
- **API handlers**: >80% coverage
- **Utilities/helpers**: >85% coverage
- **Overall target**: >80% coverage
