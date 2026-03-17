---
name: java-best-practices-debug-analyzer
description: |
  Analyzes Java stack traces, diagnoses exceptions, identifies root causes, and troubleshoots
  performance problems. Deconstructs stack traces, investigates NullPointerException,
  analyzes thread dumps, detects memory leaks, and resolves ClassNotFoundException.
  Use when debugging Java errors, analyzing stack traces, investigating exceptions,
  or troubleshooting performance issues.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

Works with Java exception logs, thread dumps, heap dumps, and error messages.
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


## Supporting Files

| File | Purpose |
|------|---------|
| `examples/debug-examples.md` | Comprehensive debugging examples (NullPointerException, ClassNotFoundException, OutOfMemoryError) |

## Requirements

- Java development experience
- Understanding of stack traces
- Familiarity with Java exceptions
- Basic knowledge of JVM internals (for memory/thread issues)

## Red Flags to Avoid

- [ ] Do not ignore root causes - treat symptoms only temporarily
- [ ] Do not skip stack trace analysis - every line contains clues
- [ ] Do not assume - verify with evidence from logs/code
- [ ] Do not provide generic solutions - tailor to specific error
- [ ] Do not forget prevention - suggest long-term fixes
- [ ] Do not ignore thread dumps - they reveal concurrency issues
- [ ] Do not overlook memory patterns - heap dumps show object retention

## Notes

- Always analyze the full stack trace, not just the first line
- Root cause is often several frames deep in the stack
- Consider the context: production load, data volume, timing
- Memory issues often have delayed manifestations
- Thread dumps require comparing multiple snapshots
- ClassNotFoundException vs NoClassDefFoundError are different issues
- Performance problems often stem from inefficient algorithms or database queries
