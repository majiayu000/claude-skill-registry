---
name: spring-boot-dependency-injection
description: Dependency injection workflow for Spring Boot projects covering constructor-first patterns, optional collaborator handling, bean selection, and validation practices.
allowed-tools: Read, Write, Bash
category: backend
tags: [spring-boot, dependency-injection, constructor-injection, bean-configuration, autowiring, testing, java]
version: 1.1.0
context7_library: /spring-projects/spring-framework
context7_trust_score: 9.0
---

# Spring Boot Dependency Injection

This skill captures the dependency injection approach promoted in this repository: constructor-first design, explicit optional collaborators, and deterministic configuration that keeps services testable and framework-agnostic.

## Overview

- Prioritize constructor injection to keep dependencies explicit, immutable, and mockable.
- Treat optional collaborators through guarded setters or providers while documenting defaults.
- Resolve bean ambiguity intentionally through qualifiers, primary beans, and profiles.
- Validate wiring with focused unit tests before relying on Spring's TestContext framework.

## When to Use

- Implement constructor injection for new `@Service`, `@Component`, or `@Repository` classes.
- Replace legacy field injection while modernizing Spring modules.
- Configure optional or pluggable collaborators (feature flags, multi-tenant adapters).
- Audit bean definitions before adding integration tests or migrating Spring Boot versions.

## Prerequisites

- Align project with Java 17+ and Spring Boot 3.5.x (or later) to leverage records and `@ServiceConnection`.
- Keep build tooling ready to run `./gradlew test` or `mvn test` for validation.
- Load supporting material from `./references/` when deeper patterns or samples are required.

## Workflow

### 1. Map Collaborators
- Inventory constructors, `@Autowired` members, and configuration classes.
- Classify dependencies as mandatory (must exist) or optional (feature-flagged, environment-specific).

### 2. Apply Constructor Injection
- Introduce constructors (or Lombok `@RequiredArgsConstructor`) that accept every mandatory collaborator.
- Mark injected fields `final` and protect invariants with `Objects.requireNonNull` if Lombok is not used.
- Update `@Configuration` or `@Bean` factories to pass dependencies explicitly; consult `./references/reference.md` for canonical bean wiring.

### 3. Handle Optional Collaborators
- Supply setters annotated with `@Autowired(required = false)` or inject `ObjectProvider<T>` for lazy access.
- Provide deterministic defaults (for example, no-op implementations) and document them inside configuration modules.
- Follow `./references/examples.md#example-2-setter-injection-for-optional-dependencies` for a full workflow.

### 4. Resolve Bean Selection
- Choose `@Primary` for dominant implementations and `@Qualifier` for niche variants.
- Use profiles, conditional annotations, or factory methods to isolate environment-specific wiring.
- Reference `./references/reference.md#conditional-bean-registration` for conditional and profile-based samples.

### 5. Validate Wiring
- Write unit tests that instantiate classes manually with mocks to prove Spring-free testability.
- Add slice or integration tests (`@WebMvcTest`, `@DataJpaTest`, `@SpringBootTest`) only after constructor contracts are validated.
- Reuse patterns in `./references/reference.md#testing-with-dependency-injection` to select the proper test style.

## Examples

### Basic Constructor Injection
```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;

    public User register(UserRegistrationRequest request) {
        User user = User.create(request.email(), request.name());
        userRepository.save(user);
        emailService.sendWelcome(user);
        return user;
    }
}
```
- Instantiate directly in tests: `new UserService(mockRepo, mockEmailService);` with no Spring context required.

### Intermediate: Optional Dependency with Guarded Setter
```java
@Service
public class ReportService {
    private final ReportRepository reportRepository;
    private CacheService cacheService = CacheService.noOp();

    public ReportService(ReportRepository reportRepository) {
        this.reportRepository = reportRepository;
    }

    @Autowired(required = false)
    public void setCacheService(CacheService cacheService) {
        this.cacheService = cacheService;
    }
}
```
- Provide fallbacks such as `CacheService.noOp()` to ensure deterministic behavior when the optional bean is absent.

### Advanced: Conditional Configuration Across Modules
```java
@Configuration
@Import(DatabaseConfig.class)
public class MessagingConfig {

    @Bean
    @ConditionalOnProperty(name = "feature.notifications.enabled", havingValue = "true")
    public NotificationService emailNotificationService(JavaMailSender sender) {
        return new EmailNotificationService(sender);
    }

    @Bean
    @ConditionalOnMissingBean(NotificationService.class)
    public NotificationService noopNotificationService() {
        return NotificationService.noOp();
    }
}
```
- Combine `@Import`, profiles, and conditional annotations to orchestrate cross-cutting modules.

Additional worked examples (including tests and configuration wiring) are available in `./references/examples.md`.

## Best Practices

- Prefer constructor injection for mandatory dependencies; allow Spring 4.3+ to infer `@Autowired` on single constructors.
- Encapsulate optional behavior inside dedicated adapters or providers instead of accepting `null` pointers.
- Keep service constructors lightweight; extract orchestrators when dependency counts exceed four.
- Favor domain interfaces in the domain layer and defer framework imports to infrastructure adapters.
- Document bean names and qualifiers in shared constants to avoid typo-driven mismatches.

## Constraints
 
- Avoid field injection and service locator patterns because they obscure dependencies and impede unit testing.
- Prevent circular dependencies by publishing domain events or extracting shared abstractions.
- Limit `@Lazy` usage to performance-sensitive paths and record the deferred initialization risk.
- Do not add profile-specific beans without matching integration tests that activate the profile.
- Ensure each optional collaborator has a deterministic default or feature-flag handling path.

## Reference Materials

- [extended documentation covering annotations, bean scopes, testing, and anti-pattern mitigations](references/reference.md)
- [progressive examples from constructor injection basics to multi-module configurations](references/examples.md)
- [curated excerpts from the official Spring Framework documentation (constructor vs setter guidance, conditional wiring)](references/spring-official-dependency-injection.md)

## Related Skills

- `spring-boot-crud-patterns` – service-layer orchestration patterns that rely on constructor injection.
- `spring-boot-rest-api-standards` – controller-layer practices that assume explicit dependency wiring.
- `unit-test-service-layer` – Mockito-based testing patterns for constructor-injected services.
