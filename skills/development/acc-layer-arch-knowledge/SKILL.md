---
name: acc-layer-arch-knowledge
description: Layered Architecture knowledge base. Provides patterns, antipatterns, and PHP-specific guidelines for traditional N-tier/Layered Architecture audits.
---

# Layered Architecture Knowledge Base

Quick reference for Layered (N-Tier) Architecture patterns and PHP implementation guidelines.

## Core Principles

### Layered Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
│         (Controllers, Views, API Endpoints, CLI)                │
│                                                                 │
│  Responsibilities:                                              │
│  - Handle user input                                            │
│  - Display output                                               │
│  - Validate input format                                        │
│  - Route requests                                               │
└───────────────────────────┬─────────────────────────────────────┘
                            │ calls
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                           │
│           (Services, Use Cases, DTOs, Facades)                  │
│                                                                 │
│  Responsibilities:                                              │
│  - Orchestrate business operations                              │
│  - Transaction management                                       │
│  - Coordinate domain objects                                    │
│  - Map between layers                                           │
└───────────────────────────┬─────────────────────────────────────┘
                            │ calls
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                               │
│      (Entities, Value Objects, Domain Services, Rules)          │
│                                                                 │
│  Responsibilities:                                              │
│  - Business logic                                               │
│  - Business rules and invariants                                │
│  - Domain events                                                │
│  - Core algorithms                                              │
└───────────────────────────┬─────────────────────────────────────┘
                            │ calls
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE LAYER                          │
│       (Repositories, External APIs, Database, Cache)            │
│                                                                 │
│  Responsibilities:                                              │
│  - Data persistence                                             │
│  - External service integration                                 │
│  - Technical infrastructure                                     │
│  - Framework-specific code                                      │
└─────────────────────────────────────────────────────────────────┘
```

**Core Rule:** Each layer only communicates with the layer directly below it.

### Layer Communication Rules

| From Layer | Can Call | Cannot Call |
|------------|----------|-------------|
| Presentation | Application | Domain, Infrastructure |
| Application | Domain, Infrastructure | Presentation |
| Domain | Infrastructure (via interfaces) | Presentation, Application |
| Infrastructure | — | All upper layers |

## Quick Checklists

### Presentation Layer Checklist

- [ ] Controllers are thin
- [ ] No business logic
- [ ] Input validation only
- [ ] Calls application services
- [ ] Transforms output for display
- [ ] Framework code contained here

### Application Layer Checklist

- [ ] Orchestrates operations
- [ ] Transaction boundaries
- [ ] No direct DB access
- [ ] Uses domain objects
- [ ] DTOs for input/output
- [ ] No framework dependencies

### Domain Layer Checklist

- [ ] Pure business logic
- [ ] No infrastructure code
- [ ] Rich entity behavior
- [ ] Value objects for concepts
- [ ] Business rules encapsulated
- [ ] Repository interfaces only

### Infrastructure Layer Checklist

- [ ] Implements domain interfaces
- [ ] Database operations
- [ ] External API calls
- [ ] Caching logic
- [ ] No business logic

## Common Violations Quick Reference

| Violation | Where to Look | Severity |
|-----------|---------------|----------|
| Skipping layers | Controller calling DB | Critical |
| Upward dependency | Domain using Application | Critical |
| Business in Controller | if/switch in controllers | Warning |
| Anemic services | Service = simple delegation | Warning |
| Fat repository | Logic in repository | Warning |

## PHP 8.5 Layered Architecture Patterns

### Presentation Layer (Controller)

```php
<?php

declare(strict_types=1);

namespace Presentation\Api\Order;

use Application\Order\Service\OrderService;
use Application\Order\DTO\CreateOrderDTO;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;

final readonly class OrderController
{
    public function __construct(
        private OrderService $orderService
    ) {}

    public function create(Request $request): JsonResponse
    {
        $dto = CreateOrderDTO::fromRequest($request);

        $result = $this->orderService->createOrder($dto);

        return new JsonResponse($result->toArray(), 201);
    }

    public function show(string $id): JsonResponse
    {
        $order = $this->orderService->getOrder($id);

        return new JsonResponse($order->toArray());
    }
}
```

### Application Layer (Service)

```php
<?php

declare(strict_types=1);

namespace Application\Order\Service;

use Application\Order\DTO\CreateOrderDTO;
use Application\Order\DTO\OrderDTO;
use Domain\Order\Entity\Order;
use Domain\Order\Repository\OrderRepositoryInterface;
use Domain\Order\ValueObject\OrderId;

final readonly class OrderService
{
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
        private TransactionManagerInterface $transactionManager
    ) {}

    public function createOrder(CreateOrderDTO $dto): OrderDTO
    {
        return $this->transactionManager->transactional(function () use ($dto) {
            $order = Order::create(
                id: $this->orderRepository->nextIdentity(),
                customerId: $dto->customerId,
                lines: $dto->lines
            );

            $this->orderRepository->save($order);

            return OrderDTO::fromEntity($order);
        });
    }

    public function getOrder(string $id): OrderDTO
    {
        $order = $this->orderRepository->findById(new OrderId($id));

        if ($order === null) {
            throw new OrderNotFoundException($id);
        }

        return OrderDTO::fromEntity($order);
    }
}
```

### Domain Layer (Entity)

```php
<?php

declare(strict_types=1);

namespace Domain\Order\Entity;

use Domain\Order\ValueObject\OrderId;
use Domain\Order\ValueObject\CustomerId;
use Domain\Order\ValueObject\Money;
use Domain\Order\Enum\OrderStatus;

final class Order
{
    private OrderStatus $status;
    private array $lines = [];

    public function __construct(
        private readonly OrderId $id,
        private readonly CustomerId $customerId
    ) {
        $this->status = OrderStatus::Draft;
    }

    public static function create(OrderId $id, CustomerId $customerId, array $lines): self
    {
        $order = new self($id, $customerId);

        foreach ($lines as $line) {
            $order->addLine($line);
        }

        return $order;
    }

    public function confirm(): void
    {
        if (!$this->canBeConfirmed()) {
            throw new CannotConfirmOrderException();
        }

        $this->status = OrderStatus::Confirmed;
    }

    public function total(): Money
    {
        return array_reduce(
            $this->lines,
            fn (Money $carry, OrderLine $line) => $carry->add($line->total()),
            Money::zero('USD')
        );
    }

    private function canBeConfirmed(): bool
    {
        return $this->status === OrderStatus::Draft && !empty($this->lines);
    }
}
```

### Infrastructure Layer (Repository)

```php
<?php

declare(strict_types=1);

namespace Infrastructure\Persistence\Order;

use Domain\Order\Entity\Order;
use Domain\Order\Repository\OrderRepositoryInterface;
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

- `references/layer-responsibilities.md` — Detailed layer responsibilities
- `references/layer-communication.md` — Inter-layer communication patterns
- `references/dto-patterns.md` — Data Transfer Object patterns
- `references/antipatterns.md` — Common violations with detection patterns
