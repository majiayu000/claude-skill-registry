---
name: dynamic-loglevel-rfc-27
description: >
  RFC-27 compliant runtime log level control for Java services. Covers proper log level
  usage, enabling dynamic log levels in estate-catalog, and changing levels via Developer
  Portal or Bitso CLI. Use when debugging production issues or configuring logging for services.
compatibility: Java projects using Spring Boot
metadata:
  version: "2.0.0"
  technology: java
  category: observability
  tags:
    - java
    - logging
    - rfc-27
    - developer-portal
    - bitso-cli
    - estate-catalog
---

# Dynamic Log Level (RFC-27)

RFC-27 compliant runtime log level control for Java services. This skill covers proper log level usage, enabling the feature for your service, and changing levels at runtime.

## When to Use This Skill

- Understanding which log level to use for different scenarios
- Enabling dynamic log level support for a new service
- Changing log levels at runtime for debugging
- Using Developer Portal or Bitso CLI to manage log levels

## Skill Contents

- [Log Level Best Practices](#log-level-best-practices) - Choosing the right level and logging guidelines
- [Enabling Dynamic Log Levels](#enabling-dynamic-log-levels) - Estate catalog configuration
- [Using Dynamic Log Levels](#using-dynamic-log-levels) - Developer Portal and Bitso CLI
- [Operational Workflows](#operational-workflows) - Debugging and bulk operations
- [References](#references) - Official documentation
- [Related Skills](#related-skills) - Logback and structured logging

---

## Log Level Best Practices

### Choosing the Right Level

| Level | When to Use | Examples |
|-------|-------------|----------|
| `ERROR` | Unexpected failures requiring immediate attention | Exception handling, failed transactions, service unavailable |
| `WARN` | Potential issues that don't stop execution | Deprecated API usage, retry attempts, fallback activated |
| `INFO` | Key business events and operational milestones | Request received, transaction completed, service started |
| `DEBUG` | Detailed information for troubleshooting | Method parameters, intermediate calculations, state changes |
| `TRACE` | Extremely detailed (rarely used in production) | Loop iterations, byte-level data, framework internals |

### Logging Guidelines

**DO:**

```java
// ERROR - Actual failure with context
log.error("Payment processing failed for orderId={}, userId={}", orderId, userId, exception);

// WARN - Recoverable issue
log.warn("Rate limit approaching for userId={}, currentRate={}", userId, rate);

// INFO - Business event (no sensitive data)
log.info("Order completed: orderId={}, amount={}", orderId, amount);

// DEBUG - Technical details for troubleshooting
log.debug("Validating request payload: size={}, headers={}", payload.size(), headers);
```

**DON'T:**

```java
// ❌ Don't log sensitive data
log.info("User logged in: email={}, password={}", email, password);

// ❌ Don't use ERROR for expected conditions
log.error("User not found"); // Use WARN or DEBUG

// ❌ Don't log without context
log.error("Failed"); // What failed? Where? Why?

// ❌ Don't use string concatenation
log.info("Processing order " + orderId); // Use parameterized logging
```

### Consistent Logging Across Services

- Use structured logging (see `structured-logs-rfc-34` skill)
- Include correlation IDs in all logs
- Log entry/exit for critical operations at DEBUG level
- Default production level: `INFO` for `com.bitso.*`

---

## Enabling Dynamic Log Levels

### Prerequisites

Your service must be registered in estate-catalog. Most Bitso Spring Boot services already have the necessary infrastructure.

### Step 1: Register in Estate Catalog

To enable dynamic log levels via Developer Portal and Bitso CLI, add the `logs` configuration to your entity's `.cue` file in estate-catalog.

1. **Open a PR to estate-catalog** updating your entity file:

```cue
// catalog/entities/my-service.cue
{
    // ... existing configuration
    logs: {
        format:     "json"       // or "plain-text" for non-structured logs
        management: "managed"    // This enables dynamic log levels
    }
    // ... rest of configuration
}
```

1. **Merge the PR** - Dynamic log levels will be available after the next estate-catalog sync

### Step 2: Verify Setup

After registration, verify your service appears in the Developer Portal under the observability section with log level controls available.

---

## Using Dynamic Log Levels

### Option 1: Developer Portal (Recommended)

The Developer Portal provides a user-friendly interface for managing log levels.

1. Navigate to **Developer Portal** → **Services** → **Your Service**
2. Go to the **Observability** tab
3. Select **Log Levels** section
4. Choose the specific logger class (e.g., `com.bitso.myservice.processor.OrderProcessor`)
   - **Tip**: Start with the most specific logger to minimize log noise
   - Only broaden to package level if the specific class doesn't help
5. Select the desired level from the dropdown
6. Click **Apply**

The change takes effect immediately across all instances.

### Option 2: Bitso CLI

For command-line access or automation:

```bash
# List current log levels for a service
bitso logs level list --service my-service

# Get level for a specific logger (use specific class for targeted debugging)
bitso logs level get --service my-service --logger com.bitso.payments.processor.PaymentProcessor

# Set log level (prefer specific class over full package)
bitso logs level set --service my-service --logger com.bitso.payments.processor.PaymentProcessor --level DEBUG

# Reset to default
bitso logs level reset --service my-service --logger com.bitso.payments.processor.PaymentProcessor

# Set temporary level (auto-resets after duration)
bitso logs level set --service my-service --logger com.bitso.payments.processor.PaymentProcessor --level DEBUG --duration 30m
```

### Available Log Levels

| Level | Description |
|-------|-------------|
| `TRACE` | Most detailed logging |
| `DEBUG` | Development and troubleshooting |
| `INFO` | Normal operations (default) |
| `WARN` | Potential issues |
| `ERROR` | Errors only |
| `OFF` | Disable logging for this logger |

---

## Operational Workflows

### Debugging a Production Issue

1. **Identify the specific class/logger** causing the issue (prefer specific class over full package)
2. **Set DEBUG level temporarily**:

   ```bash
   # Target the specific class first for minimal log noise
   bitso logs level set --service my-service --logger com.bitso.payments.processor.PaymentProcessor --level DEBUG --duration 15m
   
   # Only broaden to package if needed
   bitso logs level set --service my-service --logger com.bitso.payments.processor --level DEBUG --duration 15m
   ```

3. **Reproduce the issue** and capture logs
4. **Level auto-resets** after the duration expires
5. **Analyze logs** in Datadog/observability platform

### Bulk Operations for Related Services

When debugging a flow across multiple services (use sparingly - prefer specific loggers):

```bash
# Set DEBUG on a specific component across services
for service in order-service payment-service notification-service; do
  bitso logs level set --service $service --logger com.bitso.common.validation.RequestValidator --level DEBUG --duration 30m
done
```

### Audit Trail

All log level changes are audited:

- **Who** made the change
- **When** it was made
- **What** was changed (logger, old level, new level)
- **Duration** if temporary

View audit logs in the Developer Portal or via:

```bash
bitso logs level history --service my-service
```

---

## References

| Reference | Description |
|-----------|-------------|
| [Confluence: How to use dynamic log level](https://bitsomx.atlassian.net/wiki/spaces/BAB/pages/4927455595) | Official documentation |

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| [logback-config-rfc-27](.claude/skills/logback-config-rfc-27/SKILL.md) | Static Logback configuration |
| [structured-logs-rfc-34](.claude/skills/structured-logs-rfc-34/SKILL.md) | Structured logging format |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/dynamic-loglevel-rfc-27/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

