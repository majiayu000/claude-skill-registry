---
name: clean-architecture
description: Provides implementation patterns for Clean Architecture, Domain-Driven Design (DDD), and Hexagonal Architecture (Ports & Adapters) in NestJS/TypeScript applications. Use when structuring complex backend systems, designing domain layers with entities/value objects/aggregates, implementing ports and adapters, creating use cases, or refactoring from anemic models to rich domain models with dependency inversion.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Clean Architecture, DDD & Hexagonal Architecture for NestJS

## Overview

This skill provides comprehensive guidance for implementing Clean Architecture, Domain-Driven Design (DDD), and Hexagonal Architecture patterns in NestJS/TypeScript applications. It covers the architectural layers, tactical patterns, and practical implementation examples for building maintainable, testable, and loosely-coupled backend systems.

## When to Use

- Architecting complex NestJS applications with long-term maintainability
- Refactoring from tightly-coupled MVC to layered architecture
- Implementing rich domain models with business logic encapsulation
- Designing testable systems with swappable infrastructure
- Creating microservices with clear bounded contexts
- Separating business rules from framework code
- Implementing event-driven architectures with domain events

## Instructions

### 1. Understand the Architectural Layers

Clean Architecture organizes code into concentric layers where dependencies flow inward. Inner layers have no knowledge of outer layers:

```
+-------------------------------------+
|  Infrastructure (Frameworks, DB)    |  Outer layer - volatile
+-------------------------------------+
|  Adapters (Controllers, Repositories)|  Interface adapters
+-------------------------------------+
|  Application (Use Cases)            |  Business rules
+-------------------------------------+
|  Domain (Entities, Value Objects)   |  Core - most stable
+-------------------------------------+
```

The Hexagonal Architecture (Ports & Adapters) pattern complements this:
- **Ports**: Interfaces defining what the application needs
- **Adapters**: Concrete implementations of ports
- **Domain Core**: Pure business logic with zero dependencies

### 2. Learn DDD Tactical Patterns

Apply these patterns in your domain layer:
- **Entities**: Objects with identity and lifecycle
- **Value Objects**: Immutable, defined by attributes
- **Aggregates**: Consistency boundaries with aggregate roots
- **Domain Events**: Capture state changes
- **Repositories**: Abstract data access for aggregates

### 3. Organize Your Project Structure

Structure your NestJS project following Clean Architecture principles:

```
src/
+-- domain/                    # Inner layer - no external deps
|   +-- entities/              # Domain entities
|   +-- value-objects/         # Immutable value objects
|   +-- aggregates/            # Aggregate roots
|   +-- events/                # Domain events
|   +-- repositories/          # Repository interfaces (ports)
|   +-- services/              # Domain services
+-- application/               # Use cases - orchestration
|   +-- use-cases/             # Individual use cases
|   +-- ports/                 # Input/output ports
|   +-- dto/                   # Application DTOs
|   +-- services/              # Application services
+-- infrastructure/            # External concerns
|   +-- database/              # ORM config, migrations
|   +-- http/                  # HTTP clients
|   +-- messaging/             # Message queues
+-- adapters/                  # Interface adapters
    +-- http/                  # Controllers, presenters
    +-- persistence/           # Repository implementations
    +-- external/              # External service adapters
```

### 4. Implement the Domain Layer

Create pure domain objects with no external dependencies:

1. **Value Objects**: Immutable objects validated at construction
2. **Entities**: Objects with identity containing business logic
3. **Aggregates**: Consistency boundaries protecting invariants
4. **Repository Ports**: Interfaces defining data access contracts

### 5. Implement the Application Layer

Create use cases that orchestrate business logic:

1. Define input/output DTOs for each use case
2. Inject repository ports via constructor
3. Implement business workflows in the `execute` method
4. Keep use cases focused on a single responsibility

### 6. Implement Adapters

Create concrete implementations of ports:

1. **Persistence Adapters**: Map domain objects to/from ORM entities
2. **HTTP Adapters**: Controllers that transform requests to use case inputs
3. **External Service Adapters**: Integrate with third-party services

### 7. Configure Dependency Injection

Wire everything together in NestJS modules:

1. Register use cases as providers
2. Provide repository implementations using interface tokens
3. Import required infrastructure modules (TypeORM, etc.)

### 8. Apply Best Practices

Follow these principles throughout implementation:

1. **Dependency Rule**: Dependencies only point inward. Domain knows nothing about NestJS, TypeORM, or HTTP.
2. **Rich Domain Models**: Put business logic in entities, not services. Avoid anemic domain models.
3. **Immutability**: Value objects must be immutable. Create new instances instead of modifying.
4. **Interface Segregation**: Keep repository interfaces small and focused.
5. **Constructor Injection**: Use NestJS DI in outer layers only. Domain entities use plain constructors.
6. **Validation**: Validate at boundaries (DTOs) and enforce invariants in domain.
7. **Testing**: Domain layer tests require no NestJS testing module - pure unit tests.
8. **Transactions**: Keep transactions in the application layer, not domain.

## Examples

### Example 1: Value Objects

Value objects are immutable and validated at construction:

```typescript
// domain/value-objects/email.vo.ts
export class Email {
  private constructor(private readonly value: string) {}

  static create(email: string): Email {
    if (!this.isValid(email)) {
      throw new Error('Invalid email format');
    }
    return new Email(email.toLowerCase().trim());
  }

  private static isValid(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  getValue(): string {
    return this.value;
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }
}

// domain/value-objects/money.vo.ts
export class Money {
  private constructor(
    private readonly amount: number,
    private readonly currency: string,
  ) {}

  static create(amount: number, currency: string): Money {
    if (amount < 0) throw new Error('Amount cannot be negative');
    return new Money(amount, currency);
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error('Cannot add different currencies');
    }
    return new Money(this.amount + other.amount, this.currency);
  }

  getAmount(): number { return this.amount; }
  getCurrency(): string { return this.currency; }
}
```

### Example 2: Entity with Business Logic

Entities contain identity and encapsulate business rules:

```typescript
// domain/entities/order-item.entity.ts
import { Money } from '../value-objects/money.vo';

export class OrderItem {
  constructor(
    private readonly productId: string,
    private readonly quantity: number,
    private readonly unitPrice: Money,
  ) {
    if (quantity <= 0) throw new Error('Quantity must be positive');
  }

  getSubtotal(): Money {
    return Money.create(
      this.unitPrice.getAmount() * this.quantity,
      this.unitPrice.getCurrency(),
    );
  }
}
```

### Example 3: Aggregate Root with Domain Events

Aggregate roots protect invariants and emit domain events:

```typescript
// domain/aggregates/order.aggregate.ts
import { AggregateRoot } from '@nestjs/cqrs';
import { OrderItem } from '../entities/order-item.entity';
import { Money } from '../value-objects/money.vo';
import { OrderCreatedEvent } from '../events/order-created.event';

export enum OrderStatus {
  PENDING = 'PENDING',
  CONFIRMED = 'CONFIRMED',
  SHIPPED = 'SHIPPED',
  CANCELLED = 'CANCELLED',
}

export class Order extends AggregateRoot {
  private items: OrderItem[] = [];
  private status: OrderStatus = OrderStatus.PENDING;

  constructor(
    private readonly id: string,
    private readonly customerId: string,
  ) {
    super();
  }

  addItem(item: OrderItem): void {
    if (this.status !== OrderStatus.PENDING) {
      throw new Error('Cannot modify confirmed order');
    }
    this.items.push(item);
  }

  getTotal(): Money {
    return this.items.reduce(
      (sum, item) => sum.add(item.getSubtotal()),
      Money.create(0, 'USD'),
    );
  }

  confirm(): void {
    if (this.items.length === 0) {
      throw new Error('Cannot confirm empty order');
    }
    this.status = OrderStatus.CONFIRMED;
    this.apply(new OrderCreatedEvent(this.id, this.customerId));
  }

  getStatus(): OrderStatus {
    return this.status;
  }
}
```

### Example 4: Repository Port (Interface)

Define repository contracts in the domain layer:

```typescript
// domain/repositories/order-repository.port.ts
import { Order } from '../aggregates/order.aggregate';

export interface OrderRepositoryPort {
  findById(id: string): Promise<Order | null>;
  findByCustomerId(customerId: string): Promise<Order[]>;
  save(order: Order): Promise<void>;
  delete(id: string): Promise<void>;
}

// Token for dependency injection
export const ORDER_REPOSITORY = Symbol('ORDER_REPOSITORY');
```

### Example 5: Use Case (Application Layer)

Use cases orchestrate business logic and infrastructure:

```typescript
// application/use-cases/create-order.use-case.ts
import { Injectable, Inject } from '@nestjs/common';
import { Order } from '../../domain/aggregates/order.aggregate';
import { OrderItem } from '../../domain/entities/order-item.entity';
import { Money } from '../../domain/value-objects/money.vo';
import { OrderRepositoryPort, ORDER_REPOSITORY } from '../../domain/repositories/order-repository.port';

export interface CreateOrderInput {
  customerId: string;
  items: Array<{
    productId: string;
    quantity: number;
    unitPrice: number;
    currency: string;
  }>;
}

export interface CreateOrderOutput {
  orderId: string;
  total: number;
  currency: string;
}

@Injectable()
export class CreateOrderUseCase {
  constructor(
    @Inject(ORDER_REPOSITORY)
    private readonly orderRepository: OrderRepositoryPort,
  ) {}

  async execute(input: CreateOrderInput): Promise<CreateOrderOutput> {
    const orderId = crypto.randomUUID();
    const order = new Order(orderId, input.customerId);

    for (const item of input.items) {
      const money = Money.create(item.unitPrice, item.currency);
      order.addItem(new OrderItem(item.productId, item.quantity, money));
    }

    order.confirm();
    await this.orderRepository.save(order);

    const total = order.getTotal();
    return {
      orderId,
      total: total.getAmount(),
      currency: total.getCurrency(),
    };
  }
}
```

### Example 6: Repository Adapter (Infrastructure)

Implement repository interfaces in the infrastructure layer:

```typescript
// adapters/persistence/order.repository.ts
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { OrderRepositoryPort } from '../../domain/repositories/order-repository.port';
import { Order } from '../../domain/aggregates/order.aggregate';
import { OrderEntity } from '../../infrastructure/database/entities/order.entity';

@Injectable()
export class OrderRepository implements OrderRepositoryPort {
  constructor(
    @InjectRepository(OrderEntity)
    private readonly repository: Repository<OrderEntity>,
  ) {}

  async findById(id: string): Promise<Order | null> {
    const entity = await this.repository.findOne({
      where: { id },
      relations: ['items'],
    });
    return entity ? this.toDomain(entity) : null;
  }

  async findByCustomerId(customerId: string): Promise<Order[]> {
    const entities = await this.repository.find({
      where: { customerId },
      relations: ['items'],
    });
    return entities.map(e => this.toDomain(e));
  }

  async save(order: Order): Promise<void> {
    const entity = this.toEntity(order);
    await this.repository.save(entity);
  }

  async delete(id: string): Promise<void> {
    await this.repository.delete(id);
  }

  private toDomain(entity: OrderEntity): Order {
    // Map ORM entity to domain aggregate
    const order = new Order(entity.id, entity.customerId);
    // ... populate items, status
    return order;
  }

  private toEntity(order: Order): OrderEntity {
    // Map domain aggregate to ORM entity
    const entity = new OrderEntity();
    // ... mapping logic
    return entity;
  }
}
```

### Example 7: Controller Adapter

Controllers adapt HTTP requests to use case inputs:

```typescript
// adapters/http/order.controller.ts
import { Controller, Post, Body, Get, Param } from '@nestjs/common';
import { CreateOrderUseCase, CreateOrderInput } from '../../application/use-cases/create-order.use-case';
import { IsString, IsArray, ValidateNested, IsNumber } from 'class-validator';
import { Type } from 'class-transformer';

class OrderItemDto {
  @IsString()
  productId: string;

  @IsNumber()
  quantity: number;

  @IsNumber()
  unitPrice: number;

  @IsString()
  currency: string;
}

class CreateOrderDto implements CreateOrderInput {
  @IsString()
  customerId: string;

  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => OrderItemDto)
  items: OrderItemDto[];
}

@Controller('orders')
export class OrderController {
  constructor(private readonly createOrderUseCase: CreateOrderUseCase) {}

  @Post()
  async create(@Body() dto: CreateOrderDto) {
    return this.createOrderUseCase.execute(dto);
  }
}
```

### Example 8: Module Configuration

Wire dependencies together in NestJS modules:

```typescript
// orders.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { OrderController } from './adapters/http/order.controller';
import { CreateOrderUseCase } from './application/use-cases/create-order.use-case';
import { OrderRepository } from './adapters/persistence/order.repository';
import { ORDER_REPOSITORY } from './domain/repositories/order-repository.port';
import { OrderEntity } from './infrastructure/database/entities/order.entity';

@Module({
  imports: [TypeOrmModule.forFeature([OrderEntity])],
  controllers: [OrderController],
  providers: [
    CreateOrderUseCase,
    {
      provide: ORDER_REPOSITORY,
      useClass: OrderRepository,
    },
  ],
})
export class OrdersModule {}
```

## Best Practices

1. **Dependency Rule**: Dependencies only point inward - domain knows nothing about NestJS, TypeORM, or HTTP
2. **Rich Domain Models**: Put business logic in entities, not services - avoid anemic domain models
3. **Immutability**: Value objects must be immutable - use private constructors with static factory methods
4. **Interface Segregation**: Keep repository interfaces small and focused - one repository per aggregate
5. **Constructor Injection**: Use NestJS DI in outer layers only - domain entities use plain constructors
6. **Validation at Boundaries**: Validate DTOs at API boundary and enforce invariants in domain entities
7. **Pure Domain Tests**: Domain layer tests require no NestJS testing module - fast pure unit tests
8. **Transactions in Application**: Keep transaction management in application layer, not domain
9. **Symbol Tokens**: Use Symbol() for DI tokens to avoid string coupling in NestJS modules
10. **Aggregate Roots**: Protect invariants through aggregate roots - access entities only through aggregates

## Constraints and Warnings

### Architecture Constraints

- **Dependency Rule**: Never allow inner layers to depend on outer layers
- **Domain Purity**: Domain layer must have zero dependencies on frameworks (NestJS, TypeORM, etc.)
- **Interface Location**: Repository interfaces belong in the domain layer, implementations in adapters
- **Immutability**: Value objects must be immutable - no setters allowed

### Common Pitfalls to Avoid

- **Leaky Abstractions**: ORM entities leaking into domain layer
- **Anemic Domain**: Entities with only getters/setters, logic in services
- **Wrong Layer**: Framework decorators in domain entities
- **Missing Ports**: Direct dependency on concrete implementations instead of interfaces
- **Over-Engineering**: Clean Architecture for simple CRUD operations is unnecessary overhead

### Implementation Warnings

- **Mapping Overhead**: Repository adapters require mapping between domain and ORM entities
- **Learning Curve**: Team must understand DDD concepts before implementation
- **Boilerplate**: More files and interfaces compared to traditional layered architecture
- **Transaction Boundaries**: Transactions must be managed at the application layer, not domain

## References

- `references/typescript-clean-architecture.md` - TypeScript-specific patterns
- `references/nestjs-implementation.md` - NestJS integration details
