---
name: 403-frameworks-quarkus-validation
description: Use when you need to design, review, or improve validation in Quarkus applications — including Bean Validation on JAX-RS resources, @Valid on parameters and CDI beans, constraint groups, @ConfigMapping validation, custom constraints, nested DTO validation, and ExceptionMapper-based error mapping. This should trigger for requests such as Add validation support in Quarkus; Review Quarkus validation rules; Improve request validation in Quarkus REST APIs; Add custom validation constraints in Quarkus; Validate Quarkus @ConfigMapping properties. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Quarkus Validation Guidelines

Apply Quarkus validation best practices at REST boundaries.

**What is covered in this Skill?**

- Bean Validation annotations on DTOs and command models
- @Valid and boundary validation in Jakarta REST resources
- Validation groups and custom constraints
- Validation error mapping for client-safe responses
- Consistent handling of invalid inputs across endpoints

**Scope:** Apply recommendations based on the reference rules and good/bad examples.

## Constraints

Before applying validation changes, ensure the project compiles. After improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules and examples

## When to use this skill

- Add validation support in Quarkus
- Review Quarkus validation rules
- Improve request validation in Quarkus REST APIs
- Add custom validation constraints in Quarkus
- Validate Quarkus @ConfigMapping properties
- Improve validation error mapping with ExceptionMapper in Quarkus

## Workflow

1. **Read reference and assess project context**

Read `references/403-frameworks-quarkus-validation.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor validation-related configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/403-frameworks-quarkus-validation.md](references/403-frameworks-quarkus-validation.md).
