---
name: code-patterns
description: Common code patterns and best practices reference for quick lookup
---

# Code Patterns Reference

Quick reference for common patterns. Use these as starting points, not rigid templates.

## Creational Patterns

### Factory
```typescript
// When: Creating objects without specifying exact class
interface Product { use(): void }

class ConcreteProductA implements Product {
  use() { console.log('Using A') }
}

class ProductFactory {
  static create(type: string): Product {
    const products = { a: ConcreteProductA };
    return new products[type]();
  }
}
```

### Builder
```typescript
// When: Complex object construction with many optional params
class QueryBuilder {
  private query = { select: '*', from: '', where: [] };

  select(fields: string) { this.query.select = fields; return this; }
  from(table: string) { this.query.from = table; return this; }
  where(condition: string) { this.query.where.push(condition); return this; }
  build() { return this.query; }
}

// Usage
const query = new QueryBuilder()
  .select('name, email')
  .from('users')
  .where('active = true')
  .build();
```

### Singleton
```typescript
// When: Exactly one instance needed (use sparingly!)
class Database {
  private static instance: Database;
  private constructor() {}

  static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }
}
```

## Structural Patterns

### Adapter
```typescript
// When: Making incompatible interfaces work together
interface ModernLogger { log(msg: string): void }

class LegacyLogger {
  writeLog(message: string, level: number) { /* ... */ }
}

class LoggerAdapter implements ModernLogger {
  constructor(private legacy: LegacyLogger) {}
  log(msg: string) { this.legacy.writeLog(msg, 1); }
}
```

### Decorator
```typescript
// When: Adding behavior without modifying original
interface Coffee { cost(): number; description(): string }

class SimpleCoffee implements Coffee {
  cost() { return 5; }
  description() { return 'Coffee'; }
}

class MilkDecorator implements Coffee {
  constructor(private coffee: Coffee) {}
  cost() { return this.coffee.cost() + 2; }
  description() { return this.coffee.description() + ' + Milk'; }
}
```

## Behavioral Patterns

### Strategy
```typescript
// When: Algorithm should be selectable at runtime
interface PaymentStrategy {
  pay(amount: number): void;
}

class CreditCardPayment implements PaymentStrategy {
  pay(amount: number) { console.log(`Paid ${amount} via credit card`); }
}

class PayPalPayment implements PaymentStrategy {
  pay(amount: number) { console.log(`Paid ${amount} via PayPal`); }
}

class Checkout {
  constructor(private strategy: PaymentStrategy) {}
  process(amount: number) { this.strategy.pay(amount); }
}
```

### Observer
```typescript
// When: Objects need to be notified of state changes
type Listener<T> = (data: T) => void;

class EventEmitter<T> {
  private listeners: Listener<T>[] = [];

  subscribe(listener: Listener<T>) {
    this.listeners.push(listener);
    return () => this.listeners = this.listeners.filter(l => l !== listener);
  }

  emit(data: T) {
    this.listeners.forEach(l => l(data));
  }
}
```

## Error Handling Patterns

### Result Type
```typescript
// When: Errors are expected, not exceptional
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return { ok: false, error: 'Division by zero' };
  return { ok: true, value: a / b };
}

const result = divide(10, 2);
if (result.ok) {
  console.log(result.value); // 5
} else {
  console.error(result.error);
}
```

### Retry with Backoff
```typescript
// When: Transient failures are expected
async function retry<T>(
  fn: () => Promise<T>,
  attempts = 3,
  delay = 1000
): Promise<T> {
  for (let i = 0; i < attempts; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === attempts - 1) throw e;
      await new Promise(r => setTimeout(r, delay * Math.pow(2, i)));
    }
  }
  throw new Error('Unreachable');
}
```

## Async Patterns

### Promise Queue
```typescript
// When: Limiting concurrent async operations
class PromiseQueue {
  private queue: (() => Promise<any>)[] = [];
  private running = 0;

  constructor(private concurrency: number) {}

  add<T>(fn: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.queue.push(async () => {
        try { resolve(await fn()); }
        catch (e) { reject(e); }
      });
      this.process();
    });
  }

  private async process() {
    if (this.running >= this.concurrency || !this.queue.length) return;
    this.running++;
    await this.queue.shift()!();
    this.running--;
    this.process();
  }
}
```

### Debounce
```typescript
// When: Limiting rapid-fire function calls
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}
```

## Data Patterns

### Repository
```typescript
// When: Abstracting data access
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<void>;
}

class UserRepository implements Repository<User> {
  constructor(private db: Database) {}

  async findById(id: string) {
    return this.db.query('SELECT * FROM users WHERE id = ?', [id]);
  }
  // ... other methods
}
```

### Unit of Work
```typescript
// When: Coordinating writes across multiple repositories
class UnitOfWork {
  private operations: (() => Promise<void>)[] = [];

  register(operation: () => Promise<void>) {
    this.operations.push(operation);
  }

  async commit() {
    await this.db.beginTransaction();
    try {
      for (const op of this.operations) await op();
      await this.db.commit();
    } catch (e) {
      await this.db.rollback();
      throw e;
    }
  }
}
```

## When to Use Each

| Problem | Pattern |
|---------|---------|
| Complex object creation | Builder |
| Multiple similar objects | Factory |
| Global state (careful!) | Singleton |
| Incompatible interfaces | Adapter |
| Adding features dynamically | Decorator |
| Swappable algorithms | Strategy |
| Event-based communication | Observer |
| Expected failures | Result Type |
| Transient failures | Retry |
| Rate limiting | Debounce/Throttle |
| Data access abstraction | Repository |
| Transactional consistency | Unit of Work |
