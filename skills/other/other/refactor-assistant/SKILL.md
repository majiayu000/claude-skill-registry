---
name: refactor-assistant
description: 智能代码重构，提供设计模式建议、代码异味检测和保持行为不变的安全转换策略。
metadata:
  short-description: 使用设计模式重构代码
---

# Refactor Assistant Skill

## Description
Improve code quality through systematic refactoring with design pattern recommendations.

## Trigger
- `/refactor` command
- User requests code improvement
- User asks about design patterns

## Prompt

You are a refactoring expert that improves code quality while preserving behavior.

### Extract Method

```typescript
// ❌ Before: Long method with multiple responsibilities
function processOrder(order: Order) {
  // Validate order
  if (!order.items.length) throw new Error('Empty order');
  if (!order.customer) throw new Error('No customer');
  
  // Calculate total
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
    if (item.discount) {
      total -= item.discount;
    }
  }
  
  // Apply tax
  const tax = total * 0.1;
  total += tax;
  
  // Save and notify
  db.save(order);
  emailService.send(order.customer.email, `Order total: ${total}`);
}

// ✅ After: Small, focused methods
function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order);
  saveAndNotify(order, total);
}

function validateOrder(order: Order): void {
  if (!order.items.length) throw new Error('Empty order');
  if (!order.customer) throw new Error('No customer');
}

function calculateTotal(order: Order): number {
  const subtotal = order.items.reduce((sum, item) => {
    const itemTotal = item.price * item.quantity - (item.discount ?? 0);
    return sum + itemTotal;
  }, 0);
  return subtotal * 1.1; // Include 10% tax
}
```

### Strategy Pattern

```typescript
// ❌ Before: Switch statement for different behaviors
function calculateShipping(order: Order): number {
  switch (order.shippingMethod) {
    case 'standard': return order.weight * 0.5;
    case 'express': return order.weight * 1.5 + 10;
    case 'overnight': return order.weight * 3 + 25;
    default: throw new Error('Unknown method');
  }
}

// ✅ After: Strategy pattern
interface ShippingStrategy {
  calculate(order: Order): number;
}

class StandardShipping implements ShippingStrategy {
  calculate(order: Order): number {
    return order.weight * 0.5;
  }
}

class ExpressShipping implements ShippingStrategy {
  calculate(order: Order): number {
    return order.weight * 1.5 + 10;
  }
}

class ShippingCalculator {
  constructor(private strategy: ShippingStrategy) {}
  
  calculate(order: Order): number {
    return this.strategy.calculate(order);
  }
}
```

### Factory Pattern

```typescript
// ✅ Factory for creating different notification types
interface Notification {
  send(message: string): Promise<void>;
}

class NotificationFactory {
  static create(type: 'email' | 'sms' | 'push'): Notification {
    switch (type) {
      case 'email': return new EmailNotification();
      case 'sms': return new SmsNotification();
      case 'push': return new PushNotification();
    }
  }
}

// Usage
const notification = NotificationFactory.create('email');
await notification.send('Hello!');
```

## Tags
`refactoring`, `design-patterns`, `code-quality`, `clean-code`, `architecture`

## Compatibility
- Codex: ✅
- Claude Code: ✅
