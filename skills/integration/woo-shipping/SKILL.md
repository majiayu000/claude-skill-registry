---
name: woo-shipping
description: Build WooCommerce shipping methods — WC_Shipping_Method, shipping zones, shipping classes, rate calculation, tracking, and integration with carriers. Use when creating custom shipping integrations or configuring shipping logic.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Shipping Method Development

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.woocommerce.com shipping method api` for shipping method guide
2. Web-search `woocommerce custom shipping method tutorial` for implementation patterns
3. Fetch `https://woocommerce.github.io/code-reference/classes/WC-Shipping-Method.html` for class reference

## Shipping Architecture

### Shipping Zones

Geographic regions that determine available shipping methods:
- Zone = set of geographic rules (countries, states, postcodes)
- Each zone has one or more shipping methods assigned
- "Locations not covered by your other zones" = default catch-all zone
- Zones are evaluated in order — first match wins

### Shipping Classes

Product-level classification for rate customization:
- Assign products to shipping classes (e.g., "Heavy Items", "Fragile")
- Shipping methods can define different rates per class
- Managed in WooCommerce > Settings > Shipping > Shipping Classes

## WC_Shipping_Method

### Base Class

All custom shipping methods extend `WC_Shipping_Method`:

| Property | Description |
|----------|-------------|
| `$id` | Unique method identifier |
| `$method_title` | Admin-facing title |
| `$method_description` | Admin-facing description |
| `$title` | Customer-facing title |
| `$enabled` | Whether method is enabled |
| `$instance_id` | Zone instance ID |
| `$supports` | Supported features array |

### Registration

Filter `woocommerce_shipping_methods`:
```php
add_filter( 'woocommerce_shipping_methods', function( $methods ) {
    $methods['my_shipping'] = 'My_Shipping_Method';
    return $methods;
});
```

## Implementation Methods

### Required Methods

- **`__construct( $instance_id )`** — set `$id`, `$method_title`, `$supports`, initialize settings
- **`init_form_fields()`** — define settings fields (flat rate, per-item, per-class)
- **`calculate_shipping( $package )`** — compute rates and add via `$this->add_rate()`

### calculate_shipping()

Receives `$package` array containing:
- `contents` — cart items in this package
- `destination` — shipping address (country, state, postcode, city)
- `cart_subtotal` — package subtotal

Returns rates via `$this->add_rate()`:
```php
$this->add_rate( [
    'id'       => $this->get_rate_id(),
    'label'    => $this->title,
    'cost'     => $calculated_cost,
    'taxes'    => '', // empty = auto-calculate, 'false' = tax-free
    'calc_tax' => 'per_order', // or 'per_item'
    'package'  => $package,
]);
```

### Instance Settings

For zone-based configuration (per-zone settings):
- Set `$this->instance_form_fields` instead of `$this->form_fields`
- Add `'instance-settings'` and `'instance-settings-modal'` to `$this->supports`
- Settings are stored per zone instance, not globally

## Shipping Packages

### What Packages Are

Cart items grouped for shipping calculation:
- Default: all items in one package
- Filter `woocommerce_cart_shipping_packages` to split items into multiple packages
- Each package is calculated independently (different rates for different groups of items)

### Package Format

```php
$package = [
    'contents'        => [ /* cart items */ ],
    'contents_cost'   => 50.00,
    'applied_coupons' => [],
    'destination'     => [
        'country'  => 'US',
        'state'    => 'CA',
        'postcode' => '90210',
        'city'     => 'Beverly Hills',
    ],
];
```

## Rate Calculation Patterns

### Flat Rate

Fixed cost regardless of cart contents. Optionally add per-item or per-class surcharges.

### Weight-Based

Calculate from total package weight:
- Sum `$item['data']->get_weight() * $item['quantity']` for all items
- Apply rate tiers (e.g., $5 for 0-1kg, $10 for 1-5kg)

### Table Rate

Complex rate calculation based on combinations of weight, item count, destination, and price. Often implemented with rate tables stored in custom DB tables.

### Live API Rates

Call carrier APIs (UPS, FedEx, USPS, DHL):
- Send package dimensions, weight, origin, destination
- Receive available services and rates
- Cache responses (transients) to avoid excessive API calls
- Handle API failures gracefully with fallback rates

## Tracking

### Adding Tracking Data

Store tracking info as order meta:
- `$order->update_meta_data( '_tracking_number', $number )`
- `$order->update_meta_data( '_tracking_provider', $carrier )`
- Display in order emails and My Account via hooks

## Free Shipping

Built-in `WC_Shipping_Free_Shipping` — enable based on:
- Minimum order amount
- Coupon with free shipping
- Both (coupon AND minimum amount)

## Best Practices

- Cache rate calculations (transients) for API-based methods
- Handle API failures with fallback/default rates
- Support shipping classes for per-product rate customization
- Use instance settings for per-zone configuration
- Validate destination before calculating rates
- Return multiple rate options when available (e.g., Standard, Express, Overnight)
- Add tracking support for customer transparency
- Test with various cart compositions (single item, multiple, heavy, virtual mix)

Fetch the WooCommerce shipping method documentation for exact method signatures, package format, and instance settings patterns before implementing.
