---
name: 415-frameworks-quarkus-mongodb
description: Use when you need MongoDB persistence in Quarkus — including Panache Mongo entities/repositories, document design, indexes, transactions where applicable, and error handling. This should trigger for requests such as Add MongoDB in Quarkus; Review Quarkus Mongo Panache design; Improve Mongo error handling in Quarkus services. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Quarkus — MongoDB

Apply Quarkus MongoDB guidance with concrete examples for design, implementation, and error handling.

## Constraints

Compile before MongoDB refactors; verify after changes.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add MongoDB in Quarkus
- Review Quarkus Mongo Panache entities/repositories
- Improve duplicate key handling, retry policy, or optimistic locking in Quarkus Mongo

## Workflow

1. **Read reference and assess project context**

Read `references/415-frameworks-quarkus-mongodb.md` and inspect persistence setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify model/query consistency needs and define safe improvements.

3. **Apply framework-aligned changes**

Implement/refactor Panache Mongo mappings, repository access, and failure handling.

4. **Run verification and report results**

Execute build/tests and summarize what changed, what was verified, and follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/415-frameworks-quarkus-mongodb.md](references/415-frameworks-quarkus-mongodb.md).
