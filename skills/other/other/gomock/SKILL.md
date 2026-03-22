---
name: gomock
description: GoMock for generating and using mock implementations of Go interfaces
category: Testing BDD
---

# Skill: gomock

## What I do

I provide expertise in using GoMock to create and manage mock implementations of interfaces for unit testing. I focus on defining expectations, verifying call sequences, and isolating components for reliable BDD-style testing.

## When to use me

- When writing unit tests for components that depend on interfaces
- When verifying complex interactions between a service and its repository
- When simulating error conditions or specific return values from dependencies

## Core principles

1. **Isolation**: Use mocks to test the logic of a single component without invoking its real dependencies.
2. **Expectation setting**: Clearly define what calls are expected, what they should return, and how many times they should occur.
3. **Verification**: Ensure that all expected calls were made by verifying the controller state at the end of the test.
4. **Readability**: Keep mock setups concise and readable to maintain the focus on the behaviour being tested.

## Patterns & examples

**Basic mock setup:**
```go
func TestUserService(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish() // Required to verify expectations

    mockRepo := mocks.NewMockUserRepository(ctrl)
    svc := NewUserService(mockRepo)

    // Set expectations
    mockRepo.EXPECT().
        Get(gomock.Eq(1)).
        Return(&User{ID: 1, Name: "Alice"}, nil).
        Times(1)

    user, err := svc.FindUser(1)
    // Assertions...
}
```

**Using argument matchers:**
Use `gomock.Any()` when the specific value doesn't matter, or custom matchers for complex validation.
```go
mockRepo.EXPECT().Save(gomock.Any()).Return(nil)
```

**Stubbing behavior with DoAndReturn:**
```go
mockRepo.EXPECT().Get(gomock.Any()).DoAndReturn(func(id int) (*User, error) {
    if id == 0 {
        return nil, errors.New("not found")
    }
    return &User{ID: id}, nil
})
```

**Ordering calls:**
```go
gomock.InOrder(
    mockRepo.EXPECT().Get(1).Return(u, nil),
    mockRepo.EXPECT().Save(u).Return(nil),
)
```

## Anti-patterns to avoid

- ❌ **Over-mocking**: Do not mock internal implementation details. Only mock at interface boundaries.
- ❌ **Ignoring ctrl.Finish()**: Forgetting to call `Finish()` (or use the built-in cleanup in newer Go versions) means failed expectations won't cause the test to fail.
- ❌ **Brittle expectations**: Avoid overly strict ordering or call counts unless they are critical to the system's correctness.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/Gomock.md`

## Related skills

- `bdd-workflow`: For structuring tests that describe system behaviour
- `ginkgo-gomega`: For using mocks within a Ginkgo test suite
- `code-generation`: For automating the creation of mock files using `mockgen`
- `golang`: For principles of interface design and composition
