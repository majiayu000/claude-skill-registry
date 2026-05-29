---
name: System Boundaries
description: Defining clear boundaries between systems, services, and modules to manage complexity and enable independent evolution.
---

# System Boundaries

## Overview

System Boundaries define where one system ends and another begins, establishing clear interfaces, ownership, and responsibilities. Well-defined boundaries reduce coupling and enable teams to work independently.

**Core Principle**: "Strong boundaries enable weak coupling. Define interfaces, not implementations."

---

## 1. Why System Boundaries Matter

- **Reduces Coupling**: Systems can evolve independently
- **Enables Scaling**: Teams can own and scale their systems
- **Clarifies Ownership**: Clear who is responsible for what
- **Improves Testability**: Easier to test in isolation
- **Facilitates Understanding**: Simpler mental models

---

## 2. Types of Boundaries

### Service Boundaries
```
┌─────────────────┐     ┌─────────────────┐
│  User Service   │────▶│  Order Service  │
│  (owns users)   │     │  (owns orders)  │
└─────────────────┘     └─────────────────┘
        │                        │
        ▼                        ▼
   Users Table              Orders Table
```

### Module Boundaries (within monolith)
```typescript
// src/modules/auth/
export interface AuthService {
  login(credentials: Credentials): Promise<Token>;
  verify(token: Token): Promise<User>;
}

// src/modules/orders/
import { AuthService } from '../auth';  // Uses interface, not implementation
```

### Data Boundaries
```
Each service owns its own database:
- User Service → users_db
- Order Service → orders_db
- Payment Service → payments_db

No cross-database queries allowed!
```

---

## 3. Bounded Contexts (DDD)

```markdown
## E-commerce System Boundaries

### Sales Context
- **Entities**: Product, Cart, Order
- **Language**: "Add to cart", "Checkout", "Purchase"
- **Owner**: Sales team

### Inventory Context
- **Entities**: Stock, Warehouse, SKU
- **Language**: "Restock", "Allocate", "Reserve"
- **Owner**: Operations team

### Shipping Context
- **Entities**: Shipment, Carrier, Tracking
- **Language**: "Ship", "Deliver", "Track"
- **Owner**: Logistics team

**Note**: "Product" means different things in each context!
- Sales: Product with price, description
- Inventory: Product with stock level, location
- Shipping: Product with weight, dimensions
```

---

## 4. Interface Definition

### REST API Boundary
```typescript
// Public API contract (boundary)
interface OrderAPI {
  POST /orders
  GET /orders/:id
  PUT /orders/:id/cancel
}

// Implementation details (hidden)
class OrderService {
  private database: Database;
  private paymentGateway: PaymentGateway;
  
  // Internal methods not exposed via API
  private validateInventory() { }
  private processPayment() { }
}
```

### Event-Driven Boundary
```typescript
// Published events (boundary)
interface OrderEvents {
  'order.created': { orderId: string; userId: string; total: number };
  'order.shipped': { orderId: string; trackingNumber: string };
}

// Other services subscribe to events, don't call directly
```

---

## 5. Ownership and Responsibilities

```markdown
## Service Ownership Matrix

| Service | Team | Owns Data | Provides | Consumes |
|---------|------|-----------|----------|----------|
| User Service | Identity Team | Users, Profiles | User CRUD, Auth | - |
| Order Service | Commerce Team | Orders, Line Items | Order Management | User Service (user validation) |
| Payment Service | Finance Team | Transactions | Payment Processing | Order Service (order details) |
| Notification Service | Platform Team | - | Email/SMS | All services (events) |
```

---

## 6. Anti-Corruption Layer

```typescript
// External API has different model than our domain
interface ExternalPaymentAPI {
  charge(amount_cents: number, card_token: string): ExternalResponse;
}

// Anti-corruption layer translates
class PaymentAdapter {
  constructor(private external: ExternalPaymentAPI) {}
  
  async processPayment(payment: Payment): Promise<PaymentResult> {
    // Translate our domain model to external API
    const response = await this.external.charge(
      payment.amount * 100,  // dollars to cents
      payment.cardToken
    );
    
    // Translate response back to our domain
    return {
      success: response.status === 'succeeded',
      transactionId: response.id
    };
  }
}
```

---

## 7. Boundary Crossing Patterns

### Synchronous (API Call)
```typescript
// Order Service calls User Service
const user = await userService.getUser(userId);
if (!user) throw new Error('User not found');
```

### Asynchronous (Events)
```typescript
// Order Service publishes event
eventBus.publish('order.created', { orderId, userId, total });

// Notification Service subscribes
eventBus.subscribe('order.created', async (event) => {
  await sendOrderConfirmationEmail(event.userId, event.orderId);
});
```

### Shared Database (Anti-pattern)
```typescript
// ❌ DON'T: Order Service directly queries users table
const user = await db.query('SELECT * FROM users WHERE id = ?', [userId]);

// ✅ DO: Call User Service API
const user = await userService.getUser(userId);
```

---

## 8. Boundary Violations

### Common Violations
```typescript
// ❌ Violation: Reaching into another service's database
await orderDb.query('SELECT * FROM users WHERE id = ?', [userId]);

// ❌ Violation: Exposing internal implementation
class OrderService {
  public database: Database;  // Leaking internals
}

// ❌ Violation: Tight coupling
class OrderService {
  constructor(private userService: UserServiceImpl) {}  // Depends on concrete class
}

// ✅ Correct: Use interface
class OrderService {
  constructor(private userService: IUserService) {}  // Depends on interface
}
```

---

## 9. Boundary Testing

```typescript
// Test boundary with mocks
describe('OrderService', () => {
  it('validates user exists before creating order', async () => {
    const mockUserService = {
      getUser: jest.fn().mockResolvedValue(null)
    };
    
    const orderService = new OrderService(mockUserService);
    
    await expect(
      orderService.createOrder({ userId: '123', items: [] })
    ).rejects.toThrow('User not found');
    
    expect(mockUserService.getUser).toHaveBeenCalledWith('123');
  });
});
```

---

## 10. System Boundaries Checklist

- [ ] **Clear Ownership**: Each boundary has an owner?
- [ ] **Well-Defined Interfaces**: APIs/events documented?
- [ ] **No Shared Databases**: Each service owns its data?
- [ ] **Bounded Contexts**: Domain language consistent within boundary?
- [ ] **Anti-Corruption Layers**: External systems isolated?
- [ ] **Testable**: Can test each boundary independently?
- [ ] **Documented**: Boundaries documented in architecture diagrams?
- [ ] **Enforced**: Linting/architecture tests prevent violations?

---

## Related Skills
- `59-architecture-decision/adr-templates`
- `40-system-resilience/service-mesh`
- `51-contracts-governance/api-contracts`
