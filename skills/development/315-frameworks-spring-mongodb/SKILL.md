---
name: 315-frameworks-spring-mongodb
description: Use when you need to design or implement MongoDB data access in Spring Boot — including document modeling, Spring Data Mongo repositories/templates, indexing, optimistic concurrency, and error handling. This should trigger for requests such as Add MongoDB in Spring Boot; Review Spring Data Mongo design; Improve error handling for Mongo writes. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Spring Boot — MongoDB

Apply Spring Data MongoDB guidance with concrete examples for design, implementation, and error handling.

## Constraints

Compile before MongoDB refactors; verify after changes.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add MongoDB in Spring Boot
- Review Spring Data Mongo repositories/documents
- Improve duplicate key handling, retries, or optimistic locking in Mongo flows

## Workflow

1. **Read reference and assess project context**

Read `references/315-frameworks-spring-mongodb.md` and inspect persistence setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify data model, consistency, and query requirements to define safe improvements.

3. **Apply framework-aligned changes**

Implement/refactor mappings, repositories, indexes, and failure handling policies.

4. **Run verification and report results**

Execute build/tests and summarize what changed, what was verified, and follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/315-frameworks-spring-mongodb.md](references/315-frameworks-spring-mongodb.md).
