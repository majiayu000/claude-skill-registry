---
name: java-cdi
description: Core CDI patterns including constructor injection, scopes, producers, and container configuration
allowed-tools: [Read, Edit, Write, Bash, Grep, Glob]
---

# Java CDI Skill

Core CDI (Contexts and Dependency Injection) standards applicable to any CDI container. This skill covers dependency injection patterns, scopes, and producer methods.

## Prerequisites

This skill applies to Jakarta CDI projects:
- `jakarta.inject:jakarta.inject-api`
- `jakarta.enterprise:jakarta.enterprise.cdi-api`

## Required Imports

```java
// CDI Core
import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;

// CDI Scopes
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.context.RequestScoped;
import jakarta.enterprise.context.SessionScoped;
import jakarta.enterprise.context.Dependent;

// CDI Producers and Optional Dependencies
import jakarta.enterprise.inject.Produces;
import jakarta.enterprise.inject.Instance;

// Quarkus Configuration
import org.eclipse.microprofile.config.inject.ConfigProperty;
```

## References

* [CDI 2.0 Specification](https://docs.oracle.com/javaee/7/tutorial/cdi-basic.htm)
* [Quarkus CDI Guide](https://quarkus.io/guides/cdi)

---

## Constructor Injection (Mandatory)

**REQUIRED**: Always use constructor injection instead of field injection.

For foundational constructor injection principles (immutability, testability, fail-fast behavior), see `pm-dev-java:java-core` skill.

### Single Constructor Rule

When a CDI bean has exactly **one constructor**, CDI automatically treats it as the injection point - no `@Inject` needed:

```java
@ApplicationScoped
public class OrderService {
    private final PaymentService paymentService;
    private final InventoryService inventoryService;

    // No @Inject needed - only one constructor
    public OrderService(PaymentService paymentService,
                       InventoryService inventoryService) {
        this.paymentService = paymentService;
        this.inventoryService = inventoryService;
    }
}
```

### Multiple Constructors Rule

When a CDI bean has **multiple constructors**, you **MUST** explicitly mark the injection constructor with `@Inject`:

```java
@ApplicationScoped
public class ConfigurableService {
    private final DatabaseService databaseService;
    private final String configValue;

    public ConfigurableService() {
        this.databaseService = null;
        this.configValue = "default";
    }

    @Inject  // REQUIRED - multiple constructors exist
    public ConfigurableService(DatabaseService databaseService,
                              @ConfigProperty(name = "app.config") String configValue) {
        this.databaseService = databaseService;
        this.configValue = configValue;
    }
}
```

### Anti-Patterns

```java
// ❌ Field Injection - FORBIDDEN
@Inject
private UserService userService;

// ❌ Setter Injection - FORBIDDEN
@Inject
public void setUserService(UserService userService) {
    this.userService = userService;
}
```

---

## CDI Scopes

| Scope | Lifecycle | Use Case |
|-------|-----------|----------|
| `@ApplicationScoped` | Single instance per application | Stateless services, most business logic |
| `@RequestScoped` | New instance per HTTP request | Request-specific data |
| `@SessionScoped` | New instance per HTTP session | User session data |
| `@Dependent` | New instance per injection | Helpers, utilities |
| `@Singleton` | Single instance (eager init) | Use sparingly, prefer @ApplicationScoped |

```java
@ApplicationScoped
public class UserService { }  // Singleton across application

@RequestScoped
public class RequestContext { }  // New instance per HTTP request
```

---

## Optional Dependencies

Use `Instance<T>` when a dependency might not be available:

```java
@ApplicationScoped
public class NotificationService {
    private final EmailService emailService;
    private final SmsService smsService;  // May be null

    public NotificationService(EmailService emailService,
                             Instance<SmsService> smsServiceInstance) {
        this.emailService = emailService;
        this.smsService = smsServiceInstance.isResolvable() ?
                         smsServiceInstance.get() : null;
    }

    public void sendNotification(String message) {
        emailService.send(message);  // Always available
        if (smsService != null) {
            smsService.send(message);  // Optional
        }
    }
}
```

---

## Producer Methods

### Scope and Null Return Rules

**CRITICAL**: CDI has strict rules about producer methods returning null.

| Scope | Can Return Null? | Reason |
|-------|------------------|--------|
| `@Dependent` | ✅ Yes | No proxy needed |
| `@RequestScoped` | ❌ No | Proxy requires target object |
| `@SessionScoped` | ❌ No | Proxy requires target object |
| `@ApplicationScoped` | ❌ No | Proxy requires target object |

### @Dependent Scope (Allows null)

```java
@ApplicationScoped
public class ServletObjectsProducer {

    @Produces
    @Dependent  // ✅ REQUIRED for null returns
    public HttpServletRequest produceHttpServletRequest() {
        return getHttpServletRequest().orElse(null);  // Safe with @Dependent
    }
}
```

### Normal Scoped Producers (Cannot return null)

```java
// ❌ ILLEGAL - will throw IllegalProductException
@Produces
@RequestScoped
public SomeService createService() {
    return null;  // CDI will throw exception at runtime
}

// ✅ CORRECT - Use Null Object pattern
@Produces
@RequestScoped
public NotificationService createNotificationService() {
    return notificationEnabled ?
           new EmailNotificationService() :
           new NoOpNotificationService();  // Never null
}
```

### Recommended Patterns for Optional Dependencies

1. **Use Instance<T> at Injection Points** (preferred)
2. **Use @Dependent Scope with Null Returns**
3. **Use Null Object Pattern**

**AVOID**: Returning `Optional<T>` from producer methods - goes against CDI design philosophy.

---

## Error Handling

### Common CDI Issues

| Problem | Exception | Solution |
|---------|-----------|----------|
| Missing dependency | `UnsatisfiedResolutionException` | Ensure dependency is a CDI bean with appropriate scope |
| Multiple implementations | `AmbiguousResolutionException` | Use `@Named` or custom qualifiers |
| Circular dependencies | `DeploymentException` | Refactor architecture or use `Instance<T>` for lazy init |

```java
// Disambiguate with @Named
@ApplicationScoped
public class PaymentService {
    public PaymentService(@Named("primary") PaymentGateway gateway) {
        // Uses specifically qualified implementation
    }
}
```

---

## Quality Checklist

- [ ] Constructor injection used (never field/setter injection)
- [ ] Final fields for all injected dependencies
- [ ] Single constructor (no @Inject needed) or @Inject on injection constructor
- [ ] Appropriate scope selected for each bean
- [ ] Instance<T> used for optional dependencies
- [ ] Producer methods use @Dependent if returning null
- [ ] Normal-scoped producers never return null

## Related Skills

- `pm-dev-java:java-cdi-quarkus` - Quarkus-specific CDI patterns, container/Docker config, security
- `pm-dev-java:java-core` - Core Java patterns
- `pm-dev-java:junit-core` - CDI testing patterns
