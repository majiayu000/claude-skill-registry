---
name: spring-boot-openapi-documentation
description: Provides patterns to generate comprehensive REST API documentation using SpringDoc OpenAPI 3.0 and Swagger UI in Spring Boot 3.x applications. Use when setting up API documentation, configuring Swagger UI, adding OpenAPI annotations, implementing security documentation, or enhancing REST endpoints with examples and schemas.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Spring Boot OpenAPI Documentation with SpringDoc

## Overview

SpringDoc OpenAPI automates generation of OpenAPI 3.0 documentation for Spring Boot projects with a Swagger UI web interface for exploring and testing APIs.

## When to Use

- Set up SpringDoc OpenAPI in Spring Boot 3.x projects
- Generate OpenAPI 3.0 specifications for REST APIs
- Configure and customize Swagger UI
- Add detailed API documentation with annotations
- Document request/response models with validation
- Implement API security documentation (JWT, OAuth2, Basic Auth)
- Document pageable and sortable endpoints
- Add examples and schemas to API endpoints
- Customize OpenAPI definitions programmatically
- Support multiple API groups and versions
- Document error responses and exception handlers
- Add JSR-303 Bean Validation to API documentation
- Support Kotlin-based Spring Boot APIs

## Quick Reference

| Concept | Description |
|---------|-------------|
| **Dependencies** | `springdoc-openapi-starter-webmvc-ui` for WebMvc, `springdoc-openapi-starter-webflux-ui` for WebFlux |
| **Configuration** | `application.yml` with `springdoc.api-docs.*` and `springdoc.swagger-ui.*` properties |
| **Access Points** | OpenAPI JSON: `/v3/api-docs`, Swagger UI: `/swagger-ui/index.html` |
| **Core Annotations** | `@Tag`, `@Operation`, `@ApiResponse`, `@Parameter`, `@Schema`, `@SecurityRequirement` |
| **Security** | Configure security schemes in OpenAPI bean, apply with `@SecurityRequirement` |
| **Pagination** | Use `@ParameterObject` with Spring Data `Pageable` |

## Instructions

### 1. Add Dependencies

Add SpringDoc starter for your application type (WebMvc or WebFlux). See [dependency-setup.md](references/dependency-setup.md) for Maven/Gradle configuration.

### 2. Configure SpringDoc

Set basic configuration in `application.yml`:

```yaml
springdoc:
  api-docs:
    path: /api-docs
  swagger-ui:
    path: /swagger-ui.html
    operationsSorter: method
```

See [configuration.md](references/configuration.md) for advanced options.

### 3. Document Controllers

Use OpenAPI annotations to add descriptive information:

```java
@RestController
@Tag(name = "Book", description = "Book management APIs")
public class BookController {

    @Operation(summary = "Get book by ID")
    @ApiResponse(responseCode = "200", description = "Book found")
    @GetMapping("/{id}")
    public Book findById(@PathVariable Long id) { }
}
```

See [controller-documentation.md](references/controller-documentation.md) for patterns.

### 4. Document Models

Apply `@Schema` annotations to DTOs:

```java
@Schema(description = "Book entity")
public class Book {
    @Schema(example = "1", accessMode = Schema.AccessMode.READ_ONLY)
    private Long id;

    @Schema(example = "Clean Code", required = true)
    private String title;
}
```

See [model-documentation.md](references/model-documentation.md) for validation patterns.

### 5. Configure Security

Set up security schemes in OpenAPI bean:

```java
@Bean
public OpenAPI customOpenAPI() {
    return new OpenAPI()
        .components(new Components()
            .addSecuritySchemes("bearer-jwt", new SecurityScheme()
                .type(SecurityScheme.Type.HTTP)
                .scheme("bearer")
                .bearerFormat("JWT")
            )
        );
}
```

Apply with `@SecurityRequirement(name = "bearer-jwt")` on controllers. See [security-configuration.md](references/security-configuration.md).

### 6. Document Pagination

Use `@ParameterObject` for Spring Data `Pageable`:

```java
@GetMapping("/paginated")
public Page<Book> findAll(@ParameterObject Pageable pageable) {
    return repository.findAll(pageable);
}
```

See [pagination-support.md](references/pagination-support.md).

### 7. Test Documentation

Access Swagger UI at `/swagger-ui/index.html` to verify documentation completeness.

### 8. Customize for Production

Configure API grouping, versioning, and build plugins. See [advanced-configuration.md](references/advanced-configuration.md) and [build-integration.md](references/build-integration.md).

## Best Practices

- **Use descriptive operation summaries**: Short (< 120 chars), clear statements
- **Document all response codes**: Include success (2xx), client errors (4xx), server errors (5xx)
- **Add examples to request/response bodies**: Use `@ExampleObject` for realistic examples
- **Leverage JSR-303 validation annotations**: SpringDoc auto-generates constraints from validation annotations
- **Use `@ParameterObject` for complex parameters**: Especially for Pageable, custom filter objects
- **Group related endpoints with `@Tag`**: Organize API by domain entities or features
- **Document security requirements**: Apply `@SecurityRequirement` where authentication needed
- **Hide internal endpoints appropriately**: Use `@Hidden` or create separate API groups
- **Customize Swagger UI for better UX**: Enable filtering, sorting, try-it-out features
- **Version your API documentation**: Include version in OpenAPI Info

## References

- **[dependency-setup.md](references/dependency-setup.md)** — Maven/Gradle dependencies and version selection
- **[configuration.md](references/configuration.md)** — Basic and advanced configuration options
- **[controller-documentation.md](references/controller-documentation.md)** — Controller and endpoint documentation patterns
- **[model-documentation.md](references/model-documentation.md)** — Entity, DTO, and validation documentation
- **[security-configuration.md](references/security-configuration.md)** — JWT, OAuth2, Basic Auth, API key configuration
- **[pagination-support.md](references/pagination-support.md)** — Pageable, Slice, and custom pagination patterns
- **[advanced-configuration.md](references/advanced-configuration.md)** — API groups, customizers, OpenAPI bean configuration
- **[exception-handling.md](references/exception-handling.md)** — Exception documentation and error response schemas
- **[build-integration.md](references/build-integration.md)** — Maven/Gradle plugins and CI/CD integration
- **[complete-examples.md](references/complete-examples.md)** — Full controller, entity, and configuration examples
- **[annotations-reference.md](references/annotations-reference.md)** — Complete annotation reference with attributes
- **[springdoc-official.md](references/springdoc-official.md)** — Official SpringDoc documentation
- **[troubleshooting.md](references/troubleshooting.md)** — Common issues and solutions

## Constraints and Warnings

- Do not expose sensitive data in API examples or schema descriptions
- Keep OpenAPI annotations minimal to avoid cluttering controller code; use global configurations when possible
- Large API definitions can impact Swagger UI performance; consider grouping APIs by domain
- Schema generation may not work correctly with complex generic types; use explicit `@Schema` annotations
- Avoid circular references in DTOs as they cause infinite recursion in schema generation
- Security schemes must be properly configured before using `@SecurityRequirement` annotations
- Hidden endpoints (`@Operation(hidden = true)`) are still visible in code and may leak through other documentation tools

## Examples

### Basic Controller Documentation

```java
@RestController
@Tag(name = "Books", description = "Book management APIs")
@RequestMapping("/api/books")
public class BookController {

    @Operation(
        summary = "Get book by ID",
        description = "Retrieves detailed information about a specific book"
    )
    @ApiResponse(responseCode = "200", description = "Book found")
    @ApiResponse(responseCode = "404", description = "Book not found")
    @GetMapping("/{id}")
    public Book getBook(@PathVariable Long id) {
        return bookService.findById(id);
    }

    @Operation(summary = "Create new book")
    @SecurityRequirement(name = "bearer-jwt")
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Book createBook(@Valid @RequestBody CreateBookRequest request) {
        return bookService.create(request);
    }
}
```

### Documented Model with Validation

```java
@Schema(description = "Book entity")
public class Book {
    @Schema(description = "Unique identifier", example = "1", accessMode = Schema.AccessMode.READ_ONLY)
    private Long id;

    @Schema(description = "Book title", example = "Clean Code", required = true)
    @NotBlank
    @Size(min = 1, max = 200)
    private String title;

    @Schema(description = "Author name", example = "Robert C. Martin")
    @NotBlank
    private String author;

    @Schema(description = "Price in USD", example = "29.99", minimum = "0")
    @NotNull
    @DecimalMin("0.0")
    private BigDecimal price;
}
```

### Security Configuration

```java
@Bean
public OpenAPI customOpenAPI() {
    return new OpenAPI()
        .info(new Info()
            .title("Book API")
            .version("1.0.0")
            .description("REST API for book management"))
        .components(new Components()
            .addSecuritySchemes("bearer-jwt", new SecurityScheme()
                .type(SecurityScheme.Type.HTTP)
                .scheme("bearer")
                .bearerFormat("JWT"))
            .addSecuritySchemes("api-key", new SecurityScheme()
                .type(SecurityScheme.Type.APIKEY)
                .in(SecurityScheme.In.HEADER)
                .name("X-API-Key")));
}
```

## Related Skills

- `spring-boot-rest-api-standards` — REST API design standards
- `spring-boot-dependency-injection` — Dependency injection patterns
- `unit-test-controller-layer` — Testing REST controllers
- `spring-boot-actuator` — Production monitoring and management

## External Resources

- [SpringDoc Official Documentation](https://springdoc.org/)
- [OpenAPI 3.0 Specification](https://swagger.io/specification/)
- [Swagger UI Configuration](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)
