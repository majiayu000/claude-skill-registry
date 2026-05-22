---
name: 503-frameworks-micronaut-validation
description: Use when you need to design, review, or improve validation in Micronaut applications — including Bean Validation on @Controller methods, @Body @Valid, query/path parameter validation, @ConfigurationProperties validation, custom constraints, nested DTO validation, and ExceptionHandler mapping for constraint violations. This should trigger for requests such as Add validation support in Micronaut; Review Micronaut validation rules; Improve request validation in Micronaut REST APIs; Add custom validation constraints in Micronaut; Validate Micronaut configuration properties. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Micronaut Validation Guidelines

Apply Micronaut validation best practices at HTTP API boundaries.

**What is covered in this Skill?**

- Bean Validation annotations on DTOs and command models
- @Valid / @Validated usage in Micronaut controllers
- Validation groups and custom validators
- Consistent mapping of validation failures to 400 responses
- Safe and predictable validation error payloads

**Scope:** Apply recommendations based on the reference rules and good/bad examples.

## Constraints

Before applying validation changes, ensure the project compiles. After improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add validation support in Micronaut
- Review Micronaut validation rules
- Improve request validation in Micronaut REST APIs
- Add custom validation constraints in Micronaut
- Validate Micronaut configuration properties
- Improve constraint violation handling in Micronaut

## Workflow

1. **Read reference and assess project context**

Read `references/503-frameworks-micronaut-validation.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor validation-related configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/503-frameworks-micronaut-validation.md](references/503-frameworks-micronaut-validation.md).
