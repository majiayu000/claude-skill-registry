---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring Go code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests. Uses table-driven tests (Go standard).
---

# Test-Driven Development Workflow (Go)

This skill ensures all Go code development follows TDD principles with comprehensive test coverage using idiomatic Go testing patterns.

## When to Activate

- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints (Fiber)
- Creating new services or repositories
- Adding Shopify webhook handlers

## Core Principles

### 1. Tests BEFORE Code
ALWAYS write tests first, then implement code to make tests pass.

### 2. Coverage Requirements
- Minimum 80% coverage (verified with `go test -cover`)
- All edge cases covered
- Error scenarios tested
- Boundary conditions verified
- Race conditions prevented (`go test -race`)

### 3. Test Types

#### Unit Tests
- Individual functions and methods
- Service layer logic
- Pure functions
- Helpers and utilities
- **ALWAYS use table-driven tests** (Go standard pattern)

#### Integration Tests
- HTTP handlers (with httptest)
- Database operations (with test containers)
- RabbitMQ workers
- Redis caching
- External API calls

#### E2E Tests (Playwright for Frontend)
- Critical user flows
- Complete workflows
- Browser automation
- UI interactions

## TDD Workflow Steps

### Step 1: Write User Journeys
```
As a [role], I want to [action], so that [benefit]

Example:
As a merchant, I want to receive webhook notifications when orders are placed,
so that I can process orders in real-time.
```

### Step 2: Generate Test Cases (Table-Driven)
For each user journey, create comprehensive test cases using Go's table-driven pattern:

```go
func TestProcessWebhook(t *testing.T) {
	tests := []struct {
		name       string
		payload    string
		hmacValid  bool
		wantErr    bool
		wantStatus WebhookStatus
	}{
		{
			name:       "valid webhook processes successfully",
			payload:    `{"order_id":"123","amount":100}`,
			hmacValid:  true,
			wantErr:    false,
			wantStatus: StatusProcessed,
		},
		{
			name:       "invalid HMAC returns error",
			payload:    `{"order_id":"123"}`,
			hmacValid:  false,
			wantErr:    true,
			wantStatus: StatusRejected,
		},
		{
			name:       "empty payload returns error",
			payload:    "",
			hmacValid:  true,
			wantErr:    true,
			wantStatus: StatusFailed,
		},
		{
			name:       "malformed JSON returns error",
			payload:    `{invalid json}`,
			hmacValid:  true,
			wantErr:    true,
			wantStatus: StatusFailed,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Test implementation
			result, err := ProcessWebhook(tt.payload, tt.hmacValid)

			if (err != nil) != tt.wantErr {
				t.Errorf("ProcessWebhook() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if result.Status != tt.wantStatus {
				t.Errorf("ProcessWebhook() status = %v, want %v", result.Status, tt.wantStatus)
			}
		})
	}
}
```

### Step 3: Run Tests (They Should Fail)
```bash
go test ./...
# Tests should fail - we haven't implemented yet
# Output: undefined: ProcessWebhook
```

### Step 4: Implement Code
Write minimal code to make tests pass:

```go
// Implementation guided by tests
func ProcessWebhook(payload string, hmacValid bool) (*WebhookResult, error) {
	if !hmacValid {
		return &WebhookResult{Status: StatusRejected}, errors.New("invalid HMAC")
	}

	if payload == "" {
		return &WebhookResult{Status: StatusFailed}, errors.New("empty payload")
	}

	var data WebhookData
	if err := json.Unmarshal([]byte(payload), &data); err != nil {
		return &WebhookResult{Status: StatusFailed}, fmt.Errorf("invalid JSON: %w", err)
	}

	return &WebhookResult{Status: StatusProcessed}, nil
}
```

### Step 5: Run Tests Again
```bash
go test ./...
# Tests should now pass
# Output: PASS
```

### Step 6: Refactor
Improve code quality while keeping tests green:
- Remove duplication
- Improve naming
- Optimize performance
- Enhance readability
- Add error context

### Step 7: Verify Coverage
```bash
go test ./... -cover
# Verify 80%+ coverage achieved

go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out
# View detailed coverage report in browser
```

## Testing Patterns

### Unit Test Pattern (Table-Driven)
```go
package service

import (
	"context"
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestGetMarket(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		want    *Market
		wantErr bool
	}{
		{
			name:  "valid market ID returns market",
			input: "market-123",
			want: &Market{
				ID:   "market-123",
				Name: "Election 2024",
			},
			wantErr: false,
		},
		{
			name:    "empty ID returns error",
			input:   "",
			want:    nil,
			wantErr: true,
		},
		{
			name:    "invalid ID returns error",
			input:   "invalid-id",
			want:    nil,
			wantErr: true,
		},
		{
			name:    "nil context returns error",
			input:   "market-123",
			want:    nil,
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Arrange
			ctx := context.Background()
			mockRepo := &MockMarketRepository{
				FindByIDFunc: func(ctx context.Context, id string) (*Market, error) {
					if id == "" || id == "invalid-id" {
						return nil, errors.New("not found")
					}
					return &Market{ID: id, Name: "Election 2024"}, nil
				},
			}
			service := NewMarketService(mockRepo)

			// Act
			got, err := service.GetMarket(ctx, tt.input)

			// Assert
			if tt.wantErr {
				assert.Error(t, err)
			} else {
				require.NoError(t, err)
				assert.Equal(t, tt.want.ID, got.ID)
				assert.Equal(t, tt.want.Name, got.Name)
			}
		})
	}
}
```

### HTTP Handler Integration Test Pattern
```go
package handler_test

import (
	"context"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"github.com/testcontainers/testcontainers-go"
	"github.com/testcontainers/testcontainers-go/modules/postgres"
)

func TestGetMarketHandler(t *testing.T) {
	// Setup test database with testcontainers
	ctx := context.Background()
	pgContainer, err := postgres.RunContainer(ctx,
		testcontainers.WithImage("postgres:15"),
	)
	require.NoError(t, err)
	defer pgContainer.Terminate(ctx)

	connStr, err := pgContainer.ConnectionString(ctx)
	require.NoError(t, err)

	db := setupTestDB(connStr)
	handler := NewMarketHandler(db)

	tests := []struct {
		name           string
		marketID       string
		setupData      func()
		expectedStatus int
		checkResponse  func(*testing.T, *http.Response)
	}{
		{
			name:     "returns market when found",
			marketID: "market-123",
			setupData: func() {
				insertMarket(db, "market-123", "Election 2024")
			},
			expectedStatus: http.StatusOK,
			checkResponse: func(t *testing.T, resp *http.Response) {
				var result APIResponse
				err := json.NewDecoder(resp.Body).Decode(&result)
				require.NoError(t, err)
				assert.True(t, result.Success)
				assert.Equal(t, "market-123", result.Data.ID)
			},
		},
		{
			name:           "returns 404 when not found",
			marketID:       "invalid-id",
			setupData:      func() {},
			expectedStatus: http.StatusNotFound,
			checkResponse: func(t *testing.T, resp *http.Response) {
				var result APIResponse
				err := json.NewDecoder(resp.Body).Decode(&result)
				require.NoError(t, err)
				assert.False(t, result.Success)
				assert.Contains(t, result.Error, "not found")
			},
		},
		{
			name:           "returns 400 for empty ID",
			marketID:       "",
			setupData:      func() {},
			expectedStatus: http.StatusBadRequest,
			checkResponse:  nil,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Setup test data
			if tt.setupData != nil {
				tt.setupData()
			}

			// Create request
			req := httptest.NewRequest("GET", "/api/markets/"+tt.marketID, nil)
			w := httptest.NewRecorder()

			// Execute handler
			handler.GetMarket(w, req)

			// Assert status code
			assert.Equal(t, tt.expectedStatus, w.Code)

			// Check response body
			if tt.checkResponse != nil {
				tt.checkResponse(t, w.Result())
			}
		})
	}
}
```

### E2E Test Pattern (Playwright for Frontend)
```typescript
// Frontend E2E tests remain in TypeScript with Playwright
import { test, expect } from '@playwright/test'

test('user can search and view market', async ({ page }) => {
	await page.goto('/')

	// Search for market (Web Component selector)
	await page.locator('s-text-field[data-testid="search"]').fill('election')
	await page.waitForTimeout(600) // Debounce

	// Verify results
	const results = page.locator('[data-testid="market-card"]')
	await expect(results).toHaveCount(5, { timeout: 5000 })

	// Click first result
	await results.first().click()

	// Verify market page loaded
	await expect(page).toHaveURL(/\/markets\//)
	await expect(page.locator('s-page').getAttribute('title')).toBeTruthy()
})
```

**Note:** When testing Shopify Polaris Web Components (`s-*` prefix), use tag + attribute selectors:
```typescript
// Prefer: tag + data-testid
page.locator('s-text-field[data-testid="email"]')
page.locator('s-button[data-testid="submit"]')

// Also valid: tag + attribute
page.locator('s-button[variant="primary"]')
page.locator('s-banner[status="critical"]')

// Get attribute values from Web Components
const errorMsg = await page.locator('s-text-field').getAttribute('error')
const pageTitle = await page.locator('s-page').getAttribute('title')
```

## Test File Organization

```
project-root/
├── cmd/
│   └── api/
│       └── main.go
├── internal/
│   ├── domain/
│   │   ├── market.go
│   │   └── market_test.go           # Unit tests
│   ├── repository/
│   │   ├── market_repo.go
│   │   ├── market_repo_test.go      # Unit tests
│   │   └── market_repo_integration_test.go  # Integration tests
│   ├── service/
│   │   ├── market_service.go
│   │   └── market_service_test.go   # Unit tests with mocks
│   └── handler/
│       ├── market_handler.go
│       └── market_handler_test.go   # Integration tests with httptest
├── testutil/
│   ├── db.go                        # Test database helpers
│   ├── fixtures.go                  # Test data fixtures
│   └── mock.go                      # Common mocks
└── frontend/
    └── e2e/
        ├── markets.spec.ts          # E2E tests (Playwright)
        └── webhooks.spec.ts
```

## Mocking External Services

### Repository Mock with Interface
```go
// Define interface
type MarketRepository interface {
	FindByID(ctx context.Context, id string) (*Market, error)
	Create(ctx context.Context, m *Market) error
}

// Mock implementation
type MockMarketRepository struct {
	FindByIDFunc func(ctx context.Context, id string) (*Market, error)
	CreateFunc   func(ctx context.Context, m *Market) error
}

func (m *MockMarketRepository) FindByID(ctx context.Context, id string) (*Market, error) {
	if m.FindByIDFunc != nil {
		return m.FindByIDFunc(ctx, id)
	}
	return nil, nil
}

func (m *MockMarketRepository) Create(ctx context.Context, market *Market) error {
	if m.CreateFunc != nil {
		return m.CreateFunc(ctx, market)
	}
	return nil
}

// Use in test
func TestServiceGetMarket(t *testing.T) {
	mockRepo := &MockMarketRepository{
		FindByIDFunc: func(ctx context.Context, id string) (*Market, error) {
			return &Market{ID: id, Name: "Test Market"}, nil
		},
	}

	service := NewMarketService(mockRepo)
	market, err := service.GetMarket(context.Background(), "123")

	assert.NoError(t, err)
	assert.Equal(t, "123", market.ID)
}
```

### HTTP Mock with httptest
```go
func TestExternalAPICall(t *testing.T) {
	// Create mock server
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		assert.Equal(t, "GET", r.Method)
		assert.Equal(t, "/api/markets", r.URL.Path)

		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(APIResponse{
			Success: true,
			Data:    []Market{{ID: "1", Name: "Test"}},
		})
	}))
	defer server.Close()

	// Use mock server URL in client
	client := NewAPIClient(server.URL)
	markets, err := client.GetMarkets(context.Background())

	assert.NoError(t, err)
	assert.Len(t, markets, 1)
	assert.Equal(t, "Test", markets[0].Name)
}
```

## Test Coverage Verification

### Run Coverage Report
```bash
# Run tests with coverage
go test ./... -cover

# Generate coverage profile
go test ./... -coverprofile=coverage.out

# View coverage by package
go tool cover -func=coverage.out

# View HTML coverage report
go tool cover -html=coverage.out

# Check coverage threshold (80%+)
go test ./... -coverprofile=coverage.out
go tool cover -func=coverage.out | grep total | awk '{print $3}'
```

### Coverage Thresholds
Required coverage: **80%+** for all packages except:
- `cmd/` (main packages)
- Simple getters/setters

## Common Testing Mistakes to Avoid

### ❌ WRONG: Not Using Table-Driven Tests
```go
// Don't write separate test functions for each case
func TestValidInput(t *testing.T) { ... }
func TestEmptyInput(t *testing.T) { ... }
func TestNilInput(t *testing.T) { ... }
```

### ✅ CORRECT: Use Table-Driven Tests
```go
// DO use table-driven tests
func TestGetMarket(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		want    *Market
		wantErr bool
	}{
		{name: "valid", input: "123", want: &Market{ID: "123"}, wantErr: false},
		{name: "empty", input: "", want: nil, wantErr: true},
		{name: "nil", input: "invalid", want: nil, wantErr: true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Test logic
		})
	}
}
```

### ❌ WRONG: No Test Isolation
```go
// Tests depend on each other
var globalUser *User

func TestCreateUser(t *testing.T) {
	globalUser = createUser() // Sets global state
}

func TestUpdateUser(t *testing.T) {
	updateUser(globalUser) // Depends on previous test
}
```

### ✅ CORRECT: Independent Tests
```go
// Each test sets up its own data
func TestCreateUser(t *testing.T) {
	user := createTestUser(t)
	err := createUser(user)
	assert.NoError(t, err)
}

func TestUpdateUser(t *testing.T) {
	user := createTestUser(t)
	err := updateUser(user)
	assert.NoError(t, err)
}
```

### ❌ WRONG: Ignoring Errors
```go
// Don't ignore errors in tests
result, _ := GetMarket("123") // Ignoring error!
```

### ✅ CORRECT: Always Check Errors
```go
// DO verify error behavior
result, err := GetMarket("123")
if tt.wantErr {
	assert.Error(t, err)
} else {
	assert.NoError(t, err)
}
```

## Continuous Testing

### Watch Mode During Development
```bash
# Run tests on file changes (using air or reflex)
air -- go test ./... -v

# Or use entr
find . -name '*.go' | entr -c go test ./...
```

### Pre-Commit Hook
```bash
# Runs before every commit
go test ./... && golangci-lint run
```

### CI/CD Integration
```yaml
# GitHub Actions
- name: Run Tests
  run: go test ./... -cover -race
- name: Generate Coverage
  run: go test ./... -coverprofile=coverage.out
- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.out
```

## Best Practices

1. **Write Tests First** - Always TDD
2. **Table-Driven Tests** - Go standard pattern for multiple cases
3. **Descriptive Test Names** - Explain what's tested
4. **Arrange-Act-Assert** - Clear test structure
5. **Mock External Dependencies** - Isolate unit tests
6. **Test Edge Cases** - Nil, empty, invalid, boundary values
7. **Test Error Paths** - Not just happy paths
8. **Keep Tests Fast** - Unit tests < 10ms each
9. **Use testify/assert** - More readable assertions
10. **Review Coverage Reports** - Identify gaps

## Go Testing Tools

### Required
- `go test` - Built-in test runner
- `testify/assert` - Better assertions
- `testify/require` - Fail-fast assertions
- `httptest` - HTTP handler testing

### Recommended
- `testcontainers-go` - Integration tests with Docker
- `testify/mock` - Complex mocking
- `golangci-lint` - Linter with test checks
- `go-cmp` - Deep comparison

### Installation
```bash
go get github.com/stretchr/testify/assert
go get github.com/stretchr/testify/require
go get github.com/stretchr/testify/mock
go get github.com/testcontainers/testcontainers-go
```

## Success Metrics

- 80%+ code coverage achieved (`go test -cover`)
- All tests passing (green)
- No skipped or disabled tests (`t.Skip()`)
- Fast test execution (< 5s for unit tests)
- Race detector clean (`go test -race`)
- E2E tests cover critical user flows
- Tests catch bugs before production

---

**Remember**: Tests are not optional. They are the safety net that enables confident refactoring, rapid development, and production reliability.

**Go Testing Philosophy**: Use table-driven tests as the default pattern. They're idiomatic, maintainable, and make adding new test cases trivial. Every new function should have comprehensive table-driven tests before implementation.

**Coverage Target**: 80%+ is mandatory. Anything less indicates untested code paths that could break in production.
