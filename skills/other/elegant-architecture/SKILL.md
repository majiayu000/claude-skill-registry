---
name: elegant-architecture
description: Guides clean architecture design with strict 200-line file limits. Use when starting new features, refactoring large files, or planning module structure. Enforces modular design and real testing.
---
# Elegant Architecture

## Core Principles

- **200-line limit** — No file exceeds 200 lines of code
- **Split when exceeded** — Convert to folder or multiple files
- **Plan first, code later** — Design architecture before implementation
- **Single responsibility** — Each module does one thing well
- **Real tests only** — No mocks, test actual behavior

## Execution Flow

### 1. Analyze Requirements

```markdown
Before writing any code:
- List all features/functionalities needed
- Estimate code volume for each module
- Identify shared components
- Map dependencies between modules
```

### 2. Design File Structure

```markdown
When estimated lines > 200:
- Convert file to folder with index
- Split by sub-functionality
- Extract shared utilities

Example transformation:
```

```
# Before (user.ts - 400+ lines)
user.ts

# After (user/ folder)
user/
├── index.ts        # Public exports
├── types.ts        # Interfaces, types
├── validation.ts   # Input validation
├── repository.ts   # Data access
└── service.ts      # Business logic
```

### 3. Define Interfaces First

```typescript
// Define contracts before implementation
interface UserService {
  create(input: CreateUserInput): Promise<User>;
  findById(id: string): Promise<User | null>;
  update(id: string, input: UpdateUserInput): Promise<User>;
  delete(id: string): Promise<void>;
}

interface UserRepository {
  save(user: User): Promise<User>;
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  delete(id: string): Promise<void>;
}
```

### 4. Implement Incrementally

```markdown
For each module:
1. Create type definitions
2. Implement core logic
3. Add error handling
4. Write tests
5. Verify line count < 200
```

### 5. Test Without Mocks

```typescript
// ❌ Avoid: Mock everything
const mockRepo = jest.fn();
const service = new UserService(mockRepo);

// ✅ Prefer: Real implementations
const testDb = createTestDatabase();
const repo = new UserRepository(testDb);
const service = new UserService(repo);

// Test actual behavior
const user = await service.create({ email: 'test@example.com' });
const found = await service.findById(user.id);
expect(found).toEqual(user);
```

## Design Patterns

### Modular Design

```
src/
├── modules/
│   ├── auth/
│   │   ├── index.ts
│   │   ├── types.ts
│   │   ├── service.ts
│   │   └── middleware.ts
│   ├── user/
│   │   ├── index.ts
│   │   ├── types.ts
│   │   ├── service.ts
│   │   └── repository.ts
│   └── order/
│       ├── index.ts
│       ├── types.ts
│       ├── service.ts
│       └── repository.ts
├── shared/
│   ├── database/
│   ├── errors/
│   └── utils/
└── index.ts
```

### Dependency Injection

```typescript
// Decouple components via constructor injection
class OrderService {
  constructor(
    private readonly orderRepo: OrderRepository,
    private readonly userService: UserService,
    private readonly paymentGateway: PaymentGateway
  ) {}

  async createOrder(userId: string, items: OrderItem[]): Promise<Order> {
    const user = await this.userService.findById(userId);
    if (!user) throw new NotFoundError('User', userId);

    const order = Order.create(user, items);
    await this.paymentGateway.charge(user, order.total);
    return this.orderRepo.save(order);
  }
}

// Wire up in composition root
const orderService = new OrderService(
  new PostgresOrderRepository(db),
  new UserService(userRepo),
  new StripePaymentGateway(stripeClient)
);
```

### Factory Pattern

```typescript
// Complex object creation
class NotificationFactory {
  create(type: NotificationType, data: NotificationData): Notification {
    switch (type) {
      case 'email':
        return new EmailNotification(data, this.emailClient);
      case 'sms':
        return new SmsNotification(data, this.smsClient);
      case 'push':
        return new PushNotification(data, this.pushClient);
      default:
        throw new Error(`Unknown notification type: ${type}`);
    }
  }
}
```

### Strategy Pattern

```typescript
// Replaceable algorithms
interface PricingStrategy {
  calculate(order: Order): Money;
}

class StandardPricing implements PricingStrategy {
  calculate(order: Order): Money {
    return order.items.reduce((sum, item) => sum.add(item.price), Money.zero());
  }
}

class DiscountPricing implements PricingStrategy {
  constructor(private readonly discount: Percentage) {}

  calculate(order: Order): Money {
    const standard = new StandardPricing().calculate(order);
    return standard.subtract(standard.multiply(this.discount));
  }
}

class OrderProcessor {
  constructor(private pricing: PricingStrategy) {}

  setPricing(strategy: PricingStrategy) {
    this.pricing = strategy;
  }

  process(order: Order): ProcessedOrder {
    const total = this.pricing.calculate(order);
    return { ...order, total };
  }
}
```

## File Splitting Guidelines

### When to Split

| Indicator | Action |
|-----------|--------|
| File > 200 lines | Split immediately |
| File > 150 lines | Plan split |
| 3+ distinct responsibilities | Split by responsibility |
| Shared types growing | Extract to types.ts |
| Utility functions accumulating | Extract to utils.ts |

### How to Split

```markdown
1. Identify logical boundaries
2. Create folder with same name as file
3. Move related code to separate files
4. Create index.ts for public exports
5. Update imports in dependent files
```

### Naming Conventions

```
module/
├── index.ts          # Public API exports
├── types.ts          # Interfaces, types, enums
├── constants.ts      # Configuration, magic values
├── utils.ts          # Helper functions
├── service.ts        # Business logic
├── repository.ts     # Data access
├── validation.ts     # Input validation
└── errors.ts         # Custom errors
```

## Architecture Checklist

```markdown
## Pre-Implementation
- [ ] Requirements analyzed
- [ ] Code volume estimated
- [ ] File structure designed
- [ ] Interfaces defined
- [ ] Dependencies mapped

## Implementation
- [ ] Each file < 200 lines
- [ ] Single responsibility per module
- [ ] Dependencies injected
- [ ] Error handling complete
- [ ] No hardcoded values

## Testing
- [ ] Real implementations used
- [ ] No mocks for core logic
- [ ] Edge cases covered
- [ ] Integration tests exist

## Review
- [ ] Architecture documented
- [ ] Public APIs clear
- [ ] No circular dependencies
- [ ] Easy to extend
```

## Anti-Patterns to Avoid

```markdown
❌ God files (500+ lines doing everything)
❌ Mocking everything in tests
❌ Coding before planning
❌ Tight coupling between modules
❌ Hardcoded configuration
❌ Circular dependencies
❌ Unclear module boundaries
```

## Key Principles

1. **Measure twice, cut once** — Plan architecture before coding
2. **Small is beautiful** — 200 lines max, no exceptions
3. **Test reality** — Real tests catch real bugs
4. **Inject dependencies** — Loose coupling, easy testing
5. **Single purpose** — One reason to change per module
