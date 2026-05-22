---
name: architecture-tech-lead
description: "Expert architectural review and refactoring guidance for Java/Spring Boot and Next.js/TypeScript codebases. Use when: (1) implementing features needing architectural validation, (2) refactoring for testability, (3) reviewing complex/hard-to-test code, (4) structuring code for maximum unit/property test coverage with minimal mocking. Covers functional core/imperative shell, DDD, data-oriented design, Java 21+ features (records, sealed types, pattern matching), property-based testing (jqwik), and modern React/Next.js patterns."
imports:
  - "../../rules/architecture.md"
---

# Architecture Tech Lead Skill

Expert guidance for architectural review, refactoring, and testability optimization across Java/Spring Boot and Next.js/TypeScript stacks.

**Core principles defined in @rules/architecture.md** - this skill provides detailed patterns and review process.

---

## Review Process

### 1. Identify Testability Barriers
- Locate side effects (DB, APIs, randomness, time)
- Find business logic coupled to infrastructure
- Spot hidden dependencies and implicit state
- Identify mock-requiring areas

### 2. Architectural Analysis
- Map where business logic mixes with I/O
- Identify extractable "functional core"
- Determine "imperative shell" boundaries
- Assess dependency graph and coupling

### 3. Design Refactoring Strategy

**a) Pure Function Extraction**
- Extract business logic to pure functions
- Pass all dependencies as parameters
- Show resulting testable signatures

**b) Data Transformation Pipeline**
- Flow: fetch data -> transform (pure) -> persist
- Each step independently testable
- Show composition approach

**c) Test Strategy**
- **Unit Tests**: Pure function tests
- **Property Tests**: Invariants that always hold
- **Edge Tests**: Minimal integration for I/O only

---

## Java 21+ Architecture Patterns

### Records for Immutable Domain Models
```java
// Prefer records over classes for DTOs and value objects
public record OrderLine(ProductId productId, int quantity, Money price) {
    public OrderLine {
        if (quantity <= 0) throw new IllegalArgumentException("qty must be positive");
    }

    public Money total() {
        return price.multiply(quantity);
    }
}

public record Order(OrderId id, CustomerId customer, List<OrderLine> lines, Instant createdAt) {
    public Order {
        lines = List.copyOf(lines); // defensive copy, immutable
    }

    public Money total() {
        return lines.stream()
            .map(OrderLine::total)
            .reduce(Money.ZERO, Money::add);
    }
}
```

### Sealed Types for Domain Modeling
```java
// Exhaustive pattern matching, compiler-verified
public sealed interface PaymentResult permits PaymentSuccess, PaymentFailed, PaymentPending {
    record PaymentSuccess(TransactionId txId, Instant completedAt) implements PaymentResult {}
    record PaymentFailed(ErrorCode code, String message) implements PaymentResult {}
    record PaymentPending(String redirectUrl) implements PaymentResult {}
}

// Pattern matching in switch (Java 21+)
public String handlePayment(PaymentResult result) {
    return switch (result) {
        case PaymentSuccess(var txId, _) -> "Success: " + txId;
        case PaymentFailed(var code, var msg) -> "Failed: " + code + " - " + msg;
        case PaymentPending(var url) -> "Redirect to: " + url;
    };
}
```

### Data-Oriented Programming
```java
// Pure functions operating on immutable data
public class PricingRules {
    // Pure: no side effects, deterministic
    public static Money calculateDiscount(Order order, CustomerTier tier) {
        var subtotal = order.total();
        var discountPercent = switch (tier) {
            case GOLD -> 15;
            case SILVER -> 10;
            case BRONZE -> 5;
            case STANDARD -> 0;
        };
        return subtotal.multiply(discountPercent).divide(100);
    }

    // Pure: transforms data, returns new data
    public static Order applyDiscount(Order order, Money discount) {
        // Returns new immutable Order with discount applied
        return new Order(order.id(), order.customer(), order.lines(), order.createdAt())
            .withDiscount(discount);
    }
}
```

### Functional Core, Imperative Shell (Java)
```java
// SHELL: Handles I/O, orchestrates
@Service
public class OrderService {
    private final OrderRepository repo;
    private final CustomerRepository customerRepo;

    public OrderResult processOrder(OrderId id) {
        // Fetch (I/O)
        var order = repo.findById(id).orElseThrow();
        var customer = customerRepo.findById(order.customer()).orElseThrow();

        // Transform (pure) - delegate to functional core
        var discount = PricingRules.calculateDiscount(order, customer.tier());
        var processed = OrderProcessor.process(order, discount);

        // Persist (I/O)
        repo.save(processed);
        return OrderResult.success(processed);
    }
}

// CORE: Pure business logic, trivially testable
public class OrderProcessor {
    public static ProcessedOrder process(Order order, Money discount) {
        var finalTotal = order.total().subtract(discount);
        var status = finalTotal.isZero() ? OrderStatus.FREE : OrderStatus.PENDING_PAYMENT;
        return new ProcessedOrder(order, discount, finalTotal, status);
    }
}
```

### Railway-Oriented Programming with Either (dk.oister.util)
```java
import dk.oister.util.Either;
import dk.oister.util.Eithers;

// Composable error handling - Left = error, Right = success
public Either<OrderError, ProcessedOrder> processOrder(OrderRequest request) {
    return validateRequest(request)
        .flatMap(this::createOrder)
        .flatMap(this::applyPricing)
        .map(this::toProcessedOrder);
}

// Pattern matching with fold
public ResponseEntity<?> handleOrder(OrderRequest request) {
    return processOrder(request).fold(
        error -> ResponseEntity.badRequest().body(error.message()),
        order -> ResponseEntity.ok(order)
    );
}

// Safe exception handling
public Either<OrderError, Order> fetchOrder(OrderId id) {
    return Either.fromTryCatch(
        () -> orderRepo.findById(id).orElseThrow(),
        ex -> new OrderError("Order not found: " + id)
    );
}

// Batch processing - fail fast or collect all errors
public Either<OrderError, List<Order>> processAll(List<OrderRequest> requests) {
    return requests.stream()
        .map(this::processOrder)
        .collect(Eithers.firstFailure());  // or allFailures() for validation
}

// Collecting all validation errors
public Either<List<ValidationError>, Order> validateOrder(OrderRequest req) {
    return Stream.of(
        validateCustomer(req),
        validateItems(req),
        validatePayment(req)
    ).collect(Eithers.allFailures())
     .map(results -> buildOrder(req));
}
```

---

## Property-Based Testing (jqwik)

### When to Use Property Tests
| Use Property Tests | Use Example Tests |
|-------------------|-------------------|
| Pure functions | Side effects (DB, HTTP) |
| Validation logic | Specific business scenarios |
| Parsers/serializers | Integration flows |
| Mathematical properties | Small enumerable cases |

### Property Patterns

#### Invariants
```java
@Property
void orderTotalAlwaysEqualsLineSum(@ForAll("orders") Order order) {
    var lineSum = order.lines().stream()
        .map(OrderLine::total)
        .reduce(Money.ZERO, Money::add);
    assertThat(order.total()).isEqualTo(lineSum);
}

@Property
void discountNeverExceedsSubtotal(@ForAll("orders") Order order,
                                   @ForAll CustomerTier tier) {
    var discount = PricingRules.calculateDiscount(order, tier);
    assertThat(discount).isLessThanOrEqualTo(order.total());
}
```

#### Round-Trip / Symmetry
```java
@Property
void serializeDeserializeIsIdentity(@ForAll("orders") Order order) {
    var json = mapper.writeValueAsString(order);
    var restored = mapper.readValue(json, Order.class);
    assertThat(restored).isEqualTo(order);
}
```

#### Idempotence
```java
@Property
void normalizationIsIdempotent(@ForAll String input) {
    var once = StringUtils.normalize(input);
    var twice = StringUtils.normalize(once);
    assertThat(twice).isEqualTo(once);
}
```

### Custom Arbitraries
```java
@Provide
Arbitrary<Order> orders() {
    return Combinators.combine(
        Arbitraries.longs().map(OrderId::new),
        Arbitraries.longs().map(CustomerId::new),
        Arbitraries.lists(orderLines()).ofMinSize(1).ofMaxSize(10),
        Arbitraries.longs().map(Instant::ofEpochMilli)
    ).as(Order::new);
}

@Provide
Arbitrary<OrderLine> orderLines() {
    return Combinators.combine(
        Arbitraries.longs().map(ProductId::new),
        Arbitraries.integers().between(1, 100),
        Arbitraries.integers().between(1, 10000).map(Money::ofCents)
    ).as(OrderLine::new);
}

@Provide
Arbitrary<String> danishCprs() {
    return Combinators.combine(
        Arbitraries.integers().between(1, 31),
        Arbitraries.integers().between(1, 12),
        Arbitraries.integers().between(0, 99),
        Arbitraries.integers().between(0, 9999)
    ).as((d, m, y, s) -> String.format("%02d%02d%02d-%04d", d, m, y, s));
}
```

---

## Next.js/TypeScript Patterns

### Discriminated Unions with ts-pattern
```typescript
// Domain state modeling - exhaustive, type-safe
type OrderState =
  | { status: 'draft'; items: OrderItem[] }
  | { status: 'submitted'; items: OrderItem[]; submittedAt: Date }
  | { status: 'paid'; items: OrderItem[]; paidAt: Date; transactionId: string }
  | { status: 'failed'; error: string };

// Exhaustive pattern matching - compiler error if case missed
import { match, P } from 'ts-pattern';

const handleOrder = (order: OrderState): string =>
  match(order)
    .with({ status: 'draft' }, ({ items }) => `Draft with ${items.length} items`)
    .with({ status: 'submitted' }, ({ submittedAt }) => `Submitted at ${submittedAt}`)
    .with({ status: 'paid' }, ({ transactionId }) => `Paid: ${transactionId}`)
    .with({ status: 'failed' }, ({ error }) => `Failed: ${error}`)
    .exhaustive();

// Railway-oriented error handling
type Result<T, E = string> =
  | { ok: true; value: T }
  | { ok: false; error: E };

const processOrder = (input: unknown): Result<Order> =>
  match(validateInput(input))
    .with({ ok: true }, ({ value }) => applyPricing(value))
    .with({ ok: false }, (err) => err)
    .exhaustive();

// Pattern matching with guards
const getDiscount = (customer: Customer): number =>
  match(customer)
    .with({ tier: 'gold', ordersCount: P.number.gte(10) }, () => 20)
    .with({ tier: 'gold' }, () => 15)
    .with({ tier: 'silver' }, () => 10)
    .otherwise(() => 0);
```

### Database Operations
- Extract query logic from business logic
- Pass query results as data to pure functions
- Return data structures describing what to persist
- Test business logic with plain objects, not DB mocks

### API Integrations
- Separate API calling from response processing
- Make response processing pure functions
- Use ports and adapters pattern
- Test response handling with fixture data

### State Management (Zustand)
- Keep store actions thin - orchestrate, don't contain logic
- Extract business logic into pure functions
- Test state transitions as pure: `(state, action) => newState`

### Next.js API Routes
```typescript
// Minimal logic in route handlers
// Extract request validation into pure functions
// Route handlers: parse -> call service -> format response

export async function POST(req: Request) {
    const body = await req.json();

    // Pure validation
    const validated = validateOrderRequest(body);
    if (!validated.success) return Response.json(validated.error, { status: 400 });

    // Call service (I/O boundary)
    const result = await orderService.create(validated.data);

    // Pure response formatting
    return Response.json(formatOrderResponse(result));
}
```

### React Components
- Separate presentation from logic
- Extract complex logic into custom hooks or utility functions
- Test logic independently from rendering
- Use component testing only for integration

---

## Property Testing Patterns

### Identify Properties

1. **Invariants**: Always true
   - "Total price = sum of line items"
   - "End date > start date"

2. **Inverse Operations**: Cancel each other
   - "serialize -> deserialize -> serialize = same"

3. **Idempotence**: Repeatable safely
   - "Apply discount twice = apply once"

4. **Commutativity**: Order-independent
   - "Add items in any order = same total"

---

## Output Format

### Executive Summary
- Overall architectural assessment (1-2 sentences)
- Testability score (% easily unit testable)
- Top 3 improvement priorities

### Detailed Analysis
For each concern:
- **Issue**: What makes this hard to test?
- **Impact**: Why does it matter?
- **Root Cause**: What architectural decision led here?

### Refactoring Recommendations
For each recommendation:
- **Pattern**: Architectural pattern to apply
- **Transformation**: Step-by-step approach
- **Code Structure**: Resulting architecture
- **Test Strategy**: Unit + property tests
- **Benefits**: Testability improvement

### Testing Strategy
- **Unit Tests**: What to test, coverage expectations
- **Property Tests**: Properties to verify
- **Edge Tests**: Minimal integration tests
- **Test Examples**: Concrete test cases

### Metrics
- Estimated mocking reduction
- Projected pure function percentage increase
- Complexity reduction indicators

---

## Quality Standards

- **Be Specific**: Concrete code examples, not abstract advice
- **Prioritize**: Rank by testability impact
- **Pragmatic**: Balance ideal architecture with practical effort
- **Educational**: Explain the "why"
- **Actionable**: Clear next steps

---

## Context Awareness

### Next.js/TypeScript Stack
- Zustand for state management
- Knex.js for database access
- Chakra UI components
- NextAuth for authentication
- Mocha for unit tests

### Java/Spring Boot Stack
- Java 21+ (records, sealed types, pattern matching)
- Spring Boot 3.x
- JUnit 5 + jqwik for property tests
- AssertJ for assertions
- Constructor injection, immutable designs
- Data-oriented programming patterns

Tailor recommendations to the detected stack while maximizing testability through pure functions and minimal mocking.
