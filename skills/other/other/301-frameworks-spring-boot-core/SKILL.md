---
name: 301-frameworks-spring-boot-core
description: Use when you need to review, improve, or build Spring Boot applications — including proper usage of @SpringBootApplication, component annotations (@Controller, @Service, @Repository), bean definition and scoping, configuration classes and @ConfigurationProperties, component scanning, conditional configuration and profiles, constructor injection, bean minimization, and scheduled tasks. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Spring Boot Core Guidelines

Apply Spring Boot Core guidelines for annotations, bean management, configuration, and dependency injection.

**What is covered in this Skill?**

- @SpringBootApplication and main application class
- Component annotations: @RestController, @Service, @Repository
- Bean definition, scoping, lifecycle
- Configuration classes and @ConfigurationProperties
- Component scanning and package organization
- Conditional configuration and profiles
- Constructor dependency injection
- Bean minimization and composition
- Scheduled tasks and background processing

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any Spring Boot changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **SAFETY**: If compilation fails, stop immediately — compilation failure is a blocking condition
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules, good/bad patterns, and constraints

## When to use this skill

- Review Java code for Spring Boot application
- Apply best practices for Spring Boot application in Java code

## Reference

For detailed guidance, examples, and constraints, see [references/301-frameworks-spring-boot-core.md](references/301-frameworks-spring-boot-core.md).
