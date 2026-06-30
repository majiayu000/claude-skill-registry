---
name: 123-java-design-patterns
description: Use when you need to select, review, or implement Java design and integration patterns — including classic Java design patterns, REST API patterns, Kafka and event-driven patterns, database and persistence patterns, and cross-cutting integration patterns. This should trigger for requests such as Apply Java design patterns; Review REST API patterns; Design Kafka event-driven patterns; Improve database persistence patterns; Add resilient integration patterns. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Java Design and Integration Patterns

Guide Java developers in selecting patterns by problem signal, implementation context, and trade-off rather than by pattern name alone.

**What is covered in this Skill?**

- Classic Java design patterns for application code: creational, structural, and behavioral patterns
- REST API patterns for resource design, contracts, idempotency, versioning, and error handling
- Kafka and event-driven patterns for event schemas, partitioning, idempotency, retries, outbox, and sagas
- Database and persistence patterns for repositories, transactions, aggregates, locking, migrations, and read models
- Cross-cutting integration patterns for anti-corruption layers, resilience, observability, and reliable message boundaries

**Scope:** Use this skill to explain, review, and implement practical patterns in Java systems. Prefer simple code first; introduce a pattern only when it reduces real complexity, protects a boundary, improves testability, or makes change safer.

## Constraints

Pattern guidance must be problem-led, concrete, and safe to apply in Java projects.

- **PROBLEM FIRST**: Identify the design pressure before naming or applying a pattern
- **NO PATTERN SHOPPING**: Do not add abstractions only because a pattern exists; prefer simple code when variation is not present
- **BUILD SAFETY**: For code changes, run `./mvnw compile` or `mvn compile` before refactoring and `./mvnw clean verify` or `mvn clean verify` after changes
- **REFERENCE SELECTION**: Read the relevant reference before acting: Java code patterns, REST API patterns, Kafka/event-driven patterns, database/persistence patterns, or cross-cutting integration patterns
- **TRADE-OFFS REQUIRED**: Explain the benefit, cost, and when-not-to-use guidance for any recommended pattern

## When to use this skill

- Apply Java design patterns
- Review Java code for design patterns
- Choose REST API patterns
- Design Kafka event-driven patterns
- Improve database persistence patterns
- Add resilient integration patterns

## Workflow

1. **Identify the design pressure**

Clarify the concrete problem: object creation, behavior variation, API contract evolution, event delivery, persistence consistency, integration reliability, or another recurring design force.

2. **Select the relevant reference**

Read only the matching reference(s): `references/123-java-design-patterns.md`, `references/123-rest-api-patterns.md`, `references/123-kafka-event-driven-patterns.md`, `references/123-database-persistence-patterns.md`, or `references/123-cross-cutting-integration-patterns.md`.

3. **Recommend the smallest useful pattern**

Choose the simplest pattern that addresses the design pressure. Show how it changes responsibilities, boundaries, tests, operations, or evolution safety.

4. **Implement or document the pattern**

When code changes are requested, make focused Java or configuration changes following the project conventions. When design advice is requested, provide diagrams, examples, request/response shapes, event shapes, or transaction flows as appropriate.

5. **Validate the outcome**

Verify that the resulting design remains understandable, testable, and operationally safe. Run the project build for code changes and name any remaining trade-offs.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/123-java-design-patterns.md](references/123-java-design-patterns.md)
- [references/123-rest-api-patterns.md](references/123-rest-api-patterns.md)
- [references/123-kafka-event-driven-patterns.md](references/123-kafka-event-driven-patterns.md)
- [references/123-database-persistence-patterns.md](references/123-database-persistence-patterns.md)
- [references/123-cross-cutting-integration-patterns.md](references/123-cross-cutting-integration-patterns.md)
