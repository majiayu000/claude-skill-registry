---
name: coding
description: Coding standards and best practices for implementation work
---

# Coding Standards

## Core Principles

### Single Responsibility

Every function, type, and package has **one reason to change**.

```go
// ❌ Mixed responsibilities - validates, charges, emails, tracks
func ProcessOrder(order Order) error { ... }

// ✅ Orchestrates via dependencies, doesn't implement
func (s *Service) ProcessOrder(ctx context.Context, order Order) error {
    validated, err := s.validator.Validate(ctx, order)
    if err != nil { return fmt.Errorf("validation: %w", err) }

    return s.fulfillment.Fulfill(ctx, validated)
}
```

**Test:** Can you describe what this code does without using "and"?

### Accept Interfaces, Return Structs

Functions accept interfaces (flexible for callers/testing) and return concrete types (clear for consumers).

### Fail Fast with Clear Errors

Detect errors early. Return them with context.

```go
// ❌ Silent failure
func GetUser(userID string) *User {
    user, _ := db.Find(userID)
    if user == nil {
        return &User{}  // Returns fake user, hides problem
    }
    return user
}

// ✅ Fail fast with wrapped error
func GetUser(ctx context.Context, userID string) (*User, error) {
    user, err := db.Find(ctx, userID)
    if err != nil {
        return nil, fmt.Errorf("find user %s: %w", userID, err)
    }
    if user == nil {
        return nil, fmt.Errorf("user %s: %w", userID, ErrNotFound)
    }
    return user, nil
}
```

---

## Error Handling

### Handle Errors Immediately

```go
// ✅ Happy path stays left-aligned
result, err := s.execute(ctx, req)
if err != nil {
    return nil, fmt.Errorf("execute: %w", err)
}
return result, nil
```

### Use Sentinel and Typed Errors

```go
var ErrNotFound = errors.New("not found")  // Sentinel for expected conditions

// Callers check with errors.Is / errors.As
if errors.Is(err, ErrNotFound) { /* handle */ }
```

### Never Ignore Errors

```go
// ❌ NEVER
result, _ := doSomething()

// ✅ Handle or log explicitly
if err := cleanup(); err != nil {
    log.Printf("cleanup failed: %v", err)
}
```

---

## Code Structure

### Function Design

| Guideline | Rationale |
|-----------|-----------|
| < 30 lines preferred | Fits in one mental chunk |
| < 4 parameters | More suggests missing abstraction — use options struct |
| Context first | `ctx context.Context` is always the first parameter |
| Error last | Return `error` as the last return value |
| Return early | Reduces nesting, keeps happy path left-aligned |

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Exported | MixedCaps | `ProcessOrder`, `UserID` |
| Unexported | mixedCaps | `processOrder`, `userID` |
| Acronyms | All caps | `HTTPServer`, `userID` (not `userId`) |
| Interfaces | -er suffix when possible | `Reader`, `Validator` |
| Packages | Short, lowercase, no underscores | `payment`, `userauth` |

**Name length proportional to scope.** `i` in a 3-line loop is fine; `i` at package scope is not.

---

## Documentation

| Element | Requires Comment |
|---------|------------------|
| Exported functions/methods | Yes — starts with function name |
| Exported types | Yes |
| Packages | Yes — in `doc.go` or main file |
| Non-obvious logic | Inline comment |
| Unexported | Only if complex |

**Document contracts, not implementation.** What it does and what errors it returns, not how.

---

## Package Organization

```
project/
├── cmd/server/main.go    # Entrypoint only - wiring, no logic
├── internal/             # Private to this module
└── pkg/                  # Public API (if any)
```

**`internal/` is your friend.** Prevents external packages from depending on implementation details.

---

## Code Changes

### Before Modifying Existing Code

1. **Read** the godoc comments
2. **Check** existing tests for expected behavior
3. **Understand** the interface contract before changing implementation
4. **Run** `go vet` and `staticcheck` after changes
5. **Ask** if the contract is unclear

### Change Scope Discipline

```markdown
⚠️ SCOPE BOUNDARY

Original task: Fix discount calculation bug
Observed: OrderService could use refactoring

**Correct action:** Fix the bug only. Note refactoring opportunity separately.
**Incorrect action:** Refactor while fixing bug.
```

One change type per commit. Bug fixes do not include refactoring. Refactoring does not change behavior.

---

## Tooling Requirements

**Run before every commit:**
```bash
go fmt ./...        # Format
go vet ./...        # Static analysis
staticcheck ./...   # Extended checks (if available)
go test -race ./... # Tests with race detector
```

---

## Anti-Patterns

| Pattern | Problem | Alternative |
|---------|---------|-------------|
| Naked returns | Confusing, error-prone | Always name what you're returning |
| `panic` for errors | Crashes callers | Return errors |
| `interface{}` everywhere | No type safety | Use generics or specific types |
| God package | Untestable, circular deps | Split by responsibility |
| `init()` with side effects | Hidden, order-dependent | Explicit initialization |
| Global mutable state | Race conditions, test pollution | Dependency injection |
