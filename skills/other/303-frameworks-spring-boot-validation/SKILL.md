---
name: 303-frameworks-spring-boot-validation
description: Use when you need to design, review, or improve validation in Spring Boot applications — including Bean Validation on request DTOs, @Valid/@Validated at API boundaries, constraint groups, custom constraints, @ConfigurationProperties validation, nested DTO validation, and consistent validation error handling. This should trigger for requests such as Add validation support in Spring Boot; Review Spring Boot validation rules; Improve request validation in Spring Boot REST APIs; Add custom Bean Validation constraints in Spring Boot; Validate configuration properties in Spring Boot. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Spring Boot Validation Guidelines

Apply Spring Boot validation best practices at API boundaries.

**What is covered in this Skill?**

- Bean Validation annotations on DTOs and command models
- @Valid / @Validated on controllers and method parameters
- Validation groups for create/update workflows
- Custom constraint annotations and validators
- Consistent 400 error responses for validation failures

**Scope:** Apply recommendations based on the reference rules and good/bad examples.

## Constraints

Before applying validation changes, ensure the project compiles. After improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add validation support in Spring Boot
- Review Spring Boot validation rules
- Improve request validation in Spring Boot REST APIs
- Add custom Bean Validation constraints in Spring Boot
- Validate configuration properties in Spring Boot
- Improve nested DTO validation in Spring Boot

## Workflow

1. **Read reference and assess project context**

Read `references/303-frameworks-spring-boot-validation.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor validation-related configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/303-frameworks-spring-boot-validation.md](references/303-frameworks-spring-boot-validation.md).
