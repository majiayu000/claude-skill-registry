---
name: spring-boot-web-api
description: Spring Boot 4 REST API implementation patterns. Use when creating REST controllers, REST endpoints, request validation, exception handlers with ProblemDetail (RFC 9457), API versioning, content negotiation, WebFlux reactive endpoints, HTTP clients with @HttpExchange, JSON serialization with Jackson 3, error handling, or CORS configuration. Covers @RestController patterns, Bean Validation 3.1, global error handling, and declarative HTTP clients.
spring-boot-version: "4.0"
---

# Spring Boot Web API Layer

REST API implementation patterns for Spring Boot 4 with Spring MVC and WebFlux.

## Technology Selection

| Choose | When |
|--------|------|
| **Spring MVC** | JPA/JDBC backend, simpler debugging, team knows imperative style |
| **Spring WebFlux** | High concurrency (10k+ connections), streaming, reactive DB (R2DBC) |

With Virtual Threads (Java 21+), MVC handles high concurrency without WebFlux complexity.

## Core Workflow

1. Create controller → 2. Define endpoints → 3. Add validation → 4. Handle exceptions → 5. Configure versioning

See [WORKFLOW.md](WORKFLOW.md) for detailed step-by-step instructions with code examples.

## Quick Patterns

See [EXAMPLES.md](EXAMPLES.md) for complete working examples including:
- **REST Controller** with CRUD operations and pagination (Java + Kotlin)
- **Request/Response DTOs** with Bean Validation 3.1
- **Global Exception Handler** using ProblemDetail (RFC 9457)
- **Native API Versioning** with header configuration
- **Jackson 3 Configuration** for custom serialization
- **Controller Testing** with @WebMvcTest

## Spring Boot 4 Specifics

- **Jackson 3** uses `tools.jackson` package (not `com.fasterxml.jackson`)
- **ProblemDetail** enabled by default: `spring.mvc.problemdetails.enabled=true`
- **API Versioning** via `version` attribute in mapping annotations
- **@MockitoBean** replaces `@MockBean` in tests
- **@HttpExchange** declarative HTTP clients (replaces RestTemplate patterns)
- **RestTestClient** new fluent API for testing REST endpoints

## @HttpExchange Declarative Client (Spring 7)

New declarative HTTP client interface (alternative to RestTemplate/WebClient):

```java
@HttpExchange(url = "/users", accept = "application/json")
public interface UserClient {

    @GetExchange("/{id}")
    User getUser(@PathVariable Long id);

    @PostExchange
    User createUser(@RequestBody CreateUserRequest request);

    @DeleteExchange("/{id}")
    void deleteUser(@PathVariable Long id);
}

// Configuration
@Configuration
class ClientConfig {
    @Bean
    UserClient userClient(RestClient.Builder builder) {
        RestClient restClient = builder.baseUrl("https://api.example.com").build();
        return HttpServiceProxyFactory
            .builderFor(RestClientAdapter.create(restClient))
            .build()
            .createClient(UserClient.class);
    }
}
```

**Benefits**: Type-safe, annotation-driven, works with both RestClient and WebClient.

## Detailed References

- **Workflow**: See [WORKFLOW.md](WORKFLOW.md) for detailed step-by-step web API implementation
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for complete working code examples
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and Boot 4 migration
- **Controllers & Validation**: See [references/CONTROLLERS.md](references/CONTROLLERS.md) for validation groups, custom validators, content negotiation
- **Error Handling**: See [references/ERROR-HANDLING.md](references/ERROR-HANDLING.md) for ProblemDetail patterns, exception hierarchy
- **WebFlux Patterns**: See [references/WEBFLUX.md](references/WEBFLUX.md) for reactive endpoints, functional routers, WebTestClient

## Related Skills

| Need | Skill |
|------|-------|
| DDD concepts | `domain-driven-design` |
| Data layer for DTOs | `spring-boot-data-ddd` |
| Controller testing | `spring-boot-testing` |
| API security | `spring-boot-security` |

## Anti-Pattern Checklist

| Anti-Pattern | Fix |
|--------------|-----|
| Business logic in controllers | Delegate to application services |
| Returning entities directly | Convert to DTOs |
| Generic error messages | Use typed ProblemDetail with error URIs |
| Missing validation | Add `@Valid` on `@RequestBody` |
| Blocking calls in WebFlux | Use reactive operators only |
| Catching exceptions silently | Let propagate to `@RestControllerAdvice` |

## Critical Reminders

1. **Controllers are thin** — Delegate to services, no business logic
2. **Validate at the boundary** — `@Valid` on all request bodies
3. **Use ProblemDetail** — Structured errors for all exceptions
4. **Version from day one** — Easier than retrofitting
5. **`@MockitoBean` not `@MockBean`** — Spring Boot 4 change
