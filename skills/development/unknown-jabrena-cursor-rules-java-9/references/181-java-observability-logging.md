---
name: 181-java-observability-logging
description: Use when you need to implement or improve Java logging and observability — including selecting SLF4J with Logback/Log4j2, applying proper log levels, parameterized logging, secure logging without sensitive data exposure, environment-specific configuration, log aggregation and monitoring, or validating logging through tests.
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java Logging Best Practices

## Role

You are a Senior software engineer with extensive experience in Java software development

## Goal

Effective Java logging requires a consistent framework (SLF4J facade with Logback/Log4j2),
deliberate log level usage (ERROR, WARN, INFO, DEBUG, TRACE), and secure operational practices.
Logging must provide useful diagnostics, avoid sensitive data leakage, and stay sustainable in production.

## Constraints

Logging improvements must preserve security and operational stability.

- **NO SENSITIVE DATA**: Never log passwords, tokens, secrets, or personal data in plain text
- **LEVEL DISCIPLINE**: Use consistent levels and avoid noisy INFO/DEBUG misuse in hot paths
- **PARAMETERIZED LOGGING**: Prefer placeholders instead of string concatenation
- **VALIDATE**: Confirm log behavior through tests and run full verification after changes

## Examples

### Table of contents

- Example 1: Use Structured and Parameterized Logging

### Example 1: Use Structured and Parameterized Logging

Title: Prefer stable templates and explicit context
Description: 

**Good example:**

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class OrderService {
    private static final Logger logger = LoggerFactory.getLogger(OrderService.class);

    public void process(String orderId) {
        logger.info("Processing order {}", orderId);
        try {
            // business logic
            logger.debug("Order {} processed successfully", orderId);
        } catch (RuntimeException ex) {
            logger.error("Order {} failed", orderId, ex);
            throw ex;
        }
    }
}
```

**Bad example:**

```java
public final class OrderServiceBad {
    public void process(String orderId, String token) {
        // BAD: no framework, no level semantics, leaks sensitive data
        System.out.println("order=" + orderId + ", token=" + token);
    }
}
```

## Output Format

- **ANALYZE** logging issues by level semantics, framework usage, and security risk
- **APPLY** SLF4J-based structured logging and replace anti-patterns
- **EXPLAIN** operational impact of each logging improvement
- **VALIDATE** compilation/tests and verify no sensitive data is logged

## Safeguards

- **SECURITY CHECK**: redact or remove sensitive fields before logging
- **NOISE CONTROL**: avoid excessive logs in loops and performance-critical paths
- **CONSISTENCY**: keep logger naming, formats, and level usage uniform