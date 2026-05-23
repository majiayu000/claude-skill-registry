---
name: cui-http
description: CUI HTTP client standards with HttpHandler, HttpResult pattern, and async-first adapters
user-invocable: false
allowed-tools: Read, Grep, Glob
---

# CUI HTTP Skill

**REFERENCE MODE**: This skill provides reference material. Load specific standards on-demand based on current task.

CUI-specific HTTP client standards for projects using the CUI HTTP library (cui-http). This skill covers HttpHandler usage, the HttpResult sealed interface pattern, and async-first HTTP adapters with retry and caching.

## Prerequisites

This skill requires CUI library dependencies:
- `de.cuioss:cui-http` (HttpHandler, HttpResult, HttpAdapter)

## Workflow

### Step 1: Load HTTP Client Standards

**CRITICAL**: Load this standard for any HTTP client work.

```
Read: standards/cui-http.md
```

This provides the foundational rules:
- HttpHandler builder pattern for configuration
- HttpResult sealed interface for type-safe error handling
- Async-first adapters (ETagAwareHttpAdapter, ResilientHttpAdapter)
- RetryConfig for exponential backoff

## Key Rules Summary

### HttpHandler Builder Pattern
```java
// CORRECT - Use builder pattern
HttpHandler handler = HttpHandler.builder()
    .uri("https://api.example.com/data")
    .connectionTimeoutSeconds(10)
    .readTimeoutSeconds(30)
    .build();
```

### HttpResult Pattern Matching
```java
// CORRECT - Pattern matching for result handling
return switch (result) {
    case HttpResult.Success<T>(var content, var etag, var status) -> {
        processContent(content);
        yield true;
    }
    case HttpResult.Failure<T> failure -> {
        logger.error(failure.errorMessage());
        if (failure.isRetryable()) {
            scheduleRetry();
        }
        yield false;
    }
};
```

### Async-First Adapters
```java
// CORRECT - Compose adapters for retry + caching
HttpAdapter<String> adapter = ResilientHttpAdapter.wrap(
    ETagAwareHttpAdapter.<String>builder()
        .httpHandler(httpHandler)
        .responseConverter(StringContentConverter.identity())
        .build(),
    RetryConfig.defaults()
);

// Async execution
adapter.get(Map.of("Accept", "application/json"))
    .thenAccept(result -> handleResult(result));
```

### Error Category Handling
```java
// CORRECT - Handle errors by category
result.getErrorCategory().ifPresent(category -> {
    switch (category) {
        case NETWORK_ERROR -> retryStrategy.scheduleRetry();
        case SERVER_ERROR -> retryStrategy.scheduleRetry();
        case CLIENT_ERROR -> alertOperations("Invalid request");
        case INVALID_CONTENT -> useFallbackSource();
        case CONFIGURATION_ERROR -> alertOperations("Config error");
    }
});
```

## Related Skills

- `pm-dev-java:java-core` - General Java patterns (no CUI dependencies)
- `pm-dev-java-cui:cui-testing-http` - HTTP testing with CUI MockWebServer

## Standards Reference

| Standard | Purpose |
|----------|---------|
| cui-http.md | HttpHandler, HttpResult, and adapter patterns |
