---
name: profile-blocking
description: Find blocking calls in reactive WebFlux code that can cause performance issues and thread starvation
---

# Profile Blocking Skill

Identify blocking calls in the reactive codebase that can cause thread starvation, deadlocks, and performance degradation in Spring WebFlux applications.

## Instructions

### 1. Search for Blocking Patterns

Use `Grep` to search for these blocking call patterns:

#### Direct Blocking Calls
```java
.block()           // Mono/Flux blocking subscription
.blockFirst()      // Flux blocking first element
.blockLast()       // Flux blocking last element
.blockOptional()   // Mono blocking to Optional
.toFuture().get()  // CompletableFuture blocking
.get()             // Future.get() blocking
.join()            // CompletableFuture.join()
```

#### Thread Blocking
```java
Thread.sleep(      // Thread sleep
Object.wait(       // Object monitor wait
.await(            // CountDownLatch, CyclicBarrier await
.acquire(          // Semaphore blocking acquire
synchronized       // Synchronized blocks (potential)
ReentrantLock.lock // Explicit locking
```

#### Blocking I/O
```java
InputStream        // Blocking input streams
OutputStream       // Blocking output streams
FileInputStream    // File I/O
FileOutputStream   // File I/O
BufferedReader     // Blocking readers
Scanner            // Blocking scanner
new URL(           // URL.openStream() is blocking
HttpURLConnection  // Blocking HTTP
```

#### JDBC/Database (if present)
```java
JdbcTemplate       // Blocking JDBC
EntityManager      // Blocking JPA
.save(             // Repository blocking save
.findBy            // Repository blocking find
DataSource         // Direct datasource access
```

### 2. Context-Aware Analysis

For each finding, determine if it's:

**Acceptable blocking**:
- Inside `StructuredTaskScope` (this project uses Java 24 virtual threads)
- In `@Scheduled` methods running on separate thread pool
- In test code
- Wrapped in `Mono.fromCallable()` with `.subscribeOn(Schedulers.boundedElastic())`
- In startup/initialization code (non-request path)

**Problematic blocking**:
- In `@RestController` methods returning `Mono`/`Flux`
- In reactive chain operators (map, flatMap, filter)
- On Netty event loop threads
- In `WebFilter` implementations
- Inside `Mono.create()` or `Flux.create()` without scheduler

### 3. Analyze Reactive Chains

Check for anti-patterns in reactive code:

```java
// BAD: Blocking in map
mono.map(data -> {
    blockingCall();  // Blocks event loop!
    return result;
})

// BAD: Blocking in flatMap
flux.flatMap(item -> {
    var result = blockingService.call();  // Blocks!
    return Mono.just(result);
})

// GOOD: Proper offloading
mono.flatMap(data ->
    Mono.fromCallable(() -> blockingCall())
        .subscribeOn(Schedulers.boundedElastic())
)
```

### 4. Check This Project's Specific Patterns

**Files to examine**:
- `src/main/java/**/controller/*.java` - REST endpoints
- `src/main/java/**/service/*.java` - Service layer
- `src/main/java/**/strategy/*.java` - Strategy implementations
- `src/main/java/**/config/*.java` - Configuration classes

**Known acceptable patterns in this project**:
- `StructuredTaskScope` usage in `AggregatorService` (virtual threads)
- `.block()` inside virtual thread contexts
- OkHttp calls (executed in separate thread pool)

**Patterns to flag**:
- `.block()` in controller methods
- Blocking in `WebFilter` or `HandlerFilterFunction`
- Synchronous HTTP calls without proper scheduling

### 5. Virtual Thread Considerations

This project uses Java 24 with virtual threads. Check:

```java
// Virtual thread factory usage
Thread.ofVirtual().factory()

// StructuredTaskScope usage (blocking is OK inside)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    scope.fork(() -> blockingCall());  // OK - virtual thread
    scope.join();  // OK - virtual thread blocks, not platform thread
}
```

### 6. HTTP Client Analysis

Check OkHttp usage patterns:

```java
// Synchronous call - check if on reactive thread
Response response = client.newCall(request).execute();

// Better: Use async
client.newCall(request).enqueue(callback);

// Or wrap properly
Mono.fromCallable(() -> client.newCall(request).execute())
    .subscribeOn(Schedulers.boundedElastic())
```

## Output Format

```markdown
## Blocking Call Analysis Report

### Summary
| Category | Count | Severity |
|----------|-------|----------|
| Direct .block() calls | X | High/Medium |
| Thread.sleep() | X | High |
| Blocking I/O | X | Medium |
| Synchronized blocks | X | Low |
| **Total potential issues** | **Y** | |

### Critical Issues (Event Loop Blocking)

#### [Issue Title]
**File**: `path/to/file.java:line`
**Pattern**: `.block()` in reactive chain
**Context**: Inside @RestController endpoint
**Risk**: Thread starvation, request timeouts
```java
// Current code
@GetMapping("/data")
public Mono<Data> getData() {
    return service.fetchData()
        .map(d -> blockingTransform(d));  // BLOCKS!
}
```
**Fix**:
```java
@GetMapping("/data")
public Mono<Data> getData() {
    return service.fetchData()
        .flatMap(d -> Mono.fromCallable(() -> blockingTransform(d))
            .subscribeOn(Schedulers.boundedElastic()));
}
```

### Medium Priority (Potential Issues)

| File | Line | Pattern | Context | Verdict |
|------|------|---------|---------|---------|
| Service.java | 42 | .block() | Inside StructuredTaskScope | OK |
| Handler.java | 78 | Thread.sleep | Test code | OK |

### Acceptable Blocking (Verified Safe)

These blocking calls are in appropriate contexts:

| File | Line | Pattern | Why It's OK |
|------|------|---------|-------------|
| AggregatorService.java | 120 | .block() | Inside virtual thread scope |
| ForecastService.java | 85 | OkHttp.execute() | Wrapped in fromCallable |

### Patterns Found

#### .block() Calls
```
src/main/java/.../Service.java:42  - response.block()
src/main/java/.../Service.java:87  - result.blockFirst()
```

#### Thread Blocking
```
src/main/java/.../Worker.java:23   - Thread.sleep(1000)
```

#### Blocking I/O
```
src/main/java/.../Reader.java:15   - new FileInputStream()
```

### Recommendations

1. **Immediate**: Move blocking call at `File.java:42` to bounded elastic scheduler
2. **Review**: Verify StructuredTaskScope usage covers all blocking in AggregatorService
3. **Consider**: Replace synchronous OkHttp with async calls or WebClient

### Reactive Best Practices Checklist

- [ ] No .block() in @RestController methods
- [ ] No .block() in WebFilter implementations
- [ ] Blocking I/O wrapped with boundedElastic scheduler
- [ ] Thread.sleep() only in tests or scheduled tasks
- [ ] Synchronized blocks minimized and not in hot paths
- [ ] HTTP clients properly configured for async or offloaded
```

## Execution Steps

1. Use `Grep` to find all `.block()` calls
2. Use `Grep` to find `Thread.sleep`, `.await(`, `synchronized`
3. Use `Grep` to find blocking I/O patterns
4. Read each file to determine context (controller vs service vs test)
5. Check if blocking is inside StructuredTaskScope or virtual thread
6. Categorize findings by severity
7. Generate report with fix recommendations

## Notes

- Virtual threads (Java 21+) change the blocking calculus - blocking is OK on virtual threads
- This project uses StructuredTaskScope, so verify scope boundaries
- OkHttp is blocking by default but may be acceptable if not on event loop
- Focus on request-handling paths; scheduled tasks are lower priority
- Some `.block()` in tests is normal and acceptable
- Spring WebFlux Netty uses limited event loop threads - blocking them is critical
