---
name: 414-frameworks-quarkus-kafka
description: Use when you need Kafka messaging in Quarkus with SmallRye Reactive Messaging — including channel/topic design, serialization, ack/failure strategies, retries/DLQ, and error handling. This should trigger for requests such as Add Kafka in Quarkus; Review Reactive Messaging consumers; Improve failure handling for Quarkus Kafka. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Quarkus — Kafka messaging

Apply Quarkus Kafka guidance with concrete examples for design, implementation, and error handling.

## Constraints

Compile before messaging refactors; verify after changes.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add Kafka in Quarkus
- Review Quarkus Reactive Messaging consumers/producers
- Improve retries, dead-letter handling, or idempotency in Quarkus Kafka

## Workflow

1. **Read reference and assess project context**

Read `references/414-frameworks-quarkus-kafka.md` and inspect current messaging setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify delivery semantics and resilience goals to define safe improvements.

3. **Apply framework-aligned changes**

Implement/refactor channels, serializers, and failure strategies in Reactive Messaging.

4. **Run verification and report results**

Execute build/tests and summarize what changed, what was verified, and follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/414-frameworks-quarkus-kafka.md](references/414-frameworks-quarkus-kafka.md).
