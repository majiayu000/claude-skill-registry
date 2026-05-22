---
name: aggregate-patterns
description: DDD aggregate design patterns for consistency boundaries and invariants. Use when designing aggregate roots, enforcing business invariants, handling cross-aggregate references, or optimizing aggregate size.
context: fork
agent: backend-system-architect
version: 1.0.0
tags: [ddd, aggregate, consistency, invariants, domain-modeling, python, 2026]
author: SkillForge
user-invocable: false
---

# Aggregate Design Patterns

Design aggregates with clear boundaries, invariants, and consistency guarantees.

## Overview

- Defining transactional consistency boundaries
- Enforcing business invariants across related entities
- Designing aggregate roots and their children
- Handling references between aggregates
- Optimizing aggregate size for performance

## Core Concepts

```
┌─────────────────────────────────────────────────────────┐
│                 ORDER AGGREGATE                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Order (Aggregate Root)                   │   │
│  │  • id: UUID (UUIDv7)                            │   │
│  │  • customer_id: UUID (reference by ID!)         │   │
│  │  • status: OrderStatus                          │   │
│  └─────────────────────────────────────────────────┘   │
│           │                      │                      │
│  ┌────────────────┐    ┌────────────────┐              │
│  │  OrderItem     │    │  OrderItem     │              │
│  │  (child)       │    │  (child)       │              │
│  └────────────────┘    └────────────────┘              │
│                                                         │
│  INVARIANTS enforced by root:                          │
│  • Total = sum of items                                │
│  • Max 100 items per order                             │
│  • Cannot modify after shipped                         │
└─────────────────────────────────────────────────────────┘
```

### Four Rules

1. **Root controls access** - External code only references aggregate root
2. **Transactional boundary** - One aggregate per transaction
3. **Reference by ID** - Never hold references to other aggregates
4. **Invariants enforced** - Root ensures all business rules

## Quick Reference

```python
from dataclasses import dataclass, field
from uuid import UUID
from uuid_utils import uuid7

@dataclass
class OrderAggregate:
    """Aggregate root with invariant enforcement."""

    id: UUID = field(default_factory=uuid7)
    customer_id: UUID  # Reference by ID, not Customer object!
    _items: list["OrderItem"] = field(default_factory=list)
    status: str = "draft"

    MAX_ITEMS = 100

    def add_item(self, product_id: UUID, quantity: int, price: Money) -> None:
        """Add item with invariant checks."""
        self._ensure_modifiable()
        if len(self._items) >= self.MAX_ITEMS:
            raise DomainError("Max items exceeded")
        self._items.append(OrderItem(product_id, quantity, price))

    def _ensure_modifiable(self) -> None:
        if self.status != "draft":
            raise DomainError(f"Cannot modify {self.status} order")
```

See [aggregate-root-template.py](templates/aggregate-root-template.py) for complete implementation.

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Aggregate size | Small (< 20 children), split if larger |
| Cross-aggregate refs | Always by ID, never by object |
| Consistency | Immediate within, eventual across |
| Events | Collect in root, publish after persist |

See [aggregate-sizing.md](references/aggregate-sizing.md) for sizing guidelines.

## Anti-Patterns (FORBIDDEN)

```python
# NEVER reference aggregates by object
customer: Customer  # WRONG → customer_id: UUID

# NEVER modify multiple aggregates in one transaction
order.submit()
inventory.reserve(items)  # WRONG - use domain events

# NEVER expose mutable collections
def items(self) -> list:
    return self._items  # WRONG → return tuple(self._items)

# NEVER have unbounded collections
orders: list[Order]  # WRONG - grows unbounded
```

## Related Skills

- `domain-driven-design` - DDD building blocks (entities, VOs)
- `distributed-locks` - Cross-aggregate coordination
- `idempotency-patterns` - Safe retries

## References

- [Aggregate Sizing](references/aggregate-sizing.md) - When to split
- [Invariant Enforcement](references/invariant-enforcement.md) - Business rules
- [Eventual Consistency](references/eventual-consistency.md) - Cross-aggregate

## Capability Details

### aggregate-root
**Keywords:** aggregate root, consistency boundary, transactional
**Solves:** Design aggregate roots, control child access, enforce boundaries

### invariants
**Keywords:** invariant, business rule, validation, specification
**Solves:** Enforce business rules, validate state, specification pattern

### aggregate-sizing
**Keywords:** aggregate size, small aggregate, performance
**Solves:** Right-size aggregates, when to split, performance trade-offs

### cross-aggregate
**Keywords:** reference by ID, eventual consistency, domain events
**Solves:** Reference other aggregates, coordinate changes, eventual consistency
