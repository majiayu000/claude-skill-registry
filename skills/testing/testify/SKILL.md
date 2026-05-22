---
name: Testify
description: Testing toolkit with assertions, mocks, and suites.
metadata:
  labels: [golang, testify, testing, mock]
  triggers:
    files: ['**/*_test.go']
    keywords: [testify, assert, require, mock, suite]
---

# Testify Standards

## Assert Package

```go
import (
    "testing"
    "github.com/stretchr/testify/assert"
)

func TestSomething(t *testing.T) {
    // Equality
    assert.Equal(t, 123, result)
    assert.NotEqual(t, 456, result)

    // Boolean
    assert.True(t, ok)
    assert.False(t, failed)

    // Nil checks
    assert.Nil(t, err)
    assert.NotNil(t, obj)

    // Error checks
    assert.NoError(t, err)
    assert.Error(t, err)
    assert.ErrorIs(t, err, ErrNotFound)
    assert.ErrorContains(t, err, "not found")

    // Collections
    assert.Contains(t, slice, item)
    assert.Len(t, slice, 3)
    assert.Empty(t, slice)
    assert.NotEmpty(t, slice)
    assert.ElementsMatch(t, expected, actual)  // Order independent

    // Comparison
    assert.Greater(t, 2, 1)
    assert.GreaterOrEqual(t, 2, 2)
    assert.Less(t, 1, 2)

    // Type assertions
    assert.IsType(t, &User{}, obj)
    assert.Implements(t, (*io.Reader)(nil), obj)

    // With message
    assert.Equal(t, expected, actual, "values should match")
}
```

## Require Package

```go
import "github.com/stretchr/testify/require"

func TestWithRequire(t *testing.T) {
    // Stops test immediately on failure
    user, err := GetUser(1)
    require.NoError(t, err)       // Fails here stops test
    require.NotNil(t, user)

    // Continue knowing user is valid
    assert.Equal(t, "John", user.Name)
}
```

## Mock Package

```go
import (
    "testing"
    "github.com/stretchr/testify/mock"
)

// Interface to mock
type UserRepository interface {
    FindByID(id int) (*User, error)
    Save(user *User) error
}

// Mock implementation
type MockUserRepository struct {
    mock.Mock
}

func (m *MockUserRepository) FindByID(id int) (*User, error) {
    args := m.Called(id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

func (m *MockUserRepository) Save(user *User) error {
    args := m.Called(user)
    return args.Error(0)
}

// Test using mock
func TestUserService(t *testing.T) {
    mockRepo := new(MockUserRepository)

    // Setup expectations
    mockRepo.On("FindByID", 1).Return(&User{ID: 1, Name: "John"}, nil)
    mockRepo.On("Save", mock.Anything).Return(nil)

    service := NewUserService(mockRepo)
    user, err := service.GetUser(1)

    assert.NoError(t, err)
    assert.Equal(t, "John", user.Name)

    // Verify expectations
    mockRepo.AssertExpectations(t)
    mockRepo.AssertCalled(t, "FindByID", 1)
    mockRepo.AssertNumberOfCalls(t, "FindByID", 1)
}
```

## Mock Matching

```go
// Exact match
mockRepo.On("FindByID", 1).Return(user, nil)

// Any value
mockRepo.On("Save", mock.Anything).Return(nil)

// Type match
mockRepo.On("Save", mock.AnythingOfType("*User")).Return(nil)

// Custom matcher
mockRepo.On("FindByID", mock.MatchedBy(func(id int) bool {
    return id > 0
})).Return(user, nil)

// Multiple calls
mockRepo.On("FindByID", 1).Return(user, nil).Once()
mockRepo.On("FindByID", 1).Return(nil, ErrNotFound).Once()

// Call order
mockRepo.On("Save", mock.Anything).Return(nil).Run(func(args mock.Arguments) {
    user := args.Get(0).(*User)
    user.ID = 123  // Modify argument
})
```

## Suite Package

```go
import (
    "testing"
    "github.com/stretchr/testify/suite"
)

type UserServiceTestSuite struct {
    suite.Suite
    db      *sql.DB
    service *UserService
}

func (s *UserServiceTestSuite) SetupSuite() {
    // Run once before all tests
    s.db = setupTestDB()
}

func (s *UserServiceTestSuite) TearDownSuite() {
    // Run once after all tests
    s.db.Close()
}

func (s *UserServiceTestSuite) SetupTest() {
    // Run before each test
    s.service = NewUserService(s.db)
}

func (s *UserServiceTestSuite) TearDownTest() {
    // Run after each test
    cleanupTestData(s.db)
}

func (s *UserServiceTestSuite) TestGetUser() {
    user, err := s.service.GetUser(1)
    s.NoError(err)
    s.Equal("John", user.Name)
}

func (s *UserServiceTestSuite) TestCreateUser() {
    user, err := s.service.CreateUser("Jane", "jane@example.com")
    s.NoError(err)
    s.NotZero(user.ID)
}

// Run the suite
func TestUserServiceSuite(t *testing.T) {
    suite.Run(t, new(UserServiceTestSuite))
}
```

## Table-Driven Tests

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 1, 2, 3},
        {"negative", -1, -1, -2},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            assert.Equal(t, tt.expected, result)
        })
    }
}
```

## Best Practices

1. **require vs assert**: Use `require` for setup, `assert` for verification
2. **Mocks**: Generate with mockery for large interfaces
3. **Suites**: Use for tests sharing setup/teardown
4. **Messages**: Add context with assertion messages
5. **Parallel**: Use `t.Parallel()` for independent tests
