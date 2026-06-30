---
name: 501-frameworks-micronaut-core
description: Use when building or reviewing Micronaut applications — Micronaut.run bootstrap, @Singleton/@Prototype, @Factory beans, @ConfigurationProperties, environments, @Requires, @Controller vs services, @Scheduled, graceful shutdown, @ExecuteOn for blocking work, and Jakarta-consistent APIs. This should trigger for requests such as Review Java code for Micronaut application structure and beans; Apply best practices for Micronaut configuration, @Requires, and factories; Improve scheduling, shutdown, or threading in Micronaut services. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Micronaut Core Guidelines

Apply Micronaut core guidelines for DI, configuration, HTTP adapters, and operations.

**What is covered in this Skill?**

- Thin `main` with `Micronaut.run(Application.class, args)`
- Bean scopes: @Singleton, @Prototype; request scope only when justified
- Constructor injection with `jakarta.inject.Inject`
- @Factory for third-party or explicit bean construction
- @ConfigurationProperties (grouped settings) vs scattered @Property
- @Requires and environments instead of env branching in domain code
- Thin @Controller types delegating to @Singleton services
- @Scheduled with explicit failure visibility
- @ExecuteOn(TaskExecutors.BLOCKING) (or virtual-thread executors) for blocking I/O off the event loop
- Netty graceful shutdown properties
- AOP interceptors for cross-cutting concerns

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying Micronaut changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **PREREQUISITE**: Project must compile successfully before applying Micronaut core improvements
- **SAFETY**: If compilation fails, stop immediately — compilation failure is a blocking condition
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules, good/bad patterns, and constraints

## When to use this skill

- Review Java code for Micronaut application structure and beans
- Apply best practices for Micronaut configuration, @Requires, and factories
- Improve scheduling, shutdown, or threading in Micronaut services

## Workflow

1. **Read reference and assess project context**

Read `references/501-frameworks-micronaut-core.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/501-frameworks-micronaut-core.md](references/501-frameworks-micronaut-core.md).
