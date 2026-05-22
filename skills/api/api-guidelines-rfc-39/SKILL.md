---
name: api-guidelines-rfc-39
description: >
  RFC-39 compliant API best practices for Java services. Covers request/response patterns,
  error handling, pagination, versioning, and authentication standards.
  Use when designing or reviewing REST APIs in Java services.
compatibility: Java projects using Spring Boot for REST APIs
metadata:
  version: "1.0.0"
  technology: java
  category: api
  tags:
    - java
    - api
    - rfc-39
    - rest
    - spring-boot
---

# API Guidelines (RFC-39)

RFC-39 compliant API best practices for Java services.

## When to use this skill

- Designing new REST API endpoints
- Reviewing API implementations for compliance
- Implementing error handling patterns
- Setting up pagination and filtering
- Configuring API versioning
- Implementing authentication and authorization

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L24-L32)
- [Quick Start](#quick-start) (L55-L93)
- [Request/Response Patterns](#requestresponse-patterns) (L94-L143)
- [Error Handling](#error-handling) (L144-L207)
- [Pagination](#pagination) (L208-L252)
- [Versioning](#versioning) (L253-L280)
- [Authentication](#authentication) (L281-L311)
- [References](#references) (L312-L317)
- [Related Rules](#related-rules) (L318-L321)
- [Related Skills](#related-skills) (L322-L327)

### Available Resources

**📚 references/** - Detailed documentation
- [response patterns](references/response-patterns.md)

---

## Quick Start

### 1. Controller Setup

```java
@RestController
@RequestMapping("/api/v1/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;
    private final ResponseFactory responseFactory;

    @GetMapping("/{orderId}")
    public ResponseEntity<ApiResponse<OrderDto>> getOrder(
            @PathVariable String orderId) {
        OrderDto order = orderService.findById(orderId);
        return responseFactory.ok(order);
    }
}
```

### 2. Response Factory

```java
@Component
public class ResponseFactory {

    public <T> ResponseEntity<ApiResponse<T>> ok(T data) {
        return ResponseEntity.ok(ApiResponse.success(data));
    }

    public <T> ResponseEntity<ApiResponse<T>> created(T data) {
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(ApiResponse.success(data));
    }
}
```

## Request/Response Patterns

### Standard Response Envelope

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "requestId": "abc-123",
    "timestamp": "2026-01-27T12:00:00Z"
  }
}
```

### Java Implementation

```java
@Data
@Builder
public class ApiResponse<T> {
    private boolean success;
    private T data;
    private ApiError error;
    private ApiMeta meta;

    public static <T> ApiResponse<T> success(T data) {
        return ApiResponse.<T>builder()
            .success(true)
            .data(data)
            .meta(ApiMeta.now())
            .build();
    }
}

@Data
@Builder
public class ApiMeta {
    private String requestId;
    private Instant timestamp;

    public static ApiMeta now() {
        return ApiMeta.builder()
            .requestId(MDC.get("requestId"))
            .timestamp(Instant.now())
            .build();
    }
}
```

## Error Handling

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "email",
        "message": "must be a valid email address"
      }
    ]
  },
  "meta": {
    "requestId": "abc-123",
    "timestamp": "2026-01-27T12:00:00Z"
  }
}
```

### Exception Handler

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ApiResponse<Void>> handleNotFound(
            ResourceNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(ApiResponse.error("NOT_FOUND", ex.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiResponse<Void>> handleValidation(
            MethodArgumentNotValidException ex) {
        List<FieldError> details = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(e -> new FieldError(e.getField(), e.getDefaultMessage()))
            .toList();

        return ResponseEntity.badRequest()
            .body(ApiResponse.validationError(details));
    }
}
```

### Standard Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request parameters |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource conflict |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

## Pagination

### Request Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `page` | 0 | Page number (0-indexed) |
| `size` | 20 | Page size (max 100) |
| `sort` | - | Sort field and direction |

### Response Format

```json
{
  "success": true,
  "data": [...],
  "meta": {
    "pagination": {
      "page": 0,
      "size": 20,
      "totalElements": 150,
      "totalPages": 8,
      "hasNext": true,
      "hasPrevious": false
    }
  }
}
```

### Controller Example

```java
@GetMapping
public ResponseEntity<ApiResponse<List<OrderDto>>> listOrders(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size,
        @RequestParam(required = false) String sort) {

    Pageable pageable = PageRequest.of(page, Math.min(size, 100));
    Page<OrderDto> orders = orderService.findAll(pageable);

    return responseFactory.paginated(orders);
}
```

## Versioning

### URL Path Versioning (Preferred)

```java
@RestController
@RequestMapping("/api/v1/orders")
public class OrderV1Controller { }

@RestController
@RequestMapping("/api/v2/orders")
public class OrderV2Controller { }
```

### Deprecation Headers

```java
@GetMapping("/legacy-endpoint")
@Deprecated
public ResponseEntity<ApiResponse<Void>> legacyEndpoint() {
    return ResponseEntity.ok()
        .header("Deprecation", "true")
        .header("Sunset", "Sat, 01 Mar 2026 00:00:00 GMT")
        .header("Link", "</api/v2/new-endpoint>; rel=\"successor-version\"")
        .body(ApiResponse.success(null));
}
```

## Authentication

### WebAPI Annotation

```java
@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {

    @GetMapping
    @WebAPI(AuthType.PRIVATE)  // Requires user authentication
    public ResponseEntity<...> listOrders() { }

    @GetMapping("/public-info")
    @WebAPI(AuthType.PUBLIC)   // No authentication required
    public ResponseEntity<...> getPublicInfo() { }

    @GetMapping("/internal")
    @WebAPI(AuthType.INTERNAL) // Service-to-service only
    public ResponseEntity<...> internalEndpoint() { }
}
```

### Authentication Types

| Type | Usage |
|------|-------|
| `PRIVATE` | User-authenticated endpoints |
| `PUBLIC` | Unauthenticated, public endpoints |
| `INTERNAL` | Service-to-service communication |

## References

| Reference | Description |
|-----------|-------------|
| [references/response-patterns.md](references/response-patterns.md) | Detailed response patterns |

## Related Rules

- [java-rest-api-guidelines](.cursor/rules/java-rest-api-guidelines/java-rest-api-guidelines.mdc) - REST API standards (RFC-30/RFC-39)

## Related Skills

| Skill | Purpose |
|-------|---------|
| [rest-api](.claude/skills/rest-api/SKILL.md) | REST API implementation |
| [grpc-services-rfc-33](.claude/skills/grpc-services-rfc-33/SKILL.md) | gRPC service standards |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/api-guidelines-rfc-39/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

