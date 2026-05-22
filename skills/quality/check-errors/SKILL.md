---
name: check-errors
description: Find error handling gaps including swallowed exceptions, missing handlers, inconsistent error responses, and reactive error handling issues
---

# Check Errors Skill

Identify error handling gaps, anti-patterns, and inconsistencies in exception management across the codebase.

## Instructions

### 1. Find Swallowed Exceptions

Search for empty or inadequate catch blocks:

```java
// BAD: Empty catch block
try {
    riskyOperation();
} catch (Exception e) {
    // silently swallowed!
}

// BAD: Only logging, not handling
try {
    riskyOperation();
} catch (Exception e) {
    log.error("Error", e);
    // continues as if nothing happened
}

// BAD: Catching and returning null
try {
    return fetchData();
} catch (Exception e) {
    return null;  // Caller doesn't know it failed
}
```

Use `Grep` to find:
```bash
# Empty catch blocks
catch.*\{[\s]*\}

# Catch with only comment
catch.*\{[\s]*/[/*]

# Catch with only log statement and no throw/return
catch.*\{[\s]*log\.(error|warn|info)
```

### 2. Check Reactive Error Handling

**Missing error operators in Mono/Flux chains**:

```java
// BAD: No error handling
return webClient.get()
    .retrieve()
    .bodyToMono(Data.class);  // What if it fails?

// GOOD: Proper error handling
return webClient.get()
    .retrieve()
    .bodyToMono(Data.class)
    .onErrorResume(e -> {
        log.error("Failed to fetch", e);
        return Mono.empty();
    });

// GOOD: With fallback
return service.fetchData()
    .onErrorReturn(defaultValue);

// GOOD: Transform error
return service.fetchData()
    .onErrorMap(e -> new DomainException("Fetch failed", e));
```

**Search for chains without error handling**:
```java
// Find Mono/Flux returns without onError*
\.bodyToMono\(.*\);$
\.bodyToFlux\(.*\);$
\.flatMap\(.*\);$  // without subsequent onError
```

### 3. Analyze Exception Propagation

**Checked vs Unchecked exceptions**:

```java
// BAD: Wrapping checked in RuntimeException without context
try {
    Files.readAllBytes(path);
} catch (IOException e) {
    throw new RuntimeException(e);  // Loses context
}

// GOOD: Wrap with meaningful exception
try {
    Files.readAllBytes(path);
} catch (IOException e) {
    throw new ConfigLoadException("Failed to load config: " + path, e);
}
```

**Search for generic exception wrapping**:
```bash
throw new RuntimeException\(e\)
throw new RuntimeException\(.*e\)
throw new IllegalStateException\(e\)
```

### 4. Controller Error Handling

**Check for @ExceptionHandler coverage**:

```java
// Global exception handler should exist
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(NotFoundException e) {
        return ResponseEntity.status(404).body(new ErrorResponse(e.getMessage()));
    }

    @ExceptionHandler(Exception.class)  // Catch-all
    public ResponseEntity<ErrorResponse> handleGeneral(Exception e) {
        log.error("Unexpected error", e);
        return ResponseEntity.status(500).body(new ErrorResponse("Internal error"));
    }
}
```

**Verify**:
- @ControllerAdvice exists
- Common exceptions are handled (NotFound, BadRequest, etc.)
- Catch-all handler exists
- Error responses are consistent

**Check controllers for unhandled exceptions**:
```java
// BAD: Exception can escape to framework
@GetMapping("/{id}")
public Mono<Data> getById(@PathVariable int id) {
    return service.findById(id);  // What if not found?
}

// GOOD: Proper handling
@GetMapping("/{id}")
public Mono<ResponseEntity<Data>> getById(@PathVariable int id) {
    return service.findById(id)
        .map(ResponseEntity::ok)
        .defaultIfEmpty(ResponseEntity.notFound().build());
}
```

### 5. Error Response Consistency

**Check error response format**:

```java
// All error responses should follow same structure
{
    "error": "Error message",
    "code": "ERROR_CODE",
    "timestamp": "2024-01-01T00:00:00Z",
    "path": "/api/resource"
}
```

**Find inconsistent error responses**:
```java
// Different formats
ResponseEntity.badRequest().body("Error")           // String
ResponseEntity.badRequest().body(Map.of("msg", e))  // Map
ResponseEntity.badRequest().body(new Error(e))      // Object
```

### 6. Null Handling Gaps

**Missing null checks**:

```java
// BAD: No null check before use
public void process(Data data) {
    String value = data.getValue().toUpperCase();  // NPE if null
}

// GOOD: Defensive coding
public void process(Data data) {
    if (data == null || data.getValue() == null) {
        throw new IllegalArgumentException("Data and value required");
    }
    String value = data.getValue().toUpperCase();
}

// GOOD: Optional usage
public void process(Data data) {
    Optional.ofNullable(data)
        .map(Data::getValue)
        .ifPresent(this::handleValue);
}
```

**Search patterns**:
```bash
# Method calls on potentially null returns
\.get\(\)\.           # get() followed by method call
\.findFirst\(\)\.get  # Optional.get() without isPresent
```

### 7. Resource Cleanup on Error

**Check try-with-resources usage**:

```java
// BAD: Resource leak on exception
InputStream is = new FileInputStream(file);
try {
    process(is);
} finally {
    is.close();  // May throw, masking original exception
}

// GOOD: Try-with-resources
try (InputStream is = new FileInputStream(file)) {
    process(is);
}
```

**Check OkHttp response body closure**:
```java
// BAD: Response body not closed on error
Response response = client.newCall(request).execute();
if (!response.isSuccessful()) {
    throw new ApiException("Failed");  // Body leaked!
}
String body = response.body().string();

// GOOD: Try-with-resources
try (Response response = client.newCall(request).execute()) {
    if (!response.isSuccessful()) {
        throw new ApiException("Failed: " + response.code());
    }
    return response.body().string();
}
```

### 8. Logging Quality

**Check error logging**:

```java
// BAD: No stack trace
log.error("Error occurred");
log.error("Error: " + e.getMessage());

// BAD: Wrong log level
log.info("Error occurred", e);  // Should be error/warn

// GOOD: Full context
log.error("Failed to process request for user={}", userId, e);
```

**Search for inadequate logging**:
```bash
log\.error\("[^"]*"\);$           # error without exception
log\.error\(".*" \+ e\.getMessage  # message only, no stack
catch.*\{[^}]*\}                   # catch without any log
```

### 9. Timeout and Retry Handling

**Check for timeout handling**:

```java
// BAD: No timeout
Response response = client.newCall(request).execute();

// GOOD: Configured timeout
OkHttpClient client = new OkHttpClient.Builder()
    .connectTimeout(10, TimeUnit.SECONDS)
    .readTimeout(30, TimeUnit.SECONDS)
    .build();

// Check reactive timeouts
mono.timeout(Duration.ofSeconds(30))
    .onErrorResume(TimeoutException.class, e -> fallback());
```

**Check for retry logic**:
```java
// With Spring Retry
@Retryable(value = ApiException.class, maxAttempts = 3)
public Data fetchData() { ... }

@Recover
public Data fallback(ApiException e) { ... }

// With Reactor
mono.retryWhen(Retry.backoff(3, Duration.ofSeconds(1)))
```

### 10. Project-Specific Checks

**Files to examine**:
- `controller/*.java` - HTTP error responses
- `service/*.java` - Business exception handling
- `service/strategy/*.java` - External API error handling
- `config/*Config.java` - Configuration error handling

**This project's patterns to verify**:
```java
// AggregatorService - scheduled task error handling
// ForecastService - Windguru API error handling
// CurrentConditionsService - Weather station error handling
// GoogleMapsService - URL resolution error handling
```

## Output Format

```markdown
## Error Handling Analysis Report

### Summary
| Category | Issues | Severity |
|----------|--------|----------|
| Swallowed Exceptions | X | Critical |
| Missing Reactive Handlers | X | High |
| Inconsistent Error Responses | X | Medium |
| Resource Leaks on Error | X | High |
| Inadequate Logging | X | Medium |

### Critical Issues

#### Swallowed Exception
**File**: `path/to/file.java:line`
**Code**:
```java
try {
    externalService.call();
} catch (Exception e) {
    // empty
}
```
**Risk**: Silent failures, data inconsistency
**Fix**:
```java
try {
    externalService.call();
} catch (Exception e) {
    log.error("External service call failed", e);
    throw new ServiceException("Failed to call external service", e);
}
```

### High Priority Issues

#### Missing Reactive Error Handler
**File**: `path/to/file.java:line`
**Chain**: `webClient.get()...bodyToMono()`
**Risk**: Unhandled errors propagate to framework
**Fix**: Add `.onErrorResume()` or `.onErrorReturn()`

#### Resource Leak Risk
**File**: `path/to/file.java:line`
**Resource**: OkHttp Response
**Fix**: Wrap in try-with-resources

### Medium Priority Issues

| File | Line | Issue | Recommendation |
|------|------|-------|----------------|
| Service.java | 42 | Generic RuntimeException wrap | Use domain exception |
| Handler.java | 78 | Log without stack trace | Add exception parameter |

### Error Handler Coverage

| Exception Type | Handler Exists | Location |
|----------------|----------------|----------|
| NotFoundException | ✓ | GlobalExceptionHandler:25 |
| ValidationException | ✗ | Missing |
| Generic Exception | ✓ | GlobalExceptionHandler:45 |

### Reactive Chains Analysis

| File | Line | Chain | Error Handling |
|------|------|-------|----------------|
| ForecastService | 42 | Mono<Forecast> | ✓ onErrorResume |
| AggregatorService | 78 | Flux<Spot> | ✗ Missing |

### Recommendations

1. **Critical**: Add error handling to empty catch at `File.java:42`
2. **High**: Add @ControllerAdvice for ValidationException
3. **Medium**: Standardize error response format across controllers
4. **Low**: Improve error log messages with more context

### Error Handling Checklist

- [ ] No empty catch blocks
- [ ] All reactive chains have error operators
- [ ] @ControllerAdvice covers common exceptions
- [ ] Error responses follow consistent format
- [ ] Resources closed properly on error paths
- [ ] Errors logged with stack traces
- [ ] Timeouts configured for external calls
- [ ] Retry logic for transient failures
```

## Execution Steps

1. Use `Grep` to find empty/inadequate catch blocks
2. Use `Grep` to find reactive chains without error handling
3. Check for @ControllerAdvice and @ExceptionHandler
4. Analyze error response formats in controllers
5. Find resource usages without try-with-resources
6. Check logging statements in catch blocks
7. Verify timeout and retry configurations
8. Generate comprehensive report

## Notes

- Some "swallowed" exceptions may be intentional (e.g., optional cleanup)
- Reactive error handling is critical - errors should never silently disappear
- This project uses @Retryable in some services - verify @Recover exists
- OkHttp responses MUST be closed, even on error paths
- Empty Mono/Flux is sometimes valid fallback, but should be logged
