---
name: logback-config-rfc-27
description: >
  RFC-27 compliant static Logback configuration for Java services. Covers logback.xml
  structure, appenders, encoders, and deployment-specific configuration.
  Use when setting up or reviewing logging configuration in Java services.
compatibility: Java projects using Spring Boot with Logback
metadata:
  version: "1.0.0"
  technology: java
  category: observability
  tags:
    - java
    - logging
    - rfc-27
    - logback
    - configuration
---

# Logback Configuration (RFC-27)

RFC-27 compliant static Logback configuration for Java services.

## When to use this skill

- Setting up logging configuration for new Java services
- Reviewing or updating logback.xml configuration
- Configuring environment-specific logging
- Setting up log file rotation and retention
- Configuring appenders for different outputs (console, file, JSON)

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L24-L31)
- [Quick Start](#quick-start) (L52-L90)
- [Configuration Structure](#configuration-structure) (L91-L115)
- [Appender Types](#appender-types) (L116-L134)
- [Environment Configuration](#environment-configuration) (L135-L154)
- [References](#references) (L155-L160)
- [Related Rules](#related-rules) (L161-L164)
- [Related Skills](#related-skills) (L165-L170)

### Available Resources

**📚 references/** - Detailed documentation
- [configuration patterns](references/configuration-patterns.md)

---

## Quick Start

### 1. Create logback-spring.xml

Place in `src/main/resources/logback-spring.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration scan="true" scanPeriod="30 seconds">
    <include resource="org/springframework/boot/logging/logback/defaults.xml"/>

    <!-- Console appender for local development -->
    <springProfile name="local">
        <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
            <encoder>
                <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
            </encoder>
        </appender>
        <root level="INFO">
            <appender-ref ref="CONSOLE"/>
        </root>
    </springProfile>

    <!-- JSON appender for production -->
    <springProfile name="!local">
        <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
            <encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
        </appender>
        <root level="INFO">
            <appender-ref ref="JSON"/>
        </root>
    </springProfile>
</configuration>
```

### 2. Do NOT Commit logback.xml to Git

Per RFC-27, `logback.xml` should NOT be in version control. Use `logback-spring.xml` instead, which supports Spring profiles.

## Configuration Structure

### Required Elements

| Element | Purpose |
|---------|---------|
| `<configuration>` | Root element with optional scan attributes |
| `<appender>` | Defines output destination |
| `<encoder>` | Formats log messages |
| `<root>` | Default logging level |

### Spring Profile Integration

Use `<springProfile>` to apply configuration conditionally:

```xml
<springProfile name="production">
    <!-- Production-specific config -->
</springProfile>

<springProfile name="!production">
    <!-- Non-production config -->
</springProfile>
```

## Appender Types

| Appender | Use Case |
|----------|----------|
| `ConsoleAppender` | Standard output (container logs) |
| `RollingFileAppender` | File with rotation |
| `AsyncAppender` | Non-blocking wrapper |

### Console Appender (Production)

```xml
<appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LogstashEncoder">
        <includeMdcKeyName>traceId</includeMdcKeyName>
        <includeMdcKeyName>spanId</includeMdcKeyName>
    </encoder>
</appender>
```

## Environment Configuration

### Log Levels per Environment

| Environment | Root Level | Notes |
|-------------|------------|-------|
| `local` | DEBUG | Verbose for development |
| `development` | INFO | Standard logging |
| `staging` | INFO | Match production |
| `production` | INFO | Minimize noise |

### Logger Overrides

```xml
<!-- Reduce noise from specific libraries -->
<logger name="org.apache.kafka" level="WARN"/>
<logger name="org.springframework.web" level="INFO"/>
<logger name="com.bitso" level="DEBUG"/>
```

## References

| Reference | Description |
|-----------|-------------|
| [references/configuration-patterns.md](references/configuration-patterns.md) | Detailed configuration examples |

## Related Rules

- [java-structured-logs](.cursor/rules/java-structured-logs/java-structured-logs.mdc) - Structured logging standards (RFC-34)

## Related Skills

| Skill | Purpose |
|-------|---------|
| [structured-logs-rfc-34](.claude/skills/structured-logs-rfc-34/SKILL.md) | Structured logging format |
| [dynamic-loglevel-rfc-27](.claude/skills/dynamic-loglevel-rfc-27/SKILL.md) | Runtime log level control |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/logback-config-rfc-27/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

