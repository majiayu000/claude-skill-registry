---
name: 314-frameworks-spring-kafka
description: Use when you need to design or implement Kafka messaging in Spring Boot — including topic design, producer/consumer implementation, JSON serialization with Boot factory customizers, Testcontainers `@ServiceConnection` integration tests, retries and dead-letter topics, idempotency, and error handling. This should trigger for requests such as Add Kafka in Spring Boot; Review Spring Kafka consumers; Improve retries and DLT in Spring Kafka. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Spring Boot — Kafka messaging

Apply Spring Kafka guidance with concrete examples for design, implementation, and error handling.

## Constraints

Compile before messaging refactors; verify after changes.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add Kafka in Spring Boot
- Review Spring Kafka consumers/producers
- Improve retries, dead-letter topics, or idempotency in Spring Kafka

## Workflow

1. **Read reference and assess project context**

Read `references/314-frameworks-spring-kafka.md` and inspect current messaging setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify reliability and throughput goals and define the minimum safe set of changes.

3. **Apply framework-aligned changes**

Implement/refactor Spring Kafka configuration, producer/consumer logic, and failure handling.

4. **Run verification and report results**

Execute build/tests and summarize what changed, what was verified, and follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/314-frameworks-spring-kafka.md](references/314-frameworks-spring-kafka.md).
