---
name: golang-clean-architecture
description: Clean Architecture audit for Go services. Use when reviewing layered architecture, dependency rules, or gRPC/usecase/repository patterns. Ensures proper separation of concerns and dependency inversion.
license: MIT
metadata:
  author: saifoelloh
  version: "2.0.0"
  parent_skill: golang-best-practices
  sources:
    - "Clean Architecture (Robert C. Martin)"
    - "Learning Go: An Idiomatic Approach (Jon Bodner)"
  last_updated: "2026-01-22"
---

# Golang Clean Architecture

Audit Go services for Clean Architecture compliance. Ensures proper layering, dependency rules, and separation of concerns in gRPC → Usecase → Repository → Domain architectures.

## When to Apply

Use this skill when:
- Auditing service architecture
- Reviewing new features for layer violations
- Refactoring toward Clean Architecture
- Code review for dependency rules
- Planning service structure
- Migrating to layered architecture
- Ensuring testability through dependency injection

## Architecture Layers

```
┌─────────────────────────────────────┐
│  Delivery (gRPC/HTTP/GraphQL)       │ ← Thin, no business logic
├─────────────────────────────────────┤
│  Usecase (Business Logic)           │ ← Orchestration
├─────────────────────────────────────┤
│  Repository (Data Access)           │ ← CRUD only
├─────────────────────────────────────┤
│  Domain (Entities/Interfaces)       │ ← Pure business logic
└─────────────────────────────────────┘
```

**Dependency Rule**: Dependencies point INWARD only (toward domain).

## Rules Covered (9 total)

### High-Impact Patterns (4)

- `high-business-logic-handler` - Keep delivery layer thin
- `high-business-logic-repository` - No business logic in data layer
- `high-constructor-creates-deps` - Inject dependencies, don't create
- `high-transaction-in-repository` - Transactions belong in usecase

### Architecture Rules (5)

- `arch-domain-import-infra` - Domain must not import infrastructure
- `arch-concrete-dependency` - Depend on interfaces, not concrete types
- `arch-repository-business-logic` - Repositories do CRUD only
- `arch-usecase-orchestration` - Usecases orchestrate, entities decide
- `arch-interface-segregation` - Small, consumer-defined interfaces

## Common Violations

### ❌ Business Logic in Handler

```go
// gRPC handler doing calculations
func (h *Handler) CreateOrder(ctx context.Context, req *pb.Request) (*pb.Response, error) {
    total := req.Price * req.Quantity // BAD: calculation in handler
    discount := total * 0.1           // BAD: business rules in delivery layer
    
    order := &domain.Order{
        Total: total - discount,
    }
    return h.orderRepo.Save(ctx, order)
}
```

### ✅ Business Logic in Usecase

```go
// Handler delegates to usecase
func (h *Handler) CreateOrder(ctx context.Context, req *pb.Request) (*pb.Response, error) {
    order, err := h.orderUsecase.Create(ctx, req.Price, req.Quantity)
    if err != nil {
        return nil, err
    }
    return &pb.Response{OrderId: order.ID}, nil
}

// Usecase contains business logic
func (u *OrderUsecase) Create(ctx context.Context, price, quantity int) (*domain.Order, error) {
    total := price * quantity      // GOOD: calculation in usecase
    discount := total * 0.1        // GOOD: business rules in usecase
    
    order := &domain.Order{
        Total: total - discount,
    }
    return u.orderRepo.Save(ctx, order)
}
```

### ❌ Repository with Business Logic

```go
// Repository doing validation and business rules
func (r *OrderRepo) Save(ctx context.Context, order *domain.Order) error {
    if order.Total < 0 {                    // BAD: validation in repository
        return errors.New("invalid total")
    }
    if order.Total > 1000000 {              // BAD: business rule in repository
        order.Status = "needs_approval"     // BAD: state change in repository
    }
    return r.db.Create(order)
}
```

### ✅ Repository Does CRUD Only

```go
// Repository only handles data persistence
func (r *OrderRepo) Save(ctx context.Context, order *domain.Order) error {
    return r.db.Create(order) // GOOD: simple CRUD
}

// Validation happens in usecase or domain entity
func (u *OrderUsecase) Create(ctx context.Context, price, quantity int) (*domain.Order, error) {
    order := domain.NewOrder(price, quantity) // Entity validates itself
    if err := order.Validate(); err != nil {    // GOOD: validation in domain
        return nil, err
    }
    if order.NeedsApproval() {                  // GOOD: business rule in domain
        order.Status = "needs_approval"
    }
    return u.orderRepo.Save(ctx, order)
}
```

## Trigger Phrases

This skill activates when you say:
- "Audit architecture"
- "Check layer dependencies"
- "Review Clean Architecture"
- "Verify separation of concerns"
- "Check dependency rules"
- "Review usecase/repository pattern"
- "Check for layer violations"
- "Audit service structure"

## How to Use

### For Architecture Audit

1. Identify all layers in the codebase
2. Check dependency directions (must point inward)
3. Verify each layer's responsibilities
4. Flag violations with specific rule references

### For Code Review

1. Identify which layer the code belongs to
2. Check against layer-specific rules
3. Verify dependencies are injected, not created
4. Ensure interfaces are defined by consumers

## Output Format

```
## Architecture Violations: X

### [Rule Name] (File: path/to/file.go)
**Layer**: Delivery / Usecase / Repository / Domain
**Issue**: Brief description of violation
**Impact**: Tight coupling / Untestable / Wrong responsibility
**Fix**: Suggested correction
**Example**:
```go
// Corrected code
```

## Related Skills

- [golang-design-patterns](../design-patterns/SKILL.md) - For refactoring large usecases
- [golang-idiomatic-go](../idiomatic-go/SKILL.md) - For interface design patterns
- [golang-error-handling](../error-handling/SKILL.md) - For context propagation across layers

## Philosophy

Based on Uncle Bob's Clean Architecture:

- **Independence** - Business rules don't depend on frameworks, UI, or databases
- **Testability** - Business logic can be tested without external dependencies
- **Flexibility** - Easy to swap implementations (e.g., change database)
- **Maintainability** - Clear boundaries make changes localized

**Key Principle**: The inner circles know nothing about the outer circles.

## Notes

- Rules enforce separation of concerns in Go services
- Particularly focused on gRPC/usecase/repository pattern
- Emphasizes dependency injection for testability
- All examples follow Clean Architecture principles
