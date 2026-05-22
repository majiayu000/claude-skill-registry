---
name: kratos-tests
description: Generates comprehensive table-driven tests for go-kratos microservices using testify/mock and testify/assert. Creates repository tests with in-memory SQLite, business layer tests with mocks, and service layer tests with proper context propagation. Use when writing unit tests for any kratos layer, adding test coverage, creating mock implementations, or validating CRUD operations.
---

# Kratos Testing Skill

## Purpose

Generate comprehensive, table-driven tests for all layers of a Kratos microservice (repository, business logic, service) using testify/assert and testify/mock libraries.

## Essential Patterns

### 1. Repository Layer Tests

**File**: \`internal/data/repo/{entity}_test.go\`

#### Test Setup Pattern

```go
package repo

import (
    "context"
    "testing"
    "{service}/internal/biz/domain"
    "{service}/internal/data/model"
    "github.com/stretchr/testify/assert"
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
)

// Setup in-memory database
func setupTestDB(t *testing.T) *gorm.DB {
    db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
    if err != nil {
        t.Errorf("Failed to open in-memory SQLite database: %v", err)
    }
    
    if err := db.AutoMigrate(&model.{Entity}{}, &model.{RelatedEntity}{}); err != nil {
        t.Errorf("Failed to migrate test tables: %v", err)
    }
    
    return db
}

// Cleanup function
func cleanupDB(db *gorm.DB) {
    db.Exec("DELETE FROM {related_entities}")
    db.Exec("DELETE FROM {entities}")
}

// Helper: valid domain object
func validDomain{Entity}() *domain.{Entity} {
    return &domain.{Entity}{
        Field1: "value1",
        Field2: 123,
        // ... all required fields
    }
}

// Helper: valid GORM entity
func validEntity{Entity}() *model.{Entity} {
    return &model.{Entity}{
        Field1: "value1",
        Field2: 123,
        // ... all required fields
    }
}
```

#### Table-Driven Test Pattern

```go
func TestCreate(t *testing.T) {
    tests := []struct {
        name        string
        input       *domain.{Entity}
        setup       func(*gorm.DB)
        wantErr     bool
        checkError  func(*testing.T, error)
        checkResult func(*testing.T, *domain.{Entity})
    }{
        {
            name:    "success with nested data",
            input:   validDomain{Entity}(),
            setup:   func(db *gorm.DB) {},
            wantErr: false,
            checkResult: func(t *testing.T, result *domain.{Entity}) {
                assert.NotNil(t, result)
                assert.NotZero(t, result.ID)
                assert.Equal(t, "value1", result.Field1)
            },
        },
        {
            name: "duplicate entry error",
            input: validDomain{Entity}(),
            setup: func(db *gorm.DB) {
                // Pre-create entity to cause duplicate
                entity := validEntity{Entity}()
                db.Create(entity)
            },
            wantErr: true,
            checkError: func(t *testing.T, err error) {
                assert.ErrorIs(t, err, domain.ErrDataDuplicateEntry)
            },
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            db := setupTestDB(t)
            defer cleanupDB(db)
            
            tt.setup(db)
            
            logger := log.NewStdLogger(os.Stdout)
            tx := &mockTransaction{}
            repo := New{Entity}Repo(db, tx, logger)
            
            result, err := repo.Create(context.Background(), tt.input)
            
            if tt.wantErr {
                assert.Error(t, err)
                if tt.checkError != nil {
                    tt.checkError(t, err)
                }
            } else {
                assert.NoError(t, err)
                if tt.checkResult != nil {
                    tt.checkResult(t, result)
                }
            }
        })
    }
}
```

#### List/Pagination Tests Pattern

```go
func TestList{Entities}(t *testing.T) {
    tests := []struct {
        name        string
        offset      uint64
        limit       uint32
        filter      map[string]interface{}
        setup       func(*gorm.DB)
        wantErr     bool
        checkResult func(*testing.T, []*domain.{Entity}, *pagination.Meta)
    }{
        {
            name:   "success - first page with next page",
            offset: 0,
            limit:  5,
            filter: map[string]interface{}{"project_id": uint64(1)},
            setup: func(db *gorm.DB) {
                for i := 0; i < 10; i++ {
                    entity := validEntity{Entity}()
                    entity.UID = fmt.Sprintf("uid-%d", i)
                    db.Create(entity)
                }
            },
            wantErr: false,
            checkResult: func(t *testing.T, results []*biz.{Entity}, meta *pagination.Meta) {
                assert.Len(t, results, 5)
                assert.Equal(t, uint64(10), meta.TotalCount)
                assert.True(t, meta.HasNextPage)
                assert.False(t, meta.HasPreviousPage)
            },
        },
        {
            name:   "success - filter with pagination",
            offset: 0,
            limit:  10,
            filter: map[string]interface{}{"project_id": uint64(1), "label": "test"},
            setup: func(db *gorm.DB) {
                // Create entities with matching filter
                for i := 0; i < 3; i++ {
                    entity := validEntity{Entity}()
                    entity.Label = "test"
                    db.Create(entity)
                }
                // Create entities not matching filter
                for i := 0; i < 5; i++ {
                    entity := validEntity{Entity}()
                    entity.Label = "other"
                    db.Create(entity)
                }
            },
            wantErr: false,
            checkResult: func(t *testing.T, results []*biz.{Entity}, meta *pagination.Meta) {
                assert.Len(t, results, 3)
                assert.Equal(t, uint64(3), meta.TotalCount) // Only filtered count
                for _, r := range results {
                    assert.Equal(t, "test", r.Label)
                }
            },
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            db := setupTestDB(t)
            defer cleanupDB(db)
            
            tt.setup(db)
            
            logger := log.NewStdLogger(os.Stdout)
            tx := &mockTransaction{}
            repo := New{Entity}Repo(db, tx, logger)
            
            results, meta, err := repo.List{Entities}(context.Background(), tt.offset, tt.limit, tt.filter)
            
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
                if tt.checkResult != nil {
                    tt.checkResult(t, results, meta)
                }
            }
        })
    }
}
```

### 2. Business Layer Tests (Use Case)

**File**: \`internal/biz/{entity}/usecase_test.go\` (new structure)
**Old File**: \`internal/biz/{entity}_test.go\` (legacy structure)

#### Mock Repository Pattern

```go
// Package {entity} provides tests for use cases managing {entities}.
package {entity}

import (
    "context"
    "testing"
    "platform/pagination"
    "{service}/internal/biz/domain"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// Mock repository
type Mock{Entity}Repo struct {
    mock.Mock
}

func (m *Mock{Entity}Repo) Create(ctx context.Context, entity *domain.{Entity}) (*domain.{Entity}, error) {
    args := m.Called(ctx, entity)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*domain.{Entity}), args.Error(1)
}

func (m *Mock{Entity}Repo) FindByID(ctx context.Context, id uint64) (*domain.{Entity}, error) {
    args := m.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*domain.{Entity}), args.Error(1)
}

func (m *Mock{Entity}Repo) List{Entities}(ctx context.Context, offset uint64, limit uint32, filter map[string]interface{}) ([]*domain.{Entity}, *pagination.Meta, error) {
    args := m.Called(ctx, offset, limit, filter)
    if args.Get(0) == nil {
        return nil, nil, args.Error(2)
    }
    if args.Get(1) == nil {
        return args.Get(0).([]*domain.{Entity}), nil, args.Error(2)
    }
    return args.Get(0).([]*domain.{Entity}), args.Get(1).(*pagination.Meta), args.Error(2)
}

// Test helper - legacy (without event publishing)
func setup{Entity}UseCase(mockRepo *Mock{Entity}Repo) domain.{Entity}UseCase {
    logger := log.NewStdLogger(os.Stdout)
    validator := NewValidator()
    mockTx := new(MockTransaction)
    mockTx.On("InTx", mock.Anything, mock.Anything).Return(nil).Maybe()
    return NewUseCase(mockRepo, validator, mockTx, logger)
}

func valid{Entity}() *domain.{Entity} {
    return &domain.{Entity}{
        Field1: "value1",
        Field2: 123,
    }
}
```

#### Use Case Test Pattern

```go
func TestCreate{Entity}(t *testing.T) {
    tests := []struct {
        name        string
        input       *domain.{Entity}
        mockSetup   func(*Mock{Entity}Repo, context.Context, *domain.{Entity})
        wantErr     bool
        errContains string
        checkResult func(*testing.T, *domain.{Entity})
    }{
        {
            name:  "success",
            input: valid{Entity}(),
            mockSetup: func(repo *Mock{Entity}Repo, ctx context.Context, input *{Entity}) {
                output := valid{Entity}()
                output.Id = 1
                repo.On("Create", ctx, input).Return(output, nil)
            },
            wantErr: false,
            checkResult: func(t *testing.T, result *domain.{Entity}) {
                assert.NotZero(t, result.ID)
                assert.Equal(t, "value1", result.Field1)
            },
        },
        {
            name: "validation error - missing required field",
            input: &{Entity}{
                Field2: 123,
                // Field1 missing
            },
            mockSetup:   func(repo *Mock{Entity}Repo, ctx context.Context, input *{Entity}) {},
            wantErr:     true,
            errContains: "Field1",
        },
        {
            name:  "repository error",
            input: valid{Entity}(),
            mockSetup: func(repo *Mock{Entity}Repo, ctx context.Context, input *{Entity}) {
                repo.On("Create", ctx, input).Return(nil, errors.New("database error"))
            },
            wantErr: true,
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            mockRepo := new(Mock{Entity}Repo)
            uc := setup{Entity}UseCase(mockRepo)
            ctx := context.Background()
            
            tt.mockSetup(mockRepo, ctx, tt.input)
            
            result, err := uc.Create{Entity}(ctx, tt.input)
            
            if tt.wantErr {
                assert.Error(t, err)
                if tt.errContains != "" {
                    assert.Contains(t, err.Error(), tt.errContains)
                }
            } else {
                assert.NoError(t, err)
                if tt.checkResult != nil {
                    tt.checkResult(t, result)
                }
            }
            
            mockRepo.AssertExpectations(t)
        })
    }
}
```

#### Filter Passthrough Tests

CRITICAL: Test that use case correctly passes filters to repository

```go
func TestList{Entities}(t *testing.T) {
    tests := []struct {
        name        string
        params      *pagination.OffsetPaginationParams
        filter      map[string]interface{}
        mockSetup   func(*Mock{Entity}Repo, context.Context, uint64, uint32, map[string]interface{})
        wantErr     bool
        checkResult func(*testing.T, []*{Entity}, *pagination.Meta)
    }{
        {
            name: "success - passes filter to repository",
            params: &pagination.OffsetPaginationParams{
                Offset: 0,
                Limit:  10,
            },
            filter: map[string]interface{}{"project_id": uint64(1)},
            mockSetup: func(repo *Mock{Entity}Repo, ctx context.Context, offset uint64, limit uint32, filter map[string]interface{}) {
                entities := []*domain.{Entity}{valid{Entity}()}
                meta := &pagination.Meta{TotalCount: 1, Offset: 0, Limit: 10}
                // Verify exact filter is passed through
                repo.On("List{Entities}", ctx, offset, limit, filter).Return(entities, meta, nil)
            },
            wantErr: false,
        },
        {
            name: "success - passes nil filter to repository",
            params: &pagination.OffsetPaginationParams{Offset: 0, Limit: 10},
            filter: nil,
            mockSetup: func(repo *Mock{Entity}Repo, ctx context.Context, offset uint64, limit uint32, filter map[string]interface{}) {
                entities := []*{Entity}{valid{Entity}()}
                meta := &pagination.Meta{TotalCount: 1}
                repo.On("List{Entities}", ctx, offset, limit, filter).Return(entities, meta, nil)
            },
            wantErr: false,
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            mockRepo := new(Mock{Entity}Repo)
            uc := setup{Entity}UseCase(mockRepo)
            ctx := context.Background()
            
            tt.mockSetup(mockRepo, ctx, tt.params.Offset, tt.params.Limit, tt.filter)
            
            results, meta, err := uc.List{Entities}(ctx, tt.params, tt.filter)
            
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
                if tt.checkResult != nil {
                    tt.checkResult(t, results, meta)
                }
            }
            
            mockRepo.AssertExpectations(t)
        })
    }
}
```

#### Event Publishing Tests Pattern

**When**: Use cases integrate event publishing for domain events

**Mock Setup**:
```go
// Mock event publisher
type MockPublisher struct {
	mock.Mock
}

func (m *MockPublisher) PublishSymbolCreated(ctx context.Context, symbol *domain.Symbol) error {
	args := m.Called(ctx, symbol)
	return args.Error(0)
}

func (m *MockPublisher) PublishSymbolUpdated(ctx context.Context, symbol *domain.Symbol) error {
	args := m.Called(ctx, symbol)
	return args.Error(0)
}

func (m *MockPublisher) PublishSymbolDeleted(ctx context.Context, symbol *domain.Symbol) error {
	args := m.Called(ctx, symbol)
	return args.Error(0)
}

// Mock transaction
type MockTransaction struct {
	mock.Mock
}

func (m *MockTransaction) InTx(ctx context.Context, fn func(ctx context.Context) error) error {
	args := m.Called(ctx, fn)
	if args.Error(0) != nil {
		return args.Error(0)
	}
	// Execute callback immediately without real transaction
	return fn(ctx)
}

// Test setup with all dependencies
type testDeps struct {
	repo *MockSymbolRepo
	pub  *MockPublisher
	tx   *MockTransaction
	uc   domain.SymbolUseCase
}

func setupSymbolUseCaseWithDeps() *testDeps {
	logger := log.NewStdLogger(os.Stdout)
	v := NewValidator()
	mockRepo := new(MockSymbolRepo)
	mockPub := new(MockPublisher)
	mockTx := new(MockTransaction)

	// Default transaction behavior - executes callback
	mockTx.On("InTx", mock.Anything, mock.Anything).Return(nil).Maybe()

	uc := NewUseCase(mockRepo, v, mockTx, mockPub, logger)

	return &testDeps{
		repo: mockRepo,
		pub:  mockPub,
		tx:   mockTx,
		uc:   uc,
	}
}
```

**Test Pattern - Event Publishing Success**:
```go
func TestCreateSymbol_PublishesEvent(t *testing.T) {
	tests := []struct {
		name           string
		symbol         *domain.Symbol
		repoReturn     *domain.Symbol
		publishErr     error
		wantErr        bool
		wantEventCall  bool
		checkEventData func(*testing.T, *domain.Symbol)
	}{
		{
			name:   "publishes SymbolCreated event on success",
			symbol: validSymbol(),
			repoReturn: func() *domain.Symbol {
				s := validSymbol()
				s.ID = 1
				return s
			}(),
			publishErr:    nil,
			wantErr:       false,
			wantEventCall: true,
			checkEventData: func(t *testing.T, published *domain.Symbol) {
				assert.Equal(t, uint64(1), published.ID)
				assert.Equal(t, "Test Symbol", published.Label)
			},
		},
		{
			name:   "rolls back transaction on publish failure",
			symbol: validSymbol(),
			repoReturn: func() *domain.Symbol {
				s := validSymbol()
				s.ID = 1
				return s
			}(),
			publishErr:    errors.New("publish failed"),
			wantErr:       true,
			wantEventCall: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			deps := setupSymbolUseCaseWithDeps()
			ctx := context.Background()

			// Setup repo mock
			deps.repo.On("Create", ctx, mock.AnythingOfType("*domain.Symbol")).Return(tt.repoReturn, nil)

			// Setup publisher mock - capture published symbol
			var publishedSymbol *domain.Symbol
			deps.pub.On("PublishSymbolCreated", ctx, mock.AnythingOfType("*domain.Symbol")).
				Run(func(args mock.Arguments) {
					publishedSymbol = args.Get(1).(*domain.Symbol)
				}).
				Return(tt.publishErr)

			result, err := deps.uc.CreateSymbol(ctx, tt.symbol)

			if tt.wantErr {
				assert.Error(t, err)
				assert.Nil(t, result)
			} else {
				assert.NoError(t, err)
				assert.NotNil(t, result)
			}

			if tt.wantEventCall {
				deps.pub.AssertCalled(t, "PublishSymbolCreated", ctx, mock.AnythingOfType("*domain.Symbol"))
				if tt.checkEventData != nil && publishedSymbol != nil {
					tt.checkEventData(t, publishedSymbol)
				}
			}

			deps.repo.AssertExpectations(t)
			deps.pub.AssertExpectations(t)
		})
	}
}
```

**Test Pattern - Event Not Published on Failure**:
```go
func TestEventPublishing_NotCalledOnValidationFailure(t *testing.T) {
	t.Run("CreateSymbol does not publish event on validation failure", func(t *testing.T) {
		deps := setupSymbolUseCaseWithDeps()
		ctx := context.Background()

		invalidSymbol := &domain.Symbol{
			Label: "", // Invalid - missing required field
		}

		_, err := deps.uc.CreateSymbol(ctx, invalidSymbol)

		assert.Error(t, err)
		deps.pub.AssertNotCalled(t, "PublishSymbolCreated", mock.Anything, mock.Anything)
	})

	t.Run("CreateSymbol does not publish event on repo failure", func(t *testing.T) {
		deps := setupSymbolUseCaseWithDeps()
		ctx := context.Background()

		symbol := validSymbol()
		deps.repo.On("Create", ctx, mock.AnythingOfType("*domain.Symbol")).
			Return(nil, errors.New("database error"))

		_, err := deps.uc.CreateSymbol(ctx, symbol)

		assert.Error(t, err)
		deps.pub.AssertNotCalled(t, "PublishSymbolCreated", mock.Anything, mock.Anything)
	})
}
```

**Delete with Event Publishing**:
```go
func TestDeleteSymbol_PublishesEvent(t *testing.T) {
	tests := []struct {
		name           string
		symbolID       uint64
		foundSymbol    *domain.Symbol
		publishErr     error
		wantErr        bool
		checkEventData func(*testing.T, *domain.Symbol)
	}{
		{
			name:     "publishes SymbolDeleted event on success",
			symbolID: 1,
			foundSymbol: func() *domain.Symbol {
				s := validSymbol()
				s.ID = 1
				return s
			}(),
			publishErr: nil,
			wantErr:    false,
			checkEventData: func(t *testing.T, published *domain.Symbol) {
				assert.Equal(t, uint64(1), published.ID)
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			deps := setupSymbolUseCaseWithDeps()
			ctx := context.Background()

			// Must find symbol before delete (for event payload)
			deps.repo.On("FindByID", ctx, tt.symbolID).Return(tt.foundSymbol, nil)
			deps.repo.On("Delete", ctx, tt.symbolID).Return(nil)

			// Capture published symbol
			var publishedSymbol *domain.Symbol
			deps.pub.On("PublishSymbolDeleted", ctx, mock.AnythingOfType("*domain.Symbol")).
				Run(func(args mock.Arguments) {
					publishedSymbol = args.Get(1).(*domain.Symbol)
				}).
				Return(tt.publishErr)

			err := deps.uc.DeleteSymbol(ctx, tt.symbolID)

			if tt.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}

			if tt.checkEventData != nil && publishedSymbol != nil {
				tt.checkEventData(t, publishedSymbol)
			}

			deps.repo.AssertExpectations(t)
			deps.pub.AssertExpectations(t)
		})
	}
}
```

**Key Testing Principles**:
1. **Test event publishing happens** - Verify `PublishXxxEvent` is called
2. **Test event data correctness** - Capture and assert event payload
3. **Test transaction rollback** - Verify failure prevents commit
4. **Test event not published on validation/repo failure** - Use `AssertNotCalled`
5. **Use testDeps pattern** - Return all mocks for granular assertions

### 3. Service Layer Tests

**File**: \`internal/service/{entity}_test.go\`

#### Service Mock Pattern

```go
type mock{Entity}UseCase struct {
    mock.Mock
}

func (uc *mock{Entity}UseCase) List{Entities}(ctx context.Context, params *pagination.OffsetPaginationParams, filter map[string]interface{}) ([]*biz.{Entity}, *pagination.Meta, error) {
    args := uc.Called(ctx, params, filter)
    if args.Get(0) == nil {
        return nil, nil, args.Error(2)
    }
    if args.Get(1) == nil {
        return args.Get(0).([]*biz.{Entity}), nil, args.Error(2)
    }
    return args.Get(0).([]*biz.{Entity}), args.Get(1).(*pagination.Meta), args.Error(2)
}
```

## Critical Testing Rules

### 1. Mock Signatures MUST Match Interfaces Exactly

```go
// Interface in biz/interfaces.go
List{Entities}(ctx context.Context, offset uint64, limit uint32, filter map[string]interface{}) ([]*{Entity}, *pagination.Meta, error)

// Mock MUST have identical signature
func (m *Mock{Entity}Repo) List{Entities}(ctx context.Context, offset uint64, limit uint32, filter map[string]interface{}) ([]*{Entity}, *pagination.Meta, error) {
    args := m.Called(ctx, offset, limit, filter)  // Pass ALL parameters
    // ...
}
```

### 2. Test All Filter Scenarios

- ✅ Valid filter with single field
- ✅ Valid filter with multiple fields
- ✅ Nil filter
- ✅ Empty filter (\`map[string]interface{}{}\`)
- ✅ Filter with pagination

### 3. Test All Error Paths

- ✅ Validation errors
- ✅ Repository errors
- ✅ Not found errors
- ✅ Duplicate entry errors

### 4. Always Assert Mock Expectations

```go
mockRepo.AssertExpectations(t)  // Verify all expected calls happened
```

## Validation Checklist

- [ ] Test file exists alongside implementation
- [ ] All public methods have test coverage
- [ ] Table-driven tests used for multiple scenarios
- [ ] Success and error cases both tested
- [ ] Mock signatures exactly match interface signatures
- [ ] Filter passthrough tested (if applicable)
- [ ] Pagination metadata validated
- [ ] Mock expectations asserted (\`AssertExpectations\`)
- [ ] Helper functions for valid test data
- [ ] Setup/cleanup functions for repo tests
- [ ] Context propagated to all calls

## Anti-Patterns

❌ **DON'T:**
- Have mock signatures different from interfaces
- Forget to call \`AssertExpectations(t)\`
- Skip error case testing
- Test only happy paths
- Hardcode test data in test cases
- Use production database for tests

✅ **DO:**
- Match mock signatures exactly to interfaces
- Always assert expectations
- Test both success and error paths
- Use table-driven tests
- Create helper functions for test data
- Use in-memory database for repo tests

## Success Criteria

Tests MUST:
1. Pass with \`go test ./internal/...\`
2. Achieve >85% coverage for the layer
3. Run quickly (<5s for unit tests)
4. Be deterministic (no flaky tests)
5. Clean up resources (database, mocks)
6. Verify all mock expectations
7. Test all public methods

