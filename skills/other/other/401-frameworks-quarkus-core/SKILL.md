---
name: 401-frameworks-quarkus-core
description: Use when building or reviewing core Quarkus applications with CDI beans and scopes, SmallRye Config and profiles, lifecycle, interceptors and events, virtual threads, and test-friendly design. This should trigger for requests such as Review Java code for Quarkus application structure and CDI; Apply best practices for Quarkus configuration and beans; Improve CDI interceptors, events, or programmatic injection in Quarkus; Add virtual-thread configuration or tune CDI lifecycle. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Quarkus Core Guidelines

Apply Quarkus core guidelines for CDI beans, configuration, profiles, and lifecycle.

**What is covered in this Skill?**

- @QuarkusMain and application entry (when custom main is needed)
- CDI scopes: @ApplicationScoped, @Singleton, @Dependent; bean disambiguation (@Default, @Alternative, @Named)
- Constructor injection with @Inject
- CDI interceptors (@Interceptor, @InterceptorBinding) for cross-cutting concerns
- CDI events: @Observes StartupEvent / ShutdownEvent, @ObservesAsync for async dispatch
- Programmatic injection with Instance<T> for dynamic bean selection
- @ConfigMapping and structured configuration with Bean Validation (@Valid)
- Profile-specific properties (%dev, %test, %prod) and @IfBuildProfile
- Startup and shutdown observers (@Startup, @PreDestroy)
- Virtual threads with @RunOnVirtualThread (Java 21+)
- Native-image safety: @RegisterForReflection, @DisabledOnNativeImage

**Scope:** Apply recommendations based on the reference rules and good/bad code examples.

## Constraints

Before applying any Quarkus changes, ensure the project compiles. If compilation fails, stop immediately. After applying improvements, run full verification.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before applying any change
- **PREREQUISITE**: Project must compile successfully before applying Quarkus core improvements
- **SAFETY**: If compilation fails, stop immediately — compilation failure is a blocking condition
- **BLOCKING CONDITION**: Compilation errors must be resolved by the user before proceeding
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying improvements
- **BEFORE APPLYING**: Read the reference for detailed rules, good/bad patterns, and constraints

## When to use this skill

- Review Java code for Quarkus application structure and CDI
- Apply best practices for Quarkus configuration and beans
- Improve CDI interceptors, events, or programmatic injection in Quarkus
- Add virtual-thread configuration or tune CDI lifecycle

## Workflow

1. **Read reference and assess project context**

Read `references/401-frameworks-quarkus-core.md` and inspect the current project setup before proposing changes.

2. **Gather scope and decide target improvements**

Identify requested outcomes, constraints, and the minimum safe set of changes to apply.

3. **Apply framework-aligned changes**

Implement or refactor configuration/code following the reference patterns and project conventions.

4. **Run verification and report results**

Execute appropriate build/tests and summarize what changed, what was verified, and any follow-up actions.

## Reference

For detailed guidance, examples, and constraints, see [references/401-frameworks-quarkus-core.md](references/401-frameworks-quarkus-core.md).
