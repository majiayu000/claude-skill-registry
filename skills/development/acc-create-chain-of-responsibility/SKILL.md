---
name: acc-create-chain-of-responsibility
description: Generates Chain of Responsibility pattern for PHP 8.5. Creates handler chains for request processing with middleware-style composition. Includes unit tests.
---

# Chain of Responsibility Pattern Generator

Creates Chain of Responsibility pattern infrastructure for sequential request processing.

## When to Use

| Scenario | Example |
|----------|---------|
| Multiple processors | Validation, discounts, approvals |
| Unknown handlers | Plugin systems |
| Priority processing | First match wins |
| Middleware | HTTP pipeline, logging |

## Component Characteristics

### HandlerInterface
- Defines handle method
- Optional setNext for linking
- Returns result or delegates

### AbstractHandler
- Implements chain linking
- Provides base handle logic
- Simplifies concrete handlers

### Concrete Handlers
- Process specific requests
- Decide to handle or pass
- Can terminate or continue chain

---

## Generation Process

### Step 1: Generate Handler Interface

**Path:** `src/Domain/{BoundedContext}/Handler/`

1. `{Name}HandlerInterface.php` — Handler contract with setNext and handle methods

### Step 2: Generate Abstract Handler

**Path:** `src/Domain/{BoundedContext}/Handler/`

1. `Abstract{Name}Handler.php` — Base class with chain linking logic

### Step 3: Generate Concrete Handlers

**Path:** `src/Domain/{BoundedContext}/Handler/`

1. `{Specific}{Name}Handler.php` — Specific handler implementations

### Step 4: Generate Chain Builder (Optional)

**Path:** `src/Domain/{BoundedContext}/Handler/`

1. `{Name}ChainBuilder.php` — Fluent builder for chain construction

### Step 5: Generate Tests

1. `{Handler}Test.php` — Individual handler tests
2. `{Name}ChainTest.php` — Chain integration tests

---

## File Placement

| Component | Path |
|-----------|------|
| Handler Interface | `src/Domain/{BoundedContext}/Handler/` |
| Abstract Handler | `src/Domain/{BoundedContext}/Handler/` |
| Concrete Handlers | `src/Domain/{BoundedContext}/Handler/` |
| Chain Builder | `src/Domain/{BoundedContext}/Handler/` |
| Pipeline | `src/Application/Pipeline/` |
| Unit Tests | `tests/Unit/Domain/{BoundedContext}/Handler/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Interface | `{Name}HandlerInterface` | `ValidationHandlerInterface` |
| Abstract | `Abstract{Name}Handler` | `AbstractValidationHandler` |
| Concrete | `{Specific}{Name}Handler` | `EmailValidationHandler` |
| Builder | `{Name}ChainBuilder` | `ValidationChainBuilder` |
| Test | `{ClassName}Test` | `EmailValidationHandlerTest` |

---

## Quick Template Reference

### Handler Interface

```php
interface {Name}HandlerInterface
{
    public function setNext(self $handler): self;
    public function handle({RequestType} $request): {ResultType};
}
```

### Abstract Handler

```php
abstract class Abstract{Name}Handler implements {Name}HandlerInterface
{
    private ?{Name}HandlerInterface $next = null;

    public function setNext({Name}HandlerInterface $handler): {Name}HandlerInterface
    {
        $this->next = $handler;
        return $handler;
    }

    public function handle({RequestType} $request): {ResultType}
    {
        if ($this->next !== null) {
            return $this->next->handle($request);
        }
        return $this->getDefaultResult();
    }

    abstract protected function getDefaultResult(): {ResultType};
}
```

### Concrete Handler

```php
final class {Specific}Handler extends Abstract{Name}Handler
{
    public function handle({RequestType} $request): {ResultType}
    {
        if ($this->canHandle($request)) {
            return $this->process($request);
        }
        return parent::handle($request);
    }

    private function canHandle({RequestType} $request): bool
    {
        return {condition};
    }
}
```

### Chain Builder

```php
final class {Name}ChainBuilder
{
    private array $handlers = [];

    public function add({Name}HandlerInterface $handler): self
    {
        $this->handlers[] = $handler;
        return $this;
    }

    public function build(): {Name}HandlerInterface
    {
        $first = $this->handlers[0];
        $current = $first;
        for ($i = 1; $i < count($this->handlers); $i++) {
            $current = $current->setNext($this->handlers[$i]);
        }
        return $first;
    }
}
```

---

## Usage Examples

### Validation Chain

```php
$chain = (new ValidationChainBuilder())
    ->add(new NotEmptyValidationHandler('email'))
    ->add(new EmailValidationHandler('email'))
    ->add(new MinLengthValidationHandler('password', 8))
    ->build();

$result = $chain->validate($request);

if ($result->hasErrors()) {
    throw new ValidationException($result->getMessage());
}
```

### Discount Chain

```php
$vipHandler = new VipDiscountHandler();
$promoHandler = new PromoCodeDiscountHandler($promoCodes);
$bulkHandler = new BulkDiscountHandler();

$vipHandler->setNext($promoHandler);
$promoHandler->setNext($bulkHandler);

$result = $vipHandler->apply($discountRequest);
```

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Circular Chain | Infinite loop | Validate chain structure |
| No Default | Unhandled requests | Provide fallback handler |
| Coupled Handlers | Hard to reorder | Use interface properly |
| Missing Builder | Manual chain assembly | Create ChainBuilder |
| State in Handler | Non-reentrant | Make handlers stateless |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — Handler Interface, Abstract Handler, Concrete Handler, Chain Builder, Pipeline templates
- `references/examples.md` — Validation Chain, Discount Chain examples and tests
