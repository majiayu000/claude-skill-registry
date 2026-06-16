---
name: 305-frameworks-spring-boot-modulith
description: Use when you need to design, review, or improve modular monoliths with Spring Modulith in Spring Boot applications - including application module package structure, ApplicationModules verification, named interfaces, allowed dependencies, domain events, @ApplicationModuleTest, Scenario-based module tests, generated documentation, actuator exposure, observability, and event publication registry choices. This should trigger for requests such as Add Spring Modulith to a Spring Boot application; Review Spring Modulith module boundaries; Improve modular monolith architecture in Spring Boot; Add @ApplicationModuleTest tests; Generate Spring Modulith documentation. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Spring Boot - Spring Modulith

Apply Spring Modulith guidelines for Spring Boot modular monoliths.

**What is covered in this Skill?**

- Spring Modulith BOM and starter dependency selection
- Business-capability package structure for application modules
- ApplicationModules verification and architecture tests
- Named interfaces and explicit allowed dependencies
- Domain events for loose coupling between modules
- @ApplicationModuleTest and Scenario-based module integration tests
- Generated module documentation, actuator exposure, and observability
- Event publication registry choices for reliable domain events

**Scope:** Apply recommendations based on the reference rules, official Spring Modulith documentation, and good/bad examples.

## Constraints

Before applying Spring Modulith changes, ensure the project compiles. After improvements, run full verification including module structure tests.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **PRECONDITION**: The project must be a Spring Boot application; for non-Boot Java modularity use architecture or design skills instead
- **BASELINE**: Align dependency choices with Spring Boot 4.0.x and the Spring Modulith compatibility matrix
- **SAFETY**: If compilation fails, stop immediately
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules, good/bad patterns, and official documentation links

## When to use this skill

- Add Spring Modulith to a Spring Boot application
- Review Spring Modulith module boundaries
- Improve modular monolith architecture in Spring Boot
- Add @ApplicationModuleTest tests
- Generate Spring Modulith documentation
- Refactor Spring Boot modules with Spring Modulith

## Workflow

1. **Read reference and inspect project structure**

Read `references/305-frameworks-spring-boot-modulith.md` and inspect the Spring Boot version, Maven dependencies, main application package, and current package/module boundaries.

2. **Model application modules**

Identify business-capability modules, public APIs, internal packages, named interfaces, and intentional allowed dependencies.

3. **Apply framework-aligned changes**

Add or refine Spring Modulith dependencies, package annotations, architecture verification tests, domain events, and module tests following the reference patterns.

4. **Run verification and report results**

Execute appropriate build/tests, especially `ApplicationModules.verify()` and `@ApplicationModuleTest` coverage, then summarize changes, risks, and follow-up module design work.

## Reference

For detailed guidance, examples, and constraints, see [references/305-frameworks-spring-boot-modulith.md](references/305-frameworks-spring-boot-modulith.md).
