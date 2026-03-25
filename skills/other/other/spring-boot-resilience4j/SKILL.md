---
name: spring-boot-resilience4j
description: Provides fault tolerance patterns for Spring Boot 3.x using Resilience4j. Use when implementing circuit breakers, handling service failures, adding retry logic with exponential backoff, configuring rate limiters, or protecting services from cascading failures. Generates circuit breaker, retry, rate limiter, bulkhead, time limiter, and fallback implementations. Validates resilience configurations through Actuator endpoints.
allowed-tools: Read, Write, Edit, Bash
---

# Spring Boot Resilience4j Patterns

## Overview

Provides Resilience4j patterns (circuit breaker, retry, rate limiter, bulkhead, time limiter, fallback) for Spring Boot 3.x fault tolerance with configuration and testing workflows.

## When to Use

- Implementing fault tolerance and preventing cascading failures
- Adding circuit breakers, retry logic, or rate limiting to service calls
- Handling transient failures with exponential backoff
- Protecting services from overload and resource exhaustion
- Combining multiple patterns for comprehensive resilience

## Instructions

### 1. Setup and Dependencies

Add Resilience4j dependencies to your project. For Maven, add to `pom.xml`:

```xml
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-spring-boot3</artifactId>
    <version>2.2.0</version> // Use latest stable version
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

For Gradle, add to `build.gradle`:

```gradle
implementation "io.github.resilience4j:resilience4j-spring-boot3:2.2.0"
implementation "org.springframework.boot:spring-boot-starter-aop"
implementation "org.springframework.boot:spring-boot-starter-actuator"
```

Enable AOP annotation processing with `@EnableAspectJAutoProxy` (auto-configured by Spring Boot).

### 2. Circuit Breaker Pattern

Apply `@CircuitBreaker` annotation to methods calling external services:

```java
@Service
public class PaymentService {
    private final RestTemplate restTemplate;

    public PaymentService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
    public PaymentResponse processPayment(PaymentRequest request) {
        return restTemplate.postForObject("http://payment-api/process",
            request, PaymentResponse.class);
    }

    private PaymentResponse paymentFallback(PaymentRequest request, Exception ex) {
        return PaymentResponse.builder()
            .status("PENDING")
            .message("Service temporarily unavailable")
            .build();
    }
}
```

Configure in `application.yml`:

```yaml
resilience4j:
  circuitbreaker:
    configs:
      default:
        registerHealthIndicator: true
        slidingWindowSize: 10
        minimumNumberOfCalls: 5
        failureRateThreshold: 50
        waitDurationInOpenState: 10s
    instances:
      paymentService:
        baseConfig: default
```

See @references/configuration-reference.md for complete circuit breaker configuration options.

### 3. Retry Pattern

Apply `@Retry` annotation for transient failure recovery:

```java
@Service
public class ProductService {
    private final RestTemplate restTemplate;

    public ProductService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @Retry(name = "productService", fallbackMethod = "getProductFallback")
    public Product getProduct(Long productId) {
        return restTemplate.getForObject(
            "http://product-api/products/" + productId,
            Product.class);
    }

    private Product getProductFallback(Long productId, Exception ex) {
        return Product.builder()
            .id(productId)
            .name("Unavailable")
            .available(false)
            .build();
    }
}
```

Configure retry in `application.yml`:

```yaml
resilience4j:
  retry:
    configs:
      default:
        maxAttempts: 3
        waitDuration: 500ms
        enableExponentialBackoff: true
        exponentialBackoffMultiplier: 2
    instances:
      productService:
        baseConfig: default
        maxAttempts: 5
```

See @references/configuration-reference.md for retry exception configuration.

### 4. Rate Limiter Pattern

Apply `@RateLimiter` to control request rates:

```java
@Service
public class NotificationService {
    private final EmailClient emailClient;

    public NotificationService(EmailClient emailClient) {
        this.emailClient = emailClient;
    }

    @RateLimiter(name = "notificationService",
        fallbackMethod = "rateLimitFallback")
    public void sendEmail(EmailRequest request) {
        emailClient.send(request);
    }

    private void rateLimitFallback(EmailRequest request, Exception ex) {
        throw new RateLimitExceededException(
            "Too many requests. Please try again later.");
    }
}
```

Configure in `application.yml`:

```yaml
resilience4j:
  ratelimiter:
    configs:
      default:
        registerHealthIndicator: true
        limitForPeriod: 10
        limitRefreshPeriod: 1s
        timeoutDuration: 500ms
    instances:
      notificationService:
        baseConfig: default
        limitForPeriod: 5
```

### 5. Bulkhead Pattern

Apply `@Bulkhead` to isolate resources. Use `type = SEMAPHORE` for synchronous methods:

```java
@Service
public class ReportService {
    private final ReportGenerator reportGenerator;

    public ReportService(ReportGenerator reportGenerator) {
        this.reportGenerator = reportGenerator;
    }

    @Bulkhead(name = "reportService", type = Bulkhead.Type.SEMAPHORE)
    public Report generateReport(ReportRequest request) {
        return reportGenerator.generate(request);
    }
}
```

Use `type = THREADPOOL` for async/CompletableFuture methods:

```java
@Service
public class AnalyticsService {
    @Bulkhead(name = "analyticsService", type = Bulkhead.Type.THREADPOOL)
    public CompletableFuture<AnalyticsResult> runAnalytics(
            AnalyticsRequest request) {
        return CompletableFuture.supplyAsync(() ->
            analyticsEngine.analyze(request));
    }
}
```

Configure in `application.yml`:

```yaml
resilience4j:
  bulkhead:
    configs:
      default:
        maxConcurrentCalls: 10
        maxWaitDuration: 100ms
    instances:
      reportService:
        baseConfig: default
        maxConcurrentCalls: 5

  thread-pool-bulkhead:
    instances:
      analyticsService:
        maxThreadPoolSize: 8
```

### 6. Time Limiter Pattern

Apply `@TimeLimiter` to async methods to enforce timeout boundaries:

```java
@Service
public class SearchService {
    @TimeLimiter(name = "searchService", fallbackMethod = "searchFallback")
    public CompletableFuture<SearchResults> search(SearchQuery query) {
        return CompletableFuture.supplyAsync(() ->
            searchEngine.executeSearch(query));
    }

    private CompletableFuture<SearchResults> searchFallback(
            SearchQuery query, Exception ex) {
        return CompletableFuture.completedFuture(
            SearchResults.empty("Search timed out"));
    }
}
```

Configure in `application.yml`:

```yaml
resilience4j:
  timelimiter:
    configs:
      default:
        timeoutDuration: 2s
        cancelRunningFuture: true
    instances:
      searchService:
        baseConfig: default
        timeoutDuration: 3s
```

### 7. Combining Multiple Patterns

Stack multiple patterns on a single method for comprehensive fault tolerance:

```java
@Service
public class OrderService {
    @CircuitBreaker(name = "orderService")
    @Retry(name = "orderService")
    @RateLimiter(name = "orderService")
    @Bulkhead(name = "orderService")
    public Order createOrder(OrderRequest request) {
        return orderClient.createOrder(request);
    }
}
```

Execution order: Retry → CircuitBreaker → RateLimiter → Bulkhead → Method

All patterns should reference the same named configuration instance for consistency.

### 8. Exception Handling and Monitoring

Create a global exception handler using `@RestControllerAdvice`:

```java
@RestControllerAdvice
public class ResilienceExceptionHandler {

    @ExceptionHandler(CallNotPermittedException.class)
    @ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
    public ErrorResponse handleCircuitOpen(CallNotPermittedException ex) {
        return new ErrorResponse("SERVICE_UNAVAILABLE",
            "Service currently unavailable");
    }

    @ExceptionHandler(RequestNotPermitted.class)
    @ResponseStatus(HttpStatus.TOO_MANY_REQUESTS)
    public ErrorResponse handleRateLimited(RequestNotPermitted ex) {
        return new ErrorResponse("TOO_MANY_REQUESTS",
            "Rate limit exceeded");
    }

    @ExceptionHandler(BulkheadFullException.class)
    @ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
    public ErrorResponse handleBulkheadFull(BulkheadFullException ex) {
        return new ErrorResponse("CAPACITY_EXCEEDED",
            "Service at capacity");
    }
}
```

Enable Actuator endpoints for monitoring resilience patterns in `application.yml`:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,circuitbreakers,retries,ratelimiters
  endpoint:
    health:
      show-details: always
  health:
    circuitbreakers:
      enabled: true
    ratelimiters:
      enabled: true
```

Access monitoring endpoints:
- `GET /actuator/health` - Overall health including resilience patterns
- `GET /actuator/circuitbreakers` - Circuit breaker states
- `GET /actuator/metrics` - Custom resilience metrics

### Testing & Verification Workflow

1. **Circuit Breaker**: Call endpoint with failures → check `GET /actuator/circuitbreakers` shows `OPEN` → wait `waitDurationInOpenState` → verify state transitions to `HALF_OPEN` → `CLOSED`

2. **Retry**: Enable `resilience4j.retry.metrics.enabled: true` → invoke endpoint → verify `retry.{instance}.successful-calls-with-retry-attempts` metric increases

3. **Rate Limiter**: Send requests exceeding `limitForPeriod` → verify 429 status → check `GET /actuator/ratelimiters` shows `LIMITED`

4. **Bulkhead**: Load test with concurrent requests exceeding `maxConcurrentCalls` → verify excess requests fail immediately with `BulkheadFullException`

5. **Time Limiter**: Mock async delay beyond `timeoutDuration` → verify fallback triggers after timeout

See @references/testing-patterns.md for unit and integration testing strategies.

## Best Practices

- **Provide fallback methods**: Ensure graceful degradation with meaningful responses
- **Use exponential backoff**: Prevent overwhelming recovering services (`exponentialBackoffMultiplier: 2`)
- **Set appropriate thresholds**: `failureRateThreshold` between 50-70%
- **Use constructor injection**: Never use field injection for Resilience4j dependencies
- **Enable health indicators**: Set `registerHealthIndicator: true` for all patterns
- **Retry only transient errors**: Network timeouts, 5xx; skip 4xx and business exceptions
- **Size bulkheads based on load**: Calculate thread pool and semaphore sizes from expected concurrency
- **Document fallback behavior**: Make fallback logic clear and predictable

## Constraints and Warnings

- Fallback methods must have the same signature plus an optional exception parameter
- Circuit breaker state is per-instance; ensure proper bean scoping in multi-tenant scenarios
- Retry operations must be idempotent (may execute multiple times)
- Do not use circuit breakers for operations that must always complete; use timeouts instead
- Rate limiters can cause thread blocking; configure appropriate wait durations
- Be cautious with `@Retry` on non-idempotent operations like POST requests
- Monitor memory when using thread pool bulkheads with high concurrency

## Examples

### Before → After: Circuit Breaker

```java
// BEFORE: No protection
public PaymentResponse processPayment(PaymentRequest request) {
    return restTemplate.postForObject("http://payment-api/process", request, PaymentResponse.class);
}

// AFTER: Circuit breaker with fallback
@CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
public PaymentResponse processPayment(PaymentRequest request) {
    return restTemplate.postForObject("http://payment-api/process", request, PaymentResponse.class);
}
private PaymentResponse paymentFallback(PaymentRequest request, Exception ex) {
    return PaymentResponse.builder().status("PENDING").message("Service temporarily unavailable").build();
}
```

### Before → After: Retry with Backoff

```java
// BEFORE: Single attempt
public Order getOrder(Long orderId) {
    return orderRepository.findById(orderId).orElseThrow(() -> new OrderNotFoundException(orderId));
}

// AFTER: Retry with exponential backoff
@Retry(name = "orderService", maxAttempts = 3, waitDuration = @WaitDuration(500L), fallbackMethod = "getOrderFallback")
public Order getOrder(Long orderId) {
    return orderRepository.findById(orderId).orElseThrow(() -> new OrderNotFoundException(orderId));
}
private Order getOrderFallback(Long orderId, Exception ex) { return Order.cachedOrder(orderId); }
```

### Before → After: Rate Limiting

```java
// BEFORE: Unbounded requests
@GetMapping("/api/data") public Data fetchData() { return dataService.process(); }

// AFTER: Rate limited
@RateLimiter(name = "dataService", fallbackMethod = "rateLimitFallback")
@GetMapping("/api/data") public Data fetchData() { return dataService.process(); }
private ResponseEntity<ErrorResponse> rateLimitFallback(Exception ex) {
    return ResponseEntity.status(429).body(new ErrorResponse("TOO_MANY_REQUESTS", "Rate limit exceeded"));
}
```

**See also:** [Configuration Reference](references/configuration-reference.md) · [Testing Patterns](references/testing-patterns.md) · [Examples](references/examples.md) · [Resilience4j Docs](https://resilience4j.readme.io/) · [Actuator Skill](../spring-boot-actuator/SKILL.md)
