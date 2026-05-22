---
name: domain-driven-design
description: Domain-Driven Design tactical patterns for complex business domains. Use when modeling entities, value objects, domain services, repositories, or establishing bounded contexts.
context: fork
agent: backend-system-architect
version: 1.0.0
tags: [ddd, domain-modeling, entities, value-objects, bounded-contexts, python, 2026]
author: SkillForge
user-invocable: false
---

# Domain-Driven Design Tactical Patterns

Model complex business domains with entities, value objects, and bounded contexts.

## Overview

- Modeling complex business logic
- Separating domain from infrastructure
- Establishing clear boundaries between subdomains
- Building rich domain models with behavior
- Implementing ubiquitous language in code

## Building Blocks Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    DDD Building Blocks                       │
├─────────────────────────────────────────────────────────────┤
│  ENTITIES           VALUE OBJECTS        AGGREGATES         │
│  Order (has ID)     Money (no ID)        [Order]→Items      │
│                                                              │
│  DOMAIN SERVICES    REPOSITORIES         DOMAIN EVENTS      │
│  PricingService     IOrderRepository     OrderSubmitted     │
│                                                              │
│  FACTORIES          SPECIFICATIONS       MODULES            │
│  OrderFactory       OverdueOrderSpec     orders/, payments/ │
└─────────────────────────────────────────────────────────────┘
```

## Quick Reference

### Entity (Has Identity)

```python
from dataclasses import dataclass, field
from uuid import UUID
from uuid_utils import uuid7

@dataclass
class Order:
    """Entity: Has identity, mutable state, lifecycle."""
    id: UUID = field(default_factory=uuid7)
    customer_id: UUID = field(default=None)
    status: str = "draft"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.id == other.id  # Identity equality

    def __hash__(self) -> int:
        return hash(self.id)
```

See [entities-value-objects.md](references/entities-value-objects.md) for complete patterns.

### Value Object (Immutable)

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)  # MUST be frozen!
class Money:
    """Value Object: Defined by attributes, not identity."""
    amount: Decimal
    currency: str

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
```

See [entities-value-objects.md](references/entities-value-objects.md) for Address, DateRange examples.

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Entity vs VO | Has unique ID + lifecycle? Entity. Otherwise VO |
| Entity equality | By ID, not attributes |
| Value object mutability | Always immutable (`frozen=True`) |
| Repository scope | One per aggregate root |
| Domain events | Collect in entity, publish after persist |
| Context boundaries | By business capability, not technical |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER have anemic domain models (data-only classes)
@dataclass
class Order:
    id: UUID
    items: list  # WRONG - no behavior!

# NEVER leak infrastructure into domain
class Order:
    def save(self, session: Session):  # WRONG - knows about DB!

# NEVER use mutable value objects
@dataclass  # WRONG - missing frozen=True
class Money:
    amount: Decimal

# NEVER have repositories return ORM models
async def get(self, id: UUID) -> OrderModel:  # WRONG - return domain!
```

## Related Skills

- `aggregate-patterns` - Deep dive on aggregate design
- `distributed-locks` - Cross-aggregate coordination
- `database-schema-designer` - Schema design for DDD

## References

- [Entities & Value Objects](references/entities-value-objects.md) - Full patterns
- [Repositories](references/repositories.md) - Repository pattern implementation
- [Domain Events](references/domain-events.md) - Event collection and publishing
- [Bounded Contexts](references/bounded-contexts.md) - Context mapping and ACL

## Capability Details

### entities
**Keywords:** entity, identity, lifecycle, mutable, domain object
**Solves:** Model entities in Python, identity equality, adding behavior

### value-objects
**Keywords:** value object, immutable, frozen, dataclass, structural equality
**Solves:** Create immutable value objects, when to use VO vs entity

### domain-services
**Keywords:** domain service, business logic, cross-aggregate, stateless
**Solves:** When to use domain service, logic spanning aggregates

### repositories
**Keywords:** repository, persistence, collection, IRepository, protocol
**Solves:** Implement repository pattern, abstract DB access, ORM mapping

### bounded-contexts
**Keywords:** bounded context, context map, ACL, subdomain, ubiquitous language
**Solves:** Define bounded contexts, integrate with ACL, context relationships
