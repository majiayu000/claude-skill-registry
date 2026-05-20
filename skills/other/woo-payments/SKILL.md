---
name: woo-payments
description: Build WooCommerce payment gateways — WC_Payment_Gateway, direct/redirect/hosted integrations, tokenization, subscriptions support, refunds, and PCI compliance. Use when creating custom payment method integrations.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Payment Gateway Development

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.woocommerce.com payment gateway api` for payment gateway guide
2. Web-search `woocommerce payment gateway tutorial` for implementation patterns
3. Fetch `https://woocommerce.github.io/code-reference/classes/WC-Payment-Gateway.html` for class reference

## Gateway Architecture

### Base Class: WC_Payment_Gateway

All gateways extend `WC_Payment_Gateway` (which extends `WC_Settings_API`):

| Property | Description |
|----------|-------------|
| `$id` | Unique gateway identifier |
| `$method_title` | Admin-facing title |
| `$method_description` | Admin-facing description |
| `$title` | Customer-facing title |
| `$description` | Customer-facing description |
| `$icon` | URL to gateway icon |
| `$has_fields` | Whether gateway has payment fields on checkout |
| `$supports` | Array of supported features |

### Registration

Filter `woocommerce_payment_gateways`:
```php
add_filter( 'woocommerce_payment_gateways', function( $gateways ) {
    $gateways[] = 'My_Payment_Gateway';
    return $gateways;
});
```

## Implementation Methods

### Required Methods

- **`__construct()`** — set `$id`, `$method_title`, `$supports`, call `init_form_fields()`, `init_settings()`, load saved settings, register `process_admin_options` hook
- **`init_form_fields()`** — define admin settings (API keys, sandbox mode, etc.)
- **`process_payment( $order_id )`** — core payment logic, returns `result` + `redirect` array

### Optional Methods

- `payment_fields()` — render custom payment form HTML on checkout
- `validate_fields()` — validate payment form input
- `process_refund( $order_id, $amount, $reason )` — handle refunds
- `get_icon()` — customize the gateway icon display

### process_payment Return Format

```php
return [
    'result'   => 'success', // or 'failure'
    'redirect' => $order->get_checkout_order_received_url(),
];
```

## Integration Models

### Direct Integration

Gateway processes payment inline:
1. Collect card data via `payment_fields()` (or tokenized via JS SDK)
2. Call payment processor API in `process_payment()`
3. Mark order: `$order->payment_complete( $transaction_id )`
4. Return success with redirect to thank-you page

### Redirect Integration

Customer redirected to external payment page:
1. `process_payment()` returns redirect URL to processor
2. Processor handles payment and redirects back
3. Handle return via a webhook or callback URL
4. Process the response and update order status

### Hosted/Iframe Integration

Payment form loaded in iframe on checkout page:
- Set `$has_fields = true`
- Render iframe/JS SDK in `payment_fields()`
- Handle tokenization callback

## Supports Array

```php
$this->supports = [
    'products',           // Basic payment support
    'refunds',            // process_refund()
    'tokenization',       // Saved payment methods
    'subscriptions',      // WooCommerce Subscriptions
    'subscription_cancellation',
    'subscription_reactivation',
    'subscription_suspension',
    'subscription_amount_changes',
    'subscription_date_changes',
];
```

## Tokenization (Saved Payment Methods)

### WC_Payment_Token System

- Extend `WC_Payment_Token_CC` (credit cards) or `WC_Payment_Token` (generic)
- `$this->supports[] = 'tokenization'`
- Override `tokenization_script()` to enqueue JS
- Save tokens via `WC_Payment_Tokens::set_users_default()`
- Customer manages saved methods in My Account > Payment Methods

## Webhook/IPN Handling

### Registering Webhook Endpoints

Use `WC_API` to register callback URLs:
- `add_action( 'woocommerce_api_{$id}', [ $this, 'handle_webhook' ] )`
- Callback URL: `home_url( '/wc-api/{$id}/' )`
- Verify signatures, process payment notifications, update order status

## Order Status Management

- `$order->update_status( 'processing', 'Payment received' )` — status + note
- `$order->payment_complete( $transaction_id )` — marks paid, triggers emails
- `$order->update_status( 'failed', 'Payment failed' )` — mark failed
- `$order->add_order_note( 'Note text' )` — add admin/customer note

## Block Checkout Support

For block-based checkout, gateways need a JS integration:
1. Register a payment method via `@woocommerce/blocks-registry` → `registerPaymentMethod()`
2. Provide React components for: `content`, `edit`, `label`
3. Define `canMakePayment` callback
4. Handle payment data submission via `onPaymentSetup` event

## Best Practices

- **Never** log or store raw credit card data
- Always use sandbox/test mode for development
- Verify webhook signatures to prevent spoofing
- Handle all error states gracefully with clear customer messages
- Support refunds if the processor allows them
- Declare `cart_checkout_blocks` compatibility and provide block checkout integration
- Use `$order->payment_complete()` — it handles status, stock reduction, and email triggers
- Store transaction IDs via `$order->set_transaction_id()`

Fetch the WooCommerce payment gateway documentation and code reference for exact method signatures, supported features, and block checkout integration patterns before implementing.
