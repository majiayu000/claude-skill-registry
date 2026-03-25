---
name: spring-boot-dependency-injection
description: Provides dependency injection patterns for Spring Boot projects, including constructor-first design, optional collaborator handling, bean selection, and wiring validation. Use when creating services and configurations, replacing field injection, or troubleshooting ambiguous or fragile Spring wiring.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Spring Boot Dependency Injection

## Overview

Provides constructor-first dependency injection patterns for Spring Boot:
- mandatory collaborators via constructor injection
- optional collaborators via `ObjectProvider` or no-op fallbacks
- bean selection via `@Primary` and `@Qualifier`
- validation via minimal context tests before full integration

## When to Use

Use this skill when:
- creating a new `@Service`, `@Component`, `@Repository`, or `@Configuration` class
- replacing field injection in legacy Spring code
- resolving multiple beans of the same type with qualifiers or primary beans
- handling optional features, adapters, or integrations without null-driven wiring
- reviewing circular dependencies or brittle context startup failures
- preparing code for direct constructor-based unit testing


## Instructions

### 1. Separate mandatory and optional collaborators

For each class, identify:
- mandatory collaborators required for correct behavior
- optional collaborators that enable integrations, caching, notifications, or feature-flagged behavior

Mandatory collaborators belong in the constructor. Optional ones need an explicit strategy such as `ObjectProvider`, conditional beans, or a no-op implementation.

### 2. Default to constructor injection

For application services and adapters:
- inject mandatory dependencies through the constructor
- keep injected fields `final`
- instantiate the class directly in unit tests without starting Spring

A single constructor is usually enough; `@Autowired` is unnecessary in that case.

### 3. Resolve optional behavior intentionally

Good options include:
- `ObjectProvider<T>` when lazy access is useful
- `@ConditionalOnProperty` or `@ConditionalOnMissingBean` when wiring should change by configuration
- a no-op implementation when the caller should not care whether the feature is enabled

Avoid nullable collaborators that leave runtime behavior ambiguous.

### 4. Use bean selection annotations only when needed

When multiple beans share the same type:
- use `@Primary` for the default implementation
- use `@Qualifier` for named variants
- keep the qualifier names stable and easy to grep

If selection rules become complex, move them into a dedicated configuration class instead of spreading them across services.

### 5. Keep wiring in configuration, not business code

Use `@Configuration` and `@Bean` methods when:
- the object comes from a third-party library
- conditional creation logic is needed
- you need environment-specific wiring or explicit composition

Business services should not know how infrastructure collaborators are instantiated.

### 6. Validate wiring explicitly

After writing a new service or configuration:

1. **Verify the bean loads** with a minimal context test:
   ```java
   @SpringBootTest
   @ContextConfiguration(classes = UserService.class)
   class UserServiceWiringTest {
       @Autowired UserService userService;
       @Test void serviceIsInstantiated() { assertNotNull(userService); }
   }
   ```
2. **Run constructor-based unit tests** for service behavior (no Spring needed).
3. **Add slice tests** only when MVC, JPA, or messaging integration must be verified.
4. **Reserve `@SpringBootTest`** for container-wide wiring validation.

Failures at step 1 indicate wiring issues before business logic is added.

## Examples

### Example 1: Constructor-first application service

```java
@Service
public class UserService {

    private final UserRepository userRepository;
    private final EmailSender emailSender;

    public UserService(UserRepository userRepository, EmailSender emailSender) {
        this.userRepository = userRepository;
        this.emailSender = emailSender;
    }

    public User register(UserRegistrationRequest request) {
        User user = userRepository.save(User.from(request));
        emailSender.sendWelcome(user);
        return user;
    }
}
```

This class is easy to instantiate directly in a unit test with mocks.

### Example 2: Optional dependency with a no-op fallback

```java
@Service
public class ReportService {

    private final ReportRepository reportRepository;
    private final NotificationGateway notificationGateway;

    public ReportService(
        ReportRepository reportRepository,
        ObjectProvider<NotificationGateway> notificationGatewayProvider
    ) {
        this.reportRepository = reportRepository;
        this.notificationGateway = notificationGatewayProvider.getIfAvailable(NotificationGateway::noOp);
    }
}
```

This keeps optional behavior explicit without leaking `null` handling through the rest of the class.

### Example 3: Multiple beans with clear selection

```java
@Configuration
public class PaymentConfiguration {

    @Bean
    @Primary
    PaymentGateway stripeGateway() {
        return new StripePaymentGateway();
    }

    @Bean
    @Qualifier("fallbackGateway")
    PaymentGateway mockGateway() {
        return new MockPaymentGateway();
    }
}
```

Use `@Primary` for the default path and `@Qualifier` only where a specific variant is required.

## Best Practices

- Prefer constructor injection for mandatory dependencies.
- Keep service constructors small; if a class needs too many collaborators, the design probably wants another abstraction.
- Use no-op or conditional beans instead of nullable optional dependencies.
- Keep framework-specific creation logic in configuration classes.
- Test services without Spring first, then add container tests only where they add value.
- Remove field injection during refactors instead of extending it.

## Constraints and Warnings

- Field injection hides dependencies and makes tests harder to write.
- Circular dependencies are usually a design problem, not a wiring trick to solve with `@Lazy`.
- Overusing qualifiers can make the codebase hard to reason about; prefer better abstractions or clearer configuration.
- Optional collaborators still need deterministic behavior when absent.
- Full-context tests can hide the real source of wiring failures if used too early.

## References

- `references/reference.md`
- `references/examples.md`
- `references/spring-official-dependency-injection.md`

## Related Skills

- `spring-boot-crud-patterns`
- `spring-boot-rest-api-standards`
- `unit-test-service-layer`
