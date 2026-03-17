---
name: spring-boot-web-api
description: Spring Boot 4 REST API implementation patterns. Use when creating REST controllers, request validation, exception handlers with ProblemDetail (RFC 9457), API versioning, content negotiation, or WebFlux reactive endpoints. Covers @RestController patterns, Bean Validation 3.1, global error handling, and Jackson 3 configuration.
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

1. **Create controller** → `@RestController` with `@RequestMapping` base path
2. **Define endpoints** → `@GetMapping`, `@PostMapping`, etc.
3. **Add validation** → `@Valid` on request body, custom validators
4. **Handle exceptions** → `@RestControllerAdvice` with `ProblemDetail`
5. **Configure versioning** → Native API versioning (Spring Boot 4)

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

- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for complete working code examples
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and Boot 4 migration
- **Controllers & Validation**: See [references/CONTROLLERS.md](references/CONTROLLERS.md) for validation groups, custom validators, content negotiation
- **Error Handling**: See [references/ERROR-HANDLING.md](references/ERROR-HANDLING.md) for ProblemDetail patterns, exception hierarchy
- **WebFlux Patterns**: See [references/WEBFLUX.md](references/WEBFLUX.md) for reactive endpoints, functional routers, WebTestClient

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
