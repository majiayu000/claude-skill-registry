---
name: refactoring-suggester
description: Suggest refactoring opportunities to improve code structure and maintainability. Use when improving code design or reducing complexity.
---

# Refactoring Suggester Skill

コードのリファクタリング提案を行うスキルです。

## 主な機能

- **Extract Method**: 長いメソッドを分割
- **Rename**: 分かりやすい命名に変更
- **Remove Duplication**: 重複排除
- **Simplify Conditionals**: 条件式の簡略化
- **Design Patterns**: パターン適用提案

## リファクタリング例

### Extract Method

```javascript
// Before
function processOrder(order) {
  // 検証
  if (!order.items || order.items.length === 0) {
    throw new Error('No items');
  }
  if (!order.customer) {
    throw new Error('No customer');
  }

  // 価格計算
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }
  const tax = total * 0.1;
  total += tax;

  // 保存
  const saved = db.orders.save(order);
  return saved;
}

// After: Extract Method
function processOrder(order) {
  validateOrder(order);
  const total = calculateTotal(order);
  return saveOrder(order, total);
}

function validateOrder(order) {
  if (!order.items || order.items.length === 0) {
    throw new Error('No items');
  }
  if (!order.customer) {
    throw new Error('No customer');
  }
}

function calculateTotal(order) {
  const subtotal = order.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  return subtotal * 1.1; // +10% tax
}

function saveOrder(order, total) {
  order.total = total;
  return db.orders.save(order);
}
```

### Replace Magic Numbers

```python
# Before
def calculate_price(item):
    if item.category == 'premium':
        return item.price * 0.9
    elif item.category == 'vip':
        return item.price * 0.8
    return item.price * 1.0

# After
DISCOUNT_RATES = {
    'premium': 0.9,
    'vip': 0.8,
    'regular': 1.0
}

def calculate_price(item):
    rate = DISCOUNT_RATES.get(item.category, 1.0)
    return item.price * rate
```

### Simplify Conditionals

```typescript
// Before
function getShippingCost(weight: number, distance: number): number {
  if (weight < 5) {
    if (distance < 100) {
      return 10;
    } else {
      return 15;
    }
  } else {
    if (distance < 100) {
      return 20;
    } else {
      return 25;
    }
  }
}

// After: Guard Clauses
function getShippingCost(weight: number, distance: number): number {
  const isLight = weight < 5;
  const isNear = distance < 100;

  if (isLight && isNear) return 10;
  if (isLight && !isNear) return 15;
  if (!isLight && isNear) return 20;
  return 25;
}

// Better: Lookup table
const SHIPPING_RATES = {
  'light_near': 10,
  'light_far': 15,
  'heavy_near': 20,
  'heavy_far': 25
};

function getShippingCost(weight: number, distance: number): number {
  const weightKey = weight < 5 ? 'light' : 'heavy';
  const distanceKey = distance < 100 ? 'near' : 'far';
  const key = `${weightKey}_${distanceKey}`;
  return SHIPPING_RATES[key];
}
```

## バージョン情報
- Version: 1.0.0
