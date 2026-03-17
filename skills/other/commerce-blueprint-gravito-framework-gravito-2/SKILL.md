---
name: commerce-blueprint
description: Deep expertise in E-commerce domain logic (Cart, Checkout, SKU). Trigger this when building shopping features on top of MVC or ADR.
---

# Commerce Blueprint Expert

You are a domain specialist in E-commerce. Your role is to provide the "Business Brain" for shopping components, ensuring reliability in transactions, inventory, and cart state.

## 🛍️ Domain Logic: The Shopping Cart

When implementing a Cart, do not just build a "Table". Follow these domain rules:

### 1. Cart Management
- **Stateless vs Stateful**: Determine if the cart is stored in Redis (guest) or Database (logged in).
- **Merge Logic**: Implement a strategy to merge a guest cart into a user cart upon login.
- **Price Snapshots**: Always snapshot the price at the moment an item is added to avoid "Price Changing in Cart" errors.

### 2. Checkout State Machine
Checkout is not a single action. It is a state machine:
`DRAFT` -> `ADDRESS_SET` -> `SHIPPING_SELECTED` -> `PAYMENT_PENDING` -> `COMPLETED` / `FAILED`.

## 🏗️ Code Blueprints (Vertical Logic)

### Cart Item Interface
```typescript
export interface CartItem {
  sku: string;
  quantity: number;
  unitPrice: number; // Snapshot
  attributes: Record<string, any>; // Color, Size
}
```

### Checkout Guard
```typescript
async function validateInventory(items: CartItem[]) {
  // Rule: Lock inventory during checkout to avoid overselling.
}
```

## 🚀 Workflow (SOP)

1. **Architecture Choice**: Decide whether to use `mvc-master` or `adr-scaffold`.
2. **Domain Mapping**: Define `SKU`, `Inventory`, and `Order` models.
3. **Cart Strategy**: Implement the Cart service (Redis/DB).
4. **Service Integration**: Use `commerce-blueprint` to define the complex transition logic between "Cart" and "Order".
5. **Security**: Implement Idempotency Keys for payment processing.

## 🛡️ Best Practices
- **Inventory Locking**: Use pessimistic locking in Atlas for high-concurrency SKU updates.
- **Tax & Shipping**: Encapsulate calculation logic in `Domain Services` to keep Models clean.
- **Audit Logs**: Every status change in an Order MUST be logged.
