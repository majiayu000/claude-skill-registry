---
name: autumn-add-payments
description: Skill for adding Stripe checkout and payment flows using Autumn.
---

# Autumn Payments

**Always consult [docs.useautumn.com](https://docs.useautumn.com) for code examples and latest API.**

Autumn handles Stripe checkout, upgrades, downgrades, and cancellations automatically.

---

## Quick Reference

### Payment Flow
1. `checkout` - Returns Stripe URL (new) or preview data (returning customer)
2. `attach` - Confirms purchase when card already on file

### Checkout Result

| Field | Description |
|-------|-------------|
| `url` | Stripe checkout URL (null if card on file) |
| `product` | Target product with scenario |
| `current_product` | Customer's current product |
| `lines` | Invoice line items |
| `total` | Amount in major currency units |
| `currency` | Currency code |

---

## Product Scenarios

| Scenario | Meaning | Action |
|----------|---------|--------|
| `new` | Not subscribed | Subscribe |
| `active` | Current plan | Current Plan |
| `scheduled` | Scheduled | Already Scheduled |
| `upgrade` | Higher tier | Upgrade |
| `downgrade` | Lower tier | Downgrade |
| `renew` | Cancelled | Renew |

---

## React Implementation

```tsx
import { useCustomer, usePricingTable } from "autumn-js/react";

const { checkout, attach } = useCustomer();
const { products } = usePricingTable();

// Checkout flow
const data = await checkout({ productId: "pro" });
if (data.url) {
  window.location.href = data.url;  // New customer
} else {
  // Show confirmation dialog, then:
  await attach({ productId: "pro" });
}

// Cancel
const { cancel } = useCustomer();
await cancel({ productId: "pro" });
// Or downgrade to free:
await attach({ productId: "free" });
```

---

## Backend Implementation

```typescript
import { Autumn } from "autumn-js";

const autumn = new Autumn({ secretKey: process.env.AUTUMN_SECRET_KEY });

// Checkout
const { data } = await autumn.checkout({ customer_id, product_id: "pro" });
if (data.url) return redirect(data.url);

// Attach (after user confirms)
await autumn.attach({ customer_id, product_id: "pro" });

// Get products with scenarios
const { data: productsData } = await autumn.products.list({ customer_id });
```

---

## Prepaid Pricing

For seat-based or prepaid products, pass quantities:

```typescript
await autumn.checkout({
  customer_id,
  product_id: "credits_pack",
  options: [{ feature_id: "credits", quantity: 500 }],
});
```

---

## Button Text Pattern

```typescript
function getButtonText(product: Product): string {
  const { scenario, properties } = product;
  if (properties?.has_trial) return "Start Trial";
  if (scenario === "active") return "Current Plan";
  
  const text = { upgrade: "Upgrade", downgrade: "Downgrade", new: "Subscribe" };
  return text[scenario] ?? "Enable";
}
```

---

## Common Gotchas

1. **URL field** - It's `data.url`, not `data.checkout_url`
2. **Don't build custom logic** - Use `products.list` for scenarios
3. **Proration automatic** - Autumn handles upgrade/downgrade proration
4. **Cancel via free** - Prefer attaching free plan over hard cancel
5. **Success URL** - Pass `success_url` to redirect after Stripe checkout

---

## Resources

- [Checkout Docs](https://docs.useautumn.com/api-reference/core/checkout)
- [Attach Docs](https://docs.useautumn.com/api-reference/core/attach)
- [LLMs.txt](https://docs.useautumn.com/llms.txt)
