---
name: check-concurrency
description: Find concurrency issues including race conditions, deadlocks, unsafe shared state, and improper synchronization
---

# Check Concurrency Skill

Identify concurrency bugs, race conditions, deadlocks, and thread safety issues in the codebase.

## Instructions

### 1. Identify Shared Mutable State

Search for mutable state that may be accessed by multiple threads:

**Instance/Static Fields**:
```java
// Dangerous - mutable shared state
private Map<K, V> cache = new HashMap<>();
private List<T> items = new ArrayList<>();
private int counter = 0;
private boolean flag = false;

// Safe alternatives
private final ConcurrentHashMap<K, V> cache = new ConcurrentHashMap<>();
private final CopyOnWriteArrayList<T> items = new CopyOnWriteArrayList<>();
private final AtomicInteger counter = new AtomicInteger();
private final AtomicBoolean flag = new AtomicBoolean();
```

Use `Grep` to find:
```
private.*Map<
private.*List<
private.*Set<
private static(?!.*final)
private.*= 0;
private.*= false;
private.*= true;
private.*= null;
```

### 2. Check for Race Conditions

**Check-Then-Act Anti-patterns**:
```java
// RACE CONDITION: check and act not atomic
if (!map.containsKey(key)) {
    map.put(key, value);  // Another thread may have put between check and act
}

// SAFE: Use atomic operations
map.putIfAbsent(key, value);
map.computeIfAbsent(key, k -> createValue());
```

**Read-Modify-Write Anti-patterns**:
```java
// RACE CONDITION: increment not atomic
counter++;
counter = counter + 1;

// SAFE: Use atomic types
atomicCounter.incrementAndGet();
```

**Lazy Initialization**:
```java
// RACE CONDITION: double-checked locking without volatile
if (instance == null) {
    synchronized(lock) {
        if (instance == null) {
            instance = new Instance();  // May return partially constructed
        }
    }
}

// SAFE: Use volatile or holder pattern
private static volatile Instance instance;
// or
private static class Holder {
    static final Instance INSTANCE = new Instance();
}
```

### 3. Detect Potential Deadlocks

**Lock Ordering Issues**:
```java
// DEADLOCK RISK: Different lock ordering
// Thread 1: synchronized(lockA) { synchronized(lockB) { ... } }
// Thread 2: synchronized(lockB) { synchronized(lockA) { ... } }
```

Search for nested synchronization:
```java
synchronized.*\{[\s\S]*synchronized
```

**Resource Acquisition**:
```java
// DEADLOCK RISK: Acquiring multiple semaphores
semaphoreA.acquire();
semaphoreB.acquire();  // What if another thread holds B, wants A?
```

### 4. Analyze Synchronization Usage

**Over-synchronization** (performance issue):
```java
// BAD: Synchronized on entire method when only part needs it
public synchronized void process(Data data) {
    // ... lots of non-shared work ...
    cache.put(key, value);  // Only this needs sync
}

// BETTER: Minimize synchronized scope
public void process(Data data) {
    // ... non-shared work ...
    synchronized(lock) {
        cache.put(key, value);
    }
}
```

**Under-synchronization** (correctness issue):
```java
// BAD: Some methods synchronized, some not
public synchronized void add(T item) { list.add(item); }
public T get(int i) { return list.get(i); }  // NOT synchronized!
```

### 5. Check Thread-Safe Collections Usage

**Compound Operations on Concurrent Collections**:
```java
ConcurrentHashMap<K, V> map = ...;

// RACE CONDITION: Compound operation not atomic
V value = map.get(key);
if (value == null) {
    value = computeValue();
    map.put(key, value);  // Another thread may have computed too
}

// SAFE: Use atomic compute methods
V value = map.computeIfAbsent(key, k -> computeValue());
```

**Iteration Safety**:
```java
// UNSAFE: ConcurrentModificationException or stale data
for (K key : map.keySet()) {
    map.remove(key);  // Modifying during iteration
}

// SAFE: Use iterator.remove() or collect keys first
```

### 6. Virtual Threads & StructuredTaskScope (Java 21+)

This project uses Java 24 virtual threads. Check for:

**Pinning Issues**:
```java
// BAD: synchronized pins virtual thread to carrier
synchronized(lock) {
    blockingCall();  // Virtual thread pinned!
}

// BETTER: Use ReentrantLock
lock.lock();
try {
    blockingCall();  // Virtual thread can unmount
} finally {
    lock.unlock();
}
```

**StructuredTaskScope Usage**:
```java
// Check for proper scope management
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var future1 = scope.fork(() -> task1());
    var future2 = scope.fork(() -> task2());
    scope.join();           // Must join before getting results
    scope.throwIfFailed();  // Must check for failures
    return combine(future1.get(), future2.get());
}

// ISSUES TO CHECK:
// - Missing join() before accessing results
// - Missing throwIfFailed() for ShutdownOnFailure
// - Scope not closed (try-with-resources required)
// - Sharing scope between threads
```

### 7. Reactive/WebFlux Concurrency

**Publisher Sharing**:
```java
// UNSAFE: Sharing mutable state in reactive chain
List<String> results = new ArrayList<>();  // Shared mutable!
flux.doOnNext(item -> results.add(item))   // Race condition!
    .subscribe();

// SAFE: Use collectList() or reduce()
flux.collectList().subscribe(results -> ...);
```

**Scheduler Awareness**:
```java
// Check that shared state access considers scheduler
mono.publishOn(Schedulers.parallel())  // Multiple threads!
    .map(data -> {
        sharedState.update(data);  // RACE CONDITION
        return data;
    });
```

### 8. This Project's Specific Patterns

**Files to examine**:
- `AggregatorService.java` - Uses StructuredTaskScope, Semaphores, ConcurrentHashMap
- `CurrentConditionsService.java` - Caching with concurrent access
- `ForecastService.java` - Data parsing with potential shared state
- `*Strategy.java` - Strategy implementations called concurrently

**Known concurrent structures in this project**:
```java
// Check these are used correctly:
ConcurrentHashMap<Integer, ForecastData> forecastCache
ConcurrentHashMap<Integer, CurrentConditions> currentConditions
AtomicReference<List<Spot>> spots
Semaphore (for rate limiting)
```

### 9. Common Concurrency Anti-patterns

| Pattern | Issue | Fix |
|---------|-------|-----|
| `HashMap` in concurrent context | Race condition | Use `ConcurrentHashMap` |
| `ArrayList` shared between threads | Race condition | Use `CopyOnWriteArrayList` or synchronize |
| `SimpleDateFormat` shared | Not thread-safe | Use `DateTimeFormatter` (immutable) |
| Non-volatile field read by multiple threads | Visibility issue | Use `volatile` or atomic |
| `synchronized(this)` | Lock on public object | Use private lock object |
| Catching `InterruptedException` silently | Lost interrupt | Re-interrupt or propagate |

## Output Format

```markdown
## Concurrency Analysis Report

### Summary
| Category | Issues Found | Severity |
|----------|--------------|----------|
| Race Conditions | X | Critical |
| Potential Deadlocks | X | Critical |
| Unsafe Shared State | X | High |
| Synchronization Issues | X | Medium |
| Virtual Thread Issues | X | Medium |

### Critical Issues

#### Race Condition: [Description]
**File**: `path/to/file.java:line`
**Pattern**: Check-then-act on HashMap
**Threads Involved**: Scheduler thread, Request threads
```java
// Current code
if (!cache.containsKey(key)) {
    cache.put(key, expensiveCompute());
}
```
**Risk**: Duplicate computation, inconsistent state
**Fix**:
```java
cache.computeIfAbsent(key, k -> expensiveCompute());
```

#### Potential Deadlock: [Description]
**File**: `path/to/file.java:line`
**Pattern**: Nested locks with inconsistent ordering
**Fix**: Establish global lock ordering or use tryLock with timeout

### High Priority Issues

#### Unsafe Shared State
| File | Line | Field | Issue | Fix |
|------|------|-------|-------|-----|
| Service.java | 15 | `Map cache` | Non-concurrent map | Use ConcurrentHashMap |

### Medium Priority Issues

#### Synchronization Improvements
- `File.java:42` - Consider narrowing synchronized scope
- `File.java:78` - Missing volatile on field read by multiple threads

### Verified Thread-Safe Patterns

| File | Pattern | Why It's Safe |
|------|---------|---------------|
| AggregatorService.java | ConcurrentHashMap | Proper atomic operations used |
| AggregatorService.java | Semaphore | Proper acquire/release in try-finally |

### StructuredTaskScope Analysis

| Location | Usage | Status |
|----------|-------|--------|
| AggregatorService:120 | ShutdownOnFailure | ✓ Correct |
| AggregatorService:150 | fork/join | ✓ Proper ordering |

### Recommendations

1. **Immediate**: Fix race condition in `Cache.java:42`
2. **Review**: Audit all HashMap usages for thread safety
3. **Consider**: Add @ThreadSafe/@NotThreadSafe annotations for documentation
4. **Testing**: Add concurrent stress tests for critical sections
```

## Execution Steps

1. Use `Grep` to find mutable field declarations
2. Use `Grep` to find `synchronized`, `Lock`, `Semaphore` usage
3. Use `Grep` to find concurrent collection usage
4. Read files to analyze compound operations
5. Check StructuredTaskScope for proper join/close
6. Look for check-then-act and read-modify-write patterns
7. Analyze lock ordering for deadlock potential
8. Generate categorized report

## Notes

- Virtual threads change some concurrency patterns (synchronized pins carrier thread)
- ConcurrentHashMap is safe for individual operations, not compound ones
- AtomicReference doesn't make the referenced object thread-safe
- Reactive chains may execute on different threads at different stages
- `@Scheduled` methods may run concurrently if previous execution is slow
- Focus on request-handling code paths over initialization code
