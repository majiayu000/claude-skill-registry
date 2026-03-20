---
name: 180-java-observability-logging
description: Use when you need to implement or improve Java logging and observability — including selecting SLF4J with Logback/Log4j2, applying proper log levels (ERROR, WARN, INFO, DEBUG, TRACE), parameterized logging, secure logging without sensitive data exposure, environment-specific configuration, log aggregation and monitoring, or validating logging through tests. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java Logging Best Practices

Implement effective Java logging following standardized frameworks, meaningful log levels, core practices (parameterized logging, exception handling, no sensitive data), flexible configuration, security-conscious logging, monitoring and alerting, and comprehensive logging validation through testing.

**What is covered in this Skill?**

- Standardized framework selection: SLF4J facade with Logback or Log4j2
- Meaningful and consistent log levels: ERROR, WARN, INFO, DEBUG, TRACE
- Core practices: parameterized logging, proper exception handling, avoiding sensitive data
- Configuration: environment-specific (logback.xml, log4j2.xml), output formats, log rotation
- Security: mask sensitive data, control log access, secure transmission, GDPR/HIPAA compliance
- Log monitoring and alerting: centralized aggregation (ELK, Splunk, Loki), automated alerts
- Logging validation through testing: assert log messages, verify formats, test levels, measure performance impact

**Scope:** The reference is organized by examples (good/bad code patterns) for each core area. Apply recommendations based on applicable examples.

## Constraints

Before applying any logging recommendations, ensure the project compiles. Compilation failure is a blocking condition. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately — do not proceed until resolved
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed good/bad examples, constraints, and safeguards for each logging pattern

## When to use this skill

- Review Java code for logging and observability
- Apply best practices for logging and observability in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/180-java-observability-logging.md](references/180-java-observability-logging.md).
