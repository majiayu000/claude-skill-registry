---
name: acc-create-strategy
description: Generates Strategy pattern for PHP 8.5. Creates interchangeable algorithm families with context class, strategy interface, and concrete implementations. Includes unit tests.
---

# Strategy Pattern Generator

Creates Strategy pattern infrastructure for interchangeable algorithm families.

## When to Use

| Scenario | Example |
|----------|---------|
| Multiple algorithms | Pricing, tax, shipping calculation |
| Runtime selection | Payment processing based on amount |
| Avoiding conditionals | Replace switch/if-else chains |
| Algorithm families | Sorting, compression, encryption |

## Component Characteristics

### StrategyInterface
- Defines algorithm contract
- Single method for execution
- Supports method for selection

### Strategy Resolver
- Resolves appropriate strategy
- Based on input criteria
- Falls back to default

### Concrete Strategies
- Implement specific algorithms
- Interchangeable via interface
- Encapsulate algorithm details

---

## Generation Process

### Step 1: Generate Strategy Interface

**Path:** `src/Domain/{BoundedContext}/Strategy/`

1. `{Name}StrategyInterface.php` — Algorithm contract with supports method

### Step 2: Generate Concrete Strategies

**Path:** `src/Domain/{BoundedContext}/Strategy/`

1. `{Variant1}{Name}Strategy.php` — First algorithm implementation
2. `{Variant2}{Name}Strategy.php` — Second algorithm implementation
3. `Default{Name}Strategy.php` — Fallback implementation

### Step 3: Generate Resolver

**Path:** `src/Domain/{BoundedContext}/Strategy/`

1. `{Name}StrategyResolver.php` — Strategy selection logic

### Step 4: Generate Service (Optional)

**Path:** `src/Domain/{BoundedContext}/Strategy/`

1. `{Name}Service.php` — Facade using resolver

### Step 5: Generate Tests

1. `{Variant}{Name}StrategyTest.php` — Individual strategy tests
2. `{Name}StrategyResolverTest.php` — Resolver tests

---

## File Placement

| Component | Path |
|-----------|------|
| Strategy Interface | `src/Domain/{BoundedContext}/Strategy/` |
| Concrete Strategies | `src/Domain/{BoundedContext}/Strategy/` |
| Resolver | `src/Domain/{BoundedContext}/Strategy/` |
| Unit Tests | `tests/Unit/Domain/{BoundedContext}/Strategy/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Interface | `{Name}StrategyInterface` | `PricingStrategyInterface` |
| Concrete | `{Variant}{Name}Strategy` | `BulkPricingStrategy` |
| Context | `{Name}Context` | `PricingContext` |
| Resolver | `{Name}StrategyResolver` | `PricingStrategyResolver` |
| Test | `{ClassName}Test` | `BulkPricingStrategyTest` |

---

## Quick Template Reference

### Strategy Interface

```php
interface {Name}StrategyInterface
{
    public function execute({InputType} $input): {OutputType};
    public function supports({InputType} $input): bool;
}
```

### Concrete Strategy

```php
final readonly class {Variant}{Name}Strategy implements {Name}StrategyInterface
{
    public function execute({InputType} $input): {OutputType}
    {
        {algorithmImplementation}
    }

    public function supports({InputType} $input): bool
    {
        return {condition};
    }
}
```

### Strategy Resolver

```php
final readonly class {Name}StrategyResolver
{
    public function __construct(
        private iterable $strategies,
        private {Name}StrategyInterface $defaultStrategy
    ) {}

    public function resolve({InputType} $input): {Name}StrategyInterface
    {
        foreach ($this->strategies as $strategy) {
            if ($strategy->supports($input)) {
                return $strategy;
            }
        }
        return $this->defaultStrategy;
    }
}
```

---

## Usage Example

```php
// Configure strategies
$resolver = new PricingStrategyResolver(
    strategies: [
        new BulkPricingStrategy(),      // 15% off for 100+ items
        new PromotionalPricingStrategy(), // Active promotion discount
        new VipPricingStrategy(),        // VIP customer discount
    ],
    defaultStrategy: new RegularPricingStrategy()
);

// Use in service
$strategy = $resolver->resolve($pricingContext);
$price = $strategy->calculatePrice($pricingContext);
```

---

## Common Strategy Examples

| Domain | Strategies |
|--------|------------|
| Pricing | Regular, Bulk, Promotional, VIP |
| Shipping | Standard, Express, Free, International |
| Tax | US, EU, Exempt, Zero-rated |
| Payment | Credit Card, PayPal, Bank Transfer |
| Discount | Percentage, Fixed, Buy-One-Get-One |

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Stateful Strategies | Side effects | Make strategies readonly |
| Fat Context | Too much coupling | Minimal context interface |
| Missing Resolver | Manual strategy selection | Use resolver pattern |
| Over-engineering | Single algorithm | Don't use pattern |
| Leaky Abstraction | Strategy-specific types | Use shared interfaces |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — Strategy Interface, Concrete Strategy, Resolver, Context templates
- `references/examples.md` — Pricing, Shipping, Tax strategies and tests
