---
name: openapi_docs
router_kit: ManagementKit
description: Generate comprehensive REST API documentation using SpringDoc OpenAPI 3.0 and Swagger UI in Spring Boot 3.x applications. Use when setting up API documentation, configuring Swagger UI, adding OpenAPI annotations, implementing security documentation, or enhancing REST endpoints with examples and schemas.
allowed-tools: Read, Write, Bash, Grep
category: backend
tags: [accessibility, api integration, api-documentation, backend, browser apis, client-side, components, css3, debugging, deployment, frameworks, frontend, fullstack, html5, javascript, libraries, node.js, npm, openapi, openapi docs, performance optimization, responsive design, seo, spring-boot, springdoc, state management, swagger, testing, typescript, ui/ux, web development]
version: 1.1.0
metadata:
  skillport:
    category: auto-healed
    tags:
      - openapi_docs
      - openapi_docs
---

# Spring Boot OpenAPI Documentation with SpringDoc

Implement comprehensive REST API documentation using SpringDoc OpenAPI 3.0 and Swagger UI in Spring Boot 3.x applications.

## When to Use

Use this skill when you need to:
- Set up SpringDoc OpenAPI in Spring Boot 3.x projects
- Generate OpenAPI 3.0 specifications for REST APIs
- Configure and customize Swagger UI
- Add detailed API documentation with annotations
- Document request/response models with validation
- Implement API security documentation (JWT, OAuth2, Basic Auth)
- Document pageable and sortable endpoints
- Add examples and schemas to API endpoints
- Customize OpenAPI definitions programmatically
- Generate API documentation for WebMvc or WebFlux applications
- Support multiple API groups and versions
- Document error responses and exception handlers
- Add JSR-303 Bean Validation to API documentation
- Support Kotlin-based Spring Boot APIs

## Setup Dependencies

### Add Maven Dependencies

```xml
<!-- Standard WebMVC support -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.8.13</version> // Use latest stable version
</dependency>

<!-- Optional: therapi-runtime-javadoc for JavaDoc support -->
<dependency>
    <groupId>com.github.therapi</groupId>
    <artifactId>therapi-runtime-javadoc</artifactId>
    <version>0.15.0</version> // Use latest stable version
    <scope>provided</scope>
</dependency>

<!-- WebFlux support -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webflux-ui</artifactId>
    <version>2.8.13</version> // Use latest stable version
</dependency>
```

### Add Gradle Dependencies

```gradle
// Standard WebMVC support
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.8.13'

// Optional: therapi-runtime-javadoc for JavaDoc support
implementation 'com.github.therapi:therapi-runtime-javadoc:0.15.0'

// WebFlux support
implementation 'org.springdoc:springdoc-openapi-starter-webflux-ui:2.8.13'
```

## Configure SpringDoc

### Basic Configuration

```properties
# application.properties
springdoc.api-docs.path=/api-docs
springdoc.swagger-ui.path=/swagger-ui-custom.html
springdoc.swagger-ui.operationsSorter=method
springdoc.swagger-ui.tagsSorter=alpha
springdoc.swagger-ui.enabled=true
springdoc.api-docs.enabled=true
springdoc.packages-to-scan=com.example.controller
springdoc.paths-to-match=/api/**
```

```yaml
# application.yml
springdoc:
  api-docs:
    path: /api-docs
    enabled: true
  swagger-ui:
    path: /swagger-ui.html
    enabled: true
    operationsSorter: method
    tagsSorter: alpha
    tryItOutEnabled: true
  packages-to-scan: com.example.controller
  paths-to-match: /api/**
```

### Access Endpoints

After configuration:
- **OpenAPI JSON**: `http://localhost:8080/v3/api-docs`
- **OpenAPI YAML**: `http://localhost:8080/v3/api-docs.yaml`
- **Swagger UI**: `http://localhost:8080/swagger-ui/index.html`

## Document Controllers

### Basic Controller Documentation

```java
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/books")
@Tag(name = "Book", description = "Book management APIs")
public class BookController {

    @Operation(
        summary = "Retrieve a book by ID",
        description = "Get a Book object by specifying its ID. The response includes id, title, author and description."
    )
    @ApiResponses(value = {
        @ApiResponse(
            responseCode = "200",
            description = "Successfully retrieved book",
            content = @Content(schema = @Schema(implementation = Book.class))
        ),
        @ApiResponse(
            responseCode = "404",
            description = "Book not found"
        )
    })
    @GetMapping("/{id}")
    public Book findById(
        @Parameter(description = "ID of book to retrieve", required = true)
        @PathVariable Long id
    ) {
        return repository.findById(id)
            .orElseThrow(() -> new BookNotFoundException());
    }
}
```

### Document Request Bodies

```java
import io.swagger.v3.oas.annotations.parameters.RequestBody;
import io.swagger.v3.oas.annotations.media.ExampleObject;

@Operation(summary = "Create a new book")
@PostMapping
@ResponseStatus(HttpStatus.CREATED)
public Book createBook(
    @RequestBody(
        description = "Book to create",
        required = true,
        content = @Content(
            schema = @Schema(implementation = Book.class),
            examples = @ExampleObject(
                value = """
                {
                    "title": "Clean Code",
                    "author": "Robert C. Martin",
                    "isbn": "978-0132350884",
                    "description": "A handbook of agile software craftsmanship"
                }
                """
            )
        )
    )
    Book book
) {
    return repository.save(book);
}
```

## Document Models

### Entity with Validation

```java
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;

@Entity
@Schema(description = "Book entity representing a published book")
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Schema(description = "Unique identifier", example = "1", accessMode = Schema.AccessMode.READ_ONLY)
    private Long id;

    @NotBlank(message = "Title is required")
    @Size(min = 1, max = 200)
    @Schema(description = "Book title", example = "Clean Code", required = true, maxLength = 200)
    private String title;

    @Pattern(regexp = "^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$")
    @Schema(description = "ISBN number", example = "978-0132350884")
    private String isbn;

    // Additional fields, constructors, getters, setters
}
```

### Hidden Fields

```java
@Schema(hidden = true)
private String internalField;

@JsonIgnore
@Schema(accessMode = Schema.AccessMode.READ_ONLY)
private LocalDateTime createdAt;
```

## Document Security

### JWT Bearer Authentication

```java
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.security.SecurityScheme;

@Configuration
public class OpenAPISecurityConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .components(new Components()
                .addSecuritySchemes("bearer-jwt", new SecurityScheme()
                    .type(SecurityScheme.Type.HTTP)
                    .scheme("bearer")
                    .bearerFormat("JWT")
                    .description("JWT authentication")
                )
            );
    }
}

// Apply security requirement
@RestController
@RequestMapping("/api/books")
@SecurityRequirement(name = "bearer-jwt")
public class BookController {
    // All endpoints require JWT authentication
}
```

### OAuth2 Configuration

```java
import io.swagger.v3.oas.models.security.OAuthFlow;
import io.swagger.v3.oas.models.security.OAuthFlows;
import io.swagger.v3.oas.models.security.Scopes;

@Bean
public OpenAPI customOpenAPI() {
    return new OpenAPI()
        .components(new Components()
            .addSecuritySchemes("oauth2", new SecurityScheme()
                .type(SecurityScheme.Type.OAUTH2)
                .flows(new OAuthFlows()
                    .authorizationCode(new OAuthFlow()
                        .authorizationUrl("https://auth.example.com/oauth/authorize")
                        .tokenUrl("https://auth.example.com/oauth/token")
                        .scopes(new Scopes()
                            .addString("read", "Read access")
                            .addString("write", "Write access")
                        )
                    )
                )
            )
        );
}
```

## Document Pagination

### Spring Data Pageable Support

```java
import org.springdoc.core.annotations.ParameterObject;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

@Operation(summary = "Get paginated list of books")
@GetMapping("/paginated")
public Page<Book> findAllPaginated(
    @ParameterObject Pageable pageable
) {
    return repository.findAll(pageable);
}
```

## Advanced Configuration

### Multiple API Groups

```java
import org.springdoc.core.models.GroupedOpenApi;

@Bean
public GroupedOpenApi publicApi() {
    return GroupedOpenApi.builder()
        .group("public")
        .pathsToMatch("/api/public/**")
        .build();
}

@Bean
public GroupedOpenApi adminApi() {
    return GroupedOpenApi.builder()
        .group("admin")
        .pathsToMatch("/api/admin/**")
        .build();
}
```

### Custom Operation Customizer

```java
import org.springdoc.core.customizers.OperationCustomizer;

@Bean
public OperationCustomizer customizeOperation() {
    return (operation, handlerMethod) -> {
        operation.addExtension("x-custom-field", "custom-value");
        return operation;
    };
}
```

### Hide Endpoints

```java
@Operation(hidden = true)
@GetMapping("/internal")
public String internalEndpoint() {
    return "Hidden from docs";
}

// Hide entire controller
@Hidden
@RestController
public class InternalController {
    // All endpoints hidden
}
```

## Document Exception Responses

### Global Exception Handler

```java
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BookNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    @Operation(hidden = true)
    public ErrorResponse handleBookNotFound(BookNotFoundException ex) {
        return new ErrorResponse("BOOK_NOT_FOUND", ex.getMessage());
    }

    @ExceptionHandler(ValidationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @Operation(hidden = true)
    public ErrorResponse handleValidation(ValidationException ex) {
        return new ErrorResponse("VALIDATION_ERROR", ex.getMessage());
    }
}

@Schema(description = "Error response")
public record ErrorResponse(
    @Schema(description = "Error code", example = "BOOK_NOT_FOUND")
    String code,

    @Schema(description = "Error message", example = "Book with ID 123 not found")
    String message,

    @Schema(description = "Timestamp", example = "2024-01-15T10:30:00Z")
    LocalDateTime timestamp
) {}
```

## Build Integration

### Maven Plugin

```xml
<plugin>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-maven-plugin</artifactId>
    <version>1.4</version>
    <executions>
        <execution>
            <phase>integration-test</phase>
            <goals>
                <goal>generate</goal>
            </goals>
        </execution>
    </executions>
    <configuration>
        <apiDocsUrl>http://localhost:8080/v3/api-docs</apiDocsUrl>
        <outputFileName>openapi.json</outputFileName>
        <outputDir>${project.build.directory}</outputDir>
    </configuration>
</plugin>
```

### Gradle Plugin

```gradle
plugins {
    id 'org.springdoc.openapi-gradle-plugin' version '1.9.0'
}

openApi {
    apiDocsUrl = "http://localhost:8080/v3/api-docs"
    outputDir = file("$buildDir/docs")
    outputFileName = "openapi.json"
}
```

## Examples

### Complete REST Controller Example

```java
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springdoc.core.annotations.ParameterObject;
import org.springframework.web.bind.annotation.*;
import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/books")
@Tag(name = "Book", description = "Book management APIs")
@SecurityRequirement(name = "bearer-jwt")
public class BookController {

    private final BookService bookService;

    public BookController(BookService bookService) {
        this.bookService = bookService;
    }

    @Operation(summary = "Get all books")
    @ApiResponses(value = {
        @ApiResponse(
            responseCode = "200",
            description = "Found all books",
            content = @Content(
                mediaType = "application/json",
                array = @ArraySchema(schema = @Schema(implementation = Book.class))
            )
        )
    })
    @GetMapping
    public List<Book> getAllBooks() {
        return bookService.getAllBooks();
    }

    @Operation(summary = "Get paginated books")
    @GetMapping("/paginated")
    public Page<Book> getBooksPaginated(@ParameterObject Pageable pageable) {
        return bookService.getBooksPaginated(pageable);
    }

    @Operation(summary = "Get book by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Book found"),
        @ApiResponse(responseCode = "404", description = "Book not found")
    })
    @GetMapping("/{id}")
    public Book getBookById(@PathVariable Long id) {
        return bookService.getBookById(id);
    }

    @Operation(summary = "Create new book")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Book created successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid input")
    })
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Book createBook(@Valid @RequestBody Book book) {
        return bookService.createBook(book);
    }

    @Operation(summary = "Update book")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Book updated"),
        @ApiResponse(responseCode = "404", description = "Book not found")
    })
    @PutMapping("/{id}")
    public Book updateBook(@PathVariable Long id, @Valid @RequestBody Book book) {
        return bookService.updateBook(id, book);
    }

    @Operation(summary = "Delete book")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "204", description = "Book deleted"),
        @ApiResponse(responseCode = "404", description = "Book not found")
    })
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteBook(@PathVariable Long id) {
        bookService.deleteBook(id);
    }
}
```

## Best Practices

1. **Use descriptive operation summaries and descriptions**
   - Summary: Short, clear statement (< 120 chars)
   - Description: Detailed explanation with use cases

2. **Document all response codes**
   - Include success (2xx), client errors (4xx), server errors (5xx)
   - Provide meaningful descriptions for each

3. **Add examples to request/response bodies**
   - Use `@ExampleObject` for realistic examples
   - Include edge cases when relevant

4. **Leverage JSR-303 validation annotations**
   - SpringDoc auto-generates constraints from validation annotations
   - Reduces duplication between code and documentation

5. **Use `@ParameterObject` for complex parameters**
   - Especially useful for Pageable, custom filter objects
   - Keeps controller methods clean

6. **Group related endpoints with @Tag**
   - Organize API by domain entities or features
   - Use consistent tag names across controllers

7. **Document security requirements**
   - Apply `@SecurityRequirement` where authentication needed
   - Configure security schemes globally in OpenAPI bean

8. **Hide internal/admin endpoints appropriately**
   - Use `@Hidden` or create separate API groups
   - Prevent exposing internal implementation details

9. **Customize Swagger UI for better UX**
   - Enable filtering, sorting, try-it-out features
   - Set appropriate default behaviors

10. **Version your API documentation**
    - Include version in OpenAPI Info
    - Consider multiple API groups for versioned APIs

## Common Annotations Reference

### Core Annotations

- `@Tag`: Group operations under a tag
- `@Operation`: Describe a single API operation
- `@ApiResponse` / `@ApiResponses`: Document response codes
- `@Parameter`: Document a single parameter
- `@RequestBody`: Document request body (OpenAPI version)
- `@Schema`: Document model schema
- `@SecurityRequirement`: Apply security to operations
- `@Hidden`: Hide from documentation
- `@ParameterObject`: Document complex objects as parameters

### Validation Annotations (Auto-documented)

- `@NotNull`, `@NotBlank`, `@NotEmpty`: Required fields
- `@Size(min, max)`: String/collection length constraints
- `@Min`, `@Max`: Numeric range constraints
- `@Pattern`: Regex validation
- `@Email`: Email validation
- `@DecimalMin`, `@DecimalMax`: Decimal constraints
- `@Positive`, `@PositiveOrZero`, `@Negative`, `@NegativeOrZero`

## Troubleshooting

For common issues and solutions, refer to the troubleshooting guide in @references/troubleshooting.md

## Related Skills

- `spring-boot-rest-api-standards` - REST API design standards
- `spring-boot-dependency-injection` - Dependency injection patterns
- `unit-test-controller-layer` - Testing REST controllers
- `spring-boot-actuator` - Production monitoring and management

## References

- [Comprehensive SpringDoc documentation](references/springdoc-official.md)
- [Common issues and solutions](references/troubleshooting.md)
- [SpringDoc Official Documentation](https://springdoc.org/)
- [OpenAPI 3.0 Specification](https://swagger.io/specification/)
*OpenAPI Docs v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [SpringDoc Official Documentation](https://springdoc.org/)

### Aşama 1: Configuration
- [ ] **Dependency**: `springdoc-openapi-starter-webmvc-ui` (v2.x for Spring Boot 3) ekle.
- [ ] **Properties**: `springdoc.api-docs.path` ve `swagger-ui.path` değerlerini sabitle (custom path kullanıyorsan).
- [ ] **Platform**: WebMVC vs WebFlux ayrımına dikkat et (dependency farklı).

### Aşama 2: Documentation Layer
- [ ] **Controller**: `@Tag` ile grupla, `@Operation` ile her endpoint'i açıkla.
- [ ] **Models**: DTO'ları `@Schema` ile tanımla, validation anotasyonlarını (`@NotNull`) ekle (otomatik yansır).
- [ ] **Security**: Global security scheme (JWT/OAuth2) tanımla ve endpoint'lere `@SecurityRequirement` ekle.

### Aşama 3: Enhancement
- [ ] **Examples**: `@ExampleObject` kullanarak request/response body'ler için gerçekçi örnekler ver.
- [ ] **Error Handling**: Global Exception Handler'daki hata response formatlarını `@ApiResponse` ile dokümante et.
- [ ] **Generation**: CI/CD pipeline'ında `springdoc-openapi-maven-plugin` ile `openapi.json` üret.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | `/v3/api-docs` JSON dönüyor mu? |
| 2 | Swagger UI'da "Try it out" butonu çalışıyor mu (CORS/Auth sorunu var mı)? |
| 3 | Enum değerleri ve required alanlar dokümanda doğru görünüyor mu? |