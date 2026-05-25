---
name: 515-frameworks-micronaut-mongodb
description: Use when you need MongoDB persistence in Micronaut — including @MongoRepository design, document modeling, indexes, query patterns, and error handling. This should trigger for requests such as Add MongoDB in Micronaut; Review Micronaut Data Mongo design; Improve error handling for Micronaut Mongo operations. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Micronaut — MongoDB

Apply Micronaut MongoDB guidance with concrete examples for design, implementation, and error handling.

## Constraints

Compile before MongoDB refactors; verify after changes.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add MongoDB in Micronaut
- Review Micronaut Mongo entities/repositories
- Improve duplicate key handling, retries, or optimistic locking in Micronaut Mongo

## Workflow

1. **Read reference and assess project context**

Read `references/515-frameworks-micronaut-mongodb.md` and inspect persistence setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify model and consistency requirements and define safe improvements.

3. **Apply framework-aligned changes**

Implement/refactor documents, repositories, indexes, and error handling.

4. **Run verification and report results**

Execute build/tests and summarize what changed, what was verified, and follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/515-frameworks-micronaut-mongodb.md](references/515-frameworks-micronaut-mongodb.md).
