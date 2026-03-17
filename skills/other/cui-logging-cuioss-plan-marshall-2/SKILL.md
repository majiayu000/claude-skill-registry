---
name: cui-logging
description: CUI logging standards with CuiLogger, LogRecord patterns, and DSL-style LogMessages classes
user-invocable: false
allowed-tools: Read, Grep, Glob
---

# CUI Logging Skill

**REFERENCE MODE**: This skill provides reference material. Load specific standards on-demand based on current task.

CUI-specific logging standards for projects using the CUI logging framework (cui-java-tools). This skill covers CuiLogger usage, LogRecord patterns, and DSL-style LogMessages classes.

## Prerequisites

This skill requires CUI library dependencies:
- `de.cuioss:cui-java-tools` (CuiLogger, LogRecord)

## Workflow

### Step 1: Load Core Logging Standards

**CRITICAL**: Load these standards for any logging-related work.

```
Read: standards/logging-standards.md
```

This provides the foundational rules:
- MUST use `CuiLogger` (SLF4J/Log4j FORBIDDEN)
- MUST use `LogRecord` for INFO/WARN/ERROR/FATAL levels
- Exception parameter MUST come first in all logging calls

### Step 2: Load Additional Standards (As Needed)

**DSL Constants Pattern** (load when creating LogMessages classes):
```
Read: standards/dsl-constants.md
```

Use when: Implementing DSL-style LogMessages classes with nested static classes and @UtilityClass pattern.

**LogMessages Documentation** (load when documenting):
```
Read: standards/logmessages-documentation.md
```

Use when: Writing AsciiDoc documentation for LogMessages classes.

**Logging Maintenance** (load for migration/refactoring):
```
Read: standards/logging-maintenance-reference.md
```

Use when: Large-scale logger migration, LogRecord implementation, or maintenance work.

## Key Rules Summary

### CuiLogger Usage
```java
// CORRECT
private static final CuiLogger LOGGER = new CuiLogger(MyClass.class);

// FORBIDDEN - Never use SLF4J or Log4j directly
private static final Logger LOGGER = LoggerFactory.getLogger(MyClass.class);
```

### LogRecord for Structured Messages
```java
// CORRECT - Use LogRecord for INFO and above
LOGGER.info(INFO.getResolver().formatted("Processing completed"));
LOGGER.warn(WARN.getResolver().formatted("Resource low: %s", resourceName));
LOGGER.error(exception, ERROR.getResolver().formatted("Failed to process"));

// DEBUG/TRACE - Direct logging allowed (no LogRecord needed)
LOGGER.debug("Debug message: %s", value);
```

### Exception Handling
```java
// CORRECT - Exception FIRST
LOGGER.error(exception, ERROR.getResolver().formatted("Operation failed"));

// WRONG - Exception position
LOGGER.error(ERROR.getResolver().formatted("Operation failed"), exception);
```

## Related Skills

- `pm-dev-java:java-core` - General Java patterns (no CUI dependencies)
- `pm-dev-java-cui:cui-testing` - CUI test utilities including JUL testing with LogAsserts

## Standards Reference

| Standard | Purpose |
|----------|---------|
| logging-standards.md | Core CuiLogger, LogRecord rules, and compliance verification |
| dsl-constants.md | DSL-style constant organization |
| logmessages-documentation.md | AsciiDoc documentation patterns |
| logging-maintenance-reference.md | Migration and maintenance |
