---
name: vendix-product-pricing
description: >
  Patterns for advanced product pricing logic, rentability calculations, and reactive price management in Vendix.
  Trigger: When editing product schemas, pricing logic, or advanced product forms.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Implementing new pricing fields in Product or ProductVariant models.
- Building UI components that require bidirectional price/margin calculations.
- Handling tax-inclusive pricing displays in frontend.
- Managing "On Sale" (Offer) price logic.

## Critical Patterns

### 1. Database Fields

Always include the four pillars of pricing in both `products` and `product_variants` tables:

- `cost_price`: The acquisition cost.
- `profit_margin`: The target profitability percentage.
- `base_price`: The listing price (PVP) before taxes.
- `sale_price`: The promotional price (Offer).
- `is_on_sale`: Boolean flag to activate the offer.

### 2. Bidirectional Calculation Logic (Angular)

When one price field changes, others should update reactively:

- **Margin -> Base Price**: `base_price = cost_price * (1 + margin / 100)`
- **Base Price -> Margin**: `margin = ((base_price - cost_price) / cost_price) * 100` (Only if cost > 0)

### 3. Tax Integration

The final price should always be calculated dynamically based on selected `tax_categories`:

- `final_price = base_price * (1 + sum(tax_rates))`

## Code Examples

### Reactive Form Setup (Angular)

```typescript
private setupPriceCalculations(form: FormGroup): void {
  const costCtrl = form.get('cost_price');
  const marginCtrl = form.get('profit_margin');
  const basePriceCtrl = form.get('base_price');

  // Cost or Margin changed -> Update Base Price
  merge(costCtrl.valueChanges, marginCtrl.valueChanges).subscribe(() => {
    const cost = Number(costCtrl.value || 0);
    const margin = Number(marginCtrl.value || 0);
    const basePrice = cost * (1 + margin / 100);
    basePriceCtrl.setValue(basePrice, { emitEvent: false });
  });

  // Base Price changed -> Update Margin
  basePriceCtrl.valueChanges.subscribe((val) => {
    const cost = Number(costCtrl.value || 0);
    if (cost > 0) {
      const margin = ((val - cost) / cost) * 100;
      marginCtrl.setValue(margin, { emitEvent: false });
    }
  });
}
```

### Prisma Schema Fields

```prisma
model products {
  base_price               Decimal                    @db.Decimal(12, 2)
  cost_price               Decimal?                   @db.Decimal(12, 2)
  profit_margin            Decimal?                   @db.Decimal(5, 2)
  is_on_sale               Boolean                    @default(false)
  sale_price               Decimal?                   @db.Decimal(12, 2)
}
```

## Commands

```bash
# Regenerate Prisma client after adding pricing fields
npx prisma generate

# Apply pricing schema changes
npx prisma migrate dev --name add_pricing_fields
```
