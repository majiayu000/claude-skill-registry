---
name: magento-checkout
description: Customize Magento 2 checkout — payment methods, shipping carriers, totals collectors, and checkout UI. Use when building custom payment/shipping integrations or modifying the checkout flow.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Magento 2 Checkout Customization

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.adobe.com commerce php tutorials frontend custom-checkout` for checkout customization tutorials
2. Web-search `site:developer.adobe.com commerce php tutorials frontend custom-checkout add-payment-method` for payment method tutorial
3. Web-search `site:developer.adobe.com commerce php development components checkout` for checkout architecture

## Conceptual Architecture

### Checkout Flow

Two-step checkout built with UI Components + KnockoutJS:
1. **Shipping Step** — address, shipping method selection
2. **Payment & Review Step** — payment method selection, order review, place order

### Quote Model

The central data structure during checkout:
- `Magento\Quote\Model\Quote` — the cart/checkout session
- Contains items, addresses (billing + shipping), payment, totals
- Converted to an Order on successful placement

## Payment Methods

### Three Categories

| Type | Description |
|------|-------------|
| **Gateway** | Data passes through Magento to processor (Stripe, Braintree) |
| **Offline** | No external provider (Check/Money Order, Bank Transfer, COD) |
| **Hosted** | Redirects to external payment page (PayPal Redirect) |

### Implementation Components

1. **Payment Model** — uses Payment Gateway Command pattern with `Magento\Payment\Model\Method\Adapter` as a virtual type (recommended). Note: `Magento\Payment\Model\Method\AbstractMethod` is deprecated; avoid for new payment methods.
2. **Config Provider** — implements `ConfigProviderInterface`, returns JS config for checkout
3. **JS Renderer** — KnockoutJS component rendering the payment form in checkout
4. **di.xml** — register config provider into composite config provider
5. **system.xml/config.xml** — admin configuration fields for enabling/configuring the method

### Payment Gateway Command Pattern

Modern approach (since 2.1) with configurable command chain:
- Command objects for each operation (authorize, capture, refund, void)
- Request builders construct gateway-specific payloads
- Response handlers process gateway responses
- Validators verify responses
- Transfer factory creates HTTP transfer objects

## Shipping Methods

### Carrier Implementation

Shipping carriers extend `Magento\Shipping\Model\Carrier\AbstractCarrier`:
- `collectRates()` — returns available shipping rates for the cart
- `getAllowedMethods()` — returns method code/name pairs
- Configuration in `config.xml` (defaults) and `system.xml` (admin fields)
- Tracking capability via `getTrackingInfo()`

## Totals Collectors

### What Totals Collectors Do

Calculate order totals (subtotal, shipping, tax, discount, grand total):
- Declared in `etc/sales.xml`
- Extend `Magento\Quote\Model\Quote\Address\Total\AbstractTotal`
- `collect()` — performs calculation, modifies quote address totals
- `fetch()` — returns the result for display

### Collector Order

Collectors run in sequence. Standard order: subtotal → discount → shipping → tax → grand_total. Custom collectors must declare their position relative to existing ones.

## Checkout UI Customization

### Layout Modification

Checkout layout is defined in `checkout_index_index.xml`. Modify via:
- Adding new UI components to checkout steps
- Moving/removing existing components
- Plugin on `LayoutProcessorInterface` for dynamic modifications

### Custom Checkout Steps

Add entire new steps via JavaScript UI components registered in the checkout layout.

## Best Practices

- Use the Payment Gateway Command pattern for new payment methods
- Test payment methods in sandbox/test mode before production
- Handle payment failures gracefully with clear customer messaging
- Use config providers to pass server config to checkout JS
- Follow PCI compliance — never log or store raw card data
- Test shipping rate calculation with various cart compositions

Fetch the checkout customization tutorials for exact class signatures, XML configurations, and JS component patterns before implementing.
