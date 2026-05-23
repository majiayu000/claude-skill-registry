---
name: spring-boot-rest-api-standards
description: Implement REST API design standards and best practices for Spring Boot projects. Use when creating or reviewing REST endpoints, DTOs, error handling, pagination, security headers, HATEOAS and architecture patterns.
category: backend
tags: [spring-boot, rest-api, dto, validation, error-handling, pagination, hateoas, architecture, java]
version: 1.1.0
allowed-tools: Read, Write, Bash
---

# Spring Boot REST API Standards

This skill provides comprehensive guidance for building RESTful APIs in Spring Boot applications with consistent design patterns, proper error handling, validation, and architectural best practices based on REST principles and Spring Boot conventions.

## Overview

Spring Boot REST API standards establish consistent patterns for building production-ready REST APIs. These standards cover resource-based URL design, proper HTTP method usage, status code conventions, DTO patterns, validation, error handling, pagination, security headers, and architectural layering. Implement these patterns to ensure API consistency, maintainability, and adherence to REST principles.

## When to Use This Skill

Use this skill when:
- Creating new REST endpoints and API routes
- Designing request/response DTOs and API contracts
- Planning HTTP methods and status codes
- Implementing error handling and validation
- Setting up pagination, filtering, and sorting
- Designing security headers and CORS policies
- Implementing HATEOAS (Hypermedia As The Engine Of Application State)
- Reviewing REST API architecture and design patterns
- Building microservices with consistent API standards
- Documenting API endpoints with clear contracts

## Instructions

### To Build RESTful API Endpoints

Follow these steps to create well-designed REST API endpoints:

1. **Design Resource-Based URLs**
   - Use plural nouns for resource names
   - Follow REST conventions: GET /users, POST /users, PUT /users/{id}
   - Avoid action-based URLs like /getUserList

2. **Implement Proper HTTP Methods**
   - GET: Retrieve resources (safe, idempotent)
   - POST: Create resources (not idempotent)
   - PUT: Replace entire resources (idempotent)
   - PATCH: Partial updates (not idempotent)
   - DELETE: Remove resources (idempotent)

3. **Use Appropriate Status Codes**
   - 200 OK: Successful GET/PUT/PATCH
   - 201 Created: Successful POST with Location header
   - 204 No Content: Successful DELETE
   - 400 Bad Request: Invalid request data
   - 404 Not Found: Resource doesn't exist
   - 409 Conflict: Duplicate resource
   - 500 Internal Server Error: Unexpected errors

4. **Create Request/Response DTOs**
   - Separate API contracts from domain entities
   - Use Java records or Lombok `@Data`/`@Value`
   - Apply Jakarta validation annotations
   - Keep DTOs immutable when possible

5. **Implement Validation**
   - Use `@Valid` annotation on `@RequestBody` parameters
   - Apply validation constraints (`@NotBlank`, `@Email`, `@Size`, etc.)
   - Handle validation errors with `MethodArgumentNotValidException`

6. **Set Up Error Handling**
   - Use `@RestControllerAdvice` for global exception handling
   - Return standardized error responses with status, error, message, and timestamp
   - Use `ResponseStatusException` for specific HTTP status codes

7. **Configure Pagination**
   - Use Pageable for large datasets
   - Include page, size, sort parameters
   - Return metadata with total elements, totalPages, etc.

8. **Add Security Headers**
   - Configure CORS policies
   - Set content security policy
   - Include X-Frame-Options, X-Content-Type-Options

## Examples

### Basic CRUD Controller

```java
@RestController
@RequestMapping("/v1/users")
@RequiredArgsConstructor
@Slf4j
public class UserController {
    private final UserService userService;

    @GetMapping
    public ResponseEntity<Page<UserResponse>> getAllUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int pageSize) {
        log.debug("Fetching users page {} size {}", page, pageSize);
        Page<UserResponse> users = userService.getAll(page, pageSize);
        return ResponseEntity.ok(users);
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUserById(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getById(id));
    }

    @PostMapping
    public ResponseEntity<UserResponse> createUser(@Valid @RequestBody CreateUserRequest request) {
        UserResponse created = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UpdateUserRequest request) {
        return ResponseEntity.ok(userService.update(id, request));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

### Request/Response DTOs

```java
// Request DTO
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CreateUserRequest {
    @NotBlank(message = "User name cannot be blank")
    private String name;

    @Email(message = "Valid email required")
    private String email;
}

// Response DTO
@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserResponse {
    private Long id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
}
```

### Global Exception Handler

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
            MethodArgumentNotValidException ex, WebRequest request) {
        String errors = ex.getBindingResult().getFieldErrors().stream()
                .map(f -> f.getField() + ": " + f.getDefaultMessage())
                .collect(Collectors.joining(", "));

        ErrorResponse errorResponse = new ErrorResponse(
                HttpStatus.BAD_REQUEST.value(),
                "Validation Error",
                "Validation failed: " + errors,
                request.getDescription(false).replaceFirst("uri=", "")
        );
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(ResponseStatusException.class)
    public ResponseEntity<ErrorResponse> handleResponseStatusException(
            ResponseStatusException ex, WebRequest request) {
        ErrorResponse error = new ErrorResponse(
            ex.getStatusCode().value(),
            ex.getStatusCode().toString(),
            ex.getReason(),
            request.getDescription(false).replaceFirst("uri=", "")
        );
        return new ResponseEntity<>(error, ex.getStatusCode());
    }
}
```

## Best Practices

### 1. Use Constructor Injection
```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
    // Dependencies are explicit and testable
}
```

### 2. Prefer Immutable DTOs
```java
// Java records (JDK 16+)
public record UserResponse(Long id, String name, String email, LocalDateTime createdAt) {}

// Lombok @Value for immutability
@Value
public class UserResponse {
    Long id;
    String name;
    String email;
    LocalDateTime createdAt;
}
```

### 3. Validate Input Early
```java
@PostMapping
public ResponseEntity<UserResponse> createUser(@Valid @RequestBody CreateUserRequest request) {
    // Validation happens automatically before method execution
    return ResponseEntity.status(HttpStatus.CREATED).body(userService.create(request));
}
```

### 4. Use ResponseEntity Flexibly
```java
return ResponseEntity.status(HttpStatus.CREATED)
    .header("Location", "/api/users/" + created.getId())
    .header("X-Total-Count", String.valueOf(userService.count()))
    .body(created);
```

### 5. Implement Proper Transaction Management
```java
@Service
@Transactional
public class UserService {

    @Transactional(readOnly = true)
    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    @Transactional
    public User create(User user) {
        return userRepository.save(user);
    }
}
```

### 6. Add Meaningful Logging
```java
@Slf4j
@Service
public class UserService {
    public User create(User user) {
        log.info("Creating user with email: {}", user.getEmail());
        return userRepository.save(user);
    }
}
```

### 7. Document APIs with Javadoc
```java
/**
 * Retrieves a user by id.
 *
 * @param id the user id
 * @return ResponseEntity containing a UserResponse
 * @throws ResponseStatusException with 404 if user not found
 */
@GetMapping("/{id}")
public ResponseEntity<UserResponse> getUserById(@PathVariable Long id)
```

## Constraints

### 1. Never Expose Entities Directly
Use DTOs to separate API contracts from domain models. This prevents accidental exposure of internal data structures and allows API evolution without database schema changes.

### 2. Follow REST Conventions Strictly
- Use nouns for resource names, not verbs
- Use correct HTTP methods for operations
- Use plural resource names (/users, not /user)
- Return appropriate HTTP status codes for each operation

### 3. Handle All Exceptions Globally
Use @RestControllerAdvice to catch all exceptions consistently. Don't let raw exceptions bubble up to clients.

### 4. Always Paginate Large Result Sets
For GET endpoints that might return many results, implement pagination to prevent performance issues and DDoS vulnerabilities.

### 5. Validate All Input Data
Never trust client input. Use Jakarta validation annotations on all request DTOs to validate data at the controller boundary.

### 6. Use Constructor Injection Exclusively
Avoid field injection (`@Autowired`) for better testability and explicit dependency declaration.

### 7. Keep Controllers Thin
Controllers should only handle HTTP request/response adaptation. Delegate business logic to service layers.

## References

- See `references/` directory for comprehensive reference material including HTTP status codes, Spring annotations, and detailed examples
- Refer to `agents/spring-boot-code-review-specialist.md` for code review guidelines
- Review `spring-boot-dependency-injection/SKILL.md` for dependency injection patterns
- Check `junit-test-patterns/SKILL.md` for testing REST APIs