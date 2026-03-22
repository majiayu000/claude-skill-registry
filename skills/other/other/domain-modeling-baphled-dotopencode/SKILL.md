---
name: domain-modeling
description: Domain-Driven Design (DDD) and domain modelling patterns
category: Domain Architecture
---

# Skill: domain-modeling

## What I do

I provide expert guidance in Domain-Driven Design (DDD). I help create software that accurately reflects complex business domains through ubiquitous language, bounded contexts, and tactical patterns like entities, value objects, and aggregates. I focus on isolating business logic from technical infrastructure.

## When to use me

- Designing features in complex business domains (e.g., finance, logistics).
- Establishing clear boundaries between different sub-systems (Bounded Contexts).
- Building a shared vocabulary (Ubiquitous Language) between dev and business.
- Refactoring "anaemic" models where logic is scattered in service classes.
- Managing consistency and transaction boundaries for related entities.

## Core principles

1. **Ubiquitous Language** - Use the same precise terminology in code, docs, and talk.
2. **Bounded Contexts** - Define explicit boundaries where a particular model applies.
3. **Rich Domain Model** - Encapsulate business logic and invariants within entities.
4. **Aggregate Roots** - Control all access and changes through a single root entity.
5. **Persistence Ignorance** - Domain models should not know about databases or APIs.

## Patterns & examples

**Pattern: Aggregate Root with Invariants**
```go
type Order struct {
    id     OrderID
    status OrderStatus
    items  []OrderLine
}

func (o *Order) AddItem(p Product, qty int) error {
    if o.status != StatusDraft {
        return ErrOrderLocked
    }
    o.items = append(o.items, OrderLine{p, qty})
    o.recalculateTotal() // Maintain invariant
    return nil
}
```

**Pattern: Value Object (Immutable)**
```go
type Money struct {
    amount   decimal.Decimal
    currency string
}

func (m Money) Add(other Money) (Money, error) {
    if m.currency != other.currency {
        return Money{}, ErrCurrencyMismatch
    }
    return Money{m.amount.Add(other.amount), m.currency}, nil
}
```

**Pattern: Domain Events**
```go
type OrderPlaced struct {
    OrderID OrderID
    Total   Money
}

func (o *Order) Place() error {
    o.status = StatusPlaced
    o.recordEvent(OrderPlaced{o.id, o.total})
    return nil
}
```

**Pattern: Specification Pattern**
```go
type PremiumCustomerSpec struct{}
func (s PremiumCustomerSpec) IsSatisfiedBy(c *Customer) bool {
    return c.TotalSpend().GreaterThan(Threshold)
}
```

**Pattern: Repository Interface**
```go
type OrderRepository interface {
    FindByID(ctx context.Context, id OrderID) (*Order, error)
    Save(ctx context.Context, order *Order) error
}
```

## Anti-patterns

- ❌ **Anaemic Domain Model** - Entities are just data bags; all logic is in services.
- ❌ **Primitive Obsession** - Using `string` for `Email` or `int` for `Money`.
- ❌ **Breaking Encapsulation** - Modifying internal aggregate state from the outside.
- ❌ **Leaking Infrastructure** - Passing database types or HTTP request objects into the domain.
- ❌ **God Models** - A single `User` or `Product` model trying to serve every team's needs.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Domain-Architecture/Domain Modeling.md`

## Related skills

- `service-layer` - Orchestrates domain logic for specific use cases.
- `architecture` - Structural patterns for layered or hexagonal systems.
- `api-design` - Exposing domain operations via consistent interfaces.
- `clean-code` - Essential for expressive ubiquitous language.

