---
name: 514-frameworks-micronaut-kafka
description: Use when you need Kafka messaging in Micronaut — including @KafkaClient and @KafkaListener design, @Serdeable serialization, topic/partition strategy, TestPropertyProvider integration tests, retries and dead-letter processing, and error handling. This should trigger for requests such as Add Kafka in Micronaut; Review Micronaut Kafka listeners; Improve retry and failure handling for Micronaut Kafka. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Micronaut — Kafka messaging

Apply Micronaut Kafka guidance with concrete examples for design, implementation, and error handling.

## Constraints

Compile before messaging refactors; verify after changes.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add Kafka in Micronaut
- Review Micronaut Kafka consumers/producers
- Improve retries, dead-letter handling, or idempotency in Micronaut Kafka

## Workflow

1. **Read reference and assess project context**

Read `references/514-frameworks-micronaut-kafka.md` and inspect current messaging setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify delivery guarantees and resilience requirements to define safe improvements.

3. **Apply framework-aligned changes**

Implement/refactor clients, listeners, and failure strategies in Micronaut Kafka.

4. **Run verification and report results**

Execute build/tests and summarize what changed, what was verified, and follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/514-frameworks-micronaut-kafka.md](references/514-frameworks-micronaut-kafka.md).
