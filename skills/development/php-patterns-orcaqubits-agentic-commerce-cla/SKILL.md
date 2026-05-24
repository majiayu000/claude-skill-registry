---
name: php-patterns
description: Apply PHP design patterns — Singleton, Factory, Strategy, Observer, Repository, Decorator, and Dependency Injection in PHP. Use when structuring WooCommerce extension code or implementing complex business logic.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# PHP Design Patterns

## Before writing code

**Fetch live docs**: Web-search `php design patterns modern` for current pattern implementations. Reference `https://refactoring.guru/design-patterns/php` for comprehensive examples.

## Singleton

### What It Does

Ensures only one instance of a class exists. Common in WordPress/WooCommerce plugins as the main plugin class.

### WooCommerce Usage

`WC()` returns the single WooCommerce instance. Extension main classes typically follow:
- Private `__construct()`, private `__clone()`, private `__wakeup()`
- Static `instance()` method
- Global accessor function (e.g., `function my_extension() { return My_Extension::instance(); }`)

### When to Use

Plugin entry points only. Avoid for everything else — singletons are hard to test and create hidden dependencies.

## Factory

### What It Does

Creates objects without specifying the exact class. Decouples object creation from usage.

### WooCommerce Usage

`WC_Product_Factory` resolves product type to correct class:
- `wc_get_product( $id )` — factory method returns `WC_Product_Simple`, `WC_Product_Variable`, etc.
- Filterable via `woocommerce_product_class` hook

### Implementation

Define a factory method or class that maps identifiers to concrete classes. Use for: product types, payment gateway selection, shipping method resolution.

## Strategy

### What It Does

Defines a family of interchangeable algorithms. Client code works with the interface, not the implementation.

### WooCommerce Usage

- Payment gateways — all implement `WC_Payment_Gateway`, swappable at checkout
- Shipping methods — all extend `WC_Shipping_Method`, configurable per zone
- Tax calculators — different calculation strategies per location

### Implementation

Define an interface/abstract class. Create concrete implementations. Select the strategy at runtime based on configuration or context.

## Observer (Hooks)

### What It Does

Objects subscribe to events and get notified when they occur. Loose coupling between event producers and consumers.

### WooCommerce Usage

WordPress hooks ARE the Observer pattern:
- `do_action()` / `apply_filters()` — notify observers
- `add_action()` / `add_filter()` — subscribe
- The entire WordPress/WooCommerce extensibility model is built on this

### Implementation

Use WordPress hooks for WooCommerce extensions. For internal events within your plugin, consider firing custom actions: `do_action( 'my_plugin_after_process', $data )`.

## Repository

### What It Does

Mediates between the domain layer and data mapping layer. Provides collection-like access to data.

### WooCommerce Usage

While WooCommerce uses Data Stores rather than formal Repositories, the concept is similar:
- `wc_get_orders( $args )` — query-based data access
- `wc_get_products( $args )` — product collection access
- CRUD objects encapsulate persistence

### Implementation

Create a class that provides methods like `find_by_id()`, `find_all()`, `save()`, `delete()`. Internally use `wc_get_orders()` or custom queries.

## Decorator

### What It Does

Adds behavior to objects dynamically by wrapping them. Each decorator adds one concern.

### WooCommerce Usage

Filters act as decorators:
- `apply_filters( 'woocommerce_product_get_price', $price, $product )` — each filter wraps/modifies the value
- Stacked filters effectively decorate the data pipeline

### Implementation

Create wrapper classes that implement the same interface as the wrapped object. Delegate most calls, add behavior where needed.

## Dependency Injection

### What It Does

Objects receive their dependencies through constructors or setters rather than creating them internally.

### WooCommerce/WordPress Context

WordPress doesn't have a built-in DI container, but you can practice DI:
- Pass dependencies through constructors
- Use a lightweight container (PHP-DI, League Container) for larger extensions
- Avoid static/global state — inject `WC()`, `$wpdb`, etc. where possible

### Implementation

```php
class OrderProcessor {
    public function __construct(
        private readonly PaymentGateway $gateway,
        private readonly ShippingCalculator $shipping,
    ) {}
}
```

## Service Locator

### What It Does

A registry that provides access to services. Less preferred than DI, but practical in WordPress.

### WooCommerce Usage

- `WC()->payment_gateways()` — access payment gateways registry
- `WC()->shipping()` — access shipping methods registry
- `WC()->cart` — access cart instance

## Template Method

### What It Does

Defines the skeleton of an algorithm in a base class, letting subclasses override specific steps.

### WooCommerce Usage

- `WC_Payment_Gateway` — defines the gateway lifecycle; subclasses implement `process_payment()`, `init_form_fields()`
- `WC_Shipping_Method` — defines shipping lifecycle; subclasses implement `calculate_shipping()`

## Best Practices

- Use Singleton sparingly — only for plugin main class
- Prefer composition over inheritance
- Use WordPress hooks (Observer pattern) for extensibility
- Inject dependencies through constructors when practical
- Use Factory pattern for polymorphic object creation
- Apply SOLID principles: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- Keep classes small and focused

Fetch design pattern references for current PHP implementations and WooCommerce core examples before implementing.
