---
name: woo-checkout
description: Customize WooCommerce checkout — classic and block-based checkout, custom fields, validation, order processing, and checkout extensibility. Use when modifying the checkout flow, adding custom checkout fields, or integrating checkout extensions.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Checkout Customization

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.woocommerce.com checkout` for checkout documentation
2. Web-search `woocommerce checkout blocks extensibility api` for block checkout patterns
3. Web-search `woocommerce classic checkout customization hooks` for classic checkout hooks

## Two Checkout Implementations

### Classic Checkout (Shortcode-Based)

- Uses `[woocommerce_checkout]` shortcode
- PHP-rendered with `WC_Checkout` class
- Fully extensible via actions and filters
- Template: `checkout/form-checkout.php`

### Block-Based Checkout (Default Since WC 8.3)

- Uses the Checkout Block in the block editor
- React-rendered on the frontend
- Extended via the Store API and `@woocommerce/blocks-checkout` package
- More structured extension API but different from classic hooks

## Classic Checkout Customization

### Checkout Fields

Filter `woocommerce_checkout_fields` to modify fields:
- Field groups: `billing`, `shipping`, `account`, `order`
- Each field has: `type`, `label`, `placeholder`, `required`, `class`, `priority`, `validate`
- Field types: `text`, `textarea`, `select`, `radio`, `checkbox`, `email`, `tel`, `password`, `country`, `state`

### Adding Custom Fields

Add to the fields array in the `woocommerce_checkout_fields` filter:
- Set `priority` to control ordering
- Set `custom_attributes` for HTML attributes

### Validating Custom Fields

Action `woocommerce_checkout_process`:
- Check `$_POST` values
- Add errors with `wc_add_notice( $message, 'error' )`

### Saving Custom Field Data

Action `woocommerce_checkout_update_order_meta` (legacy) or `woocommerce_checkout_order_processed`:
- Save to order meta: `$order->update_meta_data( '_my_field', $value ); $order->save();`

### Displaying Custom Fields

- Admin: `woocommerce_admin_order_data_after_billing_address` action
- Emails: `woocommerce_email_after_order_table` action
- Thank-you page: `woocommerce_thankyou` action

## Block Checkout Customization

### Extending via Store API

Add custom data to checkout process:
1. Register endpoint data with `ExtendSchema::register_endpoint_data()`
2. Process during checkout via `woocommerce_store_api_checkout_update_order_from_request`

### Checkout Filters (JS)

`registerCheckoutFilters` from `@woocommerce/blocks-checkout`:
- `itemName` — modify cart item name
- `cartItemPrice` — modify displayed price
- `subtotalPriceFormat` — modify subtotal format
- `coupons` — modify coupon display
- Custom filters via `__experimental_woocommerce_blocks_checkout_update_shipping_address`

### Slot Fills (JS)

Inject React components at predefined points:
- `ExperimentalOrderMeta` — after order summary
- `ExperimentalDiscountsMeta` — after discounts
- `ExperimentalOrderShippingPackages` — shipping packages area

### Inner Blocks

Register custom blocks as checkout inner blocks for maximum layout control.

## Checkout Flow

### Order Processing Sequence

1. Validate fields (`woocommerce_checkout_process`)
2. Create order (`woocommerce_checkout_create_order`)
3. Process payment (`WC_Payment_Gateway::process_payment()`)
4. On success: redirect to thank-you page
5. Hooks: `woocommerce_checkout_order_processed`, `woocommerce_payment_complete`, `woocommerce_thankyou`

### Cart to Order Conversion

`WC_Checkout::create_order()`:
- Creates `WC_Order` from cart data
- Copies billing/shipping addresses, line items, fees, coupons
- Applies `woocommerce_checkout_create_order` filter

## Checkout Fees

Add fees via `woocommerce_cart_calculate_fees` action:
- `WC()->cart->add_fee( $name, $amount, $taxable, $tax_class )`
- Negative amounts for discounts

## Best Practices

- Support both classic and block checkout — test with both
- Use CRUD methods to save order data (HPOS compatible)
- Validate on the server side — never trust client-side validation
- Sanitize all checkout field input
- Use nonces for classic checkout forms
- Add clear error messages with `wc_add_notice()`
- Declare `cart_checkout_blocks` compatibility

Fetch the WooCommerce checkout documentation for exact hook names, Store API extension methods, and block checkout patterns before implementing.
