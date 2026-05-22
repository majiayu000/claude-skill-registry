---
name: java-best-practices-debug-analyzer
description: |
  Analyze and debug Java issues including stack traces, exceptions, and performance problems.
  Use when debugging Java errors, analyzing stack traces, investigating exceptions,
  finding root causes, debugging NullPointerException, analyzing thread dumps,
  detecting memory leaks, troubleshooting performance issues, or investigating ClassNotFoundException.
  Works with Java exception logs, thread dumps, heap dumps, and error messages.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Java Debug Analyzer

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Examples](#examples)
- [Requirements](#requirements)
- [Analysis Checklist](#analysis-checklist)
- [Output Format](#output-format)
- [Error Handling](#error-handling)

## Purpose

Analyzes Java runtime issues, exceptions, stack traces, thread dumps, and performance problems to identify root causes and provide actionable solutions. Helps debug common Java errors, memory leaks, concurrency issues, and performance bottlenecks.

## When to Use

Use this skill when you need to:
- Debug Java runtime exceptions (NullPointerException, ClassNotFoundException, etc.)
- Analyze stack traces to find root causes
- Investigate memory leaks (OutOfMemoryError)
- Debug performance issues (slow responses, high CPU/memory)
- Analyze thread dumps for deadlocks or thread contention
- Diagnose ClassNotFoundException or NoClassDefFoundError
- Troubleshoot database connection issues
- Debug concurrency problems (race conditions, deadlocks)
- Investigate production errors from logs
- Root cause analysis for Java application failures

## Quick Start
Provide any Java error, exception, or log and receive root cause analysis:

```bash
# Analyze a stack trace
Analyze this Java stack trace: [paste stack trace]

# Debug an exception in logs
Debug the errors in application.log

# Analyze thread dump
Analyze the thread dump in thread-dump.txt
```

## Instructions

### Step 1: Identify Problem Type
Classify the issue to apply appropriate analysis:

**Exception Categories:**
- Runtime exceptions (NullPointerException, ClassCastException, etc.)
- Checked exceptions (IOException, SQLException, etc.)
- Custom application exceptions
- Framework exceptions (Spring, Hibernate, etc.)

**Performance Issues:**
- Slow response times
- High CPU usage
- High memory consumption
- Thread contention

**Resource Issues:**
- Memory leaks
- Connection pool exhaustion
- File handle leaks
- Thread starvation

**Configuration Issues:**
- ClassNotFoundException/NoClassDefFoundError
- Dependency conflicts
- Property misconfiguration

### Step 2: Analyze Stack Traces
Extract critical information from stack traces:

**Key Elements to Identify:**
1. **Exception type** - What went wrong
2. **Exception message** - Why it happened
3. **Caused by chain** - Root cause
4. **First application frame** - Where in your code
5. **Framework frames** - Context of execution
6. **Suppressed exceptions** - Additional context

**Analysis Pattern:**
```
Read stack trace from bottom to top:
1. Find "Caused by" at the bottom (root cause)
2. Identify the first frame in YOUR code
3. Understand the context from framework frames
4. Look for patterns (repeated exceptions, timing)
```

### Step 3: Diagnose Common Exceptions

#### NullPointerException
**Root Causes:**
- Uninitialized object reference
- Method returning null not handled
- Optional not checked
- Missing null checks in chain calls

**Analysis Steps:**
1. Identify exact line from stack trace
2. Examine variables on that line
3. Trace back to where null originated
4. Check method contracts (should it return null?)

**Example Analysis:**
```java
// Stack trace shows:
Exception in thread "main" java.lang.NullPointerException
    at com.example.UserService.getEmail(UserService.java:45)

// Line 45 is:
String email = user.getEmail().toLowerCase();

// Diagnosis: Either user is null OR user.getEmail() returns null
// Solution: Add null checks or use Optional
String email = Optional.ofNullable(user)
    .map(User::getEmail)
    .map(String::toLowerCase)
    .orElse("no-email");
```

#### ClassNotFoundException / NoClassDefFoundError
**Difference:**
- ClassNotFoundException: Class not found at runtime (missing in classpath)
- NoClassDefFoundError: Class was present at compile time but missing at runtime

**Root Causes:**
- Missing dependency in pom.xml/build.gradle
- Dependency version conflict
- Wrong classpath configuration
- JAR not packaged correctly

**Analysis Steps:**
1. Identify the missing class name
2. Check if dependency is declared
3. Verify dependency scope (runtime vs compile)
4. Check for version conflicts (mvn dependency:tree)

#### OutOfMemoryError
**Types:**
- Java heap space - Object allocation failed
- GC overhead limit exceeded - Too much time in GC
- Unable to create new native thread - Thread exhaustion
- Metaspace - Class metadata exhaustion

**Analysis Steps:**
1. Identify OOM type from message
2. Check heap size configuration (-Xmx)
3. Look for memory leak patterns
4. Analyze heap dump if available

### Step 4: Analyze Thread Dumps
Understand thread states and identify issues:

**Thread States:**
- RUNNABLE - Executing or ready to execute
- BLOCKED - Waiting for monitor lock
- WAITING - Waiting indefinitely (Object.wait())
- TIMED_WAITING - Waiting with timeout (Thread.sleep())
- TERMINATED - Thread finished execution

**Red Flags:**
- Multiple threads BLOCKED on same lock (contention)
- Many threads in WAITING state (possible deadlock)
- Threads holding locks for long time
- Repeated stack patterns (infinite loops)

**Deadlock Detection Pattern:**
```
Look for:
1. Thread A: waiting to lock <0x123> held by Thread B
2. Thread B: waiting to lock <0x456> held by Thread A
```

### Step 5: Diagnose Performance Issues

**High CPU:**
- Look for infinite loops in thread dumps
- Check for inefficient algorithms (nested loops)
- Examine regex patterns (catastrophic backtracking)
- Verify GC frequency (excessive GC)

**High Memory:**
- Large collections not cleared
- Static references preventing GC
- Memory leaks from listeners/callbacks
- Caching without size limits

**Slow Queries:**
- Missing database indexes
- N+1 query problems
- Large result sets
- Missing query optimization

### Step 6: Provide Root Cause and Solution

**Output Format:**
```markdown
## Problem Summary
[Brief description of the issue]

## Root Cause
[Detailed explanation of why this happened]

## Evidence
[Stack traces, log excerpts, analysis data]

## Solution
[Step-by-step fix]

## Prevention
[How to avoid this in the future]
```

## Examples

### Example 1: NullPointerException Analysis

**Input:**
```
Exception in thread "http-nio-8080-exec-3" java.lang.NullPointerException: Cannot invoke "String.toLowerCase()" because the return value of "com.example.model.User.getEmail()" is null
    at com.example.service.UserService.sendWelcomeEmail(UserService.java:67)
    at com.example.controller.UserController.createUser(UserController.java:45)
    at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
    at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:207)
```

**Analysis:**
```markdown
## Problem Summary
NullPointerException when attempting to call toLowerCase() on a null email string during user creation.

## Root Cause
The User.getEmail() method is returning null, and the code attempts to call toLowerCase() on the null reference without checking for null first.

The stack trace shows:
1. Line 67 in UserService.sendWelcomeEmail() - the failure point
2. Called from line 45 in UserController.createUser() - the entry point
3. HTTP request handler context - this is a web request

## Evidence
```java
// UserService.java:67 (problematic code)
String email = user.getEmail().toLowerCase();  // NPE here
```

The error message clearly states:
"Cannot invoke "String.toLowerCase()" because the return value of "com.example.model.User.getEmail()" is null"

## Solution

### Immediate Fix
Add null check before using email:

```java
// Option 1: Traditional null check
String email = user.getEmail();
if (email != null) {
    email = email.toLowerCase();
    // proceed with email sending
} else {
    throw new IllegalStateException("User email is required");
}

// Option 2: Use Optional (preferred)
String email = Optional.ofNullable(user.getEmail())
    .map(String::toLowerCase)
    .orElseThrow(() -> new IllegalStateException("User email is required"));
```

### Better Solution: Prevent at Source
Ensure email cannot be null in the first place:

```java
@Entity
public class User {
    @Column(nullable = false)  // Database constraint
    @NotNull  // Validation annotation
    @Email
    private String email;

    // Constructor that enforces email requirement
    public User(String name, @NonNull String email) {
        this.name = name;
        this.email = Objects.requireNonNull(email, "Email is required");
    }
}
```

## Prevention
1. Use Bean Validation (@NotNull, @NotBlank) on DTOs
2. Validate input at controller layer with @Valid
3. Consider using Optional<String> for nullable fields
4. Enable compiler null checking (use @NonNull annotations)
5. Add unit tests that verify null handling
```

### Example 2: ClassNotFoundException Analysis

**Input:**
```
java.lang.ClassNotFoundException: org.postgresql.Driver
    at java.base/jdk.internal.loader.BuiltinClassLoader.loadClass(BuiltinClassLoader.java:641)
    at java.base/jdk.internal.loader.ClassLoaders$AppClassLoader.loadClass(ClassLoaders.java:188)
    at java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:520)
    at java.lang.Class.forName0(Native Method)
    at java.lang.Class.forName(Class.java:375)
    at com.example.DatabaseConfig.getConnection(DatabaseConfig.java:23)
```

**Analysis:**
```markdown
## Problem Summary
PostgreSQL JDBC driver class not found at runtime, preventing database connection.

## Root Cause
The PostgreSQL JDBC driver dependency is either:
1. Not declared in project dependencies
2. Declared with wrong scope (e.g., 'provided' instead of 'runtime')
3. Not included in the final JAR/WAR package

The stack trace shows the application is trying to load the driver at line 23 of DatabaseConfig.java but the class is not available in the classpath.

## Evidence
```java
// DatabaseConfig.java:23
Class.forName("org.postgresql.Driver");  // Fails here
```

Check current dependencies:
```bash
mvn dependency:tree | grep postgresql
# or
gradle dependencies | grep postgresql
```

## Solution

### Maven (pom.xml)
Add PostgreSQL driver dependency:

```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <version>42.6.0</version>
    <scope>runtime</scope>
</dependency>
```

### Gradle (build.gradle)
```groovy
runtimeOnly 'org.postgresql:postgresql:42.6.0'
```

### Spring Boot (Simplified)
If using Spring Boot, just add:

```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

Version is managed by Spring Boot parent.

### Rebuild and Verify
```bash
# Maven
mvn clean install

# Gradle
gradle clean build

# Verify driver is in classpath
jar tf target/myapp.jar | grep postgresql
```

## Prevention
1. Declare all runtime dependencies explicitly
2. Use dependency management (Spring Boot parent, BOM)
3. Test with clean Maven/Gradle cache regularly
4. Include integration tests that verify database connectivity
5. Use tools like dependency-check to verify required dependencies
```

### Example 3: Memory Leak Analysis

**Input:**
```
java.lang.OutOfMemoryError: Java heap space
    at java.util.Arrays.copyOf(Arrays.java:3332)
    at java.lang.AbstractStringBuilder.ensureCapacityInternal(AbstractStringBuilder.java:124)
    at java.lang.AbstractStringBuilder.append(AbstractStringBuilder.java:448)
    at java.lang.StringBuilder.append(StringBuilder.java:141)
    at com.example.service.ReportService.generateReport(ReportService.java:89)

Heap dump analysis shows:
- UserSession objects: 150,000 instances (2.5 GB)
- Retained by: ServletContext attribute "activeSessions"
```

**Analysis:**
```markdown
## Problem Summary
OutOfMemoryError due to accumulation of UserSession objects never being removed from ServletContext, causing memory leak.

## Root Cause
The application stores UserSession objects in ServletContext but never removes them when users log out or sessions expire. Over time, these objects accumulate and exhaust heap memory.

Analysis of heap dump reveals:
- 150,000 UserSession instances consuming 2.5 GB
- All retained by ServletContext attribute "activeSessions"
- Many sessions are hours/days old (should have expired)

## Evidence
```java
// ReportService.java (where OOM occurred)
StringBuilder report = new StringBuilder();
for (UserSession session : activeSessions) {
    report.append(session.getDetails());  // Fails when processing large list
}
```

The StringBuilder itself isn't the problem - it's the 150,000 sessions in the list.

```java
// SessionManager.java (probable leak source)
@Component
public class SessionManager {
    private final Map<String, UserSession> activeSessions = new ConcurrentHashMap<>();

    public void addSession(String sessionId, UserSession session) {
        activeSessions.put(sessionId, session);
        // BUG: Never removes old sessions!
    }
}
```

## Solution

### Immediate: Increase Heap (Temporary)
```bash
java -Xmx4g -XX:+HeapDumpOnOutOfMemoryError -jar app.jar
```

### Proper Fix: Implement Session Cleanup
```java
@Component
@Slf4j
public class SessionManager {
    private final Map<String, UserSession> activeSessions = new ConcurrentHashMap<>();

    // Use HttpSessionListener to clean up sessions
    @EventListener
    public void onSessionCreated(HttpSessionCreatedEvent event) {
        String sessionId = event.getSession().getId();
        activeSessions.put(sessionId, new UserSession(sessionId));
        log.info("Session created: {}", sessionId);
    }

    @EventListener
    public void onSessionDestroyed(HttpSessionDestroyedEvent event) {
        String sessionId = event.getSession().getId();
        UserSession removed = activeSessions.remove(sessionId);
        log.info("Session destroyed: {}, removed: {}", sessionId, removed != null);
    }

    // Scheduled cleanup for stale sessions
    @Scheduled(fixedRate = 60000) // Every minute
    public void cleanupStaleSessions() {
        long now = System.currentTimeMillis();
        int removed = 0;

        Iterator<Map.Entry<String, UserSession>> iterator =
            activeSessions.entrySet().iterator();

        while (iterator.hasNext()) {
            Map.Entry<String, UserSession> entry = iterator.next();
            if (now - entry.getValue().getLastAccessTime() > 3600000) { // 1 hour
                iterator.remove();
                removed++;
            }
        }

        if (removed > 0) {
            log.info("Cleaned up {} stale sessions", removed);
        }
    }

    public int getActiveSessionCount() {
        return activeSessions.size();
    }
}
```

### Add Monitoring
```java
@RestController
@RequestMapping("/actuator")
public class SessionMetricsController {
    private final SessionManager sessionManager;

    @GetMapping("/sessions")
    public Map<String, Object> getSessionMetrics() {
        return Map.of(
            "activeCount", sessionManager.getActiveSessionCount(),
            "timestamp", Instant.now()
        );
    }
}
```

## Prevention
1. Always clean up resources (sessions, connections, files)
2. Use weak references for caches (WeakHashMap, Guava Cache)
3. Set max size limits on collections
4. Enable GC logging to monitor memory trends
5. Regular heap dump analysis in staging
6. Add metrics/alerts for collection sizes
7. Use profilers to detect leaks early (YourKit, JProfiler)

## Monitoring
```bash
# Enable GC logging
-Xlog:gc*:file=gc.log:time,uptime,level,tags

# Generate heap dump on OOM
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/logs/heap-dump.hprof

# Monitor with JVM metrics
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9010
```
```

### Example 4: Deadlock Analysis

**Input:**
```
Found one Java-level deadlock:
=============================
"Thread-1":
  waiting to lock monitor 0x00007f8a8c004e60 (object 0x00000007d5f5c1d0, a com.example.AccountService),
  which is held by "Thread-2"

"Thread-2":
  waiting to lock monitor 0x00007f8a8c004f10 (object 0x00000007d5f5c1e8, a com.example.TransactionService),
  which is held by "Thread-1"
```

**Analysis:**
```markdown
## Problem Summary
Deadlock detected between Thread-1 and Thread-2, each holding a lock the other needs.

## Root Cause
Classic deadlock scenario:
- Thread-1 holds lock on TransactionService, needs lock on AccountService
- Thread-2 holds lock on AccountService, needs lock on TransactionService

This occurs when two threads acquire locks in opposite order:

```java
// Thread-1 execution path
synchronized(transactionService) {     // Acquires lock A
    // ... do work ...
    synchronized(accountService) {      // Needs lock B (held by Thread-2)
        // ... never reached ...
    }
}

// Thread-2 execution path
synchronized(accountService) {          // Acquires lock B
    // ... do work ...
    synchronized(transactionService) {  // Needs lock A (held by Thread-1)
        // ... never reached ...
    }
}
```

## Evidence
Thread dump shows both threads in BLOCKED state, waiting indefinitely for locks held by each other.

## Solution

### Fix 1: Consistent Lock Ordering
Always acquire locks in the same order:

```java
// Both threads now acquire locks in same order
private static final Object LOCK_ORDER_1 = new Object();
private static final Object LOCK_ORDER_2 = new Object();

// Thread-1
synchronized(LOCK_ORDER_1) {
    synchronized(LOCK_ORDER_2) {
        // Process transaction
    }
}

// Thread-2
synchronized(LOCK_ORDER_1) {  // Same order!
    synchronized(LOCK_ORDER_2) {
        // Process account
    }
}
```

### Fix 2: Use Lock with Timeout
```java
Lock lockA = new ReentrantLock();
Lock lockB = new ReentrantLock();

try {
    if (lockA.tryLock(1, TimeUnit.SECONDS)) {
        try {
            if (lockB.tryLock(1, TimeUnit.SECONDS)) {
                try {
                    // Both locks acquired
                    processTransaction();
                } finally {
                    lockB.unlock();
                }
            } else {
                log.warn("Could not acquire lockB, aborting");
            }
        } finally {
            lockA.unlock();
        }
    }
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

### Fix 3: Redesign to Avoid Nested Locks
```java
// Instead of nested synchronization, use single lock
private final Object singleLock = new Object();

public void processTransaction() {
    synchronized(singleLock) {
        // All operations under single lock
        updateAccount();
        updateTransaction();
    }
}
```

## Prevention
1. Always acquire multiple locks in consistent order
2. Use timeout when acquiring locks (tryLock)
3. Minimize lock scope and duration
4. Avoid nested locks when possible
5. Use higher-level concurrency utilities (java.util.concurrent)
6. Enable deadlock detection in production
7. Add timeout alerts for long-running locks
```

## Requirements

### Tools
- JDK tools: jstack, jmap, jconsole, jvisualvm
- Thread dump analyzers: fastThread, Samurai
- Heap dump analyzers: Eclipse MAT, VisualVM, YourKit
- Log aggregation: ELK stack, Splunk, Datadog

### Useful JVM Flags
```bash
# Heap dumps on OOM
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/logs/

# GC logging
-Xlog:gc*:file=gc.log

# Thread dumps on demand
kill -3 <pid>  # Sends SIGQUIT to generate thread dump

# Remote monitoring
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9010
```

## Analysis Checklist

**For Exceptions:**
- [ ] Identify exception type and message
- [ ] Find root cause in "Caused by" chain
- [ ] Locate first application frame in stack trace
- [ ] Understand context from framework frames
- [ ] Check for common patterns (NPE, missing class, etc.)
- [ ] Verify configuration and dependencies

**For Performance Issues:**
- [ ] Identify bottleneck (CPU, memory, I/O, lock contention)
- [ ] Analyze thread dump for blocked/waiting threads
- [ ] Check GC logs for excessive garbage collection
- [ ] Review heap dump for large objects
- [ ] Examine database query performance
- [ ] Profile code with JProfiler/YourKit

**For Memory Leaks:**
- [ ] Capture heap dump when memory is high
- [ ] Identify largest objects and their references
- [ ] Look for growing collections
- [ ] Check for static references preventing GC
- [ ] Review listener registrations (not unregistered)
- [ ] Examine cache sizes and eviction policies

## Output Format

Always provide structured analysis:

```markdown
## Problem Summary
[One-line description]

## Root Cause
[Detailed explanation with evidence]

## Solution
[Step-by-step fix with code examples]

## Prevention
[How to avoid in future]

## Additional Notes
[Any relevant context, warnings, or follow-up actions]
```

## Error Handling

If analysis cannot be completed:

1. **Incomplete stack trace:** Request full stack trace with "Caused by" chain
2. **Missing context:** Ask for relevant code sections
3. **Need logs:** Request application logs around failure time
4. **Complex issue:** Request thread dump, heap dump, or GC logs
5. **Framework-specific:** Ask for framework version and configuration

Always provide best-effort analysis even with limited information, clearly stating assumptions and requesting additional data for definitive diagnosis.
