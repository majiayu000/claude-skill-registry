---
name: wix-service-plugin
description: Creates service plugins (SPIs) for Wix eCommerce that extend checkout and order functionality. Implements custom logic for shipping rates, additional fees, tax calculations, cart validations, gift cards, product recommendations, and catalog integrations. Use when adding custom shipping rate calculations, dynamic fees (handling, rush), tax calculation logic, cart/checkout validations, gift card/voucher systems, product recommendations, external catalog integrations, or custom discount triggers. Triggers: SPI, service plugin, shipping rates, shipping, fees, additional fees, tax, tax calculation, validation, checkout validation, gift card, voucher, recommendations, catalog, eCommerce, ecom, checkout, cart, handler.
license: MIT
compatibility: Requires Wix CLI project with eCommerce service plugin support
metadata:
  author: wix
  version: "1.0.0"
  category: wix-extensions
---

# Wix Service Plugin (SPI) Builder

Creates service plugin extensions for Wix CLI applications. Service plugins implement custom backend logic that integrates with Wix eCommerce flows, enabling customization of shipping, fees, taxes, validations, and more.

## Non-Matching Intents

Do NOT use this skill for:

- **Dashboard admin interfaces** → Use `wix-dashboard-page`
- **Database/collection schemas** → Use `wix-cms-collection`
- **Backend API endpoints** → Use `wix-backend-api`
- **Embedded scripts on site** → Use `wix-embedded-script`
- **Backend event handlers** → Use `wix-backend-event`

## Available Service Plugins

| SPI                                               | Description                                 |
| ------------------------------------------------- | ------------------------------------------- |
| `ecom.shippingRates.getShippingRates`             | Calculate custom shipping options and costs |
| `ecom.additionalFees.calculateAdditionalFees`     | Add fees like handling, rush delivery       |
| `ecom.validations.getValidationViolations`        | Validate cart/checkout conditions           |
| `ecom.taxCalculationProvider.calculateTax`        | Custom tax calculation logic                |
| `ecom.giftCardsProvider.redeem`                   | Redeem gift cards/vouchers                  |
| `ecom.giftCardsProvider.getBalance`               | Check gift card balance                     |
| `ecom.giftCardsProvider._void`                    | Void/cancel gift card redemption            |
| `ecom.recommendationsProvider.getRecommendations` | Provide product recommendations             |
| `ecom.catalog.getCatalogItems`                    | Integrate external product catalogs         |
| `ecom.customTriggers.getEligibleTriggers`         | Custom discount trigger conditions          |
| `ecom.customTriggers.listTriggers`                | List available custom triggers              |
| `ecom.paymentSettings.getPaymentSettings`         | Configure payment options                   |

## Output Structure

Service plugins live under `src/backend/service-plugins`. Each plugin has its own folder. Registration of plugins is not your concern.

```
src/backend/service-plugins/
└── {service-type}/
    └── {plugin-name}/
        ├── plugin.ts      # Main implementation
        └── plugin.json    # Plugin configuration
```

## Implementation Requirements

### Generation Requirements

1. **Implement ALL required handler functions** with complete business logic
2. **Include proper TypeScript types and error handling**
3. **Focus on implementing the EXACT business logic** described in the user prompt

### Implementation Patterns

- **If capabilities are undocumented/unavailable**, explicitly state the gap and proceed only with documented minimal logic
- **Implement all required handler functions** according to Wix specifications
- **Never use placeholders** - always implement complete, working functionality

### Data Validation

All service plugins must include comprehensive data validation:

- **Validate all input data** from Wix requests
- **Ensure required fields** are present and properly formatted
- **Handle missing or malformed data** gracefully
- **Validate business logic constraints** (e.g., minimum order amounts, valid addresses)

## Implementation Pattern

```typescript
import { shippingRates } from "@wix/ecom/service-plugins";

shippingRates.provideHandlers({
  getShippingRates: async (payload) => {
    const { request, metadata } = payload;

    // Implement custom logic based on request data
    // - request contains cart items, shipping address, etc.
    // - metadata contains currency, locale, etc.

    return {
      shippingRates: [
        {
          code: "custom-shipping",
          title: "Custom Shipping",
          logistics: {
            deliveryTime: "3-5 business days",
          },
          cost: {
            price: "9.99",
            currency: metadata.currency || "USD",
          },
        },
      ],
    };
  },
});
```

## Examples

### Custom Shipping Rates

**Request:** "Create shipping rates based on package weight with express option"

**Output:**

```typescript
import { shippingRates } from "@wix/ecom/service-plugins";
import { ChargeType } from "@wix/auto_sdk_ecom_shipping-rates";

shippingRates.provideHandlers({
  getShippingRates: async ({ request, metadata }) => {
    const totalWeight =
      request.lineItems?.reduce(
        (sum, item) =>
          sum + (item.physicalProperties?.weight || 0) * item.quantity,
        0
      ) || 0;

    const baseRate =
      totalWeight <= 5 ? 5.99 : totalWeight <= 20 ? 12.99 : 24.99;

    return {
      shippingRates: [
        {
          code: "standard",
          title: "Standard Shipping",
          logistics: { deliveryTime: "5-7 business days" },
          cost: {
            price: String(baseRate),
            currency: metadata.currency || "USD",
          },
        },
        {
          code: "express",
          title: "Express Shipping",
          logistics: { deliveryTime: "1-2 business days" },
          cost: {
            price: String(baseRate * 2.5),
            currency: metadata.currency || "USD",
          },
        },
      ],
    };
  },
});
```

### Additional Fees

**Request:** "Add a handling fee for fragile items"

**Output:**

```typescript
import { additionalFees } from "@wix/ecom/service-plugins";

additionalFees.provideHandlers({
  calculateAdditionalFees: async ({ request, metadata }) => {
    const hasFragileItems = request.lineItems?.some(
      (item) => item.catalogReference?.options?.fragile === "true"
    );

    if (!hasFragileItems) {
      return { additionalFees: [] };
    }

    return {
      additionalFees: [
        {
          code: "fragile-handling",
          name: "Fragile Item Handling",
          price: { amount: "4.99", currency: metadata.currency || "USD" },
          taxDetails: { taxable: true },
        },
      ],
    };
  },
});
```

### Cart Validation

**Request:** "Prevent checkout if cart total is under $25"

**Output:**

```typescript
import { validations } from "@wix/ecom/service-plugins";

validations.provideHandlers({
  getValidationViolations: async ({ request }) => {
    const cartTotal = parseFloat(request.priceSummary?.subtotal?.amount || "0");
    const minimumOrder = 25;

    if (cartTotal < minimumOrder) {
      return {
        violations: [
          {
            severity: "ERROR",
            target: { other: { name: "CART" } },
            description: `Minimum order amount is $${minimumOrder}. Please add $${(
              minimumOrder - cartTotal
            ).toFixed(2)} more to checkout.`,
          },
        ],
      };
    }

    return { violations: [] };
  },
});
```

### Tax Calculation

**Request:** "Calculate tax based on shipping destination state"

**Output:**

```typescript
import { taxCalculationProvider } from "@wix/ecom/service-plugins";

const STATE_TAX_RATES: Record<string, number> = {
  CA: 0.0725,
  NY: 0.08,
  TX: 0.0625,
  // Add more states as needed
};

taxCalculationProvider.provideHandlers({
  calculateTax: async ({ request }) => {
    const state = request.shippingAddress?.subdivision;
    const taxRate = STATE_TAX_RATES[state || ""] || 0;

    const lineItemTaxes =
      request.lineItems?.map((item) => {
        const amount = parseFloat(item.price?.amount || "0");
        const taxAmount = (amount * taxRate).toFixed(2);

        return {
          lineItemId: item._id,
          taxBreakdown: [
            {
              name: "State Sales Tax",
              rate: String(taxRate * 100),
              amount: {
                amount: taxAmount,
                currency: request.currency || "USD",
              },
            },
          ],
        };
      }) || [];

    return { lineItemTaxes };
  },
});
```

## Best Practices

### Development Workflow

- **Always implement complete, working functionality** - never use placeholders
- **Handle all required fields** according to Wix documentation
- **Implement proper validation** for all input data
- **Return responses in exact format** expected by Wix
- **Add comprehensive error handling** for all failure scenarios
- **Use meaningful variable names** and clear code structure
- **Test thoroughly** with different input combinations

### Implementation Guidelines

- **Validate all input:** Check required fields are present and properly formatted
- **Handle errors gracefully:** Return appropriate error responses, don't throw unhandled exceptions
- **Return exact format:** Responses must match Wix documented structure exactly
- **Use TypeScript types:** Leverage SDK types for better type safety
- **Test edge cases:** Empty carts, missing addresses, invalid data
- **Performance:** Keep calculations efficient - these run on every checkout
- **Logging:** Add console.log for debugging but keep production logs minimal

## Extension Registration

**Extension registration is MANDATORY and has TWO required steps.**

### Step 1: Create Plugin-Specific Extension File

Each service plugin requires an `extensions.ts` file in its folder with the appropriate builder method for the SPI type:

```typescript
import { extensions } from "@wix/astro/builders";

export const ecomshippingratesMyShipping = extensions.ecomShippingRates({
  id: "{{GENERATE_UUID}}",
  name: "My Shipping Rates",
  source: "./backend/service-plugins/ecom-shipping-rates/my-shipping/plugin.ts",
});
```

**CRITICAL: UUID Generation**

The `id` must be a unique, static UUID v4 string. Generate a fresh UUID for each extension - do NOT use `randomUUID()` or copy UUIDs from examples. Replace `{{GENERATE_UUID}}` with a freshly generated UUID like `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`.

| Property | Type   | Description                            |
| -------- | ------ | -------------------------------------- |
| `id`     | string | Unique static UUID v4 (generate fresh) |
| `name`   | string | Display name for the service           |
| `source` | string | Relative path to the plugin.ts         |

**Builder methods by SPI type:**

| SPI Type          | Builder Method           |
| ----------------- | ------------------------ |
| Shipping Rates    | `ecomShippingRates()`    |
| Additional Fees   | `ecomAdditionalFees()`   |
| Validations       | `ecomValidations()`      |
| Discount Triggers | `ecomDiscountTriggers()` |
| Gift Cards        | `ecomGiftCards()`        |
| Payment Settings  | `ecomPaymentSettings()`  |

### Step 2: Register in Main Extensions File

**CRITICAL:** After creating the plugin-specific extension file, you MUST read [../references/EXTENSIONS.md](../references/EXTENSIONS.md) and follow the "App Registration" section to update `src/extensions.ts`.

**Without completing Step 2, the service plugin will not be active in the eCommerce system.**
