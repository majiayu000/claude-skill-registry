---
name: 302-frameworks-spring-boot-rest
description: Use when you need to design, review, or improve REST APIs with Spring Boot — including HTTP methods, resource URIs, status codes, DTOs, versioning, error handling, security, API documentation, controller advice, and problem details for errors. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java REST API Design Principles

Apply REST API design principles for Spring Boot applications.

**What is covered in this Skill?**

- HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Resource URI design
- HTTP status codes
- Request/response DTOs
- API versioning
- Error handling
- API security
- Documentation (OpenAPI)
- Controller advice and problem details

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any REST API changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and good/bad patterns

## When to use this skill

- Review Java code for Spring Boot REST API
- Apply best practices for Spring Boot REST API in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/302-frameworks-spring-boot-rest.md](references/302-frameworks-spring-boot-rest.md).
