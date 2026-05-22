---
name: spring-boot-resilience4j
description: This skill should be used when implementing fault tolerance and resilience patterns in Spring Boot applications using the Resilience4j library. Apply this skill to add circuit breaker, retry, rate limiter, bulkhead, time limiter, and fallback mechanisms to prevent cascading failures, handle transient errors, and manage external service dependencies gracefully in microservices architectures.
allowed-tools: Read, Write, Edit, Bash
category: backend
tags: [spring-boot, resilience4j, circuit-breaker, fault-tolerance, retry, bulkhead, rate-limiter]
version: 1.1.0
---

# Spring Boot Resilience4j Patterns

## When to Use

To implement resilience patterns in Spring Boot applications, use this skill when:
- Preventing cascading failures from external service unavailability with circuit breaker pattern
- Retrying transient failures with exponential backoff
- Rate limiting to protect services from overload or downstream service capacity constraints
- Isolating resources with bulkhead pattern to prevent thread pool exhaustion
- Adding timeout controls to async operations with time limiter
- Combining multiple patterns for comprehensive fault tolerance

Resilience4j is a lightweight, composable library for adding fault tolerance without requiring external infrastructure. It provides annotation-based patterns that integrate seamlessly with Spring Boot's AOP and Actuator.

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

## Best Practices

- **Always provide fallback methods**: Ensure graceful degradation with meaningful responses rather than exceptions
- **Use exponential backoff for retries**: Prevent overwhelming recovering services with aggressive backoff (`exponentialBackoffMultiplier: 2`)
- **Choose appropriate failure thresholds**: Set `failureRateThreshold` between 50-70% depending on acceptable error rates
- **Use constructor injection exclusively**: Never use field injection for Resilience4j dependencies
- **Enable health indicators**: Set `registerHealthIndicator: true` for all patterns to integrate with Spring Boot health
- **Separate failure vs. client errors**: Retry only transient errors (network timeouts, 5xx); skip 4xx and business exceptions
- **Size bulkheads based on load**: Calculate thread pool and semaphore sizes from expected concurrent load and latency
- **Monitor and adjust**: Continuously review metrics and adjust timeouts/thresholds based on production behavior
- **Document fallback behavior**: Make fallback logic clear and predictable to users and maintainers

## Common Mistakes

Refer to `references/testing-patterns.md` for:
- Testing circuit breaker state transitions
- Simulating transient failures with WireMock
- Validating fallback method signatures
- Avoiding common misconfiguration errors

Refer to `references/configuration-reference.md` for:
- Complete property reference for all patterns
- Configuration validation rules
- Exception handling configuration

## References and Examples

- [Complete property reference and configuration patterns](references/configuration-reference.md)
- [Unit and integration testing strategies](references/testing-patterns.md)
- [Real-world e-commerce service example using all patterns](references/examples.md)
- [Resilience4j Documentation](https://resilience4j.readme.io/)
- [Spring Boot Actuator Skill](/skills/spring-boot-actuator/SKILL.md) - Monitoring resilience patterns with Actuator
