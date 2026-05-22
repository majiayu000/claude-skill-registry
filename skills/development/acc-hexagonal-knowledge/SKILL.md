---
name: acc-hexagonal-knowledge
description: Hexagonal Architecture (Ports & Adapters) knowledge base. Provides patterns, antipatterns, and PHP-specific guidelines for Hexagonal Architecture audits.
---

# Hexagonal Architecture Knowledge Base

Quick reference for Hexagonal Architecture (Ports & Adapters) patterns and PHP implementation guidelines.

## Core Principles

### Hexagonal Architecture Overview

```
                         ┌─────────────────────────────┐
                         │      PRIMARY ACTORS         │
                         │   (Users, External Apps)    │
                         └──────────────┬──────────────┘
                                        │
                         ┌──────────────▼──────────────┐
                         │     DRIVING ADAPTERS        │
                         │  (Controllers, CLI, GUI,    │
                         │   Message Consumers)        │
                         └──────────────┬──────────────┘
                                        │
              ┌─────────────────────────▼─────────────────────────┐
              │                  DRIVING PORTS                     │
              │              (Input Interfaces)                    │
              └─────────────────────────┬─────────────────────────┘
                                        │
              ┌─────────────────────────▼─────────────────────────┐
              │                                                    │
              │              APPLICATION CORE                      │
              │     ┌─────────────────────────────────┐           │
              │     │       APPLICATION LAYER         │           │
              │     │      (Use Cases, Services)      │           │
              │     └─────────────────┬───────────────┘           │
              │                       │                            │
              │     ┌─────────────────▼───────────────┐           │
              │     │         DOMAIN LAYER            │           │
              │     │  (Entities, Value Objects,      │           │
              │     │   Domain Services)              │           │
              │     └─────────────────────────────────┘           │
              │                                                    │
              └─────────────────────────┬─────────────────────────┘
                                        │
              ┌─────────────────────────▼─────────────────────────┐
              │                  DRIVEN PORTS                      │
              │            (Output Interfaces)                     │
              └─────────────────────────┬─────────────────────────┘
                                        │
                         ┌──────────────▼──────────────┐
                         │      DRIVEN ADAPTERS        │
                         │  (Repositories, External    │
                         │   APIs, Message Publishers) │
                         └──────────────┬──────────────┘
                                        │
                         ┌──────────────▼──────────────┐
                         │     SECONDARY ACTORS        │
                         │  (Database, External APIs,  │
                         │   Message Queues)           │
                         └─────────────────────────────┘
```

**Core Rule:** Application Core defines Ports. Adapters implement or use them.

### Key Concepts

| Concept | Description | Location |
|---------|-------------|----------|
| **Port** | Interface defining how to interact with the core | Application/Domain |
| **Driving Port** | Input interface (how to use the application) | Application layer |
| **Driven Port** | Output interface (what the application needs) | Application/Domain |
| **Driving Adapter** | Implements input mechanism (HTTP, CLI) | Infrastructure |
| **Driven Adapter** | Implements external dependencies | Infrastructure |
| **Application Core** | Business logic, isolated from I/O | Domain + Application |

## Quick Checklists

### Driving Port Checklist

- [ ] Interface in Application layer
- [ ] Defines use case boundary
- [ ] Uses domain/application types
- [ ] No framework types
- [ ] Single responsibility

### Driven Port Checklist

- [ ] Interface in Application/Domain layer
- [ ] Abstracts external dependency
- [ ] Uses domain types for return values
- [ ] No implementation details in signature
- [ ] Can have multiple adapters

### Driving Adapter Checklist

- [ ] Implements/calls driving port
- [ ] Converts external format to domain format
- [ ] No business logic
- [ ] Framework code contained here
- [ ] One adapter per delivery mechanism

### Driven Adapter Checklist

- [ ] Implements driven port interface
- [ ] Converts domain format to external format
- [ ] No business logic
- [ ] Handles external errors
- [ ] Easily replaceable

## Common Violations Quick Reference

| Violation | Where to Look | Severity |
|-----------|---------------|----------|
| Core depends on adapter | Domain importing Infrastructure | Critical |
| Missing port abstraction | Direct external service call | Critical |
| Business logic in adapter | if/switch in adapter | Critical |
| Framework in core | Symfony/Laravel in Domain | Warning |
| Port with implementation details | Interface using DB types | Warning |
| Adapter without port | Controller calling repository directly | Warning |

## PHP 8.5 Hexagonal Patterns

### Driving Port (Use Case Interface)

```php
<?php

declare(strict_types=1);

namespace Application\Order\Port\Input;

use Application\Order\DTO\CreateOrderRequest;
use Application\Order\DTO\CreateOrderResponse;

interface CreateOrderUseCaseInterface
{
    public function execute(CreateOrderRequest $request): CreateOrderResponse;
}
```

### Driven Port (Repository Interface)

```php
<?php

declare(strict_types=1);

namespace Domain\Order\Port\Output;

use Domain\Order\Entity\Order;
use Domain\Order\ValueObject\OrderId;

interface OrderRepositoryInterface
{
    public function findById(OrderId $id): ?Order;
    public function save(Order $order): void;
    public function nextIdentity(): OrderId;
}
```

### Driving Adapter (HTTP Controller)

```php
<?php

declare(strict_types=1);

namespace Infrastructure\Http\Controller;

use Application\Order\Port\Input\CreateOrderUseCaseInterface;
use Application\Order\DTO\CreateOrderRequest;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;

final readonly class CreateOrderController
{
    public function __construct(
        private CreateOrderUseCaseInterface $createOrder
    ) {}

    public function __invoke(Request $request): JsonResponse
    {
        $dto = CreateOrderRequest::fromArray($request->toArray());

        $response = $this->createOrder->execute($dto);

        return new JsonResponse($response->toArray(), 201);
    }
}
```

### Driven Adapter (Repository Implementation)

```php
<?php

declare(strict_types=1);

namespace Infrastructure\Persistence\Doctrine;

use Domain\Order\Entity\Order;
use Domain\Order\Port\Output\OrderRepositoryInterface;
use Domain\Order\ValueObject\OrderId;
use Doctrine\ORM\EntityManagerInterface;

final readonly class DoctrineOrderRepository implements OrderRepositoryInterface
{
    public function __construct(
        private EntityManagerInterface $em
    ) {}

    public function findById(OrderId $id): ?Order
    {
        return $this->em->find(Order::class, $id->value);
    }

    public function save(Order $order): void
    {
        $this->em->persist($order);
        $this->em->flush();
    }

    public function nextIdentity(): OrderId
    {
        return OrderId::generate();
    }
}
```

## References

For detailed information, load these reference files:

- `references/ports-patterns.md` — Driving and Driven Port patterns
- `references/adapters-patterns.md` — Adapter implementation patterns
- `references/testing-patterns.md` — Testing strategies for hexagonal architecture
- `references/antipatterns.md` — Common violations with detection patterns
