---
name: spring-boot-patterns
description: >
  Spring Boot patterns including stereotype annotations, dependency injection, profiles,
  configuration properties, and actuator endpoints. Use when the user is building Spring Boot
  applications, configuring dependency injection, setting up profiles for different environments,
  using @ConfigurationProperties, or enabling actuator health checks. Trigger on any mention
  of Spring Boot, @Component, @Service, @Repository, Spring DI, Spring profiles, or actuator.
---

# Spring Boot Patterns

Core patterns for building production-ready Spring Boot applications.

## When to Use
- User is setting up a Spring Boot project
- User asks about @Component, @Service, @Repository usage
- User needs dependency injection patterns
- User is configuring profiles for dev/staging/prod
- User asks about externalized configuration or actuator

## Core Patterns

### Stereotype Annotations -- Layer Separation

Use the correct annotation for each architectural layer. Spring applies different behaviors to each.

```java
@Repository  // Data access -- translates persistence exceptions
public class UserRepository {
    private final JdbcTemplate jdbc;
    public UserRepository(JdbcTemplate jdbc) { this.jdbc = jdbc; }

    public Optional<User> findById(Long id) {
        return jdbc.query("SELECT * FROM users WHERE id = ?",
            new BeanPropertyRowMapper<>(User.class), id).stream().findFirst();
    }
}

@Service  // Business logic -- transactional boundaries live here
public class UserService {
    private final UserRepository userRepository;
    public UserService(UserRepository userRepository) { this.userRepository = userRepository; }

    @Transactional
    public User createUser(CreateUserRequest request) {
        return userRepository.save(new User(request.name(), request.email()));
    }
}

@RestController  // Web layer -- handles HTTP requests
@RequestMapping("/api/v1/users")
public class UserController {
    private final UserService userService;
    public UserController(UserService userService) { this.userService = userService; }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse createUser(@Valid @RequestBody CreateUserRequest request) {
        return UserResponse.from(userService.createUser(request));
    }
}
```

### Constructor Injection

Always use constructor injection. It makes dependencies explicit, supports immutability, and works with final fields. Avoid field injection with @Autowired.

```java
@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentGateway paymentGateway;
    private final NotificationService notificationService;

    // Single constructor -- @Autowired is implicit, no annotation needed
    public OrderService(
            OrderRepository orderRepository,
            PaymentGateway paymentGateway,
            NotificationService notificationService) {
        this.orderRepository = orderRepository;
        this.paymentGateway = paymentGateway;
        this.notificationService = notificationService;
    }
}
```

### Profiles -- Environment-Specific Configuration

Use profiles to swap implementations and configuration per environment.

```yaml
# application.yml -- shared defaults
spring:
  application:
    name: my-service

---
# application-dev.yml
spring:
  datasource:
    url: jdbc:h2:mem:devdb
    driver-class-name: org.h2.Driver
  jpa:
    show-sql: true

---
# application-prod.yml
spring:
  datasource:
    url: jdbc:postgresql://${DB_HOST}:5432/${DB_NAME}
    username: ${DB_USER}
    password: ${DB_PASSWORD}
  jpa:
    show-sql: false
```

Profile-specific beans:

```java
@Configuration
public class StorageConfig {

    @Bean
    @Profile("dev")
    public StorageService localStorageService() {
        return new LocalFileStorageService("/tmp/uploads");
    }

    @Bean
    @Profile("prod")
    public StorageService s3StorageService(S3Client s3Client) {
        return new S3StorageService(s3Client);
    }
}
```

### @ConfigurationProperties -- Type-Safe Configuration

Bind external configuration to strongly-typed POJOs. Prefer this over scattered @Value annotations.

```java
@ConfigurationProperties(prefix = "app.mail")
public record MailProperties(
    String host,
    int port,
    String fromAddress,
    Duration timeout,
    RetryProperties retry
) {
    public record RetryProperties(int maxAttempts, Duration delay) {}
}
```

```yaml
app:
  mail:
    host: smtp.example.com
    port: 587
    from-address: noreply@example.com
    timeout: 5s
    retry:
      max-attempts: 3
      delay: 2s
```

Enable it:
```java
@SpringBootApplication
@EnableConfigurationProperties(MailProperties.class)
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### Actuator -- Production Monitoring

Expose health checks, metrics, and application info for monitoring systems.

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when-authorized
  health:
    db:
      enabled: true
    redis:
      enabled: true
```

Custom health indicator:

```java
@Component
public class PaymentGatewayHealthIndicator implements HealthIndicator {
    private final PaymentGateway gateway;
    public PaymentGatewayHealthIndicator(PaymentGateway gateway) { this.gateway = gateway; }

    @Override
    public Health health() {
        try {
            return gateway.ping()
                ? Health.up().withDetail("gateway", "reachable").build()
                : Health.down().withDetail("gateway", "unreachable").build();
        } catch (Exception e) { return Health.down(e).build(); }
    }
}
```

## Anti-Patterns

- **Field injection with @Autowired** -- Makes dependencies hidden, prevents immutability, and breaks testing. Use constructor injection instead.
- **Business logic in controllers** -- Controllers should only handle HTTP concerns (request parsing, response formatting). Delegate to services.
- **Catching all exceptions in controllers** -- Use `@ControllerAdvice` with `@ExceptionHandler` for centralized exception handling.
- **Using @Component for everything** -- Use the specific stereotype (@Service, @Repository, @Controller) so Spring applies the correct behavior (transaction proxies, exception translation).
- **Hardcoding configuration values** -- Use @ConfigurationProperties or environment variables. Never hardcode URLs, credentials, or environment-specific values.

## Quick Reference

```
Stereotype annotations:
  @Component    -- Generic Spring-managed bean
  @Service      -- Business logic layer
  @Repository   -- Data access layer (exception translation)
  @Controller   -- Web layer (returns views)
  @RestController -- Web layer (returns JSON)

Configuration:
  @ConfigurationProperties  -- Type-safe config binding
  @Value("${key}")         -- Single value injection
  @Profile("dev")          -- Environment-specific bean

Actuator endpoints:
  /actuator/health    -- Application health
  /actuator/info      -- Application info
  /actuator/metrics   -- Micrometer metrics
  /actuator/prometheus -- Prometheus-format metrics
```
